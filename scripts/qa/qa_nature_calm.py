"""QA for the Nature Calm product page (/products/nature-calm), September 28, 2026.

Checks at 1440x900 and 390x844 with motion, then 1440x900 with reduced motion:
- the page and its route in every language answer 200; the title names Nature Calm
- the chapters, in order: overview, why, inside, research, people, daily, buy
- facts against the 2019 label, typed in again here (a second transcription, so a typo in
  nature-calm.ts shows up): 18 ingredients, each amount and unit in the full-label table,
  six shown first, all 18 after "Show all"; 90 capsules, 3 a day, 30 days
- the credit "Developed by Dr. Jiankang Liu and Dr. Iris Wang." and both people, Dr. Wang
  without a photograph
- seven studies, oldest first, each link opening a new tab with rel="noopener", under Nature Calm's
  own heading ("The research behind the formula")
- the "why" chapter shows the microscope pictures, off and on (qa_nature_calm_why.py checks the
  chapter itself)
- honesty: no "rat"/"rats", no "sleep", no "clinically proven" anywhere in the page text
- phones: the giant name keeps its word space and stands centred ("Nature Calm", not "NatureCalm")
- no horizontal page scroll at any step; no console errors or page errors
- the homepage links to /products/nature-calm

Pictures: scripts/qa/out/nc-<run>-<chapter>-<nn>.png (viewport shots while scrolling through each
chapter; full-page shots break svh layouts) and nc-<run>-<chapter>-sheet.png per chapter.

    python -X utf8 scripts/qa/qa_nature_calm.py http://localhost:3013
"""
import os
import re
import sys
import time

from PIL import Image
from playwright.sync_api import sync_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3013").rstrip("/")
URL = f"{BASE}/products/nature-calm"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
ARGS = ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
CHAPTERS = ["overview", "why", "inside", "research", "people", "daily", "buy"]
CREDIT = "Developed by Dr. Jiankang Liu and Dr. Iris Wang."
# The 2019 label (old-storage/.../2019/04/sup_nature.png), typed in again: label form → amount.
LABEL = {
    "Vitamin A": "500 IU",
    "Vitamin C": "60 mg",
    "Vitamin E": "30 IU",
    "Thiamin": "4 mg",
    "Niacin": "50 mg",
    "Vitamin B6": "5 mg",
    "Folate": "800 mcg",
    "Vitamin B12": "20 mcg",
    "Pantothenic acid": "20 mg",
    "Calcium": "246 mg",
    "Coenzyme Q10": "100 mg",
    "N-acetyl-L-cysteine": "100 mg",
    "L-carnosine": "100 mg",
    "L-tyrosine": "100 mg",
    "L-theanine": "100 mg",
    "Vanillin": "20 mg",
    "Phosphatidylserine": "10 mg",
    "Resveratrol": "10 mg",
}
passed = failed = 0


def check(name, ok, detail=""):
    global passed, failed
    passed += bool(ok)
    failed += not ok
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


def open_page(browser, w, h, reduced=False, url=URL):
    ctx = browser.new_context(
        viewport={"width": w, "height": h}, reduced_motion="reduce" if reduced else "no-preference"
    )
    page = ctx.new_page()
    problems = []
    page.on(
        "console",
        lambda m: problems.append(m.text[:220])
        if m.type == "error" and "Failed to load resource" not in m.text
        else None,
    )
    page.on("pageerror", lambda e: problems.append(f"pageerror {str(e)[:220]}"))
    page.goto(url, wait_until="networkidle")
    page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    page.wait_for_timeout(1500)
    return ctx, page, problems


def box(page, chapter):
    return page.evaluate(
        f"""(() => {{ const s = document.querySelector('[data-chapter="{chapter}"]');
      return s ? {{ top: Math.round(s.getBoundingClientRect().top + scrollY), height: s.offsetHeight }} : null; }})()"""
    )


