// Every word on the homepage, in one place, for the redesign looks (September 28, 2026).
// The words are the ones Mo accepted for the current homepage (BRAND-CHEATSHEET.md): the redesign
// changes the design and feel, not the content. Each string is looked up through copy(), so the
// existing translations keep working; a new string falls back to English until it is translated.

export { researchItems, researchTypes } from "@/components/home/research-data";
export { stories } from "@/components/home/stories-data";
export {
  articles as scienceArticles,
  facts as scienceFacts,
  images as scienceImages,
} from "@/components/home/science-data";

export const hero = {
  // "Good health starts with your cells." (chosen September 18). Split for layouts that break it.
  title: ["Good health", "starts with", "your cells."],
  text: "Developed by scientists with deep expertise in cellular health and aging, BiGH’s key formulas share one purpose: helping you stay sharp, stay active, and live fully.",
  primary: "Discover NuriCell",
  secondary: "Meet our scientists",
};

// Figures the About page already shows, with its sources (about-content.ts).
export const facts = [
  { value: "280+", label: "scientific papers by Dr. Liu" },
  { value: "2016", label: "BiGH founded in California" },
  { value: "20+ years", label: "NuriCell’s formula, unchanged" },
];

export const scientists = {
  eyebrow: "Our scientific roots",
  title: ["Good science.", "Real people."],
  intro: ["Meet the minds behind our curiosity", "about cellular health."],
  name: "Dr. Jiankang Liu",
  role: "Chief Scientific Advisor, BiGH",
  specialty: "Mitochondrial science & aging",
  kicker: "A lifetime of asking better questions",
  heading: "What happens inside our cells shapes the way we understand health.",
  text: "Dr. Jiankang Liu’s work explores mitochondria, oxidative stress, and aging. These connections help shape BiGH’s focus on cellular health and mental energy.",
  link: "Get to know Dr. Liu",
  portrait: { src: "/images/jiankang-liu.jpg", width: 512, height: 768 },
  iris: { name: "Dr. Iris Wang", text: "Part of BiGH’s scientific and formulation roots." },
  ask: {
    title: "Good questions deserve clear answers.",
    text: "Introducing Ask BiGH Science, a planned customer benefit.",
    link: "Discover Ask BiGH Science",
  },
};

export const cellular = {
  eyebrow: "Why cellular health matters",
  title: ["Tiny power plants.", "A big part of your health."],
  opening:
    "Inside many of your body’s cells are mitochondria—tiny power plants that turn energy from food into a form your cells can use.",
  explanation: "That energy helps your brain think, your heart beat, and your muscles move.",
  closing: "It’s one reason good health starts with your cells.",
  link: "Explore cellular health",
  caption: "Illustrative view",
};

export const productsIntro = {
  title: "Explore our products.",
  headline: "Find your starting point.",
  text: "Discover the science, ingredients, and purpose behind each BiGH product.",
};

