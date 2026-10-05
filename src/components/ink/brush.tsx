"use client";

import { useEffect, useRef } from "react";
import type { Layout, Waypoint } from "./route-kit";
import styles from "./brush.module.css";

// The page's signature: one continuous ink brush line that draws itself down the whole page as
// you scroll, from the crane's flight path through every block to the
// purpose. It is painted, not traced: one continuous stroke envelope with calligraphic width and
// paper-tooth edges; the painter reloads where something begins (about every thousand pixels:
// beside a station, under the big bottle, where the brush lands again), so each stroke lands
// loaded at a place that means something and tapers thin, and as the ink runs out dry-brush
// streaks (flying white) open up inside the stroke. In the crane opening the line keeps the
// approved hero's own stroke. The brush lifts off the paper where the route says so (ink 0), and
// reloads where it says so (fresh): the page ends on one loaded stroke under the footer's promise.
// Section labels ([data-station]) are pinned to the line and appear as the brush reaches them.
//
// The route is a list of waypoints pinned to the blocks' own elements ([data-brush] anchors),
// measured on every layout change, so the line follows the real page at every width. The page
// is cut into horizontal canvas tiles that scroll natively with the content (no jitter); only
// tiles near the window hold pixels, and only the tile where the brush is moving redraws.
// Once painted, ink stays. Reduced motion: the whole line, still, from the first frame.

type Sample = {
  x: number;
  y: number;
  nx: number;
  ny: number;
  s: number;
  w: number;
  ink: number;
  /** Each edge's own raggedness (fraction of the half width). */
  jl: number;
  jr: number;
  /** The width before the opening stroke's breathing pressure, for the bristle brush. */
  wb: number;
  /** How dry the bristle brush is here (0 wet, 1 dry). */
  dry: number;
  /** True inside the crane opening: painted with the hero's own calligraphic stroke. */
  classic: boolean;
  /** The painter reloads here: a new stroke begins. */
  fresh: boolean;
  /** How heavily the brush is loaded (1 = the page's usual stroke). */
  load: number;
  /** How sharply the line turns here (0 straight, toward 1 a hairpin). */
  turn: number;
  /** The anchors of the two waypoints this sample lies between (for checks: where it lifts). */
  from: string;
  to: string;
};

const TILE = 1200;
const STEP = 2;
const INK = "rgb(20, 19, 17)";

function hash(i: number, seed: number) {
  let h = (Math.imul(i, 374761393) + Math.imul(seed, 668265263)) | 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  return ((h ^ (h >>> 16)) >>> 0) / 4294967295;
}

/** Smooth 1D value noise in 0..1. */
function noise(x: number, seed: number) {
  const i = Math.floor(x);
  const f = x - i;
  const u = f * f * (3 - 2 * f);
  const a = hash(i, seed);
  return a + (hash(i + 1, seed) - a) * u;
}

function smooth(edge0: number, edge1: number, x: number) {
  const t = Math.min(1, Math.max(0, (x - edge0) / (edge1 - edge0)));
  return t * t * (3 - 2 * t);
}

type Point = {
  at: string;
  x: number;
  y: number;
  w: number;
  ink: number;
  fresh: boolean;
  load: number;
};

