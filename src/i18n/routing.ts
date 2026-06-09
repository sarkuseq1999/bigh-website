import { defineRouting } from "next-intl/routing";

export const routing = defineRouting({
  locales: ["en", "zh", "ko", "es", "ja"],
  defaultLocale: "en",
  localePrefix: "always",
});

export type Locale = (typeof routing.locales)[number];
