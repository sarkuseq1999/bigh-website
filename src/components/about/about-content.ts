// The About page's words. Mo locked them on September 25, 2026: opening line A, no changes.
// Facts Mo confirmed that day: the NuriCell formula is about 23 years old (shown as "20+" so it
// stays true without an exact start year; never name its earlier Asian brand), products are made
// in California by a GMP-certified maker, the 45-day refund is current policy, and Ask BiGH Science
// stays on the page before the service exists. BiGH was incorporated in California on 05/11/2016.
// The page is About C, "The circle" (October 7, 2026), with B "The album" built beside it on its own
// branch. Before them: D (the folded letter, branch ink-pages), the first ink About (git history, up
// to c30a489) and the Glass page (Mo picked look B with opening 3 and Switzer on Sept 28, 2026),
// which is in the backup zip named in docs/about-page.md.

export const about = {
  hero: {
    label: "About BiGH",
    title: "Be in Good Health.",
    lead: "What our name stands for. What our work is for.",
  },
  purpose: {
    label: "Our purpose",
    lines: ["A full life has many parts.", "We focus on one you can’t see: your cells."],
    mission:
      "Our mission is to support cellular health and mental energy, helping people live life to the fullest.",
  },
  roots: {
    label: "Our scientific roots",
    title: "Our key formulas begin with scientists.",
    // Credits as BRAND-CHEATSHEET.md has them (Mo, Sept 25 and 28): NuriCell is Dr. Liu's alone;
    // Nature Calm is Dr. Liu's and Dr. Iris Wang's.
    text: "Dr. Jiankang Liu, our Chief Scientific Advisor, studies mitochondria and aging. He formulated NuriCell, and with Dr. Iris Wang, he developed Nature Calm.",
    stat: { value: "280+", label: "scientific papers by Dr. Liu" },
    link: "Meet our scientists",
    // Dr. Iris Wang is named in words only: she asked for no photograph on the website.
    photo: { src: "/images/jiankang-liu.jpg", alt: "Dr. Jiankang Liu" },
  },
  // Two new chapters (Mo, November 4-9, 2026; live November 9 with draft translations m1200-m1222,
  // not native-reviewed) on Mo's ideas: ingredients "from
  // the part of the world best for their natural growth" and "proudly made in California, by
  // GMP-certified makers". NuriCell's four nutrients are made, not grown, so the plants chapter
  // speaks of plants only.
  // Our ingredients: the globe (Mo picked B, November 9; plants-map.tsx). No place is named (Mo:
  // he is still finding out where the pine bark and grape seed come from): each plant carries
  // the kind of place it thrives in, true of the plant itself wherever it is bought.
  plants: {
    label: "Our ingredients",
    title: "Each plant, from where it grows best.",
    text: "We look around the world for our plants, and bring each one home from the place it grows best.",
    home: { name: "California", note: "where we make them" },
    alt: "A globe painted in ink and watercolour, California facing you. Four plants stand round its edge, and a gold dotted line runs from each over the globe to California.",
    items: [
      { key: "propolis", plant: "Green propolis", grows: "Warm, wild hillsides" },
      { key: "turmeric", plant: "Turmeric", grows: "Hot, rainy fields" },
      { key: "grape", plant: "Grape seed", grows: "Sunny slopes" },
      { key: "pine", plant: "Pine bark", grows: "Old pine forests" },
    ],
  },
  // Our home: the valley at dawn (Mo picked F, November 9; made-in-california.tsx). No bottles in
  // the painting (Mo: "I'd rather not have the product bottle there").
  home: {
    label: "Our home",
    title: "Proudly made in California.",
    text: "Every bottle we sell is made here, by GMP-certified manufacturers.",
    alt: "Early morning over California’s Central Valley from a golden foothill: rows of fields, some in gold, the snowy Sierra behind",
    // What GMP (21 CFR 111) asks of every maker: identity checks on each dietary ingredient
    // (111.75), a master manufacturing record (111.205) and a batch record (111.255).
    gmp: "GMP means Good Manufacturing Practice: the rules for making supplements with care.",
    rules: [
      "Every ingredient is checked before it’s used.",
      "Every batch follows a written recipe.",
      "Every batch is recorded, so it can be traced.",
    ],
  },
  experience: {
    label: "Our experience",
    title: "Our flagship formula is older than BiGH.",
    stats: [
      { value: "2016", unit: "", label: "BiGH founded in California" },
      { value: "20+", unit: "years", label: "NuriCell’s formula, unchanged" },
    ],
  },
  promise: {
    label: "Our promise",
    title: "What you can count on.",
    // "Know where it comes from" became the plants chapter; "Made in California" stays here too
    // (Mo, November 6, 2026: "You can still keep the Made in California there"); "Honest about the
    // research" is new (November 4).
    items: [
      { title: "Made in California.", text: "By GMP-certified manufacturers." },
      { title: "45 days to decide.", text: "Not right for you? Send it back for a refund." },
      { title: "Answers in your language.", text: "We reply in the language you write in." },
      {
        title: "Honest about the research.",
        text: "We show you the studies, and say what they don’t prove.",
      },
    ],
  },
  closing: {
    title: "Curious about the science?",
    text: "Ask BiGH Science. We help you explore the research, with guidance from the scientists we work with.",
    primary: "Ask BiGH Science",
    secondary: "Explore our products",
  },
} as const;

// Where the page's links lead. The Science page landed on main on September 28, 2026.
export const routes = {
  scientists: "/science",
  products: "/#products",
} as const;

// DRAFT: small new labels the page needs beyond the locked words. Mo approves them before launch.
export const drafts = {
  // "Answers in your language": hello in the site's five languages.
  greetings: [
    { lang: "en", text: "Hello." },
    { lang: "zh-Hans", text: "你好。" },
    { lang: "ko", text: "안녕하세요." },
    { lang: "vi", text: "Xin chào." },
    { lang: "ja", text: "こんにちは。" },
  ],
  languages: "English, Chinese, Korean, Vietnamese and Japanese",
  // Shown on every AI-made picture, as on the Science page.
  illustration: "Illustration",
} as const;
