"""Click every Science link on the site and check where it lands.

The homepage, product page and About page link to the Science page, some to one of its
sections (/science#health). A section link passes only when that section's heading is on
screen after the page has settled (the handscroll is pinned, so a jump can land short).

October 14, 2026 (Science ink, Task 6): brought up to the site as it is. The menu's Science
links are now "Cellular health" and "Research library"; the ink homepage has no "Meet our
scientists" hero link (the menu's "Explore the science" leads to the page's top instead) and
its cell's link reads "Explore cellular health" (to /science#health), and its science block has an
"Explore the science" pill (to /science); the product page's
"Science" in the menu bar opens the drop-down (its "Explore the science" leads to the page).

Run with the dev server up: python scripts/qa/qa_science_links.py [base-url]
"""
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost:3008"
ARGS = ["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"]
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


def landed(page, section):
    """Where the section sits on screen after the jump (top edge in px), or None."""
    page.wait_for_url("**/science**", timeout=20000)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3500)
    if not section:
        return page.evaluate("scrollY")
    return page.evaluate(
        f"(() => {{ const s = document.getElementById('{section}'); if (!s) return null;"
        " return Math.round(s.getBoundingClientRect().top); })()"
    )


with sync_playwright() as p:
    browser = p.chromium.launch(args=ARGS)
    errors = []

    def fresh(path, width=1440, height=900):
        ctx = browser.new_context(viewport={"width": width, "height": height})
        page = ctx.new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(BASE + path, wait_until="networkidle")
        page.wait_for_timeout(1200)
        return ctx, page

    # Homepage header: Science menu, each of its four links.
    for label, section in (
        ("Our scientists", "scientists"),
        ("Cellular health", "health"),
        ("Research library", "research"),
        ("Ask BiGH Science", "ask"),
    ):
        ctx, page = fresh("/")
        page.get_by_role("button", name="Science", exact=True).first.click()
        page.wait_for_timeout(500)
        page.get_by_role("link", name=label).first.click()
        top = landed(page, section)
        check(
            f"home menu '{label}' -> /science#{section}",
            top is not None and -40 <= top <= 300 and page.url.endswith(f"/science#{section}"),
            f"url={page.url} sectionTop={top}",
        )
        ctx.close()

    # Homepage menu "Explore the science" -> the Science page, at its top.
    ctx, page = fresh("/")
    page.get_by_role("button", name="Science", exact=True).first.click()
    page.wait_for_timeout(500)
    page.get_by_role("link", name="Explore the science").first.click()
    y = landed(page, None)
    check("home menu 'Explore the science' -> /science top", page.url.endswith("/science") and y < 5, f"url={page.url} scrollY={y}")
    ctx.close()

    # Homepage "Explore the science" pill in the page's own science block (not the menu's link).
    ctx, page = fresh("/")
    pill = page.locator("main a[href$='/science']").filter(has_text="Explore the science").first
    pill.scroll_into_view_if_needed()
    page.wait_for_timeout(800)
    pill.click()
    y = landed(page, None)
    check("home pill 'Explore the science' -> /science top", page.url.endswith("/science") and y < 5, f"url={page.url} scrollY={y}")
    ctx.close()

    # Homepage "Explore cellular health" (beside the cell) -> /science#health.
    ctx, page = fresh("/")
    link = page.get_by_role("link", name="Explore cellular health").first
    link.scroll_into_view_if_needed()
    page.wait_for_timeout(800)
    link.click()
    top = landed(page, "health")
    check("home 'Explore cellular health' -> /science#health", top is not None and -40 <= top <= 300, f"url={page.url} sectionTop={top}")
    ctx.close()

    # Homepage footer "Cellular health" -> /science#health.
    ctx, page = fresh("/")
    footer_link = page.locator("footer").get_by_role("link", name="Cellular health", exact=True).first
    footer_link.scroll_into_view_if_needed()
    footer_link.click()
    top = landed(page, "health")
    check("home footer 'Cellular health' -> /science#health", top is not None and -40 <= top <= 300, f"url={page.url} sectionTop={top}")
    ctx.close()

    # Product page menu bar "Science" -> its drop-down's "Explore the science" -> /science top.
    ctx, page = fresh("/products/nuricell")
    page.locator("header").get_by_role("button", name="Science", exact=True).first.click()
    page.wait_for_timeout(500)
    page.get_by_role("link", name="Explore the science").first.click()
    y = landed(page, None)
    check("product menu 'Explore the science' -> /science top", page.url.endswith("/science") and y < 5, f"url={page.url} scrollY={y}")
    ctx.close()

    # Korean: the menu keeps the visitor's language.
    ctx, page = fresh("/kr")
    page.locator("a[href='/kr/science#health']").first.wait_for(state="attached")
    hrefs = page.eval_on_selector_all("a[href*='science']", "els => [...new Set(els.map(e => e.getAttribute('href')))]")
    check("Korean homepage links stay Korean", all(h.startswith("/kr/science") for h in hrefs), str(hrefs))
    ctx.close()

    # About page: every link to the scientists leads to the Science page.
    ctx, page = fresh("/about")
    hrefs = page.eval_on_selector_all("a[href*='scientists'], a[href*='science']", "els => [...new Set(els.map(e => e.getAttribute('href')))]")
    check("About's scientist links -> /science", bool(hrefs) and all(h.startswith("/science") for h in hrefs), str(hrefs))
    ctx.close()

    check("no page errors", not errors, "; ".join(errors[:3]))
    browser.close()

print(f"\n{sum(results)} passed, {len(results) - sum(results)} failed")
sys.exit(0 if all(results) else 1)
