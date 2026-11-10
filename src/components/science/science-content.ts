// Words and facts for the Science page (/science). Mo's 9/16 plan: lead with the scientists, then
// the research, health explained, and Ask BiGH Science. The page is Ink & Gold (Mo, October 13-14,
// 2026; components in ./ink/): first "the handscroll", whose painting travelled sideways; since
// Mo's pick B of October 26, Dr. Liu first, then his path one place per screen going down, then the
// research, health explained, the formulas and Ask. It replaced look B, "Scroll film" (Mo's pick of
// September 28, now in reference/science-page/looks/film/); the earlier looks are in
// reference/science-page/looks/ and .../looks/round3/.
//
// Approved copy is marked "approved" with its date in BRAND-CHEATSHEET.md. Everything else is a
// DRAFT line for this build, written from facts in RESEARCH-NOTES.md, and still needs Mo's words
// pass. Strings are English source text for useCopy(); lines the homepage already uses are
// reused word for word, so their draft translations already exist.
//
// Rules kept here: Dr. Iris Wang appears in words only (no photograph), with only the credits Mo
// confirmed; no quote is invented for Dr. Liu; animal research is called "animal study"; the
// research line under the list stays.

// Round 3 (Mo, November 4, 2026: start broader, with what science BiGH focuses on and why; spec
// docs/superpowers/specs/2026-11-04-science-california-design.md). The page opens on the science,
// and names the scientist who has spent his career on it on the same screen (Mo's September rule:
// real scientists in the first impression). DRAFT lines.
export const opening = {
  title: "Our science starts in the cell.",
  // "Decades": his work on cells' energy and aging dates from Bruce Ames's laboratory, 1994
  // (RESEARCH-NOTES.md); his doctorate was in neuroscience, so not "his whole career".
  lead: "How do your cells make energy? And what changes as we age? Dr. Jiankang Liu has spent decades studying both.",
  // The zoom opening starts inside the cell (Mo, November 10, 2026: he picked A of four ideas for
  // the first screen). The line at its foot says what the gold is. "Most of": cells also make a
  // little energy outside their mitochondria.
  caption: "In gold: its mitochondria, where the cell makes most of its energy.",
  alt: "The inside of one cell painted in pale blue washes: a dark blue nucleus, and its mitochondria as drifting slivers of gold",
};

// Why the cell (DRAFT). 37 trillion: Bianconi et al. 2013, Annals of Human Biology (PubMed
// 23829164), about 3.72 x 10^13. The three lines open the kit's three explainer sheets (dialogs),
// which "Make sense of the science." opened before (that heading is the homepage's own).
export const why = {
  title: "Why start with the cell?",
  lead: "Everything you do, from a clear thought to a long walk, runs on energy your cells make. You have about 37 trillion of them, and each one makes its own.",
  lines: [
    {
      // "Your cells", not "each cell": red blood cells, most of the 37 trillion, have none.
      text: "Inside your cells, mitochondria turn food into energy.",
      link: "What are mitochondria?",
    },
    {
      text: "Making energy also makes free radicals, which your cells keep in check.",
      link: "What are free radicals?",
    },
    {
      text: "With age, mitochondria tend to work less well: one of the hallmarks of aging.",
      link: "How do cells age?",
    },
  ],
  source: "Cell count: Bianconi and colleagues, Annals of Human Biology, 2013.",
  sourceUrl: "https://pubmed.ncbi.nlm.nih.gov/23829164/",
  // Its heading and lead stand in the zoom's last view, the walker on golden hills (since
  // November 10, 2026; the cell stood here before).
  alt: "A walker with a sun hat and a stick on a trail through golden California hills and oaks, painted in ink and watercolour",
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

// Round 3 (DRAFT): the formulas' heading, short; formulasLine is its lead.
export const formulasTitle = "Every formula has a scientist behind it.";

// DRAFT: his path, one place per screen (Mo's pick B, October 26, 2026), each beside its painting
// (science-art.ts places). Years only where a source gives one: the faculty profile dates his
// postdoctoral work in Bruce Ames's laboratory 1994-1997 (RESEARCH-NOTES.md), so Berkeley says 1994,
// the year he joined, and the 2002 study is told as published then. The three numbers that stood
// under his name (280+, 1994, 2025) are told here with the same sources. Today drops the stop's old
// title (his BiGH title stands under his name above). English in every language, as the stops were.
// Round 3 (November 4): Okayama's castle painting read as Asian; his doctorate there is told in
// Berkeley's words, and the path starts in California.
export const places = [
  {
    key: "berkeley",
    when: "1994 · California",
    name: "Berkeley",
    title: "Research in Bruce Ames’s laboratory",
    text: "After a doctorate in neuroscience at Okayama University in Japan, he joined Bruce Ames at the University of California, Berkeley. In 2002 their study of two nutrients and the aging cell appeared in PNAS, as an animal study.",
    links: [
      {
        label: "Faculty profile (Chinese)",
        url: "https://faculty.xjtu.edu.cn/j.liu/zh_CN/zhym/1002677/list/index.htm",
      },
      { label: "Read the 2002 study", url: "https://pubmed.ncbi.nlm.nih.gov/11854529/" },
    ],
    alt: "The bell tower at Berkeley among tall trees on a hill over the bay, painted in ink and watercolour",
  },
  {
    key: "salzburg",
    when: "2025 · Austria",
    name: "Salzburg",
    title: "An academy honor",
    text: "Elected to the European Academy of Sciences and Arts, based in Salzburg, with more than 280 papers.",
    links: [
      { label: "University announcement", url: "https://www.uhrs.edu.cn/info/1050/1805.htm" },
    ],
    alt: "Salzburg’s fortress above the old town and the river, painted in ink and watercolour",
  },
  {
    key: "today",
    when: "",
    name: "Today",
    title: "",
    text: "His research now guides the science behind our formulas.",
    links: [],
    alt: "California oaks on golden hills under a gold sun, painted in ink and watercolour",
  },
] as const;

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

// The research library: the homepage's 36 checked sources (home/research-data.ts), grouped the way
// Timeline's "Our Studies" page groups its list. Group intros are DRAFT.
// Round 3: a heading of its own ("Curiosity, with references." is the homepage's research heading),
// no label over it. DRAFT.
export const research = {
  title: "Read the research yourself.",
  text: "Three studies to start with, and every source we cite. For each one we say what it shows, and what it does not.",
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
// Round 3: no label over the heading; "In development" and the note under the steps say it is
// planned.
export const ask = {
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

// The ink page (Mo, October 13-14, 2026; round 3 since November 4). DRAFT lines.
export const ink = {
  readStudy: "Read the study", // DRAFT
  journalsAlt:
    "Old bound journals along a library table, three laid open in front, painted in ink and watercolour", // DRAFT
  picnicAlt:
    "Two enamel camp mugs on a redwood picnic table in a California park, painted in ink and watercolour", // DRAFT
  illustration: "Illustration",
};
