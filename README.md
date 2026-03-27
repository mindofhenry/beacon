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

> **Want to see Beacon fully loaded?** Check out the [`posthog-demo`](https://github.com/mindofhenry/beacon/tree/posthog-demo) branch — a complete implementation built around [PostHog](https://posthog.com), an open-source product analytics platform. It includes curated GTM content covering objection handling, competitive positioning (vs. Mixpanel, Amplitude, Heap, FullStory, LaunchDarkly), buyer personas, and pricing — all written in rep language, not docs scraped.

This `main` branch is the **blank template**. Clone it, point `ingest.py` at your own docs repo, fill in the knowledge base files, and you have a rep intelligence tool tailored to your product in an afternoon.


---

## Architecture

```
beacon/
├── server.py              # MCP server — exposes ask_product tool
├── slack_bot.py           # Slack bot — channel-native, no slash commands needed
├── llm.py                 # LLM provider abstraction (Anthropic, OpenAI, Gemini)
├── knowledge_base/
│   ├── product.md         # Capabilities, integrations, technical specs
│   ├── objections.md      # Objection handling in rep language
│   ├── competitors.md     # Competitive positioning
│   ├── personas.md        # Buyer profiles — pains + discovery questions
│   └── pricing.md         # Packaging, free tier, negotiation scenarios
├── ingest.py              # Rebuilds KB from any public GitHub repo or docs URL
├── .env.example           # Required environment variables
├── requirements.txt
└── README.md
```

**`server.py`** — FastMCP server. Exposes one tool: `ask_product`. On each call, loads
all `.md` files from `knowledge_base/` into context and returns a structured response:
`CONFIDENCE: HIGH/LOW`, `ANSWER:`, and `BEACON_GAP:` when confidence is low. No vector
store — the full KB fits in context and keeps things simple.

**`slack_bot.py`** — Channel-native Slack bot. Reps ask questions directly in
`#ask-beacon` — no slash commands or @mentions needed for the original asker. Answers
are edited in-place for a clean UX. When confidence is low, Beacon posts its best answer
with a caveat and offers an opt-in source-code deep dive. Gaps are logged to
`#beacon-gaps` and optionally to Notion regardless of whether the rep takes the deep dive.

**`llm.py`** — Provider abstraction layer. Set `LLM_PROVIDER` in `.env` to switch
between Anthropic Claude, OpenAI GPT, or Google Gemini. No other code changes needed.

**`ingest.py`** — The reusability layer. Point it at any company's public GitHub repo
and it rebuilds the knowledge base from real docs. This is what makes Beacon a pattern
any GTM org can adopt, not a one-off demo.

---

## Quickstart

### 1. Install dependencies

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
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

## Connect to Slack

Beacon runs as a Slack bot using Socket Mode — no public URL required.

### 1. Create a Slack App

Go to [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **From scratch**.

### 2. Configure permissions

Under **OAuth & Permissions → Scopes → Bot Token Scopes**, add:
- `app_mentions:read` — detect @Beacon mentions
- `chat:write` — post and edit messages
- `channels:history` — read thread history to identify the original asker
- `groups:history` — same, for private channels

Under **Socket Mode**, enable it and generate an **App-Level Token** with
`connections:write` scope. This is your `SLACK_APP_TOKEN` (`xapp-...`).

### 3. Enable Event Subscriptions

Under **Event Subscriptions**, enable and subscribe to the following under **Bot Events**:
- `message.channels` — listens for messages in public channels
- `message.groups` — listens for messages in private channels
- `app_mention` — handles @Beacon mentions outside #ask-beacon

### 4. Install the app and get tokens

**Install App** → copy the **Bot User OAuth Token** (`xoxb-...`). This is your `SLACK_BOT_TOKEN`.

### 5. Add credentials to .env

```bash
cp .env.example .env
# Fill in all variables — see .env.example for the full list
```

### 6. Run the bot

```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

python slack_bot.py
```

### How it works

- **Top-level message in #ask-beacon** → Beacon always responds, no mention needed
- **Thread reply from the original asker** → Beacon responds without mention
- **Thread reply from a different user** → must @Beacon to get a response
- **Any other channel** → Beacon redirects to #ask-beacon

### Knowledge gaps and low-confidence answers

Beacon uses a two-tier response system:

**High confidence** — KB had a clear answer. Beacon posts it cleanly and moves on.

**Low confidence** — KB was thin or the question went beyond what's in the docs. Beacon:
1. Posts its best answer with an honest caveat: *"I'm not fully confident in this"*
2. Offers the rep an opt-in source-code deep dive: *"Reply `yes` if you want me to search deeper"*
3. Logs the gap to `#beacon-gaps` — regardless of whether the rep takes the deep dive

This keeps reps unblocked immediately while making knowledge gaps visible and actionable.

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
| Anthropic Claude | ✅ Live | Default LLM provider |
| OpenAI GPT-4o | ✅ Live | Set `LLM_PROVIDER=openai` in .env |
| Google Gemini | ✅ Live | Set `LLM_PROVIDER=google` in .env |
| Claude Desktop / Claude.ai | ✅ Live | 3-line MCP config |
| Slack (#ask-beacon) | ✅ Live | Channel-native, no slash commands needed |
| GitHub | ✅ Live | `ingest.py` pulls from any public repo |
| Notion | ✅ Live | Gap logging to a Notion database |
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
