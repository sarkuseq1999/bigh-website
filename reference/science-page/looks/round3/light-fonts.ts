import { Host_Grotesk } from "next/font/google";

// Look A's one typeface: Host Grotesk (variable, 300-800), for display and text alike. Latin only;
// Korean, Chinese and Japanese fall through to var(--font-dm-sans), which globals.css points at
// the right system fonts for each language.
export const hostGrotesk = Host_Grotesk({
  subsets: ["latin", "latin-ext"],
  display: "swap",
  variable: "--font-light",
});

// The full stack, for places outside the look's own root (the shared header, footer, story panel
// and research list read it through the theme tokens).
export const lightStack = `${hostGrotesk.style.fontFamily}, var(--font-dm-sans), Arial, sans-serif`;
