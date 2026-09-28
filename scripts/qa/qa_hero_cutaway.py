"""Browser checks for the product page's opening ("Big name") and NuriCell's capsule cutaway.

Usage: python -X utf8 scripts/qa/qa_hero_cutaway.py [base] [--gpu]
Checks, at 1440×900 and 390×844, with and without reduced motion:
- the opening shows its headline below the site header, its 3D bottle arrives (or the flat
  photo stands in), and the page never scrolls sideways;
- the giant name stays clear of the bottle: on wide screens its halves part around a
  bottle-wide gap, between the eyebrow and the words below; on phones it ends above the bottle;
- the cutaway plays its beats in order: intro, the proportion note, each ingredient's amount,
  the labels on the parted layers, "one formula", and the serving line;
- reduced motion shows the still bar and legend instead;
- no console errors.
Screenshots land in scripts/qa/out/hero-cutaway/.
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = next((a for a in sys.argv[1:] if a.startswith("http")), "http://localhost:3007")
GPU = "--gpu" in sys.argv
OUT = Path(__file__).parent / "out" / "hero-cutaway"
OUT.mkdir(parents=True, exist_ok=True)
SIZES = {"desktop": (1440, 900), "phone": (390, 844)}
ARGS = (
    ["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"]
    if GPU
    else ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
)

results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))


def opacity(page, selector: str) -> float:
    return page.evaluate(
        """(selector) => { const e = document.querySelector(selector);
        return e ? parseFloat(getComputedStyle(e).opacity) : -1; }""",
        selector,
    )


with sync_playwright() as p:
    browser = p.chromium.launch(args=ARGS)
    for size_name, (w, h) in SIZES.items():
        for reduced in (False, True):
            tag = f"{size_name}{'-reduced' if reduced else ''}"
            ctx = browser.new_context(
                viewport={"width": w, "height": h},
                reduced_motion="reduce" if reduced else "no-preference",
            )
            page = ctx.new_page()
            errors: list[str] = []
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(f"{BASE}/products/nuricell", wait_until="networkidle")
            try:
                page.wait_for_selector(
                    "[data-chapter='overview'] [data-status='ready'], [data-chapter='overview'] [data-status='flat']",
                    timeout=15000,
                )
                arrived = True
            except Exception:  # noqa: BLE001
                arrived = False
            page.wait_for_timeout(3500)
            check(f"{tag} opening: bottle arrives", arrived)
            title = page.locator("h1").first
            text = title.inner_text().strip()
            check(f"{tag} opening: headline", "Stay sharp" in text and "Live fully" in text, text[:60])
            geometry = page.evaluate(
                """() => { const h1 = document.querySelector('h1').getBoundingClientRect();
                const head = document.querySelector('header').getBoundingClientRect();
                const hero = document.querySelector("[data-chapter='overview']");
                const box = (e) => { const r = e.getBoundingClientRect(); return { top: r.top, bottom: r.bottom, left: r.left, right: r.right }; };
                const halves = [...hero.querySelectorAll('[data-giant-half]')].map(box);
                return { h1Top: h1.top, headBottom: head.bottom, halves,
                  name: [...hero.querySelectorAll('[data-giant-half]')].map(e => e.textContent).join(''),
                  opacity: Math.min(...[...hero.querySelectorAll('[data-giant-half]')].map(e => +getComputedStyle(e).opacity)),
                  top: box(hero.querySelector('[data-name-top]')), foot: box(hero.querySelector('[data-name-foot]')),
                  stage: box(hero.querySelector('[data-status]')), hero: box(hero),
                  wide: document.documentElement.scrollWidth, inner: innerWidth }; }"""
            )
            check(
                f"{tag} opening: headline clear of the header",
                geometry["h1Top"] >= geometry["headBottom"] - 1,
                f"h1 top {geometry['h1Top']:.0f}, header bottom {geometry['headBottom']:.0f}",
            )
            check(f"{tag} opening: the whole name, fully shown", geometry["name"] == "NuriCell" and geometry["opacity"] > 0.95,
                  f"{geometry['name']} at {geometry['opacity']:.2f}")
            a, b = geometry["halves"]
            if w > 900:
                gap = b["left"] - a["right"]
                centre = (a["right"] + b["left"]) / 2
                section_h = geometry["hero"]["bottom"] - geometry["hero"]["top"]
                check(f"{tag} opening: the name parts around a bottle-wide gap",
                      gap >= 0.3 * section_h and abs(centre - w / 2) < w * 0.02,
                      f"gap {gap:.0f}px for a {section_h:.0f}px stage, centred at {centre:.0f} of {w}")
                check(f"{tag} opening: the name sits between the eyebrow and the words below",
                      a["top"] >= geometry["top"]["bottom"] + 10 and a["bottom"] <= geometry["foot"]["top"] - 20,
                      f"name {a['top']:.0f}–{a['bottom']:.0f}, eyebrow ends {geometry['top']['bottom']:.0f}, words start {geometry['foot']['top']:.0f}")
            else:
                bottle_top = geometry["stage"]["top"] + 0.44 * (geometry["stage"]["bottom"] - geometry["stage"]["top"])
                check(f"{tag} opening: the whole name ends above the bottle",
                      max(a["bottom"], b["bottom"]) <= bottle_top, f"name ends {a['bottom']:.0f}, bottle starts {bottle_top:.0f}")
            check(
                f"{tag} opening: no sideways scroll",
                geometry["wide"] <= geometry["inner"],
                f"{geometry['wide']} vs {geometry['inner']}",
            )
            page.screenshot(path=str(OUT / f"{tag}-opening.jpg"), type="jpeg", quality=78)
            check(f"{tag} opening: no console errors", not errors, "; ".join(errors[:3]))
            ctx.close()

            # The cutaway.
            ctx = browser.new_context(
                viewport={"width": w, "height": h},
                reduced_motion="reduce" if reduced else "no-preference",
            )
            page = ctx.new_page()
            errors = []
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(f"{BASE}/products/nuricell", wait_until="networkidle")
            page.wait_for_timeout(1500)
            section = "[aria-label='Inside the capsule']"
            if reduced:
                page.locator(section).scroll_into_view_if_needed()
                page.wait_for_timeout(600)
                bands = page.locator(f"{section} [class*='bar'] span").count()
                legend = page.locator(f"{section} ul[class*='legend'] > li").count()
                pairs = page.locator(f"{section} ol[class*='stillLinks'] > li").count()
                check(f"{tag} cutaway: still 'work together' pairs", pairs == 3, str(pairs))
                check(f"{tag} cutaway: still bar has 4 bands", bands == 4, str(bands))
                check(f"{tag} cutaway: still legend has 4 entries", legend == 4, str(legend))
                page.screenshot(path=str(OUT / f"{tag}-cutaway-still.jpg"), type="jpeg", quality=78)
            else:
                box = page.evaluate(
                    f"""() => {{ const s = document.querySelector("{section}");
                    const r = s.getBoundingClientRect(); return {{ top: r.top + scrollY, height: r.height }}; }}"""
                )
                length = box["height"] / h - 1
                page.wait_for_function(f"document.querySelector(\"{section}\").dataset.ready === 'true'", timeout=20000)

                def at(time: float, name: str) -> None:
                    y = box["top"] + (time / length) * (box["height"] - h)
                    page.evaluate(f"window.scrollTo(0, {y})")
                    page.wait_for_timeout(1700)
                    page.screenshot(path=str(OUT / f"{tag}-cutaway-{name}.jpg"), type="jpeg", quality=78)

                at(0.35, "intro")
                check(f"{tag} cutaway: intro shows", opacity(page, "[data-beat='intro']") > 0.9)
                at(0.9, "scan")
                check(f"{tag} cutaway: intro stays through the scan", opacity(page, "[data-beat='intro']") > 0.9)
                at(2.0, "open")
                check(f"{tag} cutaway: proportion note shows", opacity(page, "[data-beat='open']") > 0.9)
                at(2.75, "labels")
                label_opacity = page.evaluate(
                    """() => [...document.querySelectorAll("[aria-label='Inside the capsule'] [data-label]")]
                    .map(e => parseFloat(e.style.opacity || '0'))"""
                )
                check(
                    f"{tag} cutaway: labels on the parted layers",
                    len(label_opacity) == 4 and min(label_opacity) > 0.6,
                    str([round(v, 2) for v in label_opacity]),
                )
                # Labels stay inside the screen.
                inside = page.evaluate(
                    """() => [...document.querySelectorAll("[aria-label='Inside the capsule'] [data-label-text]")]
                    .every(e => { const r = e.getBoundingClientRect(); return r.left >= 0 && r.right <= innerWidth + 1; })"""
                )
                check(f"{tag} cutaway: labels inside the screen", inside and len(label_opacity) == 4)
                for index in range(4):
                    at(2.85 + index * 0.72 + 0.36, f"focus-{index}")
                    check(
                        f"{tag} cutaway: ingredient {index + 1} meets you",
                        opacity(page, f"[data-beat='focus-{index}']") > 0.9,
                    )
                # How the ingredients work together: the ring, then one pair per screen.
                at(6.1, "synergy")
                check(f"{tag} cutaway: 'work together' title", opacity(page, "[data-beat='synergy']") > 0.9)
                for index in range(3):
                    at(6.33 + index * 0.9 + 0.45, f"link-{index}")
                    check(
                        f"{tag} cutaway: pair {index + 1} explained",
                        opacity(page, f"[data-beat='link-{index}']") > 0.9,
                    )
                ring_labels = page.evaluate(
                    """() => [...document.querySelectorAll("[aria-label='Inside the capsule'] [data-label]")]
                    .filter(e => (e.dataset.side || '').startsWith('ring') && parseFloat(e.style.opacity || '0') > 0.6).length"""
                )
                check(f"{tag} cutaway: names beside the ring", ring_labels == 4, str(ring_labels))
                at(9.13 + 0.45, "together")
                check(f"{tag} cutaway: one formula", opacity(page, "[data-beat='together']") > 0.9)
                at(length - 0.2, "close")
                check(f"{tag} cutaway: serving line", opacity(page, "[data-beat='close']") > 0.9)
            check(f"{tag} cutaway: no console errors", not errors, "; ".join(errors[:3]))
            ctx.close()
    browser.close()

failed = [name for name, ok, _ in results if not ok]
print(f"\n{len(results) - len(failed)}/{len(results)} passed")
sys.exit(1 if failed else 0)
