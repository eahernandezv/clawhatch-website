# Pricing V3 — Final Tier Structure

## Tiers

| | **Tinker** (€9/mo) | **Essential** (€19/mo) | **Builder** (€29/mo) |
|---|---|---|---|
| Managed instance | ✅ | ✅ | ✅ |
| Telegram + WhatsApp | ✅ | ✅ | ✅ |
| LLM | BYOK or buy credits | DeepSeek V3 | Sonnet 4 |
| Prompts/day | BYOK = unlimited | 300+ | 300+ |
| Pre-loaded skills | 17 | 20 | 23 |
| Self-service skills (customer keys) | ✅ (all 16) | ✅ (all 16) | ✅ (all 16) |
| Web search (Brave) | ❌ | ✅ | ✅ |
| Google Places | ❌ | ✅ | ✅ |
| Voice transcription (Whisper) | ❌ | ✅ | ✅ |
| Welcome Pack (one-time) | ❌ | ✅ (1x) | ✅ (2x) |
| Support | Standard | Priority | Highest |

## Welcome Pack (one-time credits at checkout)

| Credit | Essential (1x) | Builder (2x) |
|---|---|---|
| TTS voice replies | 10 | 20 |
| Image generations | 5 | 10 |
| Voice call minutes | 5 min | 10 min |
| Captcha solves | 25 | 50 |
| Residential proxy | 50MB | 100MB |

Cost to us: ~€1.30 (Essential) / ~€2.60 (Builder) per new user. One-time.

## Add-ons (any tier, after credits run out)

### Power Pack — €5/mo
- 1000 captcha solves
- 2GB residential proxy

### Creative Pack — €3/mo (TBD pricing)
- 50 image generations
- 30 TTS voice replies

### Voice Pack — €3/mo (TBD pricing)
- 30 voice call minutes

### À la carte (TBD pricing)
- Images: €1/10
- TTS: €1/15 replies
- Voice calls: €1/10 min
- Captcha: €1/500 solves
- Proxy: €2/500MB

## Skill Breakdown

### Tinker (17 pre-loaded — free/no-key skills)
weather, tmux, canvas, healthcheck, nano-pdf, openai-whisper (local), sherpa-onnx-tts (local), blogwatcher, video-frames, coding-agent, camsnap, skill-creator, session-logs, obsidian, summarize, gifgrep, model-usage

### Essential (+3 = 20 — adds our-key skills)
+ web search (Brave), goplaces (Google Places), openai-whisper-api

### Builder (+3 = 23 — adds expensive our-key skills)
+ sag (ElevenLabs TTS), openai-image-gen, voice-call

### Self-service skills (all tiers, customer provides keys)
notion, trello, slack, discord, github, gh-issues, himalaya (email), gog (Google Workspace), spotify-player, xurl (Twitter/X), openhue, sonoscli, ordercli, 1password, bear-notes, oracle, nano-banana-pro (Gemini)

Note: Customers set these up directly with their agent. No tier gating.

## Onboarding Flows

### Tinker
Payment → "Provide your LLM API key" OR "Buy credits from us" → Provision → Agent intro + skill discovery

### Essential & Builder
Payment → Provision → Agent intro + skill discovery + Welcome Pack notification

## Upsell Moments (agent-driven)
- Credits exhausted: "You've used your free image credits! Want the Creative Pack (€3/mo)?"
- Feature discovery: Agent suggests capabilities during onboarding
- Usage patterns: Agent notices user would benefit from an add-on

## Cost Analysis

| Tier | Hosting | LLM (est.) | Bundled APIs | Welcome Pack | Total cost/mo |
|---|---|---|---|---|---|
| Tinker (€9) | ~€5.40 | €0 (BYOK) | €0 | €0 | ~€5.40 |
| Essential (€19) | ~€5.40 | ~€2-4 | ~€1-2 | ~€0.10* | ~€8.50-11.50 |
| Builder (€29) | ~€5.40 | ~€5-15 | ~€1-2 | ~€0.20* | ~€11.60-22.60 |

*Welcome Pack amortized over subscription lifetime (assuming 12+ months)

## Margins

| Tier | Price | Est. cost | Gross margin |
|---|---|---|---|
| Tinker | €9 | ~€5.40 | ~40% |
| Essential | €19 | ~€10 | ~47% |
| Builder | €29 | ~€17 | ~41% |

Note: Builder margin improves significantly if user is not maxing out Sonnet daily. Add-on revenue is pure margin after infrastructure.
