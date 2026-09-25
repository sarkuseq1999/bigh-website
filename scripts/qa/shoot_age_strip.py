"""The cell at ages 20/35/50/65/80 as one strip, plus the gap between the last words and the closing button."""
import os, sys
from PIL import Image
from playwright.sync_api import sync_playwright
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3007"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "shoot_age_strip")
W, H = 1440, 900
os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    page = b.new_page(viewport={"width": W, "height": H})
    page.goto(BASE + "/", wait_until="networkidle")
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    top, height = page.evaluate("(() => { const t = document.querySelector('#learn [class*=track]'); return [t.getBoundingClientRect().top + scrollY, t.offsetHeight]; })()")
    y = top + (height - H) * 0.84
    for s in range(1, 9):
        page.evaluate(f"window.scrollTo(0, {y * s / 8})"); page.wait_for_timeout(40)
    page.wait_for_timeout(2600)
    box = page.evaluate("(() => { const r = document.querySelector('#learn [class*=visual]').getBoundingClientRect(); return [r.x, r.y, r.width, r.height]; })()")
    clip = {"x": box[0] + box[2] * 0.15, "y": box[1] + box[3] * 0.18, "width": box[2] * 0.7, "height": box[3] * 0.62}
    frames = []
    slider = page.locator("#learn input[type=range]")
    for v in (20, 35, 50, 65, 80):
        slider.evaluate("(el, v) => { const set = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set; set.call(el, v); el.dispatchEvent(new Event('input', { bubbles: true })); }", v)
        page.wait_for_timeout(1300)
        path = os.path.join(OUT, f"age-{v}.png")
        page.screenshot(path=path, clip=clip)
        frames.append(Image.open(path))
    w, h = frames[0].size
    strip = Image.new("RGB", (w * 5, h), "white")
    for i, f in enumerate(frames): strip.paste(f, (i * w, 0))
    strip.save(os.path.join(OUT, "age-strip.png"))
    # The end of the track: how far is the closing button below the last words?
    page.evaluate(f"window.scrollTo(0, {top + height - H + 400})")
    page.wait_for_timeout(800)
    gap = page.evaluate("(() => { const a = document.querySelector('#learn article[data-active=\"true\"] button').getBoundingClientRect(); const b = document.querySelector('#learn a[href=\"#research\"]').getBoundingClientRect(); return {explainerBottom: Math.round(a.bottom), exploreTop: Math.round(b.top), gap: Math.round(b.top - a.bottom)}; })()")
    print("strip", strip.size, "gap", gap)
    page.screenshot(path=os.path.join(OUT, "track-end.png"))
    b.close()
