# LLM Credit Pricing — Our Rates vs OpenRouter

## Markup Strategy
- **Big brands** (OpenAI, Anthropic, Google, xAI): 50% of OpenRouter's markup = ~2.75% over direct
- **Others** (DeepSeek, Kimi, Mistral, Meta): 25% of OpenRouter's markup

## Per-Token Pricing (per 1M tokens)

| Model | Direct Price (in/out) | OpenRouter (in/out) | Our Price (in/out) | Savings vs OR |
|---|---|---|---|---|
| DeepSeek V3 | $0.14 / $0.28 | $0.32 / $0.89 | $0.19 / $0.43 | ~40-52% |
| Kimi K2 | ~$0.40 / $1.60 | $0.55 / $2.20 | $0.44 / $1.75 | ~20% |
| GPT-5 | $1.25 / $10.00 | $1.31 / $10.55 | $1.28 / $10.28 | ~3% |
| Claude Sonnet 4.5 | $3.00 / $15.00 | $3.17 / $15.83 | $3.08 / $15.41 | ~3% |
| Claude Opus 4.6 | $5.00 / $25.00 | $5.28 / $26.38 | $5.14 / $25.69 | ~3% |
| Gemini 3 Flash | $0.50 / $3.00 | $0.53 / $3.17 | $0.51 / $3.08 | ~3% |
| Grok 4 | $3.00 / $15.00 | $3.17 / $15.83 | $3.08 / $15.41 | ~3% |
| Claude Haiku 4.5 | $1.00 / $5.00 | $1.06 / $5.28 | $1.03 / $5.14 | ~3% |
| GPT-5 Nano | $0.05 / $0.40 | $0.05 / $0.42 | $0.05 / $0.41 | ~3% |
| DeepSeek R1 | $0.55 / $2.19 | $0.70 / $2.50 | $0.59 / $2.27 | ~10-16% |

## Per-Message Estimates (for user-facing display)

Based on average conversation turn (~2,000 input tokens + ~300 output tokens):

| Model | Our Price/msg | OpenRouter/msg | You Save |
|---|---|---|---|
| DeepSeek V3 | ~€0.001 | ~€0.002 | 50% |
| Kimi K2 | ~€0.003 | ~€0.004 | 20% |
| Gemini 3 Flash | ~€0.005 | ~€0.005 | 3% |
| GPT-5 | ~€0.01 | ~€0.01 | 3% |
| Claude Sonnet | ~€0.015 | ~€0.016 | 3% |
| Grok 4 | ~€0.015 | ~€0.016 | 3% |
| Claude Opus | ~€0.03 | ~€0.03 | 3% |

## Credit Purchase Math (€10 example)

| Model | €10 gets you |
|---|---|
| DeepSeek V3 | ~10,000 msgs |
| Kimi K2 | ~3,300 msgs |
| Gemini 3 Flash | ~2,000 msgs |
| GPT-5 | ~1,000 msgs |
| Claude Sonnet | ~650 msgs |
| Grok 4 | ~650 msgs |
| Claude Opus | ~330 msgs |

## Routing Strategy
- **Direct accounts** (cheaper, no middleman): OpenAI, Anthropic, Google, xAI, DeepSeek, Kimi
- **Via OpenRouter** (fallback, niche models): everything else
- SmartRouter (Hari's project) can optimize routing for cost/quality

## Key Claims
- "Always cheaper than OpenRouter"
- "Up to 50% cheaper on popular models"
- "30+ models available"
- Credits never expire, work with any model
