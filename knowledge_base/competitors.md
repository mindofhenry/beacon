# PostHog — Competitive Positioning

## PostHog vs. Mixpanel
**Summary:** Analytics peers, but PostHog is a broader platform.

- Both: product analytics, session replay, feature flags, A/B testing (Mixpanel relaunched
  experimentation in late 2025 after deprecating it). Both support group analytics, warehouse
  connectors, and autocapture.
- **PostHog adds:** error tracking, LLM analytics, surveys (1,500 free/month vs. Mixpanel
  has none natively), built-in data warehouse with SQL on Stripe/HubSpot/Zendesk data.
- **Mixpanel's edge:** More polished UI for non-technical PMs. Longer-running product.
  Good startup program (free first year, up to 1B events). Strong for teams that only need
  analytics and don't want the broader platform.
- **Feature flags nuance:** Mixpanel's flags are newer and less mature. PostHog has local
  evaluation, bootstrapping, early access management, and scheduling. Mixpanel experiments
  is an Enterprise add-on; PostHog includes it with flags.
- **Pricing:** Both usage-based/event-based. PostHog's free tier is larger (1M events + 5K
  replays + unlimited flags vs. Mixpanel's 1M events with credit card on file).
- **Win angle:** "5 tools vs. 1. One data model. Cheaper at scale."

## PostHog vs. Amplitude
**Summary:** Amplitude for enterprise/marketing; PostHog for engineering-led teams.

- Amplitude is analytics-first with a strong enterprise motion: warehouse-native queries,
  advanced data governance, multi-touch attribution, predictive analytics, AI brand visibility.
  Built for large teams with dedicated data scientists.
- **PostHog adds:** error tracking, LLM analytics, open source/self-hosting, lower price
  with self-serve. Advanced analytics features (SQL, custom formulas, group analytics) on
  the free tier — Amplitude gates many behind paid plans.
- **Amplitude's edge:** Warehouse-native queries running directly in Snowflake/BigQuery.
  More mature for non-technical teams. Better for marketing and growth use cases. Pricing
  requires contacting sales (can be expensive).
- **Win angle:** Engineering-led teams at Series A–C startups where Amplitude is overkill
  and cost is a factor. Also: "PostHog free tier has SQL access. Amplitude doesn't."

## PostHog vs. Heap
**Summary:** PostHog is the most direct like-for-like Heap alternative.

- Both support autocapture (Heap's is more comprehensive — records everything by default,
  retroactive visual event editor). PostHog's toolbar lets you tag events without code too,
  but only on web.
- **PostHog adds:** Feature flags, A/B testing, surveys, error tracking, LLM analytics.
  Session replay with developer tooling (console logs, network monitoring, DOM explorer,
  performance metrics) — Heap's replay is simpler and lacks these debugging tools.
  Built-in data warehouse with SQL vs. Heap's "Sources" integrations (queries stay in Heap).
- **Heap situation:** Acquired by Contentsquare in September 2023. Roadmap uncertainty.
  Contentsquare is focused on marketing/e-commerce analytics — a different buyer than Heap's
  core product manager audience.
- **Win angle:** "Same autocapture plus everything Heap doesn't do — flags, experiments,
  error tracking. And PostHog is independent with a clear roadmap."

## PostHog vs. FullStory
- FullStory is session replay-first. Strong on qualitative UX research: frustration signals,
  AI session summaries (StoryAI), in-app guides.
- **PostHog's replay** includes console logs, network monitoring, DOM explorer, and
  performance metrics — better for engineers debugging. FullStory is better for dedicated
  UX research teams.
- FullStory has no feature flags, A/B testing, or error tracking natively.
- All FullStory pricing requires contacting sales. PostHog free tier includes 5K replays.
- **Win angle:** "If UX research is your primary use case and you have enterprise budget,
  FullStory is excellent. If you need replay plus the dev stack, PostHog is cheaper and
  covers more ground."

## PostHog vs. LaunchDarkly
- LaunchDarkly is best-in-class for enterprise feature flag governance: complex targeting,
  audit logs, approval workflows, RBAC.
- **PostHog's flags** are solid for most teams: boolean/multivariate, local evaluation,
  payloads, targeting, scheduling, early access management.
- **Where PostHog wins:** Integrated data model — use analytics data as experiment metrics
  without exporting. One platform for flags + analytics + experiments.
- **Where LaunchDarkly wins:** Large enterprise with dedicated platform team, complex flag
  governance requirements, regulatory audit trails.
- **Be honest:** If they're a large enterprise asking specifically about flag governance,
  LaunchDarkly may genuinely be right for flags. PostHog wins on the overall stack.

## PostHog vs. Pendo
- Pendo = product analytics + in-app guides (tooltips, walkthroughs, banners) + surveys.
  Strong for product managers focused on adoption and onboarding.
- **PostHog has no in-app guide builder.** This is a real gap. If no-code in-app guidance
  is a core requirement, Pendo is the better call. Don't oversell.
- **PostHog wins on:** error tracking, LLM analytics, open source, developer tooling, and
  price. Pendo pricing is seat-based and expensive at scale.
- **Win angle:** "If in-app guides are a must-have, Pendo wins there. If you want analytics,
  flags, replay, and error tracking without the seat-based pricing, PostHog is the call."
