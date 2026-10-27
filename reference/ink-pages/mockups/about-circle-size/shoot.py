"""Mockups for About's opening circle (Mo, October 26, 2026): "the circle is a little bit too small
... it doesn't feel immersive enough", and the gold leaf's fall and shine look cartoonish.

Each look is CSS injected into the live About page (the public demo by default, or a base URL given
first), shot at a big desktop (1920x1000, the size Mo saw it at), a laptop (1440x900) and a phone
(390x844). Pictures land in img/ as <look>-<size>[-<t>].webp.

    python -X utf8 reference/ink-pages/mockups/about-circle-size/shoot.py [base] [look,look,...]
"""

import io
import os
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
OUT = HERE / "img"
OUT.mkdir(exist_ok=True)

BASE = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].startswith("http") else (
    "https://bigh-website-demo.vercel.app"
)
ONLY = next((a.split(",") for a in sys.argv[1:] if not a.startswith("http")), None)

SIZES = {
    "desk": dict(width=1920, height=1000, scale=1),
    "laptop": dict(width=1440, height=900, scale=1),
    "phone": dict(width=390, height=844, scale=2),
}

WORDS = 'section[data-part="opening"] > div:first-of-type'

# The circle frames the words: as tall as the first screen allows, the title written inside it.
INSIDE = f"""
section[data-part="opening"] {{ padding-top: calc(88px + 8px) !important; }}
{WORDS} {{
  --W: min(calc((100svh - 88px - 96px) * 1247 / 1136), 94vw, 1040px);
  grid-template-rows: 1fr auto 1fr;
  grid-template-columns: 1fr;
}}
{WORDS} [data-enso] {{ grid-area: 1 / 1 / 4 / 2; width: var(--W) !important; margin: 0 !important; }}
{WORDS} > p:first-of-type {{ grid-area: 1 / 1; align-self: end; }}
{WORDS} > h1 {{ grid-area: 2 / 1; font-size: clamp(40px, calc(var(--W) * 0.068), 72px) !important; }}
{WORDS} > p:last-of-type {{ grid-area: 3 / 1; align-self: start; }}
section[data-part="opening"] img[data-bloom]:not([data-enso] img) {{ margin-top: -3vw !important; }}
@media (max-width: 599px) {{
  section[data-part="opening"] {{ padding-top: calc(88px + 4px) !important; }}
  {WORDS} {{
    --W: calc(100vw - 16px);
    grid-template-rows: 1fr auto 1fr auto;
    flex: 0 0 auto !important;
    margin-block: auto;
  }}
  {WORDS} > h1 {{ font-size: 40px !important; max-width: 3.6em; translate: -4% 0; }}
  {WORDS} > p:first-of-type {{ translate: -4% 0; }}
  {WORDS} > p:last-of-type {{ grid-area: 4 / 1; margin-top: 12px !important; }}
  section[data-part="opening"] img[data-bloom]:not([data-enso] img) {{ margin-top: 0 !important; }}
}}
"""

# Bigger, words still under it: as big as the first screen allows with the words below.
BELOW = f"""
section[data-part="opening"] {{ padding-top: calc(88px + 16px) !important; }}
{WORDS} [data-enso] {{
  width: min(calc((100svh - 88px - 300px) * 1247 / 1136), 72vw, 820px) !important;
  margin-bottom: 8px !important;
}}
@media (max-width: 599px) {{
  {WORDS} [data-enso] {{ width: min(100%, 340px) !important; }}
}}
"""

NO_LEAF = "[data-dot], [data-shadow], [data-sheen] { display: none !important; }"

# The flake lies still in the wet ink: it comes up as the brush passes it (no fall, no shine).
STILL_LEAF = """
[data-shadow], [data-sheen] { display: none !important; }
@keyframes leaf-laid { from { opacity: 0; } to { opacity: 1; } }
[data-enso] [data-dot] {
  animation: leaf-laid 0.5s ease-out calc(var(--stroke-delay) + 0.45s) backwards !important;
}
"""

# No flake: the gold moves to the far hilltop, which warms slowly once the circle has closed,
# like morning sun reaching a hill.
DAWN = (
    NO_LEAF
    + """
@keyframes dawn { from { filter: grayscale(1); } to { filter: grayscale(0); } }
section[data-part="opening"] img[data-bloom="waiting"]:not([data-enso] img) { filter: blur(5px) grayscale(1) !important; }
section[data-part="opening"] img[data-bloom="in"]:not([data-enso] img) { filter: grayscale(1) !important; }
section[data-part="opening"] img[data-bloom="done"]:not([data-enso] img) { animation: dawn 3.2s ease-in-out 0.3s both; }
"""
)

LOOKS = {
    "now": "",
    "inside": INSIDE,
    "below": BELOW,
    "inside-noleaf": INSIDE + NO_LEAF,
    "inside-still": INSIDE + STILL_LEAF,
    "inside-dawn": INSIDE + DAWN,
    "below-noleaf": BELOW + NO_LEAF,
}

# Moments to stop and shoot (seconds after the page opens); the last is the page at rest.
TIMES = {
    "inside-still": [1.4, 2.6, 10],
    "inside-dawn": [5, 7.5, 12],
}

INIT = """
(css => {
  const add = () => {
    const s = document.createElement('style');
    s.textContent = css;
    (document.head || document.documentElement).appendChild(s);
  };
  if (document.documentElement) add(); else document.addEventListener('DOMContentLoaded', add);
})(%s)
"""


def save(png: bytes, path: Path) -> None:
    Image.open(io.BytesIO(png)).convert("RGB").save(path, "WEBP", quality=88, method=6)


def main() -> None:
    import json

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--use-angle=d3d11"])
        for look, css in LOOKS.items():
            if ONLY and look not in ONLY:
                continue
            for size, vp in SIZES.items():
                if os.environ.get("SIZES") and size not in os.environ["SIZES"].split(","):
                    continue
                ctx = browser.new_context(
                    viewport=dict(width=vp["width"], height=vp["height"]),
                    device_scale_factor=vp["scale"],
                    is_mobile=size == "phone",
                    has_touch=size == "phone",
                )
                page = ctx.new_page()
                page.add_init_script(INIT % json.dumps(css))
                page.goto(f"{BASE}/about", wait_until="domcontentloaded")
                t0 = page.evaluate("performance.now()")
                for t in TIMES.get(look, [10]):
                    now = page.evaluate("performance.now()")
                    wait = t * 1000 - (now - t0)
                    if wait > 0:
                        page.wait_for_timeout(wait)
                    name = f"{look}-{size}" + ("" if t == TIMES.get(look, [10])[-1] else f"-{t}")
                    save(page.screenshot(), OUT / f"{name}.webp")
                    print("shot", name)
                ctx.close()
        browser.close()


if __name__ == "__main__":
    main()
