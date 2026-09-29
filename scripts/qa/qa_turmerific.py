"""QA for the Turmerific product page (/products/turmerific), the first product after NuriCell.

At 1440x900 and 390x844, with motion and with reduced motion:
- chapters: overview, why, inside, research, daily, buy, in that order (no people: nobody at BiGH
  is credited with the formula), and the index numbers them 1 to 6
- overview: the big name reads "Turme" + "rific", the 3D bottle draws (data-status ready), the
  headline and the purpose (the approved homepage copy) are there
- why: the night picture (the turmeric roots, off and lit) is loaded, with the title, three lines
  and the source line; the eyebrow is the page's own ("From turmeric root"), so the buy chapter
  does not say "Advanced curcumin" twice
- inside: one ingredient, 1,000 mg, the label panel opens with the label form, the amount and the
  other ingredients
- research: six studies, oldest first, every link to PubMed in a new tab with rel=noopener
- daily: 30 days and "One bottle, one month."
- buy: the supply and directions lines and five questions
- words: never "Verdure", never "rat" or "rats", no "UCLA" claim beyond the approved purpose line
- everywhere: no sideways page scroll, no text under 15px except the calendar's capsule counts, no
  link or button under 44x44, no console errors, no failed requests
- the homepage links Turmerific to its page

Pictures: scripts/qa/out/tu-<run>-<chapter>-<n>.png, viewport shots walked down every chapter
(full-page shots break the svh layouts), and tu-<run>-sheet.png with a run's shots side by side.

    python -X utf8 scripts/qa/qa_turmerific.py http://localhost:3012 [--gpu]
"""
import os
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "http://localhost:3012").rstrip("/")
GPU = "--gpu" in sys.argv
ARGS = (
    ["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"]
    if GPU
    else ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
)
URL = f"{BASE}/products/turmerific"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
CHAPTERS = ["overview", "why", "inside", "research", "daily", "buy"]
passed = failed = 0


def check(name, ok, detail=""):
    global passed, failed
    passed += bool(ok)
    failed += not ok
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


def open_page(browser, url, w, h, reduced):
    ctx = browser.new_context(
        viewport={"width": w, "height": h}, reduced_motion="reduce" if reduced else "no-preference"
    )
    page = ctx.new_page()
    problems = []
    page.on(
        "console",
        lambda m: problems.append(f"console {m.text[:200]}")
        if m.type == "error" and "Failed to load resource" not in m.text
        else None,
    )
    page.on("pageerror", lambda e: problems.append(f"pageerror {e}"))
    page.on(
        "response",
        lambda r: problems.append(f"{r.status} {r.url[-90:]}")
        if r.status >= 400 and "/_next/static/chunks/" not in r.url
        else None,
    )
    response = page.goto(url, wait_until="networkidle")
    if not response or response.status >= 400:
        raise RuntimeError(f"{url} answered {response.status if response else 'nothing'}")
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    return ctx, page, problems


def glide(page, y, steps=8):
    current = page.evaluate("scrollY")
    for s in range(1, steps + 1):
        page.evaluate(f"window.scrollTo({{top: {current + (y - current) * s / steps}, behavior: 'instant'}})")
        page.wait_for_timeout(40)


SIZES = """(() => {
  const bad = [], tiny = [];
  const walker = document.createTreeWalker(document.querySelector('main') || document.body, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    const text = node.nodeValue.trim(), el = node.parentElement;
    if (!text || !el || el.closest('[class*="srOnly"], [aria-hidden="true"], [hidden]')) continue;
    if (el.closest('[data-chapter="daily"] ol')) continue; // the calendar's capsule counts
    const r = el.getBoundingClientRect();
    if (r.width <= 1 || r.height <= 1) continue;
    const size = parseFloat(getComputedStyle(el).fontSize);
    if (size < 15) bad.push(size + 'px "' + text.slice(0, 30) + '"');
  }
  for (const el of document.querySelectorAll('[data-chapter] a, [data-chapter] button')) {
    const r = el.getBoundingClientRect();
    if (!r.width || getComputedStyle(el).display === 'none' || el.closest('[hidden]')) continue;
    if (r.width < 44 || r.height < 44) tiny.push(Math.round(r.width) + 'x' + Math.round(r.height) + ' ' + el.textContent.trim().slice(0, 24));
  }
  return { bad: [...new Set(bad)].slice(0, 8), tiny: [...new Set(tiny)].slice(0, 8) };
})()"""


