// What the menu bar options (October 5, 2026) offer, in one place. Every string here already
// exists on the site (homepage, footer, product summaries), so the existing translations carry it.
// Mo asked for two or three menu bar designs that match the crane homepage; each option draws
// these same links in its own way, so the comparison is about the design, not the content.

import { summaries } from "@/components/product/products/summaries";

export type NavPanelId = "products" | "science";

/** The five products, in the lineup order, each with its own page. */
export const navProducts = summaries.map((product) => ({
  slug: product.slug,
  name: product.name,
  focus: product.focus,
  href: `/products/${product.slug}`,
  bottle: product.bottle,
}));

/** The products panel's own words (the homepage's products block). */
export const navProductsIntro = {
  title: "Explore our products.",
  headline: "Find your starting point.",
  all: "Discover the science, ingredients, and purpose behind each BiGH product.",
  allLink: "/#products",
};

/** The Science page's four parts (the footer's Science column), each with its picture and the
 *  link the site already uses for it. Dr. Liu's is his real photograph (a print, never
 *  multiplied); the others are ink paintings with their paper divided out. `plate` names how the
 *  picture is placed so the four stand at one weight (round 5). */
export const navScience = [
  {
    label: "Our scientists",
    href: "/science#scientists",
    caption: "Good science. Real people.",
    link: "Meet our scientists",
    image: { src: "/images/jiankang-liu.jpg", width: 512, height: 768, plate: "print" },
  },
  {
    label: "Cellular health",
    href: "/science#health",
    caption: "Tiny power plants.",
    link: "Explore cellular health",
    image: { src: "/images/home-v2/ink/mito.webp", width: 2000, height: 1493, plate: "cell" },
  },
  {
    label: "Research library",
    href: "/science#research",
    caption: "Curiosity, with references.",
    link: "Explore the research",
    // The homepage's reading still life, cut to its table group and given body
    // (reference/nav/make_science_plates.py).
    image: {
      src: "/images/home-v2/nav/inscription/reading-still-life.webp",
      width: 1696,
      height: 1100,
      plate: "reading",
    },
  },
  {
    label: "Ask BiGH Science",
    href: "/science#ask",
    caption: "Good questions deserve clear answers.",
    link: "Discover Ask BiGH Science",
    image: {
      src: "/images/home-v2/ink/inkstone-v2.webp",
      width: 1200,
      height: 896,
      plate: "inkstone",
    },
  },
] as const;

export const navScienceIntro = {
  link: "Explore the science",
  href: "/science",
};
