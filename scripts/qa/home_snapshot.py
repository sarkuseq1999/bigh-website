"""Homepage snapshot guard for the ink kit (October 5, 2026).

The kit move must not change the homepage. This takes viewport shots of / with reduced motion (the
page is then complete and still: every painting shown, the whole brush line drawn, no mist, no
wingbeat), at four sizes, scrolling one window at a time (never full-page: svh layouts), and
compares them with a saved set.

usage:
  python -X utf8 scripts/qa/home_snapshot.py capture <base-url> <name>
  python -X utf8 scripts/qa/home_snapshot.py compare <base-url> <name> [against=baseline]
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(__file__).resolve().parent / "out" / "home-snapshots"
SIZES = [(1536, 1000), (1280, 800), (900, 1100), (390, 844)]
# A shot matches when under 0.3% of its pixels differ by more than 24 levels (text antialiasing
# and the paper texture's sub-pixel placement move a few pixels between runs).
MAX_SHARE = 0.003
LEVEL = 24


def capture(base: str, name: str) -> Path:
    folder = OUT / name
    folder.mkdir(parents=True, exist_ok=True)
    for old in folder.glob("*.png"):
        old.unlink()
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--use-angle=d3d11"])
        for width, height in SIZES:
            context = browser.new_context(
                viewport={"width": width, "height": height},
                reduced_motion="reduce",
                device_scale_factor=1,
            )
            page = context.new_page()
            page.goto(f"{base}/", wait_until="networkidle", timeout=120000)
            page.evaluate("document.fonts.ready.then(() => true)")
            page.wait_for_timeout(1500)
            total = page.evaluate("document.documentElement.scrollHeight")
            y, index = 0, 0
            while y < total:
                page.evaluate(f"window.scrollTo(0, {y})")
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(600)
                page.screenshot(path=str(folder / f"{width}-{index:02d}.png"))
                y += height
                index += 1
                total = page.evaluate("document.documentElement.scrollHeight")
            context.close()
        browser.close()
    return folder


def compare(name: str, against: str) -> bool:
    new, old = OUT / name, OUT / against
    ok = True
    names = sorted({f.name for f in old.glob("*.png")} | {f.name for f in new.glob("*.png")})
    for file in names:
        a, b = old / file, new / file
        if not a.exists() or not b.exists():
            print(f"FAIL {file}: missing in {'baseline' if not a.exists() else name}")
            ok = False
            continue
        x = np.asarray(Image.open(a).convert("RGB"), dtype=np.int16)
        y = np.asarray(Image.open(b).convert("RGB"), dtype=np.int16)
        if x.shape != y.shape:
            print(f"FAIL {file}: size {x.shape} vs {y.shape}")
            ok = False
            continue
        share = float((np.abs(x - y).max(axis=2) > LEVEL).mean())
        status = "ok  " if share <= MAX_SHARE else "FAIL"
        ok &= share <= MAX_SHARE
        print(f"{status} {file}: {share * 100:.3f}% of pixels differ")
    return ok


if __name__ == "__main__":
    mode, base, name = sys.argv[1], sys.argv[2], sys.argv[3]
    capture(base, name)
    if mode == "compare":
        against = sys.argv[4] if len(sys.argv) > 4 else "baseline"
        passed = compare(name, against)
        print("PASS" if passed else "FAIL")
        sys.exit(0 if passed else 1)
