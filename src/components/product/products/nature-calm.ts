import type { ProductPage, ProductStudy } from "../product-types";
import { studies } from "./studies";
import { summaries } from "./summaries";

const natureCalmSummary = summaries.find((item) => item.slug === "nature-calm")!;

const P = "https://pubmed.ncbi.nlm.nih.gov/";

// Studies that are not on the homepage's research list, checked on PubMed on September 28, 2026:
// Dr. Liu and Dr. Wang's own stress research (1994, 1996), Dr. Liu's review (1999), the
// N-acetylcysteine review, and the L-theanine trial with the dose it used (200 mg a day against
// Nature Calm's 100 mg). The phosphatidylserine trial on the homepage list is left out on purpose:
// it used 100–300 mg a day, and Nature Calm has 10 mg.
const ownStudies: ProductStudy[] = [
  {
    year: "1994",
    kind: "Animal study",
    title: "Stress and the body’s antioxidant defenses",
    journal: "Int J Biochem",
    note: "Dr.\u00a0Liu and Dr.\u00a0Wang found that stress lowered antioxidant defenses in the blood, and that glutathione, one of the body’s own antioxidants, lessened the change. An animal study, not a human trial.",
    url: `${P}8013736/`,
  },
  {
    year: "1996",
    kind: "Animal study",
    title: "Stress and oxidative damage in the brain",
    journal: "FASEB J",
    note: "Dr.\u00a0Liu, Dr.\u00a0Wang and colleagues found that stress raised oxidative damage to fats, proteins and DNA in the brain. The rise was larger inside the mitochondria than outside them. An animal study, not a human trial.",
    url: `${P}8940299/`,
  },
  {
    year: "1999",
    kind: "Review",
    title: "Stress, aging and oxidative damage",
    journal: "Neurochem Res",
    note: "Dr.\u00a0Liu proposes that when stress hormones, brain messengers and oxidants fall out of balance, oxidative damage can build up and add to aging. An idea drawn from earlier studies, not a trial.",
    url: `${P}10555789/`,
  },
  {
    year: "2014",
    kind: "Review",
    title: "How N-acetylcysteine works",
    journal: "Pharmacol Ther",
    note: "N-acetylcysteine’s main role is to help cells make glutathione. The review concludes it helps most where glutathione runs low, not as a strong antioxidant on its own.",
    url: `${P}24080471/`,
  },
  {
    year: "2019",
    kind: "Human trial",
    title: "L-theanine and everyday stress",
    journal: "Nutrients",
    note: "Thirty healthy adults took L-theanine for four weeks and reported fewer stress-related symptoms than on placebo. Small and short. The trial used 200 mg a day; Nature Calm has 100 mg per serving.",
    url: `${P}31623400/`,
  },
];

