import {
  footerEnding,
  fresh,
  lift,
  on,
  rule,
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
const promises: Waypoint[] = [0, 1, 2, 3].flatMap((i) => rule(`promise-${i}`));

// The stroke grows out of the wash under the cell's membrane (thin and light), swells as it
// leaves the painting, and sweeps over the open paper under the opening's words to the first
// station, where it turns down the margin.
const page: Waypoint[] = [
  on("about-cell", 0.3, 0.905, 1.2, 0.5),
  on("about-cell", 0.22, 0.97, 3),
  on("about-cell", -0.12, 1.12, 3.8),
  // Above the first station the sweep turns down in one broad bend (fixed pixels from the
  // station, so the bend keeps its size at every width, and below the opening, so the page's
  // own stroke paints it), reaching the leader as the vertical, without swinging out past it.
  on("st-purpose", 1, 0.5, 3.6, 1, 72, -92),
  on("st-purpose", 1, 0.5, 3.4, 1, 22, -46),
  fresh(station("purpose", "left"), 1),
  station("roots", "left"),
  fresh(station("roots", "left")),
  fresh(station("experience", "left")),
  fresh(station("promise", "left")),
  // Past the last station the brush runs on a little and lifts, tapering straight down.
  { ...lift("st-promise", 1, 3.6), dx: 6 },
];

export function aboutRoute(layout: Layout): Waypoint[] {
  if (layout === "page") return [...page, ...promises, ...footerEnding];
  return [...promises, ...footerEnding];
}
