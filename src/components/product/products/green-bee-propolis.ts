import type { ProductPage, ProductStudy } from "../product-types";
import { studies } from "./studies";
import { summaries } from "./summaries";

const propolisSummary = summaries.find((item) => item.slug === "green-bee-propolis")!;

const P = "https://pubmed.ncbi.nlm.nih.gov/";

// Studies checked on PubMed on September 29, 2026 (abstracts read; full text where free), beside
// the two propolis reviews from the homepage's checked list. Titles and notes are drafts for Mo.
const moreStudies: ProductStudy[] = [
  {
    year: "2004",
    kind: "Lab study",
    title: "Artepillin C comes from the shrub",
    journal: "J Agric Food Chem",
    note: "Found artepillin C in both green propolis and the resin of alecrim, the shrub bees gather it from. It was the most plentiful compound measured in each.",
    url: `${P}14995105/`,
  },
  {
    year: "2005",
    kind: "Field study",
    title: "Watching bees gather green propolis",
    journal: "Evid Based Complement Alternat Med",
    note: "In Minas Gerais, researchers watched bees snip resin from alecrim shoot tips and pack it on their legs, then found traces of the shrub in the propolis.",
    url: `${P}15841282/`,
  },
  {
    year: "2016",
    kind: "Human trial",
    title: "Antioxidant markers over 18 weeks",
    journal: "Int J Environ Res Public Health",
    note: "65 adults with type 2 diabetes took 900 mg of Brazilian green propolis a day, or none. Antioxidant markers in the blood improved; blood sugar did not change.",
    url: `${P}27187435/`,
  },
  {
    year: "2018",
    kind: "Human trial",
    title: "Two years in older adults",
    journal: "J Alzheimers Dis",
    note: "60 adults, average age 73, living at high altitude took Brazilian green propolis or a placebo for two years. Scores on a memory and thinking test held up better with propolis. One small study.",
    url: `${P}29630549/`,
  },
  {
    year: "2021",
    kind: "Human trial",
    title: "Artepillin C reaches the blood",
    journal: "J Sci Food Agric",
    note: "133 healthy adults took Brazilian green propolis or a placebo each day. Artepillin C showed up in the blood of almost everyone taking propolis, and of no one on placebo.",
    url: `${P}33543484/`,
  },
];

