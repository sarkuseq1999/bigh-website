"""QA for the homepage, "Ink & Gold" with the crane (Mo's pick, October 2, 2026).

The homepage at / (and /kr). On the real GPU (ANGLE/D3D11):
  - desktop 1440x900 (full run) and phone 390x844 (full run):
    the page answers 200; no page errors, console errors or failed requests; the blocks in order
    (top, cellular, scientists, products, stories, science, research, purpose, then the footer);
    one h1; the header's links; the opening's paintings loaded and its words clear of each other;
    the brush line draws itself (ink on the canvas, its progress grows with the scroll, it is past
    the purpose's painting there, and it ends at the very bottom as the stroke under the footer's
    promise, beside the crane at rest, after one short rule over each of the three standards);
    the opening crane beats its wings (the animated painting takes the still's place); Dr. Liu and Ask BiGH Science dialogs open and close; Dr. Liu's photo never shown
    past its own pixels; the products: five real bottles, choosing a name shows its words, NuriCell
    is chosen first and stands large on the stage, choosing each picker bottle puts its bottle,
    words and both links (the big bottle and Discover) on the stage, NuriCell's big bottle and
    Discover link to its page; the stories say
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
  - other window sizes (October 4): a wide desktop (2560x1440: the opening's words start at the
    page column's left edge, under the logo, clear of the crane); a tablet held upright
    (820x1180: the blocks are one column, so no page line runs through them; the opening's words
    fit, clear of the crane); a small phone (320x568: no words past the window's edge, no
    headline word alone on a line; the footer's links at least 44 px tall).
  - everything that opens, and the keyboard path (October 4): "Skip to content" is the first Tab
    stop and puts focus at the page's words; every header control shows the ink focus ring and is
    48 px tall; each of the seven sheets (Support from the header and the footer, Dr. Liu, Ask
    BiGH Science, the three explainers) opens from the keyboard with focus inside, keeps focus,
    closes on Escape and hands focus back to its button; the sheet is the page's paper on an ink
    wash and settles in; no button opens the product preview any more (all five products link to
    their pages); the wheel scrolls a long sheet, not the page under it; on a phone each sheet
    sits inside the window with no sideways scrolling, text at least 15 px, targets at least
    48 px and the close button in view when it scrolls; the menu (phone and a tablet held
    upright) is a full sheet with the page locked under it, links at least 48 px tall inside the
    window, Tab goes from its button into it, Escape closes it, and Support opened from it hands
    focus back to the menu button; with reduced motion a sheet and the menu are whole at once;
    in Korean the Support sheet and the menu open inside the window.
  - the research index (October 4): on two columns every note is pinned to the spine (year,
    toggle and leader on one line, no rules between notes; the year beside the title on a wide
    window, heading the note on a narrow one), its leader answers in ink when the note is
    pointed at or open, what a source tells us settles in above the page's text link, rows that
    arrive settle in (the first six stay put on "show all"), "show fewer" keeps its button under
    the pointer, a guide's label is sentence case and clear of the title (English, Vietnamese),
    no straight apostrophes; on a phone the notes are on hairlines with the title at the whole
    width, a note eases open and the toggle is not left filled after a tap; with reduced motion
    rows and an opened note are there at once.
  - fine typography (October 4, desktop and phone): no paragraph ends on a single word, none of
    two or more lines runs past 76 characters, and the sample story's opening quotation mark
    hangs in the margin.
  - Dr. Liu (round 1, October 4): his photograph large (at least 340 px wide on desktop, 240 on
    a phone; still never past its own pixels), his name at headline size (30 px or more), the
    print laid down with its one shadow (there and still with reduced motion), and the brush line
    running down beside the print, never under it.
  - the products showroom (round 2, October 4): on two columns the headline stands at the left
    with its station beside it on the brush line; pointing at a picker bottle previews it on the
    stage and moving away brings the chosen one back; the stage bottle cross-fades (not at once);
    the brush line runs down the gap between the big bottle and its words and lays a stroke under
    the bottle (its ground), never over the words and never around them; on a phone the chosen
    bottle is large (about 70vw), the picker (a swipeable snap row) comes straight under it and
    the words after; with reduced motion a choice is on the stage at once.
  - the finale (round 3, October 4): a painting with its own soft edge (the opening's landscape,
    the closing painting) keeps it while it blooms (the ink blot is laid over it, not in its
    place); the promise stands large in its own band at the top of the footer (56 px or more on
    desktop, 44 to 52 on a phone), one sentence to a line, over a hairline and before the links,
    with the crane at rest beside it (260 to 340 px tall on desktop, 120 to 150 on a phone),
    which blooms only once all of it is in the window.

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


def ink_by_print(page, x0, x1, side):
    """Dark brush pixels in a band of the page level with Dr. Liu's print (the mat): from x0 to x1
    px off the mat's left edge (side "left") or right edge (side "right"); side "mat" is the mat
    itself."""
    return page.evaluate(
        """([x0o, x1o, side]) => {
          const e = document.querySelector('#scientists [data-brush=liu] > span');
          if (!e) return -1;
          const box = e.getBoundingClientRect();
          const edge = side === 'right' ? box.right : box.left;
          const x0 = edge + x0o, x1 = side === 'mat' ? box.right : edge + x1o;
          let ink = 0;
          for (const c of document.querySelectorAll('[data-brush-layer] canvas')) {
            if (!c.width) continue;
            const b = c.getBoundingClientRect();
            const l = Math.max(x0, b.left), r = Math.min(x1, b.right);
            const t = Math.max(box.top, b.top), bo = Math.min(box.bottom, b.bottom);
            if (r - l < 1 || bo - t < 1) continue;
            const k = c.width / b.width;
            const d = c.getContext('2d').getImageData(Math.floor((l - b.left) * k), Math.floor((t - b.top) * k),
              Math.max(1, Math.floor((r - l) * k)), Math.max(1, Math.floor((bo - t) * k))).data;
            for (let i = 3; i < d.length; i += 4) if (d[i] > 40) ink++;
          }
          return ink;
        }""",
        [x0, x1, side],
    )


def ink_in_box(page, x0, y0, x1, y1):
    """Dark brush pixels inside a rectangle of the window (viewport coordinates)."""
    return page.evaluate(
        """([x0, y0, x1, y1]) => {
          let ink = 0;
          for (const c of document.querySelectorAll('[data-brush-layer] canvas')) {
            if (!c.width) continue;
            const b = c.getBoundingClientRect();
            const l = Math.max(x0, b.left), r = Math.min(x1, b.right);
            const t = Math.max(y0, b.top), bo = Math.min(y1, b.bottom);
            if (r - l < 1 || bo - t < 1) continue;
            const k = c.width / b.width;
            const d = c.getContext('2d').getImageData(Math.floor((l - b.left) * k), Math.floor((t - b.top) * k),
              Math.max(1, Math.floor((r - l) * k)), Math.max(1, Math.floor((bo - t) * k))).data;
            for (let i = 3; i < d.length; i += 4) if (d[i] > 40) ink++;
          }
          return ink;
        }""",
        [x0, y0, x1, y1],
    )


# The products stage: the shown bottle's picture, the stage link, the words, the picker, the head.
STAGE = """(() => {
  const shown = document.querySelector('#products [data-brush=stage] img[data-shown=true]');
  const r = (e) => { const b = e.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; };
  return {
    src: shown ? shown.getAttribute('src') : '', opacity: shown ? +getComputedStyle(shown).opacity : 0,
    shownCount: document.querySelectorAll('#products [data-brush=stage] img[data-shown=true]').length,
    stand: shown ? r(shown) : null,
    link: document.querySelector('#products [data-brush=stage] a')?.getAttribute('href') || '',
    discover: document.querySelector('#ink-product-panel a')?.getAttribute('href') || '',
    headline: document.querySelector('#ink-product-panel h3')?.textContent || '',
    words: r(document.querySelector('#ink-product-panel')),
    picker: r(document.querySelector('#products [data-brush=bottles]')),
    title: r(document.querySelector('#products-title')),
    titleAlign: getComputedStyle(document.querySelector('#products-title')).textAlign,
    station: r(document.querySelector('#products [data-station]')),
    column: r(document.querySelector('#products > div')),
    gutter: parseFloat(getComputedStyle(document.querySelector('#products > div')).paddingLeft),
  };
})()"""
SLUGS = [
    ("NuriCell", "nuricell", "nuricell.png"),
    ("Green Bee Propolis", "green-bee-propolis", "green-bee-propolis.png"),
    ("Advanced OPC Formula", "advanced-opc", "advanced-opc.png"),
    ("Turmerific", "turmerific", "turmerific.png"),
    ("Nature Calm", "nature-calm", "nature-calm.png"),
]


def print_at_rest(page):
    """Dr. Liu's print laid down: no lift left, and the mount's one shadow at full strength."""
    return page.evaluate(
        """(() => { const m = getComputedStyle(document.querySelector('#scientists [data-brush=liu] > span'));
          return [m.translate, m.boxShadow.includes('0.42')]; })()"""
    )


# Every blooming painting with its own edge mask (--edge): its computed mask in each bloom state,
# read on a hidden copy. [has a gradient, has the ink blot, mask-composite].
EDGES = """(() => {
  const out = [];
  for (const e of document.querySelectorAll('[data-look=ink] [data-bloom]')) {
    if (!getComputedStyle(e).getPropertyValue('--edge').trim()) continue;
    const copy = e.cloneNode(false);
    copy.removeAttribute('src'); copy.removeAttribute('srcset');
    copy.style.visibility = 'hidden';
    e.after(copy);
    const seen = {};
    for (const s of ['waiting', 'in', 'done']) {
      copy.dataset.bloom = s;
      const c = getComputedStyle(copy);
      seen[s] = [c.maskImage.includes('gradient'), c.maskImage.includes('bloom-mask'), c.maskComposite];
    }
    copy.remove();
    out.push([e.getAttribute('data-brush') || e.closest('section')?.id, seen]);
  }
  return out;
})()"""

# The finale (round 3): the promise in its own band at the top of the footer, before the link
# columns and over a hairline; its size, its lines (one sentence to each), the crane's height.
FINALE = """(() => {
  const f = document.querySelector('footer');
  const band = f.querySelector('[data-brush="footer-promise"]');
  const t = band.querySelector('[data-brush="footer-tagline"]');
  const i = band.querySelector('img');
  const tier = f.querySelector('h2').closest('div').parentElement.parentElement;
  const b = band.getBoundingClientRect(), c = tier.getBoundingClientRect();
  const parts = [...t.querySelectorAll(':scope > span')];
  return {
    first: f.firstElementChild.contains(band), above: Math.round(c.top - b.bottom),
    hairline: getComputedStyle(tier).borderTopWidth,
    font: parseFloat(getComputedStyle(t.closest('p')).fontSize),
    crane: Math.round(i.getBoundingClientRect().height),
    lines: parts.map(s => new Set([...s.getClientRects()].map(r => Math.round(r.top))).size),
    rows: new Set(parts.map(s => Math.round(s.getBoundingClientRect().top))).size,
  };
})()"""


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
        "[...document.querySelectorAll('#top img:not([src*=crane-flight])')].map(i => i.complete && i.naturalWidth > 0)"
    )
    check(f"{tag}: the opening's paintings have loaded", art and all(art), str(art))
    # The wingbeat: the animated painting is fetched once the still has bloomed, and takes its place.
    try:
        page.wait_for_selector("#top [data-brush=crane][data-flying=true]", timeout=15000)
        flying = True
    except Exception:  # noqa: BLE001
        flying = False
    wing = page.evaluate(
        "(() => { const i = document.querySelector('#top img[src*=crane-flight]'); return i ? [i.complete, i.naturalWidth, getComputedStyle(i).opacity] : null })()"
    )
    check(f"{tag}: the crane beats its wings", flying and wing and wing[0] and wing[1] > 0 and wing[2] == "1", str(wing))
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
    # Round 3: a painting whose edges dissolve through its own mask (the opening's landscape, the
    # closing painting) keeps that edge before, during and after its bloom: the ink blot is laid
    # over it (intersect), never in its place. Read on a hidden copy of each, so the page's own
    # paintings (and the mist waiting on the landscape's bloom) are left alone.
    edges = page.evaluate(EDGES)
    held = all(
        all(s[0] and s[1] and "intersect" in s[2] for s in (e[1]["waiting"], e[1]["in"]))
        and e[1]["done"][0]
        and not e[1]["done"][1]
        for e in edges
    )
    check(
        f"{tag}: paintings with their own soft edge keep it while they bloom",
        len(edges) >= 2 and held,
        str(edges),
    )
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
    # Round 1 (October 4): the photograph is the block's centre of gravity, his name set as a name.
    name_px = page.evaluate("parseFloat(getComputedStyle(document.querySelector('#scientists figcaption span')).fontSize)")
    big = 240 if mobile else 340
    check(
        f"{tag}: Dr. Liu's photograph large, his name at headline size",
        liu[1] >= big and name_px >= 30,
        f"photo {liu[1]} css px (>= {big}), name {name_px:.1f} px",
    )
    rest = print_at_rest(page)
    check(f"{tag}: Dr. Liu's print laid down, with its one shadow", rest[0] == "none" and rest[1], str(rest))
    page.evaluate("document.querySelector('#scientists img[src*=inkstone]')?.scrollIntoView({block: 'center'})")
    page.wait_for_timeout(900)
    still_life = page.evaluate(
        "(() => { const i = document.querySelector('#scientists img[src*=inkstone]'); return i ? [i.complete && i.naturalWidth > 0, i.closest('figure')?.textContent.trim()] : null })()"
    )
    check(
        f"{tag}: Ask BiGH Science's painting shows, labelled Illustration",
        bool(still_life) and still_life[0] and "Illustration" in (still_life[1] or ""),
        str(still_life),
    )
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
    stage = page.evaluate(STAGE)
    stand_w = stage["stand"][2] - stage["stand"][0] if stage["stand"] else 0
    stand_h = stage["stand"][3] - stage["stand"][1] if stage["stand"] else 0
    big = stand_w >= 0.66 * width if mobile else stand_h >= 440
    check(
        f"{tag}: NuriCell is chosen first, large on the stage",
        "nuricell" in stage["src"] and stage["shownCount"] == 1 and big,
        f"{stage['src'][-40:]}, stage picture {stand_w:.0f} x {stand_h:.0f}",
    )
    if mobile:
        snap = page.evaluate(
            "(() => { const p = document.querySelector('#products [data-brush=bottles]'); return [getComputedStyle(p).scrollSnapType, p.scrollWidth > p.clientWidth]; })()"
        )
        check(
            f"{tag}: the chosen bottle, the picker straight under it (a swipeable row), then its words",
            stage["picker"][1] >= stage["stand"][3] - 4
            and stage["picker"][1] - stage["stand"][3] <= 90
            and stage["words"][1] >= stage["picker"][3]
            and "mandatory" in snap[0]
            and snap[1],
            f"stand bottom {stage['stand'][3]:.0f}, picker {stage['picker'][1]:.0f}-{stage['picker'][3]:.0f}, words {stage['words'][1]:.0f}, snap {snap}",
        )
    else:
        left = stage["column"][0] + stage["gutter"]
        check(
            f"{tag}: the headline stands at the left, its station beside it on the brush line",
            abs(stage["title"][0] - left) <= 2
            and stage["titleAlign"] in ("start", "left")
            and stage["station"][0] > stage["title"][2]
            and stage["station"][1] < stage["title"][3],
            f"title {stage['title'][0]:.0f} (column {left:.0f}), {stage['titleAlign']}, station at {stage['station'][0]:.0f}",
        )
    page.locator("#products button[aria-pressed]", has_text="Turmerific").click()
    page.wait_for_timeout(900)
    headline = page.locator("#ink-product-panel h3").text_content()
    credit = page.locator("#ink-product-panel").text_content()
    check(
        f"{tag}: choosing a name shows its words and credit",
        "turmeric" in headline.lower() and "Longvida" in credit,
        headline,
    )
    # Round 2 (October 4) changed this ON PURPOSE: the picker bottles choose, and the big stage
    # bottle and Discover link to the shown product's page (before, every small bottle picture was
    # itself a link). So every product page is reached through the stage: choosing each picker
    # bottle puts its bottle, its words and both links on the stage.
    seen = []
    for label, slug, image in SLUGS:
        page.locator("#products button[aria-pressed]", has_text=label).click()
        page.wait_for_timeout(700)
        now = page.evaluate(STAGE)
        pressed = page.evaluate(
            "[...document.querySelectorAll('#products [data-brush=bottles] button')].map(b => b.getAttribute('aria-pressed'))"
        )
        seen.append(
            (
                image in now["src"]
                and now["link"].endswith(f"/products/{slug}")
                and now["discover"].endswith(f"/products/{slug}")
                and pressed.count("true") == 1,
                now["headline"],
            )
        )
    check(
        f"{tag}: choosing each picker bottle puts its bottle, words and both links on the stage (all five pages reachable)",
        all(ok for ok, _ in seen) and len({h for _, h in seen}) == 5,
        " | ".join(f"{'ok' if ok else 'NO'} {h[:18]}" for ok, h in seen),
    )
    page.locator("#products button[aria-pressed]", has_text="NuriCell").click()
    page.wait_for_timeout(600)
    discover = page.locator("#ink-product-panel a", has_text="Discover NuriCell").get_attribute("href")
    picture = page.locator("#products [data-brush=stage] a").first.get_attribute("href")
    check(
        f"{tag}: NuriCell's big bottle and Discover link to its page",
        (discover or "").endswith("/products/nuricell") and (picture or "").endswith("/products/nuricell"),
        f"{discover} | {picture}",
    )
    if not mobile:
        # Pointing previews; moving away brings the chosen one back; the change cross-fades.
        page.hover("#products [data-brush=bottles] button:nth-child(3)")
        page.wait_for_timeout(120)
        mid = page.evaluate(STAGE)
        page.wait_for_timeout(900)
        hovered = page.evaluate(STAGE)
        page.mouse.move(4, 4)
        page.wait_for_timeout(900)
        back = page.evaluate(STAGE)
        check(
            f"{tag}: pointing at a picker bottle previews it; moving away brings the chosen one back",
            "advanced-opc" in hovered["src"]
            and "antioxidant" in hovered["headline"]
            and hovered["link"].endswith("/products/advanced-opc")
            and "nuricell" in back["src"]
            and back["link"].endswith("/products/nuricell"),
            f"{hovered['src'][-22:]} {hovered['headline'][:20]} -> {back['src'][-18:]}",
        )
        check(
            f"{tag}: the stage bottle cross-fades (not at once)",
            0 < mid["opacity"] < 1 and hovered["opacity"] == 1,
            f"opacity at 120 ms {mid['opacity']:.2f}, at rest {hovered['opacity']}",
        )
        # The brush line: down the gap between the big bottle and its words, and one stroke under
        # the bottle as its ground; never over the words, never round them.
        page.evaluate("document.querySelector('#products [data-brush=stage]').scrollIntoView({block: 'center'})")
        page.wait_for_timeout(2600)
        now = page.evaluate(STAGE)
        l, t, r, b = now["stand"]
        base = t + 0.968 * (b - t)
        ground = ink_in_box(page, l + 0.2 * (r - l), base - 6, l + 0.8 * (r - l), base + 16)
        gap = ink_in_box(page, r, t + 0.2 * (b - t), now["words"][0] - 8, t + 0.6 * (b - t))
        wl, wt, wr, wb = now["words"]
        over = ink_in_box(page, wl - 6, wt, wr + 6, wb)
        beyond = ink_in_box(page, wr + 6, wt, wr + 400, wb)
        check(
            f"{tag}: the brush line runs between the big bottle and its words and lays its ground under the bottle",
            ground > 200 and gap > 100 and over == 0 and beyond == 0,
            f"ground {ground}, gap {gap}, over the words {over}, beyond them {beyond}",
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
    # Phones have no page line: there the route is the opening's stroke, then the lifted travel to
    # the standards' rules and the closing stroke, so less of it lies above this point.
    check(
        f"{tag}: the brush line reaches the purpose",
        end_progress > (0.6 if mobile else 0.85),
        f"progress {end_progress:.3f}",
    )
    # Round 3: the crane at rest blooms only once all of it is in the window (its bloom is the
    # page's arrival): half in view it still waits; at the page's end it has bloomed.
    crane_rest = "document.querySelector('footer img[src*=\"crane-rest\"]')"
    scroll_to(
        page,
        page.evaluate(
            f"(() => {{ const b = {crane_rest}.getBoundingClientRect(); return b.top + scrollY - innerHeight + b.height * 0.5; }})()"
        ),
        900,
    )
    half_bloom = page.evaluate(f"{crane_rest}.dataset.bloom")
    # The footer: the line comes to rest as one stroke under the promise.
    scroll_to(page, page.evaluate("document.documentElement.scrollHeight"), 2600)
    end_bloom = page.evaluate(f"{crane_rest}.dataset.bloom")
    check(
        f"{tag}: the crane at rest blooms once it is whole in the window",
        half_bloom == "waiting" and end_bloom in ("in", "done"),
        f"half in view {half_bloom}, at the end {end_bloom}",
    )
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
    rest = page.evaluate(
        """(() => {
          const i = document.querySelector('footer img[src*="crane-rest"]');
          const t = document.querySelector('[data-brush="footer-tagline"]');
          if (!i || !t) return null;
          const a = i.getBoundingClientRect(), b = t.getBoundingClientRect();
          return [i.complete && i.naturalWidth > 0, Math.round(a.left - b.right), Math.round(a.bottom - b.bottom)];
        })()"""
    )
    check(
        f"{tag}: the crane at rest stands beside the promise",
        bool(rest) and rest[0] and 0 < rest[1] < 80 and 0 < rest[2] < 60,
        str(rest),
    )
    finale = page.evaluate(FINALE)
    font_ok = 44 <= finale["font"] <= 52 if mobile else finale["font"] >= 56
    crane_ok = 120 <= finale["crane"] <= 150 if mobile else 260 <= finale["crane"] <= 340
    check(
        f"{tag}: the finale: the promise large in its own band, over a hairline, before the links",
        finale["first"]
        and finale["above"] >= 40
        and finale["hairline"] == "1px"
        and font_ok
        and crane_ok
        and finale["lines"] == [1, 1]
        and finale["rows"] == 2,
        str(finale),
    )
    # The three standards: each rule is a stroke of the brush.
    scroll_to(page, top_of(page, "#ink-standards") - 300, 2200)
    rules = page.evaluate(
        """(() => [...document.querySelectorAll('#ink-standards > li')].map(li => {
          const b = li.getBoundingClientRect();
          let ink = 0;
          for (const c of document.querySelectorAll('[data-brush-layer] canvas')) {
            if (!c.width) continue;
            const r = c.getBoundingClientRect();
            const k = c.width / r.width;
            const y0 = Math.max(0, b.top - 8 - r.top), y1 = Math.min(r.height, b.top + 10 - r.top);
            if (y1 <= y0) continue;
            const x0 = Math.max(0, b.left - r.left), x1 = Math.min(r.width, b.right - r.left);
            const data = c.getContext('2d').getImageData(Math.floor(x0 * k), Math.floor(y0 * k), Math.max(1, Math.floor((x1 - x0) * k)), Math.max(1, Math.floor((y1 - y0) * k))).data;
            for (let i = 3; i < data.length; i += 16) if (data[i] > 90) ink++;
          }
          return ink;
        }))()"""
    )
    check(f"{tag}: a brush rule over each of the three standards", len(rules) == 3 and all(r > 12 for r in rules), str(rules))
    scroll_to(page, page.evaluate("document.documentElement.scrollHeight"), 900)
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


def opening_boxes(page):
    """The opening's headline, crane, first block headline and logo, as [left, top, right, bottom]."""
    return page.evaluate(
        """(() => { const box = (s) => { const b = document.querySelector(s).getBoundingClientRect();
              return [b.left, b.top, b.right, b.bottom]; };
            return { title: box('#opening-title'), crane: box('#top [data-brush=crane]'),
              column: box('#cellular-title'), logo: box('header a[href] img'),
              opening: box('#top'),
              words: [...document.querySelectorAll('#top h1, #top p, #top a, #top button')].map(e => {
                const b = e.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; }) }; })()"""
    )


