# PostHog — Objection Handling

## "We already use Mixpanel"
**Don't fight it — expand it.**
"Makes sense — Mixpanel is solid for analytics. Quick question: are you also running feature
flags anywhere? Session replay? A/B tests? Most teams using Mixpanel have 2–3 other tools
bolted on — LaunchDarkly for flags, FullStory or Hotjar for replay, something else for
experiments. PostHog puts all of that in one place with one data model. You stop fighting
with data that doesn't sync between tools. What does your current stack look like beyond
Mixpanel?"

**If they push back on switching:** "You don't have to rip anything out day one. Most teams
start with one use case — usually flags or replay — run them side by side, and migrate
analytics when they're ready. We even have a managed migration from Mixpanel."

**On Mixpanel's new feature flags/experiments (relaunched late 2025):** "Mixpanel did
relaunch experimentation — worth knowing. Their flags are newer and less mature than ours.
PostHog has had feature flags longer, with local evaluation, bootstrapping, early access
management, and scheduling that Mixpanel's version doesn't have yet. It's also an Enterprise
add-on for them. For us it's included."

## "We already use Amplitude"
"Amplitude is strong — especially for enterprise teams that need warehouse-native analytics
and have a dedicated data science team. Where we typically win is engineering-led teams that
also need flags, experiments, error tracking, and session replay without paying for four
separate tools. Amplitude's pricing also requires contacting sales and can get expensive at
scale. What's driving the evaluation — cost, missing features, or something else?"

**Amplitude's edge to acknowledge:** "If your team leans heavily on multi-touch attribution,
predictive analytics, or AI-powered brand/LLM visibility — Amplitude genuinely has more
there. Be straight about it. Where PostHog wins is the full developer stack."

## "We use Heap"
"Heap's autocapture is great — that's one of the things we both do. Where PostHog goes
further: we include feature flags, A/B tests, surveys, and error tracking that Heap doesn't
have natively. Our session replay also has developer tooling Heap's doesn't — console logs,
network monitoring, DOM explorer. Also worth knowing: Heap was acquired by Contentsquare in
2023. There's some uncertainty about roadmap direction. PostHog is independent."

## "We're not ready to switch tools right now"
"Totally fair — we're not asking you to rip and replace. What's the one thing your current
setup doesn't do well? That's usually the right place to start. Most customers land on one
product, use it for 60 days, and expand from there."

## "Data privacy / we can't send data to a third party"
"That's a common reason teams come to us. PostHog is open source under MIT license — you
can self-host it on your own infrastructure and your data never leaves. We also have a HIPAA
BAA for cloud customers. Are you self-hosting anything today, or all SaaS?"

## "It's too expensive"
"PostHog is usage-based — you pay for what you use. The free tier is genuinely generous:
1M analytics events, 5K session replays, unlimited feature flags, 1,500 survey responses —
all free every month, no credit card required. More than 90% of customers never pay anything.
If you're on a current stack of Mixpanel + LaunchDarkly + FullStory, you're almost certainly
paying more combined than PostHog would cost. Want to walk through a rough comparison?"

**On price cuts:** "PostHog actively cuts prices. 2024: cut analytics and session replay
pricing. 2025: cut data pipelines and surveys. Their stated policy is to undercut the cheapest
big competitor for every product. That's not typical SaaS behavior."

## "We built our own analytics in-house"
"Respect — that takes real investment. The question that usually shifts the calculus is
maintenance cost over time. What does your team spend keeping it running versus building
new features? And does your internal tool have session replay, feature flags, and
experiments built in, or just event tracking?"

## "We're concerned about vendor lock-in"
"PostHog is MIT licensed and open source. You can export your data at any time, self-host
if you want full control, or run the cloud version. The code is public on GitHub. There's no
proprietary black box. Most tools give you lock-in by default — PostHog's architecture is
explicitly designed to avoid it."

## "We need HIPAA compliance"
"PostHog offers a HIPAA BAA. Single BAA covers analytics, session replay, feature flags,
experiments, and more. That matters because with a multi-tool stack you'd need separate
BAAs with each vendor — which gets complicated fast. What's your current compliance setup?"

## "Your feature flags aren't as good as LaunchDarkly"
"LaunchDarkly is the gold standard for enterprise flag governance — if you have a large
organization with very complex flag requirements, that may be the right call for flags
specifically. Where we win: if you want flags AND analytics AND experiments in one place,
the integrated data model is a real advantage. You can use experiment results directly from
your analytics data without exporting anything. Are flag governance controls the specific
concern, or is it more about the overall stack?"
