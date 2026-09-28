import { Fraunces, Hanken_Grotesk } from "next/font/google";

// Look B ("Scroll film"), round 4 (Mo, September 28, 2026: the earlier type looked "vibe coded").
// Display: Fraunces, a variable serif with an optical-size axis (big sizes get the fine display
// cut on their own) and a SOFT axis that rounds its terminals; light weights, roman and italic.
// Text, labels, captions and buttons: Hanken Grotesk. CSS always falls back to the site's
// var(--font-instrument) / var(--font-dm-sans), so Korean, Chinese and Japanese keep their fonts.
export const filmDisplay = Fraunces({
  subsets: ["latin", "latin-ext", "vietnamese"],
  style: ["normal", "italic"],
  axes: ["SOFT", "opsz"],
  variable: "--font-film-display",
  display: "swap",
});

export const filmText = Hanken_Grotesk({
  subsets: ["latin", "latin-ext", "vietnamese"],
  variable: "--font-film-text",
  display: "swap",
});
