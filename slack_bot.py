"""
slack_bot.py — Beacon Slack Bot

Channel-native rep intelligence. No slash commands needed in #ask-beacon.

Behavior:
  - #ask-beacon top-level message → Beacon always responds
  - Thread reply from original asker → Beacon responds without mention
  - Thread reply from different user → Beacon only responds if @mentioned
  - Any other channel → ignored (slash commands removed)
  - Unknown question → tells rep, points to enablement, logs to #beacon-gaps
  - Optional: logs gaps to Notion (or any external destination)

Requires in .env:
  SLACK_BOT_TOKEN=xoxb-...
  SLACK_APP_TOKEN=xapp-...
  ANTHROPIC_API_KEY=sk-ant-...
  ASK_BEACON_CHANNEL_ID=C...       # Channel ID of #ask-beacon
  BEACON_GAPS_CHANNEL_ID=C...      # Channel ID of #beacon-gaps (private)
  NOTION_API_KEY=secret_...        # Optional — for Notion gap logging
  NOTION_DATABASE_ID=...           # Optional — Notion DB to log gaps into
  ENABLEMENT_URL=https://...       # Link to your enablement materials
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# --- Load .env ---
_env_path = Path(__file__).parent / ".env"
if _env_path.exists():
    for line in _env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip())

SLACK_BOT_TOKEN        = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN        = os.environ.get("SLACK_APP_TOKEN")
ASK_BEACON_CHANNEL_ID  = os.environ.get("ASK_BEACON_CHANNEL_ID")
BEACON_GAPS_CHANNEL_ID = os.environ.get("BEACON_GAPS_CHANNEL_ID")
ENABLEMENT_URL         = os.environ.get("ENABLEMENT_URL", "")
NOTION_API_KEY         = os.environ.get("NOTION_API_KEY")
NOTION_DATABASE_ID     = os.environ.get("NOTION_DATABASE_ID")

if not SLACK_BOT_TOKEN or not SLACK_APP_TOKEN:
    print("Error: SLACK_BOT_TOKEN and SLACK_APP_TOKEN must be set in .env")
    sys.exit(1)

if not ASK_BEACON_CHANNEL_ID:
    print("Error: ASK_BEACON_CHANNEL_ID must be set in .env")
    print("Tip: Right-click #ask-beacon in Slack → View channel details → copy the ID at the bottom")
    sys.exit(1)

app = App(token=SLACK_BOT_TOKEN)

BOT_USER_ID = None

def get_bot_user_id():
    global BOT_USER_ID
    if BOT_USER_ID is None:
        result = app.client.auth_test()
        BOT_USER_ID = result["user_id"]
    return BOT_USER_ID


# --- Knowledge Base ---

KB_DIR = Path(__file__).parent / "knowledge_base"

def load_knowledge_base() -> str:
    if not KB_DIR.exists():
        return "Knowledge base directory not found."
    sections = []
    for md_file in sorted(KB_DIR.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        sections.append(f"## [{md_file.stem.upper()}]\n\n{content}")
    if not sections:
        return "Knowledge base is empty."
    return "\n\n---\n\n".join(sections)


# --- LLM ---

from llm import query_llm

def query_llm_with_kb(question: str) -> str:
    """Builds the KB-grounded prompt and queries the configured LLM provider."""
    kb = load_knowledge_base()
    prompt = (
        f"You are Beacon, a rep intelligence assistant. Answer the rep's question "
        f"using ONLY the knowledge base below. Be concise, direct, and use "
        f"rep-friendly language.\n\n"
        f"IMPORTANT: If the answer is not in the knowledge base, you MUST respond "
        f"with exactly this prefix on the first line: BEACON_GAP: "
        f"followed by a one-sentence summary of what was asked. "
        f"Then on a new line, write a polite message to the rep explaining you don't "
        f"have that answer yet and that you've flagged it for the team.\n\n"
        f"=== KNOWLEDGE BASE ===\n{kb}\n\n"
        f"=== REP'S QUESTION ===\n{question}\n\n"
        f"=== YOUR ANSWER ==="
    )
    return query_llm(prompt)


def parse_response(raw: str, question: str, asker: str) -> tuple[str, bool, str | None]:
    """
    Parses the LLM response.
    Returns:
      - message to post in Slack (str)
      - is_gap (bool) — whether to trigger gap logging
      - gap_summary (str | None) — one-liner for the gap log
    """
    if raw.startswith("BEACON_GAP:"):
        lines = raw.split("\n", 1)
        gap_summary = lines[0].replace("BEACON_GAP:", "").strip()
        rep_message = lines[1].strip() if len(lines) > 1 else "I don't have an answer for that one yet — I've flagged it for the team."

        enablement_note = (
            f"\n\nIn the meantime, you may find something useful in the "
            f"<{ENABLEMENT_URL}|enablement materials>." if ENABLEMENT_URL else ""
        )

        slack_message = (
            f"*Beacon* :satellite:\n\n"
            f"{rep_message}"
            f"{enablement_note}"
        )
        return slack_message, True, gap_summary

    return f"*Beacon* :satellite:\n\n{raw}", False, None


# --- Gap Logging ---

def log_gap_to_slack(question: str, gap_summary: str, asker: str, thread_url: str):
    """Posts an unanswered question to #beacon-gaps."""
    if not BEACON_GAPS_CHANNEL_ID:
        return
    try:
        app.client.chat_postMessage(
            channel=BEACON_GAPS_CHANNEL_ID,
            text=(
                f":warning: *Knowledge gap detected*\n\n"
                f"*Asked by:* <@{asker}>\n"
                f"*Question:* {question}\n"
                f"*Gap summary:* {gap_summary}\n"
                f"*Thread:* {thread_url}\n"
                f"*Time:* {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
            )
        )
    except Exception as e:
        print(f"[Beacon] Failed to log gap to Slack: {e}")


