# Beacon — Rep Intelligence MCP Server

Beacon is a sales rep intelligence tool built as an MCP server. It gives reps instant
access to product knowledge, objection handling, and competitive positioning — from
wherever they already work.

**The core insight: the server is the product. The interfaces are just wrappers.**

Build once, connect anywhere. Claude.ai, Slack, or any MCP-compatible client. Reps
don't open a new tool — Beacon meets them where they already are.

---

## Table of Contents
- [Why This Exists](#why-this-exists)
- [Demo](#demo)
- [Architecture](#architecture)
- [Quickstart](#quickstart)
- [Connect to Slack](#connect-to-slack)
- [Setting up #ask-beacon](#setting-up-ask-beacon)
- [Deployment](#deployment)
  - [Railway](#railway-recommended-for-getting-started)
  - [Docker](#docker-works-on-aws-gcp-azure-or-any-vps)
  - [AWS — ECS Fargate](#aws--ecs-fargate)
  - [GCP — Cloud Run](#gcp--cloud-run)
  - [Azure — Container Apps](#azure--container-apps)
- [Rebuild the Knowledge Base](#rebuild-the-knowledge-base-with-ingestpy)
- [Knowledge Base Structure](#knowledge-base-structure)
- [Integrations](#integrations)
- [Built By](#built-by)

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
├── slack_bot.py           # Slack bot — channel-native, no slash commands needed
├── llm.py                 # LLM provider abstraction (Anthropic, OpenAI, Gemini)
├── knowledge_base/
│   ├── product.md         # Capabilities, integrations, technical specs
│   ├── objections.md      # Objection handling in rep language
│   ├── competitors.md     # Competitive positioning vs. 6 competitors
│   ├── personas.md        # 4 buyer profiles — pains + discovery questions
│   ├── pricing.md         # Packaging, free tier, negotiation scenarios
│   └── hex-dashboards.md  # Approved Hex dashboards with links and context
├── ingest.py              # Rebuilds KB from any public GitHub repo or docs URL
├── Procfile               # Railway/Heroku deployment
├── railway.toml           # Railway config
├── Dockerfile             # Container deployment (AWS, GCP, Azure)
├── .dockerignore
├── .env.example           # Required environment variables
├── requirements.txt
└── README.md
```

**`server.py`** — FastMCP server. Exposes one tool: `ask_product`. On each call, loads
all `.md` files from `knowledge_base/` into context and returns a grounded, rep-ready
answer. No vector store — the full KB fits in context and keeps things simple.

**`slack_bot.py`** — Channel-native Slack bot. Reps ask questions directly in
#ask-beacon — no slash commands or @mentions needed for the original asker. Answers
are edited in-place for a clean UX. Unanswered questions are logged to #beacon-gaps
and optionally to Notion.

**`llm.py`** — Provider abstraction layer. Set `LLM_PROVIDER` in `.env` to switch
between Anthropic Claude, OpenAI GPT, or Google Gemini. No other code changes needed.

**`ingest.py`** — The reusability layer. Point it at any company's public GitHub repo
and it rebuilds the knowledge base from real docs. This is what makes Beacon a pattern
any GTM org can adopt, not a one-off PostHog demo.

---
## Quickstart

### 1. Install dependencies

```bash
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

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

---
## Setting up #ask-beacon

Beacon is designed to live in a dedicated channel where the whole team learns together.
One rep asks, everyone sees the answer.

### How it works

- **Top-level message in #ask-beacon** → Beacon always responds, no mention needed
- **Thread reply from the original asker** → Beacon responds without mention
- **Thread reply from a different user** → must @Beacon to get a response
- **Any other channel** → Beacon redirects to #ask-beacon
- **DMs** → reps can DM Beacon directly for private questions

### Setup steps

1. Create a `#ask-beacon` channel in your Slack workspace
2. Create a `#beacon-gaps` private channel for unanswered question logging
3. Invite the Beacon bot to both: `/invite @Beacon`
4. Set `ASK_BEACON_CHANNEL_ID` and `BEACON_GAPS_CHANNEL_ID` in your `.env`
5. Optionally set `ENABLEMENT_URL` to link reps to existing materials when Beacon
   can't answer

### Getting channel IDs

Right-click the channel name in Slack → **View channel details** → copy the ID at
the bottom of the panel (starts with `C`).

### Knowledge gaps

When Beacon can't answer a question it:
1. Tells the rep honestly and points them to your enablement materials
2. Posts the unanswered question to `#beacon-gaps` with a link to the thread
3. Optionally logs it to a Notion database for the team to action

This makes your knowledge gaps visible and actionable rather than silent.

---
## Deployment

Beacon runs as a persistent worker process. No HTTP port required —
Socket Mode means the bot dials out to Slack, not the other way around.

Set these environment variables wherever you deploy:
- `SLACK_BOT_TOKEN`
- `SLACK_APP_TOKEN`
- `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY` / `GOOGLE_API_KEY` depending on provider)
- `LLM_PROVIDER` — `anthropic` (default), `openai`, or `google`
- `ASK_BEACON_CHANNEL_ID`
- `BEACON_GAPS_CHANNEL_ID`
- `ENABLEMENT_URL` (optional)
- `NOTION_API_KEY` and `NOTION_DATABASE_ID` (optional)

---

### Railway (recommended for getting started)

1. Fork this repo
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select your fork
4. Add environment variables under Variables
5. Railway detects the `Procfile` automatically and deploys

Free tier includes $5/month credit — enough for light usage.

---

### Docker (works on AWS, GCP, Azure, or any VPS)

Build and run locally to verify:

```bash
docker build -t beacon .
docker run --env-file .env beacon
```

Then push to any container registry and deploy from there.

---

### AWS — ECS Fargate

1. Push your image to ECR:
```bash
aws ecr create-repository --repository-name beacon
docker tag beacon:latest <your-ecr-url>/beacon:latest
docker push <your-ecr-url>/beacon:latest
```
2. Create an ECS cluster → New Task Definition → Fargate
3. Set the container image to your ECR URL
4. Add environment variables under Environment Variables
5. Run as a Service with 1 desired task — no load balancer needed

Estimated cost: ~$5–10/month on the smallest Fargate config (0.25 vCPU, 0.5GB RAM).

---

### GCP — Cloud Run

> **Note:** Cloud Run scales to zero when idle — the bot goes offline between messages
> without `--min-instances 1`. A small Compute Engine e2-micro VM (free tier eligible)
> is simpler for an always-on setup.

```bash
gcloud run deploy beacon \
  --image gcr.io/<your-project>/beacon \
  --set-env-vars SLACK_BOT_TOKEN=...,SLACK_APP_TOKEN=...,ANTHROPIC_API_KEY=... \
  --no-allow-unauthenticated \
  --min-instances 1
```

---

### Azure — Container Apps

```bash
az containerapp create \
  --name beacon \
  --resource-group <your-rg> \
  --image <your-registry>/beacon:latest \
  --min-replicas 1 \
  --env-vars \
      SLACK_BOT_TOKEN=secretref:slack-bot-token \
      SLACK_APP_TOKEN=secretref:slack-app-token \
      ANTHROPIC_API_KEY=secretref:anthropic-api-key
```

Set secrets first via `az containerapp secret set`. The `--min-replicas 1` flag
keeps the container alive — without it the bot goes to sleep between messages.

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
`Authorization` header — raises the limit to 5,000 requests/hour.

---

## Knowledge Base Structure

Each file in `knowledge_base/` covers one GTM topic. Beacon loads all of them on every
query so answers can draw from any section.

| File | Contents |
|---|---|
| `product.md` | Full product suite, differentiators, integrations, honest gaps |
| `objections.md` | 8 common objections with rep-language handling |
| `competitors.md` | Head-to-heads vs. Mixpanel, Amplitude, Heap, FullStory, LaunchDarkly, Pendo |
| `personas.md` | 4 buyer profiles with discovery question frameworks |
| `pricing.md` | Free tier, paid tiers, add-ons, negotiation scripts |
| `hex-dashboards.md` | Approved Hex dashboards with links and context for when to use them |

---

## Integrations

| Interface | Status | Notes |
|---|---|---|
| Anthropic Claude | ✅ Live | Default LLM provider |
| OpenAI GPT-4o | ✅ Live | Set `LLM_PROVIDER=openai` in .env |
| Google Gemini | ✅ Live | Set `LLM_PROVIDER=google` in .env |
| Claude Desktop / Claude.ai | ✅ Live | 3-line MCP config |
| Slack (#ask-beacon) | ✅ Live | Channel-native, no slash commands needed |
| Railway | ✅ Live | Auto-deploys via Procfile |
| Docker / AWS / GCP / Azure | ✅ Live | Single Dockerfile, deploy anywhere |
| Hex | ✅ Live | Approved dashboards indexed in knowledge base |
| Notion | ✅ Live | Gap logging to a Notion database |
| Gong | 🔑 Requires API key | Official MCP support as of Oct 2025 |
| Nooks | 🔜 Roadmap | No public API yet |

---

## Built By

**Henry Marble** — Former SDR at Cloudflare (BDR) and Pave. Targeting GTM Engineering
and RevOps roles.

Beacon is the second portfolio piece alongside
[DOOM Inc](https://github.com/mindofhenry) — a Salesforce CRM architecture project.

The story: lived the problem as a rep, understood why the tool worked, built the pattern.
