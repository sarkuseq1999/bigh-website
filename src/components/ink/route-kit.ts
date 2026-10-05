// The brush line's route helpers, shared by every ink page (moved from the homepage's
// brush-route.ts, October 5, 2026). A route is a list of waypoints pinned to the page's own
// [data-brush] anchors; each page writes its own route from these.

export type Waypoint = {
  at: string;
  fx: number;
  fy: number;
  /** In the gap after this anchor: x is the middle between its right edge and the left edge of
   *  `at` (fx is then ignored), so the line keeps to the middle of a column gap at every width. */
  after?: string;
  /** The height is read off this anchor's box instead of `at`'s (fy, dy). */
  level?: string;
  /** Never nearer than this many pixels to that anchor: past its right edge (pixels > 0) or
   *  before its left edge (pixels < 0). Where a narrower window brings the anchor closer, the
   *  line gives way just enough. */
  clear?: [string, number];
  dx?: number;
  dy?: number;
  w?: number;
  ink?: number;
  /** The painter reloads the brush here: a new stroke lands, loaded. */
  fresh?: boolean;
  /** How heavily loaded the brush is from here on (1 = the page's usual stroke). */
  load?: number;
};

/** A point on an anchor's box, with an optional pixel offset. */
export const on = (
  at: string,
  fx: number,
  fy: number,
  w = 3.2,
  ink = 1,
  dx = 0,
  dy = 0,
): Waypoint => ({
  at,
  fx,
  fy,
  w,
  ink,
  dx,
  dy,
});

/** The point just beside a station label, where its leader line meets the brush. */
export const station = (id: string, side: "left" | "right", w = 3): Waypoint =>
  side === "right"
    ? { at: `st-${id}`, fx: 0, fy: 0.5, dx: -8, w }
    : { at: `st-${id}`, fx: 1, fy: 0.5, dx: 8, w };

/** A point in the middle of the gap between two columns (`after` is the left one). */
export const gap = (after: string, at: string, fy: number, dx = 0, dy = 0, ink = 1): Waypoint => ({
  at,
  after,
  fx: 0,
  fy,
  dx,
  dy,
  w: 3,
  ink,
});

/** The painter reloads here: a new stroke lands, loaded. */
export const fresh = (point: Waypoint, load?: number): Waypoint => ({
  ...point,
  fresh: true,
  load,
});

/** A point where the brush is off the paper (no width, no ink): the line lifts off here. */
export const lift = (at: string, fx: number, fy: number): Waypoint => ({
  at,
  fx,
  fy,
  w: 0,
  ink: 0,
});

/** One short, lightly loaded stroke along the top edge of a block: a rule the brush paints. */
export const rule = (at: string): Waypoint[] => [
  { at, fx: -0.02, fy: 0, dy: -2, w: 0, ink: 0 },
  { at, fx: 0, fy: 0, dy: 0, w: 2, ink: 1, fresh: true, load: 0.62 },
  { at, fx: 0.4, fy: 0, dy: 2, w: 2, ink: 1, load: 0.58 },
  { at, fx: 0.8, fy: 0, dy: 1, w: 2, ink: 0.8, load: 0.5 },
  { at, fx: 1, fy: 0, dy: -1, w: 1, ink: 0.4, load: 0.42 },
  { at, fx: 1.02, fy: 0, dy: -4, w: 0, ink: 0 },
];

/** Which page the line is drawn on: the phone's own opening (720 px and under), the comp's
 *  opening over one-column blocks (721 to 899 px), or the two-column page (900 px and up). */
export type Layout = "phone" | "column" | "page";

// The close, on every screen: the brush travels off the paper down to the footer, reloads, and
// lays one confident stroke under the promise ("Stay sharp. Live fully.") and the crane at rest
// beside it (the ground it stands on), sagging a little in the middle, still loaded under the
// crane's feet (they stand at about 0.88 of the band), and flicking up as it lifts past its
// tail. The line that left the crane in flight ends under the crane at rest.
const T = "footer-promise";
export const footerEnding: Waypoint[] = [
  { at: T, fx: -0.04, fy: 1, dy: 8, w: 0, ink: 0 },
  { at: T, fx: -0.008, fy: 1, dy: 13, w: 3, ink: 1, fresh: true, load: 2.2 },
  { at: T, fx: 0.24, fy: 1, dy: 18, w: 3, ink: 1, load: 2.2 },
  { at: T, fx: 0.56, fy: 1, dy: 19, w: 3, ink: 1, load: 2 },
  { at: T, fx: 0.88, fy: 1, dy: 14, w: 3, ink: 1, load: 1.9 },
  { at: T, fx: 1.0, fy: 1, dy: 8, w: 2.4, ink: 0.7, load: 1.6 },
  { at: T, fx: 1.06, fy: 1, dy: 0, w: 0, ink: 0 },
];