def sheet(paths, name):
    images = [Image.open(p).convert("RGB") for p in paths]
    scale = 0.5 if images[0].width > 800 else 0.8
    images = [im.resize((int(im.width * scale), int(im.height * scale))) for im in images]
    per_row = 3 if images[0].width > 400 else 5
    rows = [images[i : i + per_row] for i in range(0, len(images), per_row)]
    width = max(sum(im.width + 12 for im in row) for row in rows)
    height = sum(max(im.height for im in row) + 12 for row in rows)
    out = Image.new("RGB", (width, height), (40, 44, 52))
    y = 0
    for row in rows:
        x = 0
        for im in row:
            out.paste(im, (x, y))
            x += im.width + 12
        y += max(im.height for im in row) + 12
    path = os.path.join(OUT, f"nc-{name}-sheet.png")
    out.save(path)
    return path


def walk(page, run, h):
    """Scroll through every chapter in steps, one viewport shot per step, checking sideways scroll."""
    overflow = []
    for chapter in CHAPTERS:
        b = box(page, chapter)
        if not b:
            continue
        step = int(h * 0.7)
        stops = list(range(b["top"], max(b["top"] + 1, b["top"] + b["height"] - h + step), step))[:9]
        paths = []
        for i, y in enumerate(stops):
            page.evaluate(f"window.scrollTo(0, {y})")
            page.wait_for_timeout(1300)
            path = os.path.join(OUT, f"nc-{run}-{chapter}-{i:02d}.png")
            page.screenshot(path=path)
            paths.append(path)
            wide = page.evaluate("document.documentElement.scrollWidth - innerWidth")
            if wide > 0:
                overflow.append(f"{chapter}@{y}:{wide}px")
        print(f"  {chapter}: {len(paths)} shots → {sheet(paths, f'{run}-{chapter}')}")
    check(f"{run}: no horizontal page scroll", not overflow, ", ".join(overflow[:5]))


def name_spacing(page, run):
    """The giant name keeps its word space and stands centred ("Nature Calm", not "NatureCalm")."""
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(2500)
    m = page.evaluate(
        """(() => {
          const a = document.querySelector('[data-giant-half="a"]').getBoundingClientRect();
          const b = document.querySelector('[data-giant-half="b"]').getBoundingClientRect();
          const size = parseFloat(getComputedStyle(document.querySelector('[data-giant-half="a"]')).fontSize);
          return { gap: b.left - a.right, size, left: a.left, right: innerWidth - b.right };
        })()"""
    )
    check(f"{run}: name keeps its word space", m["gap"] >= 0.15 * m["size"], str(m))
    check(f"{run}: name centred", abs(m["left"] - m["right"]) <= 16, str(m))