def log_gap_to_notion(question: str, gap_summary: str, asker: str, thread_url: str):
    """
    Logs an unanswered question to a Notion database.
    Requires NOTION_API_KEY and NOTION_DATABASE_ID in .env.

    Expected Notion DB properties:
      - Question (title)
      - Gap Summary (rich_text)
      - Asked By (rich_text)
      - Thread URL (url)
      - Date (date)
      - Status (select) — suggested options: "New", "In Progress", "Resolved"

    To swap for a different destination (Confluence, Google Sheets, webhook):
    replace this function's body. The signature and call site stay the same.
    """
    if not NOTION_API_KEY or not NOTION_DATABASE_ID:
        return
    try:
        import urllib.request
        payload = {
            "parent": {"database_id": NOTION_DATABASE_ID},
            "properties": {
                "Question": {
                    "title": [{"text": {"content": question[:200]}}]
                },
                "Gap Summary": {
                    "rich_text": [{"text": {"content": gap_summary}}]
                },
                "Asked By": {
                    "rich_text": [{"text": {"content": asker}}]
                },
                "Thread URL": {
                    "url": thread_url
                },
                "Date": {
                    "date": {"start": datetime.now(timezone.utc).strftime("%Y-%m-%d")}
                },
                "Status": {
                    "select": {"name": "New"}
                }
            }
        }
        req = urllib.request.Request(
            "https://api.notion.com/v1/pages",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {NOTION_API_KEY}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"
            },
            method="POST"
        )
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"[Beacon] Failed to log gap to Notion: {e}")


def log_gap(question: str, gap_summary: str, asker: str, channel: str, thread_ts: str):
    """
    Central gap logging dispatcher.
    Add new destinations here — each is a separate function call.
    """
    # Build a link to the Slack thread
    # Format: https://slack.com/archives/CHANNEL_ID/pTHREAD_TS
    thread_url = f"https://slack.com/archives/{channel}/p{thread_ts.replace('.', '')}"

    log_gap_to_slack(question, gap_summary, asker, thread_url)
    log_gap_to_notion(question, gap_summary, asker, thread_url)
    # log_gap_to_webhook(...)   # add more destinations here


# --- Core Response Handler ---

