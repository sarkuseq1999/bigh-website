// Words and facts for the Science page (/science). Mo's 9/16 plan: lead with the scientists, then
// the research, health explained, and Ask BiGH Science. After three rounds Mo chose look B, "Scroll
// film" (September 28, 2026); the others are in reference/science-page/looks/ and .../looks/round3/.
//
// Approved copy is marked "approved" with its date in BRAND-CHEATSHEET.md. Everything else is a
// DRAFT line for this build, written from facts in RESEARCH-NOTES.md, and still needs Mo's words
// pass. Strings are English source text for useCopy(); lines the homepage already uses are
// reused word for word, so their draft translations already exist.
//
// Rules kept here: Dr. Iris Wang appears in words only (no photograph), with only the credits Mo
// confirmed; no quote is invented for Dr. Liu; animal research is called "animal study"; the
// research line under the list stays.

export const opening = {
  eyebrow: "Science",
  // Mo's proposed opening (BRAND-CHEATSHEET.md, "Science page — opening priority chosen by Mo").
  title: "Meet the scientists behind BiGH’s key formulas.",
  // The hero sets it in two lines: plain words, then a gold serif line.
  titleLead: "Meet the scientists",
  titleAccent: "behind BiGH’s key formulas.",
};

// Approved September 21, 2026 (homepage scientist section).
export const liu = {
  name: "Dr. Jiankang Liu",
  role: "Chief Scientific Advisor, BiGH",
  headline: "Recognized internationally. Focused on cellular health.",
  intro:
    "Dr. Liu is an internationally recognized scientist in mitochondrial biology and aging. His research explores the connections between cellular energy, nutrition, and how we age.",
  purpose:
    "As BiGH’s Chief Scientific Advisor, he brings decades of scientific experience to our purpose: helping people stay sharp, stay active, and live fully.",
  button: "Read his story",
  photo: { src: "/images/jiankang-liu.jpg", width: 512, height: 768 },
  highlights: [
    {
      text: "Research with Bruce Ames at the University of California, Berkeley, investigating mitochondria, nutrition, and aging in laboratory animals.",
      link: "Berkeley research report",
      url: "https://newsarchive.berkeley.edu/news/media/releases/2002/02/19_diet.html",
    },
    {
      text: "Elected to the European Academy of Sciences and Arts in 2025. His university’s announcement also reports more than 280 scientific papers.",
      link: "University announcement",
      url: "https://www.uhrs.edu.cn/info/1050/1805.htm",
    },
    {
      text: "Honored by the journal Antioxidants through a special issue recognizing his contributions to mitochondrial biology and medicine.",
      link: "Journal’s tribute",
      url: "https://www.mdpi.com/si/230528",
    },
  ],
};

// DRAFT: three big numbers for look A, each from a dated source (RESEARCH-NOTES.md).
export const liuNumbers = [
  {
    value: 280,
    suffix: "+",
    label: "scientific papers, as his university reported in 2025",
    url: "https://www.uhrs.edu.cn/info/1050/1805.htm",
  },
  {
    value: 1994,
    suffix: "",
    label: "the year he joined Bruce Ames’s laboratory at UC Berkeley",
    url: "https://faculty.xjtu.edu.cn/j.liu/zh_CN/zhym/1002677/list/index.htm",
  },
  {
    value: 2025,
    suffix: "",
    label: "elected to the European Academy of Sciences and Arts",
    url: "https://www.uhrs.edu.cn/info/1050/1805.htm",
  },
];

// The story panel ("Read his story"). The first two paragraphs are the homepage's own dialog text.
export const liuStory = {
  eyebrow: "Meet the scientists",
  paragraphs: [
    "Dr. Liu studies mitochondrial function, oxidative stress, and the biology of aging. His scientific background is central to BiGH’s approach to cellular health.",
    "He earned his doctorate at Okayama University in Japan and completed postdoctoral work in biochemistry and molecular biology at the University of California, Berkeley.",
    "In 2025, his university announced his election to the European Academy of Sciences and Arts.",
  ],
  sources: [
    { label: "University biography (Chinese)", url: "https://www.uhrs.edu.cn/info/1050/1805.htm" },
    { label: "Read the 2002 study", url: "https://pubmed.ncbi.nlm.nih.gov/11854529/" },
  ],
};

