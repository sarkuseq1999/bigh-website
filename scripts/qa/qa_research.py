"""QA for the research list: 36 sources, three filters with counts, show more, rows open, links safe."""
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3007"
LOCALES = sys.argv[2].split(",") if len(sys.argv) > 2 else ["", "kr"]
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + ("  [" + detail + "]" if detail else ""))


with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    for loc in LOCALES:
        for w, h, tag in ((1440, 900, "desk"), (390, 844, "phone")):
            page = b.new_page(viewport={"width": w, "height": h})
            problems = []
            page.on("pageerror", lambda e: problems.append("pageerror " + str(e)[:120]))
            page.on("console", lambda m: problems.append("console " + m.text[:120]) if m.type == "error" else None)
            page.goto(f"{BASE}/{loc}", wait_until="networkidle")
            page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
            page.evaluate("document.getElementById('research').scrollIntoView({block: 'start'})")
            page.wait_for_timeout(800)
            filters = page.locator("#research [aria-label] button")
            labels = filters.evaluate_all("els => els.map(e => e.textContent)")
            rows_default = page.locator("#research details").count()
            more = page.locator("#research button[aria-expanded]")
            more.click()
            page.wait_for_timeout(400)
            rows_all = page.locator("#research details").count()
            links_ok = page.evaluate("[...document.querySelectorAll('#research details a')].every(a => a.target === '_blank' && a.rel.includes('noreferrer') && a.href.startsWith('https://'))")
            # Each filter's count matches its rows.
            counts_ok = True
            per = {}
            for i in range(1, 4):
                filters.nth(i).click()
                page.wait_for_timeout(300)
                more_visible = page.locator("#research button[aria-expanded]").count()
                if more_visible:
                    page.locator("#research button[aria-expanded]").click()
                    page.wait_for_timeout(300)
                n = page.locator("#research details").count()
                shown = int("".join(ch for ch in labels[i] if ch.isdigit()))
                per[labels[i]] = (n, shown)
                counts_ok = counts_ok and n == shown
            # A row opens and shows its text and link.
            filters.nth(0).click()
            page.wait_for_timeout(300)
            page.locator("#research details").nth(2).locator("summary").click()
            page.wait_for_timeout(300)
            opened = page.locator("#research details[open]").count()
            text = page.locator("#research details[open] p").first.inner_text()
            overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            translated = loc == "" or not any(x in "".join(labels) for x in ("Science", "Ingredients", "Guides"))
            ok = (rows_default == 8 and rows_all == 36 and sum(v[0] for v in per.values()) == 36 and counts_ok
                  and links_ok and opened == 1 and len(text) > 20 and overflow == 0 and translated and not problems)
            check(f"{loc or 'en'}-{tag}: 8 rows then all 36, filters {per}, counts match, row opens, safe links, translated labels, no overflow/errors",
                  ok, f"default={rows_default} all={rows_all} links={links_ok} opened={opened} labels={labels} overflow={overflow} {problems[:2]}")
            page.close()
    b.close()
print(f"\n{sum(results)} passed, {len(results) - sum(results)} failed")
