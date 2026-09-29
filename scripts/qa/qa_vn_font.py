"""Vietnamese type: Be Vietnam Pro for Vietnamese, Switzer for everything else (Mo, Sept 28, 2026).

Asks Chrome which fonts it really drew each text with (DevTools Protocol, CSS.getPlatformFontsForNode), for every
element with its own text on the page, after scrolling the whole page once so late text has been laid out.

- /vn, /vn/products/nuricell, /vn/about, /vn/science: the Vietnamese text is drawn in Be Vietnam Pro only (no
  Switzer, DM Sans or Arial glyphs), and the English h1 on /vn/about ("Be in Good Health.", lang="en") stays in
  Switzer. Symbols the face lacks (the "↑" of "Back to top") may fall back; they are listed, not failed. Chrome
  names the static weights "Be Vietnam Pro", "Be Vietnam Pro SemiBold" and so on.
- The same pages at 1440x900 and 390x844: no tone mark touches the line above or below. For every block of 20px+
  Vietnamese text on two or more lines, each glyph's ink box (its Range rect for origin and baseline, canvas
  measureText for its ink), and for every pair on consecutive lines that overlap sideways, the gap between them
  must be above 0. The Vietnamese leading rule (globals.css) only raises line-heights (switched off and on through
  CSSOM to compare) and changes nothing under 20px.
- /, /products/nuricell, /about, /science and Korean, Japanese and Chinese pages: no Be Vietnam Pro glyphs, no Be
  Vietnam Pro face loaded (document.fonts), so the files are never downloaded there, and the leading rule matches
  nothing.
- --dump <file.json>: also writes the per-page glyph counts (compare a run before and after a type change).
- --shots <tag>: viewport shots (1440x900 and 390x844) of each /vn page's sections into out/vn-font/.
- --pages /vn/science,/science: only these pages (in Git Bash, set MSYS_NO_PATHCONV=1).

Usage: python -X utf8 scripts/qa/qa_vn_font.py [base-url] [--dump out.json] [--shots after] [--pages a,b]
"""

import json
import os
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = sys.argv[1:]


def option(name):
    return ARGS[ARGS.index(name) + 1] if name in ARGS else None


DUMP, SHOTS, ONLY = option("--dump"), option("--shots"), option("--pages")
POSITIONAL = [a for i, a in enumerate(ARGS) if not a.startswith("--") and (i == 0 or ARGS[i - 1] not in ("--dump", "--shots", "--pages"))]
BASE = POSITIONAL[0] if POSITIONAL else "http://localhost:3009"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "vn-font")
os.makedirs(OUT, exist_ok=True)
VN = ("/vn", "/vn/products/nuricell", "/vn/about", "/vn/science")
OTHERS = ("/", "/products/nuricell", "/about", "/science", "/kr", "/kr/about", "/jp", "/jp/products/nuricell", "/jp/about", "/cns", "/cns/about")
if ONLY:
    VN = tuple(p for p in VN if p in ONLY.split(","))
    OTHERS = tuple(p for p in OTHERS if p in ONLY.split(","))
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


