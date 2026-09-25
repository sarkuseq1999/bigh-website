"""Capture the reworked free-radical scene at each step and the age slider at 20/50/80."""
import os
import sys
import time
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3007"
LOC = sys.argv[2] if len(sys.argv) > 2 else ""
W, H = (int(v) for v in (sys.argv[3] if len(sys.argv) > 3 else "1440x900").split("x"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "shoot_glass3")
os.makedirs(OUT, exist_ok=True)
tag = f"{LOC or 'en'}-{W}"

def clip(page):
    box = page.evaluate("(() => { const r = document.querySelector('#learn [class*=plate]').getBoundingClientRect(); return [r.x, r.y, r.width, r.height]; })()")
    pad = 40
    return {"x": max(0, box[0] - pad), "y": max(0, box[1] - pad), "width": min(W, box[2] + 2 * pad), "height": min(H, box[3] + 2 * pad)}

with sync_playwright() as p:
    browser = p.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    page = browser.new_page(viewport={"width": W, "height": H})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: errors.append("console " + m.text[:160]) if m.type == "error" else None)
    page.goto(f"{BASE}/{LOC}", wait_until="networkidle")
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    top, height = page.evaluate("(() => { const t = document.querySelector('#learn [class*=track]'); return [t.getBoundingClientRect().top + scrollY, t.offsetHeight]; })()")
    def go(share):
        y = top + (height - H) * share
        cur = page.evaluate("scrollY")
        for s in range(1, 9):
            page.evaluate(f"window.scrollTo(0, {cur + (y - cur) * s / 8})")
            page.wait_for_timeout(40)
    go(0.5)
    page.wait_for_timeout(1200)
    ready = page.evaluate("document.querySelector('#learn [data-ready]').dataset.ready")
    lit = "(() => [...document.querySelectorAll('#learn [data-step]')].map(e => e.dataset.lit).join())()"
    deadline = time.time() + 25
    while time.time() < deadline and page.evaluate(lit) != "false,false,true":
        page.wait_for_timeout(100)
    while time.time() < deadline and page.evaluate(lit) != "true,false,false":
        page.wait_for_timeout(50)
    start = time.time()
    for at, name in ((1.6, "1-embers"), (3.75, "2-burn"), (5.6, "3-catch"), (6.5, "4-intercept"), (8.2, "5-repair")):
        page.wait_for_timeout(max(0, int((start + at - time.time()) * 1000)))
        page.screenshot(path=os.path.join(OUT, f"{tag}-radicals-{name}.png"), clip=clip(page))
        print(name, page.evaluate(lit))
    # Topic 3: the slider at 20, 50 and 80.
    go(0.84)
    page.wait_for_timeout(2600)
    slider = page.locator("#learn input[type=range]")
    for value, name in ((20, "a-20"), (50, "b-50"), (80, "c-80")):
        slider.evaluate("(el, v) => { const set = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set; set.call(el, v); el.dispatchEvent(new Event('input', { bubbles: true })); }", value)
        page.wait_for_timeout(1400)
        page.screenshot(path=os.path.join(OUT, f"{tag}-age-{name}.png"), clip=clip(page))
        print(name, page.evaluate("document.querySelector('#learn [class*=age] strong').textContent"))
    print("ready", ready, errors[:3] or "no errors")
    browser.close()
