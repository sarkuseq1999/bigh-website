import fs from "node:fs";
import path from "node:path";

import type { NextConfig } from "next";
import createNextIntlPlugin from "next-intl/plugin";

const withNextIntl = createNextIntlPlugin("./src/i18n/request.ts");

// 301s from every legacy WordPress URL to its new home, generated from the
// harvest manifest so nothing is missed. Old scheme: /nuricell_kr, /kr, /en.
// New scheme: /kr/nuricell, /kr, / (en unprefixed).
function legacyRedirects() {
  const manifest = JSON.parse(
    fs.readFileSync(path.join(__dirname, "content", "harvest", "_manifest.json"), "utf-8"),
  ) as { pages: { url: string; locale: string; slug: string }[] };

  const rules: { source: string; destination: string; permanent: boolean }[] = [
    { source: "/en", destination: "/", permanent: true },
    { source: "/vn-2", destination: "/vn", permanent: true },
  ];
  for (const p of manifest.pages) {
    if (p.locale === "en" || p.slug.startsWith("home")) continue;
    rules.push({
      source: `/${p.slug}_${p.locale}`,
      destination: `/${p.locale}/${p.slug}`,
      permanent: true,
    });
  }
  return rules;
}

const nextConfig: NextConfig = {
  // Hide the floating dev-tools indicator; it reads as a mystery UI control
  // in design reviews and screenshots.
  devIndicators: false,
  async redirects() {
    return legacyRedirects();
  },
};

export default withNextIntl(nextConfig);
