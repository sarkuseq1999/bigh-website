import { researchItems } from "@/components/home/research-data";
import type { ProductPage, ProductStudy, ProductSummary } from "./product-types";

// Short entries for all five products, from the homepage lineup (products-lineup.tsx).
export const summaries: ProductSummary[] = [
  {
    slug: "nuricell",
    name: "NuriCell",
    focus: "Cellular health & mental energy",
    headline: "Stay sharp. Live fully.",
    bottle: {
      src: "/images/products/nuricell.png",
      width: 1230,
      height: 1278,
      alt: "NuriCell bottle",
    },
    tint: "#edf5fc",
    ink: "#24578e",
  },
  {
    slug: "green-bee-propolis",
    name: "Green Bee Propolis",
    focus: "From Minas Gerais, Brazil",
    headline: "Distinctive green propolis from Minas Gerais, Brazil.",
    bottle: {
      src: "/images/products/green-bee-propolis.png",
      width: 1231,
      height: 1278,
      alt: "Green Bee Propolis bottle",
    },
    tint: "#f2f5e9",
    ink: "#58682e",
  },
  {
    slug: "advanced-opc",
    name: "Advanced OPC Formula",
    focus: "Plant-based antioxidants",
    headline: "Nature’s antioxidant power. Focused on your cells.",
    bottle: {
      src: "/images/products/advanced-opc.png",
      width: 1231,
      height: 1278,
      alt: "Advanced OPC Formula bottle",
    },
    tint: "#fcf0f1",
    ink: "#964758",
  },
  {
    slug: "turmerific",
    name: "Turmerific",
    focus: "Advanced curcumin",
    headline: "Turmeric, advanced by neuroscience.",
    bottle: {
      src: "/images/products/turmerific.png",
      width: 1230,
      height: 1278,
      alt: "Turmerific bottle",
    },
    tint: "#fff4e5",
    ink: "#956123",
  },
  {
    slug: "nature-calm",
    name: "Nature Calm",
    focus: "A cellular approach to everyday stress",
    headline: "Everyday stress. A cellular approach.",
    bottle: {
      src: "/images/products/nature-calm.png",
      width: 1230,
      height: 1278,
      alt: "Nature Calm bottle",
    },
    tint: "#eef6ed",
    ink: "#487249",
  },
];

function studies(urls: string[]): ProductStudy[] {
  return urls.map((url) => {
    const item = researchItems.find((entry) => entry.url.endsWith(url));
    if (!item) throw new Error(`Unknown study ${url}`);
    return {
      year: item.year,
      kind: item.category.split(" · ")[0],
      title: item.title,
      journal: item.journal,
      note: item.text,
      url: item.url,
    };
  });
}

const nuricellSummary = summaries[0];

