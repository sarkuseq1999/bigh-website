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

/** A point given in the comp's own pixels (1536 x 1000) on the opening's stage (the frame its
 *  paintings sit on: the whole opening, until a wide window lets the page's column centre). */
const comp = (x: number, y: number, w: number, ink = 1): Waypoint => ({
  at: "opening-stage",
  fx: x / 1536,
  fy: y / 1000,
  w,
  ink,
});

/** A point on the crane's flight path, in the comp's pixels: measured down from the crane's top
 *  edge (y 100 in the comp) at the comp's scale, so the stroke leaves the crane the same way
 *  when the opening is taller than the comp. At the comp's own shape it is `comp` exactly. */
const flight = (x: number, y: number, w: number, ink = 1): Waypoint => ({
  at: "opening-flight",
  fx: x / 1536,
  fy: (y - 100) / 1000,
  w,
  ink,
});

// Crane comp: the line leaves the crane's trailing legs, rides the air to the right, flicks up
// and lifts off over the far ridges...
const craneFlight: Waypoint[] = [
  { at: "crane", fx: 0.477, fy: 0.786, w: 0.8, ink: 0.5 },
  flight(640, 437, 1.3),
  flight(720, 452, 1.9),
  flight(800, 458, 2.3),
  flight(880, 452, 2.5),
  flight(960, 456, 2.8),
  flight(1012, 472, 3.2),
  flight(1062, 500, 4),
  flight(1112, 519, 5),
  flight(1172, 524, 5.6),
  flight(1230, 511, 5, 0.8),
  flight(1268, 497, 3, 0.45),
  flight(1292, 490, 1, 0),
];

