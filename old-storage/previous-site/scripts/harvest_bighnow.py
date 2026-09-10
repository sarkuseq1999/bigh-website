"""Harvest all content from the live (hacked) bighnow.com WordPress site.

Produces clean, spam-stripped content files the rebuild can consume:
  content/harvest/<locale>/<slug>.md   (frontmatter + markdown body)
  content/harvest/assets/<path>        (downloaded wp-content images)
  content/harvest/_manifest.json       (run summary: pages, images, spam removed, failures)

Spam pattern observed 2026-07-01: hidden <a> tags positioned off-screen
(e.g. style="position:absolute; left:-4741px") with gambling anchor text
("mega888") linking to free3d.org. We remove any off-screen-positioned link
plus anything matching known spam keywords, and log every removal for review.
"""

import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")

BASE = "https://bighnow.com"
REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "content" / "harvest"
ASSETS = OUT / "assets"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
}

LOCALES = ("cns", "kr", "jp", "hken", "vn")
SPAM_KEYWORDS = re.compile(
    r"mega888|918kiss|pussy888|xe88|joker123|casino|judi|slot\s*online|free3d\.org",
    re.I,
)
OFFSCREEN = re.compile(r"(left|top)\s*:\s*-\d{3,}px", re.I)

SKIP_PATTERNS = re.compile(
    r"wp-sitemap|/author/|/category/|/2019/|/hello-world|/wp-json|/feed|/under-construction"
)

session = requests.Session()
session.headers.update(HEADERS)


def fetch(url, binary=False, retries=2):
    for attempt in range(retries + 1):
        try:
            r = session.get(url, timeout=40)
            if r.status_code == 200:
                return r.content if binary else r.text
            if r.status_code in (301, 302, 404, 410):
                return None
        except requests.RequestException:
            if attempt == retries:
                return None
            time.sleep(2)
    return None


def sitemap_urls():
    urls = []
    root_xml = fetch(f"{BASE}/wp-sitemap.xml")
    if not root_xml:
        return urls
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    root = ElementTree.fromstring(root_xml.encode())
    submaps = [loc.text for loc in root.findall(".//sm:loc", ns)]
    for sub in submaps:
        if "users" in sub or "taxonomies" in sub:
            continue
        sub_xml = fetch(sub)
        if not sub_xml:
            continue
        sub_root = ElementTree.fromstring(sub_xml.encode())
        urls += [loc.text for loc in sub_root.findall(".//sm:loc", ns)]
    return urls


def classify(url):
    """Return (locale, slug) for a page URL."""
    path = urlparse(url).path.strip("/")
    if not path:
        return "en", "home"
    # locale home pages: /en /cns /kr /jp /hken /vn (+ the stray /vn-2)
    if path in ("en",):
        return "en", "home-en"
    if path in LOCALES:
        return path, "home"
    if path == "vn-2":
        return "vn", "home-2"
    for loc in LOCALES:
        if path.endswith(f"_{loc}"):
            return loc, path[: -(len(loc) + 1)]
    return "en", path


def strip_spam(soup):
    removed = []
    for a in soup.find_all("a"):
        style = a.get("style", "")
        text = a.get_text(" ", strip=True)
        href = a.get("href", "")
        if OFFSCREEN.search(style) or SPAM_KEYWORDS.search(text) or SPAM_KEYWORDS.search(href):
            removed.append({"text": text[:80], "href": href[:120]})
            a.decompose()
    # spam sometimes hides in other off-screen elements too
    for el in soup.find_all(style=OFFSCREEN):
        removed.append({"text": el.get_text(" ", strip=True)[:80], "href": el.get("href", "")[:120]})
        el.decompose()
    return removed


def real_src(img):
    for attr in ("data-src", "data-lazy-src", "src"):
        v = img.get(attr)
        if v and not v.startswith("data:"):
            return v
    return None