def content_checks(page, label):
    ids = page.evaluate("[...document.querySelectorAll('[data-chapter]')].map(s => s.dataset.chapter)")
    check(f"{label} chapters in order, no people", ids == CHAPTERS, str(ids))
    halves = page.evaluate("[...document.querySelectorAll('[data-giant-half]')].map(s => s.textContent)")
    check(f"{label} big name reads Turme|rific", halves == ["Turme", "rific"], str(halves))
    h1 = page.evaluate("document.querySelector('h1').textContent")
    check(f"{label} headline", "Turmeric," in h1 and "advanced by neuroscience." in h1, h1)
    text = page.evaluate("document.body.innerText")
    check(f"{label} purpose line", "Featuring Longvida® curcumin, developed with neuroscientists" in text)
    why = page.evaluate("document.querySelector('[data-chapter=\"why\"]').textContent")
    check(
        f"{label} why: title, lines and source",
        "A golden compound." in why
        and "very little of it reaches your bloodstream" in why
        and "tiny particles of fat" in why
        and "Nelson and colleagues" in why,
        why[:80].replace("\n", " "),
    )
    pictures = page.evaluate(
        "[...document.querySelectorAll('[data-chapter=\"why\"] img')].map(i => [i.currentSrc.includes('why-root-o'), i.complete && i.naturalWidth > 0])"
    )
    check(f"{label} why: both root pictures load", len(pictures) >= 2 and all(a and b for a, b in pictures), str(pictures))
    buy_head = page.evaluate("[...document.querySelectorAll('[data-chapter=\"buy\"] p')].slice(0, 2).map(p => p.textContent)")
    check(f"{label} buy: eyebrow and focus differ", len(buy_head) == 2 and buy_head[0] != buy_head[1], str(buy_head))
    rows = page.evaluate("[...document.querySelectorAll('[data-chapter=\"inside\"] ol li')].map(li => li.innerText.replace(/\\s+/g, ' '))")
    check(f"{label} inside: one ingredient, 1,000 mg", len(rows) == 1 and "1,000" in rows[0] and "mg" in rows[0], str(rows))
    page.locator("[data-chapter='inside'] button", has_text="See the full label").click()
    page.wait_for_timeout(300)
    panel = page.evaluate("[...document.querySelectorAll('[data-chapter=\"inside\"] table')].map(t => t.closest('div').innerText).join(' ')")
    check(
        f"{label} label panel",
        "Longvida® Optimised Curcumin Extract" in panel and "1,000 mg" in panel and "sunflower lecithin" in panel,
        panel[:80].replace("\n", " "),
    )
    studies = page.evaluate(
        "[...document.querySelectorAll('[data-chapter=\"research\"] [data-study]')].map(li => [li.querySelector('p').textContent.trim(), li.querySelector('a')?.target, li.querySelector('a')?.rel, li.querySelector('a')?.href])"
    )
    years = [int(s[0]) for s in studies]
    check(f"{label} research: 6 studies, oldest first", len(studies) == 6 and years == sorted(years), str(years))
    check(
        f"{label} research: PubMed links, new tab, noopener",
        all(t == "_blank" and "noopener" in (r or "") and h.startswith("https://pubmed.ncbi.nlm.nih.gov/") for _, t, r, h in studies),
    )
    daily = page.evaluate("(() => { const s = document.querySelector('[data-chapter=\"daily\"]'); return [s.querySelectorAll('ol > li').length, s.querySelector('h2').textContent]; })()")
    check(f"{label} daily: 30 days, one month", daily == [30, "One bottle, one month."], str(daily))
    buy = page.evaluate("document.querySelector('[data-chapter=\"buy\"]').innerText")
    faq = page.evaluate("document.querySelectorAll('[data-chapter=\"buy\"] details, [data-chapter=\"buy\"] [aria-expanded]').length")
    check(
        f"{label} buy: supply, directions, five questions",
        "60 vegetarian capsules · 30 servings" in buy and "Take 1 to 2 capsules a day" in buy and faq >= 5,
        f"questions {faq}",
    )
    html = page.content()
    check(f"{label} never names the ingredient's maker", "verdure" not in html.lower())
    words = page.evaluate("document.body.innerText.toLowerCase()")
    check(f"{label} no 'rat' or 'rats'", not any(w in words.replace(".", " ").replace(",", " ").split() for w in ("rat", "rats")))
    check(f"{label} UCLA only in the approved line", words.count("university of california") == 1 and "ucla" not in words)