// DRAFT. Words only, never a photograph. Credits confirmed by Mo on September 25, 2026: NuriCell is
// formulated by Dr. Liu only ("credit goes to Dr. Liu only"); Nature Calm by Dr. Liu and Dr. Iris
// Wang. This replaces his September 21 joint NuriCell credit; the homepage (main) still shows the
// old credit and needs the same change.
export const iris = {
  name: "Dr. Iris Wang",
  role: "Scientist and co-developer",
  // Draft, September 29, 2026: the second half follows Mo's Advanced OPC credit.
  text: "Dr. Iris Wang developed Nature Calm together with Dr. Liu, and guided the formulation of Advanced OPC Formula.",
};

export const formulas = [
  {
    name: "NuriCell",
    image: "/images/products/nuricell.png",
    credit: "Formulated by Dr. Jiankang Liu.",
  },
  {
    name: "Nature Calm",
    image: "/images/products/nature-calm.png",
    credit: "Developed by Dr. Jiankang Liu and Dr. Iris Wang.",
  },
  // Mo, September 29, 2026 (choosing between this page and the product page): Advanced OPC is
  // credited to Dr. Iris Wang alone, the same words as on its product page.
  // It stands beside Nature Calm, so the two products that share a credit sit together.
  {
    name: "Advanced OPC Formula",
    image: "/images/products/advanced-opc.png",
    credit: "Formulated under the guidance of Dr. Iris Wang.",
  },
  // Mo, September 28, 2026: the other products were developed "under the direction and guidance
  // of Dr. Liu and Iris Wang".
  {
    name: "Green Bee Propolis",
    image: "/images/products/green-bee-propolis.png",
    credit: "Developed under the direction and guidance of Dr. Jiankang Liu and Dr. Iris Wang.",
  },
  {
    name: "Turmerific",
    image: "/images/products/turmerific.png",
    credit: "Developed under the direction and guidance of Dr. Jiankang Liu and Dr. Iris Wang.",
  },
];

// DRAFT (from Mo's September 28 note): one line that sums up the credits.
export const formulasLine =
  "Every BiGH formula was developed by our scientists or under their direction and guidance.";

// DRAFT: his path (the film strip). Years only where a source gives one.
export const pathStops = [
  {
    mark: "Okayama",
    title: "A doctorate in neuroscience",
    text: "His scientific training began at Okayama University in Japan.",
    link: "Faculty profile (Chinese)",
    url: "https://faculty.xjtu.edu.cn/j.liu/zh_CN/zhym/1002677/list/index.htm",
  },
  {
    mark: "1994",
    title: "Berkeley",
    text: "Research in Bruce Ames’s laboratory at the University of California, Berkeley.",
    link: "Faculty profile (Chinese)",
    url: "https://faculty.xjtu.edu.cn/j.liu/zh_CN/zhym/1002677/list/index.htm",
  },
  {
    mark: "2002",
    title: "Nutrients and the aging cell",
    text: "Two nutrients, one aging cell. Published in PNAS as an animal study.",
    link: "Read the 2002 study",
    url: "https://pubmed.ncbi.nlm.nih.gov/11854529/",
  },
  {
    mark: "2025",
    title: "An academy honor",
    text: "Elected to the European Academy of Sciences and Arts, with more than 280 papers.",
    link: "University announcement",
    url: "https://www.uhrs.edu.cn/info/1050/1805.htm",
  },
  {
    mark: "Today",
    title: "Chief Scientific Advisor, BiGH",
    text: "His research now guides the science behind our formulas.",
    link: "",
    url: "",
  },
];

// DRAFT: look C's three questions (look C is in reference/science-page/looks/; kept here so it can
// come back as it was).
export const questions = [
  {
    topic: "Energy",
    title: "How do cells make energy?",
    text: "Mitochondria turn food into energy your cells can use.",
  },
  {
    topic: "Balance",
    title: "What keeps free radicals in check?",
    text: "Making energy also makes free radicals. Your cells’ defenses keep them in balance.",
  },
  {
    topic: "Aging",
    title: "What changes as we age?",
    text: "Mitochondria are one part of how cells change over time.",
  },
];