/** Measure the route's waypoints on the page, relative to the look's root. */
function measure(root: HTMLElement, waypoints: Waypoint[]): Point[] {
  const origin = root.getBoundingClientRect();
  const points: Point[] = [];
  const boxes = new Map<string, DOMRect | null>();
  const boxOf = (at: string) => {
    if (!boxes.has(at)) {
      const element = root.querySelector<HTMLElement>(`[data-brush="${at}"]`);
      boxes.set(at, element ? element.getBoundingClientRect() : null);
    }
    return boxes.get(at);
  };
  for (const point of waypoints) {
    const box = boxOf(point.at);
    if (!box || box.width === 0) continue;
    const before = point.after ? boxOf(point.after) : null;
    if (point.after && (!before || before.width === 0)) continue;
    let x =
      (before ? (before.right + box.left) / 2 : box.left + box.width * point.fx) + (point.dx ?? 0);
    const keep = point.clear ? boxOf(point.clear[0]) : null;
    if (point.clear && keep && keep.width > 0) {
      const [, by] = point.clear;
      x = by > 0 ? Math.max(x, keep.right + by) : Math.min(x, keep.left + by);
    }
    const rows = point.level ? boxOf(point.level) : box;
    if (!rows || rows.height === 0) continue;
    points.push({
      at: point.at,
      x: x - origin.left,
      y: rows.top - origin.top + rows.height * point.fy + (point.dy ?? 0),
      w: point.w ?? 3,
      ink: point.ink ?? 1,
      fresh: point.fresh ?? false,
      load: point.load ?? 1,
    });
  }
  return points;
}

/** Centripetal Catmull-Rom through the points, sampled every STEP px. */
function sample(points: Point[], scale: number): Sample[] {
  const out: Sample[] = [];
  if (points.length < 2) return out;
  const pts = [points[0], ...points, points[points.length - 1]];
  let s = 0;
  let prev: { x: number; y: number } | null = null;
  for (let i = 1; i < pts.length - 2; i++) {
    const [p0, p1, p2, p3] = [pts[i - 1], pts[i], pts[i + 1], pts[i + 2]];
    const chord = Math.hypot(p2.x - p1.x, p2.y - p1.y);
    const n = Math.max(2, Math.ceil(chord / STEP));
    const t01 = Math.pow(Math.hypot(p1.x - p0.x, p1.y - p0.y), 0.5) || 1e-4;
    const t12 = Math.pow(chord, 0.5) || 1e-4;
    const t23 = Math.pow(Math.hypot(p3.x - p2.x, p3.y - p2.y), 0.5) || 1e-4;
    // Tangents (Barry-Goldman form, scaled to the 1-2 segment).
    const m1x = (p1.x - p0.x) / t01 - (p2.x - p0.x) / (t01 + t12) + (p2.x - p1.x) / t12;
    const m1y = (p1.y - p0.y) / t01 - (p2.y - p0.y) / (t01 + t12) + (p2.y - p1.y) / t12;
    const m2x = (p2.x - p1.x) / t12 - (p3.x - p1.x) / (t12 + t23) + (p3.x - p2.x) / t23;
    const m2y = (p2.y - p1.y) / t12 - (p3.y - p1.y) / (t12 + t23) + (p3.y - p2.y) / t23;
    for (let k = i === 1 ? 0 : 1; k <= n; k++) {
      const t = k / n;
      const t2 = t * t;
      const t3 = t2 * t;
      const h00 = 2 * t3 - 3 * t2 + 1;
      const h10 = t3 - 2 * t2 + t;
      const h01 = -2 * t3 + 3 * t2;
      const h11 = t3 - t2;
      const x = h00 * p1.x + h10 * m1x * t12 + h01 * p2.x + h11 * m2x * t12;
      const y = h00 * p1.y + h10 * m1y * t12 + h01 * p2.y + h11 * m2y * t12;
      if (prev) s += Math.hypot(x - prev.x, y - prev.y);
      prev = { x, y };
      const e = smooth(0, 1, t);
      out.push({
        x,
        y,
        nx: 0,
        ny: 0,
        s,
        w: (p1.w + (p2.w - p1.w) * e) * scale,
        ink: p1.ink + (p2.ink - p1.ink) * e,
        jl: 1,
        jr: 1,
        wb: 0,
        dry: 0,
        classic: false,
        fresh: p1.fresh && k === (i === 1 ? 0 : 1),
        load: p1.load + (p2.load - p1.load) * e,
        turn: 0,
        from: p1.at,
        to: p2.at,
      });
    }
  }
  // Normals, from neighbours.
  for (let i = 0; i < out.length; i++) {
    const a = out[Math.max(0, i - 1)];
    const b = out[Math.min(out.length - 1, i + 1)];
    const len = Math.hypot(b.x - a.x, b.y - a.y) || 1;
    out[i].nx = -(b.y - a.y) / len;
    out[i].ny = (b.x - a.x) / len;
  }
  // The brush's own life: pressure that swells on the slow turns and thins on the long sweeps,
  // a slower breath of pressure on top, and two edges that each catch the paper's grain.
  const span = 7;
  for (let i = 0; i < out.length; i++) {
    const p = out[i];
    const a = out[Math.max(0, i - span)];
    const b = out[Math.min(out.length - 1, i + span)];
    const turn = Math.abs(a.nx * b.ny - a.ny * b.nx);
    p.turn = turn;
    const press = 1 + 0.7 * smooth(0.04, 0.34, turn);
    const breath = 0.32 + 1.45 * Math.pow(noise(p.s / 310, 7), 1.4);
    const grain = 0.9 + 0.2 * noise(p.s / 9, 11);
    const loaded = Math.pow(Math.max(0, p.ink), 0.55);
    p.wb = p.w * press * grain * loaded;
    p.w = p.w * 1.18 * press * breath * grain * loaded;
    p.jl = 0.86 + 0.28 * noise(p.s / 6.5, 31);
    p.jr = 0.86 + 0.28 * noise(p.s / 7.5, 37);
  }
  return out;
}