def run_sizes(browser, look):
    """Window sizes the comp was not drawn for: a wide desktop, a tablet held upright, a small phone."""
    # Wide desktop: the page's column is centred; the opening's words stand on its left edge.
    tag = f"{look} 2560x1440"
    context, page, response, problems = open_page(browser, f"{BASE}/", (2560, 1440), False)
    b = opening_boxes(page)
    check(
        f"{tag}: the opening's words start at the page column's left edge, under the logo",
        abs(b["title"][0] - b["column"][0]) <= 2 and abs(b["title"][0] - b["logo"][0]) <= 12,
        f"title {b['title'][0]:.0f}, column {b['column'][0]:.0f}, logo {b['logo'][0]:.0f}",
    )
    height = b["opening"][3] - b["opening"][1]
    check(
        f"{tag}: the crane flies clear of the headline",
        b["crane"][3] - b["title"][1] <= 0.03 * height and all(w[3] <= b["opening"][3] for w in b["words"]),
        f"crane bottom {b['crane'][3]:.0f}, headline top {b['title'][1]:.0f}",
    )
    shoot(page, f"{look}-2560-00-top")
    check(f"{tag}: no errors", not problems, "; ".join(problems[:3]))
    context.close()

    # Tablet held upright: one-column blocks, so no page line; the opening is the comp, compact.
    tag = f"{look} 820x1180"
    context, page, response, problems = open_page(browser, f"{BASE}/", (820, 1180), False)
    b = opening_boxes(page)
    height = b["opening"][3] - b["opening"][1]
    check(
        f"{tag}: the opening's words fit, clear of the crane",
        b["crane"][3] - b["title"][1] <= 0.03 * height
        and all(w[0] >= 0 and w[2] <= 820 and w[3] <= b["opening"][3] for w in b["words"]),
        f"crane bottom {b['crane'][3]:.0f}, headline top {b['title'][1]:.0f}, opening {height:.0f}",
    )
    shoot(page, f"{look}-820-00-top")
    stray = []
    for block in ("#cellular", "#scientists", "#products", "#science"):
        scroll_to(page, top_of(page, block), 1600)
        stray.append(ink_in_view(page))
    shoot(page, f"{look}-820-01-science")
    check(f"{tag}: no page line through the one-column blocks", sum(stray) == 0, f"ink {stray}")
    wide = page.evaluate("document.documentElement.scrollWidth")
    check(f"{tag}: no sideways scrolling", wide <= 820, f"scrollWidth {wide}")
    check(f"{tag}: no errors", not problems, "; ".join(problems[:3]))
    context.close()

    # Small phone: nothing past the window's edge, no headline word alone on a line.
    tag = f"{look} 320x568"
    context, page, response, problems = open_page(browser, f"{BASE}/", (320, 568), True)
    total = page.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < total:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(60)
        y += 284
    past = page.evaluate(
        """(() => { const out = []; const root = document.querySelector('[data-look=ink]');
          const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
          for (let n = walker.nextNode(); n; n = walker.nextNode()) {
            const e = n.parentElement;
            if (!n.nodeValue.trim() || !e.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true })) continue;
            if (e.closest('[data-brush=bottles], dialog, [inert]') || e.getBoundingClientRect().width <= 2) continue;
            const r = document.createRange(); r.selectNodeContents(n);
            for (const b of r.getClientRects()) if (b.width > 1 && (b.right > innerWidth + 0.5 || b.left < -0.5)) {
              out.push(n.nodeValue.trim().slice(0, 30)); break; }
          }
          return out; })()"""
    )
    check(f"{tag}: no words past the window's edge", not past, "; ".join(past[:4]))
    alone = page.evaluate(
        """(() => { const out = [];
          for (const h of document.querySelectorAll('[data-look=ink] h1, [data-look=ink] h2')) {
            const blocks = [...h.children].filter(c => getComputedStyle(c).display === 'block');
            for (const block of blocks.length ? blocks : [h]) {
              const rows = new Map(); const walker = document.createTreeWalker(block, NodeFilter.SHOW_TEXT);
              for (let n = walker.nextNode(); n; n = walker.nextNode()) { const re = /\\S+/g; let m;
                while ((m = re.exec(n.nodeValue))) { const r = document.createRange();
                  r.setStart(n, m.index); r.setEnd(n, m.index + m[0].length);
                  const k = Math.round(r.getBoundingClientRect().top / 6); rows.set(k, (rows.get(k) || 0) + 1); } }
              const counts = [...rows.entries()].sort((a, b) => a[0] - b[0]).map(x => x[1]);
              if (counts.length >= 2 && counts.reduce((s, c) => s + c, 0) >= 3 && counts.some(c => c === 1))
                out.push(block.textContent.trim().slice(0, 30)); } }
          return out; })()"""
    )
    check(f"{tag}: no headline word alone on a line", not alone, "; ".join(alone[:4]))
    low = page.evaluate(
        """[...document.querySelectorAll('footer a, footer button')]
          .filter(e => e.getBoundingClientRect().width && e.getBoundingClientRect().height < 44)
          .map(e => `${Math.round(e.getBoundingClientRect().height)}px ${(e.textContent || '').trim().slice(0, 24)}`)"""
    )
    check(f"{tag}: the footer's links at least 44 px tall", not low, "; ".join(low[:4]))
    wide = page.evaluate("document.documentElement.scrollWidth")
    check(f"{tag}: no sideways scrolling", wide <= 320, f"scrollWidth {wide}")
    shoot(page, f"{look}-320-00-footer")
    check(f"{tag}: no errors", not problems, "; ".join(problems[:3]))
    context.close()