def walk(page, run, w, h, shots):
    """Viewport shots down every chapter: its top, then a screen at a time (at most six)."""
    for chapter in CHAPTERS:
        where = page.evaluate(
            f"(() => {{ const s = document.querySelector('[data-chapter=\"{chapter}\"]'); const r = s.getBoundingClientRect(); return [Math.round(r.top + scrollY), s.offsetHeight]; }})()"
        )
        top, height = where
        stops = max(1, min(6, round(height / h)))
        for i in range(stops):
            y = top + (height - h) * (i / max(1, stops - 1)) if stops > 1 else top
            glide(page, y)
            page.wait_for_timeout(900)
            if not page.evaluate("document.documentElement.scrollWidth <= innerWidth"):
                check(f"{run} {chapter} {i}: no sideways scroll", False)
            path = os.path.join(OUT, f"tu-{run}-{chapter}-{i}.png")
            page.screenshot(path=path)
            shots.append(path)


def sheet(run, shots, scale):
    images = [Image.open(p).convert("RGB") for p in shots]
    images = [im.resize((int(im.width * scale), int(im.height * scale))) for im in images]
    per_row = 5
    rows = [images[i : i + per_row] for i in range(0, len(images), per_row)]
    width = max(sum(im.width + 10 for im in row) for row in rows)
    height = sum(max(im.height for im in row) + 10 for row in rows)
    canvas = Image.new("RGB", (width, height), (40, 44, 52))
    y = 0
    for row in rows:
        x = 0
        for im in row:
            canvas.paste(im, (x, y))
            x += im.width + 10
        y += max(im.height for im in row) + 10
    path = os.path.join(OUT, f"tu-{run}-sheet.png")
    canvas.save(path)
    return path


with sync_playwright() as p:
    browser = p.chromium.launch(args=ARGS)
    for w, h, reduced in [(1440, 900, False), (390, 844, False), (1440, 900, True), (390, 844, True)]:
        run = f"{'desk' if w > 900 else 'phone'}{'-still' if reduced else ''}"
        ctx, page, problems = open_page(browser, URL, w, h, reduced)
        page.wait_for_timeout(1500)
        try:
            page.wait_for_selector(
                "[data-chapter='overview'] [data-status='ready'], [data-chapter='overview'] [data-status='flat']",
                timeout=20000,
            )
        except Exception:
            pass
        status = page.evaluate("document.querySelector('[data-chapter=\"overview\"] [data-status]').dataset.status")
        check(f"{run} 3D bottle draws", status == "ready", status)
        shots = []
        page.wait_for_timeout(2500)
        walk(page, run, w, h, shots)
        content_checks(page, run)
        sizes = page.evaluate(SIZES)
        check(f"{run} no text under 15px", not sizes["bad"], "; ".join(sizes["bad"]))
        check(f"{run} links and buttons at least 44x44", not sizes["tiny"], "; ".join(sizes["tiny"]))
        check(f"{run} no console errors or failed requests", not problems, "; ".join(problems[:4]))
        print("sheet", sheet(run, shots, 0.4 if w > 900 else 0.6))
        ctx.close()

    ctx, page, problems = open_page(browser, BASE + "/", 1440, 900, False)
    links = page.evaluate("[...document.querySelectorAll('a[href*=\"/products/turmerific\"]')].length")
    check("homepage links Turmerific to its page", links >= 1, f"{links} links")
    ctx.close()
    browser.close()

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
