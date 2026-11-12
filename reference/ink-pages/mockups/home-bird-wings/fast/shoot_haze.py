"""The homepage hummingbird's wings on a real page: the frames the browser steps through, and shots.

    python -X utf8 shoot_haze.py <base-url> <name>

For a laptop (1440 x 900) and a phone (390 x 844), both 2x: records the near wing's frame on every
animation frame for 4 s from the moment the beat starts (how many distinct frames, how many
changes a second, when it rests), then pauses everything and shoots the bird at the rest frame,
a haze frame and a settle frame, and the first screen at a haze frame.
"""

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "shots"
SIZES = {"laptop": (1440, 900), "phone": (390, 844)}

RECORD = """(async () => {
  const w = document.querySelector('#top [data-wing=near]');
  const t0 = performance.now(); const seen = [];
  while (performance.now() - t0 < 4000) {
    await new Promise(r => requestAnimationFrame(r));
    seen.push([Math.round(performance.now() - t0), getComputedStyle(w).backgroundPosition.split(' ')[0]]);
  }
  return seen;
})()"""

FREEZE = """
*, *::before, *::after { animation-play-state: paused !important; transition: none !important; }
#top [data-wing] { animation: none !important; }
"""


def main():
    base, name = sys.argv[1].rstrip("/"), sys.argv[2]
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--use-angle=d3d11"])
        for size, (w, h) in SIZES.items():
            ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=2)
            page = ctx.new_page()
            page.goto(base + "/", wait_until="domcontentloaded")
            page.wait_for_function("!!document.querySelector('#top [data-beat=on]')", timeout=60000)
            seen = page.evaluate(RECORD)
            changes = sum(1 for a, b in zip(seen, seen[1:]) if a[1] != b[1])
            distinct = sorted({p for _, p in seen})
            rest_at = next((t for t, p in reversed(seen) if p not in ("0%",)), None)
            fps = len(seen) / 4
            first_3s = [p for t, p in seen if t < 2900]
            ch3 = sum(1 for a, b in zip(first_3s, first_3s[1:]) if a != b)
            print(f"{name} {size}: {fps:.0f} fps, {len(distinct)} distinct {distinct}, "
                  f"{ch3 / 2.9:.0f} changes a second in the haze, last non-rest frame at {rest_at} ms, "
                  f"ends on {seen[-1][1]}")
            (OUT / f"{name}-{size}-record.json").write_text(json.dumps(seen), encoding="utf-8")
            page.wait_for_timeout(1500)
            page.add_style_tag(content=FREEZE)
            b = page.locator("#top [data-brush=crane] img").first.bounding_box()
            pad = 0.08 * b["width"]
            clip = {"x": max(0, b["x"] - pad), "y": max(0, b["y"] - pad),
                    "width": b["width"] + 2 * pad, "height": b["height"] + 2 * pad}
            for k in (0, 2, 5, 9):
                page.evaluate(f"() => document.querySelectorAll('#top [data-wing]').forEach(w => w.style.backgroundPosition = '{k * 10}% 0')")
                page.wait_for_timeout(80)
                page.screenshot(path=str(OUT / f"{name}-{size}-f{k}.png"), clip=clip)
            page.evaluate("() => document.querySelectorAll('#top [data-wing]').forEach(w => w.style.backgroundPosition = '20% 0')")
            page.wait_for_timeout(80)
            page.screenshot(path=str(OUT / f"{name}-{size}-screen.png"))
            ctx.close()
        browser.close()


if __name__ == "__main__":
    main()
