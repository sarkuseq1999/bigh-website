"""QA for the homepage, "Ink & Gold" with the crane (Mo's pick, October 2, 2026).

The homepage at / (and /kr). On the real GPU (ANGLE/D3D11):
  - desktop 1440x900 (full run) and phone 390x844 (full run):
    the page answers 200; no page errors, console errors or failed requests; the blocks in order
    (top, cellular, scientists, products, stories, science, research, purpose, then the footer);
    one h1; the header's links; the opening's paintings loaded and its words clear of each other;
    the brush line draws itself (ink on the canvas, its progress grows with the scroll, it is past
    the purpose's painting there, and it ends at the very bottom as the stroke under the footer's
    promise); Dr. Liu and Ask BiGH Science dialogs open and close; Dr. Liu's photo never shown
    past its own pixels; the products: five real bottles, choosing a name shows its words, a
    bottle picture links to its own product page, Discover NuriCell links to its page; the stories say
    "Fictional sample" and "Illustration" and a name chooses a story; science: three topics, the
    age slider ages the cell and "Illustration, not a measurement" shows; research: filters and
    show all; no sideways scrolling; every image loads; text at least 15 px (reading text at least
    17 px); buttons and links at least 44 px tall.
  - desktop 1280x720: the opening holds (headline, intro and pills inside the window, clear of
    the paintings' words), no sideways scrolling.
  - Korean (/kr, desktop and phone): the blocks, no sideways scrolling, no errors.
  - reduced motion: the whole brush line from the first frame (ink down at the research spine),
    every painting shown, no errors.
  - phones: the opening keeps its own line; no stray strokes below it (the page line is
    desktop-only, the lead's decision of October 2) until the closing stroke under the footer's
    promise, which every screen gets (October 3).

Pictures: scripts/qa/out/home-ink/<page>-<tag>-NN-<block>.png (viewport shots).

Usage: python -X utf8 scripts/qa/qa_home_ink.py [base-url]
"""

import os
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = (ARGS[0] if ARGS else "http://localhost:3014").rstrip("/")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "home-ink")
os.makedirs(OUT, exist_ok=True)
GPU = ["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"]
BLOCKS = ["top", "cellular", "scientists", "products", "stories", "science", "research", "purpose"]
ROOT = "[data-look=ink]"
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


def scroll_to(page, y, wait=700):
    page.evaluate(f"window.scrollTo(0, {int(y)})")
    page.wait_for_timeout(wait)


def top_of(page, selector):
    return page.evaluate(
        f"(() => {{ const e = document.querySelector({selector!r}); return e ? e.getBoundingClientRect().top + scrollY : -1; }})()"
    )


def open_page(browser, url, size, mobile, reduced=False):
    context = browser.new_context(
        viewport={"width": size[0], "height": size[1]},
        device_scale_factor=1,
        is_mobile=mobile,
        has_touch=mobile,
        reduced_motion="reduce" if reduced else "no-preference",
    )
    page = context.new_page()
    problems = []
    page.on("pageerror", lambda e: problems.append(f"pageerror: {e}"))
    page.on(
        "console",
        lambda m: problems.append(f"console {m.type}: {m.text[:160]}") if m.type == "error" else None,
    )
    page.on(
        "requestfailed",
        lambda r: problems.append(f"failed: {r.url[-90:]} {r.failure}")
        if "/_next/webpack-hmr" not in r.url
        else None,
    )
    page.on(
        "response",
        lambda r: problems.append(f"{r.status}: {r.url[-90:]}") if r.status >= 400 else None,
    )
    response = page.goto(url, wait_until="networkidle", timeout=120000)
    page.add_style_tag(content="[data-look-switcher]{display:none!important}")
    page.wait_for_timeout(4500)
    return context, page, response, problems


def shoot(page, name):
    page.screenshot(path=os.path.join(OUT, f"{name}.png"))


def dialog_title(page):
    if not page.evaluate("document.querySelector('dialog')?.open === true"):
        return ""
    return page.locator("#home-dialog-title").text_content()


def close_dialog(page):
    page.click("dialog button[aria-label='Close details']")
    page.wait_for_timeout(450)
    return page.evaluate("document.querySelector('dialog')?.open === false")


