"""Vietnamese type: Be Vietnam Pro for Vietnamese, Switzer for everything else (Mo, Sept 28, 2026).

Asks Chrome which fonts it really drew each text with (DevTools Protocol, CSS.getPlatformFontsForNode), for every
element with its own text on the page, after scrolling the whole page once so late text has been laid out.

- /vn, /vn/products/nuricell, /vn/about: the Vietnamese text is drawn in Be Vietnam Pro only (no Switzer, DM Sans
  or Arial glyphs), and the English h1 on /vn/about ("Be in Good Health.", lang="en") stays in Switzer. Symbols
  the face lacks (the "↑" of "Back to top") may fall back; they are listed, not failed. Chrome names the static
  weights "Be Vietnam Pro", "Be Vietnam Pro SemiBold" and so on.
- /, /products/nuricell, /about and Korean, Japanese and Chinese pages: no Be Vietnam Pro glyphs, and no Be Vietnam
  Pro face loaded (document.fonts), so the files are never downloaded there.
- --dump <file.json>: also writes the per-page glyph counts (compare a run before and after a type change).
- --shots <tag>: viewport shots (1440x900 and 390x844) of each /vn page's sections into out/vn-font/.

Usage: python -X utf8 scripts/qa/qa_vn_font.py [base-url] [--dump out.json] [--shots after]
"""

import json
import os
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = sys.argv[1:]


def option(name):
    return ARGS[ARGS.index(name) + 1] if name in ARGS else None


DUMP, SHOTS = option("--dump"), option("--shots")
POSITIONAL = [a for i, a in enumerate(ARGS) if not a.startswith("--") and (i == 0 or ARGS[i - 1] not in ("--dump", "--shots"))]
BASE = POSITIONAL[0] if POSITIONAL else "http://localhost:3009"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "vn-font")
os.makedirs(OUT, exist_ok=True)
VN = ("/vn", "/vn/products/nuricell", "/vn/about")
OTHERS = ("/", "/products/nuricell", "/about", "/kr", "/kr/about", "/jp", "/jp/products/nuricell", "/jp/about", "/cns", "/cns/about")
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + ("  [" + detail + "]" if detail else ""))


# Every element with its own visible text, tagged with its language (the nearest lang attribute).
TAG_TEXT = """() => {
  let n = 0; const out = [];
  for (const e of document.body.querySelectorAll('*')) {
    if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE', 'OPTION'].includes(e.tagName)) continue;
    if (![...e.childNodes].some(c => c.nodeType === 3 && c.textContent.trim())) continue;
    const r = e.getBoundingClientRect(); if (!r.width || !r.height) continue;
    const lang = e.closest('[lang]')?.lang ?? '';
    e.dataset.fontProbe = String(n++);
    const text = [...e.childNodes].filter(c => c.nodeType === 3).map(c => c.textContent).join('').trim();
    const symbols = [...text].filter(c => !/[\\p{L}\\p{M}\\p{N}\\p{P}\\s]/u.test(c)).length;
    out.push({ id: e.dataset.fontProbe, lang, symbols, tag: e.tagName.toLowerCase(), text: text.slice(0, 48) });
  }
  return out;
}"""


def settle(page):
    """Scroll the whole page once (scroll-driven text is laid out on the way), then back to the top."""
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    page.evaluate(
        """async () => { const step = innerHeight * 0.7;
            for (let y = 0; y < document.documentElement.scrollHeight; y += step) {
              window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
            window.scrollTo(0, 0); await document.fonts.ready; }"""
    )
    page.wait_for_timeout(600)


def fonts_by_element(page):
    """{language: {family: glyphs}} for every text on the page, plus the samples."""
    cdp = page.context.new_cdp_session(page)
    cdp.send("DOM.enable")
    cdp.send("CSS.enable")
    items = page.evaluate(TAG_TEXT)
    root = cdp.send("DOM.getDocument", {"depth": -1})["root"]["nodeId"]
    totals = {}
    samples = []
    for item in items:
        node = cdp.send("DOM.querySelector", {"nodeId": root, "selector": f'[data-font-probe="{item["id"]}"]'})["nodeId"]
        if not node:
            continue
        fonts = cdp.send("CSS.getPlatformFontsForNode", {"nodeId": node})["fonts"]
        bucket = totals.setdefault(item["lang"], {})
        for f in fonts:
            bucket[f["familyName"]] = bucket.get(f["familyName"], 0) + f["glyphCount"]
        samples.append({**item, "fonts": {f["familyName"]: f["glyphCount"] for f in fonts}})
    cdp.detach()
    return totals, samples


