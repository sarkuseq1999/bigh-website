import type { MetadataRoute } from "next";

import { routing } from "@/i18n/routing";
import { listSlugs } from "@/lib/content";

const BASE = "https://www.bighnow.com";

export default function sitemap(): MetadataRoute.Sitemap {
  const entries: MetadataRoute.Sitemap = [];
  for (const locale of routing.locales) {
    const prefix = locale === "en" ? "" : `/${locale}`;
    entries.push({ url: `${BASE}${prefix || "/"}`, changeFrequency: "weekly", priority: 1 });
    for (const slug of listSlugs(locale)) {
      entries.push({
        url: `${BASE}${prefix}/${slug}`,
        changeFrequency: "monthly",
        priority: 0.7,
      });
    }
  }
  return entries;
}
