// The product page template (September 25, 2026). One layout serves every BiGH product; each
// product supplies this data, its own colours and photo, and optionally one signature moment.

export type Picture = { src: string; width: number; height: number; alt: string };

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
  lines: string[];
};

export type ProductSummary = {
  slug: string;
  name: string;
  focus: string;
  headline: string;
  bottle: Picture;
  tint: string;
  ink: string;
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
};

export type ProductPage = ProductSummary & {
  eyebrow: string;
  /** Headline broken into lines; the product picture may sit between them. */
  headlineLines: string[];
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
