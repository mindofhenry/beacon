# PostHog — Product Overview

## What is PostHog?
PostHog is an all-in-one developer platform for building successful products. It combines
every tool an engineering or product team needs — analytics, session replay, feature flags,
experiments, surveys, error tracking, and more — into a single platform with a shared data
layer. No stitching tools together. No syncing data between vendors. One stack.

Their ICP: high-growth startups led by product engineers. Self-serve, usage-based pricing,
open source core. Over 60,000 customers. Default alive. Aiming to IPO, not sell.

## The Full Product Suite (10+ paid products)
- **Product Analytics** — Funnels, retention, trends, user paths, cohorts, group analytics.
  SQL query builder included on all plans (competitors gate this behind paid tiers).
- **Web Analytics** — Traffic, bounce rate, UTM campaigns, content performance.
- **Session Replay** — Watch real user sessions. Includes console logs, network monitoring,
  DOM explorer, and performance metrics. 5,000 free replays/month.
- **Feature Flags** — Boolean and multivariate flags, local evaluation, payloads, targeting,
  scheduling, early access management. More mature than Mixpanel's (relaunched late 2025).
- **Experiments (A/B Testing)** — Built on feature flags. Supports primary, secondary, and
  guardrail metrics. Can use warehouse data as experiment metrics.
- **Surveys** — NPS, PMF, CSAT, open text. 1,500 free responses/month. Targeting + custom
  branding. No separate vendor needed.
- **Error Tracking** — Monitor exceptions and bugs in production code. Competitors don't
  have this natively.
- **LLM Analytics** — Track cost, latency, token usage, and output quality for AI products.
  Unique to PostHog among analytics platforms.
- **Data Warehouse** — Built-in. Import and query external data from Stripe, HubSpot,
  Zendesk, Salesforce, and more. Run SQL across product + business data in one place.
- **CDP (Customer Data Platform)** — Event ingestion, transformation, and routing.
- **AI Assistant** — Natural language querying, SQL generation, session summarization.
  Free tier: $20/month (2,000 AI credits). 20% markup over underlying LLM cost.

## Key Differentiators (what actually matters in a conversation)
1. **One platform, not five.** PostHog replaces Mixpanel (analytics) + LaunchDarkly (flags) +
   Optimizely (experiments) + FullStory (replay) + Sentry (errors) + survey tools. Customers
   who consolidate save money and stop fighting with data that doesn't sync.
2. **Built for engineers first.** Autocapture from day one. SDKs for every major language.
   SQL access on all plans. Toolbar for tagging events without code changes.
3. **Open source (MIT licensed).** Full self-hosting option. Data never leaves your infra.
   Massive differentiator for fintech, healthtech, and any company with data residency needs.
4. **Transparent, usage-based pricing.** No seat fees. No surprise bills. Billing limits per
   product. More than 90% of customers use PostHog for free.
5. **Actively cuts prices.** 2024: cut analytics events and session replay pricing. 2025: cut
   data pipelines and surveys. PostHog's stated policy is to undercut the cheapest big
   competitor for every product.
6. **HIPAA BAA available.** Single BAA covers analytics, replay, flags, experiments, and more.
   Competitors often require separate BAAs per product or only offer it on Enterprise.

## What PostHog Does NOT Do Well
- **No in-app guides or onboarding flows.** No tooltips, walkthroughs, or product tours.
  If that's a core requirement, Pendo is the right call.
- **Not built for marketers.** No multi-touch attribution or predictive analytics for
  growth/marketing teams. Amplitude has the edge there.
- **Feature flags less battle-hardened than LaunchDarkly** for large enterprise with complex
  flag governance requirements. Be honest about this when it comes up.

## Integrations
Salesforce, HubSpot, Stripe, Zendesk, Slack, Segment, Rudderstack, dbt, Snowflake,
BigQuery, Redshift, S3, and 50+ more via data pipelines.

## Stack Consolidation Story
PostHog replaces or consolidates: Mixpanel, Amplitude, Heap, FullStory, Hotjar,
LaunchDarkly, Optimizely, Statsig, Sentry (partially), Segment (partially), and
basic BI/warehouse tools. The pitch isn't "switch tools" — it's "stop paying for five
tools that don't talk to each other."