// Nature Calm. Approved copy (BRAND-CHEATSHEET.md, September 21 and 25, 2026): the headline, the
// purpose line, the credit and the focus. Label facts: the 2019 label saved from the old site
// (old-storage/.../2019/04/sup_nature.png and ser_nature.png), confirmed current by Mo on
// September 28, 2026. Everything else (the "why" lines, the ingredient roles, Dr. Wang's lines,
// the research heading, the FAQ and the study notes above) is a draft for Mo.
const natureCalm: ProductPage = {
  ...natureCalmSummary,
  eyebrow: "For life’s demanding days",
  headlineLines: ["Everyday stress.", "A cellular approach."],
  purpose:
    "Nature Calm brings together nutrients involved in cellular energy and antioxidant defenses, with everyday stress in mind.",
  highlights: ["Cellular energy", "Everyday stress"],
  credit: "Developed by Dr. Jiankang Liu and Dr. Iris Wang.",
  accent: "#eaa43a",
  serving: {
    capsules: 3,
    perBottle: 90,
    days: 30,
    use: "Take 3 capsules once a day, with or after a meal.",
    supply: "90 vegetarian capsules · 30-day supply",
  },
  // "Dr.\u00a0" (a no-break space) keeps a title on the same line as the name.
  why: {
    label: "Why stress matters to your cells",
    title: "Stress, seen from inside the cell.",
    // Made for this page (Mo, September 28, 2026: "B"): a microscope in the dark whose lamp comes
    // on as scientists enter the story. Gemini, prompts in reference/product-nature-calm/originals/.
    // The slide is blank on purpose: nothing under the lens.
    visual: {
      src: "/images/products/nature-calm/why-microscope-off.webp",
      width: 2752,
      height: 1536,
      alt: "A laboratory microscope on a dark background",
      lit: {
        src: "/images/products/nature-calm/why-microscope-on.webp",
        width: 2752,
        height: 1536,
      },
    },
    lines: [
      "Under stress, your body releases hormones that get it ready to respond.",
      "Scientists study what stress does inside your cells, including their mitochondria.",
      "In animal studies, Dr.\u00a0Liu and Dr.\u00a0Wang found that stress raised oxidative damage in the brain.",
      "Nature Calm brings their research into a formula for life’s demanding days.",
    ],
  },
  // The label lists the vitamins first; here the formula's own nutrients lead, since the first six
  // are what the chapter shows before "Show all". The full label table follows this order too.
  ingredients: [
    {
      key: "coq10",
      name: "Coenzyme Q10",
      form: "Coenzyme Q10 (ubiquinone)",
      amount: 100,
      unit: "mg",
      role: "Your mitochondria use it to make energy. It also works as an antioxidant.",
    },
    {
      key: "nac",
      name: "N-acetylcysteine",
      form: "N-acetyl-L-cysteine",
      amount: 100,
      unit: "mg",
      role: "Your body uses it to make glutathione, one of your cells’ own antioxidants.",
    },
    {
      key: "theanine",
      name: "L-theanine",
      form: "L-theanine",
      amount: 100,
      unit: "mg",
      role: "An amino acid found naturally in tea leaves.",
    },
    {
      key: "tyrosine",
      name: "L-tyrosine",
      form: "L-tyrosine",
      amount: 100,
      unit: "mg",
      role: "An amino acid your body uses to make dopamine and noradrenaline, messengers between nerve cells.",
    },
    {
      key: "carnosine",
      name: "L-carnosine",
      form: "L-carnosine",
      amount: 100,
      unit: "mg",
      role: "Made of two amino acids. Your body has it in muscle and in the brain.",
    },
    {
      key: "ps",
      name: "Phosphatidylserine",
      form: "Phosphatidylserine",
      amount: 10,
      unit: "mg",
      role: "A fat that is part of the membrane around each cell, plentiful in the brain.",
    },
    {
      key: "resveratrol",
      name: "Resveratrol",
      form: "Resveratrol (from Polygonum cuspidatum root)",
      amount: 10,
      unit: "mg",
      role: "A plant compound. Here it comes from the root of Japanese knotweed.",
    },
    {
      key: "vanillin",
      name: "Vanillin",
      form: "Vanillin",
      amount: 20,
      unit: "mg",
      role: "The main flavour compound of vanilla.",
    },
    {
      key: "vitamin-c",
      name: "Vitamin C",
      form: "Vitamin C (as calcium ascorbate)",
      amount: 60,
      unit: "mg",
      role: "An antioxidant vitamin. Your body also needs it to make collagen.",
    },
    {
      key: "vitamin-e",
      name: "Vitamin E",
      form: "Vitamin E (as dl-alpha-tocopheryl acetate)",
      amount: 30,
      unit: "IU",
      role: "An antioxidant vitamin that helps protect your cells from damage.",
    },
    {
      key: "vitamin-a",
      name: "Vitamin A",
      form: "Vitamin A (as retinyl palmitate)",
      amount: 500,
      unit: "IU",
      role: "Important for your vision and your immune system.",
    },
    {
      key: "thiamin",
      name: "Thiamin (vitamin B1)",
      form: "Thiamin (as thiamin mononitrate)",
      amount: 4,
      unit: "mg",
      role: "Helps turn the food you eat into energy.",
    },
    {
      key: "niacin",
      name: "Niacin (vitamin B3)",
      form: "Niacin (as niacinamide)",
      amount: 50,
      unit: "mg",
      role: "Helps turn the food you eat into energy.",
    },
    {
      key: "vitamin-b6",
      name: "Vitamin B6",
      form: "Vitamin B6 (as pyridoxine HCl)",
      amount: 5,
      unit: "mg",
      role: "Your body uses it to make messengers between nerve cells.",
    },
    {
      key: "folate",
      name: "Folate",
      form: "Folate (as folic acid)",
      amount: 800,
      unit: "mcg",
      role: "Your cells need it to make DNA when they divide.",
    },
    {
      key: "vitamin-b12",
      name: "Vitamin B12",
      form: "Vitamin B12 (as cyanocobalamin)",
      amount: 20,
      unit: "mcg",
      role: "Helps keep your nerve and blood cells healthy.",
    },
    {
      key: "pantothenic-acid",
      name: "Pantothenic acid (vitamin B5)",
      form: "Pantothenic acid (as calcium pantothenate)",
      amount: 20,
      unit: "mg",
      role: "Helps your body turn fats and other food into energy.",
    },
    {
      key: "calcium",
      name: "Calcium",
      form: "Calcium (as ascorbate / carbonate)",
      amount: 246,
      unit: "mg",
      role: "A mineral for bones and teeth. Your nerves and muscles need it too.",
    },
  ],
  otherIngredients:
    "Other ingredients: rice flour, silicon dioxide, magnesium stearate and cellulose. Capsule: vegetable cellulose.",
  // Sorted by year on the page. From the homepage's checked list: stress and mitochondria
  // (Picard & McEwen) and the CoQ10 review.
  studies: [...ownStudies, ...studies(["29389735/", "29459830/"])],
  // The first three studies are about stress, not the ingredients.
  researchTitle: "The research behind the formula",
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
    // Text only: Dr. Wang asked for no photograph. Her public name only (BRAND-CHEATSHEET.md).
    {
      name: "Dr. Iris Wang",
      title: "Co-developer of Nature Calm",
      lines: [
        "Dr.\u00a0Wang developed Nature Calm with Dr.\u00a0Liu. Together they studied how stress affects the body, down to the cell.",
      ],
    },
  ],
  faq: [
    {
      question: "How do I take Nature Calm?",
      answer: "Take 3 capsules once a day, with or after a meal.",
    },
    {
      question: "How long does one bottle last?",
      answer: "Each bottle holds 90 vegetarian capsules: a 30-day supply at 3 capsules a day.",
    },
    {
      question: "What is the capsule made of?",
      answer:
        "The capsule is vegetable cellulose. The other ingredients are rice flour, silicon dioxide, magnesium stearate and cellulose.",
    },
    {
      question: "Has Nature Calm itself been tested in a clinical trial?",
      answer:
        "The research we share is about stress and about Nature Calm’s ingredients, not the finished product. Each study says whether it was done in people or in animals.",
    },
    {
      question: "Can I take it with medicines or other supplements?",
      answer: "Ask your doctor first, especially if you have a health condition or take medicines.",
    },
  ],
  caution:
    "As with any supplement, ask your doctor before taking Nature Calm, especially if you are pregnant or breastfeeding, have a health condition or take medicines. Keep out of reach of children.",
  notes: {
    label: "Amounts per serving of 3 capsules, as printed on the Nature Calm label.",
    science:
      "Each line describes what the nutrient does in the body in general. Ingredient research does not establish the effects of the finished product.",
    research:
      "Dr.\u00a0Liu and Dr.\u00a0Wang’s research on stress, and studies of some of Nature Calm’s ingredients. None of them tested Nature Calm itself. Each one says what kind of study it was.",
    fda: "These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease.",
  },
  related: ["nuricell", "green-bee-propolis", "advanced-opc", "turmerific"],
};

export default natureCalm;
