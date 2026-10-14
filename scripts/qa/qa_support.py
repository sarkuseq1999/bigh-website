"""QA for the Support page, "Pull up a chair" (Mo, October 14, 2026; spec
docs/superpowers/specs/2026-10-14-support-page-design.md; mockups reference/ink-pages/mockups/support/).

opening (1440x900, 390x844): 200; the title "BiGH — Support"; no console errors or warnings (but
PREFETCH_CSS); no failed requests; one h1 "How can we help?"; the lead; the phone number as a tel:
link in Switzer, the email as a mailto: link, the hours; the porch painting multiplies; its steam is
gold leaf over the porch, not multiplied; nothing scrolls sideways; text 15px+; the menu bar marks
Support (Task 5 adds the link; until then the bar's root says data-page="support").
motion (1440x900): with motion the steam waits while the porch waits, then rises (its --rise grows
from under 30% to 100%+ within 6s of the porch's bloom; sampled every frame from the page's first
one, since the rise has begun by the time the page is idle); the gold never rises alone over bare
paper: with the porch's request held for 4.5s the steam's --rise stays under 30% the whole time the
porch's picture is not in (the porch has bloomed by then), and it starts to rise only once the
picture is in, and a porch whose picture fails never lets it rise; reduced motion: the steam is
whole at once; no script: the porch and the steam are whole.
rhythm (1440, 1280, 1024, 960, 768, 390, 360): Write to us, Returns and Questions each have a
painting; from 960px the sides take turns (left, right, left), below it each painting comes first
on one column; no words past the right margin; nothing scrolls sideways; the parts' words.
questions (1440x900): four <details>, the first open at rest, opening one closes the others, each
question a 48px+ target, "Ask BiGH Science" opens its sheet.
form (1440x900, 390x844, 360x780): the labels and the reaction note; the preview tag beside Send;
topic chips never one alone on a row; every control 48px+; fields are lines, never boxes; an empty
Send names the four missing things and focuses the first; a wrong email is caught; a 5 MB photo and
a PDF are refused, a picture is kept by name and can be removed; Enter sends once: one thank-you, a
ticket number like BH-1014-7K3Q carrying today's month and day, focus on "Thank you.", the preview
line (plain words, no box), the number holds still, the cup multiplies and no wrapper stops it, the
cup's plate is twice as wide as it is shown (crisp at 2x); "Write another message" brings back an
empty form focused on the name; the thank-you's steam waits for both its pictures (the cup's, then the
steam's request held for 3s: the steam stays under 30% while one is out, then rises); reduced motion:
the thank-you at once, steam whole.
form, other cases: a double send (a double click; two requestSubmit() calls in one task; with motion
and with reduced motion) gives one thank-you and one ticket (the second submit draws no second one),
and with motion the form is seen fading out first; no script: no form in the page, a line with the
email and the phone as real links, no query string; forced colors (Windows High Contrast): the fields
keep a bottom border, focus shows an outline, the chosen chip differs from the rest.
(Later tasks add: languages, links.)

Pictures: scripts/qa/out/support/<tag>.png.

Usage: python -X utf8 scripts/qa/qa_support.py [base-url] [--only=opening,motion,...]
"""

import os
import re
import sys
import tempfile
from urllib.parse import parse_qs, unquote, urlparse

from PIL import Image
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3060"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out", "support")
os.makedirs(OUT, exist_ok=True)
results = []

PREFETCH_CSS = re.compile(
    r"^The resource \S+/_next/static/\S+\.css was preloaded using link preload but not used "
    r"within a few seconds from the window's load event\."
)


def check(name, ok, detail=""):
    results.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}{(' — ' + str(detail)) if detail and not ok else ''}")


def counted(message):
    return message.type != "warning" or not PREFETCH_CSS.match(message.text)


