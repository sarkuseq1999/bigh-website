import fs from "node:fs";
import path from "node:path";
import { marked } from "marked";

import { routing, type Locale } from "@/i18n/routing";

// Reads the spam-stripped clone of the legacy site harvested by
// scripts/harvest_bighnow.py. All lookups happen at build time (SSG).

const HARVEST = path.join(process.cwd(), "content", "harvest");

export interface PageFrontmatter {
  source_url: string;
  locale: Locale;
  slug: string;
  title: string;
  description: string;
  images: string[];
  external_links: { text: string; href: string }[];
}

export interface HarvestPage {
  front: PageFrontmatter;
  markdown: string;
}

// Legacy slugs that are routed specially and must not render as generic pages
const EXCLUDED_SLUGS = new Set(["home", "home-en", "home-2"]);

export function loadPage(locale: Locale, slug: string): HarvestPage | null {
  const file = path.join(HARVEST, locale, `${slug}.md`);
  if (!fs.existsSync(file)) return null;
  const raw = fs.readFileSync(file, "utf-8");
  const parts = raw.split("---");
  const front = JSON.parse(parts[1]) as PageFrontmatter;
  const markdown = parts.slice(2).join("---").trim();
  return { front, markdown };
}

export function loadHome(locale: Locale): HarvestPage | null {
  return loadPage(locale, locale === "en" ? "home-en" : "home");
}

export function listSlugs(locale: Locale): string[] {
  const dir = path.join(HARVEST, locale);
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".md"))
    .map((f) => f.replace(/\.md$/, ""))
    .filter((slug) => !EXCLUDED_SLUGS.has(slug));
}

export function localesWithSlug(slug: string): Locale[] {
  return routing.locales.filter((locale) =>
    fs.existsSync(path.join(HARVEST, locale, `${slug}.md`)),
  );
}

/** Rewrite a legacy asset URL to the locally served copy. */
export function localAsset(url: string): string {
  return url.replace(/^https?:\/\/(www\.)?bighnow\.com\/wp-content\//, "/original/");
}

/** Rewrite legacy internal links to the new URL scheme. */
export function localLink(href: string): string {
  const m = href.match(/^https?:\/\/(?:www\.)?bighnow\.com\/([^?#]*)/);
  if (!m) return href;
  let p = m[1].replace(/\/+$/, "");
  if (p === "" || p === "en") return "/";
  if (p === "vn-2") return "/vn";
  if ((routing.locales as readonly string[]).includes(p)) return `/${p}`;
  for (const loc of routing.locales) {
    if (loc !== "en" && p.endsWith(`_${loc}`)) {
      return `/${loc}/${p.slice(0, -(loc.length + 1))}`;
    }
  }
  return `/${p}`;
}

/** Render harvested markdown to HTML with all URLs rewritten locally. */
export function mdToHtml(markdown: string): string {
  const rewritten = markdown
    .replace(/https?:\/\/(www\.)?bighnow\.com\/wp-content\//g, "/original/")
    .replace(/\]\((https?:\/\/(?:www\.)?bighnow\.com\/[^)]*)\)/g, (_all, url) => `](${localLink(url)})`);
  return marked.parse(rewritten, { async: false });
}

/** Noise images that shouldn't render as page content. */
const IMAGE_NOISE = /shapedivider|buynow_web|Black-Logo|logo/i;

export function productImages(page: HarvestPage): string[] {
  return page.front.images.filter((u) => !IMAGE_NOISE.test(u)).map(localAsset);
}

export function buyLink(page: HarvestPage): string | null {
  const link = page.front.external_links.find((l) =>
    /office2office|imatrixoffice/i.test(l.href),
  );
  return link?.href ?? null;
}

/** First real heading of a page, for clean <title>/<h1> use. */
export function pageHeading(page: HarvestPage): string | null {
  const m = page.markdown.match(/^#{1,3}\s+(.+)$/m);
  return m ? m[1].replace(/[​]/g, "").trim() : null;
}

// ── structured product-page content ─────────────────────────────────────────
// The legacy product pages share one Elementor shape: intro → facts links →
// price → buy → gallery → "Key Ingredients" (h3 cards) → prose sections.
// Parsing is structural (not string-matched) so every locale works.

export interface ProductSection {
  title: string;
  paragraphs: string[];
  cards: { title: string; text: string; icon: string | null }[];
  images: string[];
}

export interface ProductContent {
  intro: string[];
  factsLinks: { label: string; href: string }[];
  price: string | null;
  sections: ProductSection[];
}

const MD_IMAGE = /!\[[^\]]*\]\([^)]*\)/g;
const MD_LINK = /\[([^\]]*)\]\(([^)]*)\)/g;