// ...a new stroke drops from behind the near peaks and runs down to the bottom left, on into the
// page. (Between the phone and the two-column page, 721 to 899 px, there is no page for it to
// run into and the words no longer shrink out of its way: there the opening keeps the flight
// stroke alone, as the phone's opening keeps its own.)
const crane: Waypoint[] = [
  ...craneFlight,
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
// sets the headline to the right of the photo), past that station, and bows in toward the print
// ("liu" is the mat), running down beside it, never under it, like a stroke framing a print.
const craneToScience: Waypoint[] = [
  station("cellular", "right", 3),
  on("cellular-mito", 0, 0.42, 3.4, 1, -54),
  on("cellular-mito", 0.04, 0.78, 3.6),
  on("cellular-mito", 0.2, 1.0, 3),
  on("cellular", 0.44, 1, 2.6, 1, 0, -14),
  station("scientists", "left", 3),
  on("liu", 1, 0.18, 3, 1, 36),
];

// Shared: down beside the print, easing out past its lower corner (clear of his name); down the
// gap between the two columns, past the station beside "What happens inside our cells…" and Ask
// BiGH Science; on down the same gap into the products, past their station and between the big
// bottle and its words; there the brush reloads and lays one stroke under the bottle, the ground
// it stands on (as the crane at rest stands on the closing stroke), and runs on into the left
// margin, past the picker and down beside the story painting; across above "Make sense of the
// science." and down the far side of its painting; under it to the research spine (past the
// station beside its headline), down between the sources, out around the notes and across to the
// purpose's station; then it lifts off in the open sky, before the painting.
const shared: Waypoint[] = [
  on("liu", 1, 0.52, 3.2, 1, 24),
  on("liu", 1, 0.94, 3.2, 1, 38),
  station("work", "left", 3.2),
  on("work-main", 0, 0.6, 3.4, 1, SPINE),
  on("ask-body", 0, 0.3, 3, 1, SPINE),
  on("ask-body", 0, 1, 2.8, 1, SPINE + 4, 46),
  station("products", "right", 3),
  on("product-spine", 0, 0.28, 3),
  on("product-spine", 0, 0.66, 2.6),
  { at: "product-spine", fx: 0, fy: 0.86, dx: -6, w: 3, fresh: true, load: 1.2 },
  { at: "stage", fx: 0.9, fy: 0.974, w: 3.4, load: 1.7 },
  { at: "stage", fx: 0.62, fy: 0.982, w: 3.8, load: 1.9 },
  { at: "stage", fx: 0.36, fy: 0.982, w: 3.8, load: 1.8 },
  { at: "stage", fx: 0.1, fy: 0.97, w: 3.2, load: 1.4 },
  { at: "stage", fx: 0, fy: 1, dx: -46, dy: 64, w: 2.8, load: 1 },
  on("bottles", 0, 0.5, 2.8, 1, -40),
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
// line, and the station labels sit under their headings with their leader lines. The same holds
// wherever the blocks are one column (under 900 px): the route above is drawn for two columns
// and would run through the words.
const lift = (at: string, fx: number, fy: number): Waypoint => ({ at, fx, fy, w: 0, ink: 0 });

// The close, on every screen: the brush travels off the paper down to the footer, reloads, and
// lays one confident stroke under the promise ("Stay sharp. Live fully.") and the crane at rest
// beside it (the ground it stands on), sagging a little in the middle, still loaded under the
// crane's feet (they stand at about 0.88 of the band), and flicking up as it lifts past its
// tail. The line that left the crane in flight ends under the crane at rest.
/** One short, lightly loaded stroke along the top edge of a block: a rule the brush paints. */
const rule = (at: string): Waypoint[] => [
  { at, fx: -0.02, fy: 0, dy: -2, w: 0, ink: 0 },
  { at, fx: 0, fy: 0, dy: 0, w: 2, ink: 1, fresh: true, load: 0.62 },
  { at, fx: 0.4, fy: 0, dy: 2, w: 2, ink: 1, load: 0.58 },
  { at, fx: 0.8, fy: 0, dy: 1, w: 2, ink: 0.8, load: 0.5 },
  { at, fx: 1, fy: 0, dy: -1, w: 1, ink: 0.4, load: 0.42 },
  { at, fx: 1.02, fy: 0, dy: -4, w: 0, ink: 0 },
];

// Before the close, on every screen: the brush touches down three times, one rule over each of
// the three standards we keep.
const standards: Waypoint[] = [0, 1, 2].flatMap((i) => rule(`standard-${i}`));

const T = "footer-promise";
const promise: Waypoint[] = [
  { at: T, fx: -0.04, fy: 1, dy: 8, w: 0, ink: 0 },
  { at: T, fx: -0.008, fy: 1, dy: 13, w: 3, ink: 1, fresh: true, load: 2.2 },
  { at: T, fx: 0.24, fy: 1, dy: 18, w: 3, ink: 1, load: 2.2 },
  { at: T, fx: 0.56, fy: 1, dy: 19, w: 3, ink: 1, load: 2 },
  { at: T, fx: 0.88, fy: 1, dy: 14, w: 3, ink: 1, load: 1.9 },
  { at: T, fx: 1.0, fy: 1, dy: 8, w: 2.4, ink: 0.7, load: 1.6 },
  { at: T, fx: 1.06, fy: 1, dy: 0, w: 0, ink: 0 },
];

const cranePhone: Waypoint[] = [
  { at: "crane", fx: 0.477, fy: 0.786, w: 0.8, ink: 0.5 },
  on("opening-art", 0.72, 0.7, 2.4),
  on("opening-art", 0.92, 0.9, 2.2, 0.5),
  lift("opening-art", 0.97, 1.0),
];

/** Which page the line is drawn on: the phone's own opening (720 px and under), the comp's
 *  opening over one-column blocks (721 to 899 px), or the two-column page (900 px and up). */
export type Layout = "phone" | "column" | "page";

/** The opening's waypoints, the route through the rest of the page (only where the blocks are
 *  two columns), then the three standards' rules and the closing stroke under the footer's
 *  promise (every screen). */
export function route(layout: Layout): Waypoint[] {
  if (layout === "phone") return [...cranePhone, ...standards, ...promise];
  if (layout === "column") return [...craneFlight, ...standards, ...promise];
  return [...crane, ...craneToScience, ...shared, ...standards, ...promise];
}