def extract(url, html, spam_log):
    soup = BeautifulSoup(html, "html.parser")
    for junk in soup.find_all(["script", "style", "noscript", "template"]):
        junk.decompose()
    removed = strip_spam(soup)
    if removed:
        spam_log[url] = removed

    title = soup.title.get_text(strip=True) if soup.title else ""
    meta = soup.find("meta", attrs={"name": "description"})
    description = meta["content"].strip() if meta and meta.get("content") else ""

    main = (
        soup.find("div", attrs={"data-elementor-type": "wp-page"})
        or soup.find("main")
        or soup.body
    )
    if main is None:
        return None

    # normalize lazy-loaded images to their real URL before conversion
    images = []
    for img in main.find_all("img"):
        src = real_src(img)
        if src:
            src = urljoin(url, src)
            img["src"] = src
            if "/wp-content/" in src:
                images.append(src)

    links = []
    for a in main.find_all("a", href=True):
        href = urljoin(url, a["href"])
        if not href.startswith(BASE):
            links.append({"text": a.get_text(" ", strip=True)[:80], "href": href})

    md = markdownify(str(main), heading_style="ATX", strip=["script", "style"])
    md = re.sub(r"\n{3,}", "\n\n", md).strip()

    return {
        "title": title,
        "description": description,
        "markdown": md,
        "images": sorted(set(images)),
        "external_links": links,
    }


def save_page(locale, slug, url, data):
    folder = OUT / locale
    folder.mkdir(parents=True, exist_ok=True)
    front = {
        "source_url": url,
        "locale": locale,
        "slug": slug,
        "title": data["title"],
        "description": data["description"],
        "images": data["images"],
        "external_links": data["external_links"],
    }
    body = "---\n" + json.dumps(front, ensure_ascii=False, indent=2) + "\n---\n\n" + data["markdown"] + "\n"
    (folder / f"{slug}.md").write_text(body, encoding="utf-8")


def download_images(all_images):
    ok, failed = 0, []
    for src in sorted(all_images):
        rel = urlparse(src).path.replace("/wp-content/", "").lstrip("/")
        dest = ASSETS / rel
        if dest.exists():
            ok += 1
            continue
        blob = fetch(src, binary=True)
        if blob is None:
            failed.append(src)
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(blob)
        ok += 1
        time.sleep(0.15)
    return ok, failed


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    urls = sitemap_urls()
    urls = sorted({u.rstrip("/") for u in urls if not SKIP_PATTERNS.search(u)})
    print(f"sitemap pages to harvest: {len(urls)}")

    spam_log, failures, harvested = {}, [], []
    all_images = set()

    for i, url in enumerate(urls, 1):
        html = fetch(url)
        if html is None:
            failures.append(url)
            print(f"  [{i}/{len(urls)}] FAIL {url}")
            continue
        data = extract(url, html, spam_log)
        if data is None:
            failures.append(url)
            continue
        locale, slug = classify(url)
        save_page(locale, slug, url, data)
        all_images.update(data["images"])
        harvested.append({"url": url, "locale": locale, "slug": slug, "chars": len(data["markdown"])})
        print(f"  [{i}/{len(urls)}] {locale:5s} {slug:30s} {len(data['markdown']):6d} chars, {len(data['images'])} imgs")
        time.sleep(0.4)

    print("downloading images...")
    img_ok, img_failed = download_images(all_images)

    manifest = {
        "harvested_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "pages_ok": len(harvested),
        "pages_failed": failures,
        "images_ok": img_ok,
        "images_failed": img_failed,
        "spam_removals": {u: v for u, v in spam_log.items()},
        "spam_pages_count": len(spam_log),
        "pages": harvested,
    }
    (OUT / "_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        f"DONE: {len(harvested)} pages, {img_ok} images, "
        f"{len(spam_log)} pages had spam stripped, {len(failures)} failures"
    )


if __name__ == "__main__":
    main()
