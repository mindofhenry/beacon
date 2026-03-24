# Beacon — Rep Intelligence MCP Server

Beacon is a sales rep intelligence tool built as an MCP server. It gives reps instant
access to product knowledge, objection handling, and competitive positioning — from
wherever they already work.

**The core insight: the server is the product. The interfaces are just wrappers.**

Build once, connect anywhere. Claude.ai, Slack, or any MCP-compatible client. Reps
don't open a new tool — Beacon meets them where they already are.

---

## Why This Exists

Most sales orgs have good product knowledge locked in Confluence pages, Notion docs, or
Guru cards that reps never read. When a rep hits an objection on a call or needs to know
how their product compares to a competitor, they fumble, guess, or interrupt a teammate.

The better orgs build internal tools that surface this knowledge in context. Beacon is a
portable, open version of that pattern — one any company can stand up against their own
docs in an afternoon.

> *"I saw this change how reps operate at a previous company. I understood why it worked,
> and I built a version myself."*

---

## Demo

Beacon is demoed against **PostHog** — an open-source product analytics platform with a
rich competitive landscape (vs. Mixpanel, Amplitude, Heap, FullStory, LaunchDarkly).

The knowledge base is curated GTM content written in rep language — objection handling,
competitive positioning, discovery questions, pricing scenarios. Not a docs scrape.

**Example queries:**
- *"How do we handle the objection that a prospect already uses Mixpanel?"*
- *"What's our positioning against Amplitude for an enterprise buyer?"*
- *"What discovery questions should I ask a PM persona?"*
- *"Walk me through the pricing conversation when they say it's too expensive."*


---

## Architecture

```
beacon/
├── server.py              # MCP server — exposes ask_product tool
├── knowledge_base/
│   ├── product.md         # Capabilities, integrations, technical specs
│   ├── objections.md      # Objection handling in rep language
│   ├── competitors.md     # Competitive positioning vs. 6 competitors
│   ├── personas.md        # 4 buyer profiles — pains + discovery questions
│   └── pricing.md         # Packaging, free tier, negotiation scenarios
├── ingest.py              # Rebuilds KB from any public GitHub repo or docs URL
├── .env                   # (optional) GitHub token for private repos
├── requirements.txt
└── README.md
```

**`server.py`** — FastMCP server. Exposes one tool: `ask_product`. On each call, loads
all `.md` files from `knowledge_base/` into context and returns a grounded, rep-ready
answer. No vector store — the full KB fits in context and keeps things simple.

**`ingest.py`** — The reusability layer. Point it at any company's public GitHub repo
and it rebuilds the knowledge base from real docs. This is what makes Beacon a pattern
any GTM org can adopt, not a one-off PostHog demo.

---

## Quickstart

### 1. Install dependencies

```bash
pip install mcp
```

### 2. Connect to Claude Desktop

Add to `%APPDATA%\Claude\claude_desktop_config.json` (Windows) or
`~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "beacon": {
      "command": "python",
      "args": ["/absolute/path/to/beacon/server.py"]
    }
  }
}
```

Restart Claude Desktop. Beacon will appear as a connected tool.

### 3. Ask it something

In any Claude chat:
> *"How do we handle the objection that a prospect already uses Mixpanel?"*


---

## Rebuild the Knowledge Base with ingest.py

`ingest.py` pulls markdown files from any public GitHub repo and writes them to
`knowledge_base/`. No GitHub token required for public repos.

```bash
# Dry run — see what would be downloaded without writing anything
python ingest.py https://github.com/PostHog/posthog.com \
  --path contents/docs/getting-started \
  --dry-run

# Download specific files
python ingest.py https://github.com/PostHog/posthog.com \
  --path contents/docs/getting-started \
  --files install.mdx send-events.mdx

# Pull an entire docs folder (use with care on large repos)
python ingest.py https://github.com/YourCompany/your-docs --path docs
```

**To adapt Beacon for a different product:** point `ingest.py` at your company's docs
repo, then edit the downloaded files into rep language. The server requires no changes.

**Rate limiting:** GitHub's unauthenticated API allows 60 requests/hour. For larger
ingests, add a `GITHUB_TOKEN` to `.env` and update `ingest.py` to pass it as an
`Authorization` header — this raises the limit to 5,000 requests/hour.

---

## Integrations

| Interface | Status | Notes |
|---|---|---|
| Claude Desktop / Claude.ai | ✅ Live | 3-line MCP config |
| Slack | 🚧 In progress | Slash command wrapper |
| GitHub | ✅ Live | `ingest.py` pulls from any public repo |
| Gong | 🔑 Requires API key | Official MCP support as of Oct 2025 |
| Nooks | 🔜 Roadmap | No public API yet |

---

## Knowledge Base Structure

Each file in `knowledge_base/` covers one GTM topic. Beacon loads all of them on every
query, so the rep gets answers that can draw from any section.

| File | Contents |
|---|---|
| `product.md` | Full product suite, differentiators, integrations, honest gaps |
| `objections.md` | 8 common objections with rep-language handling |
| `competitors.md` | Head-to-heads vs. Mixpanel, Amplitude, Heap, FullStory, LaunchDarkly, Pendo |
| `personas.md` | 4 buyer profiles with discovery question frameworks |
| `pricing.md` | Free tier, paid tiers, add-ons, negotiation scripts |

---

## Built By

**Henry Marble** — Former SDR at Cloudflare (BDR) and Pave. Targeting GTM Engineering
and RevOps roles.

Beacon is the second portfolio piece alongside
[DOOM Inc](https://github.com/henrymarble) — a Salesforce CRM architecture project.

The story: lived the problem as a rep, understood why the tool worked, built the pattern.
