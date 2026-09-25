"""Full-viewport phone captures of topics 2 and 3 to check the stage fits and nothing overlaps."""
import os, sys
from playwright.sync_api import sync_playwright
BASE = sys.argv[1]; W, H = (int(v) for v in sys.argv[2].split("x"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "shoot_phone_stage")
os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    page = b.new_page(viewport={"width": W, "height": H})
    page.goto(BASE + "/" + (sys.argv[3] if len(sys.argv) > 3 else ""), wait_until="networkidle")
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    top, height = page.evaluate("(() => { const t = document.querySelector('#learn [class*=track]'); return [t.getBoundingClientRect().top + scrollY, t.offsetHeight]; })()")
    for share, name in ((0.5, "2"), (0.84, "3")):
        y = top + (height - H) * share
        cur = page.evaluate("scrollY")
        for s in range(1, 9):
            page.evaluate(f"window.scrollTo(0, {cur + (y - cur) * s / 8})"); page.wait_for_timeout(40)
        page.wait_for_timeout(3200)
        page.screenshot(path=os.path.join(OUT, f"stage-{W}-{name}.png"))
        info = page.evaluate("""(() => { const s = document.querySelector('#learn [class*=stage]'); const r = s.getBoundingClientRect();
          const btn = document.querySelector('#learn article[data-active="true"] button').getBoundingClientRect();
          const cap = document.querySelector('#learn [class*=caption]').getBoundingClientRect();
          const title = document.querySelector('#learn article[data-active="true"] h3').getBoundingClientRect();
          return {stage: [Math.round(r.top), Math.round(r.height)], scrollH: s.scrollHeight, buttonBottom: Math.round(btn.bottom), captionBottom: Math.round(cap.bottom), titleTop: Math.round(title.top)}; })()""")
        print(name, info)
    b.close()