INK = "rgb(12, 11, 10)"
SUPPORT = "document.querySelector('#home-navigation > button')"
SHEETS = [
    ("Support (header)", SUPPORT, None),
    ("Dr. Liu", "document.querySelectorAll('#scientists button')[0]", None),
    ("Ask BiGH Science", "document.querySelectorAll('#scientists button')[1]", None),
    ("explainer 1", "[...document.querySelectorAll('#science [role=tabpanel] button')].pop()", 0),
    ("explainer 2", "[...document.querySelectorAll('#science [role=tabpanel] button')].pop()", 1),
    ("explainer 3", "[...document.querySelectorAll('#science [role=tabpanel] button')].pop()", 2),
    ("Support (footer)", "document.querySelector('footer button')", None),
]
MENU_BUTTON = "button[aria-controls='home-navigation']"
ACTIVE = "(document.activeElement.getAttribute('aria-label') || document.activeElement.textContent || '').trim().slice(0, 28)"


def ring(page):
    """Is the focused control's ring the page's ink ring (2 px, solid, sumi ink)?"""
    return page.evaluate(
        f"(() => {{ const s = getComputedStyle(document.activeElement); return s.outlineStyle === 'solid' && parseFloat(s.outlineWidth) >= 2 && s.outlineColor === '{INK}'; }})()"
    )


