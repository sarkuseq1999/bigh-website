"""The FDA statement at the foot of every page (Mo's pick, October 12, 2026: "A. Label strip").

On the ink pages (home, About, NuriCell) and the Science page: one statement, in the footer, the
exact words, bold, 15 px (and the preview note too), under one painted brush line that really
shows (pixels, a light line on the dark Science footer) and with none below (Mo, October 13, 2026:
fewer lines; no hairline in the footer either); one line on a 1280+ window, centred; left-aligned
on a phone; no sideways scroll. The ink footer: the statement under the copyright line, across
the column, and the preview note, the page's last line, under it (October 13, 2026: with the
promise under the logo the footer is short, so the note no longer needs the room beside it).
The words appear once per page (NuriCell no longer repeats them above the footer), also on the
four old-template product pages and in another language. The last screen still shows the whole
crane at rest and the whole promise clear of the menu bar on the short laptop windows, on every
ink page (the homepage's own QA checks the homepage the same way).

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
STRIP_PAGES = {"home": "/", "about": "/about", "nuricell": "/products/nuricell", "science": "/science"}
INK = ("home", "about", "nuricell")
OLD = ["/products/green-bee-propolis", "/products/advanced-opc", "/products/turmerific", "/products/nature-calm"]
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
    problems = []
    page.on("pageerror", lambda e: problems.append(str(e)))
    page.on(
        "response",
        lambda r: problems.append(f"{r.status} {r.url}") if "rule-lifted" in r.url and r.status >= 400 else None,
    )
    page.goto(BASE + path, wait_until="networkidle", timeout=120000)
    return context, page, problems


GEOMETRY = """(() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; };
  const strips = [...document.querySelectorAll('[data-fda]')];
  const strip = strips[0];
  const p = strip?.querySelector('p');
  const s = p && getComputedStyle(p);
  // Lines of words: the words' own line boxes (not the star's, which hangs outside the line on a
  // wide window and sits a little higher).
  const words = p ? [...p.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()) : [];
  const lines = new Set(words.flatMap(n => { const range = document.createRange(); range.selectNodeContents(n);
    return [...range.getClientRects()].filter(b => b.width > 2).map(b => Math.round(b.top)); })).size;
  const first = (() => { if (!words.length) return null; const range = document.createRange(); range.selectNodeContents(words[0]);
    const b = range.getClientRects()[0]; return b && [b.left, b.top, b.right, b.bottom]; })();
  const before = strip && getComputedStyle(strip, '::before');
  const after = strip && getComputedStyle(strip, '::after');
  const footer = document.querySelector('footer:last-of-type') || [...document.querySelectorAll('footer')].pop();
  const note = [...(footer?.querySelectorAll('p') || [])].find(e => e.textContent.startsWith('Educational content'));
  const legal = [...(footer?.querySelectorAll('span') || [])].find(e => e.textContent.startsWith('©'));
  const logo = footer?.querySelector('a[aria-label] img, img[alt=BiGH]');
  const grid = strip?.parentElement;
  return {
    count: strips.length,
    inFooter: !!strip && !!strip.closest('footer'),
    text: p ? p.textContent.replace(/^\\s*\\*\\s*/, '').trim() : '',
    star: p?.querySelector('span[aria-hidden]')?.textContent.trim(),
    weight: s ? parseInt(s.fontWeight) : 0,
    size: s ? parseFloat(s.fontSize) : 0,
    align: s?.textAlign,
    lines,
    rules: [before, after].map(c => c && { content: c.content, h: parseFloat(c.height), mask: c.maskImage || c.webkitMaskImage, op: parseFloat(c.opacity) }),
    hairline: grid ? parseFloat(getComputedStyle(grid).borderTopWidth) + parseFloat(getComputedStyle(grid).borderBottomWidth) : -1,
    noteSize: note ? parseFloat(getComputedStyle(note).fontSize) : 0,
    starBox: r(p?.querySelector('span[aria-hidden]')), first,
    strip: r(strip), footer: r(footer), note: r(note), legal: r(legal), logo: r(logo), grid: r(grid),
    mentions: document.body.innerText.split('Food and Drug Administration').length - 1,
    sideways: document.documentElement.scrollWidth - innerWidth,
    win: [innerWidth, innerHeight],
  };
})()"""


def inked(page, box, probe):
    """Share of the brush line's columns with paint: pixels that differ from the ground (sampled
    in the strip's padding just inside the line) by 25+ levels of grey."""
    x0, y0, x1, y1 = box
    shot = Image.open(io.BytesIO(page.screenshot())).convert("L")
    scale = shot.width / page.viewport_size["width"]
    ground = shot.crop([round(v * scale) for v in probe])
    values = sorted(ground.tobytes())
    bg = values[len(values) // 2]
    line = shot.crop([round(v * scale) for v in (x0, y0, x1, y1)])
    w, h = line.size
    px = line.load()
    cols = sum(1 for x in range(w) if any(abs(px[x, y] - bg) >= 25 for y in range(h)))
    return cols / max(w, 1)


def run_strip(browser):
    sizes = ((1440, 900), (1280, 720), (1024, 768), (390, 844))
    for name, path in STRIP_PAGES.items():
        for size in sizes:
            tag = f"{name} {size[0]}x{size[1]}"
            context, page, problems = open_page(browser, path, size)
            page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
            page.wait_for_timeout(900)
            g = page.evaluate(GEOMETRY)
            check(
                f"{tag}: one statement, in the footer, the exact words, the gold star hidden from readers",
                g["count"] == 1 and g["inFooter"] and g["text"] == STATEMENT and g["star"] == "*",
                f"count {g['count']}, words {'ok' if g['text'] == STATEMENT else g['text'][:60]}",
            )
            check(f"{tag}: the words appear once on the page", g["mentions"] == 1, f"{g['mentions']}")
            if not g["strip"]:
                check(f"{tag}: the strip is there to measure", False)
                context.close()
                continue
            check(
                f"{tag}: bold (600+), and it and the preview note 15 px or more (the site's smallest type)",
                g["weight"] >= 600 and g["size"] >= 15 and g["noteSize"] >= 15,
                f"{g['weight']}, {g['size']} px, note {g['noteSize']} px",
            )
            above, below = g["rules"]
            rule_ok = above and above["h"] >= 4 and "rule-lifted" in (above["mask"] or "") and above["op"] > 0.3
            x0, y0, x1, y1 = g["strip"]
            top = inked(page, (x0, y0, x1, y0 + 5), (x0 + 40, y0 + 7, x1 - 40, y0 + 9))
            # Under the words: paper only (October 13: one line above the statement, none below).
            bottom = inked(page, (x0, y1 - 5, x1, y1 + 4), (x0 + 40, y1 - 9, x1 - 40, y1 - 7))
            check(
                f"{tag}: one brush line painted across the strip above the words (the menu bar's stroke), none below",
                rule_ok and top >= 0.6 and below and below["content"] == "none" and bottom <= 0.05,
                f"painted columns: above {top:.0%}, below {bottom:.0%}",
            )
            check(f"{tag}: no hairline in the footer's second tier", g["hairline"] == 0, f"{g['hairline']} px")
            if size[0] >= 1280:
                check(f"{tag}: one line, centred", g["lines"] == 1 and g["align"] == "center", f"{g['lines']} lines, {g['align']}")
            elif size[0] <= 720:
                check(f"{tag}: left-aligned on a phone", g["align"] == "left", f"{g['align']}, {g['lines']} lines")
            else:
                check(f"{tag}: two lines at most, centred", g["lines"] <= 2 and g["align"] == "center", f"{g['lines']} lines")
            star, first = g["starBox"], g["first"]
            check(
                f"{tag}: the gold star before the first word, 4 px or more clear of it, on its line",
                star and first and first[0] - star[2] >= 4 and abs((star[1] + star[3]) / 2 - (first[1] + first[3]) / 2) <= 6,
                f"star {star and [round(v) for v in star]}, first word starts {first and round(first[0])}",
            )
            check(f"{tag}: no sideways scroll", g["sideways"] <= 0, f"{g['sideways']} px")
            if name in INK:
                note, legal, strip, logo, foot = g["note"], g["legal"], g["strip"], g["logo"], g["footer"]
                check(
                    f"{tag}: the statement under the copyright line, across the column; the preview note last, under it",
                    note and legal
                    and strip[1] >= legal[3]
                    and 0 <= note[1] - strip[3] <= 32
                    and foot[3] - note[3] <= 48
                    and abs((strip[2] - strip[0]) - (g["grid"][2] - g["grid"][0])) <= 2,
                    f"© ends {legal[3]:.0f}, strip {strip[1]:.0f}-{strip[3]:.0f}, note {note[1]:.0f}-{note[3]:.0f}, "
                    f"footer end {foot[3]:.0f}" if note and legal else "no note or legal line",
                )
            page.screenshot(path=os.path.join(OUT, f"{name}-{size[0]}x{size[1]}.png"))
            check(f"{tag}: no errors", not problems, "; ".join(problems[:3]))
            context.close()


def run_last_screen(browser):
    """The ink footer grew a line: the last screen must still begin with the whole promise and the
    whole crane at rest, clear of the menu bar (the homepage's rounds 6 and 10)."""
    for name in INK:
        for size in ((1280, 800), (1440, 900), (1536, 1000), (1280, 720), (1536, 864), (1366, 657), (1440, 700)):
            tag = f"{name} last screen {size[0]}x{size[1]}"
            context, page, problems = open_page(browser, STRIP_PAGES[name], size)
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
    shows the strip too (its words stay in English until a translation lands)."""
    for path in OLD:
        context, page, problems = open_page(browser, path, (1440, 900))
        n = page.evaluate("document.body.innerText.split('Food and Drug Administration').length - 1")
        check(f"{path}: the statement once (the old template's footer)", n == 1, f"{n}")
        context.close()
    for path in ("/kr", "/vn/about"):
        context, page, problems = open_page(browser, path, (1440, 900))
        page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
        page.wait_for_timeout(700)
        g = page.evaluate(GEOMETRY)
        check(
            f"{path}: the strip, its words, one line",
            g["count"] == 1 and g["text"] == STATEMENT and g["lines"] == 1 and g["mentions"] == 1,
            f"count {g['count']}, lines {g['lines']}",
        )
        check(f"{path}: no errors", not problems, "; ".join(problems[:3]))
        context.close()


with sync_playwright() as p:
    browser = p.chromium.launch(args=GPU)
    run_strip(browser)
    run_last_screen(browser)
    run_elsewhere(browser)
    browser.close()

passed = sum(1 for r in results if r[1])
print(f"\n{passed}/{len(results)} checks passed. Pictures: {OUT}")
sys.exit(0 if passed == len(results) else 1)
