# PostHog — Buyer Personas

## Persona 1: The Product Engineer / Engineering Lead
**Title:** Senior Engineer, Staff Engineer, Engineering Manager, CTO (seed–Series B)
**Company profile:** 20–200 person startup, engineering-led culture, shipping fast
**Core pain:** Fragmented stack. They're managing 4–6 tools that don't share a data model.
Switching between Mixpanel, LaunchDarkly, Sentry, and Hotjar to answer one question.
**What they care about:** SDK quality, autocapture, SQL access, self-hosting option, not
being locked into a black box, not babysitting integrations between tools.
**Buying trigger:** Hit a scaling pain with current stack, new hire pushing for consolidation,
or evaluating stack for a new product build.
**Discovery questions:**
- "Who owns analytics instrumentation on your team — product or eng?"
- "How many tools are you running for analytics, flags, and replay right now?"
- "Are you self-hosting anything, or all SaaS?"
- "When you hit a bug in production, what's your workflow for going from alert to session replay?"
- "Do you have feature flags in place? What tool?"
**Pitch angle:** One platform, one data model, open source, SQL on everything.

## Persona 2: The Product Manager
**Title:** PM, Senior PM, Head of Product (mid-size startup or growth-stage)
**Company profile:** Series B–D, dedicated product team, analytics is a daily workflow
**Core pain:** Can't get answers fast enough. Has to wait on data team or engineering for
custom queries. Wants self-serve. Current tool (often Mixpanel or Amplitude) gates advanced
features behind expensive tiers.
**What they care about:** Self-serve insight building, funnel visualization, NPS/surveys,
session replay to understand where users get stuck, A/B testing to validate decisions.
**Discovery questions:**
- "How long does it take you to answer 'why did activation drop last week'?"
- "Are you running A/B tests today? What tool and how's the process?"
- "Do you have session replay? Is it connected to your analytics data?"
- "Who has SQL access on your team? Is that a bottleneck?"
- "Are you running NPS or PMF surveys anywhere?"
**Pitch angle:** SQL on free tier. Surveys built in. Replay connected to funnel data.
No waiting on engineering for advanced analysis.

## Persona 3: The Data / Growth Engineer
**Title:** Data Engineer, Analytics Engineer, Growth Engineer, Head of Data (Series B–D)
**Company profile:** Has a data warehouse (Snowflake, BigQuery), uses dbt, cares about
data integrity and source of truth.
**Core pain:** Product events are inconsistent and hard to trust. Analytics tools don't
connect to the warehouse cleanly. Feature flag data never makes it into their models.
**What they care about:** Warehouse integration, dbt compatibility, SQL access, data pipelines
that are reliable, ability to use warehouse data as experiment metrics.
**Discovery questions:**
- "Are you sending product events to a warehouse today? What's the pipeline?"
- "What does your current data stack look like — Snowflake, BigQuery, Redshift?"
- "How do you handle feature flag data in your analytics today? Does it make it into dbt?"
- "Do you have a single source of truth for product + business data, or is it stitched?"
- "Are you running any experiments? How do you measure results?"
**Pitch angle:** Built-in data warehouse + CDP. Use Stripe and HubSpot data as experiment
metrics directly in PostHog. Warehouse connectors for Snowflake/BigQuery. dbt-compatible.

## Persona 4: The Compliance-Conscious Buyer (Fintech / Healthtech)
**Title:** CTO, VP Engineering, Head of Security/Compliance at regulated company
**Company profile:** Handles PII, PHI, or financial data. Legal/compliance team is involved
in tooling decisions. EU data residency or HIPAA may be requirements.
**Core pain:** Most analytics vendors are a non-starter because of data residency or
compliance requirements. Building internal tools is expensive.
**What they care about:** Self-hosting option, HIPAA BAA, data residency (EU options),
SOC 2 certification, no PII in third-party systems.
**Discovery questions:**
- "What compliance standards are you operating under — HIPAA, GDPR, SOC 2, PCI?"
- "Does your current analytics vendor have a BAA in place?"
- "Do you have requirements around where data is stored geographically?"
- "Is self-hosting something you've considered, or does cloud work if compliance is met?"
**Pitch angle:** MIT licensed, fully self-hostable. HIPAA BAA covers the full platform
(one BAA vs. multiple vendor BAAs). EU data residency available. SOC 2 certified.

## Shared Discovery Framework (use across all personas)
**Qualify the stack first:**
"Walk me through what your current analytics/tooling stack looks like — what are you
using for analytics, feature flags, session replay, and A/B testing?"

**Find the pain:**
"What's the thing your current setup doesn't do that you wish it did?"

**Understand the buyer:**
"Who else is involved in evaluating or deciding on tooling changes?"

**Size the opportunity:**
"Roughly how many monthly active users are you tracking? Do you know your current
event volume?"