function cleanText(s: string): string {
  return s
    .replace(/\\([*_'".])/g, "$1") // unescape BEFORE stripping emphasis
    .replace(MD_IMAGE, "")
    .replace(MD_LINK, "$1")
    .replace(/\*\*?/g, "")
    .replace(/\\(?=\s|$)/g, "")
    .replace(/[​]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

/** Prose cleaner for product copy: links are buttons on these pages, so they
 * are deleted outright instead of collapsing to their text. */
function cleanProse(s: string): string {
  return cleanText(s.replace(MD_IMAGE, "").replace(/\[[^\]]*\]\([^)]*\)/g, ""));
}

/** True when a markdown block is only links/images (a button row, not prose). */
function isLinkOnlyBlock(s: string): boolean {
  const stripped = s
    .replace(MD_IMAGE, "")
    .replace(/\[[^\]]*\]\([^)]*\)/g, "")
    .replace(/[[\]!\\]/g, "")
    .trim();
  return stripped === "";
}

export function parseProduct(page: HarvestPage): ProductContent {
  const md = page.markdown;

  // facts/serving sheet links: markdown links with text pointing at an uploads image
  const factsLinks: { label: string; href: string }[] = [];
  for (const m of md.matchAll(/(?<!!)\[([^\]]+)\]\((https?:\/\/(?:www\.)?bighnow\.com\/wp-content\/[^)]+\.(?:png|jpe?g))\)/g)) {
    const label = cleanText(m[1]);
    if (
      label &&
      !label.includes("![") &&
      !/^\$/.test(label) &&
      !/buynow|purchase|1140_|shapedivider/i.test(m[1] + m[2])
    ) {
      factsLinks.push({ label, href: localAsset(m[2]) });
    }
  }

  // split into h2 sections
  const rawParts = md.split(/^##\s+/m);
  let price: string | null = null;
  const intro: string[] = [];
  const sections: ProductSection[] = [];

  rawParts.forEach((part, idx) => {
    if (idx === 0) return; // preamble before the product-name heading
    const lines = part.split("\n");
    const title = cleanText(lines[0]);
    const body = lines.slice(1).join("\n");

    if (/^\$/.test(title)) {
      price = title;
      return;
    }
    if (idx === 1) {
      // first section = product name; its prose paragraphs are the intro
      // (button/link rows and images are rendered separately, not as prose)
      for (const p of body.split(/\n{2,}/)) {
        if (isLinkOnlyBlock(p)) continue;
        const t = cleanProse(p);
        if (t) intro.push(t);
      }
      return;
    }

    const cards: { title: string; text: string; icon: string | null }[] = [];
    const paragraphs: string[] = [];
    const subParts = body.split(/^###\s+/m);
    const blockImages = (block: string): string[] =>
      [...block.matchAll(/!\[[^\]]*\]\((https?:\/\/(?:www\.)?bighnow\.com\/wp-content\/[^)]+)\)/g)]
        .filter((m) => !/1140_|final6|buynow|shapedivider|sup_|ser_|Supplement|Suggested|Serving/i.test(m[1]))
        .map((m) => localAsset(m[1]));

    // In the legacy markup each ingredient icon appears BEFORE its ### heading,
    // i.e. the icon for card N sits at the end of block N-1 (or the section
    // preamble for the first card).
    const preambleImages = blockImages(subParts[0]);
    let pendingIcon: string | null =
      subParts.length > 1 ? (preambleImages.pop() ?? null) : null;
    // remaining preamble images are real section content (e.g. Reishi photo)
    const images: string[] = [];
    for (const p of preambleImages) {
      if (!images.includes(p)) images.push(p);
    }
    for (const p of subParts[0].split(/\n{2,}/)) {
      if (isLinkOnlyBlock(p)) continue;
      const t = cleanProse(p);
      if (t) paragraphs.push(t);
    }
    for (const sub of subParts.slice(1)) {
      const subLines = sub.split("\n");
      const subTitle = cleanText(subLines[0]);
      const subBody = subLines.slice(1).join("\n");
      const subText = cleanProse(subBody);
      if (subTitle) {
        cards.push({ title: subTitle, text: subText, icon: pendingIcon });
      }
      // an image at the end of this block is the NEXT card's icon
      pendingIcon = blockImages(subBody).pop() ?? null;
    }
    if (title || paragraphs.length || cards.length || images.length) {
      sections.push({ title, paragraphs, cards, images });
    }
  });

  return { intro, factsLinks, price, sections };
}
