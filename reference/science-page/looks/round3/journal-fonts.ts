import { Newsreader, Schibsted_Grotesk } from "next/font/google";

// Look C, "Journal": Newsreader (variable weight and optical size, with italics) for display and
// body, Schibsted Grotesk for labels, captions, figure numbers and numerals in tables. The CSS
// falls back to var(--font-instrument) / var(--font-dm-sans), so Korean, Chinese and Japanese keep
// their system fonts.
export const newsreader = Newsreader({
  subsets: ["latin", "latin-ext", "vietnamese"],
  style: ["normal", "italic"],
  axes: ["opsz"],
  variable: "--font-newsreader",
  display: "swap",
});

export const schibsted = Schibsted_Grotesk({
  subsets: ["latin", "latin-ext"],
  variable: "--font-schibsted",
  display: "swap",
});