def handle_question(client, channel: str, thread_ts: str, question: str, asker: str):
    """
    Posts an acknowledgment, gets the answer, then edits the message in place.
    This is the single entry point for all question handling.
    """
    # Post acknowledgment — this is the message we'll edit
    result = client.chat_postMessage(
        channel=channel,
        thread_ts=thread_ts,
        text=":hourglass_flowing_sand: Great question — let me check that for you..."
    )
    ack_ts = result["ts"]

    # Get the answer
    raw = query_llm_with_kb(question)
    slack_message, is_gap, gap_summary = parse_response(raw, question, asker)

    # Edit the acknowledgment message with the answer
    client.chat_update(
        channel=channel,
        ts=ack_ts,
        text=slack_message
    )

    # Log the gap if needed
    if is_gap and gap_summary:
        log_gap(question, gap_summary, asker, channel, thread_ts)


# --- Thread Helper ---

def get_thread_starter(client, channel: str, thread_ts: str) -> str | None:
    """
    Returns the user ID of whoever posted the first message in a thread.
    Used to decide whether a reply needs an @mention to trigger Beacon.
    """
    try:
        result = client.conversations_replies(channel=channel, ts=thread_ts, limit=1)
        messages = result.get("messages", [])
        if messages:
            return messages[0].get("user")
    except Exception:
        pass
    return None


# --- Event: Top-level message in #ask-beacon ---

@app.event("message")
def handle_message(event, client):
    """
    Listens for all messages. Handles two cases:

    1. Top-level message in #ask-beacon → always respond
    2. Thread reply in #ask-beacon:
       - Original asker → respond without mention
       - Anyone else → only respond if @Beacon mentioned
    """
    # Ignore bot messages
    if event.get("bot_id") or event.get("subtype") == "bot_message":
        return

    channel  = event.get("channel")
    text     = event.get("text", "").strip()
    user     = event.get("user")
    ts       = event.get("ts")
    thread_ts = event.get("thread_ts")

    # Only operate in #ask-beacon
    if channel != ASK_BEACON_CHANNEL_ID:
        return

    bot_id = get_bot_user_id()

    # --- Case 1: Top-level message ---
    if not thread_ts or thread_ts == ts:
        # Ignore empty messages
        if not text:
            return
        # Use the message's own ts as the thread root
        handle_question(client, channel, ts, text, user)
        return

    # --- Case 2: Thread reply ---
    mentioned = f"<@{bot_id}>" in text

    # Get the thread starter
    thread_starter = get_thread_starter(client, channel, thread_ts)
    is_original_asker = (user == thread_starter)

    if is_original_asker:
        # Original asker can just reply — no mention needed
        # Strip any @mention if they did include one, avoid double-processing
        question = text.replace(f"<@{bot_id}>", "").strip()
        if question:
            handle_question(client, channel, thread_ts, question, user)
    elif mentioned:
        # Different user must @mention Beacon
        question = text.replace(f"<@{bot_id}>", "").strip()
        if question:
            handle_question(client, channel, thread_ts, question, user)
    # else: different user, no mention — ignore silently


# --- App Mention fallback (outside #ask-beacon) ---

@app.event("app_mention")
def handle_mention_outside_channel(event, say):
    """
    If someone @mentions Beacon outside #ask-beacon, redirect them politely.
    """
    channel = event.get("channel")
    if channel == ASK_BEACON_CHANNEL_ID:
        # Already handled by handle_message above
        return

    thread_ts = event.get("thread_ts") or event.get("ts")
    say(
        text=(
            f"Hey! I'm only active in <#{ASK_BEACON_CHANNEL_ID}>. "
            f"Head over there and ask your question — "
            f"your teammates will see the answer too. :satellite:"
        ),
        thread_ts=thread_ts
    )


# --- Entry Point ---

if __name__ == "__main__":
    print("Starting Beacon...")
    print(f"  Listening in channel: {ASK_BEACON_CHANNEL_ID}")
    print(f"  Gap logging channel:  {BEACON_GAPS_CHANNEL_ID or 'not set'}")
    print(f"  Notion logging:       {'enabled' if NOTION_API_KEY else 'disabled'}")
    print("\nPress Ctrl+C to stop.\n")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()