// The five products in the lineup order, with the words Mo accepted (September 21–28).
// `index` matches the product dialog order in SiteDialogs.
export const products = [
  {
    index: 0,
    name: "NuriCell",
    image: "/images/products/nuricell.png",
    size: { width: 1230, height: 1278 },
    story: "/images/products/stories/nuricell-coast-v1.webp",
    focus: "Cellular health & mental energy",
    headline: "Stay sharp. Live fully.",
    description:
      "Our flagship supplement focuses on the health of your mitochondria—the tiny power plants that supply energy for your brain and body.",
    credit: "Formulated by Dr. Jiankang Liu.",
    highlights: ["Mitochondrial health", "Mental energy"],
    flagship: "BiGH’s flagship formula",
    tint: "#edf5fc",
    ink: "#24578e",
  },
  {
    index: 1,
    name: "Green Bee Propolis",
    image: "/images/products/green-bee-propolis.png",
    size: { width: 1230, height: 1278 },
    story: "/images/products/stories/propolis-v1.webp",
    focus: "From Minas Gerais, Brazil",
    headline: "Distinctive green propolis from Minas Gerais, Brazil.",
    description:
      "Brazilian green propolis, shaped by local plants and the bees that gather their resins.",
    credit:
      "Its characteristic compounds include artepillin C—one reason researchers study Brazilian green propolis for its antioxidant properties.",
    highlights: ["Minas Gerais, Brazil", "Distinctive plant compounds"],
    tint: "#f2f5e9",
    ink: "#58682e",
  },
  {
    index: 2,
    name: "Advanced OPC Formula",
    image: "/images/products/advanced-opc.png",
    size: { width: 1230, height: 1278 },
    story: "/images/products/stories/opc-v1.webp",
    focus: "Plant-based antioxidants",
    headline: "Nature’s antioxidant power. Focused on your cells.",
    description:
      "A diverse blend of concentrated plant extracts, bringing together antioxidant compounds from grape seeds, pine bark, and other botanical sources.",
    credit:
      "Designed to support your cells’ natural defenses against free radicals—unstable molecules that can damage cells.",
    highlights: ["Plant-based antioxidants", "Free-radical defenses"],
    tint: "#fcf0f1",
    ink: "#964758",
  },
  {
    index: 3,
    name: "Turmerific",
    image: "/images/products/turmerific.png",
    size: { width: 1230, height: 1278 },
    story: "/images/products/stories/turmeric-v1.webp",
    focus: "Advanced curcumin",
    headline: "Turmeric, advanced by neuroscience.",
    description:
      "Turmeric’s active compound, delivered as Longvida® curcumin with a specialized system designed to improve absorption.",
    credit:
      "Longvida® was developed with neuroscientists at the University of California, Los Angeles.",
    highlights: ["Longvida® curcumin", "Advanced delivery"],
    tint: "#fff4e5",
    ink: "#956123",
  },
  {
    index: 4,
    name: "Nature Calm",
    image: "/images/products/nature-calm.png",
    size: { width: 1230, height: 1278 },
    story: "/images/products/stories/calm-v1.webp",
    focus: "A cellular approach to everyday stress",
    headline: "Everyday stress. A cellular approach.",
    description:
      "A cellular approach to everyday stress, bringing nutrients involved in cellular energy and antioxidant defenses into one formula.",
    credit:
      "Developed by Dr. Jian Kang Liu and Dr. Iris Wang, drawing on their research into stress and cellular health.",
    highlights: ["Cellular energy", "Everyday stress"],
    tint: "#eef6ed",
    ink: "#487249",
  },
] as const;

export type HomeProduct = (typeof products)[number];

export const storiesIntro = {
  title: "In their own words.",
  text: "The routines, questions, and choices behind everyday wellbeing.",
  note: "Design draft — all testimonials and reviewer names below are fictional samples.",
  sample: "Fictional sample",
  photo: "Illustrative photo",
};

export const science = {
  title: "Make sense of the science.",
  text: "Explore cellular health, mental energy, and healthy aging—with explanations that make the science easier to understand.",
  button: "Explore the science",
  explainer: "Read a quick explainer",
  ageLabel: "Illustration, not a measurement",
  topics: ["Mitochondria", "Free radicals", "Aging cells"],
};

export const research = {
  eyebrow: "Follow the evidence",
  title: ["Curiosity,", "with references."],
  text: "Science is most useful when you can understand it. Explore the ideas behind our approach, and see what each source actually tells us.",
  showAll: "Show all sources",
  showFewer: "Show fewer",
  readSource: "Read original source",
  note: "Ingredient research and general science do not establish the effects of a finished BiGH product.",
};

export const purpose = {
  eyebrow: "Be in good health",
  title: ["Our purpose is simple.", "Help you live fully."],
  graphic: ["Small beginnings.", "Bigger possibilities."],
  lead: "We believe a fuller life starts with understanding what supports it.",
  body: [
    "Our mission is to support cellular health and mental energy. We bring scientific curiosity to our products, and clear explanations to the people who use them.",
    "From the first question to the details of a formula, we want you to feel informed.",
  ],
  links: { product: "Discover NuriCell", standards: "What matters to us" },
  standards: [
    {
      title: "Know what’s inside.",
      text: "Clear ingredient information and a thoughtful explanation of each formula.",
    },
    {
      title: "Ask how it’s made.",
      text: "Specific, documented information about sourcing and manufacturing.",
    },
    {
      title: "Keep asking questions.",
      text: "Research in context, honest answers, and room for what we’re still learning.",
    },
  ],
};

export const footer = {
  tagline: "Stay sharp. Live fully.",
  lines: ["Cellular health.", "Mental energy.", "Everyday possibilities."],
  note: "Educational content is for general information. Product details and packaging are subject to confirmation. Purchases and question submissions are not available in this preview. Lifestyle imagery is illustrative.",
};