def progress(page):
    return float(page.evaluate("+(document.querySelector('[data-brush-layer]')?.dataset.progress || 0)"))


def ink_in_view(page):
    """Dark pixels painted on the brush tiles inside the window."""
    return page.evaluate(
        """(() => {
          let ink = 0;
          for (const c of document.querySelectorAll('[data-brush-layer] canvas')) {
            if (!c.width) continue;
            const b = c.getBoundingClientRect();
            const top = Math.max(0, -b.top), bottom = Math.min(b.height, innerHeight - b.top);
            if (bottom <= top) continue;
            const k = c.width / b.width;
            const data = c.getContext('2d').getImageData(0, Math.floor(top * k), c.width, Math.max(1, Math.floor((bottom - top) * k))).data;
            for (let i = 3; i < data.length; i += 16) if (data[i] > 120) ink++;
          }
          return ink;
        })()"""
    )


def page_checks(page, tag, width, view_h, problems):
    """Images, sideways scrolling, sizes, targets, errors, after scrolling the whole page."""
    total = page.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < total:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(110)
        y += view_h // 2
    page.wait_for_timeout(1500)
    broken = page.evaluate(
        "[...document.querySelectorAll('img')].filter(i => i.getClientRects().length > 0 && (!i.complete || i.naturalWidth === 0)).map(i => i.currentSrc || i.src)"
    )
    check(f"{tag}: every image loads", not broken, str(broken[:4]))
    wide = page.evaluate("document.documentElement.scrollWidth")
    check(f"{tag}: no sideways scrolling", wide <= width, f"scrollWidth {wide}")
    small = page.evaluate(
        f"""(() => {{
          const out = [];
          const walker = document.createTreeWalker(document.querySelector('{ROOT}'), NodeFilter.SHOW_TEXT);
          while (walker.nextNode()) {{
            const node = walker.currentNode;
            const text = node.textContent.trim();
            if (!text) continue;
            const el = node.parentElement;
            if (el.closest('[data-look-switcher], [aria-hidden=true], dialog, [class*=visuallyHidden], option, select, header [role=status]')) continue;
            const style = getComputedStyle(el);
            if (style.display === 'none' || style.visibility === 'hidden') continue;
            const box = el.getBoundingClientRect();
            if (!box.width || !box.height) continue;
            const size = parseFloat(style.fontSize);
            if (size < 15) out.push(`${{size}}px ${{text.slice(0, 40)}}`);
            else if (text.length > 70 && size < 17 && !el.closest('footer')) out.push(`${{size}}px body ${{text.slice(0, 40)}}`);
          }}
          return out;
        }})()"""
    )
    check(f"{tag}: text sizes (>=15 px, reading text >=17 px)", not small, "; ".join(small[:5]))
    tiny = page.evaluate(
        """[...document.querySelectorAll('main a, main button, main summary, main input')]
          .filter(e => { const b = e.getBoundingClientRect(); const s = getComputedStyle(e);
            return b.width && s.visibility !== 'hidden' && !e.closest('[inert]') && b.height < 44; })
          .map(e => `${Math.round(e.getBoundingClientRect().height)}px ${(e.textContent || e.getAttribute('aria-label') || '').trim().slice(0, 30)}`)"""
    )
    check(f"{tag}: buttons and links at least 44 px tall", not tiny, "; ".join(tiny[:5]))
    check(f"{tag}: no errors or failed requests", not problems, "; ".join(problems[:4]))