// Green Bee Propolis (September 29, 2026). Approved copy (BRAND-CHEATSHEET.md, September 21): the
// headline and the description. Everything else is a draft for Mo. Label facts (serving, amount,
// other ingredients, directions, caution): the 2019 label, from the old site's bottle pictures
// (old-storage/previous-site/.../2019/03/1140_1183_propolis_2-1.png and 3-1.png), confirmed
// current by Mo on September 29, 2026.
const greenBeePropolis: ProductPage = {
  ...propolisSummary,
  eyebrow: "Made by bees",
  // The full approved headline (Mo, September 29: "2B", over a shorter two-line draft).
  headlineLines: ["Distinctive green propolis", "from Minas Gerais, Brazil."],
  purpose:
    "Bees produce this green propolis from local plant resins. Its characteristic compounds include artepillin C—one reason researchers study Brazilian green propolis for its antioxidant properties.",
  highlights: ["Minas Gerais, Brazil", "Artepillin C"],
  // The range credit (BRAND-CHEATSHEET.md, September 28, as the Science page shows), placed under
  // Add to cart (Mo, October 2, 2026, with Turmerific's: "Propolis yes"). "Dr.\u00a0" keeps each
  // title on the same line as its name.
  credit:
    "Developed under the direction and guidance of Dr.\u00a0Jiankang Liu and Dr.\u00a0Iris Wang.",
  accent: "#d9a21b",
  serving: {
    capsules: 1,
    perBottle: 60,
    days: 60,
    use: "Take 1 capsule a day.",
    supply: "60 vegetarian capsules · 60-day supply",
  },
  // Drafts (September 29, 2026). Sources: resin gathering, Teixeira et al., Evid Based Complement
  // Alternat Med 2005 (bees in Minas Gerais took 7 minutes on average from starting to collect to
  // packing a resin load on the leg); hive use, Simone-Finstrom et al., Insects 2017 (bees line the
  // hive's walls with propolis and seal cracks); artepillin C in the shrub's resin, Park et al.,
  // J Agric Food Chem 2004. The picture is a render made for this chapter (see its sidecar in
  // reference/product-pages/green-bee-propolis/originals/).
  why: {
    label: "Why green propolis",
    title: "Gathered by bees, from one Brazilian shrub.",
    lines: [
      "Bees make propolis from the resin they gather from plants. They line their hive with it and seal its cracks.",
      "In Minas Gerais, they snip it from the shoot tips of one shrub, alecrim, and carry it home on their legs.",
      "That resin carries artepillin C, the compound green propolis is known for.",
    ],
    visual: {
      src: "/images/products/green-bee-propolis/why-bee-off.webp",
      width: 2752,
      height: 1536,
      alt: "A honeybee gathering resin at the green shoot tip of a shrub, on a dark background",
      lit: {
        src: "/images/products/green-bee-propolis/why-bee-on.webp",
        width: 2752,
        height: 1536,
      },
    },
    facts: [
      { figure: 7, unit: "", line: "Minutes, on average, for one bee to gather a load of resin." },
    ],
    source:
      "Sources: Teixeira et al. 2005 (Minas Gerais); Simone-Finstrom et al. 2017; Park et al. 2004.",
  },
  ingredients: [
    {
      key: "propolis",
      name: "Green propolis extract",
      form: "Green Bee Propolis Extract",
      amount: 200,
      unit: "mg",
      role: "Made by bees from the resin of alecrim, a shrub that grows in Minas Gerais. Its characteristic compound is artepillin C.",
    },
  ],
  // The 2019 label spells it "silicone dioxide"; the web page of that year listed a plain
  // hydroxypropyl methylcellulose capsule. The bottle's own panel is followed here.
  otherIngredients:
    "Other ingredients: rice flour, silicon dioxide and magnesium stearate. Capsule: hypromellose, titanium dioxide and yellow iron oxide.",
  studies: [...moreStudies, ...studies(["33152464/", "34444688/"])],
  people: [],
  faq: [
    {
      question: "How do I take Green Bee Propolis?",
      answer: "Take 1 capsule a day, or as your healthcare professional advises.",
    },
    {
      question: "How long does one bottle last?",
      answer: "Each bottle holds 60 vegetarian capsules: a 60-day supply at 1 capsule a day.",
    },
    {
      question: "What is the capsule made of?",
      answer:
        "The capsule is vegetarian: hypromellose, with titanium dioxide and yellow iron oxide for its colour. The other ingredients are rice flour, silicon dioxide and magnesium stearate.",
    },
    {
      question: "I’m allergic to bee products. Can I take it?",
      answer:
        "Propolis is made by bees. The label advises caution if you are allergic to bee products, so ask your doctor first.",
    },
    {
      question: "Has Green Bee Propolis itself been tested in a clinical trial?",
      answer:
        "The research we share is about Brazilian green propolis, not the finished product. Each study says what kind of study it was.",
    },
    {
      question: "Can I take it during pregnancy?",
      answer: "No. The label advises not to take it if you are pregnant or breastfeeding.",
    },
  ],
  caution:
    "As with any supplement, ask your doctor before taking Green Bee Propolis, especially if you have a health condition. Do not take if pregnant or breastfeeding. Use with caution if you are allergic to bee products. Keep out of reach of children.",
  notes: {
    label: "Amount per serving of 1 capsule, as printed on the Green Bee Propolis label.",
    science:
      "Each line describes what the ingredient does in general. Ingredient research does not establish the effects of the finished product.",
    research:
      "These studies are about propolis, not the finished product. Each one says what kind of study it was.",
    fda: "These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease.",
  },
  related: ["nuricell", "advanced-opc", "turmerific", "nature-calm"],
};

export default greenBeePropolis;