/** The longest stroke one load of ink makes; a longer one is shared out into even loads. */
const STROKE_MAX = 1500;
/** A stroke that ends by lifting off the paper still has ink when it lifts (the ground under the
 *  big bottle, the three rules, the closing stroke): its ink lasts as if it ran this far. */
const STROKE_LIFT = 1150;

/**
 * The brush's life below the opening. The painter reloads where the route says (fresh: beside a
 * station, under the big bottle, where the brush touches down again), so each stroke lands loaded
 * at a place that means something (about 3.6 px at the comp's width) and has thinned toward
 * about 1 px and dried by the next reload; a stroke longer than STROKE_MAX is shared out into even
 * loads. Along the way the hand slows and presses a little wider where the line turns, and the
 * pressure breathes on the long runs, so no stretch is mechanically even. Where the route lifts
 * the brush (ink 0) the stroke tapers to nothing and ends. Samples above `classicUntil` (page y)
 * keep the opening's own stroke, untouched.
 */
function material(samples: Sample[], classicUntil: number, scale: number) {
  let start = -1;
  for (let i = 0; i < samples.length; i++) {
    const p = samples[i];
    p.classic = start < 0 && p.y < classicUntil;
    if (!p.classic && start < 0) start = i;
  }
  if (start < 0) return;
  // Where each stroke begins: the first page sample, then every reload.
  const strokes = [start];
  for (let i = start + 1; i < samples.length; i++) if (samples[i].fresh) strokes.push(i);
  for (let k = 0; k < strokes.length; k++) {
    const a = strokes[k];
    const b = k + 1 < strokes.length ? strokes[k + 1] : samples.length;
    // The stroke's ink ends at the next reload, or earlier where the brush lifts off the paper.
    let end = b - 1;
    for (let i = a + 1; i < b; i++) {
      if (samples[i].ink < 0.02) {
        end = i;
        break;
      }
    }
    const lifts = end < b - 1;
    const run = samples[end].s - samples[a].s;
    const total = lifts ? Math.max(run, STROKE_LIFT) : Math.max(run, 400);
    const loads = Math.max(1, Math.ceil(total / STROKE_MAX));
    const length = total / loads;
    for (let i = a; i < b; i++) {
      const p = samples[i];
      const along = p.s - samples[a].s;
      const piece = Math.min(loads - 1, Math.floor(along / length));
      const into = along - piece * length;
      const phase = Math.min(1, into / length);
      // The first stroke picks up where the opening's line leaves off, already loaded; every
      // other one lands, pressing to its full load over its first few dozen pixels.
      const first = k === 0 && piece === 0;
      const land = first ? 1 : smooth(0, 36 * scale, into);
      const load = land * Math.pow(1 - phase, 0.85);
      const loaded = Math.pow(Math.max(0, p.ink), 0.6);
      const width = (1.0 + 2.6 * load) * scale * loaded * p.load;
      if (first) {
        // The opening's own line (and on a phone, the opening's whole stroke) as approved.
        p.w = width * (0.92 + 0.16 * noise(p.s / 90, 13));
      } else {
        // The brush's head where it lands: it presses down, then lifts a little into the stroke.
        const head = 1 + 0.42 * smooth(4, 22, into) * (1 - smooth(26, 90, into));
        const press = 1 + 0.35 * smooth(0.05, 0.3, p.turn);
        const breath = 0.78 + 0.3 * noise(p.s / 340, 13) + 0.14 * noise(p.s / 80, 19);
        p.w = width * head * press * breath;
      }
      p.dry = Math.min(1, Math.max(smooth(0.16, 0.9, phase), (1 - p.ink) * 1.2));
    }
  }
  for (let i = start; i < samples.length; i++) {
    const p = samples[i];
    // Paper tooth: each edge catches the fibres on its own, more as the brush dries.
    const tooth = 0.18 + 0.22 * p.dry;
    p.jl = 1 - tooth / 2 + tooth * noise(p.s / 1.7, 31) + 0.08 * noise(p.s / 11, 33);
    p.jr = 1 - tooth / 2 + tooth * noise(p.s / 1.9, 37) + 0.08 * noise(p.s / 13, 39);
  }
  // Join the opening's line without a seam: the first page sample overlaps the last classic one.
  if (start > 0) samples[start - 1].w = Math.max(samples[start - 1].w, samples[start].w);
}