def run(browser, look, mobile):
    tag = f"{look} {'phone' if mobile else 'desk'}"
    name = f"{look}-{'phone' if mobile else 'desk'}"
    width, view_h = (390, 844) if mobile else (1440, 900)
    url = f"{BASE}/"
    context, page, response, problems = open_page(browser, url, (width, view_h), mobile)
    check(f"{tag}: answers 200", response and response.status == 200, str(response and response.status))

    ids = page.evaluate("[...document.querySelectorAll('main > section[id]')].map(s => s.id)")
    check(f"{tag}: blocks in order", ids == BLOCKS, ",".join(ids))
    check(f"{tag}: footer present", page.locator("footer").count() >= 1)
    check(f"{tag}: one h1", page.locator("h1").count() == 1)

    # Header links.
    if mobile:
        page.click("button[aria-controls='home-navigation']")
        page.wait_for_timeout(300)
    nav = page.evaluate(
        "[...document.querySelectorAll('#home-navigation > a')].map(a => [a.textContent.trim(), a.getAttribute('href')])"
    )
    hrefs = {text: href for text, href in nav}
    check(
        f"{tag}: header links",
        hrefs.get("Products") == "#products"
        and (hrefs.get("Science") or "").endswith("/science")
        and (hrefs.get("About") or "").endswith("/about")
        and page.locator("#home-navigation button", has_text="Support").count() == 1,
        str(nav),
    )
    if mobile:
        page.click("button[aria-controls='home-navigation']")
        page.wait_for_timeout(300)

    # The opening: paintings loaded, words clear of each other, the brush line leaving it.
    art = page.evaluate(
        "[...document.querySelectorAll('#top img')].map(i => i.complete && i.naturalWidth > 0)"
    )
    check(f"{tag}: the opening's paintings have loaded", art and all(art), str(art))
    boxes = page.evaluate(
        """[...document.querySelectorAll('#top h1, #top p, #top a, #top button')].map(e => {
            const b = e.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; })"""
    )
    overlaps = [
        (a, b)
        for i, a in enumerate(boxes)
        for b in boxes[i + 1 :]
        if a[0] < b[2] - 1 and b[0] < a[2] - 1 and a[1] < b[3] - 1 and b[1] < a[3] - 1
    ]
    inside = all(b[0] >= 0 and b[2] <= width for b in boxes)
    check(f"{tag}: the opening's words sit clear, inside the window", not overlaps and inside, f"{len(overlaps)} overlaps")
    start_ink = ink_in_view(page)
    start_progress = progress(page)
    # Desktop: the page line starts in the opening and draws on. Phones (lead's decision, October
    # 2): the opening keeps its own line, drawn in full; there is no page line below it until the
    # closing stroke under the footer's promise (October 3), so the opening is a small part of
    # the whole route on every screen.
    check(
        f"{tag}: the brush line leaves the opening",
        start_ink > 40 and 0 < start_progress < 0.3,
        f"ink {start_ink}, progress {start_progress:.3f}",
    )
    shoot(page, f"{name}-00-top")

    # Tiny power plants.
    scroll_to(page, top_of(page, "#cellular") + (0 if mobile else 40), 2200)
    mid_progress = progress(page)
    if mobile:
        stray = ink_in_view(page)
        check(f"{tag}: no stray brush strokes below the opening", stray == 0, f"ink {stray}")
    else:
        check(
            f"{tag}: the brush line draws on as the page scrolls",
            mid_progress > start_progress and ink_in_view(page) > 40,
            f"{start_progress:.3f} -> {mid_progress:.3f}",
        )
    lines = page.locator("#cellular ol li").count()
    check(f"{tag}: three numbered lines", lines == 3, str(lines))
    shoot(page, f"{name}-01-cellular")

    # Scientists and dialogs.
    scroll_to(page, top_of(page, "#scientists") + (40 if mobile else 0), 1200)
    shoot(page, f"{name}-02-scientists")
    facts = page.locator("#scientists dl > div").count()
    check(f"{tag}: Dr. Liu's three facts", facts == 3, str(facts))
    page.locator("#scientists button", has_text="Get to know Dr. Liu").click()
    page.wait_for_timeout(500)
    title = dialog_title(page)
    check(f"{tag}: Dr. Liu dialog opens and closes", "Liu" in (title or "") and close_dialog(page), title or "")
    page.locator("#scientists button", has_text="Discover Ask BiGH Science").click()
    page.wait_for_timeout(450)
    ask = dialog_title(page)
    page.keyboard.press("Escape")
    page.wait_for_timeout(450)
    check(
        f"{tag}: Ask BiGH Science dialog opens and closes",
        ask == "Ask BiGH Science" and page.evaluate("!document.querySelector('dialog').open"),
        ask or "",
    )
    liu = page.evaluate(
        """(() => { const i = document.querySelector('#scientists img[alt="Dr. Jiankang Liu"]');
          return [i.naturalWidth, Math.round(i.getBoundingClientRect().width)]; })()"""
    )
    check(f"{tag}: Dr. Liu's photo shown at a sharp size", liu[0] >= liu[1], f"natural {liu[0]} shown {liu[1]} css px")
    iris = page.locator("#scientists", has_text="Dr. Iris Wang").count()
    iris_photo = page.locator("#scientists img[alt*='Iris']").count()
    check(f"{tag}: Dr. Iris Wang in words only", iris == 1 and iris_photo == 0)

    # Products.
    scroll_to(page, top_of(page, "#products [data-brush=bottles]") - (160 if mobile else 260), 1200)
    shoot(page, f"{name}-03-products")
    bottles = page.evaluate(
        "[...document.querySelectorAll('#products [data-brush=bottles] img')].filter(i => i.src.includes('products') && i.complete && i.naturalWidth > 0).length"
    )
    check(f"{tag}: five real bottles", bottles == 5, str(bottles))
    page.locator("#products button[aria-pressed]", has_text="Turmerific").click()
    page.wait_for_timeout(900)
    headline = page.locator("#ink-product-panel h3").text_content()
    credit = page.locator("#ink-product-panel").text_content()
    check(
        f"{tag}: choosing a name shows its words and credit",
        "turmeric" in headline.lower() and "Longvida" in credit,
        headline,
    )
    # Since all five products have their own page (main, October 2026), every bottle picture links
    # to it; a product without a page would open its preview dialog instead (ProductAction).
    bottle_links = page.evaluate(
        "[...document.querySelectorAll('#products [data-brush=bottles] a')].map(a => a.getAttribute('href'))"
    )
    expected = ["nuricell", "green-bee-propolis", "advanced-opc", "turmerific", "nature-calm"]
    check(
        f"{tag}: every bottle picture links to its product page",
        all(any((h or "").endswith(f"/products/{slug}") for h in bottle_links) for slug in expected),
        str(bottle_links),
    )
    page.locator("#products button[aria-pressed]", has_text="NuriCell").click()
    page.wait_for_timeout(600)
    discover = page.locator("#ink-product-panel a", has_text="Discover NuriCell").get_attribute("href")
    picture = page.locator("#products [data-brush=bottles] a").first.get_attribute("href")
    check(
        f"{tag}: NuriCell's picture and Discover link to its page",
        (discover or "").endswith("/products/nuricell") and (picture or "").endswith("/products/nuricell"),
        f"{discover} | {picture}",
    )

    # Stories.
    scroll_to(page, top_of(page, "#stories article") - (120 if mobile else 220), 1200)
    shoot(page, f"{name}-04-stories")
    sample = page.locator("#stories article").text_content()
    caption = page.locator("#stories figure figcaption").text_content()
    check(f"{tag}: the story says Fictional sample", "Fictional sample" in sample, sample[:40])
    check(f"{tag}: the painting is labelled Illustration", "Illustration" in caption, caption)
    page.locator("#stories button[aria-pressed]", has_text="Michael R.").click()
    page.wait_for_timeout(1200)
    quote_title = page.locator("#stories article h3").text_content()
    check(f"{tag}: a name chooses its story", "read up" in quote_title, quote_title)

    # Science.
    scroll_to(page, top_of(page, "#science") + (0 if mobile else 40), 1500)
    shoot(page, f"{name}-05-science")
    page.click("#science [role=tab]:has-text('Free radicals')")
    page.wait_for_timeout(1300)
    radicals = page.locator("#science [role=tabpanel] h3").text_content()
    page.click("#science [role=tab]:has-text('Aging cells')")
    page.wait_for_timeout(1300)
    aging = page.locator("#science [role=tabpanel] h3").text_content()
    page.evaluate(
        """(() => { const input = document.querySelector('#science input[type=range]');
          const set = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
          set.call(input, '70'); input.dispatchEvent(new Event('input', { bubbles: true })); })()"""
    )
    page.wait_for_timeout(1200)
    age = page.locator("#science label strong").first.text_content()
    honesty = page.evaluate(
        "(() => { const e = [...document.querySelectorAll('#science p')].find(s => s.textContent.includes('Illustration, not a measurement')); if (!e) return 0; return +getComputedStyle(e.parentElement).opacity; })()"
    )
    aged = float(
        page.evaluate(
            "(() => { const i = [...document.querySelectorAll('#science img')].find(i => i.src.includes('mito-aged')); return i ? +getComputedStyle(i).opacity : 0; })()"
        )
    )
    if mobile:
        scroll_to(page, top_of(page, "#science figure") - 90, 900)
    shoot(page, f"{name}-06-science-age")
    check(
        f"{tag}: three topics switch the words",
        "free radicals" in radicals.lower() and "age" in aging.lower(),
        f"{radicals} | {aging}",
    )
    check(
        f"{tag}: the age slider ages the cell; honesty label shown",
        age == "70" and honesty > 0.9 and 0.7 < aged < 0.9,
        f"age {age}, label {honesty}, aged {aged:.2f}",
    )
    page.click("#science [role=tab]:has-text('Mitochondria')")

    # Research.
    scroll_to(page, top_of(page, "#research") + (0 if mobile else 40), 900)
    shoot(page, f"{name}-07-research")
    page.click("#research button[aria-pressed]:has-text('Ingredients')")
    page.wait_for_timeout(300)
    first = page.locator("#research ul > li").count()
    page.click("#research button[aria-expanded]")
    page.wait_for_timeout(300)
    every = page.locator("#research ul > li").count()
    page.click("#research button[aria-pressed]:has-text('Guides')")
    page.wait_for_timeout(300)
    page.click("#research button[aria-expanded]")
    page.wait_for_timeout(300)
    guides = page.locator("#research ul > li").count()
    page.locator("#research summary").first.click()
    page.wait_for_timeout(300)
    opened_row = page.evaluate("document.querySelector('#research details').open")
    note = page.locator("#research", has_text="do not establish the effects").count()
    check(
        f"{tag}: research filters, show all and the note",
        first == 6 and every == 17 and guides == 10 and opened_row and note == 1,
        f"first {first} all {every} guides {guides}",
    )
    page.click("#research button[aria-pressed]:has-text('All')")

    # Purpose: the brush line lifts off in the closing painting (the rest of its route is the
    # lifted travel to the footer and the closing stroke).
    scroll_to(page, top_of(page, "#purpose") + (0 if mobile else 40), 2600)
    shoot(page, f"{name}-08-purpose")
    scroll_to(page, top_of(page, "#purpose") + 500, 2600)
    end_progress = progress(page)
    check(f"{tag}: the brush line reaches the purpose", end_progress > 0.88, f"progress {end_progress:.3f}")
    # The footer: the line comes to rest as one stroke under the promise.
    scroll_to(page, page.evaluate("document.documentElement.scrollHeight"), 2600)
    rest_progress = progress(page)
    stroke = page.evaluate(
        """(() => {
          const t = document.querySelector('[data-brush="footer-tagline"]');
          if (!t) return -1;
          const b = t.getBoundingClientRect();
          let ink = 0;
          for (const c of document.querySelectorAll('[data-brush-layer] canvas')) {
            if (!c.width) continue;
            const r = c.getBoundingClientRect();
            const k = c.width / r.width;
            const y0 = Math.max(0, b.bottom - 6 - r.top), y1 = Math.min(r.height, b.bottom + 40 - r.top);
            if (y1 <= y0) continue;
            const x0 = Math.max(0, b.left - 30 - r.left), x1 = Math.min(r.width, b.right + 30 - r.left);
            const data = c.getContext('2d').getImageData(Math.floor(x0 * k), Math.floor(y0 * k), Math.max(1, Math.floor((x1 - x0) * k)), Math.max(1, Math.floor((y1 - y0) * k))).data;
            for (let i = 3; i < data.length; i += 16) if (data[i] > 120) ink++;
          }
          return ink;
        })()"""
    )
    check(
        f"{tag}: the brush line ends as the stroke under the footer's promise",
        rest_progress >= 0.999 and stroke > 40,
        f"progress {rest_progress:.3f}, ink under the promise {stroke}",
    )
    shoot(page, f"{name}-09-footer")

    page_checks(page, tag, width, view_h, problems)
    context.close()


