import type { ProductPage, ProductStudy } from "../product-types";
import { studies } from "./studies";
import { summaries } from "./summaries";

const turmerificSummary = summaries.find((item) => item.slug === "turmerific")!;

const P = "https://pubmed.ncbi.nlm.nih.gov/";

// Longvida studies that are not in the homepage's research list, each checked at PubMed on
// September 28, 2026 (abstracts read; the retracted SLCP mouse papers are left out on purpose).
// Doses are stated so a reader can compare them with Turmerific's serving. Drafts for Mo.
const longvidaStudies: ProductStudy[] = [
  {
    year: "2010",
    kind: "Human study",
    title: "Longvida curcumin in the blood",
    journal: "J Agric Food Chem",
    note: "Gota and colleagues measured curcumin in the blood of healthy volunteers after 650 mg of the Longvida form. After the same amount of ordinary curcumin extract, none was detected. It measured absorption, not health effects.",
    url: `${P}20092313/`,
  },
  {
    year: "2017",
    kind: "Human trial",
    title: "Longvida and blood vessel function",
    journal: "Aging",
    note: "39 healthy adults aged 45 to 74 took 2,000 mg of Longvida a day, or a placebo, for 12 weeks. Blood vessels widened more readily in the Longvida group. Twice Turmerific’s serving; a small study.",
    url: `${P}28070018/`,
  },
  {
    year: "2018",
    kind: "Human trial",
    title: "The same trial: movement and thinking",
    journal: "Nutr Healthy Aging",
    note: "In the same 39 adults, 12 weeks of Longvida did not change strength, balance, memory or processing speed. Shown on purpose, beside the studies that found changes.",
    url: `${P}29951592/`,
  },
  {
    year: "2020",
    kind: "Human trial",
    title: "A 12-week follow-up in older adults",
    journal: "Nutrients",
    note: "80 adults aged 50 to 80 took 400 mg of Longvida a day, or a placebo. After 12 weeks the Longvida group did better on working-memory tasks and reported less fatigue. Blood sugar was also higher in that group. A small study.",
    url: `${P}32512782/`,
  },
];

// Turmerific. Approved copy (BRAND-CHEATSHEET.md, September 21): the headline, the purpose (the
// homepage card's description). Never name the ingredient's maker, and
// never say UCLA developed, tested or endorsed Turmerific itself (Mo, September 21).
// Label facts: BiGH's own 2020 Turmerific label (supplement facts, suggested use, other
// ingredients, precaution and caution), read from bighnow.com on September 28; Mo confirmed on
// September 29 that it is still the current label. Mo approved every new line on September 29.
// A liver-safety answer (NCCIH, April 2025) was left out until Mo has researched it herself.
const turmerific: ProductPage = {
  ...turmerificSummary,
  eyebrow: "From turmeric root",
  headlineLines: ["Turmeric,", "advanced by neuroscience."],
  purpose:
    "Featuring Longvida® curcumin, developed with neuroscientists at the University of California, Los Angeles. Its specialized delivery system is designed to improve how your body absorbs turmeric’s active compound.",
  highlights: ["Longvida® curcumin", "Designed for absorption"],
  accent: "#e98b2a",
  serving: {
    capsules: 2,
    perBottle: 60,
    days: 30,
    use: "Take 1 to 2 capsules a day, or as your healthcare professional advises.",
    supply: "60 vegetarian capsules · 30 servings",
  },
  // Sources: NCCIH, "Turmeric" (updated April 2025): curcumin gives turmeric its colour; Nelson
  // et al., J Med Chem 2017: curcumin is poorly absorbed; Gota et al. 2010: solid lipid particles.
  // The picture, like the other products' (September 29): fresh turmeric roots cut open in the dark,
  // their golden flesh lit as you scroll. A Gemini render; prompt in
  // reference/product-pages/turmerific/originals/, made with scripts/product-pages/why_turmerific.py.
  why: {
    label: "Why the form matters",
    title: "A golden compound. A hard one to absorb.",
    lines: [
      "Curcumin is the compound that gives turmeric its golden colour.",
      "On its own, very little of it reaches your bloodstream.",
      "Longvida® carries curcumin in tiny particles of fat, designed to help your body absorb it.",
    ],
    visual: {
      src: "/images/products/turmerific/why-root-off.webp",
      width: 2752,
      height: 1536,
      alt: "Fresh turmeric roots, cut open, on a dark background",
      lit: { src: "/images/products/turmerific/why-root-on.webp", width: 2752, height: 1536 },
    },
    source:
      "Sources: NIH (NCCIH); Nelson and colleagues, J Med Chem 2017; Gota and colleagues, 2010.",
  },
  ingredients: [
    {
      key: "longvida",
      name: "Longvida® curcumin",
      form: "Longvida® Optimised Curcumin Extract (Curcuma longa) (rhizome)",
      amount: 1000,
      unit: "mg",
      role: "Curcumin from turmeric root, in a form designed to be absorbed. The amount is the weight of the whole extract, not of pure curcumin.",
    },
  ],
  otherIngredients:
    "Other ingredients: rice flour, vegetable oil powder, vegetable cellulose (capsule), sunflower lecithin, stearic acid, maltodextrin, ascorbyl palmitate (vitamin C) and silicon dioxide.",
  studies: [...studies(["25277322/", "28074653/"]), ...longvidaStudies],
  // No people chapter: no BiGH scientist is credited with Turmerific's formula.
  people: [],
  faq: [
    {
      question: "How do I take Turmerific?",
      answer: "Take 1 to 2 capsules a day, or as your healthcare professional advises.",
    },
    {
      question: "How long does one bottle last?",
      answer:
        "Each bottle holds 60 vegetarian capsules: 30 days at 2 capsules a day, or 60 days at 1.",
    },
    {
      question: "Is the 1,000 mg all curcumin?",
      answer:
        "No. 1,000 mg is the weight of the whole Longvida® extract in 2 capsules. Curcumin is one part of it.",
    },
    {
      question: "Has Turmerific itself been tested in a clinical trial?",
      answer:
        "The research we share is about Longvida®, the curcumin in Turmerific, not the finished product. Each study says who took part and how much they took.",
    },
    {
      question: "Can I take it with medicines, before surgery or during pregnancy?",
      answer:
        "Ask your doctor first. The label advises this especially if you are pregnant or nursing, have surgery planned, take medicines regularly or are under medical care.",
    },
  ],
  caution:
    "As with any supplement, ask your doctor before taking Turmerific, especially if you are pregnant or nursing, have surgery planned, take medicines regularly or are under medical care. Keep out of reach of children. Do not use if the seal under the cap is broken.",
  notes: {
    label: "Amount per serving of 2 capsules, as printed on the Turmerific label.",
    science:
      "This line describes the ingredient in general. Ingredient research does not establish the effects of the finished product.",
    research:
      "These studies are about Longvida®, the curcumin in Turmerific, not the finished product. Each one says who took part and how much they took.",
    fda: "These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease.",
  },
  related: ["nuricell", "green-bee-propolis", "advanced-opc", "nature-calm"],
};

export default turmerific;
