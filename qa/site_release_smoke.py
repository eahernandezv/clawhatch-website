#!/usr/bin/env python3
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (Hermes website smoke)"
BASE = "https://clawhatch.app"
CONFIG_PATH = Path(__file__).with_name("site_release_expectations.json")
checks = []


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode("utf-8", "replace")
        return {"url": r.geturl(), "status": getattr(r, "status", 200), "headers": dict(r.headers.items()), "text": body}


def fetch_allow_error(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Cache-Control": "no-cache"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return getattr(r, "status", 200), r.geturl(), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.geturl(), e.read().decode("utf-8", "replace")


def bust(path):
    ts = int(time.time())
    sep = "&" if "?" in path else "?"
    return f"{BASE}{path}{sep}v={ts}"


def title(text):
    m = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
    return re.sub(r"<.*?>", "", m.group(1)).strip() if m else None


def h1(text):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.I | re.S)
    return re.sub(r"<.*?>", "", m.group(1)).strip() if m else None


def ok(name, cond, detail):
    checks.append({"name": name, "ok": bool(cond), "detail": detail})


def assert_substrings(prefix, text, required, forbidden):
    for needle in required:
        ok(f"{prefix}-has-{needle[:30]}", needle in text, needle)
    for needle in forbidden:
        ok(f"{prefix}-not-{needle[:30]}", needle not in text, needle)


def assert_success_page_wiring(wiring):
    """Success pages must forward Stripe's resolve_token to /select-runtime
    and /resolve-claim. See success_page_wiring in the expectations JSON."""
    for page in wiring.get("pages", []):
        path = page["path"]
        page_data = fetch(bust(path))
        ok(f"wiring-{path}-status", page_data["status"] == 200, page_data["url"])
        assert_substrings(
            f"wiring-{path}",
            page_data["text"],
            page["required_substrings"],
            page["forbidden_substrings"],
        )