/**
 * Where the drawn line is off the paper: each run of samples too thin to paint (the painters'
 * own thresholds), as [the anchor it lifts after, the anchor it lands at, its length along the
 * path, its top, its bottom] in page pixels. Published on the layer for the checks, so the
 * route's lifts can be held to a list of designed ones.
 */
function lifts(samples: Sample[]) {
  const out: [string, string, number, number, number][] = [];
  let a = -1;
  for (let i = 0; i <= samples.length; i++) {
    const p = samples[i];
    const off = !!p && p.w <= (p.classic ? 0.25 : 0.2);
    if (off && a < 0) a = i;
    if (!off && a >= 0) {
      const run = samples.slice(a, i);
      const ys = run.map((q) => q.y);
      const [first, last] = [run[0], run[run.length - 1]];
      const length = Math.round(last.s - first.s);
      out.push([
        first.from,
        last.to,
        length,
        Math.round(Math.min(...ys)),
        Math.round(Math.max(...ys)),
      ]);
      a = -1;
    }
  }
  return out;
}

/**
 * The page's ink stroke: one continuous envelope with calligraphic width and paper-tooth edges,
 * a faint bleed into the fibres, and dry-brush streaks cut INSIDE the envelope where the brush
 * runs dry (flying white): the outer edges always hold, so the stroke never breaks into dashes.
 */
