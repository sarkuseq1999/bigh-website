"""Mockups for Mo (November 10, 2026): four ideas for the Science page's first screen, on the real page.

  python -X utf8 reference/ink-pages/mockups/science-hero/shoot_hero.py <base-url> [idea ...] [--film] [--only=desk|phone]

Opens <base-url>/en/science (the dev server), swaps the first screen for each idea by injecting CSS
and a few elements (ideas.py), and takes a desktop and a phone picture. With --film it also takes
the frames of each idea's resting motion (one loop) for make_loops.py. Nothing in src/ changes: a
throwaway sample, not site code. Pictures land in reference/ink-pages/science/plates/hero/
(git-ignored).
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ideas import HELPERS, IDEAS  # noqa: E402

HERE = Path(__file__).resolve().parent
PLATES = HERE.parent.parent / "science" / "plates" / "hero"
SHOTS = PLATES / "shots"
SHOTS.mkdir(parents=True, exist_ok=True)

args = [a for a in sys.argv[1:] if not a.startswith("--")]
FILM = "--film" in sys.argv
BASE = args[0].rstrip("/") if args else "http://localhost:3007"
WANT = args[1:] or list(IDEAS)
# The phone is shot at twice its size, so its words stay sharp on a real phone's screen.
SIZES = (("desk", 1440, 900, 1), ("phone", 390, 844, 2))
ONLY = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--only=")), None)


def serve(route):
    """/__mock/<file> is read from plates/hero/."""
    name = route.request.url.split("/__mock/", 1)[1].split("?")[0]
    path = PLATES / name
    if path.exists():
        route.fulfill(path=str(path))
    else:
        route.fulfill(status=404, body="missing " + name)


with sync_playwright() as p:
    b = p.chromium.launch()
    for key in WANT:
        idea = IDEAS[key]
        for name, w, h, dense in SIZES:
            if ONLY and name != ONLY:
                continue
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dense)
            ctx.route("**/__mock/**", serve)
            pg = ctx.new_page()
            pg.goto(BASE + "/en/science", wait_until="networkidle")
            pg.wait_for_timeout(2500)
            if idea.get("css"):
                pg.add_style_tag(content=idea["css"])
            pg.evaluate(HELPERS)
            if idea.get("js"):
                pg.evaluate(idea["js"])
            pg.wait_for_timeout(idea.get("settle", 2500))
            pg.screenshot(path=str(SHOTS / f"{key}-{name}.png"))
            for i, stop in enumerate(idea.get("stops", ())):
                pg.evaluate(
                    """s => { const t = document.querySelector('[data-zoom]');
                    scrollTo({ top: t.offsetTop + (t.offsetHeight - innerHeight) * s, behavior: 'instant' }); }""",
                    stop,
                )
                pg.wait_for_timeout(1500)
                pg.screenshot(path=str(SHOTS / f"{key}-{name}-s{i + 1}.png"))
            if FILM and idea.get("loop"):
                pg.evaluate("scrollTo({ top: 0, behavior: 'instant' })")
                pg.wait_for_timeout(400)
                # Ten frames a second is smooth here: nothing moves a pixel between two frames.
                seconds, fps = idea["loop"], 10
                frames = SHOTS / f"{key}-{name}-frames"
                frames.mkdir(exist_ok=True)
                for old in frames.glob("*"):
                    old.unlink()
                # Every CSS animation is paused and stepped by hand, so the loop is exact.
                pg.evaluate("document.getAnimations().forEach(a => a.pause())")
                for f in range(int(seconds * fps)):
                    pg.evaluate(
                        """t => document.getAnimations().forEach(a => {
                          if (a.effect && a.effect.target && a.effect.target.closest('[data-mock]')) a.currentTime = t; })""",
                        f * 1000 / fps,
                    )
                    pg.screenshot(path=str(frames / f"{f:04d}.jpg"), type="jpeg", quality=93)
            ctx.close()
        print("shot", key)
    b.close()
print("shots in", SHOTS)
