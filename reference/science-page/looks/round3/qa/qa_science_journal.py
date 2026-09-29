"""QA for the Science page, round 3, look C "Journal" (/science?look=journal).

Checks the whole page between the shared header and footer: the cover (headline split into lines,
plate wiped open), Dr. Liu's feature (portrait focus-in, story panel), inline citations (preview on
hover, link to the numbered references), the pinned sideways chronology on wide screens, the five
formulas with their credits, the three references and "See all 36", further reading, the letters
page, no sideways scroll, no errors, no words cut off, nothing stuck invisible, and a calm
reduced-motion version. Screenshots go to scripts/qa/out/science-journal/, including mid-animation
frames of the cover and the chronology.

python -X utf8 scripts/qa/qa_science_journal.py http://localhost:3008 [locale]
"""
import os
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3008"
LOCALE = sys.argv[2] if len(sys.argv) > 2 else ""
URL = f"{BASE}{'/' + LOCALE if LOCALE else ''}/science?look=journal"
SHOTS = os.path.join(os.path.dirname(__file__), "out", "science-journal")
os.makedirs(SHOTS, exist_ok=True)
GPU = ["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"]
passed = failed = 0


def check(name, ok, detail=""):
    global passed, failed
    passed += bool(ok)
    failed += not ok
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


def open_page(browser, w, h, reduced=False, wait="networkidle"):
    ctx = browser.new_context(
        viewport={"width": w, "height": h},
        reduced_motion="reduce" if reduced else "no-preference",
        device_scale_factor=1,
    )
    page = ctx.new_page()
    problems = []
    page.on("pageerror", lambda e: problems.append(f"pageerror {e}"))
    page.on("console", lambda m: problems.append(f"console {m.text[:160]}") if m.type == "error" else None)
    page.on("response", lambda r: problems.append(f"{r.status} {r.url[-60:]}") if r.status >= 400 and "favicon" not in r.url else None)
    page.goto(URL, wait_until=wait)
    return ctx, page, problems


def walk(page, y, steps=10):
    current = page.evaluate("scrollY")
    for s in range(1, steps + 1):
        page.evaluate(f"window.scrollTo(0, {current + (y - current) * s / steps})")
        page.wait_for_timeout(35)


def top_of(page, selector):
    return page.evaluate(f"(() => {{ const e = document.querySelector('{selector}'); return e ? e.getBoundingClientRect().top + scrollY : -1; }})()")


CLIPPED = """(() => {
  // Words cut off at the side of the screen. The sideways chronology track is exempt.
  const out = [];
  for (const el of document.querySelectorAll('main h1, main h2, main h3, main p, main button, main a, main td, main th')) {
    if (el.closest('[data-chron-track]') || el.closest('[aria-hidden="true"]')) continue;
    const r = el.getBoundingClientRect();
    if (!r.width || r.bottom < 0 || r.top > innerHeight) continue;
    const style = getComputedStyle(el);
    if (style.visibility === 'hidden' || +style.opacity === 0) continue;
    if (r.left < -1 || r.right > innerWidth + 1) out.push(el.textContent.trim().slice(0, 40));
  }
  return out;
})()"""

# Anything a reader should see that is still (nearly) invisible after the whole page was walked.
STUCK = """(() => [...document.querySelectorAll('main h1, main h2, main h3, main p, main td, main th, main img, main a')]
  .filter(e => {
    const r = e.getBoundingClientRect();
    if (!r.width || !r.height || e.closest('dialog') || e.closest('[aria-hidden="true"]')) return false;
    let n = e;
    while (n && n !== document.body) { if (+getComputedStyle(n).opacity < 0.5) return true; n = n.parentElement; }
    return false;
  })
  .map(e => (e.textContent || e.getAttribute('alt') || e.tagName).trim().slice(0, 36)))()"""

clipped_seen = []


def shoot(page, name, clip=True):
    page.screenshot(path=os.path.join(SHOTS, name + ".png"))
    if clip:
        clipped_seen.extend(f"{name}: {text}" for text in page.evaluate(CLIPPED))


def overflow(page):
    return page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")


COMMON = """(() => {
  const main = document.querySelector('main');
  const first = main.querySelector('section');
  const img = (s) => { const e = document.querySelector(s); return e ? e.naturalWidth : 0; };
  return {
    h1: document.querySelector('h1')?.textContent.trim(),
    firstId: first?.id,
    cover: img('[data-cover-image]'),
    photo: img('[data-portrait-image]'),
    sections: ['#scientists', '#chronology', '#formulations', '#research', '#health', '#ask'].map(s => !!document.querySelector(s)),
    stops: document.querySelectorAll('[data-stop]').length,
    formulas: document.querySelectorAll('#formulations tbody tr').length,
    credits: [...document.querySelectorAll('#formulations tbody td:last-child')].map(e => e.textContent.trim()),
    refs: document.querySelectorAll('#research li[id^=ref-]').length,
    rows: document.querySelectorAll('#research details').length,
    cites: document.querySelectorAll('main sup a[href^="#ref-"]').length,
    doors: document.querySelectorAll('#health article').length,
    letters: document.querySelectorAll('#ask article').length,
    forms: document.querySelectorAll('#ask form, #ask input, #ask textarea').length,
  };
})()"""