def open_sheet(page, opener, topic=None, wait=1200):
    """Open a sheet the way a keyboard does: focus its button, press Enter."""
    if topic is not None:
        page.evaluate(
            f"document.querySelectorAll('#science [role=tab]')[{topic}].scrollIntoView({{ block: 'center', behavior: 'instant' }})"
        )
        page.wait_for_timeout(500)
        page.locator("#science [role=tab]").nth(topic).click()
        page.wait_for_timeout(900)
    page.evaluate(
        f"(() => {{ const e = {opener}; e.scrollIntoView({{ block: 'center', behavior: 'instant' }}); e.focus(); window.__opener = e; }})()"
    )
    page.wait_for_timeout(400)
    page.keyboard.press("Enter")
    page.wait_for_timeout(wait)


def run_opens(browser):
    """Everything the page opens, and the keyboard path through it."""
    # Desktop: the keyboard path, and each sheet from the keyboard.
    tag = "opens desk"
    context, page, response, problems = open_page(browser, f"{BASE}/", (1440, 900), False)
    page.keyboard.press("Tab")
    page.wait_for_timeout(300)
    first = page.evaluate(f"[{ACTIVE}, getComputedStyle(document.activeElement).opacity]")
    shoot(page, "opens-desk-00-skip")
    # Tab on: the logo, the five links, Log in and the language (Sign up is a placeholder, off).
    stops, pale = [], []
    for _ in range(9):
        page.keyboard.press("Tab")
        page.wait_for_timeout(200)
        if not page.evaluate("!!document.activeElement.closest('header')"):
            break
        name = page.evaluate(ACTIVE)
        stops.append(name)
        if not ring(page):
            pale.append(name)
    check(
        f"{tag}: the header's eight controls each show the ink focus ring",
        len(stops) == 8 and not pale,
        f"{len(stops)} stops {stops}, without the ring: {pale}",
    )
    page.evaluate("document.querySelector('[data-look=ink] > a').focus()")
    page.keyboard.press("Enter")
    page.wait_for_timeout(400)
    landed = page.evaluate("document.activeElement.tagName")
    page.keyboard.press("Tab")
    page.wait_for_timeout(300)
    after = page.evaluate("!!document.activeElement.closest('#top')")
    check(
        f"{tag}: Skip to content is the first Tab stop and puts focus at the page's words",
        first == ["Skip to content", "1"] and landed == "MAIN" and after,
        f"{first}, landed on {landed}, next stop in the opening {after}",
    )
    low = page.evaluate(
        """[...document.querySelectorAll('#home-navigation a, #home-navigation button, #home-navigation select')]
          .filter(e => e.getBoundingClientRect().height < 48)
          .map(e => `${Math.round(e.getBoundingClientRect().height)}px ${e.textContent.trim().slice(0, 14)}`)"""
    )
    check(f"{tag}: the header's controls at least 48 px tall", not low, "; ".join(low))
    page.evaluate("window.scrollTo(0, 0)")

    unopened, loose, unreturned, pale = [], [], [], []
    surface = None
    settle = None
    for name, opener, topic in SHEETS:
        open_sheet(page, opener, topic, wait=0)
        try:
            page.wait_for_function("document.querySelector('dialog').open", timeout=3000)
        except Exception:  # noqa: BLE001
            unopened.append(name)
            continue
        early = float(page.evaluate("getComputedStyle(document.querySelector('dialog')).opacity"))
        page.wait_for_timeout(1300)
        state = page.evaluate(
            """(() => { const d = document.querySelector('dialog'); const s = getComputedStyle(d); const b = getComputedStyle(d, '::backdrop');
              return { inside: d.contains(document.activeElement), title: d.querySelector('h2').textContent.trim(), opacity: s.opacity,
                paper: s.backgroundImage.includes('paper'), shadow: s.boxShadow, radius: parseFloat(s.borderRadius),
                wash: b.backgroundColor, blur: b.backdropFilter }; })()"""
        )
        if not state["inside"] or not state["title"]:
            unopened.append(name)
        if not ring(page):
            pale.append(name)
        if surface is None:
            surface = state
            settle = (early, float(state["opacity"]))
            shoot(page, "opens-desk-01-sheet")
        for _ in range(6):
            page.keyboard.press("Tab")
            page.wait_for_timeout(90)
            where = page.evaluate(
                "(() => { const a = document.activeElement; return document.querySelector('dialog').contains(a) ? 'in' : a === document.body ? 'body' : 'out'; })()"
            )
            if where == "out":
                loose.append(name)
                break
            if where == "in" and not ring(page):
                pale.append(f"{name}: {page.evaluate(ACTIVE)}")
        page.keyboard.press("Escape")
        page.wait_for_timeout(600)
        back = page.evaluate("[document.querySelector('dialog').open, document.activeElement === window.__opener, document.body.style.overflow]")
        if back != [False, True, ""]:
            unreturned.append(f"{name} {back}")
    check(f"{tag}: seven sheets open from the keyboard with focus inside", not unopened, f"not opened: {unopened}")
    check(f"{tag}: focus stays in each sheet, with the ink focus ring", not loose and not pale, f"left the sheet: {loose}; no ring: {pale[:4]}")
    check(
        f"{tag}: Escape closes each sheet, focus returns to its button and the page scrolls again",
        not unreturned,
        "; ".join(unreturned[:3]),
    )
    warm = [int(v) for v in (surface or {}).get("wash", "").replace("rgba(", "").replace("rgb(", "").split(")")[0].split(",")[:3] if v.strip().isdigit()]
    check(
        f"{tag}: the sheet is the page's paper (its fibre, no shadow, square corners) on a warm ink wash",
        bool(surface)
        and surface["paper"]
        and surface["shadow"] == "none"
        and surface["radius"] <= 4
        and surface["blur"] == "none"
        and len(warm) == 3
        and warm[0] >= warm[2],
        str(surface),
    )
    check(
        f"{tag}: the sheet settles in (not at once) and is whole within the breath",
        bool(settle) and settle[0] < 1 and settle[1] == 1,
        f"opacity as it opens {settle and settle[0]:.2f}, at rest {settle and settle[1]}",
    )
    preview = page.evaluate(
        """[[...document.querySelectorAll('footer > div:nth-child(2) > div:nth-child(2) > div:first-child a')].length,
            [...document.querySelectorAll('#top button, #products [data-brush=bottles] button:not([aria-pressed]), #ink-product-panel button, #stories article button, #purpose button, footer > div:nth-child(2) > div:nth-child(2) > div:first-child button')].map(e => e.textContent.trim().slice(0, 24))]"""
    )
    check(
        f"{tag}: no button opens the product preview (all five products link to their pages)",
        preview[0] == 5 and not preview[1],
        str(preview),
    )
    check(f"{tag}: no errors", not problems, "; ".join(problems[:3]))
    context.close()

    # A short window: the wheel scrolls the sheet, and the page under it stays where it is.
    tag = "opens 1280x640"
    context, page, response, problems = open_page(browser, f"{BASE}/", (1280, 640), False)
    open_sheet(page, SHEETS[1][1])
    before = page.evaluate("[scrollY, document.querySelector('dialog').scrollHeight - document.querySelector('dialog').clientHeight]")
    page.mouse.move(640, 320)
    for _ in range(6):
        page.mouse.wheel(0, 120)
        page.wait_for_timeout(120)
    page.wait_for_timeout(1300)
    moved = page.evaluate("[scrollY, document.querySelector('dialog').scrollTop]")
    check(
        f"{tag}: the wheel scrolls a long sheet, not the page under it",
        before[1] > 20 and moved[0] == before[0] and moved[1] >= before[1] - 2,
        f"page {before[0]} -> {moved[0]}, sheet scrolled {moved[1]} of {before[1]}",
    )
    context.close()

    # Phone: each sheet in the window; the menu.
    tag = "opens phone"
    context, page, response, problems = open_page(browser, f"{BASE}/", (390, 844), True)
    outside, small, lost = [], [], []
    for name, opener, topic in SHEETS:
        if name == "Support (header)":
            page.click(MENU_BUTTON)
            page.wait_for_timeout(900)
        open_sheet(page, opener, topic)
        m = page.evaluate(
            """(() => { const d = document.querySelector('dialog'); if (!d.open) return null; const b = d.getBoundingClientRect();
              const sizes = []; const walker = document.createTreeWalker(d, NodeFilter.SHOW_TEXT);
              for (let n = walker.nextNode(); n; n = walker.nextNode()) if (n.nodeValue.trim()) sizes.push(parseFloat(getComputedStyle(n.parentElement).fontSize));
              const targets = [...d.querySelectorAll('a, button, summary')].map(e => Math.round(e.getBoundingClientRect().height));
              d.scrollTo(0, 99999);
              const c = d.querySelector('button[aria-label]').getBoundingClientRect();
              return { box: [b.left, b.top, b.right, b.bottom].map(Math.round), wide: [d.scrollWidth, d.clientWidth, document.documentElement.scrollWidth],
                text: Math.min(...sizes), target: Math.min(...targets), scrolls: d.scrollHeight > d.clientHeight + 4,
                close: c.top >= b.top && c.bottom <= b.bottom && c.right <= b.right && c.width >= 48 }; })()"""
        )
        if name == "Ask BiGH Science":
            page.wait_for_timeout(300)
            shoot(page, "opens-phone-01-sheet-end")
        if not m or m["box"][0] < 0 or m["box"][1] < 0 or m["box"][2] > 390 or m["box"][3] > 844 or m["wide"][0] > m["wide"][1] or m["wide"][2] > 390:
            outside.append(f"{name} {m and m['box']} {m and m['wide']}")
        if m and (m["text"] < 15 or m["target"] < 48):
            small.append(f"{name} text {m['text']} target {m['target']}")
        if m and not m["close"]:
            lost.append(name)
        if m:
            closed = close_dialog(page)
            if not closed:
                outside.append(f"{name} did not close")
    check(f"{tag}: each sheet sits inside the window, no sideways scrolling", not outside, "; ".join(outside[:3]))
    check(f"{tag}: sheet text at least 15 px, targets at least 48 px", not small, "; ".join(small[:3]))
    check(f"{tag}: the close button stays in view when a sheet scrolls", not lost, str(lost))
    check(f"{tag}: no errors", not problems, "; ".join(problems[:3]))
    context.close()

    for size, mobile in (((390, 844), True), ((820, 1180), False)):
        tag = f"opens {'phone' if mobile else '820x1180'}"
        context, page, response, problems = open_page(browser, f"{BASE}/", size, mobile)
        page.evaluate(f"document.querySelector(\"{MENU_BUTTON}\").focus()")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1500)
        menu = page.evaluate(
            """(() => { const n = document.querySelector('#home-navigation'); const b = n.getBoundingClientRect(); const s = getComputedStyle(n);
              const links = [...n.querySelectorAll(':scope > a, :scope > button')].map(e => { const r = e.getBoundingClientRect();
                return [Math.round(r.left), Math.round(r.right), Math.round(r.height), parseFloat(getComputedStyle(e).fontSize), getComputedStyle(e).opacity]; });
              const rest = [...n.querySelectorAll(':scope > div a, :scope > div button, :scope > div select')].map(e => { const r = e.getBoundingClientRect();
                return [Math.round(r.left), Math.round(r.right), Math.round(r.height), parseFloat(getComputedStyle(e).fontSize), Math.round(r.bottom)]; });
              return { shown: s.display !== 'none', box: [Math.round(b.top), Math.round(b.bottom)], paper: s.backgroundImage.includes('paper'), links, rest,
                locked: document.body.style.overflow, wide: document.documentElement.scrollWidth, win: [innerWidth, innerHeight],
                expanded: document.querySelector('header button[aria-controls]').getAttribute('aria-expanded') }; })()"""
        )
        shoot(page, f"opens-{'phone' if mobile else '820'}-00-menu")
        check(
            f"{tag}: the menu opens as a full sheet of the page's paper, the page locked under it",
            menu["shown"] and menu["expanded"] == "true" and menu["paper"] and menu["box"][1] >= size[1] - 1 and menu["locked"] == "hidden",
            f"box {menu['box']}, paper {menu['paper']}, body overflow {menu['locked']!r}",
        )
        every = menu["links"] + menu["rest"]
        check(
            f"{tag}: five menu links, each at least 48 px tall and 18 px type, every control inside the window",
            len(menu["links"]) == 5
            and all(l[2] >= 48 and l[3] >= 18 and l[4] == "1" for l in menu["links"])
            and all(r[2] >= 48 and r[3] >= 18 and r[4] <= size[1] for r in menu["rest"])
            and all(e[0] >= 0 and e[1] <= size[0] for e in every)
            and menu["wide"] <= size[0],
            f"links {menu['links']}, rest {menu['rest']}",
        )
        walk = []
        for _ in range(3):
            page.keyboard.press("Tab")
            page.wait_for_timeout(150)
            walk.append(page.evaluate(f"[!!document.activeElement.closest('#home-navigation'), {ACTIVE}]"))
        ringed = ring(page)
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
        shut = page.evaluate(f"[document.querySelector('header button[aria-controls]').getAttribute('aria-expanded'), {ACTIVE}, document.body.style.overflow]")
        check(
            f"{tag}: Tab goes from the menu's button into the menu; Escape closes it, focus back on the button",
            all(w[0] for w in walk) and ringed and shut == ["false", "Open menu", ""],
            f"{walk}, ring {ringed}, after Escape {shut}",
        )
        page.keyboard.press("Enter")
        page.wait_for_timeout(900)
        page.evaluate(f"{SUPPORT}.focus()")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1300)
        title = dialog_title(page)
        page.keyboard.press("Escape")
        page.wait_for_timeout(600)
        home = page.evaluate(f"[document.querySelector('dialog').open, {ACTIVE}]")
        check(
            f"{tag}: Support opened from the menu hands focus back to the menu's button",
            title == "BiGH support" and home == [False, "Open menu"],
            f"{title!r}, then {home}",
        )
        check(f"{tag}: no errors (menu)", not problems, "; ".join(problems[:3]))
        context.close()

    # Reduced motion: a sheet and the menu are whole at once, and a sheet is gone at once.
    tag = "opens reduced motion"
    context, page, response, problems = open_page(browser, f"{BASE}/", (1440, 900), False, reduced=True)
    open_sheet(page, SUPPORT, wait=0)
    page.wait_for_function("document.querySelector('dialog').open", timeout=3000)
    whole = page.evaluate(
        """(() => { const d = document.querySelector('dialog'); const s = getComputedStyle(d); const b = getComputedStyle(d, '::backdrop');
          return [s.opacity, s.translate, b.opacity, b.maskImage, d.getAnimations().length]; })()"""
    )
    page.keyboard.press("Escape")
    gone = page.evaluate("getComputedStyle(document.querySelector('dialog')).display")
    check(
        f"{tag}: a sheet is whole at once and gone at once",
        whole[0] == "1" and whole[1] in ("none", "0px") and whole[2] == "1" and whole[3] == "none" and whole[4] == 0 and gone == "none",
        f"{whole}, after Escape display {gone}",
    )
    context.close()
    context, page, response, problems = open_page(browser, f"{BASE}/", (390, 844), True, reduced=True)
    page.click(MENU_BUTTON)
    still = page.evaluate(
        """(() => { const n = document.querySelector('#home-navigation');
          return [getComputedStyle(n).display, ...[n, ...n.children].map(e => getComputedStyle(e).opacity + ' ' + getComputedStyle(e).animationName)]; })()"""
    )
    check(
        f"{tag}: the menu is whole at once",
        still[0] == "flex" and all(v == "1 none" for v in still[1:]),
        str(still),
    )
    check(f"{tag}: no errors (opens)", not problems, "; ".join(problems[:3]))
    context.close()

    # Korean, on a phone: the Support sheet and the menu.
    tag = "opens kr phone"
    context, page, response, problems = open_page(browser, f"{BASE}/kr", (390, 844), True)
    page.click(MENU_BUTTON)
    page.wait_for_timeout(1300)
    links = page.evaluate(
        "[...document.querySelectorAll('#home-navigation > a, #home-navigation > button')].map(e => { const r = e.getBoundingClientRect(); return [e.textContent.trim(), Math.round(r.right), Math.round(r.height)]; })"
    )
    shoot(page, "opens-kr-phone-00-menu")
    page.locator("#home-navigation > button").click()
    page.wait_for_timeout(1300)
    sheet = page.evaluate(
        """(() => { const d = document.querySelector('dialog'); const b = d.getBoundingClientRect();
          return [d.open, d.querySelector('h2').textContent.trim(), Math.round(b.left), Math.round(b.right), d.scrollWidth <= d.clientWidth, document.documentElement.scrollWidth, d.querySelectorAll('details').length]; })()"""
    )
    shoot(page, "opens-kr-phone-01-sheet")
    check(
        f"{tag}: the menu and the Support sheet open in Korean, inside the window",
        len(links) == 5
        and all(l[1] <= 390 and l[2] >= 48 for l in links)
        and "고객" in links[4][0]
        and sheet[0]
        and "BiGH" in sheet[1]
        and sheet[1] != "BiGH support"
        and sheet[2] >= 0
        and sheet[3] <= 390
        and sheet[4]
        and sheet[5] <= 390
        and sheet[6] == 4,
        f"{links} | {sheet}",
    )
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
    rest = print_at_rest(page)
    check(f"{tag}: Dr. Liu's print there and still, with its shadow", rest[0] == "none" and rest[1], str(rest))
    # The brush line frames the print: it runs down beside the mat (within 120 px of its right
    # edge, level with it) and never under it, nor within 16 px of it.
    scroll_to(page, top_of(page, "#scientists") - 40, 1200)
    under = ink_by_print(page, 0, 0, "mat")
    close = ink_by_print(page, 0, 16, "right")
    beside = ink_by_print(page, 0, 120, "right")
    check(
        f"{tag}: the brush line runs beside Dr. Liu's print, never under it",
        under == 0 and close == 0 and beside > 200,
        f"under {under}, within 16 px {close}, beside {beside}",
    )
    scroll_to(page, top_of(page, "#products [data-brush=bottles]") - 500, 900)
    page.locator("#products button[aria-pressed]", has_text="Nature Calm").click()
    page.wait_for_timeout(60)
    instant = page.evaluate(STAGE)
    check(
        f"{tag}: a choice is on the stage at once",
        "nature-calm" in instant["src"] and instant["opacity"] == 1,
        f"{instant['src'][-22:]} opacity {instant['opacity']}",
    )
    scroll_to(page, top_of(page, "#research") + 200, 1200)
    end_ink = ink_in_view(page)
    scroll_to(page, top_of(page, "#purpose") + 300, 1200)
    shoot(page, f"{look}-reduced-01-purpose")
    check(f"{tag}: the whole brush line from the first frame", whole >= 0.999 and end_ink > 40, f"progress {whole}, ink {end_ink}")
    check(f"{tag}: every painting shown (no bloom waiting)", hidden == 0, str(hidden))
    gliding = page.evaluate(
        "[...document.querySelectorAll('#top img, #top [data-brush=crane]')].filter(i => getComputedStyle(i).display !== 'none' && getComputedStyle(i).animationName !== 'none').length + document.querySelectorAll('#top img[src*=crane-flight]').length"
    )
    check(f"{tag}: nothing moves", gliding == 0, str(gliding))
    check(f"{tag}: no errors", not problems, "; ".join(problems[:3]))
    context.close()