def facts(page, run):
    title = page.title()
    check(f"{run}: title names Nature Calm", "Nature Calm" in title, title)
    order = page.evaluate("[...document.querySelectorAll('[data-chapter]')].map(s => s.dataset.chapter)")
    check(f"{run}: chapters in order", order == CHAPTERS, str(order))

    inside = page.locator('[data-chapter="inside"]')
    first = inside.locator("ol").first.locator(":scope > li")
    check(f"{run}: six ingredients shown first", first.count() == 6, str(first.count()))
    more = inside.get_by_role("button", name=re.compile("Show all 18 ingredients"))
    check(f"{run}: 'Show all 18 ingredients' button", more.count() == 1)
    if more.count():
        more.scroll_into_view_if_needed()
        more.click()
        page.wait_for_timeout(600)
        shown = page.evaluate(
            """[...document.querySelectorAll('[data-chapter="inside"] ol > li')]
               .filter(li => li.offsetParent !== null).length"""
        )
        check(f"{run}: all 18 ingredients after Show all", shown == 18, str(shown))

    label_button = inside.get_by_role("button", name="See the full label")
    label_button.scroll_into_view_if_needed()
    label_button.click()
    page.wait_for_timeout(600)
    rows = page.evaluate(
        """[...document.querySelectorAll('[data-chapter="inside"] table tbody tr')]
           .map(r => [r.querySelector('th').innerText.trim(), r.querySelector('td').innerText.trim()])"""
    )
    check(f"{run}: label table has 18 rows", len(rows) == 18, str(len(rows)))
    for start, amount in LABEL.items():
        match = [r for r in rows if r[0].startswith(start)]
        check(
            f"{run}: label {start} = {amount}",
            len(match) == 1 and match[0][1] == amount,
            str(match),
        )
    text = page.evaluate("document.body.innerText")
    check(
        f"{run}: capsule wall and other ingredients",
        "rice flour, silicon dioxide, magnesium stearate and cellulose" in text
        and "Capsule: vegetable cellulose." in text,
    )
    check(f"{run}: serving line", "Take 3 capsules once a day, with or after a meal." in text)
    check(f"{run}: 90 capsules, 30 days", "90 vegetarian capsules · 30-day supply" in text)
    check(f"{run}: credit", CREDIT in text)

    people = page.locator('[data-chapter="people"]')
    people_text = people.inner_text()
    check(
        f"{run}: both people named",
        "Dr. Jiankang Liu" in people_text and "Dr. Iris Wang" in people_text,
    )
    alts = page.evaluate(
        "[...document.querySelectorAll('[data-chapter=\"people\"] img')].map(i => i.alt)"
    )
    check(f"{run}: only Dr. Liu pictured", alts == ["Portrait of Dr. Jiankang Liu"], str(alts))

    heading = page.locator('[data-chapter="research"] h2').inner_text().replace("\n", " ").strip()
    check(f"{run}: research heading is Nature Calm's own", heading == "The research behind the formula", heading)
    why = page.evaluate(
        """(() => { const s = document.querySelector('[data-chapter="why"]');
          return [...s.querySelectorAll('img')].map(i => i.getAttribute('src')); })()"""
    )
    check(
        f"{run}: why chapter shows the microscope, off and on",
        any("why-microscope-off" in src for src in why) and any("why-microscope-on" in src for src in why),
        str(why),
    )
    years = page.evaluate(
        "[...document.querySelectorAll('[data-chapter=\"research\"] [data-study]')].map(li => li.querySelector('p').innerText.trim())"
    )
    check(f"{run}: seven studies", len(years) == 7, str(years))
    check(f"{run}: studies oldest first", years == sorted(years), str(years))
    links = page.evaluate(
        """[...document.querySelectorAll('[data-chapter="research"] a[href*="pubmed"]')]
           .map(a => [a.target, a.rel])"""
    )
    check(
        f"{run}: study links open a new tab safely",
        len(links) == 7 and all(t == "_blank" and "noopener" in r for t, r in links),
        str(links[:2]),
    )
    lower = text.lower()
    banned = [w for w in ("rat", "rats", "sleep", "clinically proven") if re.search(rf"\b{w}\b", lower)]
    check(f"{run}: no banned words", not banned, str(banned))


with sync_playwright() as p:
    browser = p.chromium.launch(args=ARGS)

    ctx = browser.new_context()
    for locale in ["", "/kr", "/cns", "/jp", "/vn"]:
        r = ctx.request.get(f"{BASE}{locale}/products/nature-calm")
        check(f"route {locale or '/'}products/nature-calm answers 200", r.status == 200, str(r.status))
    ctx.close()

    ctx, page, problems = open_page(browser, 1440, 900, url=f"{BASE}/")
    hrefs = page.evaluate(
        "[...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')).filter(h => h.includes('nature-calm'))"
    )
    check("homepage links to the Nature Calm page", any("/products/nature-calm" in h for h in hrefs), str(hrefs[:3]))
    ctx.close()

    for run, (w, h, reduced) in {
        "desktop": (1440, 900, False),
        "phone": (390, 844, False),
        "desktop-reduced": (1440, 900, True),
    }.items():
        print(f"— {run} {w}x{h}{' reduced motion' if reduced else ''}")
        ctx, page, problems = open_page(browser, w, h, reduced)
        if run == "phone":
            name_spacing(page, run)
        if run != "desktop-reduced":
            walk(page, run, h)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(800)
        facts(page, run)
        time.sleep(0.5)
        check(f"{run}: no console or page errors", not problems, "; ".join(problems[:3]))
        ctx.close()
    browser.close()

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