function paintInk(
  ctx: CanvasRenderingContext2D,
  samples: Sample[],
  from: number,
  to: number,
  head: number,
) {
  let end = to;
  while (end > from && samples[end].s > head) end--;
  if (end - from < 1) return;
  // Runs of page samples (one sample of overlap into the opening's line, for a seamless join).
  const runs: [number, number][] = [];
  let begin = -1;
  for (let i = from; i <= end; i++) {
    const page = !samples[i].classic && samples[i].w > 0.2;
    if (page && begin < 0) begin = Math.max(from, i - 1);
    if (!page && begin >= 0) {
      if (i - 1 - begin >= 1) runs.push([begin, i - 1]);
      begin = -1;
    }
  }
  if (begin >= 0 && end - begin >= 1) runs.push([begin, end]);
  if (!runs.length) return;
  const width = (i: number) => {
    const p = samples[i];
    return p.w * (0.3 + 0.7 * smooth(0, 34, head - p.s));
  };
  const outline = (a: number, b: number, spread: number, pad: number) => {
    ctx.beginPath();
    for (let i = a; i <= b; i++) {
      const p = samples[i];
      const w = (width(i) / 2) * p.jl * spread + pad;
      if (i === a) ctx.moveTo(p.x + p.nx * w, p.y + p.ny * w);
      else ctx.lineTo(p.x + p.nx * w, p.y + p.ny * w);
    }
    for (let i = b; i >= a; i--) {
      const p = samples[i];
      const w = (width(i) / 2) * p.jr * spread + pad;
      ctx.lineTo(p.x - p.nx * w, p.y - p.ny * w);
    }
    ctx.closePath();
    ctx.fill();
  };
  ctx.globalCompositeOperation = "source-over";
  ctx.fillStyle = INK;
  ctx.globalAlpha = 0.12;
  for (const [a, b] of runs) outline(a, b, 1.5, 0.3);
  ctx.globalAlpha = 0.78;
  for (const [a, b] of runs) outline(a, b, 1, 0);

  // Flying white: where the brush runs dry, the paper shows through in streaks INSIDE the
  // envelope (its edges always hold), and the ink thins in patches along the stroke.
  ctx.globalCompositeOperation = "destination-out";
  ctx.lineCap = "butt";
  const lanes = [-0.2, 0, 0.2];
  for (const [a, b] of runs) {
    for (let i = a; i < b; i += 2) {
      const p = samples[i];
      if (p.classic || p.dry < 0.08) continue;
      const w = width(i);
      const q = samples[Math.min(b, i + 2)];
      const wq = width(Math.min(b, i + 2));
      // Patchy density across the whole stroke.
      const thin = p.dry * (noise(p.s / 22, 251) * 0.55 + noise(p.s / 5, 257) * 0.2) - 0.08;
      if (thin > 0) {
        ctx.globalAlpha = Math.min(0.5, thin);
        ctx.lineWidth = w * 0.62;
        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(q.x, q.y);
        ctx.stroke();
      }
      // Thin passages only thin out; streaks need a stroke wide enough to hold them inside.
      if (w < 2.6) continue;
      lanes.forEach((lane, k) => {
        const streak = noise(p.s / (9 + 5 * k), 211 + k) * 0.8 + noise(p.s / 3, 223 + k) * 0.35;
        const cut = p.dry * 1.2 + streak - 1.05;
        if (cut <= 0) return;
        const off = lane + (noise(p.s / 40, 241 + k) - 0.5) * 0.1;
        ctx.globalAlpha = Math.min(0.95, cut * 2.2);
        ctx.lineWidth = Math.max(0.3, w * 0.15);
        ctx.beginPath();
        ctx.moveTo(p.x + p.nx * w * off, p.y + p.ny * w * off);
        ctx.lineTo(q.x + q.nx * wq * off, q.y + q.ny * wq * off);
        ctx.stroke();
      });
    }
  }
  ctx.globalCompositeOperation = "source-over";
  ctx.globalAlpha = 1;
}

