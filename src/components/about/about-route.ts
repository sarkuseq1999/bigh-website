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
// On two columns it sets down on the paper beside the foot of the ink cell, sweeps down to the
// left and runs down the page's left margin, past the four stations (each label sits left of the
// line, its leader pointing at it), reloading beside each. Then it touches down four times, one
// short rule over each promise, travels to the footer and lays the stroke the crane at rest stands
// on. Under 900px the line would run through the words: on a tablet held upright the opening's
// stroke runs from beside the cell's foot to the first station's leader; then (and on a phone)
// only the four rules and the footer's stroke.
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
 *  brush carries the most ink here (`load`), so a stroke swells through its middle. */
const lean = (st: string, level: string, fy: number, by: number, load = 1.9): Waypoint => ({
  at: `st-${st}`,
  fx: 1,
  fy,
  level,
  dx: 8 + by,
  w: 3,
  clear: [level, -26],
  load,
});

/** The brush arrives at a station still loaded and rises off the paper for a hair at the leader's
 *  tip (ink 0.015: about half a pixel, never a gap) before it reloads there. A stroke that ends by
 *  lifting keeps its ink to the end (the kit's STROKE_LIFT, as the closing stroke does), so the
 *  line holds real ink down the margin instead of running into a long dry pen line. */
const arrive = (id: string, load = 1.6): Waypoint[] => [
  { ...station(id, "left"), dy: -12, load },
  { ...station(id, "left"), ink: 0.015, load },
];

/** The station's reload: a new stroke lands, loaded, beside the leader. */
const land = (id: string, load = 1.3): Waypoint => fresh(station(id, "left"), load);

/** A point on the cell's painting (fractions of its picture), with the brush's load there. */
const cell = (fx: number, fy: number, load: number, ink = 1): Waypoint => ({
  ...on("about-cell", fx, fy, 3, ink),
  load,
});

/** A point beside the cell's foot: `left` pixels to the left of and `down` pixels below the
 *  painting's lower-left outer-wash point (fx 0.203 / fy 0.85 of the picture; the lowest ink of
 *  its left lobe lies a few pixels under it). Fixed pixels, so the gap to the painting holds at
 *  every size. */
const foot = (left: number, down: number, load: number): Waypoint => ({
  ...on("about-cell", 0.203, 0.85, 3, 1, -left, down),
  load,
});

/** The line begins as a brush set down on the paper beside the cell's foot, already travelling
 *  left, never as something hanging from the painting. The first touch sits about 25px under the
 *  foot's lowest ink and a little to its left, so the painting lies above the stroke's end, not
 *  ahead of it: the stroke's axis runs level along the paper over its first 40px (never
 *  climbing), then drifts down by degrees into the fall, and the cell's underside slopes away to
 *  the right behind it. The head is a pressed, round tip. The kit lands the page's first stroke
 *  at the load its waypoints give it (no thin lead-in), so the tip carries a quarter of the load
 *  and swells to the full load within five pixels (a round end, not a square cut), holds it for a
 *  dozen pixels (the press) and thins into the run. The ink stays at 1 here, so the head is wet,
 *  with no dry-brush streaks. */
const leaving: Waypoint[] = [
  foot(12, 26, 0.5),
  foot(17, 26.1, 1.9),
  foot(28, 26.4, 1.9),
  foot(52, 27.5, 1.6),
  foot(80, 34, 1.62),
];

// Two columns: from beside the cell's foot the sweep runs left over the open paper, falling into a
// long, slow sag (its middle halfway between the station and the cell, never nearer the station
// than 150px) and turns down in one broad bend (fixed pixels from the station, so the bend keeps
// its size at every width) to meet the first leader as the vertical, pressing into the turn. Down
// the margin it lands beside each station, swells through the middle, wavers a little (a calm lean
// beside Dr. Liu's print), and arrives at the next station still holding ink; past the last
// station it sweeps left as it lifts. Every load stays within the homepage's brush (its strokes
// run to 1.9, its closing stroke to 2.2).
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
    load: 1.7,
  },
  { ...on("st-purpose", 1, 0.5, 3.6, 1, 72, -92), load: 1.9 },
  { ...on("st-purpose", 1, 0.5, 3.4, 1, 22, -46), load: 1.9 },
  ...arrive("purpose", 1.9),
  land("purpose"),
  lean("purpose", "purpose-body", 0.5, -8),
  ...arrive("roots"),
  land("roots"),
  lean("roots", "roots", 0.55, 18),
  ...arrive("experience"),
  land("experience"),
  lean("experience", "figures", 0.5, -8),
  ...arrive("promise"),
  land("promise"),
  // The tail stays short (about 130px), so the promises' rules, which come after it, draw while
  // the reader reaches them.
  { ...on("st-promise", 1, 0.5, 3, 1, 9, 56), load: 1.5 },
  { ...on("st-promise", 1, 0.5, 2.4, 0.7, -6, 98), load: 1.2 },
  { ...lift("st-promise", 1, 0.5), dx: -38, dy: 130 },
];

// One column (721-899px, the cell beside the words): the page's line arrives at its first station.
// From beside the cell's foot it runs left on a gentle fall (no tick under the painting), sweeps
// under the opening's words and comes down into the tip of the "Our purpose" leader (the leader's
// free end, at the left of the label), where it lifts: it ends where the station hangs, never in
// open paper.
const column: Waypoint[] = [
  ...leaving,
  cell(-0.14, 1.03, 1.6),
  { ...on("st-purpose", 0, 0.5, 3, 1, 70, -50), load: 1.6 },
  { ...on("st-purpose", 0, 0.5, 3, 1, 22, -14), load: 1.3 },
  { ...lift("st-purpose", 0, 0.5) },
];

// A phone (the cell over the words) has no stroke out of the cell: a short one read as a tail on
// the painting. The line starts at the promises' rules.
export function aboutRoute(layout: Layout): Waypoint[] {
  const opening = layout === "page" ? page : layout === "column" ? column : [];
  return [...opening, ...promises, ...footerEnding];
}
