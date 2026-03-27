"""
Beacon — Rep Intelligence MCP Server
Exposes a single tool: ask_product
Reads from the knowledge_base/ directory and answers rep questions.

Response format (always):
  CONFIDENCE: HIGH | LOW
  ANSWER: <rep-ready answer>
  BEACON_GAP: <one-sentence summary>   ← only present when CONFIDENCE is LOW
"""

from mcp.server.fastmcp import FastMCP
from pathlib import Path

# --- Setup ---
# FastMCP is the high-level interface. We give the server a name,
# which shows up when Claude or other clients connect to it.
mcp = FastMCP("Beacon")

# Path to the knowledge base folder, relative to this file
KB_DIR = Path(__file__).parent / "knowledge_base"

# --- Knowledge Base Loader ---
def load_knowledge_base() -> str:
    """
    Reads all .md files in knowledge_base/ and concatenates them.
    Each file gets a header so the model knows which section it's reading.
    Returns a single string with the full KB content.
    """
    if not KB_DIR.exists():
        return "Knowledge base directory not found."

    sections = []
    for md_file in sorted(KB_DIR.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        sections.append(f"## [{md_file.stem.upper()}]\n\n{content}")

    if not sections:
        return "Knowledge base is empty. Add .md files to the knowledge_base/ folder."

    return "\n\n---\n\n".join(sections)


# --- Tool Definition ---
@mcp.tool()
def ask_product(question: str) -> str:
    """
    Ask anything about the product: features, pricing, objections,
    competitors, or buyer personas. Returns a rep-ready answer
    grounded in the Beacon knowledge base.

    Args:
        question: The rep's question, e.g. "How do we handle the
                  'we already use Mixpanel' objection?"
    """
    kb = load_knowledge_base()

    # The prompt requires the model to declare confidence explicitly.
    # This gives downstream consumers (Slack bot, future clients) a reliable
    # signal to route on — rather than trying to detect hedging language after
    # the fact, which is fragile.
    #
    # CONFIDENCE: HIGH — KB had a clear answer. Post it and move on.
    # CONFIDENCE: LOW  — KB was thin or silent. Post what we found, offer
    #                    the source-code deep dive, and log the gap.
    return f"""You are Beacon, a rep intelligence assistant. Answer the rep's question
using ONLY the knowledge base below. Be concise, direct, and use rep-friendly language.

You MUST respond in exactly this format — no exceptions:

CONFIDENCE: HIGH or LOW
ANSWER: <your answer here>
BEACON_GAP: <one-sentence summary of what was missing>   <- include ONLY if CONFIDENCE is LOW

Rules for CONFIDENCE:
- HIGH: The knowledge base contains a clear, specific answer to this question.
- LOW: The knowledge base is silent, vague, or you are extrapolating beyond what it says.
       When LOW, still give the best answer you can from available context — do not
       just say "I don't know." Then include the BEACON_GAP line.

=== KNOWLEDGE BASE ===
{kb}

=== REP'S QUESTION ===
{question}

=== YOUR ANSWER ==="""


# --- Entry Point ---
if __name__ == "__main__":
    # transport="stdio" means Claude Desktop / Claude.ai connects via
    # standard input/output — the standard way to run a local MCP server.
    mcp.run(transport="stdio")
