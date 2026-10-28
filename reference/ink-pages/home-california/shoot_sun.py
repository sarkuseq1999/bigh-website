"""Shoot the desktop sun ideas on the live homepage (October 28, 2026).

Mo: on desktop the sun feels "a little too big or too close to the tree"; the phone is fine.
Each idea moves or resizes the live sun by injected CSS, in the opening's own units (--u, one
comp pixel; --inset, how far a wide window moves the column in), so it holds at every desktop
width; nothing in src/ changes.

- now: the live sun (290 comp px, its left at 60% of the window, at most 1000 px in).
- a: smaller, about three quarters (218 comp px), shrunk about its own centre.
- b: smaller as a, and moved 100 comp px left, into the middle of the clearing, away from the
  giant trunk (a first take moved the full-size sun alone; it still felt heavy).
- c: lower and a little smaller (85%), rising behind the young firs, partly hidden, moved 60
  comp px left so it clears the trunk.

    python -X utf8 reference/ink-pages/home-california/shoot_sun.py [base-url] [idea ...]

Shots go to plates/sun/ (git-ignored).
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "plates" / "sun"

SUN = "section#top span[class*='__sun']"
HOME = "calc(var(--inset) + min(60%, 1000px))"

IDEAS = {
    "now": "",
    "a": f"""{SUN} {{ width: calc(218 * var(--u)) !important;
        left: calc({HOME} + 36 * var(--u)) !important; top: calc(10% + 36 * var(--u)) !important; }}""",
    "b": f"""{SUN} {{ width: calc(218 * var(--u)) !important;
        left: calc({HOME} - 64 * var(--u)) !important; top: calc(10% + 36 * var(--u)) !important; }}""",
    "c": f"""{SUN} {{ width: calc(246 * var(--u)) !important;
        left: calc({HOME} - 38 * var(--u)) !important; top: calc(10% + 330 * var(--u)) !important; }}""",
}

SIZES = [("w1920", 1920, 1040), ("w1440", 1440, 900), ("w1280", 1280, 720)]


def main():
    args = sys.argv[1:]
    base = next((a.rstrip("/") for a in args if "://" in a), "https://bigh-website-demo.vercel.app")
    picks = [a for a in args if "://" not in a] or list(IDEAS)
    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--use-angle=d3d11", "--enable-gpu"])
        for key in picks:
            for size, w, h in SIZES:
                ctx = browser.new_context(viewport={"width": w, "height": h})
                page = ctx.new_page()
                page.goto(f"{base}/", wait_until="networkidle")
                if IDEAS[key]:
                    page.add_style_tag(content=IDEAS[key])
                page.wait_for_timeout(7000)
                page.screenshot(path=str(SHOTS / f"{key}-{size}.png"))
                print(key, size)
                ctx.close()
        browser.close()


if __name__ == "__main__":
    main()