def probe(browser, path, w=1440, h=900):
    page = browser.new_page(viewport={"width": w, "height": h})
    page.goto(BASE + path, wait_until="networkidle")
    page.wait_for_timeout(1500)
    settle(page)
    totals, samples = fonts_by_element(page)
    info = page.evaluate(
        """() => ({ lang: document.documentElement.lang,
                  bodyFont: getComputedStyle(document.body).fontFamily,
                  h1Font: getComputedStyle(document.querySelector('h1') ?? document.body).fontFamily,
                  loaded: [...new Set([...document.fonts].filter(f => f.status === 'loaded')
                    .map(f => `${f.family} ${f.weight}`))].sort() })"""
    )
    page.close()
    return {"totals": totals, "samples": samples, **info}


def shoot(browser, path, tag):
    name = path.strip("/").replace("/", "-") or "home"
    for w, h, size in ((1440, 900, "desk"), (390, 844, "phone")):
        page = browser.new_page(viewport={"width": w, "height": h})
        page.goto(BASE + path, wait_until="networkidle")
        page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
        page.wait_for_timeout(2400)
        page.screenshot(path=os.path.join(OUT, f"{tag}-{name}-{size}-00.png"))
        # One shot per section heading, read where it sits a fifth of the way down the window.
        tops = page.evaluate(
            """() => [...document.querySelectorAll('main h2, main h3, footer')]
                .filter(e => e.getBoundingClientRect().width)
                .map(e => Math.round(e.getBoundingClientRect().top + scrollY - innerHeight * 0.2))"""
        )
        last = -10_000
        index = 1
        for y in sorted(tops):
            if y - last < h * 0.6:
                continue
            last = y
            page.evaluate(f"window.scrollTo(0, {y})")
            page.wait_for_timeout(1600)
            page.screenshot(path=os.path.join(OUT, f"{tag}-{name}-{size}-{index:02d}.png"))
            index += 1
        page.close()


def short(totals):
    return ", ".join(f"{k} {v}" for k, v in sorted(totals.items(), key=lambda kv: -kv[1]))


with sync_playwright() as p:
    browser = p.chromium.launch()
    report = {}
    for path in VN + OTHERS:
        report[path] = probe(browser, path)
        r = report[path]
        print(f"\n{path} lang={r['lang']}")
        for lang, fonts in r["totals"].items():
            print(f"  {lang or '-'}: {short(fonts)}")
        print(f"  faces loaded: {r['loaded']}")

    bvp = lambda family: family.startswith("Be Vietnam Pro")
    for path in VN:
        own = report[path]["totals"].get("vi", {})
        # Glyphs from another face, beyond the symbols the element holds, are letters or digits in the wrong face.
        wrong, symbols = [], []
        for s in report[path]["samples"]:
            other = sum(n for family, n in s["fonts"].items() if not bvp(family))
            if s["lang"] == "vi" and other:
                (symbols if other <= s["symbols"] else wrong).append(f"{s['text'][:24]!r} {s['fonts']}")
        check(
            f"{path}: Vietnamese text is drawn in Be Vietnam Pro only",
            any(bvp(f) for f in own) and not wrong,
            f"{short(own)}; wrong={wrong[:3]} symbols={symbols[:3]}",
        )
    en = report["/vn/about"]["totals"].get("en", {})
    check("/vn/about: the English h1 (lang=en) stays in Switzer", en and all(k.startswith("Switzer") for k in en), short(en))
    for path in OTHERS:
        r = report[path]
        drawn = {}
        for fonts in r["totals"].values():
            for family, n in fonts.items():
                drawn[family] = drawn.get(family, 0) + n
        loaded = [f for f in r["loaded"] if "vietnam" in f.lower()]
        check(f"{path}: no Be Vietnam Pro drawn or downloaded", not any(bvp(f) for f in drawn) and not loaded, f"{short(drawn)} loaded={loaded}")

    if DUMP:
        with open(DUMP, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=1)
        print(f"\nwrote {DUMP}")
    if SHOTS:
        for path in VN:
            shoot(browser, path, SHOTS)
        print(f"shots in {OUT}")
    browser.close()

print(f"\n{sum(results)} passed, {len(results) - sum(results)} failed")
