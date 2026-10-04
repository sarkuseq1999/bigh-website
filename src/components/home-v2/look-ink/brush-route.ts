// The brush line's route down the page: waypoints pinned to the blocks' own [data-brush] anchors
// (fx, fy = fractions of the anchor's box, dx/dy = pixels), with the brush's width in pixels at
// the comp's 1536 width (w) and how much ink it carries (ink: 0 lifts the brush off the paper).
// The opening's waypoints are read off the approved crane comp.

export type Waypoint = {
  at: string;
  fx: number;
  fy: number;
  dx?: number;
  dy?: number;
  w?: number;
  ink?: number;
  /** The painter reloads the brush here: a new stroke lands, loaded. */
  fresh?: boolean;
  /** How heavily loaded the brush is from here on (1 = the page's usual stroke). */
  load?: number;
};

/** A point given in the comp's own pixels (1536 x 1000) on the opening. */
const comp = (x: number, y: number, w: number, ink = 1): Waypoint => ({
  at: "opening",
  fx: x / 1536,
  fy: y / 1000,
  w,
  ink,
});

// Crane comp: the line leaves the crane's trailing legs, rides the air to the right, flicks up
// and lifts off over the far ridges; a new stroke drops from behind the near peaks and runs down
// to the bottom left, on into the page.
const crane: Waypoint[] = [
  { at: "crane", fx: 0.477, fy: 0.786, w: 0.8, ink: 0.5 },
  comp(640, 437, 1.3),
  comp(720, 452, 1.9),
  comp(800, 458, 2.3),
  comp(880, 452, 2.5),
  comp(960, 456, 2.8),
  comp(1012, 472, 3.2),
  comp(1062, 500, 4),
  comp(1112, 519, 5),
  comp(1172, 524, 5.6),
  comp(1230, 511, 5, 0.8),
  comp(1268, 497, 3, 0.45),
  comp(1292, 490, 1, 0),
  comp(1302, 560, 0, 0),
  comp(1263, 624, 1, 0.15),
  comp(1242, 660, 2.6),
  comp(1223, 696, 3.4),
  comp(1240, 722, 4),
  comp(1249, 746, 3.6),
  comp(1218, 782, 3),
  comp(1150, 826, 2.6, 0.55),
  comp(1098, 851, 2.6),
  comp(980, 905, 3),
  comp(870, 955, 3.2),
  comp(790, 1000, 3),
  comp(700, 1060, 2.8),
];

/** A point on an anchor's box, with an optional pixel offset. */
const on = (at: string, fx: number, fy: number, w = 3.2, ink = 1, dx = 0, dy = 0): Waypoint => ({
  at,
  fx,
  fy,
  w,
  ink,
  dx,
  dy,
});

/** The point just beside a station label, where its leader line meets the brush. */
const station = (id: string, side: "left" | "right", w = 3): Waypoint =>
  side === "right"
    ? { at: `st-${id}`, fx: 0, fy: 0.5, dx: -8, w }
    : { at: `st-${id}`, fx: 1, fy: 0.5, dx: 8, w };

/** Half the scientists block's column gap (clamp(40px, 7.8vw, 120px)) at a 1440 window. */
const SPINE = -56;

// Crane page: from the landscape the line drops straight down through the gap beside "Tiny
// power plants." (past its station label), wraps the mitochondrion's lower left side, and comes
// back under the words to the gap between Dr. Liu's photograph and his record (the crane comp
// sets the headline to the right of the photo), past that station, into the photo from above.
const craneToScience: Waypoint[] = [
  station("cellular", "right", 3),
  on("cellular-mito", 0, 0.42, 3.4, 1, -54),
  on("cellular-mito", 0.04, 0.78, 3.6),
  on("cellular-mito", 0.2, 1.0, 3),
  on("cellular", 0.44, 1, 2.6, 1, 0, -14),
  station("scientists", "left", 3),
  on("liu", 0.74, 0.1, 3),
  on("liu", 0.56, 0.2, 3),
];

