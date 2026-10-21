"""Menu bar concept mockups, laid over the real public demo pages.

The real header is hidden and a static mock of each concept is placed where it stands, using the
site's own fonts, paper, logo and painted strokes, plus the two new Codex strokes (served from
./assets under /__mock/). Usage: python -X utf8 mock.py [A B C] [--only home-top,...]
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://bigh-website-demo.vercel.app"
HERE = Path(__file__).parent
ASSETS = HERE / "assets"
OUT = HERE / "shots"
OUT.mkdir(exist_ok=True)

CHEV = (
    '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
)
GLOBE = (
    '<svg class="globe" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/>'
    '<path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>'
)
LOGO = (
    '<a class="logo"><span class="logo-crop"><img src="/images/brand/bigh-logo-black-green.png" '
    'alt="BiGH"></span></a>'
)

COMMON = """
header:has(#site-navigation), a[class*="skip"] { visibility: hidden !important; }
.mk, .mk * { box-sizing: border-box; }
.mk { position: fixed; inset: 0 0 auto 0; z-index: 2147483000; height: var(--h); color: #0c0b0a;
  font-family: Switzer, "DM Sans", Arial, sans-serif; pointer-events: none; }
.mk .ground { position: absolute; inset: 0 0 auto 0; height: calc(var(--h) + 22px); opacity: 0;
  background: #f8f3ea url("/images/home-v2/ink/paper.webp") 0 0 / 800px 800px;
  mask-image: linear-gradient(#000 calc(100% - 14px), transparent); }
.mk[data-settled] .ground { opacity: 1; }
.mk .logo { display: block; }
.mk .logo-crop { display: block; width: 100%; aspect-ratio: 1448 / 710; overflow: hidden; }
.mk .logo img { display: block; width: 100%; height: auto; }
.mk .chev { width: 14px; height: 14px; margin-left: 7px; flex: none; }
.mk .globe { width: 16px; height: 16px; margin-right: 9px; flex: none; }
.mk .w { position: relative; display: inline-flex; align-items: center; white-space: nowrap; }
.mk .here::after { content: ""; position: absolute; left: 0; width: 90%; bottom: -12px; height: 7px;
  background: #0c0b0a; opacity: 0.85;
  mask: url("/images/home-v2/nav/inscription/current-stroke.webp") 0 0 / 100% 100% no-repeat; }
.mk .rule { position: absolute; left: 50%; translate: -50% -50%; width: min(1300px, 100% - 32px);
  aspect-ratio: 3406 / 22; min-height: 5px; background: #141311; opacity: 0.8;
  mask: url("/images/home-v2/nav/inscription/rule-lifted.webp") 0 0 / 100% 100% no-repeat; }
.mk .pill { display: inline-flex; align-items: center; justify-content: center; height: 48px;
  padding: 0 22px; border: 1.5px solid #0c0b0a; border-radius: 999px; }
"""

# ---------------------------------------------------------------- A: signed with one brushstroke
A_CSS = """
.mk { --h: 106px; }
.mk[data-settled] { --h: 84px; }
.mk .bar { position: relative; height: 100%; max-width: 1300px; margin: 0 auto;
  display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;
  font-family: Ysabeau, Switzer, sans-serif; font-weight: 500; font-size: 23px; letter-spacing: 0.005em; }
.mk .side { display: flex; align-items: center; }
.mk .side.l { justify-content: space-between; padding-right: 44px; }
.mk .side.r { justify-content: space-between; padding-left: 44px; }
.mk .links { display: flex; gap: 42px; }
.mk .logo { width: 150px; }
.mk[data-settled] .logo { width: 112px; }
.mk .rule { top: calc(var(--h) - 4px); }
.mk .account { display: flex; align-items: center; gap: 26px; }
.mk .swash { position: relative; isolation: isolate; display: inline-flex; align-items: center; justify-content: center;
  height: 50px; padding: 0 30px 2px 22px; color: #f8f3ea; font-size: 21px; }
.mk .swash::before { content: ""; position: absolute; inset: 0 -6px 0 -4px; z-index: -1;
  background: #0c0b0a; mask: url("/__mock/swash.webp") 0 50% / 100% 100% no-repeat; }
.mk .hover { isolation: isolate; }
.mk .hover::before { content: ""; position: absolute; inset: -14px -22px; z-index: -1;
  background: #141311; opacity: 0.5;
  mask: url("/__mock/band.webp") 45% 50% / 340% 100% no-repeat,
    linear-gradient(90deg, transparent, #000 22%, #000 78%, transparent);
  mask-composite: intersect; }
@media (max-width: 700px) {
  .mk { --h: 76px; }
  .mk .bar { grid-template-columns: 1fr auto 1fr; padding: 0 16px; font-size: 21px; }
  .mk .logo { width: 112px; }
  .mk .side.l, .mk .side.r { padding: 0; }
  .mk .side.r { justify-content: flex-end; }
  .mk .rule { width: calc(100% - 24px); }
  .mk .swash { height: 46px; padding: 0 22px 2px 18px; font-size: 19px; }
}
"""


def a_html(current, settled, phone, hover):
    def word(name, chev=False):
        cls = "w" + (" here" if current == name else "") + (" hover" if hover == name else "")
        return f'<span class="{cls}">{name}{CHEV if chev else ""}</span>'

    if phone:
        return f"""<div class="mk" {'data-settled' if settled else ''}><span class="ground"></span>
<div class="bar"><div class="side l"><span class="swash">Menu</span></div>{LOGO}
<div class="side r"><span class="w">{GLOBE}EN{CHEV}</span></div></div><span class="rule"></span></div>"""
    return f"""<div class="mk" {'data-settled' if settled else ''}><span class="ground"></span>
<div class="bar">
 <div class="side l"><span class="w">{GLOBE}English{CHEV}</span>
  <span class="links">{word("Products", True)}{word("Science", True)}</span></div>
 {LOGO}
 <div class="side r"><span class="links">{word("About")}{word("Support")}</span>
  <span class="account"><span class="w">Log in</span><span class="swash">Sign up</span></span></div>
</div><span class="rule"></span></div>"""


# ---------------------------------------------------------------- B: title page (two lines)
B_CSS = """
.mk { --h: 184px; }
.mk[data-settled] { --h: 84px; }
.mk .top { position: relative; max-width: 1300px; margin: 0 auto; height: 112px;
  display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; font-size: 20px; font-weight: 450; }
.mk .top .r { display: flex; justify-content: flex-end; align-items: center; gap: 26px; }
.mk .logo { width: 184px; margin-top: 6px; }
.mk .rule { top: 120px; }
.mk .row { position: absolute; left: 0; right: 0; top: 128px; height: 52px; display: flex;
  justify-content: center; align-items: center; gap: 0; font-size: 22px; font-weight: 450; }
.mk .row .w { padding: 0 30px; }
.mk .row .dot { width: 26px; height: 6px; background: #141311; opacity: 0.7;
  mask: url("/images/home-v2/nav/inscription/current-stroke.webp") 0 50% / 100% 100% no-repeat; }
/* settled: today's one line */
.mk[data-settled] .top, .mk[data-settled] .row { display: none; }
.mk .one { display: none; }
.mk[data-settled] .one { position: relative; max-width: 1300px; margin: 0 auto; height: 100%;
  display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; font-size: 20px; font-weight: 450; }
.mk[data-settled] .rule { top: calc(var(--h) - 4px); }
.mk .one .l { display: flex; justify-content: space-between; padding-right: 40px; }
.mk .one .r { display: flex; justify-content: space-between; padding-left: 40px; align-items: center; }
.mk .one .links { display: flex; gap: 40px; }
.mk .one .logo { width: 110px; margin: 0; }
.mk .one .account { display: flex; gap: 26px; align-items: center; }
@media (max-width: 700px) {
  .mk { --h: 128px; }
  .mk .top { height: 74px; padding: 0 16px; font-size: 18px; }
  .mk .logo { width: 118px; margin-top: 4px; }
  .mk .rule { top: 80px; width: calc(100% - 24px); }
  .mk .row { top: 82px; height: 48px; font-size: 17px; }
  .mk .row .w { padding: 0 11px; }
  .mk .row .chev { width: 12px; height: 12px; margin-left: 4px; }
  .mk .row .dot { width: 14px; height: 4px; }
  .mk .ground { opacity: 1; }
}
"""


def b_html(current, settled, phone, hover):
    def word(name, chev=False):
        cls = "w" + (" here" if current == name else "")
        return f'<span class="{cls}">{name}{CHEV if chev else ""}</span>'

    dot = ''
    row = f'<div class="row">{word("Products", True)}{dot}{word("Science", True)}{dot}{word("About")}{dot}{word("Support")}</div>'
    if phone:
        top = f"""<div class="top"><span class="w">{GLOBE}EN</span>{LOGO}<div class="r"><span class="w">Log in</span></div></div>"""
        return f'<div class="mk"><span class="ground"></span>{top}<span class="rule"></span>{row}</div>'
    top = f"""<div class="top"><span class="w">{GLOBE}English{CHEV}</span>{LOGO}
<div class="r"><span class="w">Log in</span><span class="pill">Sign up</span></div></div>"""
    one = f"""<div class="one"><div class="l"><span class="w">{GLOBE}English{CHEV}</span>
<span class="links">{word("Products", True)}{word("Science", True)}</span></div>{LOGO}
<div class="r"><span class="links">{word("About")}{word("Support")}</span>
<span class="account"><span class="w">Log in</span><span class="pill">Sign up</span></span></div></div>"""
    return f"""<div class="mk" {'data-settled' if settled else ''}><span class="ground"></span>
{top}<span class="rule"></span>{row}{one}</div>"""


# ---------------------------------------------------------------- C: the bar is one brushstroke
C_CSS = """
.mk { --h: 112px; }
.mk[data-settled] { --h: 92px; }
.mk .band { position: absolute; top: 24px; height: 72px; left: calc(50% - 418px); width: 846px;
  background: #141311; opacity: 0.5;
  mask: url("/__mock/band.webp") 0 50% / 100% 100% no-repeat,
    linear-gradient(90deg, #000 80%, transparent);
  mask-composite: intersect; }
.mk[data-settled] .band { top: 12px; height: 66px; }
.mk .bar { position: relative; height: 100%; max-width: 1300px; margin: 0 auto; padding-top: 6px;
  display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; font-size: 20px; font-weight: 450; }
.mk[data-settled] .bar { padding-top: 0; }
.mk .side { display: flex; align-items: center; }
.mk .side.l { justify-content: space-between; padding-right: 42px; padding-left: 22px; }
.mk .side.r { justify-content: space-between; padding-left: 42px; }
.mk .links { display: flex; gap: 40px; }
.mk .logo { width: 152px; }
.mk[data-settled] .logo { width: 118px; }
.mk .account { display: flex; align-items: center; gap: 26px; }
@media (max-width: 700px) {
  .mk { --h: 84px; }
  .mk .band { top: 12px; height: 62px; left: -10px; width: calc(100% + 10px);
    mask-size: 190% 100%, 100% 100%; }
  .mk .ground { opacity: 1; }
  .mk .bar { padding: 4px 16px 0; font-size: 18px; }
  .mk .logo { width: 112px; }
  .mk .side.l, .mk .side.r { padding: 0; }
  .mk .side.r { justify-content: flex-end; }
}
"""


def c_html(current, settled, phone, hover):
    def word(name, chev=False):
        cls = "w" + (" here" if current == name else "")
        return f'<span class="{cls}">{name}{CHEV if chev else ""}</span>'

    if phone:
        return f"""<div class="mk"><span class="ground"></span><span class="band"></span>
<div class="bar"><div class="side l"><span class="w">Menu</span></div>{LOGO}
<div class="side r"><span class="w">{GLOBE}EN{CHEV}</span></div></div></div>"""
    return f"""<div class="mk" {'data-settled' if settled else ''}><span class="ground"></span><span class="band"></span>
<div class="bar">
 <div class="side l"><span class="w">{GLOBE}English{CHEV}</span>
  <span class="links">{word("Products", True)}{word("Science", True)}</span></div>
 {LOGO}
 <div class="side r"><span class="links">{word("About")}{word("Support")}</span>
  <span class="account"><span class="w">Log in</span><span class="pill">Sign up</span></span></div>
</div></div>"""


CONCEPTS = {
    "A": (A_CSS, a_html, 0, 0),
    "B": (B_CSS, b_html, 78, 52),
    "C": (C_CSS, c_html, 0, 0),
}

# name, path, scroll, phone, current, hover
SHOTS = [
    ("home-top", "/", 0, False, None, None),
    ("home-settled", "/", 1400, False, None, None),
    ("nuricell-top", "/products/nuricell", 0, False, "Products", None),
    ("home-hover", "/", 0, False, None, "Science"),
    ("phone-home", "/", 0, True, None, None),
]


def shoot(page, letter, name, path, scroll, phone, current, hover):
    css, html, shift_desk, shift_phone = CONCEPTS[letter]
    page.goto(BASE + path, wait_until="networkidle", timeout=90000)
    page.wait_for_timeout(3000)
    if scroll:
        page.mouse.wheel(0, scroll)
        page.wait_for_timeout(2200)
    shift = shift_phone if phone else shift_desk
    extra = f"main#main {{ margin-top: {shift}px; }}" if shift and not scroll else ""
    page.add_style_tag(content=COMMON + css + extra)
    page.evaluate(
        "(h) => document.body.insertAdjacentHTML('beforeend', h)",
        html(current, bool(scroll), phone, hover),
    )
    page.evaluate("() => document.fonts.ready")
    page.wait_for_timeout(2600 if extra else 700)
    page.screenshot(path=str(OUT / f"{letter}-{name}.png"))


def main():
    letters = [a for a in sys.argv[1:] if a in CONCEPTS] or list(CONCEPTS)
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    with sync_playwright() as p:
        browser = p.chromium.launch()
        desk = browser.new_page(viewport={"width": 1536, "height": 900})
        phone = browser.new_page(
            viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True
        )
        for page in (desk, phone):
            page.route(
                "**/__mock/**",
                lambda route: route.fulfill(path=str(ASSETS / route.request.url.split("/__mock/")[1])),
            )
        for letter in letters:
            for name, path, scroll, is_phone, current, hover in SHOTS:
                if only and name not in only:
                    continue
                if hover and letter != "A":
                    continue
                shoot(phone if is_phone else desk, letter, name, path, scroll, is_phone, current, hover)
                print(letter, name, flush=True)
        browser.close()


main()
