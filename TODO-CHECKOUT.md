# TODO: In-Website Checkout Flows

## Universal Flow (all tiers)
```
[Select tier on website] → [Modal overlay: summary + tier-specific options] → [Stripe Checkout (redirect)] → [Success page with Telegram bot link] → [User taps /start] → [Bot sends progress + "You're live!"]
```

## Modal Overlay Design
- Appears on top of pricing section (dimmed background)
- Tap ✕ or outside → back to pricing
- "Switch to [higher tier]" swaps modal content in place (no close/reopen)
- Mobile-first, expandable sections for detail

## Tinker Modal (€9/mo)
```
Tinker — €9/mo

✓ Private managed server
✓ Telegram today • WhatsApp soon
✓ 17 skills pre-loaded
✓ All self-service integrations

── Your AI needs a brain ──

○ I'll add my API key later (DEFAULT)
○ Buy LLM credits [€____] (min €5)

Available models:              [▸ see pricing]
• DeepSeek V3 (default) — fast, great value
• GPT-4o — versatile, widely trusted
• Claude Sonnet — excellent reasoning
• Claude Opus — most powerful

┌─────────────────────────────────┐
│ 💡 Skip the hassle?             │
│ Essential includes AI for       │
│ just €10/mo more. No keys.      │
│ [Switch to Essential →]         │
└─────────────────────────────────┘

[Pay with Stripe — €9/mo →]
14-day money-back · Cancel anytime
```

### Expandable "see pricing":
```
Model           Cost/msg*   €10 gets you
DeepSeek V3     ~€0.002     ~5,000 msgs
GPT-4o          ~€0.01      ~1,000 msgs
Claude Sonnet   ~€0.015     ~650 msgs
Claude Opus     ~€0.07      ~140 msgs

*Estimates based on average conversation length
```

## Essential Modal (€19/mo)
```
Essential — €19/mo

✓ AI included — no keys needed     [▸ more]
✓ 300+ prompts/day                  [▸ more]
✓ 20 skills pre-loaded              [▸ more]
✓ Web search, Places, voice-to-text [▸ more]
✓ Welcome Pack included             [▸ more]
✓ Priority support

[Pay with Stripe — €19/mo →]
14-day money-back · Cancel anytime
```

## Builder Modal (€29/mo)
```
Builder — €29/mo

✓ Smartest AI — advanced reasoning  [▸ more]
✓ 300+ prompts/day                  [▸ more]
✓ 23 skills pre-loaded              [▸ more]
✓ Voice replies, image creation     [▸ more]
✓ Web automation pack               [▸ more]
✓ 2x Welcome Pack                   [▸ more]
✓ Highest priority support

[Pay with Stripe — €29/mo →]
14-day money-back · Cancel anytime
```

## A/B Variant B (full upsell) — `?v=b`
Essential modal adds:
- Add-on checkboxes: Creative Pack +€3/mo, Power Pack +€5/mo
- Builder nudge box: "Go all-in? Builder = smartest AI + creative tools for €10 more"

Builder modal adds:
- Add-on checkboxes: Creative Pack +€3/mo, Power Pack +€5/mo

## LLM Credits System
- **Credits are credits** — universal, work with any available model
- Customer chooses credit amount at checkout (Tinker) or via agent (Essential/Builder)
- Minimum purchase: €5
- **No expiry** — credits carry over month to month
- Default model: DeepSeek V3 (can change anytime via agent)
- All models available to all credit holders
- When credits run out: agent notifies + offers to buy more (upsell moment)

## Monthly Prompt Caps (Essential/Builder)
- Cap is MONTHLY (matches billing cycle)
- Expressed as DAILY on website for simplicity ("300+/day")
- **At 90%:** agent warns "You've used 90% of your monthly prompts"
- **At 100%:** agent offers to buy credits or wait for reset
- Hard stop if no credits purchased — no auto-overage, no surprise charges
- Resets on billing cycle date

## Assistant Name
- All assistants named "Claw" — no personality step during checkout
- May revisit with rebrand

## "What It Does In Week One" Section (TODO)
- Add concrete examples section above FAQ or below pricing
- 3 vivid use-case bullets, e.g.:
  - "Auto-file your invoices to Notion and ping you for approvals"
  - "Draft smart replies to inbound leads on Telegram in your tone"
  - "Watch flight prices and alert you when to buy"
- Keep it short, specific, outcome-focused

## Email (via Stripe)
- Stripe Checkout collects email — no extra field on our side
- Stripe webhook gives us the email for all post-payment comms
- **Uses:**
  - Order receipt (Stripe auto-sends or we customize)
  - Provisioning failure: "We hit a snag, your payment is safe, we'll email when ready"
  - Provisioning success: backup to Telegram link
  - Cancellation/refund confirmation + data backup link
- **Safety net:** if user never opens Telegram, we can still reach them via email

## A/B Test: Checkout Upsell

### Plan A (light upsell) — default URL
- **Tinker:** summary + LLM brain choice (add key later / buy credits) + Essential nudge box
- **Essential:** summary only → Pay
- **Builder:** summary only → Pay

### Plan B (full upsell) — `?v=b`
- **Tinker:** same as Plan A
- **Essential:** summary + add-on checkboxes (Creative Pack €3, Power Pack €5) + Builder nudge box
- **Builder:** summary + add-on checkboxes (Creative Pack €3, Power Pack €5)

### Track via Stripe metadata
- Pass variant (a/b) + selected tier + any add-ons to Stripe session metadata
- Compare conversion rate + ARPU between variants

## Status: IN PROGRESS — copy finalized, ready to build
