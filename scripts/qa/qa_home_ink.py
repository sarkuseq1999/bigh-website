"""QA for the homepage, "Ink & Gold" with the crane (Mo's pick, October 2, 2026).

The homepage at / (and /kr). On the real GPU (ANGLE/D3D11):
  - desktop 1440x900 (full run) and phone 390x844 (full run):
    the page answers 200; no page errors, console errors or failed requests; the blocks in order
    (top, cellular, scientists, products, stories, science, research, purpose, then the footer);
    one h1; the header's links; the opening's paintings loaded and its words clear of each other;
    the brush line draws itself (ink on the canvas, its progress grows with the scroll, it is past
    the purpose's painting there, and it ends at the very bottom as the stroke under the footer's
    promise, beside the crane at rest, after one short rule over each of the three standards);
    the opening crane beats its wings (the animated painting takes the still's place) and stays a
    painting through the beat (its thinnest frame keeps at least 45% of the first pose's solid black
    ink: round 8; the old take fell to 38%), its wingbeats run without a pause (October 5: no frame
    held longer than 300 ms; the old loop held the wings up for seconds), and it beats twice and
    then rests on the still's pose (Mo, October 5: loop count 2, the last frame the first); Dr. Liu and Ask BiGH Science dialogs open and close; Dr. Liu's photo never shown
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
  - three painting sizes (round 4, October 4): on two columns the cell in "Tiny power plants." is
    the page's biggest painting after the opening (at least 1.3 times the science stage, which is
    at least 1.8 times the inkstone), runs off the right edge of the window with its gold folds
    inside it, keeps clear of its words' column and keeps its label in the window; the story
    still life runs off the left edge (about half the window wide), its label in the window, the
    quotation set large (4vw), the names and arrows under it and working; on a phone both run to
    both edges of the screen; with reduced motion (the whole line drawn) the brush line runs down
    the gaps beside both paintings and never over their subjects, their words or the story's
    names and arrows.
  - the phone as its own design (round 5, October 4): the opening is a painting first (its
    picture at least 44% of the window's height, the bird at least 58% of its width, a wingbeat
    picture sharp for the screen) with its two pills one over the other at the column's full
    width; the closing painting keeps the gold sun and both cranes in the window, the cranes on
    their own flying layer and the light on the sun's leaf; the stories open with their heading,
    then the still life, then the sample; the still lifes ship at their full 1744 px; the three
    science topics sit on one line and the age slider takes no room until its topic.
  - one centred pause and the page's rhythm (round 6, October 4): Ask BiGH Science's painting,
    headline, words and button are centred (the painting 300 to 410 px on desktop, about 70vw on
    a phone), its headline on two lines with no word alone, open paper above and below it; with
    the whole line drawn (1536 and 1440) the brush line passes it in the left margin, over none of
    it; on a phone no empty band between the story arrows and the science; at 1280x800, 1440x900,
    1536x1000, 1280x720, 1536x864, 1366x657 and 1440x700 the last screen shows the whole crane at
    rest and the whole promise, clear of the header.
  - the science as a scroll story (round 7, October 4): on two columns with motion the block is
    about two windows tall, its painting pinned beside the words; the desktop checks that
    clicked the three tabs are replaced on purpose: scrolling to each topic shows its words
    (earlier ones dissolved) beside its painting, pinned with the index level with it; the index
    glides to a topic; a topic leaves whole (its heading with its words) and between two topics a
    heading always stands in focus under the index (the next comes into focus as one leaves);
    the age slider ages the
    cell on the third topic, with its honesty line;
    each topic's explainer opens its own sheet; the painting, the index and the last topic leave
    together with no jump; the brush line passes beside the pinned painting (round 9: in the gap
    between the words and the painting's column, no longer the far margin), never over the
    painting, slider, index or words (1536x1000 and 1280x800, the whole line
    drawn); on a short window (1366x657) the whole pinned painting, slider and honesty line stay
    in the window; on a narrow one (1024x768) where a topic is taller than the room under the
    index, the block is the tabbed one instead (round 10, on purpose; it used to keep the index
    static beside a pinned painting); at 900x1000 the index sets its topics on one line. Phones
    and reduced motion keep the three tabs (no tall scroll, nothing pinned), with their checks as
    before.
  - authored arrivals and the finish (round 10, October 5): the products' big bottle rises 10px
    onto its ground as its pool gathers and the picker's five follow 70ms apart, waiting visibly
    out of view, never on a page opened at the products, never with reduced motion; choosing a
    product keeps the cross-fade without a rise; changing the story blooms the new still life
    through the ink mask (names and arrows), at once with reduced motion; at 900px the brush line
    keeps clear of the story names; the last screen shows the whole crane at 1280x720 and
    1536x864 too.
  - the brush line as one gesture (round 9, October 5): it passes the science in the gap between
    its words and its painting; every station's leader meets the line (1536x1000 and 1280x800,
    the whole line drawn). Round 9's lift over the picker was turned round ON PURPOSE (October 5,
    Mo saw a broken line): the line keeps going in one S, laying its ground under the first two
    picker bottles below their names (20 px or more under the chosen name's underline, never over
    a bottle or a name) and bending broadly down into the story gap, with no return (no ink under
    the last two bottles or beyond them) and 40 px or more clear of the stories' heading, unbroken
    from the big bottle's ground to the story gap (1440x900, and run_line at 900, 1024, 1280,
    1440, 1536, 1600 and 1920).
  - the page line's continuity (run_line, October 5): on every two-column width the route the
    page actually draws (the layer's data-lifts) leaves the paper only at the designed lifts
    named in DESIGNED_LIFTS; a new lift fails until it is added there on purpose.
    `--only=line` runs just these checks.

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


def ink_through_beat(page, src):
    """The wingbeat picture's solid black ink (dark areas at least 7 px across, so its thin lines
    are left out; 5 px in the phones' small picture) in its thinnest frame, as a share of the first
    pose's (the still's), its frame count, its longest frame in milliseconds, its loop count (0 =
    forever) and how far its last frame is from its first (mean difference, premultiplied, 0-255)."""
    import io

    import numpy as np
    from PIL import Image, ImageFilter, ImageSequence

    picture = Image.open(io.BytesIO(page.request.get(src).body()))
    k = 7 if picture.width >= 900 else 5
    solid = []
    longest = 0
    first = last = None
    for frame in ImageSequence.Iterator(picture):
        a = np.asarray(frame.convert("RGBA")).astype(np.float32)
        longest = max(longest, int(frame.info.get("duration") or 0))  # known once the frame is loaded
        last = np.concatenate([a[..., :3] * a[..., 3:] / 255, a[..., 3:]], axis=-1)
        first = last if first is None else first
        lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
        dark = Image.fromarray((((lum < 80) & (a[..., 3] > 128)) * 255).astype(np.uint8))
        solid.append(int((np.asarray(dark.filter(ImageFilter.MinFilter(k)).filter(ImageFilter.MaxFilter(k))) > 0).sum()))
    rest = float(np.abs(last - first).mean())
    return min(solid) / max(solid[0], 1), len(solid), longest, int(picture.info.get("loop", 0)), rest


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


def stations_on_line(page):
    """Round 9: each station's leader meets the brush line: ink just past the leader's tip, level
    with it (data-side names the side of the line the label sits on). Returns (label, ink)."""
    out = []
    count = page.evaluate("document.querySelectorAll('[data-station]').length")
    for i in range(count):
        page.evaluate(f"document.querySelectorAll('[data-station]')[{i}].scrollIntoView({{block: 'center'}})")
        page.wait_for_timeout(450)
        l, t, r, b, side, text = page.evaluate(
            f"""(() => {{ const e = document.querySelectorAll('[data-station]')[{i}]; const k = e.getBoundingClientRect();
              return [k.left, k.top, k.right, k.bottom, e.dataset.side, e.textContent.trim()]; }})()"""
        )
        cy = (t + b) / 2
        x0, x1 = (r + 2, r + 18) if side == "left" else (l - 18, l - 2)
        out.append((text, ink_in_box(page, x0, cy - 7, x1, cy + 7)))
    return out


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


def ink_joined(page, a, b):
    """Is there one unbroken run of brush ink from near window point a to near window point b?
    (The tiles' ink inside the window, flood-filled; a break wider than 2 px parts it.)"""
    return page.evaluate(
        """([ax, ay, bx, by]) => {
          const W = innerWidth, H = innerHeight;
          const c = document.createElement('canvas'); c.width = W; c.height = H;
          const ctx = c.getContext('2d');
          for (const t of document.querySelectorAll('[data-brush-layer] canvas')) {
            if (!t.width) continue;
            const r = t.getBoundingClientRect();
            ctx.drawImage(t, r.left, r.top, r.width, r.height);
          }
          const d = ctx.getImageData(0, 0, W, H).data;
          const ink = new Uint8Array(W * H);
          for (let i = 0; i < W * H; i++) ink[i] = d[i * 4 + 3] > 40 ? 1 : 0;
          const near = (x, y) => { let best = -1, bd = 1e9;
            for (let yy = Math.max(0, Math.round(y) - 14); yy <= Math.min(H - 1, Math.round(y) + 14); yy++)
              for (let xx = Math.max(0, Math.round(x) - 14); xx <= Math.min(W - 1, Math.round(x) + 14); xx++)
                if (ink[yy * W + xx]) { const e = (xx - x) ** 2 + (yy - y) ** 2; if (e < bd) { bd = e; best = yy * W + xx; } }
            return best; };
          const s = near(ax, ay), e = near(bx, by);
          if (s < 0 || e < 0) return [false, s < 0 ? 'no ink at the start' : 'no ink at the end'];
          const seen = new Uint8Array(W * H); const q = [s]; seen[s] = 1;
          while (q.length) {
            const i = q.pop(); if (i === e) return [true, 'joined'];
            const x = i % W, y = (i - x) / W;
            for (let dy = -2; dy <= 2; dy++) for (let dx = -2; dx <= 2; dx++) {
              const xx = x + dx, yy = y + dy;
              if (xx < 0 || yy < 0 || xx >= W || yy >= H) continue;
              const j = yy * W + xx; if (ink[j] && !seen[j]) { seen[j] = 1; q.push(j); }
            }
          }
          return [false, 'broken'];
        }""",
        [a[0], a[1], b[0], b[1]],
    )


# The picker and its neighbours, for the brush line: each pick's box, each small bottle (the
# photograph's middle, where the bottle stands), each name's words, the chosen name's 2px
# underline, the stories' heading (its words), the big bottle's ground and the story gap.
PICKER = """(() => {
  const r = (e) => { const b = e.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; };
  const text = (e) => { const g = document.createRange(); g.selectNodeContents(e); return r(g); };
  const picks = [...document.querySelectorAll('#products [data-brush=bottles] button')];
  const chosen = picks.find(p => p.getAttribute('aria-pressed') === 'true').querySelector('span:last-child');
  const c = r(chosen), cx = (c[0] + c[2]) / 2;
  const stand = r(document.querySelector('#products [data-brush=stage] img[data-shown=true]'));
  const painting = r(document.querySelector('[data-brush=story-painting]'));
  const words = r(document.querySelector('[data-brush=story-words]'));
  return {
    picker: r(document.querySelector('#products [data-brush=bottles]')),
    picks: picks.map(r),
    minis: picks.map(p => { const [l, t, rr, b] = r(p.querySelector('img:last-of-type')); const w = rr - l; return [l + 0.22 * w, t, rr - 0.22 * w, t + 0.96 * (b - t)]; }),
    names: picks.map(p => text(p.querySelector('span:last-child'))),
    underline: [cx - 22, c[3] - 2, cx + 22, c[3]],
    title: text(document.querySelector('#stories-title')),
    ground: [(stand[0] + stand[2]) / 2, stand[1] + 0.968 * (stand[3] - stand[1])],
    gap: [(painting[2] + words[0]) / 2 - 8, words[1] + 60],
  };
})()"""


def line_at_picker(page, tag):
    """The brush line round the products' picker (the whole line drawn, the picker in the window):
    the S (Mo, October 5): one ground under the first two small bottles below their names, never
    over a bottle or a name, 20 px or more under the chosen name's underline; then one broad bend
    down into the story gap, unbroken from the big bottle's ground, with no return and no turn in
    the right margin (no ink under the last two bottles or beyond them), 40 px or more clear of
    the stories' heading."""
    width = page.evaluate("innerWidth")
    g = page.evaluate(PICKER)
    pl, pt, pr, pb = g["picker"]
    under = [ink_in_box(page, l, pb + 6, r, pb + 64) for l, _, r, _ in g["picks"][:2]]
    over = [ink_in_box(page, *box) for box in g["minis"]] + [
        ink_in_box(page, l - 4, t - 4, r + 4, b + 4) for l, t, r, b in g["names"]
    ]
    check(
        f"{tag}: the brush lays its ground under the first two picker bottles, below their names, never over a bottle or a name",
        all(u > 30 for u in under) and not any(over),
        f"ground under the first two {under}, over bottles and names {over}",
    )
    ul, ut, ur, ub = g["underline"]
    near = ink_in_box(page, ul - 12, ut - 30, ur + 12, ub + 20)
    below = ink_in_box(page, ul - 12, ub + 20, ur + 12, ub + 70)
    check(
        f"{tag}: the ground passes under the chosen name 20 px or more clear of its underline",
        near == 0 and below > 30,
        f"ink within 20 px of the underline {near}, the ground below it {below}",
    )
    tl, tt, tr, tb = g["title"]
    beyond = ink_in_box(page, g["picks"][3][0], pt, width, tt)
    over_title = ink_in_box(page, tl - 4, tt - 40, tr + 4, tb)
    joined, how = ink_joined(page, g["ground"], g["gap"])
    check(
        f"{tag}: unbroken from the big bottle's ground, one bend down into the story gap (no return, 40 px clear of the heading)",
        joined and beyond == 0 and over_title == 0,
        f"{how}, under the last two bottles or beyond them {beyond}, within 40 px of the heading {over_title}",
    )


# The brush line's designed lifts on the two-column page: the only places the page line may leave
# the paper, each as (the anchor it lifts after, the anchor it lands at), as the brush layer
# publishes them (data-lifts, brush.tsx). The picker's lift (round 9) was taken out on Mo's word
# (October 5): a new lift must be added here on purpose.
DESIGNED_LIFTS = {
    ("opening-flight", "opening-stage"): "the opening's own lift over the far ridges",
    ("purpose-painting", "standard-0"): "the lift into the closing painting's sky, on to the first standard's rule",
    ("standard-0", "standard-1"): "the travel between the standards' rules",
    ("standard-1", "standard-2"): "the travel between the standards' rules",
    ("standard-2", "footer-promise"): "the travel to the footer's closing stroke",
}
LIFT_MIN = 40  # px of path off the paper; anything shorter is a taper, not a lift
LINE_SIZES = [(900, 1000), (1024, 1000), (1280, 800), (1440, 900), (1536, 1000), (1600, 1000), (1920, 1080)]


def run_line(browser):
    """The page line's continuity on every two-column width (the guard round 9's picker gap slipped
    past): it leaves the paper only at the designed lifts above, read from the route the page
    actually draws; and round the picker it runs on unbroken (the whole line drawn: reduced motion)."""
    context, page, response, problems = open_page(browser, f"{BASE}/", (1536, 1000), False)
    for w, h in LINE_SIZES:
        page.set_viewport_size({"width": w, "height": h})
        page.wait_for_timeout(900)
        lifts = page.evaluate("JSON.parse(document.querySelector('[data-brush-layer]')?.dataset.lifts || 'null')")
        real = [l for l in (lifts or []) if l[2] > LIFT_MIN]
        stray = [f"{a} -> {b} ({n} px at y {y0}-{y1})" for a, b, n, y0, y1 in real if (a, b) not in DESIGNED_LIFTS]
        seen = {(a, b) for a, b, *_ in real}
        read = lifts is not None and ("opening-flight", "opening-stage") in seen and ("standard-2", "footer-promise") in seen
        check(
            f"line {w}x{h}: the page line leaves the paper only at its designed lifts",
            read and not stray,
            ("; ".join(stray) or f"{len(real)} lifts, all designed") if read else f"lifts not readable: {lifts}",
        )
    context.close()
    context, page, response, problems = open_page(browser, f"{BASE}/", (1536, 1000), False, reduced=True)
    for w, h in LINE_SIZES:
        page.set_viewport_size({"width": w, "height": h})
        page.wait_for_timeout(700)
        page.evaluate("document.querySelector('#products [data-brush=bottles]').scrollIntoView({block: 'center'})")
        page.wait_for_timeout(500)
        line_at_picker(page, f"line {w}x{h}")
    check("line: no errors", not problems, "; ".join(problems[:3]))
    context.close()


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

# Round 4: the three painting sizes. The cell (its figure, unturned) and its words, the story
# still life and its words, the quotation's size, the story's names and arrows, and the science
# stage and the inkstone for scale, as [left, top, right, bottom] in the window.
PAINTINGS = """(() => {
  const r = (s) => { const e = document.querySelector(s); if (!e) return null; const b = e.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; };
  const text = (s) => { const g = document.createRange(); g.selectNodeContents(document.querySelector(s)); const b = g.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; };
  return {
    win: innerWidth,
    cell: r('#cellular [data-brush=cellular-mito]'), cellWords: r('#cellular [data-brush=cellular-words]'),
    cellCap: text('#cellular figcaption'), cellLines: r('#cellular ol'),
    still: r('#stories [data-brush=story-painting]'), stillTag: r('#stories figcaption'),
    storyWords: r('#stories [data-brush=story-words]'), storyHead: r('#stories header'), story: r('#stories article'),
    quote: parseFloat(getComputedStyle(document.querySelector('#stories article h3')).fontSize),
    choices: r('#stories [data-brush=story-choices]'), arrows: r('#stories button[aria-label="Next sample story"]'),
    arrowsBox: r('#stories button[aria-label="Previous sample story"]'),
    science: r('#science [data-brush=science-mito]'), inkstone: r('#scientists img[src*=inkstone]'),
  };
})()"""


# Round 5, phones: the opening's picture, the bird's width (its picture is 64.6% bird), the
# wingbeat picture's own width and the pixels the crane needs on this screen (the full picture is
# 900), the two pills and the words' column, as [left, top, right, bottom].
PHONE_OPENING = """(() => {
  const r = (e) => { const b = e.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; };
  const art = document.querySelector('#top [data-brush=opening-art]').getBoundingClientRect();
  const crane = document.querySelector('#top [data-brush=crane]').getBoundingClientRect();
  const flight = document.querySelector('#top img[src*=crane-flight]');
  const title = document.querySelector('#opening-title');
  const pills = [...title.parentElement.querySelectorAll(':scope > div > a, :scope > div > button')].map(r);
  return { art: art.height, bird: crane.width * 0.646, flight: flight ? flight.naturalWidth : 0,
    need: Math.min(900, Math.round(crane.width * devicePixelRatio)), pills,
    col: r(title.parentElement.querySelector('p')) };
})()"""

# Round 5, phones: where the closing painting's gold sun (76.7% to 84.6% of its width) and the
# cranes' layer fall in the window, and whether the cranes and the light on the leaf are shown.
PURPOSE_FRAME = """(() => {
  const p = document.querySelector('#purpose [data-brush=purpose-painting]').getBoundingClientRect();
  const f = document.querySelector('#purpose img[src*=purpose-cranes]');
  const b = f.parentElement.getBoundingClientRect();
  const light = document.querySelector('#purpose [data-brush=purpose-painting] + span');
  return { sun: [Math.round(p.left + 0.767 * p.width), Math.round(p.left + 0.846 * p.width)],
    cranes: [Math.round(b.left), Math.round(b.right)], flight: getComputedStyle(f.parentElement).display,
    light: getComputedStyle(light).display, loaded: f.complete && f.naturalWidth > 0 };
})()"""

# Round 5: each story still life's own picture width (the file the optimizer is given).
STILL_SOURCE = """(async () => Promise.all([...document.querySelectorAll('#stories figure img')].map((i) =>
  new Promise((ok) => { const u = new URL(i.getAttribute('src'), location.href);
    const im = new Image(); im.onload = () => ok(im.naturalWidth); im.onerror = () => ok(0);
    im.src = u.searchParams.get('url') || u.pathname; }))))()"""


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


def set_age(page, value):
    """Move the age slider (as a hand would) and read the age shown, the honesty line's opacity
    and the aged painting's opacity."""
    page.evaluate(
        f"""(() => {{ const input = document.querySelector('#science input[type=range]');
          const set = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
          set.call(input, '{value}'); input.dispatchEvent(new Event('input', {{ bubbles: true }})); }})()"""
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
    return age, honesty, aged


# Round 7: the science block's mode (the scroll story or the tabs) and its height.
TABBED = """(() => { const s = document.querySelector('#science');
  return { story: s.dataset.story, tabs: s.querySelectorAll('[role=tab]').length, height: s.offsetHeight,
    sticky: getComputedStyle(s.querySelector('figure')).position }; })()"""

# Round 7: the scroll story's state: the pinned painting and index, the topic shown, each topic's
# heading (top, bottom, opacity, words) and each painting layer's opacity (closeup, young, radicals,
# aged), in the window.
STORY_STATE = """(() => {
  const s = document.querySelector('#science'); const cs = getComputedStyle(s);
  const fig = s.querySelector('figure'); const nav = s.querySelector('nav');
  const r = (e) => { const b = e.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; };
  const pin = parseFloat(cs.getPropertyValue('--pin'));
  return { story: s.dataset.story, height: s.offsetHeight, sticky: getComputedStyle(fig).position,
    tabs: s.querySelectorAll('[role=tab]').length, steps: s.querySelectorAll('[data-step]').length,
    pin, landing: pin + (nav ? nav.offsetHeight : 0), topic: +fig.dataset.topic,
    current: nav ? [...nav.querySelectorAll('button')].findIndex(b => b.getAttribute('aria-current') === 'step') : -1,
    fig: r(fig), stage: r(fig.firstElementChild), age: r(fig.querySelector('input').closest('div')),
    copy: r(s.querySelector('[data-brush=science-copy]')),
    index: nav ? r(nav) : null, scroll: scrollY,
    titles: [...s.querySelectorAll('[data-step] h3')].map(h => [r(h)[1], r(h)[3], +getComputedStyle(h).opacity * +getComputedStyle(h.parentElement).opacity, h.textContent]),
    words: [...s.querySelectorAll('[data-step]')].map(e => { const k = [...e.children].map(r);
      return [Math.min(...k.map(b => b[0])), Math.min(...k.map(b => b[1])), Math.max(...k.map(b => b[2])), Math.max(...k.map(b => b[3]))]; }),
    layers: [...fig.querySelectorAll('img')].map(i => +getComputedStyle(i).opacity),
  };
})()"""


def walk_to(page, y, wait=2600):
    """Scroll there the way a reader does (in short steps), then wait for the painting."""
    cur = page.evaluate("scrollY")
    step = 150 if y > cur else -150
    while abs(y - cur) > 150:
        cur += step
        page.evaluate(f"window.scrollTo(0, {int(cur)})")
        page.wait_for_timeout(30)
    page.evaluate(f"window.scrollTo(0, {int(y)})")
    page.wait_for_timeout(wait)


def story_landing(page, i):
    """The scroll position at which topic i has arrived under the pinned index."""
    return page.evaluate(
        f"""(() => {{ const s = document.querySelector('#science'); const nav = s.querySelector('nav');
          const landing = parseFloat(getComputedStyle(s).getPropertyValue('--pin')) + nav.offsetHeight;
          return Math.round(scrollY + s.querySelectorAll('[data-step]')[{i}].getBoundingClientRect().top - landing); }})()"""
    )


def painting_shows(state, i):
    """Is topic i's painting the one on the stage (the others gone)?"""
    a = state["layers"]
    if i == 0:
        return a[0] >= 0.95 and a[2] <= 0.05 and a[3] <= 0.05
    if i == 1:
        return a[2] >= 0.95 and a[0] <= 0.05 and a[3] <= 0.05
    return a[1] + a[3] >= 0.95 and a[0] <= 0.05 and a[2] <= 0.05


def science_story(page, tag, name, view_h):
    """Round 7 (October 4): on two columns with motion "Make sense of the science." is a scroll
    story, one idea per screen. This replaces, on purpose, the desktop checks that clicked the
    three tabs: scrolling to each topic shows its words and its painting (pinned beside them),
    the index takes you to a topic, the age slider still ages the cell on the third, each topic's
    explainer opens its own sheet, and the pinned painting leaves with the last topic, no jump."""
    s = page.evaluate(STORY_STATE)
    check(
        f"{tag}: the science is a scroll story, about two windows tall, its painting pinned",
        s["story"] == "true" and s["tabs"] == 0 and s["steps"] == 3 and s["sticky"] == "sticky"
        and 1.8 * view_h <= s["height"] <= 4 * view_h,
        f"story {s['story']}, height {s['height']} ({s['height'] / view_h:.1f} windows), {s['sticky']}",
    )
    seen, bad = [], []
    for i in range(3):
        walk_to(page, story_landing(page, i))
        st = page.evaluate(STORY_STATE)
        shoot(page, f"{name}-05-science-step{i + 1}")
        top, bottom, opacity, words = st["titles"][i]
        earlier = [t[2] for t in st["titles"][:i]]
        ok = (
            st["topic"] == i
            and st["current"] == i
            and opacity >= 0.99
            and top >= st["landing"] - 1
            and bottom <= view_h
            and all(o <= 0.01 for o in earlier)
            and painting_shows(st, i)
            and abs(st["fig"][1] - st["pin"]) <= 1
            and abs(st["index"][1] - st["pin"]) <= 1
        )
        seen.append(f"{i + 1}: topic {st['topic']} index {st['current']} words {top:.0f}-{bottom:.0f} at {opacity:.2f}, earlier {earlier}, layers {st['layers']}, painting at {st['fig'][1]:.0f} (pin {st['pin']:.0f})")
        if not ok:
            bad.append(i + 1)
    check(
        f"{tag}: scrolling to each topic shows its words beside its painting, pinned (earlier words gone)",
        not bad,
        f"wrong: {bad}; " + " | ".join(seen),
    )
    # A topic leaves whole: just past its place every line of it is equally faded (no paragraph
    # left without its heading).
    walk_to(page, story_landing(page, 1) + 28, 400)
    fades = page.evaluate(
        "[...document.querySelectorAll('#science [data-step=\"1\"] > *')].map(e => +(+getComputedStyle(e).opacity).toFixed(2))"
    )
    check(
        f"{tag}: a topic leaves whole, its heading with its words",
        len(fades) == 4 and max(fades) - min(fades) <= 0.02 and 0.15 <= fades[0] <= 0.85,
        f"opacity of heading, words, facts, links {fades}",
    )
    # Wherever the reader stops between two topics, a topic's heading stands in the room under
    # the index, at least half in focus (the words are never all gone: as one leaves, the next
    # comes into focus).
    a, b = story_landing(page, 0), story_landing(page, 1)
    walk_to(page, a, 600)
    empty = []
    for y in range(a, b + 1, 40):
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(70)
        st = page.evaluate(STORY_STATE)
        if not any(o >= 0.5 and t >= st["landing"] - 1 and bo <= view_h for t, bo, o, _ in st["titles"]):
            empty.append(y - a)
    check(
        f"{tag}: between two topics a heading always stands under the index, in focus",
        not empty,
        f"no heading at {empty} px past the first topic (of {b - a})",
    )
    walk_to(page, story_landing(page, 2))
    # The third topic: the age slider still ages the cell, with its honesty line.
    age, honesty, aged = set_age(page, 70)
    check(
        f"{tag}: on the third topic the age slider ages the cell; honesty label shown",
        age == "70" and honesty > 0.9 and 0.7 < aged < 0.9,
        f"age {age}, label {honesty}, aged {aged:.2f}",
    )
    shoot(page, f"{name}-06-science-age")
    set_age(page, 45)
    # The index: choosing a topic glides the page until that topic has arrived.
    reached = []
    for i, label in ((0, "Mitochondria"), (1, "Free radicals"), (2, "Aging cells")):
        page.click(f"#science nav button:has-text('{label}')")
        page.wait_for_timeout(2600)
        st = page.evaluate(STORY_STATE)
        top = st["titles"][i][0]
        reached.append((i, st["topic"], st["current"], round(top - st["landing"]), st["titles"][i][2]))
    check(
        f"{tag}: choosing a topic in the index glides to it",
        all(t == i and c == i and 40 <= d <= 56 and o >= 0.99 for i, t, c, d, o in reached),
        f"(topic, shown, index, words below the index, opacity) {reached}",
    )
    # Each topic's explainer opens its own sheet.
    titles = []
    for i in range(3):
        page.evaluate(f"document.querySelector('#science [data-step=\"{i}\"] button').scrollIntoView({{block: 'center'}})")
        page.wait_for_timeout(1700)
        page.click(f"#science [data-step=\"{i}\"] button")
        page.wait_for_timeout(700)
        titles.append(dialog_title(page))
        page.keyboard.press("Escape")
        page.wait_for_timeout(600)
    check(
        f"{tag}: each topic's explainer opens its own sheet",
        all(titles) and len(set(titles)) == 3,
        " | ".join(titles),
    )
    # The end: from the last topic's arrival the painting, the index and the last topic's words
    # leave together, with the scroll, and before it the painting holds still: no jump.
    release = story_landing(page, 2)
    walk_to(page, release - 200, 900)
    trace = []
    for k in range(21):
        page.evaluate(f"window.scrollTo(0, {release - 200 + 20 * k})")
        page.wait_for_timeout(60)
        st = page.evaluate(STORY_STATE)
        trace.append((st["scroll"], st["fig"][1], st["index"][1], st["titles"][2][0]))
    pin = st["pin"]
    off = [
        round(f - (pin - max(0, y - release)), 1)
        for y, f, _, _ in trace
    ]
    together = [round((f - i), 1) for _, f, i, _ in trace]
    step_words = [round(trace[k + 1][3] - trace[k][3], 1) for k in range(10, 20)]
    check(
        f"{tag}: the pinned painting holds still, then leaves with the index and the last topic (no jump)",
        max(abs(v) for v in off) <= 1.5 and max(together) - min(together) <= 1.5 and all(abs(d + 20) <= 1.5 for d in step_words),
        f"painting off its expected place {off}; painting minus index {sorted(set(together))}; last words per 20 px {step_words}",
    )
    shoot(page, f"{name}-05-science-release")


def run_story(browser):
    """Round 7: the brush line passes the scroll story beside the pinned painting, never over the
    painting, the age slider, the index or the words (at 1536x1000, after scrolling to the end so
    the whole line is drawn); no sideways scrolling; the same story holds at 1280x800. Round 9:
    it passes in the gap between the words and the painting's column (no longer in the far
    margin), and every station's leader meets the line."""
    for size in ((1536, 1000), (1280, 800)):
        tag = f"story {size[0]}x{size[1]}"
        context, page, response, problems = open_page(browser, f"{BASE}/", size, False)
        total = page.evaluate("document.documentElement.scrollHeight")
        y = 0
        while y < total:
            page.evaluate(f"window.scrollTo(0, {y})")
            page.wait_for_timeout(40)
            y += 200
        try:
            page.wait_for_function("+document.querySelector('[data-brush-layer]').dataset.progress >= 0.999", timeout=15000)
        except Exception:  # noqa: BLE001
            pass
        top = top_of(page, "#science")
        stops = [("start", top - 40)] + [(f"topic {i + 1}", story_landing(page, i)) for i in range(3)]
        stops.insert(2, ("between 1 and 2", (stops[1][1] + story_landing(page, 1)) // 2))
        stops.append(("after", stops[-1][1] + 240))
        over, beside = [], []
        for label, at in stops:
            walk_to(page, at, 1600)
            st = page.evaluate(STORY_STATE)
            fl, ft, fr, fb = st["stage"]
            inset = 0.08 if label == "start" else 0.0
            w, h = fr - fl, fb - ft
            hits = {
                "painting": ink_in_box(page, fl + inset * w, ft + inset * h, fr - inset * w, fb - inset * h),
                "slider": ink_in_box(page, *st["age"]) if st["topic"] == 2 else 0,
                "index": ink_in_box(page, *st["index"]),
            }
            for i, box in enumerate(st["words"]):
                if box[3] > 0 and box[1] < size[1] and st["titles"][i][2] > 0.05:
                    hits[f"words {i + 1}"] = ink_in_box(page, box[0] - 4, box[1], box[2] + 4, box[3])
            hits = {k: v for k, v in hits.items() if v}
            if hits:
                over.append(f"{label}: {hits}")
            if label.startswith("topic"):
                beside.append(ink_in_box(page, st["copy"][2], max(st["fig"][1], 90), st["fig"][0], st["fig"][3]))
            if size[0] == 1536:
                shoot(page, f"story-{size[0]}-{label.replace(' ', '-')}")
        check(
            f"{tag}: the brush line passes the scroll story in the gap beside the painting, never over the painting, slider, index or words",
            not over and all(b > 150 for b in beside),
            f"over: {over}; in the gap beside the pinned painting at each topic {beside}",
        )
        missed = [f"{text} {ink}" for text, ink in stations_on_line(page) if ink == 0]
        check(f"{tag}: every station's leader meets the brush line", not missed, f"no ink at the leader's tip: {missed}")
        wide = page.evaluate("document.documentElement.scrollWidth")
        check(f"{tag}: no sideways scrolling", wide <= size[0], f"scrollWidth {wide}")
        check(f"{tag}: no errors", not problems, "; ".join(problems[:3]))
        context.close()
    # A short laptop window (1366x657): the painting gives way so all of it, the slider and its
    # honesty line stay in the window while pinned. A narrow one (1024x768), where a topic is
    # taller than the room under the index: the tabbed block instead (round 10).
    for size in ((1366, 657), (1024, 768)):
        tag = f"story {size[0]}x{size[1]}"
        context, page, response, problems = open_page(browser, f"{BASE}/", size, False)
        walk_to(page, top_of(page, "#science"), 600)
        if size[1] >= 700:
            # Round 10 changed this ON PURPOSE: where a topic is taller than the room under the
            # index the index used to stay put (static) while the painting stayed pinned, so the
            # index scrolled away from a pinned painting. Now the block gives way to the tabbed
            # block there: nothing pinned, the three topics on one line, one panel at a time.
            k = page.evaluate(
                """(() => { const s = document.querySelector('#science');
                  const tabs = [...s.querySelectorAll('[role=tab]')].map(t => Math.round(t.getBoundingClientRect().top));
                  return { story: s.dataset.story, tabs, panels: s.querySelectorAll('[role=tabpanel]').length,
                    sticky: getComputedStyle(s.querySelector('figure')).position, steps: s.querySelectorAll('[data-step]').length }; })()"""
            )
            page.click("#science [role=tab]:has-text('Aging cells')")
            page.wait_for_timeout(1300)
            aged = page.evaluate(STORY_STATE)
            check(
                f"{tag}: a topic taller than the room under the index: the tabbed block instead, its three topics on one line",
                k["story"] == "false" and len(k["tabs"]) == 3 and len(set(k["tabs"])) == 1 and k["panels"] == 1
                and k["sticky"] != "sticky" and k["steps"] == 0 and aged["topic"] == 2,
                f"{k}, after choosing Aging cells topic {aged['topic']}",
            )
            shoot(page, "story-1024x768-tabs")
            wide = page.evaluate("document.documentElement.scrollWidth")
            check(f"{tag}: no sideways scrolling, no errors", wide <= size[0] and not problems, f"scrollWidth {wide}; {problems[:2]}")
            context.close()
            continue
        walk_to(page, story_landing(page, 2), 2600)
        st = page.evaluate(STORY_STATE)
        check(
            f"{tag}: on a short window the whole painting, its slider and honesty line stay in the window, pinned",
            st["story"] == "true" and abs(st["fig"][1] - st["pin"]) <= 1 and st["fig"][3] <= size[1]
            and st["age"][3] <= size[1] and st["topic"] == 2,
            f"painting {st['fig'][1]:.0f} to {st['fig'][3]:.0f}, slider ends {st['age'][3]:.0f}, window {size[1]}",
        )
        wide = page.evaluate("document.documentElement.scrollWidth")
        check(f"{tag}: no sideways scrolling, no errors", wide <= size[0] and not problems, f"scrollWidth {wide}; {problems[:2]}")
        context.close()
    # Round 10: on a narrow two-column window the index sets its three topics on one line (at 21px
    # "Aging cells" broke onto a row of its own), and where a topic fits, the story runs.
    context, page, response, problems = open_page(browser, f"{BASE}/", (900, 1000), False)
    walk_to(page, top_of(page, "#science"), 600)
    k = page.evaluate(
        """(() => { const s = document.querySelector('#science'); const nav = s.querySelector('nav');
          return { story: s.dataset.story, tops: nav ? [...nav.querySelectorAll('button')].map(b => Math.round(b.getBoundingClientRect().top)) : [],
            font: nav ? parseFloat(getComputedStyle(nav.querySelector('button')).fontSize) : 0 }; })()"""
    )
    check(
        "story 900x1000: the scroll story runs, its index's three topics on one line",
        k["story"] == "true" and len(k["tops"]) == 3 and len(set(k["tops"])) == 1 and k["font"] >= 17,
        str(k),
    )
    context.close()


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
        "[...document.querySelectorAll('img')].filter(i => i.getClientRects().length > 0 && !i.closest('[data-nav-panel]:not([data-open]), header:not([data-menu]) [data-nav-sheet]') && (!i.complete || i.naturalWidth === 0)).map(i => i.currentSrc || i.src)"
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

    # Header links (the menu bar "Inscription", October 5, 2026; scripts/qa/qa_nav.py checks how it
    # behaves): Products and Science open their drop-downs, no "Home" (the mark goes home). Each
    # drop-down reaches every page: the five product pages, the Science page's four parts.
    nav = page.evaluate(
        """(() => { const n = document.querySelector('#site-navigation');
          return { triggers: [...n.querySelectorAll('[data-nav-trigger]')].map(b => b.dataset.navTrigger),
            about: n.querySelector('a[href$="/about"]')?.getAttribute('href') || '',
            support: [...n.querySelectorAll('button')].some(b => b.textContent.trim() === 'Support'),
            home: [...n.querySelectorAll('a')].some(a => a.textContent.trim() === 'Home'),
            products: new Set([...n.querySelectorAll('[data-nav-panel=products] a[href*="/products/"]')].map(a => a.getAttribute('href'))).size,
            science: new Set([...n.querySelectorAll('[data-nav-panel=science] a[href*="/science#"]')].map(a => a.getAttribute('href'))).size }; })()"""
    )
    check(
        f"{tag}: header links",
        nav["triggers"] == ["products", "science"]
        and nav["about"].endswith("/about")
        and nav["support"]
        and not nav["home"]
        and nav["products"] == 5
        and nav["science"] == 4,
        str(nav),
    )

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
    # Round 8: the wingbeat stays a painting (the old take turned into an outline drawing mid-beat).
    src = page.evaluate("document.querySelector('#top img[src*=crane-flight]')?.currentSrc || ''")
    thinnest, frames, longest, loops, rest = ink_through_beat(page, src) if src else (0, 0, 0, -1, 99)
    check(
        f"{tag}: the wingbeat keeps its black ink through the beat",
        frames > 30 and thinnest >= 0.45,
        f"thinnest frame {thinnest:.0%} of the first pose's solid ink, {frames} frames, {src[-28:]}",
    )
    # October 5 (Mo): the wings beat without a pause. The old loop held the wings-up pose for 1.4 s
    # and 4.2 s around each beat, which read as fake; no frame may stay longer than 300 ms. Changed
    # ON PURPOSE the same day (Mo: "fly like 2 times, then stop"): the beats still run without a
    # pause, and the rest after them is the picture stopping (its loop count), not a held frame.
    check(
        f"{tag}: the crane's wingbeats run without a pause (no frame held over 300 ms)",
        frames > 30 and 0 < longest <= 300,
        f"longest frame {longest} ms",
    )
    # Mo (October 5): two beats, then the crane rests for good in the still painting's pose. The
    # picture plays twice (loop count 2) and its last frame, where it stops, is its first pose.
    check(
        f"{tag}: the crane beats twice, then rests on the still's pose (loop count 2, last frame = first)",
        loops == 2 and rest <= 0.8,
        f"loop count {loops}, last frame differs from the first by {rest:.2f} (0-255)",
    )
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
    # Round 5: the phone's opening is a painting first: the picture about 46% of the window's
    # height, the bird about 62% of its width (a wingbeat picture sharp for the screen: the full
    # one on a 2x screen), and the two pills one over the other at the column's full width, 52 px or taller.
    if mobile:
        o = page.evaluate(PHONE_OPENING)
        check(
            f"{tag}: the opening is a painting first, the crane nearly the window's width",
            o["art"] >= 0.44 * view_h and o["bird"] >= 0.58 * width and o["flight"] >= o["need"],
            f"picture {o['art']:.0f} px tall, bird {o['bird']:.0f} px wide, wingbeat picture {o['flight']} px (needs {o['need']})",
        )
        pills, col = o["pills"], o["col"]
        check(
            f"{tag}: the opening's two pills stack at the column's full width",
            len(pills) == 2
            and all(abs(p[0] - col[0]) < 1 and abs(p[2] - col[2]) < 1 and p[3] - p[1] >= 52 for p in pills)
            and pills[1][1] >= pills[0][3],
            f"pills {[[round(v) for v in p] for p in pills]}, column {round(col[0])} to {round(col[2])}",
        )
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
    # Round 4: three painting sizes. The cell is the page's biggest painting after the opening.
    g = page.evaluate(PAINTINGS)
    cl, ct, cr, cb = g["cell"]
    cw = cr - cl
    cap = g["cellCap"]
    if mobile:
        check(
            f"{tag}: the cell runs to both edges of the screen, its label in the window",
            cl <= 0 and cr >= g["win"] and cap[0] >= 0 and cap[2] <= g["win"],
            f"cell {cl:.0f} to {cr:.0f}, label {cap[0]:.0f} to {cap[2]:.0f}",
        )
    else:
        sci = g["science"][2] - g["science"][0]
        stone = g["inkstone"][2] - g["inkstone"][0]
        check(
            f"{tag}: three painting sizes: the cell, then the science stage, then the inkstone",
            cw >= 1.3 * sci and sci >= 1.8 * stone,
            f"cell {cw:.0f}, science {sci:.0f}, inkstone {stone:.0f} css px",
        )
        check(
            f"{tag}: the cell runs off the window's right edge, its gold inside it, clear of its words, its label in view",
            cr >= g["win"] + 0.12 * cw
            and cl + 0.65 * cw <= g["win"] - 40
            and cl >= g["cellWords"][2]
            and cap[2] <= g["win"] - 20,
            f"cell {cl:.0f} to {cr:.0f} (window {g['win']}), words end {g['cellWords'][2]:.0f}, label ends {cap[2]:.0f}",
        )

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
        # Round 9 lifted the brush at the end of the big bottle's ground and landed it again under
        # the picker. Mo saw a broken line (October 5), so this check is turned round ON PURPOSE:
        # the line keeps going, in one S. It bows down past the left of the picker, lays its
        # ground under the first two bottles below their names (never over a bottle or a name,
        # clear of the chosen name's underline) and bends broadly down into the story gap,
        # unbroken (run_line holds it at every two-column width).
        page.evaluate("document.querySelector('#products [data-brush=bottles]').scrollIntoView({block: 'center'})")
        page.wait_for_timeout(2600)
        line_at_picker(page, tag)

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
    # Round 4: the still life runs off the window's edge; the quotation is set large; the names
    # and arrows stay under it and work.
    g = page.evaluate(PAINTINGS)
    sl, st, sr, sb = g["still"]
    if mobile:
        check(
            f"{tag}: the still life runs to both edges of the screen, its label at the gutter",
            sl <= 0 and sr >= g["win"] and g["stillTag"][0] >= 16,
            f"still life {sl:.0f} to {sr:.0f}, label at {g['stillTag'][0]:.0f}",
        )
        # Round 5: the block opens with its heading; the still life sits between it and the sample.
        check(
            f"{tag}: the stories open with their heading, then the still life, then the sample",
            g["storyHead"][3] <= st + 1 and g["story"][1] >= sb - 1,
            f"heading ends {g['storyHead'][3]:.0f}, still life {st:.0f} to {sb:.0f}, sample from {g['story'][1]:.0f}",
        )
        widths = page.evaluate(STILL_SOURCE)
        check(
            f"{tag}: the still lifes ship at their full 1744 px (sharp on 2x screens)",
            len(widths) == 3 and all(w >= 1700 for w in widths),
            str(widths),
        )
    else:
        check(
            f"{tag}: the still life runs off the window's left edge, about half the window wide, its label in view",
            sl <= -0.08 * (sr - sl)
            and sr - sl >= 0.47 * g["win"]
            and sr <= g["storyWords"][0] - 40
            and g["stillTag"][0] >= 16,
            f"still life {sl:.0f} to {sr:.0f}, words from {g['storyWords'][0]:.0f}, label at {g['stillTag'][0]:.0f}",
        )
        check(
            f"{tag}: the quotation set large, the names and arrows under the still life",
            g["quote"] >= 0.039 * g["win"] and g["choices"][1] >= sb - 1 and g["arrows"][1] >= sb - 1,
            f"quotation {g['quote']:.1f} px, names from {g['choices'][1]:.0f}, still life ends {sb:.0f}",
        )
    page.click("#stories button[aria-label='Next sample story']")
    page.wait_for_timeout(1000)
    after = page.locator("#stories article h3").text_content()
    check(f"{tag}: the arrow goes on to the next story", "source" in after, after)

    # Science.
    scroll_to(page, top_of(page, "#science") + (0 if mobile else 40), 1500)
    shoot(page, f"{name}-05-science")
    # Round 7: on two columns with motion the science is a scroll story (its own checks); phones
    # keep the three tabs, checked as before.
    if not mobile:
        science_story(page, tag, name, view_h)
    # Round 5: on a phone the three topics sit on one line, and the age slider takes no room
    # under the stage until its own topic is chosen.
    if mobile:
        k = page.evaluate(TABBED)
        check(
            f"{tag}: the science keeps its three tabs (no tall scroll, nothing pinned)",
            k["story"] == "false" and k["tabs"] == 3 and k["sticky"] != "sticky" and k["height"] < 2 * view_h,
            str(k),
        )
        t = page.evaluate(
            """(() => ({ tops: [...document.querySelectorAll('#science [role=tab]')].map(t => Math.round(t.getBoundingClientRect().top)),
              age: getComputedStyle(document.querySelector('#science input[type=range]').closest('div')).display }))()"""
        )
        check(
            f"{tag}: the three topics sit on one line; the age slider waits for its topic",
            len(t["tops"]) == 3 and len(set(t["tops"])) == 1 and t["age"] == "none",
            str(t),
        )
        page.click("#science [role=tab]:has-text('Free radicals')")
        page.wait_for_timeout(1300)
        radicals = page.locator("#science [role=tabpanel] h3").text_content()
        page.click("#science [role=tab]:has-text('Aging cells')")
        page.wait_for_timeout(1300)
        aging = page.locator("#science [role=tabpanel] h3").text_content()
        age, honesty, aged = set_age(page, 70)
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
    # Round 5: on a phone the closing painting is framed for the window: the gold sun and both
    # cranes inside it, the cranes on their own (flying) layer, the light on the sun's leaf on.
    if mobile:
        c = page.evaluate(PURPOSE_FRAME)
        check(
            f"{tag}: the closing painting keeps the gold sun and both cranes in the window, flying",
            0 <= c["sun"][0]
            and c["sun"][1] <= width
            and 0 <= c["cranes"][0]
            and c["cranes"][1] <= width
            and c["flight"] != "none"
            and c["light"] != "none"
            and c["loaded"],
            str(c),
        )
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
              column: box('#cellular-title'),
              bar: (() => { const l = [...document.querySelectorAll('#site-navigation label')].find(e => e.getClientRects().length);
                const b = l.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; })(),
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
        f"{tag}: the opening's words start at the page column's left edge, under the bar's first control",
        abs(b["title"][0] - b["column"][0]) <= 2 and abs(b["title"][0] - b["bar"][0]) <= 12,
        f"title {b['title'][0]:.0f}, column {b['column'][0]:.0f}, bar {b['bar'][0]:.0f}",
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
# The visible Support in the header: the bar's on a desktop, the open menu's on a phone.
SUPPORT = (
    "[...document.querySelectorAll('header button:not([data-nav-menu-button]):not([data-nav-trigger])"
    ":not([data-nav-sheet-toggle]):not(:disabled)')].find(b => b.getClientRects().length)"
)
SHEETS = [
    ("Support (header)", SUPPORT, None),
    ("Dr. Liu", "document.querySelectorAll('#scientists button')[0]", None),
    ("Ask BiGH Science", "document.querySelectorAll('#scientists button')[1]", None),
    # The tabs' panel (phones, reduced motion) or, in the scroll story (round 7), the topic's own.
    ("explainer 1", "[...document.querySelectorAll('#science [role=tabpanel] button, #science [data-step=\"0\"] button')].pop()", 0),
    ("explainer 2", "[...document.querySelectorAll('#science [role=tabpanel] button, #science [data-step=\"1\"] button')].pop()", 1),
    ("explainer 3", "[...document.querySelectorAll('#science [role=tabpanel] button, #science [data-step=\"2\"] button')].pop()", 2),
    ("Support (footer)", "document.querySelector('footer button')", None),
]
MENU_BUTTON = "[data-nav-menu-button]"
SHEET = "[data-nav-sheet]"
ACTIVE = "(document.activeElement.getAttribute('aria-label') || document.activeElement.textContent || '').trim().slice(0, 28)"


def ring(page):
    """Is the focused control's ring the page's ink ring (2 px, solid, sumi ink)?"""
    return page.evaluate(
        f"(() => {{ const s = getComputedStyle(document.activeElement); return s.outlineStyle === 'solid' && parseFloat(s.outlineWidth) >= 2 && s.outlineColor === '{INK}'; }})()"
    )


def open_sheet(page, opener, topic=None, wait=1200):
    """Open a sheet the way a keyboard does: focus its button, press Enter."""
    if topic is not None and page.locator("#science [role=tab]").count():
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
    # Tab on: the language, Products, Science, the mark, About, Support and Log in (Sign up is a
    # placeholder, off).
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
        f"{tag}: the header's seven controls each show the ink focus ring",
        len(stops) == 7 and not pale,
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
        """[...document.querySelectorAll('#site-navigation a, #site-navigation button, #site-navigation select')]
          .filter(e => e.getClientRects().length && !e.closest('[data-nav-panel]'))
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
            """(() => { const n = document.querySelector('[data-nav-sheet]'); const b = n.getBoundingClientRect(); const s = getComputedStyle(n);
              const paper = [n, ...n.querySelectorAll('*'), ...document.querySelectorAll('header > span')]
                .some(e => getComputedStyle(e).backgroundImage.includes('paper'));
              const lines = [...new Set(n.querySelectorAll('[data-nav-sheet-toggle], [class*=sheetLink]'))].map(e => { const r = e.getBoundingClientRect();
                return [Math.round(r.left), Math.round(r.right), Math.round(r.height), parseFloat(getComputedStyle(e).fontSize), getComputedStyle(e).opacity]; });
              const rest = [...n.querySelectorAll('[class*=sheetFoot] a, [class*=sheetFoot] button, [class*=sheetFoot] select')]
                .filter(e => e.getClientRects().length).map(e => { const r = e.getBoundingClientRect();
                return [Math.round(r.left), Math.round(r.right), Math.round(r.height), parseFloat(getComputedStyle(e).fontSize), Math.round(r.bottom)]; });
              return { shown: document.querySelector('header').hasAttribute('data-menu') && s.display !== 'none', box: [Math.round(b.top), Math.round(b.bottom)], paper, links: lines, rest,
                locked: document.body.style.overflow, wide: document.documentElement.scrollWidth, win: [innerWidth, innerHeight],
                expanded: document.querySelector('[data-nav-menu-button]').getAttribute('aria-expanded') }; })()"""
        )
        shoot(page, f"opens-{'phone' if mobile else '820'}-00-menu")
        check(
            f"{tag}: the menu opens as a full sheet of the page's paper, the page locked under it",
            menu["shown"] and menu["expanded"] == "true" and menu["paper"] and menu["box"][1] >= size[1] - 1 and menu["locked"] == "hidden",
            f"box {menu['box']}, paper {menu['paper']}, body overflow {menu['locked']!r}",
        )
        every = menu["links"] + menu["rest"]
        check(
            f"{tag}: four menu lines (Products, Science, About, Support), each at least 48 px tall and 18 px type, every control inside the window",
            len(menu["links"]) == 4
            and all(l[2] >= 48 and l[3] >= 18 and l[4] == "1" for l in menu["links"])
            and all(r[2] >= 48 and r[3] >= 18 and r[4] <= size[1] for r in menu["rest"])
            and all(e[0] >= 0 and e[1] <= size[0] for e in every)
            and menu["wide"] <= size[0],
            f"links {menu['links']}, rest {menu['rest']}",
        )
        # From the menu's button Tab passes the bar's mark (and the language where the bar shows it)
        # and goes into the menu; every stop stays in the header.
        walk = []
        for _ in range(4):
            page.keyboard.press("Tab")
            page.wait_for_timeout(150)
            walk.append(page.evaluate(f"[!!document.activeElement.closest('header'), {ACTIVE}, !!document.activeElement.closest('{SHEET}')]"))
            if walk[-1][2]:
                break
        ringed = ring(page)
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
        shut = page.evaluate(f"[document.querySelector('{MENU_BUTTON}').getAttribute('aria-expanded'), {ACTIVE}, document.body.style.overflow]")
        check(
            f"{tag}: Tab goes from the menu's button into the menu; Escape closes it, focus back on the button",
            all(w[0] for w in walk) and walk[-1][2] and ringed and shut == ["false", "Open menu", ""],
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
    page.wait_for_timeout(60)
    still = page.evaluate(
        """(() => { const n = document.querySelector('[data-nav-sheet]');
          const running = document.getAnimations().filter(a => a.playState === 'running' && n.contains(a.effect?.target)).length;
          const lines = [...n.querySelectorAll('[data-nav-sheet-toggle], [class*=sheetLink]')].map(e => getComputedStyle(e).opacity);
          return { shown: getComputedStyle(n).display !== 'none' && document.querySelector('header').hasAttribute('data-menu'),
            running, lines }; })()"""
    )
    check(
        f"{tag}: the menu is whole at once",
        still["shown"] and still["running"] == 0 and all(o == "1" for o in still["lines"]),
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
        "[...new Set(document.querySelectorAll('[data-nav-sheet] [data-nav-sheet-toggle], [data-nav-sheet] [class*=sheetLink]'))].map(e => { const r = e.getBoundingClientRect(); return [e.textContent.trim(), Math.round(r.right), Math.round(r.height)]; })"
    )
    shoot(page, "opens-kr-phone-00-menu")
    page.evaluate(f"{SUPPORT}.click()")
    page.wait_for_timeout(1300)
    sheet = page.evaluate(
        """(() => { const d = document.querySelector('dialog'); const b = d.getBoundingClientRect();
          return [d.open, d.querySelector('h2').textContent.trim(), Math.round(b.left), Math.round(b.right), d.scrollWidth <= d.clientWidth, document.documentElement.scrollWidth, d.querySelectorAll('details').length]; })()"""
    )
    shoot(page, "opens-kr-phone-01-sheet")
    check(
        f"{tag}: the menu and the Support sheet open in Korean, inside the window",
        len(links) == 4
        and all(l[1] <= 390 and l[2] >= 48 for l in links)
        and "고객" in links[3][0]
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
    # Round 4: the brush line keeps to the gaps beside the two big paintings: never over the cell's
    # body or its words, never over the still life's objects, the sample's words or the names and
    # arrows (the whole line is drawn from the first frame here).
    page.evaluate("document.querySelector('#cellular [data-brush=cellular-mito]').scrollIntoView({block: 'center'})")
    page.wait_for_timeout(900)
    g = page.evaluate(PAINTINGS)
    cl, ct, cr, cb = g["cell"]
    cw, chh = cr - cl, cb - ct
    wl, wt, wr, wb = g["cellWords"]
    words = ink_in_box(page, wl - 4, wt, wr + 4, wb)
    body = ink_in_box(page, cl + 0.2 * cw, ct + 0.12 * chh, min(cr, g["win"]), ct + 0.9 * chh)
    gap = ink_in_box(page, wr + 4, g["cellLines"][1], cl + 0.15 * cw, g["cellLines"][3])
    check(
        f"{tag}: the brush line runs down between the cell and its words, over neither",
        words == 0 and body == 0 and gap > 100,
        f"over the words {words}, over the cell {body}, in the gap {gap}",
    )
    page.evaluate("document.querySelector('#stories [data-brush=story-painting]').scrollIntoView({block: 'center'})")
    page.wait_for_timeout(900)
    g = page.evaluate(PAINTINGS)
    sl, st, sr, sb = g["still"]
    sw, sh = sr - sl, sb - st
    wl, wt, wr, wb = g["storyWords"]
    subject = ink_in_box(page, max(0, sl), st + 0.1 * sh, sl + 0.8 * sw, sb - 0.06 * sh)
    words = ink_in_box(page, wl, wt, wr + 4, wb)
    gap = ink_in_box(page, sr, st + 0.2 * sh, wl, st + 0.8 * sh)
    names = ink_in_box(page, *g["choices"])
    arrows = ink_in_box(page, g["arrowsBox"][0] - 4, g["arrowsBox"][1] - 4, g["arrows"][2] + 4, g["arrows"][3] + 4)
    check(
        f"{tag}: the brush line runs down between the still life and its words, over neither, nor the names or arrows",
        subject == 0 and words == 0 and names == 0 and arrows == 0 and gap > 100,
        f"over the still life {subject}, the words {words}, the names {names}, the arrows {arrows}; in the gap {gap}",
    )
    # Round 7: with reduced motion the science keeps its three tabs (no tall scroll, nothing
    # pinned), and the brush line still passes down the far side of its painting, over none of it.
    page.evaluate("document.querySelector('#science figure').scrollIntoView({block: 'center'})")
    page.wait_for_timeout(900)
    k = page.evaluate(TABBED)
    st = page.evaluate(STORY_STATE)
    fl, ft, fr, fb = st["stage"]
    over = ink_in_box(page, fl + 0.06 * (fr - fl), ft + 0.08 * (fb - ft), fr - 0.03 * (fr - fl), fb)
    side = ink_in_box(page, st["copy"][2], ft, st["fig"][0], fb)
    check(
        f"{tag}: the science keeps its three tabs; the brush line passes beside its painting (in the gap), not over it",
        k["story"] == "false" and k["tabs"] == 3 and k["sticky"] != "sticky" and k["height"] < 1.6 * 900
        and over == 0 and side > 150,
        f"{k}; over the painting {over}, beside it {side}",
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


PAUSE = """(() => {
  const r = (e) => { const b = e.getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; };
  const ask = document.querySelector('#scientists [data-brush=ask]');
  const img = ask.querySelector('img'), h = ask.querySelector('h3'), p = ask.querySelector('p'), btn = ask.querySelector('button');
  const cs = getComputedStyle(ask), box = r(ask);
  const mid = (box[0] + parseFloat(cs.paddingLeft) + box[2] - parseFloat(cs.paddingRight)) / 2;
  const rows = new Map(); const walker = document.createTreeWalker(h, NodeFilter.SHOW_TEXT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) { const re = /\\S+/g; let m;
    while ((m = re.exec(n.nodeValue))) { const rg = document.createRange(); rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length);
      const k = Math.round(rg.getBoundingClientRect().top / 6); rows.set(k, (rows.get(k) || 0) + 1); } }
  return { win: innerWidth, mid, img: r(img), title: r(h), text: r(p), button: r(btn),
    rows: [...rows.entries()].sort((a, b) => a[0] - b[0]).map((x) => x[1]),
    work: r(document.querySelector('#scientists [data-brush=work-main]')),
    products: r(document.querySelector('#products h2')),
    arrows: r([...document.querySelectorAll('#stories button[aria-label]')].pop()),
    science: r(document.querySelector('#science h2')) };
})()"""


def run_pause(browser):
    """Round 6: Ask BiGH Science is the page's one centred pause, on open paper; the brush line
    passes it in the margin; the phone has no empty band before the science; on a short laptop
    window the last screen shows the whole crane at rest and the whole promise, clear of the
    header."""
    for size, mobile in (((1536, 1000), False), ((1440, 900), False), ((390, 844), True)):
        tag = f"pause {size[0]}"
        context, page, response, problems = open_page(browser, f"{BASE}/", size, mobile, reduced=not mobile)
        page.evaluate("document.querySelector('#scientists [data-brush=ask]').scrollIntoView({block: 'center'})")
        page.wait_for_timeout(900)
        g = page.evaluate(PAUSE)
        off = [abs((b[0] + b[2]) / 2 - g["mid"]) for b in (g["img"], g["title"], g["text"], g["button"])]
        width = g["img"][2] - g["img"][0]
        modest = 0.66 * g["win"] <= width <= 0.74 * g["win"] if mobile else 300 <= width <= 410
        check(
            f"{tag}: the painting, headline, words and button are centred, the painting modest",
            max(off) <= 2 and modest and g["img"][3] <= g["title"][1] + 24 and g["title"][3] <= g["text"][1],
            f"off centre {max(off):.1f} px, painting {width:.0f} px",
        )
        check(
            f"{tag}: the pause's headline sets on two lines, no word alone on one",
            len(g["rows"]) == 2 and min(g["rows"]) >= 2,
            f"words per line {g['rows']}",
        )
        above = g["img"][1] - g["work"][3]
        below = g["products"][1] - g["button"][3]
        room = (64, 160) if mobile else (120, 260)
        check(
            f"{tag}: open paper above and below the pause",
            room[0] <= above <= room[1] and room[0] <= below <= room[1] + 40,
            f"above {above:.0f}, below {below:.0f} px",
        )
        if mobile:
            page.evaluate("document.querySelector('#science h2').scrollIntoView({block: 'center'})")
            page.wait_for_timeout(500)
            g = page.evaluate(PAUSE)
            band = g["science"][1] - g["arrows"][3]
            check(f"{tag}: no empty band between the story arrows and the science", band <= 110, f"{band:.0f} px")
        else:
            pad = 10
            over = sum(
                ink_in_box(page, b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad)
                for b in (g["img"], g["title"], g["text"], g["button"])
            )
            left = min(g["img"][0], g["title"][0], g["text"][0]) - pad
            beside = ink_in_box(page, 0, g["img"][1], left, g["button"][3])
            right = ink_in_box(page, max(g["title"][2], g["img"][2]) + pad, g["img"][1], g["win"], g["button"][3])
            check(
                f"{tag}: the brush line passes the pause in the left margin, over none of it",
                over == 0 and beside > 200 and right == 0,
                f"over it {over}, beside it {beside}, at its right {right}",
            )
        shoot(page, f"pause-{size[0]}")
        check(f"{tag}: no errors", not problems, "; ".join(problems[:3]))
        context.close()

    # Round 10: also the shorter windows (1280x720 cut the crane's head by 22 px, 1536x864 by 20).
    # Menu bar round 1 (October 5): the solid bar hid half of "Stay sharp." at 1366x657 (the window
    # of a 1366x768 laptop), so the promise's top must clear the bar too, at 1366x657 and 1440x700.
    for size in ((1280, 800), (1440, 900), (1536, 1000), (1280, 720), (1536, 864), (1366, 657), (1440, 700)):
        tag = f"last screen {size[0]}x{size[1]}"
        context, page, response, problems = open_page(browser, f"{BASE}/", size, False, reduced=True)
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
        shoot(page, f"last-{size[0]}x{size[1]}")
        context.close()


# Round 10: the products' arrival. The stage's and the picker's state, the shown bottle, the
# layer it rises in, its pool and the picker's five bottles.
ARRIVE = """(() => {
  const s = document.querySelector('#products [data-brush=stage]');
  const row = document.querySelector('#products [data-brush=bottles]');
  const big = s.querySelector('img[data-shown=true]');
  const lift = big.parentElement;
  const pool = s.querySelector('a > img');
  const minis = [...row.querySelectorAll('button > span:first-child')];
  const cs = (e) => getComputedStyle(e);
  return {
    stage: s.dataset.arrive || '', row: row.dataset.arrive || '',
    top: big.getBoundingClientRect().top + scrollY, bigOpacity: +cs(big).opacity,
    lift: cs(lift).translate, liftAnim: cs(lift).animationName, liftOpacity: +cs(lift).opacity,
    pool: +(+cs(pool).opacity).toFixed(3), poolAnim: cs(pool).animationName,
    poolRunning: pool.getAnimations().some((a) => a.playState === 'running'),
    minis: minis.map((m) => +(+cs(m).opacity).toFixed(3)),
    delays: minis.map((m) => cs(m).animationDelay),
  };
})()"""

# Round 10: the stories' still lifes (opacity, animations, mask, bloom size, blur) and the quote.
STILLS = """(() => [...document.querySelectorAll('#stories figure img')].map((e) => {
  const c = getComputedStyle(e);
  return { on: e.dataset.on, opacity: +(+c.opacity).toFixed(3), anim: c.animationName,
    mask: c.maskImage || c.webkitMaskImage || '', bloom: c.getPropertyValue('--bloom').trim(),
    filter: c.filter, settle: getComputedStyle(document.querySelector('#stories article')).animationName };
}))()"""


def run_arrivals(browser):
    """Round 10 (October 5), authored arrivals. The products: as the stage comes into view the
    big bottle rises 10 px onto its ground while its pool gathers (one breath), and the picker's
    five bottles follow 70 ms apart; out of view they wait visibly (never invisible), a page
    opened with the stage in view does not wait, choosing another product keeps the cross-fade
    and the pool gathering without a rise, and reduced motion marks nothing. The stories:
    changing the story blooms the new still life through the ink mask over its own edges while
    the last one dissolves (names and arrows); reduced motion swaps at once. At 900 px the brush
    line keeps clear of the story names."""
    tag = "arrival 1536"
    context, page, response, problems = open_page(browser, f"{BASE}/", (1536, 1000), False)
    a0 = page.evaluate(ARRIVE)
    check(
        f"{tag}: out of view the stage and the picker wait, visibly (the bottle whole, the picker in a paler ink)",
        a0["stage"] == "waiting" and a0["row"] == "waiting" and a0["bigOpacity"] == 1 and a0["liftOpacity"] == 1
        and a0["lift"] == "0px 10px" and a0["pool"] <= 0.55 and all(0.35 <= m <= 0.45 for m in a0["minis"]),
        f"{a0['stage']}/{a0['row']}, bottle {a0['bigOpacity']}, lift {a0['lift']}, pool {a0['pool']}, minis {a0['minis']}",
    )
    stage_top = top_of(page, "#products [data-brush=stage]")
    walk_to(page, stage_top - 380, 0)
    a1 = page.evaluate(ARRIVE)
    page.wait_for_timeout(450)
    a2 = page.evaluate(ARRIVE)
    page.wait_for_timeout(3000)
    a3 = page.evaluate(ARRIVE)
    rise = a0["top"] - a3["top"]
    check(
        f"{tag}: as the stage comes into view the bottle rises 10 px onto its ground while its pool gathers, in one breath",
        a1["stage"] == "in" and a1["liftAnim"] != "none" and 0.5 < a2["pool"] < 0.9 and a3["stage"] == "done"
        and abs(rise - 10) <= 1.5 and a3["lift"] in ("none", "0px") and a3["pool"] >= 0.9,
        f"{a1['stage']} -> {a3['stage']}, rose {rise:.1f} px, pool {a0['pool']} -> {a2['pool']} -> {a3['pool']}",
    )
    row_top = top_of(page, "#products [data-brush=bottles]")
    walk_to(page, row_top - 520, 0)
    page.wait_for_timeout(200)
    b1 = page.evaluate(ARRIVE)
    page.wait_for_timeout(3400)
    b2 = page.evaluate(ARRIVE)
    stagger = [round(float(d[:-1]) * (1000 if d.endswith("s") and not d.endswith("ms") else 1)) for d in b1["delays"]]
    check(
        f"{tag}: the picker's five bottles follow, 70 ms apart, and come to rest whole",
        b1["row"] == "in" and stagger == [120, 190, 260, 330, 400] and b1["minis"] == sorted(b1["minis"], reverse=True)
        and b1["minis"][0] > b1["minis"][4] and b2["row"] == "done" and all(m == 1 for m in b2["minis"]),
        f"delays {stagger}, opacity at 200 ms {b1['minis']}, at rest {b2['minis']}",
    )
    page.locator("#products button[aria-pressed]", has_text="Turmerific").click()
    page.wait_for_timeout(120)
    c1 = page.evaluate(ARRIVE)
    page.wait_for_timeout(1200)
    c2 = page.evaluate(ARRIVE)
    check(
        f"{tag}: choosing another product keeps the cross-fade and the pool gathering, without a rise",
        0 < c1["bigOpacity"] < 1 and c1["liftAnim"] == "none" and c1["lift"] in ("none", "0px") and c1["poolRunning"]
        and c2["bigOpacity"] == 1 and abs(c2["top"] - a3["top"]) <= 0.5,
        f"bottle at 120 ms {c1['bigOpacity']:.2f}, lift {c1['lift']} {c1['liftAnim']}, pool gathering {c1['poolRunning']}, moved {c2['top'] - a3['top']:.1f} px",
    )
    check(f"{tag}: no errors", not problems, "; ".join(problems[:3]))
    context.close()

    # A page opened at the products (#products: the jump comes after the page wakes, so the stage
    # may arrive as the window lands on it) is never left waiting.
    context, page, response, problems = open_page(browser, f"{BASE}/#products", (1536, 1000), False)
    d = page.evaluate(ARRIVE)
    check(
        "arrival 1536: opened at the products, nothing is left waiting",
        d["stage"] in ("", "done") and d["lift"] in ("none", "0px")
        and d["bigOpacity"] == 1 and d["pool"] >= 0.9,
        f"stage '{d['stage']}', picker '{d['row']}', lift {d['lift']}, pool {d['pool']}",
    )
    context.close()

    # Reduced motion: nothing is marked, nothing moves.
    context, page, response, problems = open_page(browser, f"{BASE}/", (1536, 1000), False, reduced=True)
    r0 = page.evaluate(ARRIVE)
    walk_to(page, top_of(page, "#products [data-brush=bottles]") - 600, 100)
    r1 = page.evaluate(ARRIVE)
    check(
        "arrival reduced motion: the products are simply there (no waiting, no rise, no stagger)",
        r0["stage"] == r0["row"] == r1["stage"] == r1["row"] == "" and r1["lift"] in ("none", "0px")
        and all(m == 1 for m in r0["minis"] + r1["minis"]) and abs(r0["top"] - r1["top"]) <= 0.5,
        f"{r0['stage']}/{r0['row']} -> {r1['stage']}/{r1['row']}, minis {r1['minis']}",
    )
    # ...and a story swaps at once.
    page.evaluate("document.querySelector('#stories figure').scrollIntoView({block: 'center'})")
    page.wait_for_timeout(500)
    page.locator("#stories button[aria-pressed]", has_text="Michael R.").click()
    page.wait_for_timeout(80)
    s = page.evaluate(STILLS)
    check(
        "stories reduced motion: changing the story swaps the still life at once",
        s[1]["opacity"] == 1 and s[0]["opacity"] == 0 and s[1]["anim"] == "none" and s[1]["settle"] == "none",
        f"opacities {[x['opacity'] for x in s]}, animation {s[1]['anim']}",
    )
    context.close()

    # The stories: the new still life blooms through the ink blot.
    tag = "stories 1536"
    context, page, response, problems = open_page(browser, f"{BASE}/", (1536, 1000), False)
    page.evaluate("document.querySelector('#stories figure').scrollIntoView({block: 'center'})")
    page.wait_for_timeout(4200)
    s0 = page.evaluate(STILLS)
    page.locator("#stories button[aria-pressed]", has_text="Michael R.").click()
    page.wait_for_timeout(300)
    s1 = page.evaluate(STILLS)
    page.wait_for_timeout(3600)
    s2 = page.evaluate(STILLS)
    shoot(page, "stories-bloomed")
    mid = s1[1]
    size = float(mid["bloom"].rstrip("%") or 0)
    check(
        f"{tag}: changing the story blooms the new still life through the ink mask over its own edges; the last one dissolves",
        s0[0]["anim"] == "none"
        and "unfold" in mid["anim"] and "sharpen" in mid["anim"] and mid["opacity"] == 1
        and "bloom-mask" in mid["mask"] and mid["mask"].count("linear-gradient") == 2 and 2 < size < 278
        and 0 < s1[0]["opacity"] < 1 and "settle" in mid["settle"]
        and s2[1]["bloom"] == "280%" and s2[0]["opacity"] == 0 and s2[1]["opacity"] == 1,
        f"first still {s0[0]['anim']}; at 300 ms bloom {mid['bloom']}, {mid['anim']}, last one {s1[0]['opacity']}; then {s2[1]['bloom']}, last {s2[0]['opacity']}",
    )
    page.click("#stories button[aria-label='Next sample story']")
    page.wait_for_timeout(300)
    s3 = page.evaluate(STILLS)
    check(
        f"{tag}: the arrows bloom the next still life the same way",
        s3[2]["on"] == "true" and "unfold" in s3[2]["anim"] and 2 < float(s3[2]["bloom"].rstrip("%") or 0) < 278,
        f"third still {s3[2]['on']} {s3[2]['anim']} at {s3[2]['bloom']}",
    )
    check(f"{tag}: no errors", not problems, "; ".join(problems[:3]))
    context.close()

    # At 900 px the brush line keeps clear of the story names (round 10: it touched "Susan L.").
    tag = "stories 900"
    context, page, response, problems = open_page(browser, f"{BASE}/", (900, 1000), False)
    total = page.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < total:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(40)
        y += 200
    page.evaluate("document.querySelector('[data-brush=story-choices]').scrollIntoView({block: 'center'})")
    page.wait_for_timeout(900)
    boxes = page.evaluate(
        "[...document.querySelectorAll('[data-brush=story-choices] button')].map(b => { const r = b.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; })"
    )
    hits = [ink_in_box(page, l - 8, t - 8, r + 8, b + 8) for l, t, r, b in boxes]
    passing = ink_in_box(page, boxes[-1][2] + 8, boxes[-1][1], boxes[-1][2] + 140, boxes[-1][3])
    check(
        f"{tag}: the brush line passes the story names clear of them (8 px or more)",
        not any(hits) and passing > 50,
        f"ink on the names {hits}, beside the last {passing}",
    )
    shoot(page, "stories-900-names")
    context.close()


ONLY = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--only=")), None)

with sync_playwright() as p:
    browser = p.chromium.launch(args=GPU)
    if ONLY == "line":
        run_line(browser)
        browser.close()
        passed = sum(1 for r in results if r[1])
        print(f"\n{passed}/{len(results)} checks passed.")
        sys.exit(0 if passed == len(results) else 1)
    run(browser, "home", mobile=False)
    run(browser, "home", mobile=True)
    run_short(browser, "home")
    run_sizes(browser, "home")
    run_reduced(browser, "home")
    run_story(browser)
    run_opens(browser)
    run_korean(browser, mobile=False)
    run_korean(browser, mobile=True)
    run_vietnamese(browser, mobile=False)
    run_vietnamese(browser, mobile=True)
    run_research(browser)
    run_type(browser, mobile=False)
    run_type(browser, mobile=True)
    run_pause(browser)
    run_arrivals(browser)
    run_line(browser)
    browser.close()

passed = sum(1 for r in results if r[1])
print(f"\n{passed}/{len(results)} checks passed. Pictures: {OUT}")
sys.exit(0 if passed == len(results) else 1)