# The ink gap between consecutive lines of every block of 20px+ Vietnamese text (a heading or paragraph is one
# block, across the spans and split lines inside it). Glyph ink boxes: the Range rect gives the glyph's origin and
# its line's baseline (the rect spans the font's ascent + descent), canvas measureText gives the ink around them.
GAPS = r"""() => {
  const ctx = document.createElement('canvas').getContext('2d'); const metric = new Map();
  const blockOf = (el) => {
    let whole = null;
    for (let e = el; e && e !== document.body; e = e.parentElement) if (/^(H[1-6]|P|BLOCKQUOTE|FIGCAPTION|DD|DT)$/.test(e.tagName)) whole = e;
    if (whole) return whole;
    for (let e = el; e && e !== document.body; e = e.parentElement) if (!['inline', 'contents'].includes(getComputedStyle(e).display)) return e;
    return null;
  };
  const groups = new Map(); const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let node;
  while ((node = walker.nextNode())) {
    const el = node.parentElement; if (!el || !node.textContent.trim()) continue;
    if (el.closest('script, style, [aria-hidden="true"]') || el.closest('[lang]')?.lang !== 'vi') continue;
    const cs = getComputedStyle(el); const size = parseFloat(cs.fontSize);
    if (size < 20 || cs.visibility === 'hidden' || +cs.opacity === 0) continue;
    const block = blockOf(el); if (!block) continue;
    const font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`; ctx.font = font; const fm = ctx.measureText('x');
    const text = node.textContent;
    for (let i = 0; i < text.length; i++) {
      const ch = text[i]; if (!/[\p{L}\p{N}\p{P}\p{S}]/u.test(ch)) continue;
      const r = document.createRange(); r.setStart(node, i); r.setEnd(node, i + 1);
      const rect = [...r.getClientRects()].find(q => q.width > 0); if (!rect) continue;
      const key = font + '|' + ch;
      if (!metric.has(key)) { ctx.font = font; const m = ctx.measureText(ch); metric.set(key, [m.actualBoundingBoxAscent, m.actualBoundingBoxDescent, m.actualBoundingBoxLeft, m.actualBoundingBoxRight]); }
      const [asc, desc, left, right] = metric.get(key);
      const scale = rect.height / (fm.fontBoundingBoxAscent + fm.fontBoundingBoxDescent);
      const base = rect.top + fm.fontBoundingBoxAscent * scale;
      if (!groups.has(block)) groups.set(block, []);
      groups.get(block).push({ ch, base, top: base - asc * scale, bottom: base + desc * scale, l: rect.left - left * scale, r: rect.left + right * scale, size });
    }
  }
  const out = [];
  for (const [block, glyphs] of groups) {
    glyphs.sort((a, b) => a.base - b.base);
    const lines = [];
    for (const g of glyphs) { const last = lines[lines.length - 1]; if (last && g.base - last.base < g.size * 0.5) last.glyphs.push(g); else lines.push({ base: g.base, glyphs: [g] }); }
    let worst = null;
    for (let i = 0; i + 1 < lines.length; i++) for (const a of lines[i].glyphs) for (const b of lines[i + 1].glyphs) {
      if (a.l >= b.r || b.l >= a.r) continue;
      const gap = b.top - a.bottom; if (!worst || gap < worst.gap) worst = { gap, pair: a.ch + '/' + b.ch };
    }
    if (worst) out.push({ gap: +worst.gap.toFixed(1), pair: worst.pair, size: Math.round(parseFloat(getComputedStyle(block).fontSize)),
      text: block.textContent.trim().replace(/\s+/g, ' ').slice(0, 30) });
  }
  return out;
}"""

# The Vietnamese leading rule, switched off and on through CSSOM: what it matches, and whether it ever lowers a
# line-height or changes one under 20px.
RULE = """() => {
  let rule = null;
  for (const sheet of document.styleSheets) { let rules; try { rules = sheet.cssRules; } catch { continue; }
    for (const r of rules) if (r.selectorText && r.selectorText.includes('__faqItem') && r.style.lineHeight) rule = r; }
  if (!rule) return { found: false };
  const els = [...document.querySelectorAll('*')].filter(e => e.matches(rule.selectorText) && e.getClientRects().length);
  const read = () => els.map(e => { const cs = getComputedStyle(e); return [parseFloat(cs.fontSize), parseFloat(cs.lineHeight)]; });
  const on = read(); const value = rule.style.getPropertyValue('line-height'); const prio = rule.style.getPropertyPriority('line-height');
  rule.style.removeProperty('line-height'); const off = read(); rule.style.setProperty('line-height', value, prio);
  const lowered = [], small = [];
  els.forEach((e, i) => { const [size, a] = on[i]; const b = off[i][1];
    if (!isNaN(b) && a < b - 0.3) lowered.push(e.textContent.trim().slice(0, 24));
    if (size < 20 && Math.abs(a - b) > 0.3) small.push(e.textContent.trim().slice(0, 24)); });
  return { found: true, value, matched: els.length, lowered, small };
}"""


def leading(browser, path, w, h):
    """Ink gaps and the leading rule's effect, with reduced motion (every reveal settled, no line masks)."""
    ctx = browser.new_context(viewport={"width": w, "height": h}, reduced_motion="reduce")
    page = ctx.new_page()
    page.goto(BASE + path, wait_until="networkidle")
    settle(page)
    gaps = page.evaluate(GAPS)
    rule = page.evaluate(RULE)
    ctx.close()
    return gaps, rule


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
    if "/vn/about" in report:
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

    # The leading: no tone mark touches the next line, and the rule only ever raises Vietnamese display lines.
    for path in VN:
        for w, h in ((1440, 900), (390, 844)):
            gaps, rule = leading(browser, path, w, h)
            touching = [g for g in gaps if g["gap"] <= 0]
            worst = min(gaps, key=lambda g: g["gap"]) if gaps else None
            check(
                f"{path} {w}px: no tone mark touches the line above or below ({len(gaps)} multi-line blocks of 20px+)",
                gaps and not touching,
                f"touching={touching[:3]} smallest gap={worst}",
            )
            check(
                f"{path} {w}px: the Vietnamese leading rule only raises line-heights, and none under 20px",
                rule["found"] and rule["matched"] > 0 and not rule["lowered"] and not rule["small"],
                f"{rule}",
            )
    for path in OTHERS:
        _, rule = leading(browser, path, 1440, 900)
        check(f"{path}: the Vietnamese leading rule matches nothing", rule["found"] and rule["matched"] == 0, f"matched={rule.get('matched')}")

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