// Shared: behind the photograph and out at its right; down the gap between the two columns, past
// the station beside "What happens inside our cells…" and Ask BiGH Science; across to the right
// margin and the products' station; down to the bottles and under their row, as the ground they
// stand on; down the left margin beside the story painting, across above "Make sense of the
// science." and down the far side of its painting; under it to the research spine (past the
// station beside its headline), down between the sources, out around the notes and across to the
// purpose's station; then it lifts off in the open sky, before the painting.
const shared: Waypoint[] = [
  on("liu", 0.6, 0.45, 3),
  on("liu", 0.84, 0.62, 3.2),
  on("facts", 0, 0.92, 3.2, 1, SPINE),
  station("work", "left", 3.2),
  on("work-main", 0, 0.6, 3.4, 1, SPINE),
  on("ask-body", 0, 0.3, 3, 1, SPINE),
  on("ask-body", 0, 1, 2.8, 1, SPINE + 4, 46),
  on("scientists", 0.75, 1, 2.8, 1, 0, -10),
  station("products", "left", 3),
  on("bottles", 1.02, 0.55, 3.2),
  on("bottles", 0.96, 1, 3, 1, 0, 30),
  on("bottles", 0.5, 1, 2.4, 1, 0, 38),
  on("bottles", 0.04, 1, 2.6, 1, 0, 30),
  on("stories", 0.03, 0.08, 3.2),
  on("stories", 0.034, 0.5, 3.4),
  on("stories", 0.03, 0.94, 3),
  on("science", 0.25, 0, 2.6, 0.8, 0, 42),
  on("science", 0.62, 0, 3, 1, 0, 52),
  on("science-mito", 1.0, 0.08, 3.2, 1, 16),
  on("science-mito", 1.0, 0.6, 3.4, 1, 20),
  on("science-mito", 0.78, 1, 3, 1, 0, 36),
  on("research", 0.52, 0, 2.8, 1, 0, 24),
  station("research", "left", 3),
  on("research-list", 0.5, 0, 3.2, 1, 0, -8),
  on("research-list", 0.503, 0.5, 3.4),
  on("research-list", 0.5, 1, 3, 1, 0, 20),
  on("research-list", 0.76, 1, 2.6, 1, 0, 34),
  on("research-list", 1.0, 1, 2.8, 1, 10, 80),
  on("research", 0.94, 1, 2.8, 1, 0, -30),
  station("purpose", "right", 2.8),
  on("purpose-painting", 0.6, 0.27, 2.2),
  on("purpose-painting", 0.588, 0.33, 1.2, 0.5),
  on("purpose-painting", 0.582, 0.36, 0.3, 0),
];

// Phones: at 390 the gutter cannot hold a page-long line without crowding the words, so the
// page line is dropped on phones (the lead's decision, October 2): each opening keeps its own
// line, and the station labels sit under their headings with their leader lines.
const lift = (at: string, fx: number, fy: number): Waypoint => ({ at, fx, fy, w: 0, ink: 0 });

// The close, on every screen: the brush travels off the paper down to the footer, reloads, and
// lays one confident stroke under the promise ("Stay sharp. Live fully."), sagging a little in
// the middle and flicking up as it lifts. The line that left the crane ends here.
const T = "footer-tagline";
const promise: Waypoint[] = [
  { at: T, fx: -0.04, fy: 1, dy: 8, w: 0, ink: 0 },
  { at: T, fx: -0.008, fy: 1, dy: 13, w: 3, ink: 1, fresh: true, load: 2.2 },
  { at: T, fx: 0.24, fy: 1, dy: 18, w: 3, ink: 1, load: 2.2 },
  { at: T, fx: 0.56, fy: 1, dy: 19, w: 3, ink: 1, load: 2 },
  { at: T, fx: 0.84, fy: 1, dy: 14, w: 3, ink: 0.9, load: 1.8 },
  { at: T, fx: 0.97, fy: 1, dy: 8, w: 2, ink: 0.55, load: 1.5 },
  { at: T, fx: 1.02, fy: 1, dy: 0, w: 0, ink: 0 },
];

const cranePhone: Waypoint[] = [
  { at: "crane", fx: 0.477, fy: 0.786, w: 0.8, ink: 0.5 },
  on("opening-art", 0.72, 0.7, 2.4),
  on("opening-art", 0.92, 0.9, 2.2, 0.5),
  lift("opening-art", 0.97, 1.0),
];

/** The opening's waypoints, the route through the rest of the page (none on phones), and the
 *  closing stroke under the footer's promise (every screen). */
export function route(phone = false): Waypoint[] {
  return phone ? [...cranePhone, ...promise] : [...crane, ...craneToScience, ...shared, ...promise];
}
