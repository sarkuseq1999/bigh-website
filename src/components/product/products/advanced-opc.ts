import type { ProductPage } from "../product-types";
import { studies } from "./studies";
import { summaries } from "./summaries";

const opcSummary = summaries.find((item) => item.slug === "advanced-opc")!;

// Advanced OPC Formula (docs/advanced-opc-page.md). Approved copy (BRAND-CHEATSHEET.md, September
// 21, 2026): the headline, the purpose and "free radicals—unstable molecules that can damage cells"
// from the homepage card; "Making energy also makes a few free radicals", "Antioxidants keep them in
// balance" and "Your body also makes its own antioxidants" from the homepage's science section.
// Label facts: the 2019 label and usage card from the old site (old-storage/.../uploads/2019/04/
// sup_opc.png, ser_opc.png), NOT yet confirmed current by Mo. No formulation credit: still open
// (ask Mo). Everything else is a draft for Mo.
const advancedOpc: ProductPage = {
  ...opcSummary,
  // Short on purpose: on phones the eyebrow must fit one line above the giant name (360px wide).
  eyebrow: "From nature",
  headlineLines: ["Nature’s antioxidant power.", "Focused on your cells."],
  purpose:
    "A diverse blend of concentrated plant extracts, bringing together antioxidant compounds from grape seeds, pine bark, and other botanical sources.",
  highlights: ["Nine plant extracts", "Vegetarian capsules"],
  accent: "#d9785f",
  serving: {
    capsules: 2,
    perBottle: 120,
    days: 60,
    use: "Take 1 to 2 capsules once a day, with or after a meal.",
    supply: "120 vegetarian capsules · 60 servings",
  },
  // A still life of the plant sources (reference/product-pages/advanced-opc/originals/plants.jpeg).
  photo: {
    src: "/images/products/advanced-opc/plants.webp",
    width: 2752,
    height: 1536,
    alt: "Grapes, grape seeds, pine bark, bilberries, tea leaves, an orange slice and a marigold on pink linen",
    line: "Nine plant extracts. One formula.",
  },
  // The grapes, dark then lit: the light comes on with the antioxidants. Sources for the lines:
  // NCCIH "Antioxidant supplements: what you need to know" (cells make reactive oxygen substances
  // in normal activity; the body has its own defenses), MedlinePlus "Antioxidants" (fruits and
  // vegetables are rich sources), Cochrane 2020 (pine bark is rich in proanthocyanidins, which are
  // antioxidants) and NCCIH "Grape seed extract" (it contains proanthocyanidins).
  why: {
    label: "Why antioxidants matter",
    title: "A balance worth keeping.",
    lines: [
      "Making energy also makes a few free radicals—unstable molecules that can damage cells.",
      "Antioxidants keep them in balance. Your body makes its own, and plants are full of them.",
      "Grape seeds and pine bark are rich in OPCs, plant compounds that act as antioxidants.",
    ],
    visual: {
      src: "/images/products/advanced-opc/why-grapes-off.webp",
      width: 2752,
      height: 1536,
      alt: "A bunch of red grapes hanging in the dark",
      lit: { src: "/images/products/advanced-opc/why-grapes-on.webp", width: 2752, height: 1536 },
    },
    source: "Sources: NIH (NCCIH, MedlinePlus); Cochrane review of pine bark extract, 2020.",
  },
  // Plants first (Mo, September 21: vitamins C and E should not lead), then the vitamins and
  // selenium. Amounts, units and label forms exactly as printed.
  ingredients: [
    {
      key: "grape-seed",
      name: "Grape seed extract",
      form: "Grape seed extract (Vitis vinifera, 95% polyphenols)",
      amount: 25,
      unit: "mg",
      role: "Made from grape seeds, a rich source of OPCs.",
    },
    {
      key: "pine-bark",
      name: "Pine bark extract",
      form: "Pine bark (Pinus pinaster, 95% polyphenol)",
      amount: 25,
      unit: "mg",
      role: "From the bark of the maritime pine, also rich in OPCs.",
    },
    {
      key: "red-wine",
      name: "Red wine extract",
      form: "Red wine 10:1",
      amount: 25,
      unit: "mg",
      role: "The plant compounds of red wine, concentrated.",
    },
    {
      key: "bilberry",
      name: "Bilberry",
      form: "Bilberry (fruit) extract (Vaccinium myrtillus, 25% anthocyanosides)",
      amount: 25,
      unit: "mg",
      role: "A small dark berry that looks like a blueberry. Anthocyanins give it its deep colour.",
    },
    {
      key: "tea",
      name: "Tea blend",
      form: "Tea (leaf) extract blend from white tea 30%, green tea 45 and black tea 20% polyphenols, Camellia sinensis",
      amount: 40,
      unit: "mg",
      role: "White, green and black tea: three teas from the same plant, each with its own polyphenols.",
    },
    {
      key: "citrus",
      name: "Citrus bioflavonoids",
      form: "Citrus bioflavonoids (fruit) 25%",
      amount: 100,
      unit: "mg",
      role: "Flavonoids, a large family of plant compounds, from citrus fruit.",
    },
    {
      key: "noni",
      name: "Noni",
      form: "Noni concentrate (fruit) (Morinda citrifolia 5:1)",
      amount: 25,
      unit: "mg",
      role: "Concentrated from the fruit of noni, a small evergreen tree of the Pacific Islands and Southeast Asia.",
    },
    {
      key: "lutein",
      name: "Lutein",
      form: "Lutein (marigold petal extract 5% from flower)",
      amount: 3,
      unit: "mg",
      role: "A yellow plant pigment that collects in the retina, at the back of your eye.",
    },
    {
      key: "melilotus",
      name: "Sweet clover",
      form: "LymphaSelect (flower) (Melilotus officinalis extract)",
      amount: 20,
      unit: "mg",
      role: "An extract of sweet clover, a yellow-flowered plant of the pea family.",
    },
    {
      key: "vitamin-c",
      name: "Vitamin C",
      form: "Vitamin C (from ascorbic acid)",
      amount: 300,
      unit: "mg",
      role: "A water-soluble antioxidant. Your body also needs it to make collagen.",
    },
    {
      key: "vitamin-e",
      name: "Vitamin E",
      form: "Vitamin E (as d-alpha-tocopherol succinate, natural E)",
      amount: 20,
      unit: "IU",
      role: "A fat-soluble antioxidant. Antioxidants help protect cells from free radicals.",
    },
    {
      key: "gamma-tocopherol",
      name: "Gamma-tocopherol",
      form: "Gamma-tocopherol",
      amount: 5,
      unit: "mg",
      role: "Another natural form of vitamin E, the one most common in vegetable oils and American diets.",
    },
    {
      key: "selenium",
      name: "Selenium",
      form: "Selenium (as selenomethionine)",
      amount: 10,
      unit: "mcg",
      role: "A trace mineral your body needs to make DNA and to help protect cells.",
    },
  ],
  otherIngredients:
    "Other ingredients: rice flour, magnesium stearate and silica. Capsule: hydroxypropyl methylcellulose (HPMC).",
  studies: [
    ...studies(["21802563/", "20876405/", "37714962/"]),
    // Checked at PubMed on September 28, 2026 (abstracts read).
    {
      year: "2008",
      kind: "Human trial",
      title: "Pine bark extract and memory in older adults",
      journal: "J Psychopharmacol",
      note: "101 healthy adults aged 60 to 85 took pine bark extract or a placebo for three months. The extract group did better on working memory and showed less of a marker of oxidative damage. They took 150 mg a day, six times the pine bark in this formula.",
      url: "https://pubmed.ncbi.nlm.nih.gov/18701642/",
    },
    {
      year: "2020",
      kind: "Cochrane review",
      title: "Pine bark extract: what 27 trials can tell us",
      journal: "Cochrane",
      note: "A review of 27 trials in 1,641 people with ten long-term conditions. The trials were small and often poorly reported, so the authors could draw no firm conclusions. Shown for balance.",
      url: "https://pubmed.ncbi.nlm.nih.gov/32990945/",
    },
  ],
  people: [],
  faq: [
    {
      question: "What does OPC mean?",
      answer:
        "OPC stands for oligomeric proanthocyanidins: small chains of plant compounds found in grape seeds and pine bark. Both are in this formula.",
    },
    {
      question: "How do I take Advanced OPC Formula?",
      answer:
        "Take 1 to 2 capsules once a day, with or after a meal, or as your healthcare professional advises.",
    },
    {
      question: "How long does one bottle last?",
      answer:
        "Each bottle holds 120 vegetarian capsules: 60 days at 2 capsules a day, or longer if you take 1.",
    },
    {
      question: "What is the capsule made of?",
      answer:
        "The capsule is vegetarian: hydroxypropyl methylcellulose (HPMC). The other ingredients are rice flour, magnesium stearate and silica.",
    },
    {
      question: "Has Advanced OPC Formula itself been tested in a clinical trial?",
      answer:
        "The research we share is about its ingredients, not the finished product. Each study says whether it was done in people or in animals.",
    },
    {
      question: "Can I take it with medicines or other supplements?",
      answer:
        "Ask your doctor first, especially if you have a health condition, take medicines, or are pregnant or breastfeeding.",
    },
  ],
  caution:
    "As with any supplement, ask your doctor before taking Advanced OPC Formula, especially if you have a health condition, take medicines, or are pregnant or breastfeeding.",
  notes: {
    label: "Amounts per serving of 2 capsules, as printed on the Advanced OPC Formula label.",
    science:
      "Each line describes the ingredient in general. Ingredient research does not establish the effects of the finished product.",
    research:
      "These studies are about antioxidants and this formula’s ingredients, not the finished product. Each one says what kind of study it was.",
    fda: "These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease.",
  },
  related: ["nuricell", "green-bee-propolis", "turmerific", "nature-calm"],
};

export default advancedOpc;