def run_vietnamese(browser, mobile):
    """Vietnamese readers get one face: Be Vietnam Pro through the brand token, never Arial filling
    the letters Switzer lacks (Chrome's own record of the fonts it used, glyph by glyph)."""
    tag = f"vn {'phone' if mobile else 'desk'}"
    size = (390, 844) if mobile else (1536, 1000)
    context, page, response, problems = open_page(browser, f"{BASE}/vn", size, mobile)
    check(f"{tag}: answers 200", response and response.status == 200)
    cdp = context.new_cdp_session(page)
    cdp.send("DOM.enable")
    cdp.send("CSS.enable")
    root = cdp.send("DOM.getDocument")["root"]["nodeId"]
    ids = cdp.send("DOM.querySelectorAll", {"nodeId": root, "selector": "h1, h2, h3, p"})["nodeIds"]
    glyphs = {}
    for node in ids:
        for font in cdp.send("CSS.getPlatformFontsForNode", {"nodeId": node})["fonts"]:
            glyphs[font["familyName"]] = glyphs.get(font["familyName"], 0) + font["glyphCount"]
    arial = sum(n for name, n in glyphs.items() if "Arial" in name)
    brand = sum(n for name, n in glyphs.items() if "Be Vietnam Pro" in name)
    check(f"{tag}: no Arial glyphs in any h1, h2, h3 or paragraph", arial == 0 and brand > 500, str(glyphs))
    check(f"{tag}: no sideways scrolling", page.evaluate("document.documentElement.scrollWidth") <= size[0])
    context.close()


