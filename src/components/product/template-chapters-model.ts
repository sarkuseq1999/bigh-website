import type { ProductPage, ProductStudy } from "./product-types";

// The chapter model and its pure helpers, with no side effects and no animation library: the
// Chapters template (template-chapters-kit.ts and template-chapters-daily.tsx re-export these) and
// the ink product page (ink/) both use them, and the ink page must not load the template's GSAP kit.

export type ChapterId = "overview" | "why" | "inside" | "research" | "people" | "daily" | "buy";
/** "night": a dark photo chapter that paints itself; the page stays paper, the index turns light. */
export type Tone = "paper" | "tint" | "night";
export type Chapter = { id: ChapterId; name: string; tone: Tone; number: number };

/** The chapter's element id, also its #anchor, so the index works before scripts load. */
export function anchorId(id: ChapterId) {
  return `chapter-${id}`;
}

/** Where the giant name parts for the bottle: at the word break nearest the middle ("Nuri|Cell",
 *  "Green Bee|Propolis"), or in the middle of a single word. (Here, not in the hero, so the ink
 *  page's opening can use it without loading the hero's 3D code.) */
export function splitName(name: string): [string, string] {
  const middle = name.length / 2;
  const breaks = [...name.matchAll(/ |(?<=[a-z])(?=[A-Z])/g)].map((match) => match.index);
  if (breaks.length === 0) {
    const half = Math.ceil(middle);
    return [name.slice(0, half), name.slice(half)];
  }
  const at = breaks.reduce((best, cut) =>
    Math.abs(cut - middle) < Math.abs(best - middle) ? cut : best,
  );
  return [name.slice(0, at).trim(), name.slice(at).trim()];
}

/** Small counts as words, for headings ("Inside every capsule, four ingredients."). */
export const WORDS: readonly string[] = [
  "",
  "one",
  "two",
  "three",
  "four",
  "five",
  "six",
  "seven",
  "eight",
  "nine",
  "ten",
];

/** Oldest first. Studies from the same year keep the order the product's data gives them. */
export function byYear(studies: ProductStudy[]) {
  const year = (study: ProductStudy) => Number.parseInt(study.year, 10) || 0;
  return studies
    .map((study, index) => ({ study, index }))
    .sort((a, b) => year(a.study) - year(b.study) || a.index - b.index)
    .map(({ study }) => study);
}

/** The most days drawn. A longer bottle still counts to its full number. */
const MAX_DAYS = 120;

/** A whole number from the data, or 0 when it is missing, zero, negative or not a number. */
function whole(value: unknown) {
  const number = Math.floor(Number(value));
  return Number.isFinite(number) && number > 0 ? number : 0;
}

/** The serving as the calendar needs it, safe for any values (2 a day for 60 days, missing ones). */
export function monthPlan(serving: Partial<ProductPage["serving"]> | undefined) {
  const perDay = whole(serving?.capsules);
  const perBottle = whole(serving?.perBottle);
  const days = whole(serving?.days) || (perDay && perBottle ? Math.floor(perBottle / perDay) : 0);
  const total = perBottle || perDay * days;
  const drawn = Math.min(days, MAX_DAYS);
  // About 6 across and 5 down for a month on wide screens, 5 across and 6 down on phones.
  const wide = Math.min(12, Math.max(4, Math.round(Math.sqrt(drawn * 1.3))));
  const narrow = Math.min(8, Math.max(4, Math.round(Math.sqrt(drawn * 0.8))));
  return {
    perDay,
    days,
    total,
    drawn,
    wide,
    narrow,
    wideRows: Math.max(1, Math.ceil(drawn / wide)),
    narrowRows: Math.max(1, Math.ceil(drawn / narrow)),
  };
}

/** The title, in months when the bottle lasts about a month or two or three. */
export function titleFor(days: number) {
  if (days >= 28 && days <= 31) return "One bottle, one month.";
  if (days >= 56 && days <= 62) return "One bottle, two months.";
  if (days >= 84 && days <= 93) return "One bottle, three months.";
  if (days === 1) return "One bottle, one day.";
  return "One bottle, {days} days.";
}
