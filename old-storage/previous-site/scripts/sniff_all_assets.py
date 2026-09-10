"""Load every original page in a real browser and download every wp-content
image the browser fetches (covers CSS/Elementor backgrounds on all pages)."""

import pathlib
import re
import sys
from urllib.parse import urlparse

import requests
from playwright.sync_api import sync_playwright

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")

BASE = pathlib.Path(__file__).resolve().parent.parent / "content" / "harvest" / "assets"
H = {"User-Agent": "Mozilla/5.0"}

PAGES = [
    "en", "kr", "jp", "cns", "hken", "vn",
    "advanced-opc-formula", "deer-horn-reishi", "green-bee-propolis", "heart-q10",
    "nature-calm", "nano-detoxifier", "nuricell", "super-green", "turmerific", "uber-calcium",
    "about", "science", "support", "organic", "non-gmo", "gluten-free", "vegan",
    "opportunity", "career", "signup", "login", "privacy-notice", "return-policy",
]

seen: set[str] = set()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.on(
        "response",
        lambda r: seen.add(r.url)
        if re.search(r"\.(png|jpe?g|webp|gif)([?#].*)?$", r.url, re.I)
        else None,
    )
    for path in PAGES:
        try:
            pg.goto(f"https://bighnow.com/{path}", wait_until="domcontentloaded", timeout=60000)
            pg.wait_for_timeout(1800)
            pg.evaluate(
                "async () => { for (let y = 0; y <= document.body.scrollHeight; y += 600) {"
                " window.scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); } }"
            )
            pg.wait_for_timeout(800)
        except Exception as e:
            print(path, "FAIL", str(e)[:80])
    b.close()

new = 0
for u in sorted(seen):
    if "wp-content" not in u:
        continue
    rel = urlparse(u).path.split("/wp-content/")[-1]
    dest = BASE / rel
    if dest.exists():
        continue
    try:
        r = requests.get(u, headers=H, timeout=60)
        if r.status_code == 200:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(r.content)
            new += 1
            print(" +", rel)
    except requests.RequestException:
        print(" fail", rel)

print(f"browser saw {len(seen)} images; downloaded {new} new")