# The research index's notes (the first six): where the year, the toggle and the leader sit.
NOTES = """() => {
  const list = document.querySelector('#research ul');
  return [...list.children].slice(0, 6).map((li) => {
    const box = li.getBoundingClientRect();
    const summary = li.querySelector('summary');
    const [year, what, toggle] = summary.children;
    const title = what.children[0];
    const centre = (e) => { const r = e.getBoundingClientRect(); return r.top + r.height / 2 - box.top; };
    const lead = getComputedStyle(li, '::after');
    const y = year.getBoundingClientRect(), t = title.getBoundingClientRect(), g = toggle.getBoundingClientRect();
    return {
      year: centre(year), toggle: centre(toggle),
      leader: lead.content === 'none' ? null : parseFloat(lead.top) + 0.5,
      leaderWidth: lead.content === 'none' ? 0 : parseFloat(lead.width),
      rule: parseFloat(getComputedStyle(li).borderTopWidth),
      beside: y.right <= t.left + 0.5, above: y.bottom <= t.top + 0.5,
      titleWidth: t.width, rowWidth: box.width, toggleSize: [g.width, g.height],
      summary: summary.getBoundingClientRect().height,
      label: [getComputedStyle(year).textTransform, getComputedStyle(year, '::first-letter').textTransform],
    };
  });
}"""
LEADER = "(n) => getComputedStyle(document.querySelector(`#research ul > li:nth-child(${n})`), '::before').scale"
ROW_OPACITY = "[...document.querySelectorAll('#research ul > li')].map((e) => +(+getComputedStyle(e).opacity).toFixed(2))"
ROW_HEIGHT = "document.querySelector('#research ul > li:nth-child(2)').getBoundingClientRect().height"
MORE_OPACITY = "+getComputedStyle(document.querySelector('#research details[open] > div')).opacity"

