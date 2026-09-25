// "Make sense of the science." Mo accepted this copy on September 21, 2026 (BRAND-CHEATSHEET.md).
// The full articles are not written yet, so each article opens the short explainer dialog
// (Homepage's openArticle, same index order: mitochondria, free radicals, aging cells).
export const intro = {
  title: "Make sense of the science.",
  text: "Explore cellular health, mental energy, and healthy aging—with explanations that make the science easier to understand.",
  button: "Explore the science",
};

export const articles = [
  {
    id: "energy",
    topic: "Mitochondria",
    title: "What are mitochondria—and why do they matter?",
    preview:
      "A simple guide to your cells’ tiny power plants, their role in everyday energy, and what mitochondrial health means.",
  },
  {
    id: "balance",
    topic: "Free radicals",
    title: "What are free radicals—and how do antioxidants help?",
    preview:
      "A simple explanation of free radicals, the damage they can cause, and your cells’ natural defenses.",
  },
  {
    id: "aging",
    topic: "Aging cells",
    title: "What happens to your cells as you age?",
    preview:
      "A closer look at how cells change over time and what researchers are learning about healthy aging.",
  },
] as const;

// Short facts per topic, each a condensed line from the approved explainer or plain background
// science (mitochondria are a main source of free radicals; the body makes its own antioxidants).
export const facts = [
  ["Inside most of your cells", "Turn food into usable energy", "A small part with a big job"],
  [
    "Mitochondria are one of the main sources of free radicals",
    "Your body also makes its own antioxidants",
    "More antioxidants are not automatically better",
  ],
  [
    "Many processes change with age",
    "Mitochondria are one part of the story",
    "No single ingredient explains it all",
  ],
];

// GPT Image 2.5 originals and prompts: reference/science-section/originals/sci2-glass.png (the
// young cell), sci3-aged.png (the same cell rendered old, from the young one as a reference) and
// sci3-droplet.png (an antioxidant droplet of lime glass, on a transparent ground). The depth map
// is derived from the render's silhouette (a smooth dome) for the WebGL parallax.
const S = "/images/science";
export const images = {
  glass: { src: `${S}/glass-cell.webp`, width: 1920, height: 1086 },
  glassAged: `${S}/glass-cell-aged.webp`,
  glassDepth: `${S}/glass-cell-depth.png`,
  drop: `${S}/antioxidant.webp`,
};

export type ScienceDesignProps = {
  onOpenArticle: (index: number) => void;
  onAsk: () => void;
};