def open_page(browser, width, height, path="/support", reduced=False):
    context = browser.new_context(
        viewport={"width": width, "height": height},
        reduced_motion="reduce" if reduced else "no-preference",
    )
    page = context.new_page()
    errors, failed = [], []
    page.on("console", lambda m: errors.append(m.text) if m.type in ("error", "warning") and counted(m) else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("requestfailed", lambda r: failed.append(r.url))
    response = page.goto(f"{BASE}{path}", wait_until="networkidle", timeout=120000)
    page.evaluate("document.fonts.ready.then(() => true)")
    page.wait_for_timeout(1200)
    return context, page, response, errors, failed


def scroll_through(page, step=450, pause=250):
    """Read to the end like a visitor (lazy pictures load, blooms fire), then back to the top."""
    total = page.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < total:
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(pause)
        y += step
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(600)


SMALL_TEXT_JS = """[...document.querySelectorAll('main *')].filter(e => {
  if (!e.childNodes.length || ![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return false;
  const s = getComputedStyle(e); return s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.fontSize) < 15;
}).map(e => [e.textContent.trim().slice(0, 30), getComputedStyle(e).fontSize])"""


def opening(browser):
    for width, height in ((1440, 900), (390, 844)):
        tag = f"opening {width}"
        context, page, response, errors, failed = open_page(browser, width, height)
        check(f"{tag}: 200", response and response.status == 200, response and response.status)
        check(f"{tag}: the title", page.title() == "BiGH — Support", page.title())
        h1 = page.evaluate("[...document.querySelectorAll('h1')].map(h => h.textContent.trim())")
        check(f"{tag}: one h1, 'How can we help?'", h1 == ["How can we help?"], h1)
        main = page.inner_text("main")
        for words in ["Pull up a chair. We’re listening.", "Call us", "Email us", "Hours",
                      "Monday to Friday, 9am to 6pm Pacific"]:
            check(f"{tag}: says {words!r}", words in main)
        tel = page.evaluate("""(() => { const a = document.querySelector('main a[href^="tel:"]');
          return a ? [a.getAttribute('href'), a.textContent.trim(), getComputedStyle(a).fontFamily] : null; })()""")
        check(f"{tag}: the number is a tel: link in Switzer",
              tel and tel[0] == "tel:+18009192089" and tel[1] == "800-919-2089" and "ysabeau" not in tel[2].lower(), tel)
        mail = page.evaluate("document.querySelector('main a[href^=\"mailto:\"]')?.getAttribute('href')")
        check(f"{tag}: the email is a mailto: link", mail == "mailto:support@bighnow.com", mail)
        blend = page.evaluate("""[...document.querySelectorAll('[data-part="opening"] img')].map(i =>
          [i.getAttribute('src').includes('steam') ? 'steam' : 'ink', getComputedStyle(i).mixBlendMode])""")
        check(f"{tag}: the porch multiplies, its steam does not",
              ["ink", "multiply"] in blend and ["steam", "normal"] in blend, blend)
        title_font = page.evaluate("getComputedStyle(document.querySelector('h1')).fontFamily")
        check(f"{tag}: the title is in Ysabeau", "ysabeau" in title_font.lower(), title_font)
        sideways = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        check(f"{tag}: nothing scrolls sideways", sideways <= 0, sideways)
        small = page.evaluate(SMALL_TEXT_JS)
        check(f"{tag}: text 15px or more", not small, small[:3])
        check(f"{tag}: the page says it is Support", page.evaluate("document.querySelector('[data-look]')?.dataset.page") == "support")
        page.screenshot(path=os.path.join(OUT, f"opening-{width}.png"))
        scroll_through(page)
        check(f"{tag}: no errors", not errors, errors[:3])
        check(f"{tag}: no failed requests", not failed, failed[:3])
        context.close()


RISE_JS = "parseFloat(getComputedStyle(document.querySelector('[data-steam]')).getPropertyValue('--rise'))"

# Watches the steam from the first frame the page has one (open_page waits for the network, the
# fonts and 1.2s, by when the steam has long been rising): one sample per frame,
# [ms since the page began, the steam's --rise, the porch's data-bloom, whether the porch's picture
# is in (complete, with a width)].
WATCH_RISE = """
window.__rise = [];
const t0 = performance.now();
const tick = () => {
  const steam = document.querySelector('[data-steam]');
  const porch = document.querySelector('[data-part="opening"] [data-bloom]');
  if (steam) window.__rise.push([performance.now() - t0,
    parseFloat(getComputedStyle(steam).getPropertyValue('--rise')), porch && porch.dataset.bloom,
    !!porch && porch.complete && porch.naturalWidth > 0]);
  if (window.__rise.length < 6000) requestAnimationFrame(tick);
};
requestAnimationFrame(tick);
"""


def is_porch(url):
    """The porch's own picture (not its steam, "porch-steam-v1"), as Next's image route serves it."""
    return "/_next/image" in url and "porch-v1" in url


def watched_page(browser, on_porch=None, **options):
    """A 1440x900 page that records the steam from its first frame; on_porch(route) handles the
    porch's picture request (hold it, or fail it)."""
    context = browser.new_context(viewport={"width": 1440, "height": 900}, **options)
    context.add_init_script(WATCH_RISE)
    page = context.new_page()
    if on_porch is not None:
        page.route(is_porch, on_porch)
    return context, page


def motion(browser):
    context, page = watched_page(browser, reduced_motion="no-preference")
    page.goto(f"{BASE}/support", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_function("window.__rise.some(s => s[2] && s[2] !== 'waiting')", timeout=30000)
    page.wait_for_timeout(6500)
    samples = page.evaluate("window.__rise")
    waiting = [s for s in samples if s[2] == "waiting"]
    bloomed = [s for s in samples if s[2] != "waiting"]
    check("motion: the steam waits while the porch waits",
          waiting and all(s[1] < 30 for s in waiting), [round(s[1]) for s in waiting[:5]])
    start, end = bloomed[0], max(s[1] for s in bloomed if s[0] <= bloomed[0][0] + 6000)
    check("motion: the steam rises after the porch blooms", start[1] < 30 and end >= 100,
          [round(start[1]), round(end)])
    context.close()

    # The gold never rises alone over bare paper (About's circle, Mo): the porch's request is held
    # for 4.5s. The porch has bloomed by then (the kit opens a painting once its box is on screen,
    # picture or not), so a rise tied only to the bloom would run in that time.
    held = []
    context, page = watched_page(browser, on_porch=lambda route: held.append(route), reduced_motion="no-preference")
    page.goto(f"{BASE}/support", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_function("window.__rise.some(s => s[2] && s[2] !== 'waiting')", timeout=30000)
    page.wait_for_timeout(4500)
    out = page.evaluate("window.__rise")
    bare = [s for s in out if not s[3]]
    check("motion (late porch): the porch has bloomed and its picture is still out (the case is real)",
          held and any(s[2] != "waiting" for s in bare) and bare[-1][0] - bare[0][0] >= 4000,
          [len(held), len(bare), round(bare[-1][0] - bare[0][0]) if bare else None])
    check("motion (late porch): the steam stays down while the porch's picture is out",
          bare and all(s[1] < 30 for s in bare), max((round(s[1]) for s in bare), default=None))
    for route in held:
        route.continue_()
    page.wait_for_function("window.__rise.some(s => s[3])", timeout=30000)
    page.wait_for_timeout(6500)
    after = page.evaluate("window.__rise")
    rising = next((s for s in after if s[1] >= 30), None)
    check("motion (late porch): once the picture is in, the steam rises",
          rising and rising[3] and max(s[1] for s in after) >= 100,
          [rising and round(rising[0]), rising and rising[3], round(max(s[1] for s in after))])
    context.close()

    # A porch whose picture fails never lets the gold rise.
    context, page = watched_page(browser, on_porch=lambda route: route.abort(), reduced_motion="no-preference")
    page.goto(f"{BASE}/support", wait_until="domcontentloaded", timeout=120000)
    page.wait_for_function("window.__rise.some(s => s[2] && s[2] !== 'waiting')", timeout=30000)
    page.wait_for_timeout(5000)
    failed = page.evaluate("window.__rise")
    state = page.evaluate("document.querySelector('[data-steam]').dataset.steam")
    check("motion (failed porch): the steam never rises", all(s[1] < 30 for s in failed) and state == "waiting",
          [round(max(s[1] for s in failed)), state])
    context.close()

    context, page, *_ = open_page(browser, 1440, 900, reduced=True)
    whole = page.evaluate(RISE_JS)
    check("motion (reduced): the steam is whole at once", whole >= 100, whole)
    context.close()

    # With no script nothing can mark the porch's picture in or its bloom: both show whole.
    context = browser.new_context(viewport={"width": 1440, "height": 900}, java_script_enabled=False)
    page = context.new_page()
    page.goto(f"{BASE}/support", wait_until="networkidle", timeout=120000)
    page.wait_for_timeout(800)
    seen = page.evaluate("""(() => ({
      rise: parseFloat(getComputedStyle(document.querySelector('[data-steam]')).getPropertyValue('--rise')),
      porch: getComputedStyle(document.querySelector('[data-part="opening"] img[data-bloom]')).opacity }))()""")
    check("motion (no script): the porch and its steam are whole", seen["rise"] >= 100 and seen["porch"] == "1", seen)
    context.close()


SIDES_JS = """[...document.querySelectorAll('main [data-part]')].filter(s => s.querySelector('[data-picture]') && s.dataset.part !== 'opening').map(s => {
  const p = s.querySelector('[data-picture]').getBoundingClientRect(), w = s.querySelector('[data-words]').getBoundingClientRect();
  return [s.dataset.part, p.left < w.left ? 'left' : p.top < w.top ? 'first' : 'right', Math.round(w.right), Math.round(p.width)]; })"""


def rhythm(browser):
    for width, height in ((1440, 900), (1280, 800), (1024, 768), (960, 800), (768, 1024), (390, 844), (360, 780)):
        tag = f"rhythm {width}"
        context, page, *_ = open_page(browser, width, height)
        scroll_through(page)
        sides = page.evaluate(SIDES_JS)
        parts = [s[0] for s in sides]
        check(f"{tag}: write, returns and questions each have a painting", parts == ["write", "returns", "questions"], parts)
        if width >= 960:
            check(f"{tag}: sides take turns (left, right, left)", [s[1] for s in sides] == ["left", "right", "left"], sides)
        else:
            check(f"{tag}: one column, each painting first", all(s[1] == "first" for s in sides), sides)
        over = page.evaluate("""[...document.querySelectorAll('main [data-words] *')].filter(e => e.getBoundingClientRect().right > window.innerWidth - 16 && e.textContent.trim()).map(e => e.textContent.trim().slice(0, 24))""")
        check(f"{tag}: no words past the right margin", not over, over[:3])
        sideways = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        check(f"{tag}: nothing scrolls sideways", sideways <= 0, sideways)
        main = page.inner_text("main")
        for words in ["45 days to decide.", "Send returns to", "Glendora, CA 91740", "Orders and shipping",
                      "Common questions.", "A question about health or science?"]:
            check(f"{tag}: says {words!r}", words in main)
        page.screenshot(path=os.path.join(OUT, f"rhythm-{width}.png"), full_page=False)
        context.close()


def questions(browser):
    context, page, *_ = open_page(browser, 1440, 900)
    faq = page.locator("#questions details")
    check("questions: four questions", faq.count() == 4, faq.count())
    check("questions: the first is open at rest", faq.nth(0).get_attribute("open") is not None)
    faq.nth(2).locator("summary").click()
    page.wait_for_timeout(300)
    opened = page.evaluate("[...document.querySelectorAll('#questions details')].map(d => d.open)")
    check("questions: opening one closes the others", opened == [False, False, True, False], opened)
    heights = page.evaluate("[...document.querySelectorAll('#questions summary')].map(s => Math.round(s.getBoundingClientRect().height))")
    check("questions: every question is a 48px+ target", all(h >= 48 for h in heights), heights)
    ask = page.locator("#questions button", has_text="Ask BiGH Science")
    ask.scroll_into_view_if_needed()
    ask.click()
    page.wait_for_timeout(1200)
    check("questions: Ask BiGH Science opens its sheet", page.evaluate("!!document.querySelector('dialog[open]')"))
    page.keyboard.press("Escape")
    context.close()


TICKET = re.compile(r"^BH-\d{4}-[A-HJKMNP-Z2-9]{4}$")


def fill(page, name="Ana Ruiz", email="ana@example.com", topic="A return", message="The seal on my bottle was broken."):
    page.fill("#support-name", name)
    page.fill("#support-email", email)
    if topic:
        page.locator("label", has_text=topic).click()
    page.fill("#support-message", message)


def form(browser):
    for width, height in ((1440, 900), (390, 844), (360, 780)):
        tag = f"form {width}"
        context, page, *_ = open_page(browser, width, height)
        page.locator("#write").scroll_into_view_if_needed()
        page.wait_for_timeout(600)
        main = page.inner_text("#write")
        for words in ["Your name", "Email", "Order number (optional)", "What is it about?", "Your message",
                      "Add a photo (optional)", "I had a reaction", "In an emergency, call 911."]:
            check(f"{tag}: says {words!r}", words in main)
        check(f"{tag}: the preview tag stands beside Send", page.locator("form [data-honesty]").inner_text().strip() == "Preview: messages aren’t sent yet")
        rows = page.evaluate("""(() => { const tops = {}; document.querySelectorAll('[data-topics] label').forEach(l => { const t = Math.round(l.getBoundingClientRect().top); tops[t] = (tops[t] || 0) + 1; }); return Object.values(tops); })()""")
        check(f"{tag}: the topic chips never leave one alone on a row", rows == [1, 1, 1, 1, 1] or 1 not in rows, rows)
        targets = page.evaluate("""[...document.querySelectorAll('form input:not([type=radio]):not([type=file]), form textarea, form button, [data-topics] label, form label[for=support-photo]')]
          .map(e => [e.id || e.textContent.trim().slice(0, 20), Math.round(e.getBoundingClientRect().height)]).filter(([, h]) => h < 48)""")
        check(f"{tag}: every control is 48px or more", not targets, targets)
        boxes = page.evaluate("""[...document.querySelectorAll('form input:not([type=radio]):not([type=file]), form textarea')].filter(e => {
          const s = getComputedStyle(e); return parseFloat(s.borderTopWidth) > 0 || parseFloat(s.borderLeftWidth) > 0; }).map(e => e.id)""")
        check(f"{tag}: fields are writing lines, never boxes", not boxes, boxes)

        # Send with nothing filled: four plain messages, focus on the first field.
        page.click("form button[type=submit]")
        page.wait_for_timeout(300)
        errs = page.evaluate("[...document.querySelectorAll('form [data-error]')].map(e => e.textContent.trim())")
        check(f"{tag}: empty Send says what is missing", errs == ["Please add your name.", "Please add an email we can reply to.", "Please choose what it’s about.", "Please write your message."], errs)
        check(f"{tag}: focus goes to the first missing field", page.evaluate("document.activeElement.id") == "support-name")
        check(f"{tag}: the missing fields are marked invalid", page.evaluate("document.querySelector('#support-name').getAttribute('aria-invalid')") == "true")

        # A wrong email, then a fix.
        fill(page, email="ana@")
        page.click("form button[type=submit]")
        page.wait_for_timeout(300)
        errs = page.evaluate("[...document.querySelectorAll('form [data-error]')].map(e => e.textContent.trim())")
        check(f"{tag}: a wrong email is caught", errs == ["Please add an email we can reply to."], errs)

        # Photos: too big, not a picture, then a good one, removed.
        with tempfile.TemporaryDirectory() as tmp:
            big = os.path.join(tmp, "big.jpg")
            with open(big, "wb") as f:
                f.write(b"\xff\xd8\xff" + b"0" * (5 * 1024 * 1024))
            pdf = os.path.join(tmp, "label.pdf")
            with open(pdf, "wb") as f:
                f.write(b"%PDF-1.4\n%%EOF\n")
            small = os.path.join(tmp, "bottle.png")
            with open(small, "wb") as f:
                f.write(bytes.fromhex("89504e470d0a1a0a0000000d4948445200000001000000010806000000"
                                      "1f15c4890000000d49444154789c6360000002000154a24f5d0000000049454e44ae426082"))
            page.set_input_files("#support-photo", big)
            page.wait_for_timeout(200)
            check(f"{tag}: a 5 MB photo is refused", "Photos up to 4 MB, please." in page.inner_text("form"))
            page.set_input_files("#support-photo", pdf)
            page.wait_for_timeout(200)
            check(f"{tag}: a PDF is refused", "Please choose a photo (JPG, PNG or HEIC)." in page.inner_text("form"))
            page.set_input_files("#support-photo", small)
            page.wait_for_timeout(200)
            check(f"{tag}: a picture is kept, by name", "bottle.png" in page.inner_text("form"))
            page.click("form button:has-text('Remove photo')")
            page.wait_for_timeout(200)
            check(f"{tag}: the photo can be removed", "bottle.png" not in page.inner_text("form"))

        # Enter in a field sends (the form fades out for 0.3s first): one thank-you, one number. A real
        # double send is in double_send() below.
        fill(page)
        page.focus("#support-name")
        page.keyboard.press("Enter")
        page.wait_for_timeout(900)
        panels = page.locator("[data-sent]").count()
        ticket = page.locator("[data-ticket]").inner_text().strip() if panels else ""
        check(f"{tag}: one thank-you", panels == 1, panels)
        check(f"{tag}: a ticket number like BH-1014-7K3Q", TICKET.match(ticket) is not None, ticket)
        today = page.evaluate("(() => { const d = new Date(); return String(d.getMonth() + 1).padStart(2, '0') + String(d.getDate()).padStart(2, '0'); })()")
        check(f"{tag}: the ticket carries today's month and day", ticket[3:7] == today, [ticket, today])
        check(f"{tag}: focus moves to the thank-you", page.evaluate("document.activeElement.id") == "sent-title")
        sent = page.inner_text("[data-sent]")
        check(f"{tag}: the thank-you says nothing was sent, and how to reach us",
              "This is a preview, so nothing was sent." in sent and "800-919-2089" in sent and "support@bighnow.com" in sent, sent)
        page.wait_for_timeout(1500)
        check(f"{tag}: the number holds still", page.locator("[data-ticket]").inner_text().strip() == ticket)
        # The cup multiplies onto the paper, its steam does not, and nothing between the cup and the
        # page root makes a stacking context (which would stop the multiply).
        stack = page.evaluate("""(() => {
          const img = document.querySelector('[data-sent] img:not([data-steam])');
          const steam = document.querySelector('[data-sent] img[data-steam]');
          const bad = [];
          for (let e = img.parentElement; e && !e.hasAttribute('data-look'); e = e.parentElement) {
            const s = getComputedStyle(e);
            if (parseFloat(s.opacity) < 1 || s.transform !== 'none' || s.filter !== 'none' || s.isolation === 'isolate'
                || s.maskImage !== 'none' || s.mixBlendMode !== 'normal' || s.perspective !== 'none' || s.clipPath !== 'none'
                || (s.zIndex !== 'auto' && s.position !== 'static') || s.translate !== 'none' || s.rotate !== 'none'
                || s.scale !== 'none' || s.willChange !== 'auto' || s.contain.includes('paint'))
              bad.push(e.tagName + '.' + String(e.className).slice(0, 30));
          }
          return [getComputedStyle(img).mixBlendMode, getComputedStyle(steam).mixBlendMode, bad];
        })()""")
        check(f"{tag}: the cup multiplies, its steam does not, and no wrapper stops the multiply",
              stack[0] == "multiply" and stack[1] == "normal" and not stack[2], stack)
        # The preview line is plain words (DESIGN.md: nothing is boxed); the honesty tag beside Send is
        # the kit's one-line pill and stays.
        box = page.evaluate("""(() => { const s = getComputedStyle(document.querySelector('[data-sent] [data-honesty]'));
          return [s.borderTopWidth, s.borderLeftWidth, s.borderTopLeftRadius, s.paddingTop, s.paddingLeft]; })()""")
        check(f"{tag}: the thank-you's preview line is plain text, not a box", box == ["0px"] * 5, box)
        # The cup stays crisp on a 2x screen: its plate is at least twice as wide as it is shown.
        shown = page.evaluate("document.querySelector('[data-sent] img:not([data-steam])').getBoundingClientRect().width")
        current = page.evaluate("document.querySelector('[data-sent] img:not([data-steam])').currentSrc")
        plate = Image.open(os.path.join(REPO, "public", unquote(parse_qs(urlparse(current).query)["url"][0]).lstrip("/"))).width
        check(f"{tag}: the cup's plate ({plate}px) is at least twice its width on the page ({shown:.0f}px)",
              plate >= 2 * shown, [plate, shown])
        page.screenshot(path=os.path.join(OUT, f"sent-{width}.png"))

        # Write another message: an empty form, focus on the name.
        page.click("[data-sent] button:has-text('Write another message')")
        page.wait_for_timeout(400)
        check(f"{tag}: Write another message brings back an empty form",
              page.locator("form[data-support-form]").count() == 1 and page.input_value("#support-name") == "")
        check(f"{tag}: focus goes to Your name", page.evaluate("document.activeElement.id") == "support-name")
        context.close()

    # Reduced motion: the thank-you is there at once, its steam whole.
    context, page, *_ = open_page(browser, 1440, 900, reduced=True)
    page.locator("#write").scroll_into_view_if_needed()
    fill(page)
    page.click("form button[type=submit]")
    page.wait_for_timeout(100)
    rise = page.evaluate("parseFloat(getComputedStyle(document.querySelector('[data-sent] [data-steam]')).getPropertyValue('--rise'))")
    check("form (reduced): the thank-you at once, its steam whole", page.locator("[data-sent]").count() == 1 and rise >= 100, rise)
    context.close()

    late_picture(browser, "cup")
    late_picture(browser, "steam")
    double_send(browser)
    no_script(browser)
    forced_colors(browser)


def is_cup(url):
    """The thank-you's cup picture, as Next's image route serves it (its steam is "cup-steam-v2")."""
    return "/_next/image" in url and "cup-v2" in url


def is_cup_steam(url):
    return "/_next/image" in url and "cup-steam-v2" in url


# One sample per frame once the thank-you has a steam: [ms, the steam's --rise, its data-steam, whether
# both of its pictures are in (the cup's and the steam's: complete, with a width)].
WATCH_SENT = """
window.__sent = [];
const t0 = performance.now();
const isIn = (img) => !!img && img.complete && img.naturalWidth > 0;
const tick = () => {
  const steam = document.querySelector('[data-sent] [data-steam]');
  const cup = document.querySelector('[data-sent] img:not([data-steam])');
  if (steam) window.__sent.push([performance.now() - t0,
    parseFloat(getComputedStyle(steam).getPropertyValue('--rise')), steam.dataset.steam,
    isIn(cup) && isIn(steam)]);
  if (window.__sent.length < 6000) requestAnimationFrame(tick);
};
requestAnimationFrame(tick);
"""


def late_picture(browser, which):
    """The gold never rises alone over bare paper (the porch's rule, here for the thank-you too): both
    of the thank-you's pictures load only after Send, so one request (the cup's or the steam's) is
    held for 3s and the steam must stay down until both are in."""
    tag = f"form (late {which})"
    held = []
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="no-preference")
    page = context.new_page()
    page.route(is_cup if which == "cup" else is_cup_steam, lambda route: held.append(route))
    page.goto(f"{BASE}/support", wait_until="networkidle", timeout=120000)
    page.evaluate("document.fonts.ready.then(() => true)")
    page.wait_for_timeout(1200)
    page.locator("#write").scroll_into_view_if_needed()
    fill(page)
    page.evaluate(WATCH_SENT)
    page.click("form button[type=submit]")
    page.wait_for_timeout(3500)
    out = page.evaluate("window.__sent")
    bare = [s for s in out if not s[3]]
    check(f"{tag}: the thank-you is up and the {which}'s picture is still out (the case is real)",
          held and len(bare) > 10 and bare[-1][0] - bare[0][0] >= 2500,
          [len(held), len(bare), round(bare[-1][0] - bare[0][0]) if bare else None])
    check(f"{tag}: the steam waits, and stays down while the {which} is out",
          bare and all(s[1] < 30 and s[2] == "waiting" for s in bare),
          [max((round(s[1]) for s in bare), default=None), sorted({s[2] for s in bare})])
    for route in held:
        route.continue_()
    page.wait_for_function("window.__sent.some(s => s[3])", timeout=30000)
    page.wait_for_timeout(5000)
    after = page.evaluate("window.__sent")
    rising = next((s for s in after if s[1] >= 30), None)
    check(f"{tag}: once both pictures are in, the steam rises",
          rising and rising[3] and max(s[1] for s in after) >= 100,
          [rising and round(rising[0]), rising and rising[3], round(max(s[1] for s in after))])
    context.close()


SENT_JS = "[document.querySelectorAll('[data-sent]').length, [...document.querySelectorAll('[data-ticket]')].map(t => t.textContent.trim())]"
FORM_NOW_JS = """(() => { const f = document.querySelector('form[data-support-form]');
  return [!!f, f ? parseFloat(getComputedStyle(f).opacity) : null, document.querySelectorAll('[data-sent]').length]; })()"""


def double_send(browser):
    """Send twice in a row, as a person with a quick finger or a double click does: one thank-you and
    one number, whether the form fades out first (motion) or goes at once (reduced motion)."""
    for how in ("a double click", "two requestSubmit() calls in one task"):
        for reduced in (False, True):
            tag = f"form (double send, {how}{', reduced' if reduced else ''})"
            context, page, *_ = open_page(browser, 1440, 900, reduced=reduced)
            page.locator("#write").scroll_into_view_if_needed()
            fill(page)
            # Make the ticket's four signs countable: each call of Math.random is the next sign
            # (A, B, C, D, E ...). A second submit that makes a second ticket would show as calls 5-8.
            page.evaluate("(() => { let n = 0; window.__draws = 0; Math.random = () => { window.__draws += 1; return (n++ % 31 + 0.5) / 31; }; })()")
            if how == "a double click":
                page.dblclick("form button[type=submit]")
            else:
                page.evaluate("(() => { const f = document.querySelector('form[data-support-form]'); f.requestSubmit(); f.requestSubmit(); })()")
            page.wait_for_timeout(80)
            if not reduced:
                # Spec "The moment": the form fades out (0.3s) before the thank-you comes.
                mid = page.evaluate(FORM_NOW_JS)
                check(f"{tag}: the form is fading out and no thank-you has come yet", mid[0] and mid[1] < 1 and mid[2] == 0, mid)
            page.wait_for_timeout(1000)
            count, tickets = page.evaluate(SENT_JS)
            check(f"{tag}: one thank-you, one number",
                  count == 1 and len(tickets) == 1 and TICKET.match(tickets[0]) is not None, [count, tickets])
            draws = page.evaluate("window.__draws")
            check(f"{tag}: the second submit made no second ticket (the first one is the one shown)",
                  draws == 4 and tickets and tickets[0].endswith("-ABCD"), [draws, tickets])
            if not (reduced and how == "a double click"):
                # (With reduced motion the form is gone after the first click, so the second click
                # lands on the thank-you's plain paper and the browser itself moves focus to the page.)
                check(f"{tag}: focus is on the thank-you", page.evaluate("document.activeElement.id") == "sent-title")
            page.wait_for_timeout(1500)
            check(f"{tag}: the number holds still", page.evaluate(SENT_JS) == [count, tickets])
            context.close()


def no_script(browser):
    """Without script (or before it has loaded) the page has no form to send: Send would be a GET with
    the message in the address. It says how to write instead, with real links."""
    context = browser.new_context(viewport={"width": 1440, "height": 900}, java_script_enabled=False)
    page = context.new_page()
    page.goto(f"{BASE}/support", wait_until="networkidle", timeout=120000)
    page.wait_for_timeout(800)
    forms = page.locator("main form").count()
    check("form (no script): no form in the page", forms == 0, forms)
    line = page.locator("#write [data-fallback]")
    check("form (no script): the fallback line says how to write to us",
          line.count() == 1 and line.inner_text().strip() == "To write to us, email support@bighnow.com or call 800-919-2089.",
          line.count() and line.inner_text())
    links = line.locator("a").evaluate_all("els => els.map(a => [a.getAttribute('href'), a.textContent.trim()])") if line.count() else []
    check("form (no script): the email and the phone are real links",
          links == [["mailto:support@bighnow.com", "support@bighnow.com"], ["tel:+18009192089", "800-919-2089"]], links)
    page.keyboard.press("Enter")
    page.wait_for_timeout(300)
    check("form (no script): no query string ever appears", "?" not in page.url, page.url)
    context.close()


def forced_colors(browser):
    """Windows High Contrast (forced colors) throws away shadows, gradients and chip fills: the
    lines, the focus and the chosen chip must still show."""
    context = browser.new_context(viewport={"width": 1440, "height": 900}, forced_colors="active")
    page = context.new_page()
    page.goto(f"{BASE}/support", wait_until="networkidle", timeout=120000)
    page.evaluate("document.fonts.ready.then(() => true)")
    page.wait_for_timeout(1200)
    page.locator("#write").scroll_into_view_if_needed()
    check("form (forced colors): the page is in forced colors", page.evaluate("matchMedia('(forced-colors: active)').matches"))
    for field in ("#support-name", "#support-email", "#support-order", "#support-message"):
        line = page.evaluate(f"(() => {{ const s = getComputedStyle(document.querySelector('{field}')); return [s.borderBottomWidth, s.borderBottomStyle]; }})()")
        check(f"form (forced colors): {field} keeps its line (a bottom border)", float(line[0][:-2]) > 0 and line[1] != "none", line)
    for field in ("#support-name", "#support-message"):
        page.focus(field)
        ring = page.evaluate(f"(() => {{ const s = getComputedStyle(document.querySelector('{field}')); return [s.outlineWidth, s.outlineStyle]; }})()")
        check(f"form (forced colors): focus shows on {field} (an outline)", float(ring[0][:-2]) > 0 and ring[1] != "none", ring)
    page.locator("label", has_text="A return").click()
    chips = page.evaluate("""[...document.querySelectorAll('[data-topics] label')].map(l => { const s = getComputedStyle(l);
      return [s.borderTopWidth, s.borderTopColor, s.backgroundColor, s.color].join(' '); })""")
    check("form (forced colors): the chosen chip looks different from the others",
          chips[1] not in [c for i, c in enumerate(chips) if i != 1], chips)
    context.close()


GROUPS = [opening, motion, rhythm, questions, form]
ONLY = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--only=")), None)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--use-angle=d3d11"])
        for group in GROUPS:
            if ONLY is None or group.__name__ in ONLY:
                group(browser)
        browser.close()
    passed = sum(ok for _, ok in results)
    print(f"\n{passed}/{len(results)} passed")
    sys.exit(0 if passed == len(results) else 1)
