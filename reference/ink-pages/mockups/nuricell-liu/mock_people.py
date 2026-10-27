"""Mockups of NuriCell's chapter 5 (Dr. Liu) idea A, "Where it started: Berkeley", on the real page.

Injects the composed plates and the new words into the running site, then takes viewport
screenshots like a visitor (desktop 1440x900, phone 390x844), plus the current section for
comparison. Nothing in the repo changes.

Usage: python -X utf8 mock_people.py <base-url> <comp-dir> <out-dir>
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE, COMP, OUT = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True)

WORDS = """
<h2 id="chapter-people-title" class="{h2}">Dr. Jiankang Liu</h2>
<p class="{role}">Chief Scientific Advisor, BiGH</p>
<p class="mock-lead">At UC Berkeley, he studied two of NuriCell’s nutrients together.</p>
<p class="{text}">In Bruce Ames’s laboratory, his 2002 study gave acetyl-L-carnitine and
alpha-lipoic acid to older animals. Both are in NuriCell, which he formulated.</p>
<p class="mock-note">An animal study, not a test of NuriCell.</p>
"""

BASE_CSS = """
nextjs-portal { display: none !important; }
[data-chapter="people"] .mock-lead {
  margin: 22px 0 14px; max-width: 17em; color: var(--ink, #1d1b18);
  font-size: clamp(22px, 2vw, 30px); line-height: 1.28; text-wrap: balance;
}
[data-chapter="people"] .mock-note {
  margin: 14px 0 0; padding-left: 22px; color: var(--muted, #6b655c); font-size: 15px; line-height: 1.5;
}
"""

# A1: the portrait with the Berkeley hills behind his shoulders, in his own column (a little wider,
# running into the page's right margin).
A1_CSS = """
@media (min-width: 960px) {
  [data-chapter="people"] > div > figure {
    width: min(620px, calc((100svh - 190px) * 0.897)) !important;
    justify-self: end; margin-right: -40px !important;
  }
}
"""

# A2: one wide painting across the whole chapter (the bay and the bridge under the words' sky, him on
# the hill at the right); the words sit in the sky. Phones keep one column with their own crop.
A2_CSS = """
@media (min-width: 960px) {
  [data-chapter="people"] { position: relative; padding-block: 0 !important; }
  [data-chapter="people"] > div > figure { display: none !important; }
  [data-chapter="people"] > div { height: calc(100vw * 1444 / 2600); align-items: start !important; grid-template-columns: minmax(0, 6fr) minmax(0, 5fr) !important; }
  [data-chapter="people"] [data-words] { position: relative; z-index: 1; padding-top: 1.6vw; }
  [data-chapter="people"] .mock-wide {
    position: absolute; left: 0; top: 0; width: 100%; height: auto;
    mix-blend-mode: multiply; pointer-events: none;
  }
  [data-chapter="people"] .mock-wide-cap { position: absolute; right: 7.7%; bottom: 2%; z-index: 1; }
}
@media (max-width: 959px) {
  [data-chapter="people"] .mock-wide, [data-chapter="people"] .mock-wide-cap { display: none; }
  [data-chapter="people"] > div > figure { width: 100vw !important; max-width: none !important; margin-left: calc(50% - 50vw) !important; justify-self: start !important; }
  [data-chapter="people"] > div > figure figcaption { padding-right: 24px; }
}
"""


def route_mocks(page):
    def handle(route):
        name = route.request.url.rsplit("/", 1)[-1]
        route.fulfill(path=str(COMP / name), content_type="image/png")

    page.route("**/__mock/*.png", handle)


def settle(page, phone):
    page.goto(f"{BASE}/products/nuricell", wait_until="networkidle")
    page.wait_for_timeout(800)
    # Scroll down through the page like a visitor so lazy pictures and blooms run.
    page.evaluate(
        """async () => {
        const c = document.querySelector('[data-chapter="people"]');
        const end = c.offsetTop;
        for (let y = 0; y < end; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); }
    }"""
    )
    page.wait_for_timeout(600)


def frame(page, phone):
    """Scroll so the chapter sits like a visitor would stop on it."""
    page.evaluate(
        """(phone) => {
        const c = document.querySelector('[data-chapter="people"]');
        const r = c.getBoundingClientRect();
        const top = window.scrollY + r.top;
        if (phone) { window.scrollTo(0, top + 10); return; }
        const spread = c.firstElementChild.getBoundingClientRect();
        const mid = window.scrollY + spread.top + spread.height / 2;
        window.scrollTo(0, mid - (75 + (window.innerHeight - 75) / 2));  // centred under the menu bar
    }""",
        phone,
    )
    page.wait_for_timeout(3500)  # the painting's bloom and the bar's settle


def inject(page, variant, phone):
    page.evaluate(
        """([variant, phone, WORDS]) => {
        const c = document.querySelector('[data-chapter="people"]');
        const words = c.querySelector('[data-words]');
        const cls = (sel) => (words.querySelector(sel) || {}).className || '';
        const html = WORDS
          .replace('{label}', cls('p:nth-of-type(1)'))
          .replace('{h2}', cls('h2'))
          .replace('{role}', cls('p:nth-of-type(2)'))
          .replace('{text}', cls('p:nth-of-type(3)'));
        words.innerHTML = html;
        const fig = c.querySelector('figure');
        const img = fig.querySelector('img');
        const plate = variant === 'a1' ? 'liu-berkeley-a1.png'
          : phone ? 'liu-berkeley-a2-phone.png' : 'liu-berkeley-a2.png';
        const aspect = variant === 'a1' ? 1400 / 1560 : phone ? 1800 / 1540 : 2600 / 1444;
        img.removeAttribute('srcset'); img.removeAttribute('sizes');
        img.loading = 'eager';
        img.src = '/__mock/' + plate;
        fig.style.setProperty('--aspect', String(aspect));
        if (variant === 'a2') {
          const wide = document.createElement('img');
          wide.className = 'mock-wide'; wide.alt = '';
          wide.src = '/__mock/liu-berkeley-a2.png';
          c.appendChild(wide);
          const cap = fig.querySelector('figcaption').cloneNode(true);
          cap.classList.add('mock-wide-cap');
          c.appendChild(cap);
        }
    }""",
        [variant, phone, WORDS],
    )
    page.add_style_tag(content=BASE_CSS + (A1_CSS if variant == "a1" else A2_CSS))
    page.wait_for_function(
        """() => [...document.querySelectorAll('[data-chapter="people"] img')].every(i => i.complete && i.naturalWidth > 0)"""
    )


def run():
    with sync_playwright() as p:
        b = p.chromium.launch()
        for phone in (False, True):
            vp = {"width": 390, "height": 844} if phone else {"width": 1440, "height": 900}
            dsf = 2 if phone else 1
            tag = "phone" if phone else "desktop"
            for variant in ("now", "a1", "a2"):
                ctx = b.new_context(viewport=vp, device_scale_factor=dsf)
                page = ctx.new_page()
                route_mocks(page)
                settle(page, phone)
                if variant != "now":
                    inject(page, variant, phone)
                frame(page, phone)
                out = OUT / f"{variant}-{tag}.png"
                page.screenshot(path=str(out))
                if phone:  # the words under the picture too
                    page.evaluate("window.scrollBy(0, 560)")
                    page.wait_for_timeout(700)
                    page.screenshot(path=str(OUT / f"{variant}-{tag}-2.png"))
                print(out)
                ctx.close()
        b.close()


run()
