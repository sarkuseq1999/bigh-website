import type { NextConfig } from "next";
import createNextIntlPlugin from "next-intl/plugin";

const withNextIntl = createNextIntlPlugin("./src/i18n/request.ts");

const nextConfig: NextConfig = {
  // Hide the floating dev-tools indicator; it reads as a mystery UI control
  // in design reviews and screenshots.
  devIndicators: false,
};

export default withNextIntl(nextConfig);
