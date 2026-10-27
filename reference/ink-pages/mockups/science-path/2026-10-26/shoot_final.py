"""Shoot mockup B: the live Science page with mock_b.js injected, viewport shots scrolled like a visitor."""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3007"
TAG = sys.argv[2] if len(sys.argv) > 2 else "v1"
HERE = Path(__file__).parent
MOCK = HERE / "mock"
OUT = HERE / "shots-b" / TAG
OUT.mkdir(parents=True, exist_ok=True)
SCRIPT = (HERE / "mock_b.js").read_text(encoding="utf-8")

SIZES = {"desk": (1440, 900), "phone": (390, 844)}


def serve(route):
    name = route.request.url.split("/__mock/")[1].split("?")[0]
    route.fulfill(path=str(MOCK / name), content_type="image/webp")


with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-angle=d3d11"])
    for name, (w, h) in SIZES.items():
        ctx = browser.new_context(
            viewport={"width": w, "height": h},
            device_scale_factor=2 if name == "phone" else 1,
            is_mobile=name == "phone",
            has_touch=name == "phone",
        )
        page = ctx.new_page()
        page.route("**/__mock/**", serve)
        page.goto(f"{BASE}/science", wait_until="networkidle")
        page.wait_for_timeout(1500)
        page.evaluate(SCRIPT)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1200)
        tops = page.evaluate(
            """() => Object.fromEntries(['mock-hero','mock-path','research','health','formulas','ask']
              .map(id => [id, Math.round(document.getElementById(id).getBoundingClientRect().top + scrollY)])
              .concat([['places', [...document.querySelectorAll('.place')].map(e => Math.round(e.getBoundingClientRect().top + scrollY))],
                       ['pageH', document.documentElement.scrollHeight]]))"""
        )
        print(name, tops)
        # One shot per stop on the way down: the top, each place centred, then the rest.
        marks = page.evaluate(
            """() => {
              const nav = 80;
              const mid = (el) => {
                const r = el.getBoundingClientRect();
                return Math.max(0, Math.round(r.top + scrollY - nav - Math.max(0, (innerHeight - nav - r.height) / 2)));
              };
              const top = (id) => Math.round(document.getElementById(id).getBoundingClientRect().top + scrollY - nav + 4);
              return [["top", 0], ...[...document.querySelectorAll('.place')].map((el, i) => ["place" + (i + 1), mid(el)]),
                      ["research", top('research')], ["health", top('health')], ["formulas", top('formulas')], ["ask", top('ask')]];
            }"""
        )
        for label, y in marks:
            page.evaluate(f"window.scrollTo(0, {y})")
            page.wait_for_timeout(900)
            page.screenshot(path=str(OUT / f"{name}-{label}.png"))
        print(name, "shots", [m[0] for m in marks])
        ctx.close()
    browser.close()
