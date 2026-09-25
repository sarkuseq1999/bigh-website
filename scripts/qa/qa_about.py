"""QA for the About page (/about, look A "Calm", Mo's pick) at desktop (1440x900) and phone (390x844).

At each size: no page or console errors and no failed requests; all the locked words on the page,
and never "CellGen"; one h1; the four part anchors; no review switcher left; no sideways scrolling;
every image has an alt; tap targets in the page body at least 44 px; body text at least 17 px; the
Ask BiGH Science and Support panels open and close; the opening photo is soft below the fold and
sharp once it reaches the middle of the window. A reduced-motion run checks the photo is sharp from
the start, and Korean is smoke-tested.

Pictures: scripts/qa/out/about-a-<size>-NN.png, viewport shots taken while scrolling (full-page
screenshots break the svh layouts). The review looks B, C and the A-then-B mix, and their checks,
are in the history at commit 2db8f07.

Usage: python -X utf8 scripts/qa/qa_about.py [base-url]
"""

import os
import re
import sys

from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3009"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
results = []

LOCKED = [
    "About BiGH",
    "Be in Good Health.",
    "What our name stands for. What our work is for.",
    "A full life has many parts.",
    "We focus on one you can’t see: your cells.",
    "Our mission is to support cellular health and mental energy, helping people live life to the fullest.",
    "Our key formulas begin with scientists.",
    "Dr. Jian Kang Liu, our Chief Scientific Advisor, studies mitochondria and aging. With Dr. Iris Wang, he developed NuriCell and Nature Calm.",
    "280+",
    "scientific papers by Dr. Liu",
    "Meet our scientists",
    "Our flagship formula is older than BiGH.",
    "2016",
    "BiGH founded in California",
    "20+ years",
    "NuriCell’s formula, unchanged",
    "What you can count on.",
    "Made in California.",
    "By GMP-certified manufacturers.",
    "Know where it comes from.",
    "Our green propolis comes only from Minas Gerais, Brazil.",
    "45 days to decide.",
    "Not right for you? Send it back for a refund.",
    "Answers in your language.",
    "We reply in the language you write in.",
    "Curious about the science?",
    "Ask BiGH Science. We help you explore the research, with guidance from the scientists we work with.",
    "Explore our products",
]
SIZES = ((1440, 900, "desk"), (390, 844, "phone"))
BLUR = "() => { const f = getComputedStyle(document.querySelector('[class*=photoImage]')).filter; const m = /blur\\(([\\d.]+)px\\)/.exec(f); return m ? parseFloat(m[1]) : 0 }"


def check(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + ("  [" + detail + "]" if detail else ""))


def watch(page):
    problems = []
    page.on("pageerror", lambda e: problems.append("pageerror " + str(e)[:140]))
    page.on(
        "console",
        lambda m: problems.append(f"console.{m.type} " + m.text[:140]) if m.type in ("error", "warning") else None,
    )
    page.on("requestfailed", lambda r: problems.append("requestfailed " + r.url[-80:]))
    page.on("response", lambda r: problems.append(f"http {r.status} " + r.url[-80:]) if r.status >= 400 else None)
    return problems


def shoot_scroll(page, name):
    """Viewport shots from top to bottom."""
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(700)
    height = page.evaluate("document.documentElement.scrollHeight")
    view = page.evaluate("innerHeight")
    y, i = 0, 0
    while True:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(600)
        page.screenshot(path=os.path.join(OUT, f"{name}-{i:02d}.png"))
        i += 1
        if y + view >= height or i >= 24:
            break
        y = min(y + int(view * 0.9), height - view)
    return i


