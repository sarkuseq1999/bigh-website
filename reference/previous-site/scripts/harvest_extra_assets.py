"""Second-pass asset harvest: files the page-content pass missed.

Covers (1) wp-content URLs that appear as *links* in harvested markdown
(supplement-facts sheets, full-size gallery images), and (2) CSS background
images + header logos referenced only from live HTML/stylesheets.
"""

import pathlib
import re
import sys
import time
from urllib.parse import urlparse

import requests

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
}
BASE = pathlib.Path(__file__).resolve().parent.parent / "content" / "harvest" / "assets"
IMG_URL = r"https?://(?:www\.)?bighnow\.com/wp-content/[^\s\)\"'&]+?\.(?:png|jpe?g|gif|webp|svg)"

urls: set[str] = set()

for p in (BASE.parent).rglob("*.md"):
    urls |= set(re.findall(IMG_URL, p.read_text(encoding="utf-8")))

for page in ["https://bighnow.com/en", "https://bighnow.com/nuricell", "https://bighnow.com/kr"]:
    html = requests.get(page, headers=HEADERS, timeout=40).text
    urls |= set(re.findall(IMG_URL, html))
    for css in set(re.findall(r"href=\"(https?://(?:www\.)?bighnow\.com/wp-content/[^\"]+?\.css[^\"]*)\"", html)):
        try:
            body = requests.get(css, headers=HEADERS, timeout=40).text
            urls |= set(re.findall(IMG_URL, body))
        except requests.RequestException:
            pass

new, fail = 0, []
for u in sorted(urls):
    rel = urlparse(u).path.replace("/wp-content/", "").lstrip("/")
    dest = BASE / rel
    if dest.exists():
        continue
    try:
        r = requests.get(u, headers=HEADERS, timeout=60)
        if r.status_code == 200:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(r.content)
            new += 1
        else:
            fail.append((r.status_code, u))
    except requests.RequestException:
        fail.append(("ERR", u))
    time.sleep(0.15)

print(f"urls found: {len(urls)} | newly downloaded: {new} | failed: {len(fail)}")
for f in fail[:10]:
    print("  fail:", f)