def http_call(method, url, *, body=None, headers=None):
    req = urllib.request.Request(url, method=method)
    req.add_header("User-Agent", UA)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    data = None
    if body is not None:
        data = body.encode("utf-8") if isinstance(body, str) else body
    try:
        with urllib.request.urlopen(req, data=data, timeout=30) as r:
            return getattr(r, "status", 200), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def assert_api_resolve_token(wiring):
    api = wiring["api_base"].rstrip("/")
    a = wiring["api_assertions"]

    # /resolve-claim must require resolve_token.
    status, body = http_call("GET", f"{api}/resolve-claim?session_id=cs_smoke_fake")
    ok(
        "api-resolve-claim-missing-token",
        status == a["resolve_claim_missing_token_status"],
        f"status={status} body={body[:120]}",
    )

    # /resolve-claim with a bad token must not leak a claim code.
    q = urllib.parse.urlencode({"session_id": "cs_smoke_fake", "resolve_token": "wrong"})
    status, body = http_call("GET", f"{api}/resolve-claim?{q}")
    ok(
        "api-resolve-claim-bad-token",
        status in a["resolve_claim_bad_token_status_options"],
        f"status={status} body={body[:120]}",
    )

    # /select-runtime with missing token: hard-fail expected once the
    # SELECT_RUNTIME_ALLOW_UNTOKENED escape hatch is removed. Warn-only
    # while the hatch is on so the smoke still surfaces the state.
    status, body = http_call(
        "POST",
        f"{api}/select-runtime",
        body=json.dumps({"session_id": "cs_smoke_fake", "runtime_type": "openclaw"}),
        headers={"Content-Type": "application/json"},
    )
    escape_hatch_off = status == 400 and "resolve_token required" in body
    if escape_hatch_off:
        ok("api-select-runtime-missing-token-strict", True, "escape hatch is OFF (strict mode)")
    elif a.get("select_runtime_missing_token_warn_only"):
        checks.append({
            "name": "api-select-runtime-missing-token-warn",
            "ok": True,
            "warn": True,
            "detail": f"SELECT_RUNTIME_ALLOW_UNTOKENED still ON (status={status} body={body[:120]})",
        })
    else:
        ok(
            "api-select-runtime-missing-token-strict",
            False,
            f"escape hatch expected OFF but got status={status} body={body[:120]}",
        )

    # Mismatched token must never be accepted.
    status, body = http_call(
        "POST",
        f"{api}/select-runtime",
        body=json.dumps({
            "session_id": "cs_smoke_fake",
            "runtime_type": "openclaw",
            "resolve_token": "wrong",
        }),
        headers={"Content-Type": "application/json"},
    )
    ok(
        "api-select-runtime-bad-token",
        status in a["select_runtime_bad_token_status_options"],
        f"status={status} body={body[:120]}",
    )

    # CORS preflight must succeed — real browser POSTs send OPTIONS first.
    status, _ = http_call(
        "OPTIONS",
        f"{api}/select-runtime",
        headers={
            "Origin": "https://clawhatch.app",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    ok(
        "api-select-runtime-cors-preflight",
        status in a["cors_preflight_success_status_options"],
        f"status={status}",
    )


def load_config():
    cfg = json.loads(CONFIG_PATH.read_text())
    profile_name = sys.argv[1] if len(sys.argv) > 1 else cfg["active_profile"]
    profile = cfg["profiles"].get(profile_name)
    if not profile:
        raise SystemExit(f"unknown profile: {profile_name}")
    return cfg, profile_name, profile


def main():
    cfg, profile_name, profile = load_config()

    root = fetch(bust("/"))
    root_text = root["text"]
    ok("root-status", root["status"] == 200, root["url"])
    assert_substrings("root", root_text, profile["root"]["required_substrings"], profile["root"]["forbidden_substrings"])

    thirty = fetch(bust("/30days/"))
    thirty_text = thirty["text"]
    ok("30-status", thirty["status"] == 200, thirty["url"])
    assert_substrings("30", thirty_text, profile["thirty"]["required_substrings"], profile["thirty"]["forbidden_substrings"])

    for key, path, etitle, eh1 in cfg["pages"]:
        r = fetch(bust(path))
        txt = r["text"]
        ok(f"{key}-status", r["status"] == 200, r["url"])
        ok(f"{key}-body", len(txt) > 1500, f"len={len(txt)}")
        ok(f"{key}-title", title(txt) == etitle, repr(title(txt)))
        ok(f"{key}-h1", h1(txt) == eh1, repr(h1(txt)))

    video = fetch(bust("/crab-video.mp4"))
    ok("video-status", video["status"] == 200, video["url"])
    ok("video-type", video["headers"].get("Content-Type", "").startswith("video/mp4"), video["headers"].get("Content-Type", ""))
    poster = fetch(bust("/crab-video-poster.png"))
    ok("poster-status", poster["status"] == 200, poster["url"])
    ok("poster-type", poster["headers"].get("Content-Type", "").startswith("image/"), poster["headers"].get("Content-Type", ""))

    bot_status, bot_url, _ = fetch_allow_error(profile["telegram_bot_url"])
    ok("bot-external", bot_status == 200, f"{bot_status} {bot_url}")
    for name, url in [
        ("rodrigo-linkedin", "https://www.linkedin.com/in/rodrigo-r-ramos/"),
        ("maria-linkedin", "https://www.linkedin.com/in/maria-ioana-manastireanu/"),
        ("mauricio-linkedin", "https://www.linkedin.com/in/mauricioaviles/"),
    ]:
        st, final, _ = fetch_allow_error(url)
        ok(name, st in (200, 999), f"{st} {final}")

    wiring = cfg.get("success_page_wiring")
    if wiring:
        assert_success_page_wiring(wiring)
        assert_api_resolve_token(wiring)

    failed = [c for c in checks if not c["ok"]]
    warned = [c for c in checks if c.get("warn")]
    print(json.dumps({
        "profile": profile_name,
        "passed": len(checks) - len(failed),
        "failed": len(failed),
        "warnings": len(warned),
        "results": checks,
    }, indent=2))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
