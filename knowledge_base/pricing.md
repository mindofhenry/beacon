# PostHog — Pricing & Packaging

## The Model
Usage-based. No seat fees. No monthly minimums. You pay for data ingested — events,
recordings, flag requests, survey responses. Every product has its own billing line.
Set a billing limit per product so you never get an unexpected bill.

PostHog's stated pricing philosophy: undercut the cheapest significant competitor for
every product. They've cut prices multiple times (analytics + replay in 2024, pipelines +
surveys in 2025). This is a real differentiator to use in conversation.

## Free Tier (always free, no credit card required)
- **Product Analytics:** 1,000,000 events/month
- **Session Replay:** 5,000 recordings/month
- **Feature Flags:** Unlimited (first 1M requests free)
- **Experiments:** Unlimited (billed with flags)
- **Surveys:** 1,500 responses/month
- **Error Tracking:** 5,000 exceptions/month
- **Web Analytics:** 1,000,000 events/month
- **AI credits:** $20/month free (2,000 credits — natural language queries, SQL gen, etc.)

**Key point:** More than 90% of PostHog customers never pay anything. Lead with this.

## Paid Pricing (approximate — always direct to posthog.com/pricing for current rates)
Usage scales with volume and discounts kick in at higher tiers.
- **Analytics events:** ~$0.000225/event beyond free tier
- **Session replay:** ~$0.005/recording beyond free tier
- **Feature flags:** Priced per request beyond free tier
- **Surveys:** Per response beyond free tier

Typical paid ranges by stage:
- Early-stage startup (500K MAU, moderate usage): $200–$800/month
- Growth-stage (2–5M events/month): $500–$2,000/month
- Scale-up: Custom/negotiated

## Platform Add-Ons (Boost, Scales, Enterprise)
These are organization-level add-ons on top of usage:
- **Boost:** White labeling, HIPAA BAA, unlimited projects, SSO enforcement
- **Scales:** RBAC, priority support, SAML
- **Enterprise:** Dedicated account manager via Slack/email, training, custom MSA,
  custom pricing, invoice billing

## Self-Hosted (Open Source)
- MIT licensed — free forever
- Full feature set, community support
- You own infrastructure and maintenance
- Data never leaves your environment
- No BAA required (you control the data)
- Trade-off: your team owns upgrades and ops

## Common Negotiation Scenarios
**"Can we get a discount?"**
"Yes — there's a startup program with 25% off. Email sales@posthog.com from your account
email with basic org details. Startups can also get $50K in free credits via PostHog for
Startups."

**"We need an annual commitment for budgeting."**
"PostHog doesn't require annual contracts but can offer them as part of an Enterprise
agreement if you need locked-in pricing. Month-to-month is the default."

**"How does this compare to what we pay for Mixpanel + LaunchDarkly + FullStory?"**
"Walk them through the stack math. Mixpanel: typically $500–2K+/month at growth stage.
LaunchDarkly: $75–300/month per seat for starter plans. FullStory: $300+/month.
PostHog covering all three use cases is almost always cheaper, often dramatically so."

## What Costs Extra (honest caveats)
- Enterprise SSO enforcement, SAML, advanced RBAC — requires Scales/Enterprise add-on
- HIPAA BAA — requires Boost or Enterprise add-on
- Dedicated support with SLAs — requires Enterprise
- Training from PostHog team — Enterprise only
