"""
slack_bot.py — Beacon Slack Bot

Connects Beacon's knowledge base to Slack via Socket Mode.
Reps can ask questions by mentioning @Beacon or using /beacon in any channel.

Usage:
    python slack_bot.py

Requires in .env:
    SLACK_BOT_TOKEN=xoxb-...
    SLACK_APP_TOKEN=xapp-...
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Load credentials from .env
load_dotenv()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")

if not SLACK_BOT_TOKEN or not SLACK_APP_TOKEN:
    print("Error: SLACK_BOT_TOKEN and SLACK_APP_TOKEN must be set in .env")
    sys.exit(1)

# Initialise the Bolt app (token-based, no signing secret needed in Socket Mode)
app = App(token=SLACK_BOT_TOKEN)

# Reuse the same KB loader from server.py
KB_DIR = Path(__file__).parent / "knowledge_base"

def load_knowledge_base() -> str:
    """Loads all .md files from knowledge_base/ into a single string."""
    if not KB_DIR.exists():
        return "Knowledge base directory not found."
    sections = []
    for md_file in sorted(KB_DIR.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        sections.append(f"## [{md_file.stem.upper()}]\n\n{content}")
    if not sections:
        return "Knowledge base is empty."
    return "\n\n---\n\n".join(sections)


def ask_beacon(question: str) -> str:
    """
    Core answer logic — same as the MCP tool.
    Loads the KB and returns a formatted prompt string.
    In the Slack context, we call the Anthropic API directly to get
    a real answer back (not just a prompt). See query_claude() below.
    """
    kb = load_knowledge_base()
    return (
        f"You are Beacon, a rep intelligence assistant. Answer the rep's question "
        f"using ONLY the knowledge base below. Be concise, direct, and use "
        f"rep-friendly language. If the answer isn't in the KB, say so clearly.\n\n"
        f"=== KNOWLEDGE BASE ===\n{kb}\n\n"
        f"=== REP'S QUESTION ===\n{question}\n\n"
        f"=== YOUR ANSWER ==="
    )


def query_claude(question: str) -> str:
    """
    Calls the Anthropic API with the KB-grounded prompt and returns the answer.
    Requires ANTHROPIC_API_KEY in .env.
    """
    try:
        import anthropic
        client = anthropic.Anthropic()
        prompt = ask_beacon(question)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except ImportError:
        return ask_beacon(question)  # Fallback: return raw prompt if no SDK
    except Exception as e:
        return f"Beacon error: {str(e)}"

# --- Slash Command: /beacon ---
@app.command("/beacon")
def handle_beacon_command(ack, respond, command):
    """
    Handles /beacon <question> slash commands.
    ack() tells Slack we received it (required within 3 seconds).
    respond() sends the answer back — visible only to the user by default.
    """
    ack()
    question = command.get("text", "").strip()
    if not question:
        respond("Usage: `/beacon <your question>` — e.g. `/beacon how do we handle the Mixpanel objection?`")
        return

    respond(f"_Searching knowledge base..._")
    answer = query_claude(question)
    respond(f"*Beacon* :satellite:\n\n{answer}")


# --- App Mention: @Beacon <question> ---
@app.event("app_mention")
def handle_mention(event, say):
    """
    Handles messages where the bot is @mentioned.
    Strips the mention and treats the rest as the question.
    Replies in-thread so channels stay clean.
    """
    # Remove the <@BOTID> mention from the text
    text = event.get("text", "")
    # Everything after the first > is the question
    question = text.split(">", 1)[-1].strip()

    if not question:
        say(
            text="Ask me anything about the product: `/beacon <question>` or just @mention me with your question.",
            thread_ts=event.get("ts")
        )
        return

    say(text="_Searching knowledge base..._", thread_ts=event.get("ts"))
    answer = query_claude(question)
    say(text=f"*Beacon* :satellite:\n\n{answer}", thread_ts=event.get("ts"))


# --- Entry Point ---
if __name__ == "__main__":
    print("Starting Beacon Slack bot in Socket Mode...")
    print("Press Ctrl+C to stop.\n")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
