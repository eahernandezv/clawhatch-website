#!/usr/bin/env python3
import json
import re
import sys
import time
import urllib.request
import urllib.error

UA = 'Mozilla/5.0 (Hermes website smoke)'
BASE = 'https://clawhatch.app'

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Cache-Control': 'no-cache'})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode('utf-8', 'replace')
        return {'url': r.geturl(), 'status': getattr(r, 'status', 200), 'headers': dict(r.headers.items()), 'text': body}

def fetch_allow_error(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Cache-Control': 'no-cache'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return getattr(r, 'status', 200), r.geturl(), r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.geturl(), e.read().decode('utf-8', 'replace')

def bust(path):
    ts = int(time.time())
    sep = '&' if '?' in path else '?'
    return f'{BASE}{path}{sep}v={ts}'

def title(text):
    m = re.search(r'<title>(.*?)</title>', text, re.I | re.S)
    return re.sub(r'<.*?>', '', m.group(1)).strip() if m else None

def h1(text):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.I | re.S)
    return re.sub(r'<.*?>', '', m.group(1)).strip() if m else None

checks = []
def ok(name, cond, detail):
    checks.append({'name': name, 'ok': bool(cond), 'detail': detail})

root = fetch(bust('/'))
root_text = root['text']
ok('root-status', root['status'] == 200, root['url'])
ok('root-copy-60', 'Start delegating in 60 seconds' in root_text, 'Apr10 copy present')
ok('root-not-under5', 'under 5 min' not in root_text, 'later copy absent')
ok('root-7day', '7-Day Free Trial' in root_text and 'Start 7-day free trial' in root_text, '7-day root offer')
ok('root-not-30day', '30-Day Free Trial' not in root_text, 'no 30-day root offer')
ok('root-bot-handle', 'ClawHatchBot' in root_text and 'ClawHatchSetupBot' not in root_text, 'Apr10 bot handle on root')

thirty = fetch(bust('/30days/'))
thirty_text = thirty['text']
ok('30-status', thirty['status'] == 200, thirty['url'])
ok('30-copy-60', 'Start delegating in 60 seconds' in thirty_text, 'Apr10 copy present')
ok('30-not-under5', 'under 5 min' not in thirty_text, 'later copy absent')
ok('30-offer', '30-Day Free Trial' in thirty_text and 'Start 30-day free trial' in thirty_text, '30-day variant works')
ok('30-not-7day', '7-Day Free Trial' not in thirty_text, 'no 7-day on /30days/')
ok('30-bot-handle', 'ClawHatchBot' in thirty_text and 'ClawHatchSetupBot' not in thirty_text, 'Apr10 bot handle on /30days/')
ok('30-variant-b', "var variant = 'b';" in thirty_text, 'variant b script')

pages = [
    ('guide', '/blog/ultimate-guide-hosting-openclaw-2026.html', 'The Ultimate Guide to Hosting OpenClaw in 2026 | ClawHatch Guides', 'The Ultimate Guide to Hosting OpenClaw in 2026'),
    ('easiest', '/blog/easiest-openclaw-setup.html', 'The Easiest OpenClaw Setup Path | ClawHatch Guides', 'The Easiest OpenClaw Setup Path'),
    ('telegram', '/blog/openclaw-telegram-bot.html', 'How to Use OpenClaw Through Telegram | ClawHatch Guides', 'How to Use OpenClaw Through Telegram'),
    ('vps', '/blog/openclaw-vps-alternative.html', 'A Better Alternative to DIY OpenClaw VPS Hosting | ClawHatch Guides', 'A Better Alternative to DIY OpenClaw VPS Hosting'),
    ('phone', '/blog/how-to-use-openclaw-on-your-phone.html', 'How to Use OpenClaw on Your Phone | ClawHatch Guides', 'How to Use OpenClaw on Your Phone'),
    ('macmini', '/blog/how-to-install-openclaw-without-mac-mini.html', 'How to Install OpenClaw Without a Mac Mini | ClawHatch Guides', 'How to Install OpenClaw Without a Mac Mini'),
    ('privacy', '/privacy', 'Privacy Policy — ClawHatch', 'Privacy Policy'),
    ('terms', '/terms', 'Terms of Service — ClawHatch', 'Terms of Service'),
    ('data-deletion', '/data-deletion/', 'Data Deletion — ClawHatch', 'Data Deletion'),
    ('success', '/success/', 'Welcome to ClawHatch! 🎉', "You're In! 🎉"),
    ('c-success', '/c/success/', 'Welcome to ClawHatch! 🎉', "You're In! 🎉"),
]
for key, path, etitle, eh1 in pages:
    r = fetch(bust(path))
    txt = r['text']
    ok(f'{key}-status', r['status'] == 200, r['url'])
    ok(f'{key}-body', len(txt) > 1500, f'len={len(txt)}')
    ok(f'{key}-title', title(txt) == etitle, repr(title(txt)))
    ok(f'{key}-h1', h1(txt) == eh1, repr(h1(txt)))

video = fetch(bust('/crab-video.mp4'))
ok('video-status', video['status'] == 200, video['url'])
ok('video-type', video['headers'].get('Content-Type','').startswith('video/mp4'), video['headers'].get('Content-Type',''))
poster = fetch(bust('/crab-video-poster.png'))
ok('poster-status', poster['status'] == 200, poster['url'])
ok('poster-type', poster['headers'].get('Content-Type','').startswith('image/'), poster['headers'].get('Content-Type',''))

bot_status, bot_url, _ = fetch_allow_error('https://t.me/ClawHatchBot')
ok('bot-external', bot_status == 200, f'{bot_status} {bot_url}')
for name, url in [
    ('rodrigo-linkedin', 'https://www.linkedin.com/in/rodrigo-r-ramos/'),
    ('maria-linkedin', 'https://www.linkedin.com/in/maria-ioana-manastireanu/'),
    ('mauricio-linkedin', 'https://www.linkedin.com/in/mauricioaviles/'),
]:
    st, final, _ = fetch_allow_error(url)
    ok(name, st in (200, 999), f'{st} {final}')

failed = [c for c in checks if not c['ok']]
print(json.dumps({'passed': len(checks)-len(failed), 'failed': len(failed), 'results': checks}, indent=2))
sys.exit(1 if failed else 0)