/** Paint the samples from `from` to `to` (indices), up to arc length `head`. */
function paint(
  ctx: CanvasRenderingContext2D,
  samples: Sample[],
  from: number,
  to: number,
  head: number,
) {
  let end = to;
  while (end > from && samples[end].s > head) end--;
  if (end - from < 1) return;
  const widths: number[] = [];
  for (let i = from; i <= end; i++) {
    const p = samples[i];
    // The tip of the moving brush tapers, like a brush lifting as it travels.
    const tip = 0.3 + 0.7 * smooth(0, 26, head - p.s);
    widths.push(p.w * tip);
  }
  // Body: one filled outline with calligraphic width, laid twice: a wider, faint pass where the
  // ink bleeds into the paper's fibres, then the stroke itself. Runs where the ink is gone break
  // it up.
  ctx.globalCompositeOperation = "source-over";
  ctx.fillStyle = INK;
  const outline = (a: number, b: number, spread: number) => {
    ctx.beginPath();
    for (let i = a; i <= b; i++) {
      const p = samples[i];
      const w = (widths[i - from] / 2) * p.jl * spread + (spread > 1 ? 0.35 : 0);
      if (i === a) ctx.moveTo(p.x + p.nx * w, p.y + p.ny * w);
      else ctx.lineTo(p.x + p.nx * w, p.y + p.ny * w);
    }
    for (let i = b; i >= a; i--) {
      const p = samples[i];
      const w = (widths[i - from] / 2) * p.jr * spread + (spread > 1 ? 0.35 : 0);
      ctx.lineTo(p.x - p.nx * w, p.y - p.ny * w);
    }
    ctx.closePath();
    ctx.fill();
  };
  const runsOf: [number, number][] = [];
  let start = -1;
  for (let i = from; i <= end; i++) {
    const visible = widths[i - from] > 0.25 && samples[i].classic;
    if (visible && start < 0) start = i;
    if (!visible && start >= 0) {
      if (i - 1 - start >= 1) runsOf.push([start, i - 1]);
      start = -1;
    }
  }
  if (start >= 0 && end - start >= 1) runsOf.push([start, end]);
  ctx.globalAlpha = 0.16;
  for (const [a, b] of runsOf) outline(a, b, 1.35);
  ctx.globalAlpha = 0.8;
  for (const [a, b] of runsOf) outline(a, b, 1);

  // Dry brush: bristle streaks lifted out of the body where the ink runs low or the stroke is
  // wide, so the paper shows through in fine lines.
  ctx.globalCompositeOperation = "destination-out";
  ctx.lineCap = "round";
  const strands = [-0.36, -0.22, -0.08, 0.06, 0.2, 0.33];
  strands.forEach((offset, k) => {
    for (let i = from; i < end; i += 3) {
      const p = samples[i];
      const w = widths[i - from];
      if (w < 2.2 || !p.classic) continue;
      // Flying white: where the ink runs low, and in long dry passages the brush finds on its own.
      const load = 0.5 + 0.5 * noise(p.s / 520, 41);
      const dry =
        (1 - p.ink) * 1.4 + (noise(p.s / 38 + k * 9.7, 23 + k) - 0.62) * 1.6 + (0.45 - load);
      if (dry <= 0.04) continue;
      const q = samples[Math.min(end, i + 3)];
      const wq = widths[Math.min(end, i + 3) - from];
      ctx.globalAlpha = Math.min(0.9, dry * 1.1);
      ctx.lineWidth = Math.max(0.4, w * 0.085);
      ctx.beginPath();
      ctx.moveTo(p.x + p.nx * w * offset, p.y + p.ny * w * offset);
      ctx.lineTo(q.x + q.nx * wq * offset, q.y + q.ny * wq * offset);
      ctx.stroke();
    }
  });
  // A fine brush leaves its bristles' parting down the middle of a thin stroke: a faint lighter
  // seam that comes and goes.
  for (let i = from; i < end; i += 2) {
    const p = samples[i];
    const w = widths[i - from];
    if (w < 1.5 || w > 5.5 || !p.classic) continue;
    const seam = noise(p.s / 70, 53) - 0.35;
    if (seam <= 0) continue;
    const q = samples[Math.min(end, i + 2)];
    const offset = (noise(p.s / 120, 59) - 0.5) * 0.3;
    ctx.globalAlpha = Math.min(0.55, seam * 0.9);
    ctx.lineWidth = Math.max(0.35, w * 0.26);
    ctx.beginPath();
    ctx.moveTo(p.x + p.nx * w * offset, p.y + p.ny * w * offset);
    ctx.lineTo(q.x + q.nx * w * offset, q.y + q.ny * w * offset);
    ctx.stroke();
  }
  ctx.globalCompositeOperation = "source-over";
  ctx.globalAlpha = 1;
}

