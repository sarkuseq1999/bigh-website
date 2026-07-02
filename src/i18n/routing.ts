import { defineRouting } from "next-intl/routing";

// Locale codes mirror the legacy site's own suffixes (_kr, _jp, _cns, _hken, _vn)
// so harvested content, redirects, and URLs stay 1:1 traceable to the old site.
export const routing = defineRouting({
  locales: ["en", "kr", "jp", "cns", "hken", "vn"],
  defaultLocale: "en",
  localePrefix: "as-needed",
});

export type Locale = (typeof routing.locales)[number];
