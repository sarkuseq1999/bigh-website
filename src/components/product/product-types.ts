// The product page template (September 25, 2026). One layout serves every BiGH product; each
// product supplies this data, its own colours and photo, and optionally one signature moment.

export type Picture = { src: string; width: number; height: number; alt: string };

/** A painting from a page's build script: its paper divided out to white, so it multiplies onto the
 *  page's own paper; `gold` is its gold-leaf light mask, for the kit's glint. */
export type InkArt = { src: string; width: number; height: number; gold?: string };
export type InkPainting = InkArt & { alt: string };

/** A painting the real bottle stands inside: where it stands (its width, and its picture's bottom
 *  above the painting's, as fractions of the painting), and `front`, the painting's lowest band cut
 *  to the bottle's shape (white elsewhere, the painting's size), laid again in front of the bottle's
 *  foot, so it stands in the painting, not on top of it. */
export type InkScene = InkPainting & {
  bottle: { width: number; bottom: number };
  front: string;
};

/**
 * The product's paintings for its ink page (NuriCell, October 9, 2026; spec
 * docs/superpowers/specs/2026-10-09-nuricell-ink-design.md). A product with `ink` gets the ink page
 * (one painting per chapter, beside its words); the others keep the Chapters template.
 */
export type ProductInk = {
  /**
   * Why it matters: one painting unlit and lit, in register (its light comes on). With `spread`
   * (Green Bee Propolis, October 14, 2026), the lit painting is revealed outward from that point
   * (fractions of the painting) instead of cross-fading in: the gold runs along the hive's cracks.
   * With `soak` (Turmerific, October 16, 2026), it soaks in through a sprite of `frames` masks
   * stacked top to bottom, each a wider stretch of the gold (the last whole): one layer of the lit
   * painting per mask fades in after the one before, so the gold spreads into the paper in its own
   * ragged shape, as watercolour does.
   */
  why: {
    unlit: InkArt;
    lit: InkArt;
    alt: string;
    spread?: { x: number; y: number };
    soak?: { sprite: string; frames: number };
  };
  inside: InkPainting;
  research: InkPainting;
  /** How to take it: a picture of when, and the serving as a painted sum (its numbers and their
   *  centres). Without a sum (one capsule a day: "1 × 60 = 60" says nothing new), none is shown. */
  daily: {
    picture: InkPainting;
    sum?: InkArt & { numbers: readonly number[]; centres: readonly number[] };
  };
  /** The buy chapter: the real bottle on one brush stroke (NuriCell), or standing inside a painted
   *  scene (Green Bee Propolis, October 14, 2026: the bottle photo is never redrawn). */
  buy: { stroke: InkArt } | { scene: InkScene };
  /** The opening's "One bottle" card: a small painted picture beside the supply (decorative). */
  supply?: InkArt;
};

export type ProductIngredient = {
  key: string;
  /** Everyday name used in headings. */
  name: string;
  /** The exact form printed on the label. */
  form: string;
  /** Amount per serving, as printed on the label. */
  amount: number;
  unit: "mg" | "mcg" | "IU";
  /** Draft: what the nutrient does in the body in general. Never a claim about the product. */
  role?: string;
  /**
   * A small round photo of the plant or source, leading the ingredient's row (Mo, September 28,
   * 2026, for Advanced OPC's plants). Decorative: the name beside it says what it is. When any
   * ingredient has one, rows without keep the space so the names line up.
   */
  picture?: Omit<Picture, "alt">;
};

export type ProductStudy = {
  year: string;
  /** Plain kind of study, e.g. "Animal study" or "Review of trials". */
  kind: string;
  title: string;
  journal: string;
  note: string;
  url: string;
};

export type ProductPerson = {
  name: string;
  title: string;
  /** Only people who have agreed to a photograph have one; everyone else is text only. */
  photo?: Picture;
  /** A painting of the person, for the ink page (Dr. Liu, October 9, 2026: Mo's call). */
  painting?: InkPainting;
  /**
   * What the painting shows: the person (a portrait, captioned "Portrait painting"; the default)
   * or their work (Advanced OPC Formula, October 16, 2026: Dr. Wang has no photograph and her
   * face is never generated, so a mortar and pestle stands beside her words, captioned
   * "Illustration" like every other painting).
   */
  paintingOf?: "person" | "work";
  lines: string[];
};