type Tile = { index: number; canvas: HTMLCanvasElement; drawn: number; live: boolean };

export function BrushLine({
  motion,
  route,
}: {
  motion: boolean;
  /**
   * The page's route for each layout (the page's own [data-brush] anchors). Pass a stable
   * reference (a module-level function): the layer is rebuilt whenever the route's identity changes.
   */
  route: (layout: Layout) => Waypoint[];
}) {
  const layer = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const host = layer.current;
    const root = host?.parentElement;
    if (!host || !root) return;
    let samples: Sample[] = [];
    // Per tile: index ranges of samples that fall inside it (with a margin for the brush width).
    let runs: [number, number][][] = [];
    let tiles: Tile[] = [];
    let head = 0;
    let target = 0;
    let introDone = !motion;
    let raf = 0;
    let dpr = Math.min(2, window.devicePixelRatio || 1);
    let width = 0;
    let stations: { element: HTMLElement; s: number }[] = [];

    const layout = () => {
      dpr = Math.min(2, window.devicePixelRatio || 1);
      width = root.clientWidth;
      const scale = Math.min(1.15, Math.max(0.62, width / 1536));
      // The same breakpoints as the stylesheets: the phone's own opening at 720 px and under,
      // the two-column page (the one the page line is routed through) from 900 px.
      const layout: Layout = window.matchMedia("(max-width: 720px)").matches
        ? "phone"
        : window.matchMedia("(min-width: 900px)").matches
          ? "page"
          : "column";
      samples = sample(measure(root, route(layout)), scale);
      const top = root.getBoundingClientRect().top;
      const hero = root.querySelector<HTMLElement>('[data-brush="opening"]');
      const heroBottom = hero ? hero.getBoundingClientRect().bottom - top : 0;
      material(samples, layout === "phone" ? -1 : heroBottom, scale);
      host.dataset.lifts = JSON.stringify(lifts(samples));
      host.dataset.layout = layout;
      // Each section label is reached when the brush comes level with it.
      stations = [...root.querySelectorAll<HTMLElement>("[data-station]")].map((element) => {
        const box = element.getBoundingClientRect();
        const y = box.top - top + box.height / 2;
        let at = samples.length ? samples[samples.length - 1].s : 0;
        for (const p of samples) {
          if (p.y >= y) {
            at = p.s;
            break;
          }
        }
        return { element, s: at };
      });
      const height = root.offsetHeight;
      const count = Math.ceil(height / TILE);
      host.style.height = `${height}px`;
      tiles.forEach((tile) => tile.canvas.remove());
      tiles = [];
      runs = [];
      for (let t = 0; t < count; t++) {
        const top = t * TILE - 24;
        const bottom = (t + 1) * TILE + 24;
        const list: [number, number][] = [];
        let a = -1;
        samples.forEach((p, i) => {
          const inside = p.y >= top && p.y <= bottom;
          if (inside && a < 0) a = Math.max(0, i - 1);
          if (!inside && a >= 0) {
            list.push([a, i]);
            a = -1;
          }
        });
        if (a >= 0) list.push([a, samples.length - 1]);
        runs.push(list);
        const canvas = document.createElement("canvas");
        canvas.className = styles.tile;
        canvas.style.top = `${t * TILE}px`;
        canvas.style.height = `${TILE}px`;
        host.appendChild(canvas);
        tiles.push({ index: t, canvas, drawn: -1, live: false });
      }
      if (!motion) head = Infinity;
      update();
    };

    const draw = (tile: Tile) => {
      const { canvas } = tile;
      if (!tile.live) {
        canvas.width = Math.round(width * dpr);
        canvas.height = Math.round(TILE * dpr);
        canvas.style.width = `${width}px`;
        tile.live = true;
      }
      const ctx = canvas.getContext("2d");
      if (!ctx) return;
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.setTransform(dpr, 0, 0, dpr, 0, -tile.index * TILE * dpr);
      for (const [a, b] of runs[tile.index]) {
        paint(ctx, samples, a, b, head);
        paintInk(ctx, samples, a, b, head);
      }
      tile.drawn = head;
    };

    /** Arc length the brush has reached when the reader's eye is at page height y. */
    const reach = (y: number) => {
      for (const p of samples) if (p.y > y) return p.s;
      return samples.length ? samples[samples.length - 1].s + 1 : 0;
    };

    const update = () => {
      raf = 0;
      if (!samples.length) return;
      const view = window.innerHeight;
      const scrollTop = -root.getBoundingClientRect().top;
      if (motion && introDone) target = Math.max(target, reach(scrollTop + view * 0.78));
      // At the very bottom of the page the last stroke always finishes, however tall the window.
      const page = document.documentElement;
      if (motion && introDone && window.scrollY + view >= page.scrollHeight - 4) {
        target = samples[samples.length - 1].s + 1;
      }
      if (motion) {
        const gap = target - head;
        head = Math.abs(gap) < 0.6 ? target : head + gap * 0.085;
      }
      const near0 = Math.floor((scrollTop - view) / TILE);
      const near1 = Math.floor((scrollTop + 2 * view) / TILE);
      for (const tile of tiles) {
        const near = tile.index >= near0 && tile.index <= near1;
        if (!near) {
          if (tile.live) {
            tile.canvas.width = 0;
            tile.canvas.height = 0;
            tile.live = false;
            tile.drawn = -1;
          }
          continue;
        }
        const list = runs[tile.index];
        if (!list.length) continue;
        const first = samples[list[0][0]].s;
        const last = samples[list[list.length - 1][1]].s;
        const changed = tile.drawn < 0 || (head > tile.drawn && head > first && tile.drawn < last);
        if (changed) draw(tile);
      }
      for (const station of stations) {
        const reached = String(head >= station.s - 24);
        if (station.element.dataset.reached !== reached) station.element.dataset.reached = reached;
      }
      // How far the brush has come, for checks (0 to 1).
      const total = samples[samples.length - 1].s;
      host.dataset.progress = Math.min(1, head / Math.max(1, total)).toFixed(3);
      if (motion && head !== target) raf = requestAnimationFrame(update);
    };

    const schedule = () => {
      if (!raf) raf = requestAnimationFrame(update);
    };

    // The opening's stroke: leaving the crane and running to the bottom of the
    // first window, in one slow breath after the paintings settle.
    let intro = 0;
    if (motion) {
      const begin = performance.now() + 1100;
      const run = () => {
        const t = Math.min(1, Math.max(0, (performance.now() - begin) / 2600));
        const eased = 1 - Math.pow(1 - t, 3);
        const scrollTop = -root.getBoundingClientRect().top;
        const goal = reach(scrollTop + window.innerHeight * 1.02);
        target = Math.max(target, goal * eased);
        head = target;
        schedule();
        if (t < 1) intro = requestAnimationFrame(run);
        else introDone = true;
      };
      intro = requestAnimationFrame(run);
    }

    let timer = 0;
    const relayout = () => {
      window.clearTimeout(timer);
      timer = window.setTimeout(layout, 120);
    };
    const observer = new ResizeObserver(relayout);
    observer.observe(root);
    layout();
    window.addEventListener("scroll", schedule, { passive: true });
    document.fonts?.ready.then(relayout);
    return () => {
      observer.disconnect();
      window.clearTimeout(timer);
      cancelAnimationFrame(raf);
      cancelAnimationFrame(intro);
      window.removeEventListener("scroll", schedule);
      tiles.forEach((tile) => tile.canvas.remove());
      stations.forEach((station) => delete station.element.dataset.reached);
    };
  }, [motion, route]);

  return <div ref={layer} className={styles.layer} aria-hidden="true" data-brush-layer />;
}
