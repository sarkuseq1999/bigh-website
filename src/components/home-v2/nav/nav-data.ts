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

/** The Science page's four parts (the footer's Science column), each with an ink painting. */
export const navScience = [
  {
    label: "Our scientists",
    href: "/science#scientists",
    caption: "Good science. Real people.",
    image: { src: "/images/jiankang-liu.jpg", width: 512, height: 768, photo: true },
  },
  {
    label: "Cellular health",
    href: "/science#health",
    caption: "Tiny power plants.",
    image: { src: "/images/home-v2/ink/mito.webp", width: 0, height: 0, photo: false },
  },
  {
    label: "Research library",
    href: "/science#research",
    caption: "Curiosity, with references.",
    image: { src: "/images/home-v2/ink/story-reading-v2.webp", width: 0, height: 0, photo: false },
  },
  {
    label: "Ask BiGH Science",
    href: "/science#ask",
    caption: "Good questions deserve clear answers.",
    image: { src: "/images/home-v2/ink/inkstone-v2.webp", width: 0, height: 0, photo: false },
  },
] as const;

export const navScienceIntro = {
  title: "Make sense of the science.",
  link: "Explore the science",
  href: "/science",
};
