"""Screenshots of the zoom mockup at several scroll depths, desktop and phone.

  python -X utf8 reference/ink-pages/mockups/science-zoom/shoot_zoom_mock.py
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "shots"
SHOTS.mkdir(exist_ok=True)
STOPS = (0.0, 0.2, 0.34, 0.48, 0.66, 0.78, 1.0)

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, w, h in (("desk", 1440, 900), ("phone", 390, 844)):
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto((HERE / "index.html").as_uri())
        pg.wait_for_timeout(1500)
        for s in STOPS:
            pg.evaluate(
                "s => { const t = document.getElementById('track');"
                " const y = t.offsetTop + (t.offsetHeight - innerHeight) * s; scrollTo(0, y); }",
                s,
            )
            pg.wait_for_timeout(400)
            pg.screenshot(path=str(SHOTS / f"{name}-{int(s * 100):03d}.png"))
        pg.close()
    b.close()
print("shots in", SHOTS)
