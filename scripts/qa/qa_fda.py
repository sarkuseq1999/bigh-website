"""The FDA statement at the foot of every page, on its painted California trail sign (Mo's pick "I",
October 13, 2026; ink/fda-statement.tsx).

On the ink pages (home, About, NuriCell) and the Science page: one statement, in the footer, the
exact words as real text, in Zilla Slab (loaded), 600, 15 px or more (the preview note too); the
sign's picture drawn as the paragraph's border (fda-sign.webp, or fda-sign-phone.webp without the
oak on a phone), loading, and really painted (brown wood in the pixels, on the dark Science footer
too); every line of the words inside the sign's face; cream letters at 4.5:1 or more against the
painted face (measured from the pixels); two lines on a 1280+ window, centred; no sideways scroll;
no hairline in the footer. The ink footer (no logo since the footer-crane redesign): the sign
under the copyright line, centred, and the preview note last, under it, at every width. The last
screen still shows the whole promise and crane at rest clear of the menu bar at eight laptop sizes
(home, About, NuriCell). The words appear once per page (NuriCell does not repeat them above the
footer), also on the four old-template product pages and in another language.

Run: python -X utf8 scripts/qa/qa_fda.py [base-url]   (default http://localhost:3036)
"""
import io
import os
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3036").rstrip("/")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "fda")
os.makedirs(OUT, exist_ok=True)
GPU = ["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"]
STATEMENT = (
    "These statements have not been evaluated by the Food and Drug Administration. "
    "This product is not intended to diagnose, treat, cure, or prevent any disease."
)
PAGES = {"home": "/", "about": "/about", "nuricell": "/products/nuricell", "science": "/science"}
INK = ("home", "about", "nuricell")
OLD = ["/products/green-bee-propolis", "/products/advanced-opc", "/products/turmerific", "/products/nature-calm"]
CREAM = (246, 231, 189)
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok)))
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


def open_page(browser, path, size):
    mobile = size[0] < 768
    context = browser.new_context(
        viewport={"width": size[0], "height": size[1]},
        is_mobile=mobile,
        has_touch=mobile,
        reduced_motion="reduce",
    )
    page = context.new_page()
    problems, signs = [], []

    def on_response(r):
        if "fda-sign" in r.url:
            signs.append((r.status, r.url))
            if r.status >= 400:
                problems.append(f"{r.status} {r.url}")

    page.on("pageerror", lambda e: problems.append(str(e)))
    page.on("response", on_response)
    page.goto(BASE + path, wait_until="networkidle", timeout=120000)
    return context, page, problems, signs


GEOMETRY = """(() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; };
  const signs = [...document.querySelectorAll('[data-fda]')];
  const sign = signs[0];
  const p = sign?.querySelector('p');
  const s = p && getComputedStyle(p);
  // The words' own line boxes: the text inside the words' span (the span's own box would count as
  // one more line).
  const range = document.createRange();
  if (p?.firstElementChild) range.selectNodeContents(p.firstElementChild);
  const glyphs = p?.firstElementChild ? [...range.getClientRects()].filter(b => b.width > 2) : [];
  const footer = sign?.closest('footer');
  const note = [...(footer?.querySelectorAll('p') || [])].find(e => e.textContent.startsWith('Educational content'));
  const legal = [...(footer?.querySelectorAll('span') || [])].find(e => e.textContent.startsWith('©'));
  const logo = footer?.querySelector('a[aria-label] img, img[alt=BiGH]');
  const grid = sign?.parentElement;
  const px = (v) => parseFloat(v) || 0;
  return {
    count: signs.length,
    inFooter: !!footer,
    text: p ? p.textContent.trim() : '',
    family: s?.fontFamily || '',
    loaded: s ? document.fonts.check(`600 ${s.fontSize} "Zilla Slab"`) : false,
    weight: s ? parseInt(s.fontWeight) : 0,
    size: s ? px(s.fontSize) : 0,
    color: s?.color,
    align: s?.textAlign,
    image: s?.borderImageSource || '',
    borders: s ? [px(s.borderTopWidth), px(s.borderRightWidth), px(s.borderBottomWidth), px(s.borderLeftWidth)] : null,
    lines: new Set(glyphs.map(b => Math.round(b.top))).size,
    glyphs: glyphs.length ? [Math.min(...glyphs.map(b => b.left)), Math.min(...glyphs.map(b => b.top)),
                             Math.max(...glyphs.map(b => b.right)), Math.max(...glyphs.map(b => b.bottom))] : null,
    reach: p ? [-px(getComputedStyle(p.firstElementChild).marginLeft), -px(getComputedStyle(p.firstElementChild).marginRight)] : null,
    hairline: grid ? px(getComputedStyle(grid).borderTopWidth) + px(getComputedStyle(grid).borderBottomWidth) : -1,
    noteSize: note ? px(getComputedStyle(note).fontSize) : 0,
    sign: r(p), footer: r(footer), note: r(note), legal: r(legal), logo: r(logo), grid: r(grid),
    mentions: document.body.innerText.split('Food and Drug Administration').length - 1,
    sideways: document.documentElement.scrollWidth - innerWidth,
  };
})()"""