// NuriCell. Approved copy (BRAND-CHEATSHEET.md): headline, purpose, highlights, credit, the "why"
// lines and Dr. Liu's section. Label facts: the 2019 label, confirmed current by Mo on
// September 24, 2026. The ingredient roles and the FAQ are drafts to workshop with Mo.
const nuricell: ProductPage = {
  ...nuricellSummary,
  eyebrow: "Our flagship formula",
  headlineLines: ["Stay sharp.", "Live fully."],
  purpose:
    "Our flagship supplement focuses on the health of your mitochondria—the tiny power plants that supply energy for your brain and body.",
  highlights: ["Mitochondrial health", "Mental energy"],
  credit: "Formulated by Dr. Jiankang Liu.",
  accent: "#eaa43a",
  serving: {
    capsules: 3,
    perBottle: 90,
    days: 30,
    use: "Take 3 capsules once a day, with or after a meal.",
    supply: "90 vegetarian capsules · 30-day supply",
  },
  // No photo moment: the coast photo is a homepage image (Mo, September 25).
  why: {
    label: "Why cellular health matters",
    title: "Tiny power plants. A big part of your health.",
    lines: [
      "Inside many of your body’s cells are mitochondria—tiny power plants that turn energy from food into a form your cells can use.",
      "That energy helps your brain think, your heart beat, and your muscles move.",
      "It’s one reason good health starts with your cells.",
    ],
    // The glass mitochondrion is a homepage image; a light bulb, off then on, made for this page.
    visual: {
      src: "/images/products/nuricell/why-bulb-off.webp",
      width: 2752,
      height: 1536,
      alt: "A glass light bulb on a dark background",
      lit: { src: "/images/products/nuricell/why-bulb-on.webp", width: 2752, height: 1536 },
    },
    facts: [
      { figure: 2, unit: "%", line: "Your brain is about 2% of your body’s weight." },
      { figure: 20, unit: "%", line: "Yet it uses about 20% of your body’s energy." },
    ],
    comparison: "About 20 watts, day and night. Like a light that never goes out.",
    source: "Brain energy figures: Raichle & Gusnard, PNAS 2002.",
  },
  ingredients: [
    {
      key: "alcar",
      name: "Acetyl-L-carnitine",
      form: "Acetyl-L-carnitine hydrochloride",
      amount: 400,
      unit: "mg",
      role: "A form of carnitine. Carnitine carries fats into your mitochondria, where they are turned into energy.",
    },
    {
      key: "creatine",
      name: "Creatine",
      form: "Creatine monohydrate",
      amount: 400,
      unit: "mg",
      role: "Helps your cells keep a quick reserve of energy.",
    },
    {
      key: "ala",
      name: "Alpha-lipoic acid",
      form: "Alpha-lipoic acid",
      amount: 200,
      unit: "mg",
      role: "Helps your mitochondria turn food into energy. It also works as an antioxidant.",
    },
    {
      key: "choline",
      name: "Choline",
      form: "Choline bitartrate",
      amount: 100,
      unit: "mg",
      role: "Your body uses it to make acetylcholine, a messenger between nerve cells.",
    },
  ],
  otherIngredients:
    "Other ingredients: rice flour, silicon dioxide and magnesium stearate. Capsule: hypromellose and titanium dioxide.",
  studies: studies([
    "11854529/",
    "11854487/",
    "17605107/",
    "29704637/",
    "19664690/",
    "12598816/",
    "12804452/",
  ]),
  people: [
    {
      name: "Dr. Jiankang Liu",
      title: "Chief Scientific Advisor, BiGH",
      photo: {
        src: "/images/jiankang-liu.jpg",
        width: 512,
        height: 768,
        alt: "Portrait of Dr. Jiankang Liu",
      },
      lines: [
        "Dr. Liu is an internationally recognized scientist in mitochondrial biology and aging. His research explores the connections between cellular energy, nutrition, and how we age.",
        "As BiGH’s Chief Scientific Advisor, he brings decades of scientific experience to our purpose: helping people stay sharp, stay active, and live fully.",
      ],
    },
  ],
  faq: [
    {
      question: "How do I take NuriCell?",
      answer: "Take 3 capsules once a day, with or after a meal.",
    },
    {
      question: "How long does one bottle last?",
      answer: "Each bottle holds 90 vegetarian capsules: a 30-day supply at 3 capsules a day.",
    },
    {
      question: "What is the capsule made of?",
      answer:
        "The capsule is vegetarian: hypromellose, with titanium dioxide for its white colour. The other ingredients are rice flour, silicon dioxide and magnesium stearate.",
    },
    {
      question: "Has NuriCell itself been tested in a clinical trial?",
      answer:
        "The research we share is about NuriCell’s ingredients, not the finished product. Each study says whether it was done in people or in animals.",
    },
    {
      question: "Can I take it with medicines or other supplements?",
      answer: "Ask your doctor first, especially if you have a health condition or take medicines.",
    },
    {
      question: "Can I take NuriCell during pregnancy?",
      answer: "No. The label advises not to take it if you are pregnant or breastfeeding.",
    },
  ],
  caution:
    "As with any supplement, ask your doctor before taking NuriCell, especially if you have a health condition. Do not take if pregnant or breastfeeding. Keep out of reach of children.",
  notes: {
    label: "Amounts per serving of 3 capsules, as printed on the NuriCell label.",
    science:
      "Each line describes what the nutrient does in the body in general. Ingredient research does not establish the effects of the finished product.",
    research:
      "These studies are about NuriCell’s ingredients, not the finished product. Each one says what kind of study it was.",
    fda: "These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease.",
  },
  signature: "capsule",
  // Drafts (September 28, 2026). Sources: Liu et al. and Hagen et al., PNAS 2002 (old-animal
  // studies: the pair "most effective" / "more than either compound alone"); acetyl-L-carnitine
  // as an acetyl donor for acetylcholine (review, Expert Rev Neurother 2013).
  synergy: {
    title: "Why these four work together",
    note: "How each nutrient works in the body in general, and what researchers have studied. Not a study of NuriCell itself.",
    links: [
      {
        from: "alcar",
        to: "ala",
        title: "Fuel in, energy out",
        line: "Acetyl-L-carnitine carries fuel into your mitochondria. Alpha-lipoic acid helps turn it into energy, and helps clear the wear that making energy leaves behind.",
        evidence:
          "In Dr. Liu’s 2002 animal studies, the two together did more than either one alone.",
      },
      {
        from: "ala",
        to: "creatine",
        title: "Energy on hand",
        line: "Creatine keeps some of that energy in reserve, ready for the moments your brain and muscles need it fast.",
      },
      {
        from: "choline",
        to: "alcar",
        title: "Two halves of a messenger",
        line: "Your body joins choline with an acetyl group, which acetyl-L-carnitine can supply, to make acetylcholine, a messenger between nerve cells.",
      },
    ],
  },
  related: ["green-bee-propolis", "advanced-opc", "turmerific", "nature-calm"],
};

const pages: Record<string, ProductPage> = { nuricell };

export const productSlugs = Object.keys(pages);

export function getProduct(slug: string): ProductPage | undefined {
  return pages[slug];
}

export function getSummary(slug: string): ProductSummary | undefined {
  return summaries.find((summary) => summary.slug === slug);
}
