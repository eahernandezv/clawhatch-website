# Launch TODO List
**Updated: 2026-03-01 (evening)**

---

## ✅ Done Today (Feb 28)

- [x] **Bot roster audit** — queried BotFather via Telethon, found 11 bots
- [x] **Bot role reassignment** — @ClawHatchSetupBot = management, @ClawHatchBot = proxy #1
- [x] **Deleted @ClawSetupBot** — legacy, no longer needed
- [x] **Telethon runbook saved** — `runbooks/telethon-auth.md` (web auth on port 8888)
- [x] **Provisioner rewritten** — removed BotFather dependency; assigns proxy bot slots instead
- [x] **Proxy slot assignment** — sequential per customer (1st assistant → bot #1, 2nd → #2, max 5)
- [x] **Templates updated** — customer VPS no longer gets Telegram channel config (messages via relay)
- [x] **Success page updated** — points to @ClawHatchSetupBot
- [x] **E2E test passed** — website → pay → claim → personality → provision → live ✅ (no BotFather!)
- [x] **OpenClaw version in status** — provisioner grabs version after install; shows in My Bot(s)
- [x] **Reboot polling** — Fix My Bot + Force Reboot now poll up to 60-90s instead of single check
- [x] **TIER_INFO unified** — single source of truth in status.js; V3 tiers + legacy fallbacks
- [x] **My Plan updated** — shows Tinker/Essential/Builder with correct prices, no model names
- [x] **Change Plan updated** — V3 tiers only, correct upgrade/downgrade arrows
- [x] **Price diff in confirmations** — shows "+€10/mo" or "-€20/mo" on plan changes
- [x] **Stripe subscription updates on tier change** — upgrades prorate immediately; downgrades at period end
- [x] **Payment portal** — Stripe Customer Portal link (manage subscription, update card, view invoices)
- [x] **New Assistant flow updated** — shows Tinker €9 / Essential €19 / Builder €29
- [x] **Validators updated** — accepts new tier names
- [x] **Refresh Status simplified** — goes to bot detail view, not Fix My Bot flow
- [x] **Reboot message improved** — "This usually takes 1-2 minutes"
- [x] **Downgrade messaging** — Tinker-specific BYOK warning; savings shown
- [x] **3 test Stripe subscriptions cancelled** — cleaned up
- [x] **Bot env vars cleaned up** — CLAWHATCH_SETUP_BOT_TOKEN + PROXY_BOT_1_TOKEN

---

## 🔴 Pre-Launch (Must Do)

### Bot UX (remaining)
- [ ] **Tier picker: show plan features** — two improvements needed:
  1. **Tier selection screen**: add "ℹ️ Compare plans" button below tiers → sends detailed comparison message (skills count, AI model, daily prompts, Welcome Pack, what's included)
  2. **After selecting a tier**: confirm screen should list that tier's key features (not just name + price + "300+/day"). E.g. Essential: "✓ AI included ✓ 20 skills ✓ Web search ✓ 300+/day ✓ Welcome Pack"
- [ ] **Personality input during onboarding** — re-add personality customization step (currently skipped, using defaults). Must work outside conversations plugin context. Options: handle in post-setup "Edit Personality" flow, or use a dedicated text input handler.
- [ ] **Add-ons page** — needs V3 update (Power Pack €5, Creative Pack €3, or remove entirely for launch)
- [x] **Create @ClawHatch_5_Bot** — ✅ All 5 proxy slots active
- [x] **Get proxy bot tokens** — ✅ All 5 verified: @ClawHatchBot, @ClawHatch_2-5_Bot

### Proxy System
- [x] **Start proxy bot services** — ✅ proxy-bot.js running as 5 systemd services (clawhatch-proxy-1 through -5)
- [x] **Wire proxy bots #1-5** — ✅ All polling
- [x] **Test chat routing** — ✅ E2E tested, relay working
- [x] **Message relay on customer VPS** — ✅ Verified, restarts after openclaw_setup

### Payments & Provisioning
- [x] **Enable Stripe auto-receipts** — ✅ Ernesto enabled in Dashboard
- [x] **Enable plan switching in Stripe Portal** — ✅ Ernesto enabled in Dashboard
- [ ] **Handle Tinker BYOK flow** — guide user to add API key post-provisioning
- [x] **Essential/Builder auto-configure** — ✅ TIER_MODELS in templates.js: Essential=DeepSeek V3, Builder=Gemini 3.1 Pro
- [x] **Credit purchase flow** — ✅ Built (usage-tracker.js, account.js, stripe-webhook.js, api-server.js)
- [x] **Monthly prompt cap** — ✅ Built (9000/mo, 90% warning, 100% hard stop, proxy-bot.js enforced)
- [ ] **Failed payment handling** — test webhook for failed charges

### Legal
- [ ] **Set effective date** on T&C + Privacy Policy
- [ ] **Deploy legal pages** — terms.html + privacy.html

### Infrastructure
- [x] **Pre-load skills per tier** — ✅ skill-tiers.js updated; `clawhub install` during provisioning; 28 skills active on Linux
- [x] **Install free skills on all tiers** — ✅ via clawhub marketplace install
- [x] **Install self-service skills on all tiers** — ✅ pre-installed, agent guides key setup
- [x] **Monitor sidecar on all VPS** — ✅ Deployed to Hari, Ernesto's VPS, Maria's VPS; typing_stuck detection active
- [x] **Skills display in bot** — ✅ Shows only Linux-compatible skills; runs as openclaw user for correct detection
- [x] **Hetzner server limit** — ✅ No limit hit; 4+ servers work fine on ClawHatch project
- [ ] **Provision our-key API keys** — Salvor will inject keys into customer VPS during provisioning. Blocked on Ernesto getting the accounts:
  - [ ] 🔑 **OpenAI API key** *(Ernesto)* — covers whisper-api + image-gen (Essential+Builder)
  - [ ] 🔑 **Google Cloud project + API keys** *(Ernesto)* — enable Places API (goplaces) + get Tenor API key (gifgrep) (Essential+Builder)
  - [ ] 🔑 **ElevenLabs API key** *(Ernesto)* — TTS/sag skill (Builder only)
  - [ ] 🔑 **Twilio or Telnyx account** *(Ernesto)* — voice-call skill (Builder only, can defer to post-launch)
  - [ ] 🌐 **Residential proxy for Builder tier** — customer VPS or shared pool; needed for web automation pack (captcha solving, form filling, scraping without blocks)
  - [ ] 🧩 **Captcha resolver for Builder tier** — integrate captcha service (2Captcha, CapSolver, etc.) into customer VPS provisioning
- [x] ~~**Monthly prompt cap**~~ — moved to Payments section (done)
- [ ] **Welcome Pack credits** — track one-time credits per feature

### Analytics
- [x] **Configure Umami** — ✅ Running at analytics.clawhatch.app, website added (ID: dea915ba...)
- [x] **Add event tracking** — ✅ Already wired: page views, tier_selected, checkout_started, pricing_modal_open
- [ ] **A/B conversion dashboard** — set up Umami filters to compare variant A vs B conversions



---

## 🟡 Post-Launch

- [ ] **Secret/credential management for customers** — hybrid approach combining Hari's vault (AES-256 encrypted files, password-gated) with bot-level `/secret` command (intercepts before LLM, per-instance key derivation, auto-loads at runtime). Two tiers: `/secret` for API keys (zero-friction, auto-decrypt), password-gated vault for master secrets (Hari's approach). Needs: bot-level intercept, encryption at rest, shred-safe cleanup.
- [ ] Register Eenmanszaak — March 20 appointment
- [ ] Update Stripe with own KVK
- [ ] Usage dashboard for customers
- [ ] Add-on purchase flow (Creative Pack, Power Pack)
- [ ] "What It Does In Week One" website section
- [ ] 3-day free trial
- [ ] Migrate maintenance to Hari
- [ ] 2-3 testimonials / social proof
- [ ] WhatsApp Business API
- [ ] SmartRouter integration
- [ ] Message template system (messages.js — 162 call sites identified)

---

## 🟢 Roadmap (Q2 2026+)

- [ ] Proxy Phase 2: standby proxies (2x CX11)
- [ ] Proxy Phase 3: VPS pool (instant onboarding)
- [ ] Voice message support
- [ ] Calendar/email integration
- [ ] Group AI — shared assistant
- [ ] Ambient listening mode

---

## ✅ Decisions Locked

| Decision | Choice |
|---|---|
| Brand name | **ClawHatch** ✅ (decided 2026-03-01) |
| Pricing V3 | Tinker €9 / Essential €19 / Builder €29 |
| AI models | Tinker=BYOK, Essential=DeepSeek V3, Builder=Sonnet 4 |
| Bot architecture | @ClawHatchSetupBot = management; @ClawHatchBot + _2-_5 = proxy |
| Proxy assignment | Sequential per customer (Nth assistant → bot #N) |
| Checkout flow | Website → Stripe → success page → Telegram deep link |
| Tier changes | Upgrades: prorate immediately; Downgrades: at period end |
| Payment management | Stripe Customer Portal |
| All assistants named | "Claw" (revisit with rebrand) |
| Payment provider | Stripe live mode |
| Business entity | Partner's KVK for MVP; own Eenmanszaak March 20 |