# The page's paragraphs, line by line: one that ends on a single word, one that runs too wide;
# and the sample story's opening quotation mark.
TYPE = """() => {
  const root = document.querySelector('[data-look=ink]');
  const out = { wrap: getComputedStyle(root).textWrapStyle, widows: [], wide: [] };
  // (a station label is not a paragraph: beside the products it sits on two lines in the margin)
  for (const p of root.querySelectorAll('main p:not([data-station])')) {
    if (!p.checkVisibility()) continue;
    const walker = document.createTreeWalker(p, NodeFilter.SHOW_TEXT);
    const lines = new Map();
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      const re = /\\S+/g; let m;
      while ((m = re.exec(n.nodeValue))) {
        const range = document.createRange(); range.setStart(n, m.index); range.setEnd(n, m.index + m[0].length);
        const r = range.getClientRects()[0]; if (!r || !r.width) continue;
        const key = Math.round((r.top + r.height / 2) / 8);
        lines.set(key, (lines.get(key) || []).concat(m[0]));
      }
    }
    const rows = [...lines.entries()].sort((a, b) => a[0] - b[0]).map((x) => x[1].join(' '));
    if (rows.length < 2) continue;
    if (!rows[rows.length - 1].includes(' ')) out.widows.push(rows[rows.length - 1]);
    const longest = Math.max(...rows.map((r) => r.length));
    if (longest > 76) out.wide.push(`${longest}: ${rows[0].slice(0, 30)}`);
  }
  const quote = document.querySelector('#stories h3');
  const mark = quote.querySelector('span');
  const range = document.createRange(); range.setStart(mark.nextSibling, 0); range.setEnd(mark.nextSibling, 1);
  const left = quote.getBoundingClientRect().left;
  out.hang = [mark.textContent, +(mark.getBoundingClientRect().right - left).toFixed(1), +(range.getBoundingClientRect().left - left).toFixed(1), +(document.querySelector('#stories blockquote p').getBoundingClientRect().left - left).toFixed(1), Math.round(mark.getBoundingClientRect().left)];
  return out;
}"""


