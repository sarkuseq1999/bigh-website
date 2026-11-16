import type { MetadataRoute } from "next";
import { productSlugs } from "@/components/product/catalog";
import { LANGUAGES, SITE_URL, localized } from "@/lib/seo";

// Every page in every language, each listing its translations (hreflang).
const PATHS = [
  "/",
  "/about",
  "/science",
  "/support",
  ...productSlugs.map((slug) => `/products/${slug}`),
  "/privacy",
  "/terms",
  "/returns",
];

export default function sitemap(): MetadataRoute.Sitemap {
  return PATHS.flatMap((path) => {
    const languages = Object.fromEntries(
      LANGUAGES.map((language) => [
        language.hreflang,
        `${SITE_URL}${localized(language.locale, path)}`,
      ]),
    );
    return LANGUAGES.map((language) => ({
      url: `${SITE_URL}${localized(language.locale, path)}`,
      changeFrequency: "monthly" as const,
      priority: path === "/" ? 1 : path.startsWith("/products/") ? 0.9 : 0.6,
      alternates: { languages },
    }));
  });
}