CREDITS = [
    "Formulated by Dr. Jiankang Liu.",
    "Developed by Dr. Jiankang Liu and Dr. Iris Wang.",
    "Developed under the direction and guidance of Dr. Jiankang Liu and Dr. Iris Wang.",
    "Developed under the direction and guidance of Dr. Jiankang Liu and Dr. Iris Wang.",
    "Developed under the direction and guidance of Dr. Jiankang Liu and Dr. Iris Wang.",
]

with sync_playwright() as p:
    browser = p.chromium.launch(args=GPU)
    for label, (w, h) in {"desk": (1440, 900), "laptop": (1280, 720), "phone": (390, 844)}.items():
        tag = f"{label}{'-' + LOCALE if LOCALE else ''}"
        wide = w > 900

        # The cover's moving moment, frame by frame (fresh load, before networkidle).
        ctx, page, problems = open_page(browser, w, h, wait="domcontentloaded")
        for t, name in ((350, "a"), (650, "b"), (700, "c"), (900, "d")):
            page.wait_for_timeout(t)
            shoot(page, f"{tag}-cover-{name}", clip=False)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2600)
        info = page.evaluate(COMMON)
        split = page.evaluate("document.querySelectorAll('[data-cover-title] [class*=line], [data-cover-title] div div').length")
        clip = page.evaluate("getComputedStyle(document.querySelector('[data-cover-plate]')).clipPath")
        check(f"{tag}: cover, portrait and every part render; #scientists first",
              bool(info["h1"]) and info["firstId"] == "scientists" and info["cover"] > 0 and info["photo"] > 0
              and all(info["sections"]) and info["stops"] == 5 and info["doors"] == 3 and info["letters"] == 3
              and info["forms"] == 0, str({k: info[k] for k in ("firstId", "cover", "photo", "sections", "stops", "doors", "letters", "forms")}))
        check(f"{tag}: five formulas with their credits exactly as approved",
              info["formulas"] == 5 and info["credits"] == CREDITS, str(info["credits"]))
        check(f"{tag}: three references, three inline citations, list closed",
              info["refs"] == 3 and info["cites"] >= 4 and info["rows"] == 0, f"refs={info['refs']} cites={info['cites']} rows={info['rows']}")
        check(f"{tag}: headline split into masked lines and the plate fully open",
              split >= 2 and clip in ("none", "inset(0%)", "inset(0% 0% 0% 0%)", "inset(0px)"), f"lines={split} clip={clip}")
        shoot(page, f"{tag}-00")

        # Inline citation: a preview on hover (mouse screens), and the link lands on its reference.
        if wide:
            page.evaluate("document.querySelector('#dr-liu').scrollIntoView({block: 'center'})")
            page.wait_for_timeout(1600)
            cite = page.locator('main sup a[href="#ref-1"]').first
            cite.hover()
            page.wait_for_timeout(400)
            tip = page.evaluate("(() => { const t = document.querySelector('[role=tooltip]'); if (!t) return null; const r = t.getBoundingClientRect(); return { text: t.textContent.slice(0, 60), left: r.left, right: r.right, top: r.top }; })()")
            if label == "desk":
                shoot(page, f"{tag}-cite-preview", clip=False)
            check(f"{tag}: citation preview shows its study, inside the screen",
                  bool(tip) and "PNAS" in tip["text"] and tip["left"] >= 0 and tip["right"] <= w and tip["top"] >= 0, str(tip))
            cite.click()
            page.wait_for_timeout(1800)
            landed = page.evaluate("(() => { const r = document.querySelector('#ref-1').getBoundingClientRect(); return { top: Math.round(r.top), bottom: Math.round(r.bottom) }; })()")
            check(f"{tag}: citation link lands on reference 1", 0 <= landed["top"] < h * 0.7, str(landed))
            if label == "desk":
                page.wait_for_timeout(150)
                shoot(page, f"{tag}-cite-landed", clip=False)

        # "See all 36 sources" opens the full list and closes again.
        page.evaluate("document.querySelector('#research').scrollIntoView()")
        page.wait_for_timeout(600)
        more = page.locator("#research button[aria-expanded]").first
        more.click()
        page.wait_for_timeout(500)
        opened = page.evaluate("document.querySelectorAll('#research details').length")
        if label == "desk":
            page.evaluate("document.querySelector('#research details').scrollIntoView({block: 'center'})")
            page.wait_for_timeout(500)
            shoot(page, f"{tag}-all-sources")
        more.scroll_into_view_if_needed()
        more.click()
        page.wait_for_timeout(400)
        shut = page.evaluate("document.querySelectorAll('#research details').length")
        check(f"{tag}: 'See all' opens all 36 sources and closes", opened == 36 and shut == 0, f"open={opened} closed={shut}")

        # "Read his story" opens the story panel; its close button shuts it.
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(500)
        button = page.get_by_role("button", name="Read his story").first
        button.scroll_into_view_if_needed()
        page.wait_for_timeout(700)
        button.click()
        page.wait_for_timeout(600)
        story = page.evaluate("(() => { const d = document.querySelector('dialog'); return d.open && !!d.querySelector('img') && d.querySelectorAll('p').length >= 4; })()")
        if label == "desk":
            shoot(page, f"{tag}-story", clip=False)
        page.locator("dialog button").first.click()
        page.wait_for_timeout(400)
        closed = page.evaluate("!document.querySelector('dialog').open")
        check(f"{tag}: 'Read his story' opens and closes", story and closed, f"opened={story} closed={closed}")

        # The chronology: pinned and sliding sideways on wide screens; top to bottom on phones.
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(400)
        start = top_of(page, "[data-chron]")
        if wide:
            walk(page, start, 14)
            page.wait_for_timeout(900)
            span = page.evaluate("(() => { const t = document.querySelector('[data-chron-track]'); return t.scrollWidth - innerWidth; })()")
            frames = []
            for i, f in enumerate((0.0, 0.3, 0.62, 1.0)):
                walk(page, start + span * f, 10)
                page.wait_for_timeout(1300)
                state = page.evaluate("""(() => {
                  const s = document.querySelector('[data-chron]').getBoundingClientRect();
                  const m = new DOMMatrix(getComputedStyle(document.querySelector('[data-chron-track]')).transform);
                  return { top: Math.round(s.top), x: Math.round(m.m41), lit: document.querySelectorAll('[data-stop][data-lit]').length };
                })()""")
                frames.append(state)
                shoot(page, f"{tag}-chron-{i}", clip=False)
            pinned = all(abs(f["top"]) <= 2 for f in frames)
            moves = frames[0]["x"] > frames[1]["x"] > frames[2]["x"] > frames[3]["x"]
            lights = frames[0]["lit"] <= frames[1]["lit"] <= frames[2]["lit"] <= frames[3]["lit"] and frames[3]["lit"] == 5
            check(f"{tag}: chronology pins, slides sideways, lights every year", pinned and moves and lights, str(frames))
            # Every stop's words fit on the pinned screen.
            fit = page.evaluate("""[...document.querySelectorAll('[data-stop]')].map(s => {
              const r = s.getBoundingClientRect(); return Math.round(r.bottom); }).every(b => b <= innerHeight - 8)""")
            check(f"{tag}: chronology words fit the pinned screen", fit)
        else:
            pin = page.evaluate("!!document.querySelector('[data-chron]').closest('.pin-spacer')")
            check(f"{tag}: no sideways pin on phones", not pin)

        # Step through the whole page one screen at a time (pictures + cut-off words).
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(600)
        end = page.evaluate("document.documentElement.scrollHeight") - h
        y, n = 0, 1
        while y < end and n < 70:
            y = min(end, y + h * 0.85)
            walk(page, y)
            page.wait_for_timeout(900)
            shoot(page, f"{tag}-{n:02d}")
            n += 1
        ov = overflow(page)
        check(f"{tag}: no sideways scroll, no errors", ov == 0 and not problems, f"overflow={ov} {problems[:3]}")
        mine = [c for c in clipped_seen if c.startswith(tag + "-")]
        check(f"{tag}: no words cut off at the screen edge", not mine, "; ".join(mine[:4]))
        stuck = page.evaluate(STUCK)
        check(f"{tag}: nothing left invisible after scrolling through", not stuck, str(stuck[:5]))
        ctx.close()

    # Reduced motion: everything readable at once, no pin, no hidden cover.
    for label, (w, h) in {"reduced-desk": (1440, 900), "reduced-phone": (390, 844)}.items():
        ctx, page, problems = open_page(browser, w, h, reduced=True)
        page.wait_for_timeout(900)
        shoot(page, f"{label}-00")
        hidden = page.evaluate("""[...document.querySelectorAll('main h1, main h2, main h3, main p, main img')]
          .filter(e => { let n = e; while (n && n !== document.body) { if (+getComputedStyle(n).opacity < 0.5) return true; n = n.parentElement; } return false; })
          .map(e => (e.textContent || e.tagName).trim().slice(0, 30))""")
        pin = page.evaluate("!!document.querySelector('.pin-spacer')")
        clip = page.evaluate("getComputedStyle(document.querySelector('[data-cover-plate]')).clipPath")
        check(f"{label}: every line and picture visible at once, no pin, plate open",
              not hidden and not pin and clip == "none" and not problems, f"{hidden[:4]} pin={pin} clip={clip} {problems[:2]}")
        start = top_of(page, "[data-chron]")
        page.evaluate(f"window.scrollTo(0, {start})")
        page.wait_for_timeout(500)
        shoot(page, f"{label}-chron")
        ov = overflow(page)
        check(f"{label}: no sideways scroll", ov == 0, f"overflow={ov}")
        ctx.close()
    browser.close()

print()
print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
