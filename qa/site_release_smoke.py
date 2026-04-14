#!/usr/bin/env python3
import json
import re
import sys
import time
import urllib.request
import urllib.error
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

    failed = [c for c in checks if not c["ok"]]
    print(json.dumps({"profile": profile_name, "passed": len(checks) - len(failed), "failed": len(failed), "results": checks}, indent=2))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
