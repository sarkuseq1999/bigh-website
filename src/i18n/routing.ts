import { defineRouting } from "next-intl/routing";

// Keep existing URL codes. The selector offers five languages; /hken redirects to /cns.
// The layout maps URL codes to valid document language tags (ko, ja, zh-Hans, vi).
export const routing = defineRouting({
  locales: ["en", "kr", "jp", "cns", "hken", "vn"],
  defaultLocale: "en",
  localePrefix: "as-needed",
});

export type Locale = (typeof routing.locales)[number];