def luminance(rgb):
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (lin(float(v)) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def pixels(page, box):
    shot = Image.open(io.BytesIO(page.screenshot())).convert("RGB")
    k = shot.width / page.viewport_size["width"]
    x0, y0, x1, y1 = [round(v * k) for v in box]
    return shot.crop((max(0, x0), max(0, y0), min(shot.width, x1), min(shot.height, y1)))


def wood_share(img):
    """Share of the sign's box painted in wood brown (warm, mid-dark): paper and navy are not."""
    px = list(img.getdata())
    brown = sum(1 for r, g, b in px if r > g > b and r - b >= 25 and 45 <= (r + g + b) / 3 <= 175)
    return brown / max(len(px), 1)


def face_contrast(img):
    """Contrast of the cream words against the face: the face is the median of the content box's
    pixels (the words cover a small share of it)."""
    px = sorted(img.getdata(), key=lambda c: sum(c))
    face = px[len(px) // 2]
    l1, l2 = luminance(CREAM), luminance(face)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05), face


def run_sign(browser):
    sizes = ((1440, 900), (1280, 720), (1024, 768), (390, 844))
    for name, path in PAGES.items():
        for size in sizes:
            tag = f"{name} {size[0]}x{size[1]}"
            phone = size[0] <= 720
            context, page, problems, signs = open_page(browser, path, size)
            page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(1200)
            g = page.evaluate(GEOMETRY)
            check(
                f"{tag}: one statement, in the footer, the exact words as real text",
                g["count"] == 1 and g["inFooter"] and g["text"] == STATEMENT,
                f"count {g['count']}, words {'ok' if g['text'] == STATEMENT else g['text'][:60]}",
            )
            check(f"{tag}: the words appear once on the page", g["mentions"] == 1, f"{g['mentions']}")
            if not g["sign"]:
                check(f"{tag}: the sign is there to measure", False)
                context.close()
                continue
            check(
                f"{tag}: Zilla Slab, loaded, 600, 15 px or more (the preview note too)",
                "Zilla Slab" in g["family"] and g["loaded"] and g["weight"] >= 600 and g["size"] >= 15 and g["noteSize"] >= 15,
                f"{g['family'][:30]}, loaded {g['loaded']}, {g['weight']}, {g['size']} px, note {g['noteSize']} px",
            )
            want = "fda-sign-phone.webp" if phone else "fda-sign.webp"
            loaded = any(st == 200 and want in u for st, u in signs)
            check(
                f"{tag}: the sign's picture ({want}) is the paragraph's border, and loads",
                want in g["image"] and all(b > 0 for b in g["borders"]) and loaded,
                f"border {[round(b) for b in g['borders']]}, responses {[(st, u.rsplit('/', 1)[-1]) for st, u in signs][:2]}",
            )
            share = wood_share(pixels(page, g["sign"]))
            check(f"{tag}: the sign is really painted (wood brown in its box)", share >= 0.25, f"{share:.0%} of its pixels")
            x0, y0, x1, y1 = g["sign"]
            bt, br, bb, bl = g["borders"]
            rl, rr = g["reach"]
            face = (x0 + bl - rl, y0 + bt, x1 - br + rr, y1 - bb)
            gl = g["glyphs"]
            check(
                f"{tag}: every line of the words inside the sign's face",
                gl and gl[0] >= face[0] - 1 and gl[2] <= face[2] + 1 and gl[1] >= face[1] - 1 and gl[3] <= face[3] + 1,
                f"words {[round(v) for v in gl] if gl else None}, face {[round(v) for v in face]}",
            )
            ratio, tone = face_contrast(pixels(page, (x0 + bl, y0 + bt, x1 - br, y1 - bb)))
            check(
                f"{tag}: cream words at 4.5:1 or more against the painted face",
                g["color"] == "rgb(246, 231, 189)" and ratio >= 4.5,
                f"{ratio:.2f}:1 against {tone}",
            )
            if size[0] >= 1280:
                check(f"{tag}: two lines, centred", g["lines"] == 2 and g["align"] == "center", f"{g['lines']} lines, {g['align']}")
            elif phone:
                check(f"{tag}: six lines at most on a phone, centred", g["lines"] <= 6 and g["align"] == "center", f"{g['lines']} lines")
            else:
                check(f"{tag}: three lines at most, centred", g["lines"] <= 3 and g["align"] == "center", f"{g['lines']} lines")
            check(f"{tag}: no sideways scroll", g["sideways"] <= 0, f"{g['sideways']} px")
            check(f"{tag}: no hairline in the footer's second tier", g["hairline"] == 0, f"{g['hairline']} px")
            if name in INK:
                note, legal, sign, foot, grid = g["note"], g["legal"], g["sign"], g["footer"], g["grid"]
                check(
                    f"{tag}: the sign under the copyright line, centred; the preview note last, under it",
                    note and legal
                    and sign[1] >= legal[3]
                    and abs((sign[0] + sign[2]) / 2 - (grid[0] + grid[2]) / 2) <= 2
                    and 0 <= note[1] - sign[3] <= 40
                    and foot[3] - note[3] <= 48,
                    f"© ends {legal[3]:.0f}, sign {sign[1]:.0f}-{sign[3]:.0f}, note {note[1]:.0f}-{note[3]:.0f}, "
                    f"footer end {foot[3]:.0f}" if note and legal else "no note or legal line",
                )
            page.screenshot(path=os.path.join(OUT, f"{name}-{size[0]}x{size[1]}.png"))
            check(f"{tag}: no errors", not problems, "; ".join(problems[:3]))
            context.close()


def run_last_screen(browser):
    """The sign is taller than the strip it replaced: the last screen must still show the whole
    promise and the whole crane at rest clear of the menu bar (the homepage's rounds 6 and 10),
    the sign drawing smaller on short windows."""
    for name in INK:
        for size in ((1280, 800), (1440, 900), (1536, 1000), (1280, 720), (1536, 864), (1366, 657), (1440, 700), (1920, 1080)):
            tag = f"{name} last screen {size[0]}x{size[1]}"
            context, page, _, _ = open_page(browser, PAGES[name], size)
            page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
            page.wait_for_timeout(900)
            crane, promise, header = page.evaluate(
                """[document.querySelector('footer img:not([alt=BiGH])').getBoundingClientRect().top,
                   document.querySelector('footer [data-brush=footer-promise] p').getBoundingClientRect().top,
                   document.querySelector('#site-navigation').getBoundingClientRect().bottom]"""
            )
            check(
                f"{tag}: the whole crane at rest and the whole promise, clear of the header",
                crane >= header + 8 and promise >= header + 8,
                f"crane top {crane:.0f}, promise top {promise:.0f}, header {header:.0f}",
            )
            context.close()


def run_elsewhere(browser):
    """The old-template product pages keep their own footer's statement (once); another language
    shows the sign too (its words stay in English until a translation lands)."""
    for path in OLD:
        context, page, _, _ = open_page(browser, path, (1440, 900))
        n = page.evaluate("document.body.innerText.split('Food and Drug Administration').length - 1")
        check(f"{path}: the statement once (the old template's footer)", n == 1, f"{n}")
        context.close()
    for path in ("/kr", "/vn/about"):
        context, page, problems, _ = open_page(browser, path, (1440, 900))
        page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(900)
        g = page.evaluate(GEOMETRY)
        check(
            f"{path}: the sign, its words, two lines",
            g["count"] == 1 and g["text"] == STATEMENT and g["lines"] == 2 and g["mentions"] == 1 and "fda-sign.webp" in g["image"],
            f"count {g['count']}, lines {g['lines']}",
        )
        check(f"{path}: no errors", not problems, "; ".join(problems[:3]))
        context.close()


with sync_playwright() as p:
    browser = p.chromium.launch(args=GPU)
    run_sign(browser)
    run_elsewhere(browser)
    run_last_screen(browser)
    browser.close()

passed = sum(1 for r in results if r[1])
print(f"\n{passed}/{len(results)} checks passed. Pictures: {OUT}")
sys.exit(0 if passed == len(results) else 1)