def run_research(browser):
    """The research index (October 4). Two columns: every note is pinned to the spine (its year,
    its round toggle and its leader on one line, no rules between notes), the leader answers in ink
    when the note is pointed at or open, what a source tells us settles in, rows that arrive settle
    in, "show fewer" keeps its button under the pointer, a guide's label is sentence case and clear
    of the title, and no straight apostrophes are left. One column: notes on hairlines, the year
    heading the note, the title at the whole width, the note easing open. Reduced motion: all of
    it at once."""
    tag = "research desk"
    context, page, response, problems = open_page(browser, f"{BASE}/", (1536, 1000), False)
    scroll_to(page, top_of(page, "#research ul") - 220, 1500)
    notes = page.evaluate(NOTES)
    check(
        f"{tag}: every note's year, toggle and leader share one line (year beside the title, no rules)",
        len(notes) == 6
        and all(
            n["leader"] is not None
            and abs(n["year"] - n["toggle"]) <= 2
            and abs(n["leader"] - n["toggle"]) <= 2
            and n["leaderWidth"] >= 12
            and n["rule"] == 0
            and n["beside"]
            for n in notes
        ),
        str([(round(n["year"]), round(n["toggle"]), n["leader"], n["leaderWidth"], n["rule"]) for n in notes[:2]]),
    )
    rest = page.evaluate(LEADER, 3)
    page.hover("#research ul > li:nth-child(3) summary")
    page.wait_for_timeout(900)
    pointed = page.evaluate(LEADER, 3)
    page.mouse.move(5, 5)
    page.wait_for_timeout(700)
    left = page.evaluate(LEADER, 3)
    page.locator("#research ul > li:nth-child(3) summary").click()
    page.mouse.move(5, 5)
    page.wait_for_timeout(100)
    arriving = page.evaluate(MORE_OPACITY)
    page.wait_for_timeout(1300)
    settled = page.evaluate(MORE_OPACITY)
    opened = page.evaluate(LEADER, 3)
    link = page.evaluate(
        "(() => { const a = document.querySelector('#research details[open] a'); const s = getComputedStyle(a); return [s.textUnderlineOffset, s.textDecorationThickness, a.target, Math.round(a.getBoundingClientRect().height)]; })()"
    )
    shoot(page, "research-desk-00-open")
    check(
        f"{tag}: the leader answers in ink when the note is pointed at or open",
        rest.startswith("0") and pointed in ("1", "1 1") and left.startswith("0") and opened in ("1", "1 1"),
        f"{rest} | {pointed} | {left} | {opened}",
    )
    check(
        f"{tag}: what a source tells us settles in; its link is the page's text link",
        arriving < 0.9 and settled == 1 and link == ["8px", "1px", "_blank", 48],
        f"{arriving:.2f} -> {settled} | {link}",
    )
    page.locator("#research ul > li:nth-child(3) summary").click()
    page.click("#research button[aria-pressed] >> nth=2")
    page.wait_for_timeout(60)
    arriving = page.evaluate(ROW_OPACITY)
    page.wait_for_timeout(1800)
    settled = page.evaluate(ROW_OPACITY)
    page.click("#research button[aria-expanded]")
    page.wait_for_timeout(60)
    more = page.evaluate(ROW_OPACITY)
    page.wait_for_timeout(1800)
    everything = page.evaluate(ROW_OPACITY)
    check(
        f"{tag}: rows that arrive settle in (a filter: all six; show all: the new ones only)",
        len(arriving) == 6
        and max(arriving) < 0.9
        and settled == [1] * 6
        and len(more) == 17
        and more[:6] == [1] * 6
        and max(more[6:]) < 0.9
        and everything == [1] * 17,
        f"{arriving} -> {settled} | {more[:9]}",
    )
    button = page.locator("#research button[aria-expanded]")
    button.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    before = button.bounding_box()["y"]
    button.click()
    page.wait_for_timeout(600)
    moved = button.bounding_box()["y"] - before
    fewer = page.locator("#research ul > li").count()
    check(f"{tag}: show fewer keeps its button under the pointer", abs(moved) <= 2 and fewer == 6, f"moved {moved:.1f}, rows {fewer}")
    page.click("#research button[aria-pressed] >> nth=3")
    page.wait_for_timeout(1500)
    guides = page.evaluate(NOTES)
    word = page.evaluate("document.querySelector('#research summary > span').innerText")
    shoot(page, "research-desk-01-guides")
    check(
        f"{tag}: a guide's label is sentence case and clear of the title",
        all(g["label"] == ["lowercase", "uppercase"] and (g["beside"] or g["above"]) for g in guides) and word == "Guide",
        f"{word} {guides[0]['label']}",
    )
    page.click("#research button[aria-pressed] >> nth=0")
    page.click("#research button[aria-expanded]")
    page.wait_for_timeout(400)
    words = page.evaluate("document.querySelector('#research').textContent")
    rows = page.locator("#research ul > li").count()
    check(f"{tag}: all 36 sources, no straight apostrophes", rows == 36 and "'" not in words and "Curcumin’s" in words, f"rows {rows}")
    check(f"{tag}: no errors", not problems, "; ".join(problems[:3]))
    context.close()

    # A narrow two-column window: the year heads the note, the leader still on its line.
    tag = "research 1024"
    context, page, response, problems = open_page(browser, f"{BASE}/", (1024, 768), False)
    scroll_to(page, top_of(page, "#research ul") - 220, 1500)
    notes = page.evaluate(NOTES)
    shoot(page, "research-1024-00")
    check(
        f"{tag}: the year heads each note, the leader on its line",
        all(
            n["above"] and n["leader"] is not None and abs(n["leader"] - n["toggle"]) <= 2 and abs(n["year"] - n["toggle"]) <= 2 and n["rule"] == 0
            for n in notes
        ),
        str([(round(n["year"]), round(n["toggle"]), n["leader"]) for n in notes[:2]]),
    )
    context.close()

    # A phone: one column, on hairlines.
    tag = "research phone"
    context, page, response, problems = open_page(browser, f"{BASE}/", (390, 844), True)
    scroll_to(page, top_of(page, "#research ul") - 160, 1500)
    notes = page.evaluate(NOTES)
    check(
        f"{tag}: notes on hairlines, the year heading the note, the title at the whole width, 44 px toggle",
        all(
            n["rule"] == 1
            and n["leader"] is None
            and n["above"]
            and n["titleWidth"] >= n["rowWidth"] - 1
            and n["toggleSize"] == [44, 44]
            and n["summary"] >= 44
            for n in notes
        ),
        str([(n["rule"], n["leader"], round(n["titleWidth"]), n["toggleSize"]) for n in notes[:2]]),
    )
    eases = page.evaluate("CSS.supports('selector(::details-content)') && CSS.supports('interpolate-size', 'allow-keywords')")
    closed = page.evaluate(ROW_HEIGHT)
    page.locator("#research ul > li:nth-child(2) summary").tap()
    page.wait_for_timeout(120)
    opening = page.evaluate(ROW_HEIGHT)
    page.wait_for_timeout(1200)
    opened = page.evaluate(ROW_HEIGHT)
    filled = page.evaluate("getComputedStyle(document.querySelector('#research ul > li:nth-child(2) summary > span:last-child')).backgroundColor")
    shoot(page, "research-phone-00-open")
    check(
        f"{tag}: a note eases open; the toggle is not left filled after a tap",
        opened > closed + 80 and (closed < opening < opened if eases else opening == opened) and filled == "rgba(0, 0, 0, 0)",
        f"{closed:.0f} -> {opening:.0f} -> {opened:.0f}, toggle {filled}",
    )
    check(f"{tag}: no errors", not problems, "; ".join(problems[:3]))
    context.close()

    # Reduced motion: rows and what a source tells us are there at once.
    tag = "research reduced motion"
    context, page, response, problems = open_page(browser, f"{BASE}/", (1536, 1000), False, reduced=True)
    scroll_to(page, top_of(page, "#research ul") - 220, 900)
    page.click("#research button[aria-pressed] >> nth=2")
    page.wait_for_timeout(60)
    rows = page.evaluate(ROW_OPACITY)
    page.locator("#research ul > li:nth-child(1) summary").click()
    page.wait_for_timeout(60)
    words = page.evaluate(MORE_OPACITY)
    check(f"{tag}: rows and an opened note are there at once", rows == [1] * 6 and words == 1, f"{rows} | {words}")
    context.close()

    # Vietnamese: the longest label in the year's place.
    tag = "research vn"
    context, page, response, problems = open_page(browser, f"{BASE}/vn", (1536, 1000), False)
    scroll_to(page, top_of(page, "#research ul") - 220, 900)
    page.click("#research button[aria-pressed] >> nth=3")
    page.wait_for_timeout(1500)
    guides = page.evaluate(NOTES)
    word = page.evaluate("document.querySelector('#research summary > span').innerText")
    shoot(page, "research-vn-00-guides")
    check(
        f"{tag}: the guide label is sentence case and clear of the title",
        all(g["beside"] or g["above"] for g in guides) and word.replace("\n", " ") == "Hướng dẫn",
        word,
    )
    context.close()


def run_type(browser, mobile):
    """Fine typography (October 4): lines are set so no paragraph ends on a single word, no
    paragraph of two or more lines runs past about 75 characters, and the sample story's opening
    quotation mark hangs in the margin (its first letter on the same edge as the lines under it)."""
    tag = f"type {'phone' if mobile else 'desk'}"
    size = (390, 844) if mobile else (1536, 1000)
    context, page, response, problems = open_page(browser, f"{BASE}/", size, mobile)
    total = page.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < total:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(60)
        y += size[1] // 2
    scroll_to(page, top_of(page, "#stories h3") - 300, 1200)
    shoot(page, f"type-{'phone' if mobile else 'desk'}-00-quote")
    found = page.evaluate(TYPE)
    check(
        f"{tag}: no paragraph ends on a single word; none runs past 76 characters a line",
        found["wrap"] == "pretty" and not found["widows"] and not found["wide"],
        f"{found['wrap']} | widows {found['widows']} | wide {found['wide']}",
    )
    mark, mark_right, letter, lines, mark_left = found["hang"]
    check(
        f"{tag}: the story's opening quotation mark hangs in the margin",
        mark == "“" and abs(mark_right) <= 1 and abs(letter) <= 1 and abs(lines) <= 1 and mark_left >= 4,
        str(found["hang"]),
    )
    context.close()


with sync_playwright() as p:
    browser = p.chromium.launch(args=GPU)
    run(browser, "home", mobile=False)
    run(browser, "home", mobile=True)
    run_short(browser, "home")
    run_sizes(browser, "home")
    run_reduced(browser, "home")
    run_opens(browser)
    run_korean(browser, mobile=False)
    run_korean(browser, mobile=True)
    run_vietnamese(browser, mobile=False)
    run_vietnamese(browser, mobile=True)
    run_research(browser)
    run_type(browser, mobile=False)
    run_type(browser, mobile=True)
    browser.close()

passed = sum(1 for r in results if r[1])
print(f"\n{passed}/{len(results)} checks passed. Pictures: {OUT}")
sys.exit(0 if passed == len(results) else 1)