export type ProductSummary = {
  slug: string;
  name: string;
  focus: string;
  headline: string;
  bottle: Picture;
  tint: string;
  /** The product's deep colour for small details. (Named inkColor, not ink: `ink` on a ProductPage
   *  holds the ink page's paintings, October 9, 2026.) */
  inkColor: string;
};

/** A big number that counts up on its own screen, with one plain line that says it in words. */
export type WhyFact = { figure: number; unit: string; line: string };

export type ProductWhy = {
  label: string;
  title: string;
  lines: string[];
  /**
   * A photo on a dark ground, made for this chapter: the chapter turns dark and the story plays
   * over it. `lit` is the same photo, framed identically, with its light on; the chapter switches
   * it on as you scroll (it shares the visual's description). Without a visual the chapter is a
   * quiet list on paper, and facts, comparison and source are not shown.
   */
  visual?: Picture & { lit?: Omit<Picture, "alt"> };
  /** Figures shown one per screen before the lines; a figure counts up from the one before. */
  facts?: WhyFact[];
  /** One familiar comparison after the figures. */
  comparison?: string;
  /** Where the figures come from, shown small at the foot of the chapter. */
  source?: string;
  /**
   * More photos for the night story, one per idea (Turmerific, October 2, 2026). Each takes over
   * from the moment `from` (0 is the first figure, comparison or line; the title is the last) with
   * a liquid wash drawn in WebGL. Framed like the visual, on the same night, subject at the same
   * point. With scenes, the visual's light comes on while the first moment is on screen, before
   * the first hand-over. `ripple` is a faint living ripple for liquid scenes (about 0.003).
   * The words carry the story, so the scenes are decorative to screen readers.
   */
  scenes?: (Omit<Picture, "alt"> & { from: number; ripple?: number })[];
};

export type ProductPage = ProductSummary & {
  eyebrow: string;
  /** Headline broken into lines; the product picture may sit between them. */
  headlineLines: string[];
  /**
   * Where the giant name parts round the bottle, when the automatic split looks lopsided.
   * Turmerific: "Turm | erific" sets two halves of nearly equal width (Mo, October 2, 2026).
   */
  nameHalves?: [string, string];
  /**
   * A short first word set small over the first half, as wide as it (Advanced OPC Formula, October
   * 16, 2026: "Advanced" over "OPC", then the bottle, then "Formula" at the same size as "OPC"; the
   * halves are "OPC" and "Formula"). Without it the name is its halves alone.
   */
  nameLead?: string;
  /**
   * The ink page's opening name as a lockup: one word large on the bottle's left, the rest stacked
   * smaller on its right, one word a line. Green Bee Propolis: "Green" | "Bee" over "Propolis" (Mo,
   * October 16, 2026, after NuriCell's "Nuri | Cell").
   */
  nameLockup?: { left: string; right: readonly string[] };
  purpose: string;
  highlights: string[];
  credit?: string;
  /** A warm accent used for light and small details. */
  accent: string;
  serving: { capsules: number; perBottle: number; days: number; use: string; supply: string };
  photo?: Picture & { line: string };
  /** Why the product exists, in the brand's plain words. */
  why?: ProductWhy;
  ingredients: ProductIngredient[];
  otherIngredients: string;
  studies: ProductStudy[];
  /** The research chapter's heading when "The research on the ingredients" is not true of every
   *  study (Nature Calm leads with its scientists' own research on stress). */
  researchTitle?: string;
  people: ProductPerson[];
  faq: { question: string; answer: string }[];
  caution: string;
  /** label: under amounts; science: under ingredient roles; research: leads the studies. */
  notes: { label: string; science: string; research: string; fda: string };
  /** The product's own moment inside the template. NuriCell: the capsule opens. */
  signature?: "capsule";
  /**
   * How the ingredients work together (Mo, September 28, 2026: "the most important part").
   * Each link joins two ingredients by key. Lines describe the nutrients in general and what
   * researchers studied; the note says so. Drafts until Mo approves them.
   */
  synergy?: ProductSynergy;
  related: string[];
  /** The product's paintings: with them the product gets the ink page. */
  ink?: ProductInk;
};

export type ProductSynergyLink = {
  from: string;
  to: string;
  title: string;
  line: string;
  /** A short, sourced research note, e.g. what a study of the pair found. */
  evidence?: string;
};

export type ProductSynergy = { title: string; note: string; links: ProductSynergyLink[] };

export type InkProduct = ProductPage & { ink: ProductInk };