// Health explained: the three article titles and previews (approved September 21, 2026).
export const health = {
  eyebrow: "Health, explained simply",
  title: "Make sense of the science.",
  text: "Explore cellular health, mental energy, and healthy aging—with explanations that make the science easier to understand.",
  soon: "Article coming soon",
  doors: [
    {
      topic: "Mitochondria",
      title: "What are mitochondria—and why do they matter?",
      preview:
        "A simple guide to your cells’ tiny power plants, their role in everyday energy, and what mitochondrial health means.",
      image: "/images/science/glass-cell.webp",
    },
    {
      topic: "Free radicals",
      title: "What are free radicals—and how do antioxidants help?",
      preview:
        "A simple explanation of free radicals, the damage they can cause, and your cells’ natural defenses.",
      image: "/images/science/antioxidant.webp",
    },
    {
      topic: "Aging cells",
      title: "What happens to your cells as you age?",
      preview:
        "A closer look at how cells change over time and what researchers are learning about healthy aging.",
      image: "/images/science/glass-cell-aged.webp",
    },
  ],
};

// The research library: the homepage's 36 checked sources (home/research-data.ts), grouped the way
// Timeline's "Our Studies" page groups its list. Group intros are DRAFT.
export const research = {
  eyebrow: "The research",
  title: "Curiosity, with references.",
  text: "Science is most useful when you can understand it. Explore the ideas behind our approach, and see what each source actually tells us.",
  groups: [
    {
      type: "Science",
      title: "How cells work and age",
      text: "Reviews of the biology behind cellular health.",
    },
    {
      type: "Ingredients",
      title: "Ingredient research",
      text: "Studies of ingredients used in BiGH formulas. None is a study of a finished BiGH product.",
    },
    {
      type: "Guides",
      title: "Plain-language guides",
      text: "Pages from public health institutes.",
    },
  ],
  // Rows written by or with Dr. Liu get a small tag.
  byLiu: ["https://pubmed.ncbi.nlm.nih.gov/11854529/", "https://pubmed.ncbi.nlm.nih.gov/17605107/"],
  tag: "Dr. Liu’s work",
  note: "Ingredient research and general science do not establish the effects of a finished BiGH product.",
  // Round 2: Mo found 36 rows overwhelming. Three key studies lead (two of Dr. Liu's own and the
  // review that frames aging); the rest wait behind "See all sources". Row texts come from
  // home/research-data.ts by URL, so their draft translations carry over.
  key: [
    "https://pubmed.ncbi.nlm.nih.gov/11854529/",
    "https://pubmed.ncbi.nlm.nih.gov/17605107/",
    "https://pubmed.ncbi.nlm.nih.gov/36599349/",
  ],
  keyTitle: "Three studies to start with.",
  seeAll: "See all {count} sources",
  hideAll: "Show fewer sources",
};

// Ask BiGH Science: the homepage's own words (its dialog and strip).
export const ask = {
  eyebrow: "A planned customer benefit",
  title: "Ask BiGH Science",
  lead: "Good questions deserve clear answers.",
  // The homepage dialog's line without its opening sentence, which repeated the lead (DRAFT).
  text: "We are developing a way for BiGH customers to explore broader health and science questions with input from participating scientists.",
  steps: [
    "Start with a question about topics such as cellular health, nutrition, or healthy aging.",
    "BiGH explains what the research says and involves scientific advisors when deeper input is needed.",
    "Each answer identifies its contributors and where the science remains uncertain.",
  ],
  // DRAFT: example questions, labeled as examples.
  examplesLabel: "Questions like these",
  examples: [
    "What do mitochondria actually do?",
    "Are more antioxidants always better?",
    "What changes in our cells as we age?",
  ],
  status: "In development",
  note: "The question service is not accepting submissions yet. Eligibility and response arrangements are still being agreed. This will be general science education, not personal medical care.",
};
