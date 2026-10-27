"""Mockups of the footer's "end of the trail" (Mo picked B, October 26, 2026): the crane leaves
the promise and stands in the grass beside the FDA park sign; the promise stands alone, a size
smaller. The live page is shot as it is, with CSS and one picture laid over it (nothing in the
site changes). Pictures land in reference/ink-pages/mockups/footer-crane/.

usage: python -X utf8 reference/ink-pages/footer-crane/shoot_mockups.py [base] [option ...]
"""

import base64
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
MOCK = HERE.parents[0] / "mockups" / "footer-crane"
IMG = MOCK / "img"
BASE = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].startswith("http") else "http://localhost:3007"
ONLY = [a for a in sys.argv[1:] if not a.startswith("http")]

CRANES = json.loads((IMG / "cranes.json").read_text(encoding="utf-8"))

# Per option: which crane, its height from feet to the top of the bird (in the sign painting's
# pixels, the posts standing 488 tall), and where its feet stand (past the sign's right edge, in
# the sign painting's pixels).
OPTIONS = {
    "now": None,
    "a": {"crane": "a1", "tall": 540, "gap": 120},
    "b": {"crane": "b1", "tall": 410, "gap": 120},
    "c": {"crane": "c1", "tall": 300, "gap": 250, "phoneTall": 220, "phoneGap": 140},
}
PAGES = {"home": "/en", "science": "/en/science"}
SIZES = {"desktop": (1440, 900), "phone": (390, 844)}

CSS = """
footer [class*="promise"] > img { display: none !important; }
footer [class*="footerMessage"] { font-size: clamp(34px, 2.9vw, 48px) !important; }
@media (max-width: 720px) {
  footer [class*="footerMessage"] { font-size: clamp(30px, 8.6vw, 36px) !important; }
  /* The narrower sign runs past the 6 lines balance works on: no word alone on the last line. */
  [data-fda] p, [data-fda] p > span { text-wrap: pretty !important; }
}
"""

PLACE = """([src, c, o]) => {
  const fda = document.querySelector('[data-fda]');
  const p = fda.querySelector('p');
  const k = parseFloat(getComputedStyle(fda).getPropertyValue('--k')) * 0.8333;  // CSS px per sign-painting px
  const phone = innerWidth <= 720;
  // A wide pose stands smaller on a phone, so the sign keeps its width.
  const tall = (phone && o.phoneTall) || o.tall;
  o = { ...o, gap: (phone && o.phoneGap) || o.gap };
  const s = (tall * k) / (c.feetY - c.top);  // CSS px per crane-painting px
  // How far the crane reaches past the sign's right edge.
  const reach = o.gap * k + (c.w - c.feetX) * s;
  fda.style.position = 'relative';
  if (phone) {
    // The sign gives the crane the room at its right; the crane's faded grass may run to the
    // window's edge.
    const gutter = innerWidth - fda.getBoundingClientRect().right;
    p.style.width = `calc(100% - ${Math.max(reach - gutter, 0)}px)`;
    fda.style.justifyContent = 'flex-start';
  } else {
    // The sign and the crane, together, centred.
    fda.style.paddingRight = `${reach}px`;
  }
  const host = fda.getBoundingClientRect();
  const r = p.getBoundingClientRect();
  const img = new Image();
  img.src = src;
  img.alt = '';
  Object.assign(img.style, {
    position: 'absolute',
    width: `${c.w * s}px`,
    height: `${c.h * s}px`,
    left: `${r.right - host.left + o.gap * k - c.feetX * s}px`,
    top: `${r.bottom - host.top - 75 * k - c.feetY * s}px`,
    mixBlendMode: 'multiply',
    pointerEvents: 'none',
    maxWidth: 'none',
  });
  fda.append(img);
  return { k, s, reach, sign: [r.left, r.top, r.right, r.bottom], lines: Math.round((r.height - 0) / 1) };
}"""


def main():
    MOCK.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for name, opt in OPTIONS.items():
            if ONLY and name not in ONLY:
                continue
            for page_name, path in PAGES.items():
                src = None
                if opt:
                    # The homepage's paintings wear "green spring": the crane's crown is red there.
                    tint = "-spring" if page_name == "home" else ""
                    data = (IMG / f"crane-{opt['crane']}{tint}.png").read_bytes()
                    src = "data:image/png;base64," + base64.b64encode(data).decode()
                for size_name, size in SIZES.items():
                    mobile = size[0] < 768
                    ctx = browser.new_context(
                        viewport={"width": size[0], "height": size[1]},
                        is_mobile=mobile,
                        has_touch=mobile,
                        reduced_motion="reduce",
                        device_scale_factor=2,
                    )
                    page = ctx.new_page()
                    if opt:
                        page.add_init_script(
                            "document.addEventListener('DOMContentLoaded', () => {"
                            f"const s = document.createElement('style'); s.textContent = {json.dumps(CSS)};"
                            "document.head.append(s); });"
                        )
                    page.goto(BASE + path, wait_until="networkidle", timeout=120000)
                    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
                    page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
                    page.evaluate("document.fonts.ready")
                    page.wait_for_timeout(1500)
                    if opt:
                        info = page.evaluate(PLACE, [src, CRANES[opt["crane"]], opt])
                        print(name, page_name, size_name, info)
                    page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
                    page.wait_for_timeout(1200)
                    out = MOCK / f"{name}-{page_name}-{size_name}.png"
                    page.screenshot(path=str(out))
                    print("saved", out.name)
                    ctx.close()
        browser.close()


if __name__ == "__main__":
    main()
