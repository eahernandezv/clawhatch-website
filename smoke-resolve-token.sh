#!/usr/bin/env bash
# Prod smoke test for the resolve_token wiring on clawhatch.app.
#
# Verifies:
#   1. Live success pages read resolve_token from URLSearchParams.
#   2. Live success pages forward resolve_token to /select-runtime (POST body).
#   3. Live success pages append resolve_token to /resolve-claim (GET query).
#   4. api.clawhatch.app /resolve-claim rejects missing/bad resolve_token.
#   5. api.clawhatch.app /select-runtime rejects missing resolve_token
#      when the SELECT_RUNTIME_ALLOW_UNTOKENED escape hatch is off
#      (informational — will pass while the hatch is still on).
#
# Usage:  ./smoke-resolve-token.sh
# Exit 0 if all hard checks pass, non-zero if any fail.
set -u

API=https://api.clawhatch.app
SITE=https://clawhatch.app
PAGES=(/success /c/success)

pass=0
fail=0
warn=0

log_pass() { printf '  \033[32m✓\033[0m %s\n' "$1"; pass=$((pass+1)); }
log_fail() { printf '  \033[31m✗\033[0m %s\n' "$1"; fail=$((fail+1)); }
log_warn() { printf '  \033[33m!\033[0m %s\n' "$1"; warn=$((warn+1)); }
section() { printf '\n\033[1m== %s ==\033[0m\n' "$1"; }

# ---- 1. static pages ----
section "success pages serve the resolve_token-aware JS"
for path in "${PAGES[@]}"; do
  html=$(curl -sfL "$SITE$path" 2>/dev/null) || { log_fail "$path: fetch failed"; continue; }
  if grep -q "resolve_token" <<<"$html"; then
    log_pass "$path: resolve_token present in HTML"
  else
    log_fail "$path: resolve_token MISSING — Cloudflare Pages build hasn't landed"
  fi
  if grep -q "resolve_token: resolveToken" <<<"$html"; then
    log_pass "$path: /select-runtime POST forwards resolve_token"
  else
    log_fail "$path: /select-runtime still missing resolve_token in POST body"
  fi
  if grep -q "resolve-claim?session_id=.*resolve_token=" <<<"$html"; then
    log_pass "$path: /resolve-claim URL appends resolve_token"
  else
    log_fail "$path: /resolve-claim URL still missing resolve_token"
  fi
done

# ---- 2. API: /resolve-claim rejects missing / bad token ----
section "API /resolve-claim token enforcement"
r=$(curl -s -o /tmp/_smoke_body -w '%{http_code}' "$API/resolve-claim?session_id=cs_smoke_fake")
body=$(cat /tmp/_smoke_body)
if [ "$r" = "400" ] && grep -q "resolve_token required" <<<"$body"; then
  log_pass "missing resolve_token -> 400 resolve_token required"
else
  log_fail "missing resolve_token: expected 400, got $r body=$body"
fi

r=$(curl -s -o /tmp/_smoke_body -w '%{http_code}' "$API/resolve-claim?session_id=cs_smoke_fake&resolve_token=wrong")
body=$(cat /tmp/_smoke_body)
# Two acceptable responses: 404 not_found (session unknown) or 403 mismatch.
if [ "$r" = "404" ] || [ "$r" = "403" ]; then
  log_pass "bogus session+token -> $r ($(jq -r .error 2>/dev/null <<<"$body" || echo "$body"))"
else
  log_fail "bogus session+token: expected 403/404, got $r body=$body"
fi

# ---- 3. API: /select-runtime behavior ----
section "API /select-runtime token enforcement"
payload_no_token='{"session_id":"cs_smoke_fake","runtime_type":"openclaw"}'
r=$(curl -s -o /tmp/_smoke_body -w '%{http_code}' -X POST "$API/select-runtime" \
    -H 'Content-Type: application/json' --data "$payload_no_token")
body=$(cat /tmp/_smoke_body)
case "$r" in
  400)
    if grep -q "resolve_token required" <<<"$body"; then
      log_pass "missing resolve_token -> 400 (escape hatch is OFF; strict mode)"
    else
      log_warn "400 but unexpected body: $body"
    fi
    ;;
  200|404|409)
    log_warn "escape hatch still ON: SELECT_RUNTIME_ALLOW_UNTOKENED=1 (got $r). Flip it off once Pages deploys."
    ;;
  *)
    log_fail "unexpected /select-runtime response: $r body=$body"
    ;;
esac

payload_bad_token='{"session_id":"cs_smoke_fake","runtime_type":"openclaw","resolve_token":"wrong"}'
r=$(curl -s -o /tmp/_smoke_body -w '%{http_code}' -X POST "$API/select-runtime" \
    -H 'Content-Type: application/json' --data "$payload_bad_token")
body=$(cat /tmp/_smoke_body)
case "$r" in
  403|404)
    log_pass "bogus token -> $r ($(jq -r .error 2>/dev/null <<<"$body" || echo "$body"))"
    ;;
  *)
    log_fail "bogus token on /select-runtime: expected 403/404, got $r body=$body"
    ;;
esac

# ---- 4. CORS preflight (a real browser POST goes through OPTIONS first) ----
section "CORS preflight"
r=$(curl -s -o /dev/null -w '%{http_code}' -X OPTIONS "$API/select-runtime" \
    -H 'Origin: https://clawhatch.app' \
    -H 'Access-Control-Request-Method: POST' \
    -H 'Access-Control-Request-Headers: content-type')
if [ "$r" = "204" ] || [ "$r" = "200" ]; then
  log_pass "OPTIONS /select-runtime -> $r"
else
  log_fail "OPTIONS /select-runtime -> $r (browsers will block the POST)"
fi

section "Summary"
printf '  pass: %d  fail: %d  warn: %d\n' "$pass" "$fail" "$warn"
rm -f /tmp/_smoke_body
[ "$fail" = 0 ]
