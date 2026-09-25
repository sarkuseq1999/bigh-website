// The About page's words. Mo locked them on September 25, 2026: opening line A, no changes.
// Facts Mo confirmed that day: the NuriCell formula is about 23 years old (shown as "20+" so it
// stays true without an exact start year; never name its earlier Asian brand), products are made
// in California by a GMP-certified maker, the 45-day refund is current policy, and Ask BiGH Science
// stays on the page before the service exists. BiGH was incorporated in California on 05/11/2016.
// All three looks render these same words; only the design differs.

// Mo liked A and B (Sept 25) and asked to try "an A look and then a B look": the "ab" mix starts
// light like A and dives into B's dark cell. C is parked: no longer in the switcher, still at ?look=c.
export const looks = [
  { id: "a", name: "Calm" },
  { id: "b", name: "Deep space" },
  { id: "ab", name: "A then B" },
] as const;

export type Look = "a" | "b" | "c" | "ab";

export function toLook(value: unknown): Look {
  return value === "b" || value === "c" || value === "ab" ? value : "a";
}

export const about = {
  hero: {
    label: "About BiGH",
    title: "Be in Good Health.",
    lead: "What our name stands for. What our work is for.",
  },
  purpose: {
    label: "Our purpose",
    lines: ["A full life has many parts.", "We focus on one you can’t see: your cells."],
    mission:
      "Our mission is to support cellular health and mental energy, helping people live life to the fullest.",
  },
  roots: {
    label: "Our scientific roots",
    title: "Our key formulas begin with scientists.",
    text: "Dr. Jian Kang Liu, our Chief Scientific Advisor, studies mitochondria and aging. With Dr. Iris Wang, he developed NuriCell and Nature Calm.",
    stat: { value: "280+", label: "scientific papers by Dr. Liu" },
    link: "Meet our scientists",
    // Dr. Iris Wang is named in words only: she asked for no photograph on the website.
    photo: { src: "/images/jiankang-liu.jpg", alt: "Dr. Jian Kang Liu" },
  },
  experience: {
    label: "Our experience",
    title: "Our flagship formula is older than BiGH.",
    stats: [
      { value: "2016", unit: "", label: "BiGH founded in California" },
      { value: "20+", unit: "years", label: "NuriCell’s formula, unchanged" },
    ],
  },
  promise: {
    label: "Our promise",
    title: "What you can count on.",
    items: [
      { title: "Made in California.", text: "By GMP-certified manufacturers." },
      {
        title: "Know where it comes from.",
        text: "Our green propolis comes only from Minas Gerais, Brazil.",
      },
      { title: "45 days to decide.", text: "Not right for you? Send it back for a refund." },
      { title: "Answers in your language.", text: "We reply in the language you write in." },
    ],
  },
  closing: {
    title: "Curious about the science?",
    text: "Ask BiGH Science. We help you explore the research, with guidance from the scientists we work with.",
    primary: "Ask BiGH Science",
    secondary: "Explore our products",
  },
} as const;

// Where the page's links lead while the Science page lives on its own branch. Point "scientists"
// at "/science" once that branch lands.
export const routes = {
  scientists: "/#scientists",
  products: "/#products",
} as const;

// Shared pictures, all already approved for the homepage.
export const media = {
  coast: "/images/life-in-full.png",
  cellStill: "/media/hero/deep-space-background-v1.png",
  cellVideo: "/media/hero/deep-space-motion-v2.mp4",
  cells: "/images/closing/space-cells.webp",
  mitochondrion: "/images/science/glass-cell.webp",
  nuricell: "/images/products/nuricell.png",
} as const;
