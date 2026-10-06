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
// Under 900px the line would run through the words: the opening keeps its own short stroke out of
// the cell, then only the four rules and the footer's stroke.
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
 *  the words. The leans alternate, so the line passes each leader mid-swing, not in a corner. The
 *  brush carries more ink here than where it lands (`load`), so a stroke stays full through its
 *  middle and runs dry only toward the next station. */
const lean = (st: string, level: string, fy: number, by: number, load = 1.5): Waypoint => ({
  at: `st-${st}`,
  fx: 1,
  fy,
  level,
  dx: 8 + by,
  w: 3,
  clear: [level, -26],
  load,
});

/** A point on the cell's painting (fractions of its picture), with the brush's load there. */
const cell = (fx: number, fy: number, load: number, ink = 1): Waypoint => ({
  ...on("about-cell", fx, fy, 3, ink),
  load,
});

/** The stroke out of the cell, as in the comp: it grows out of the dark membrane at the cell's
 *  lower left (a thin first touch), lands loaded on the membrane's lower edge, and leaves the
 *  painting falling steeply down and to the left before it starts to turn. */
const leaving: Waypoint[] = [
  cell(0.27, 0.8, 0.45, 0.5),
  fresh(cell(0.235, 0.86, 1.3), 1.3),
  cell(0.195, 0.95, 1.5),
  cell(0.115, 1.047, 1.8),
];

// Two columns: out of the cell the sweep falls, then runs left over the open paper in a long, slow
// sag (its middle halfway between the station and the cell, never nearer the station than 150px)
// and turns down in one broad bend (fixed pixels from the station, so the bend keeps its size at
// every width) to meet the first leader as the vertical; the brush presses into the turn and the
// ink runs dry before it reloads there. Down the margin it lands loaded beside each station (about
// 4.5px at the comp), stays full through the middle, wavers a little (a calm lean beside Dr. Liu's
// print) and runs dry toward the next reload; past the last station it sweeps left as it lifts.
const page: Waypoint[] = [
  ...leaving,
  {
    at: "about-cell",
    after: "st-purpose",
    fx: 0,
    fy: 0.5,
    level: "st-purpose",
    dy: -104,
    clear: ["st-purpose", 150],
    w: 3,
    load: 2.2,
  },
  { ...on("st-purpose", 1, 0.5, 3.6, 1, 72, -92), load: 2.4 },
  { ...on("st-purpose", 1, 0.5, 3.4, 1, 22, -46), load: 2.2 },
  fresh(station("purpose", "left"), 1.25),
  lean("purpose", "purpose-body", 0.5, -8),
  fresh(station("roots", "left"), 1.25),
  lean("roots", "roots", 0.55, 18),
  fresh(station("experience", "left"), 1.25),
  lean("experience", "figures", 0.5, -8),
  fresh(station("promise", "left"), 1.25),
  // The tail stays short (about 130px), so the promises' rules, which come after it, draw while
  // the reader reaches them.
  { ...on("st-promise", 1, 0.5, 3, 1, 9, 56), load: 1.3 },
  { ...on("st-promise", 1, 0.5, 2.4, 0.7, -6, 98), load: 1.1 },
  { ...lift("st-promise", 1, 0.5), dx: -38, dy: 130 },
];

// One column (721-899px, the cell beside the words): the opening keeps its own short stroke, the
// comp's first arc out of the cell's foot, turning left under the painting and lifting before the
// words (it stays right of the lead and above the first station).
const column: Waypoint[] = [
  ...leaving,
  cell(-0.12, 1.12, 1.4),
  { ...cell(-0.2, 1.16, 1.2), w: 0, ink: 0 },
];

// A phone (the cell over the words): the same first arc, shorter, lifting in the margin above the
// opening's words.
const phone: Waypoint[] = [
  cell(0.27, 0.8, 0.45, 0.5),
  fresh(cell(0.235, 0.86, 1.6), 1.6),
  cell(0.2, 0.93, 1.6),
  cell(0.15, 0.985, 1.4),
  { ...cell(0.1, 1.02, 1.2), w: 0, ink: 0 },
];

export function aboutRoute(layout: Layout): Waypoint[] {
  const opening = layout === "page" ? page : layout === "column" ? column : phone;
  return [...opening, ...promises, ...footerEnding];
}
