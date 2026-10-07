// The About page's words. Mo locked them on September 25, 2026: opening line A, no changes.
// Facts Mo confirmed that day: the NuriCell formula is about 23 years old (shown as "20+" so it
// stays true without an exact start year; never name its earlier Asian brand), products are made
// in California by a GMP-certified maker, the 45-day refund is current policy, and Ask BiGH Science
// stays on the page before the service exists. BiGH was incorporated in California on 05/11/2016.
// The page is "The name, on a folded letter" (Mo's design D, October 6, 2026). Before it: the first
// ink About (October 5), which is in git history (commits up to c30a489), and the Glass page (Mo
// picked look B with opening 3 and Switzer on Sept 28, 2026), which is in the backup zip named in
// docs/about-page.md.

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
    items: [
      { title: "Made in California.", text: "By GMP-certified manufacturers." },
      {
        title: "Know where it comes from.",
        text: "Our green propolis comes only from Minas Gerais, Brazil.",
      },
      { title: "45 days to decide.", text: "Not right for you? Send it back for a refund." },
      { title: "Answers in your language.", text: "We reply in the language you write in." },
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
