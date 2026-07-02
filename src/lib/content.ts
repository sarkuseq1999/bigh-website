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