def run_short(browser, look):
    """1280 x 720: the opening holds at a short laptop window."""
    tag = f"{look} 1280x720"
    context, page, response, problems = open_page(browser, f"{BASE}/", (1280, 720), False)
    boxes = page.evaluate(
        """[...document.querySelectorAll('#top h1, #top p, #top a, #top button')].map(e => {
            const b = e.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; })"""
    )
    inside = all(b[0] >= 0 and b[2] <= 1280 and b[1] >= 84 and b[3] <= 720 for b in boxes)
    overlaps = [
        1
        for i, a in enumerate(boxes)
        for b in boxes[i + 1 :]
        if a[0] < b[2] - 1 and b[0] < a[2] - 1 and a[1] < b[3] - 1 and b[1] < a[3] - 1
    ]
    check(f"{tag}: the opening's words fit the window, clear of each other", inside and not overlaps, str([[round(v) for v in b] for b in boxes]))
    shoot(page, f"{look}-1280-00-top")
    wide = page.evaluate("document.documentElement.scrollWidth")
    check(f"{tag}: no sideways scrolling", wide <= 1280, f"scrollWidth {wide}")
    check(f"{tag}: no errors", not problems, "; ".join(problems[:3]))
    context.close()


def run_korean(browser, mobile):
    tag = f"kr {'phone' if mobile else 'desk'}"
    size = (390, 844) if mobile else (1440, 900)
    context, page, response, problems = open_page(browser, f"{BASE}/kr", size, mobile)
    check(f"{tag}: answers 200", response and response.status == 200)
    ids = page.evaluate("[...document.querySelectorAll('main > section[id]')].map(s => s.id)")
    check(f"{tag}: blocks in order", ids == BLOCKS, ",".join(ids))
    shoot(page, f"kr-{'phone' if mobile else 'desk'}-00-top")
    scroll_to(page, top_of(page, "#scientists"), 1200)
    shoot(page, f"kr-{'phone' if mobile else 'desk'}-01-scientists")
    scroll_to(page, top_of(page, "#products"), 1200)
    shoot(page, f"kr-{'phone' if mobile else 'desk'}-02-products")
    total = page.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < total:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(90)
        y += size[1] // 2
    wide = page.evaluate("document.documentElement.scrollWidth")
    check(f"{tag}: no sideways scrolling", wide <= size[0], f"scrollWidth {wide}")
    check(f"{tag}: no errors", not problems, "; ".join(problems[:3]))
    context.close()


