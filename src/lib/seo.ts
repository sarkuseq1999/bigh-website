import type { Metadata } from "next";

// Search and sharing for every page (November 16, 2026, for launch). Two settings on Vercel:
//
//   SITE_INDEXING=on      lets search engines index the site (robots.txt, the robots meta tag).
//                         Leave it unset on the demo and previews: they stay out of search.
//   NEXT_PUBLIC_SITE_URL  the site's public address, used for canonical links, the sitemap and
//                         link previews. Rarely needed: it defaults to https://bighnow.com once
//                         indexing is on, and to the public demo before then (bighnow.com still
//                         serves the old site, so previews pointing there would show nothing).
//
// Turning indexing on is the one switch for launch day; nothing else changes.

export const INDEXABLE = process.env.SITE_INDEXING === "on";
export const SITE_URL = (
  process.env.NEXT_PUBLIC_SITE_URL ||
  (INDEXABLE ? "https://bighnow.com" : "https://bigh-website-demo.vercel.app")
).replace(/\/$/, "");

/** The five languages the site offers, with their hreflang and Open Graph tags. /hken redirects. */
export const LANGUAGES = [
  { locale: "en", hreflang: "en", og: "en_US" },
  { locale: "cns", hreflang: "zh-Hans", og: "zh_CN" },
  { locale: "kr", hreflang: "ko", og: "ko_KR" },
  { locale: "vn", hreflang: "vi", og: "vi_VN" },
  { locale: "jp", hreflang: "ja", og: "ja_JP" },
] as const;

/** A path in a locale: English has no prefix (localePrefix "as-needed"). */
export function localized(locale: string, path: string): string {
  if (locale === "en") return path;
  return path === "/" ? `/${locale}` : `/${locale}${path}`;
}

export const ROBOTS: Metadata["robots"] = INDEXABLE
  ? { index: true, follow: true }
  : { index: false, follow: false };

export const DEFAULT_IMAGE = { url: "/og/home-v1.jpg", width: 1200, height: 630, alt: "BiGH" };

/** Title, description, canonical and language links, and the link preview for one page. */
export function pageMetadata({
  locale,
  path,
  title,
  description,
  image = DEFAULT_IMAGE,
}: {
  locale: string;
  path: string;
  title: string;
  description: string;
  image?: { url: string; width: number; height: number; alt: string };
}): Metadata {
  const url = localized(locale, path);
  const languages: Record<string, string> = { "x-default": path };
  for (const language of LANGUAGES) languages[language.hreflang] = localized(language.locale, path);
  return {
    title,
    description,
    alternates: { canonical: url, languages },
    openGraph: {
      type: "website",
      siteName: "BiGH",
      title,
      description,
      url,
      locale: LANGUAGES.find((language) => language.locale === locale)?.og ?? "en_US",
      images: [image],
    },
    twitter: { card: "summary_large_image", title, description, images: [image.url] },
    robots: ROBOTS,
  };
}