def page_checks(page, tag):
    main_text = re.sub(r"\s+", " ", page.evaluate("document.querySelector('main').innerText"))
    missing = [words for words in LOCKED if words not in main_text]
    check(f"{tag}: every locked line is on the page", not missing, f"missing={missing}")
    check(f"{tag}: never names CellGen", "cellgen" not in main_text.lower())
    h1 = page.locator("h1").count()
    anchors = page.evaluate("['purpose','roots','experience','promise'].filter(id => !document.getElementById(id))")
    check(f"{tag}: one h1 and the four part anchors", h1 == 1 and not anchors, f"h1={h1} missingAnchors={anchors}")
    switcher = page.locator("nav[aria-label='Design options']").count()
    check(f"{tag}: no review switcher left", switcher == 0, f"switchers={switcher}")
    overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    check(f"{tag}: no sideways scrolling", overflow == 0, f"overflow={overflow}")
    no_alt = page.evaluate("[...document.images].filter(i => !i.hasAttribute('alt')).map(i => i.src.slice(-40))")
    check(f"{tag}: every image has an alt", not no_alt, f"{no_alt}")
    small = page.evaluate(
        """() => [...document.querySelectorAll('main a, main button')]
            .map(e => [e.textContent.trim().slice(0, 30), e.getBoundingClientRect()])
            .filter(([, r]) => r.width > 0 && (r.height < 44 || r.width < 44))
            .map(([t, r]) => `${t}:${Math.round(r.width)}x${Math.round(r.height)}`)"""
    )
    check(f"{tag}: tap targets in the page are at least 44 px", not small, f"{small}")
    tiny = page.evaluate(
        """() => [...document.querySelectorAll('main p, main li, main h3')]
            .filter(e => e.offsetParent && parseFloat(getComputedStyle(e).fontSize) < 17)
            .map(e => e.textContent.trim().slice(0, 30) + ':' + getComputedStyle(e).fontSize)"""
    )
    check(f"{tag}: body text at least 17 px", not tiny, f"{tiny[:4]}")


def photo_check(page, tag):
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(400)
    at_top = page.evaluate(BLUR)
    page.evaluate(
        "() => { const r = document.querySelector('[class*=photo]').getBoundingClientRect(); window.scrollBy(0, r.top + r.height / 2 - innerHeight / 2) }"
    )
    page.wait_for_timeout(500)
    in_middle = page.evaluate(BLUR)
    check(f"{tag}: the photo is soft below the fold and sharp in the middle", at_top > in_middle and in_middle < 0.3, f"blur top={at_top} middle={in_middle}")


def panel_checks(page, tag):
    page.evaluate("window.scrollTo(0, 0)")
    page.get_by_role("button", name="Ask BiGH Science").first.click()
    page.wait_for_timeout(400)
    title = page.evaluate("document.querySelector('dialog[open] h2')?.textContent")
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    closed = page.evaluate("!document.querySelector('dialog[open]')")
    check(f"{tag}: Ask BiGH Science panel opens and Escape closes it", title == "Ask BiGH Science" and closed, f"title={title} closed={closed}")
    if tag == "phone":
        page.get_by_role("button", name="Open menu").click()
        page.wait_for_timeout(300)
    page.locator("header").get_by_role("button", name="Support").click()
    page.wait_for_timeout(400)
    title = page.evaluate("document.querySelector('dialog[open] h2')?.textContent")
    page.get_by_role("button", name="Close details").click()
    page.wait_for_timeout(300)
    closed = page.evaluate("!document.querySelector('dialog[open]')")
    check(f"{tag}: Support panel opens from the menu and closes", title == "BiGH support" and closed, f"title={title} closed={closed}")


with sync_playwright() as p:
    browser = p.chromium.launch()
    for w, h, tag in SIZES:
        page = browser.new_page(viewport={"width": w, "height": h})
        problems = watch(page)
        page.goto(f"{BASE}/about", wait_until="networkidle")
        page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
        page.wait_for_timeout(600)
        page_checks(page, tag)
        photo_check(page, tag)
        shots = shoot_scroll(page, f"about-a-{tag}")
        panel_checks(page, tag)
        check(f"{tag}: no errors, warnings or failed requests ({shots} shots)", not problems, f"{problems[:3]}")
        page.close()

        # Reduced motion: the photo is sharp from the start.
        page = browser.new_page(viewport={"width": w, "height": h}, reduced_motion="reduce")
        problems = watch(page)
        page.goto(f"{BASE}/about", wait_until="networkidle")
        page.wait_for_timeout(600)
        f = page.evaluate("getComputedStyle(document.querySelector('[class*=photoImage]')).filter")
        check(f"{tag}-reduced: the photo is sharp from the start, no errors", f == "none" and not problems, f"filter={f} {problems[:3]}")
        page.close()

    # Korean: the page renders (untranslated About lines fall back to English for now).
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    problems = watch(page)
    page.goto(f"{BASE}/kr/about", wait_until="networkidle")
    page.wait_for_timeout(600)
    lang = page.evaluate("document.documentElement.lang")
    check("kr-desk: the page renders in the Korean site with no errors", lang == "ko" and page.locator("h1").count() == 1 and not problems, f"lang={lang} {problems[:3]}")
    page.close()
    browser.close()

print(f"\n{sum(results)} passed, {len(results) - sum(results)} failed")