def run_reduced(browser, look):
    tag = f"{look} reduced motion"
    context, page, response, problems = open_page(browser, f"{BASE}/", (1440, 900), False, reduced=True)
    whole = progress(page)
    shoot(page, f"{look}-reduced-00-top")
    hidden = page.evaluate(
        "[...document.querySelectorAll('[data-bloom]')].filter(e => e.dataset.bloom !== 'done').length"
    )
    scroll_to(page, top_of(page, "#research") + 200, 1200)
    end_ink = ink_in_view(page)
    scroll_to(page, top_of(page, "#purpose") + 300, 1200)
    shoot(page, f"{look}-reduced-01-purpose")
    check(f"{tag}: the whole brush line from the first frame", whole >= 0.999 and end_ink > 40, f"progress {whole}, ink {end_ink}")
    check(f"{tag}: every painting shown (no bloom waiting)", hidden == 0, str(hidden))
    gliding = page.evaluate(
        "[...document.querySelectorAll('#top img')].filter(i => getComputedStyle(i).display !== 'none' && getComputedStyle(i).animationName !== 'none').length"
    )
    check(f"{tag}: nothing moves", gliding == 0, str(gliding))
    check(f"{tag}: no errors", not problems, "; ".join(problems[:3]))
    context.close()


with sync_playwright() as p:
    browser = p.chromium.launch(args=GPU)
    run(browser, "home", mobile=False)
    run(browser, "home", mobile=True)
    run_short(browser, "home")
    run_reduced(browser, "home")
    run_korean(browser, mobile=False)
    run_korean(browser, mobile=True)
    browser.close()

passed = sum(1 for r in results if r[1])
print(f"\n{passed}/{len(results)} checks passed. Pictures: {OUT}")
sys.exit(0 if passed == len(results) else 1)
