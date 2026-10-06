import {
  footerEnding,
  fresh,
  lift,
  on,
  station,
  type Layout,
  type Waypoint,
} from "@/components/ink/route-kit";

// The About page's brush line (October 5, 2026; mockup reference/ink-pages/mockups/about.jpg).
// On two columns it leaves the foot of the ink cell, sweeps down to the left and runs down the
// page's left margin, past the four stations (each label sits left of the line, its leader
// pointing at it), reloading beside each. Then it touches down four times, one short rule over
// each promise, travels to the footer and lays the stroke the crane at rest stands on.
// Under 900px the line would run through the words: only the four rules and the footer's stroke.
//
// The opening has no approved stroke of its own to keep (the homepage's crane stroke is), so the
// About opening carries no "opening" anchor and the whole line is painted as the page's brush
// line: one calligraphic envelope that lands loaded, tapers and runs dry (DESIGN.md, Brush Line).

/** One short brush-stroke rule along the top of a promise. The mockup's rules are loaded strokes,
 *  so these carry more ink than the kit's light `rule` (the homepage's standards): each lands
 *  loaded at the left, dips a hair, and runs out toward the right as it lifts. */
const promiseRule = (at: string): Waypoint[] => [
  { at, fx: -0.02, fy: 0, dy: -2, w: 0, ink: 0 },
  { at, fx: 0, fy: 0, dy: 0, w: 3, ink: 1, fresh: true, load: 1.55 },
  { at, fx: 0.3, fy: 0, dy: 2, w: 3, ink: 1, load: 1.45 },
  { at, fx: 0.7, fy: 0, dy: 1.5, w: 3, ink: 0.9, load: 1.15 },
  { at, fx: 1, fy: 0, dy: -1, w: 2, ink: 0.5, load: 0.8 },
  { at, fx: 1.03, fy: 0, dy: -4, w: 0, ink: 0 },
];

const promises: Waypoint[] = [0, 1, 2, 3].flatMap((i) => promiseRule(`promise-${i}`));

/** Between two stations the hand leans a little (`by` pixels from the leaders' line, at `fy` of
 *  the height of a part's words, `level`), as the mockup's line wavers, never nearer than 26px to
 *  the words. The leans alternate, so the line passes each leader mid-swing, not in a corner. */
const lean = (st: string, level: string, fy: number, by: number): Waypoint => ({
  at: `st-${st}`,
  fx: 1,
  fy,
  level,
  dx: 8 + by,
  w: 3,
  clear: [level, -26],
});

// The stroke grows out of the wash under the cell's membrane (thin and light), presses as it
// leaves the painting, and sweeps over the open paper under the opening's words to the first
// station, where it turns down the margin; it lands loaded beside each station, wavers a little
// (a calm lean beside Dr. Liu's print), and past the last station sweeps to the left as it lifts.
const page: Waypoint[] = [
  { ...on("about-cell", 0.3, 0.905, 1.2, 0.5), load: 0.4 },
  { ...on("about-cell", 0.22, 0.97, 3), load: 1.2 },
  { ...on("about-cell", -0.12, 1.12, 3.8), load: 1.45 },
  // Above the first station the sweep turns down in one broad bend (fixed pixels from the
  // station, so the bend keeps its size at every width), reaching the leader as the vertical,
  // without swinging out past it; the brush presses into the turn and, on the same load, runs
  // on past the first station (as in the mockup, no reload there) to land again at the second.
  { ...on("st-purpose", 1, 0.5, 3.6, 1, 72, -92), load: 2.1 },
  { ...on("st-purpose", 1, 0.5, 3.4, 1, 22, -46), load: 2.1 },
  { ...station("purpose", "left"), load: 1.8 },
  { ...lean("purpose", "purpose-body", 0.5, -8), load: 1.4 },
  fresh(station("roots", "left")),
  lean("roots", "roots", 0.55, 18),
  fresh(station("experience", "left")),
  lean("experience", "figures", 0.5, -8),
  fresh(station("promise", "left")),
  // The tail stays short (about 130px), so the promises' rules, which come after it, draw while
  // the reader reaches them.
  on("st-promise", 1, 0.5, 3, 1, 9, 56),
  on("st-promise", 1, 0.5, 2.4, 0.7, -6, 98),
  { ...lift("st-promise", 1, 0.5), dx: -38, dy: 130 },
];

export function aboutRoute(layout: Layout): Waypoint[] {
  if (layout === "page") return [...page, ...promises, ...footerEnding];
  return [...promises, ...footerEnding];
}
