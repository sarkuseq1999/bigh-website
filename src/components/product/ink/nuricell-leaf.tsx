"use client";

import Image from "next/image";
import { useEffect, useRef, useState } from "react";
import { nuricellGold } from "./nuricell-gold";
import styles from "./nuricell-inside.module.css";

// NuriCell's What's inside painting, its gold leaf moving (Mo picked 1, "rise, then float", October
// 26, 2026; mockups reference/ink-pages/mockups/nuricell-inside/). The figure's picture is the
// painting without its leaf (capsule-ink); every flake is drawn on one canvas over it, from the
// leaf sheet (build_nuricell_gold.py). As the painting comes into view the flakes lift out of the
// powder, sway, and settle where they are painted; then each keeps turning slowly in the air,
// catching the light and showing its darker side, as real gold leaf does: no glow, no sparkle.
// Drawn only while in view. Reduced motion, and no script: the leaf as painted (capsule-gold, a
// see-through layer that blooms with the painting).

const { leaf, flakes, tips } = nuricellGold.capsule;
/** The biggest flakes turn and catch the light; the specks only drift. */
const BIG = 12;
/** The sheet's three bands: as painted, lit, turned away (build_nuricell_gold.py's LIGHT). */
const LIT = 1.42;
const DARK = 0.8;

/** A seeded random, so every visit moves the same way. */
function seeded(seed: number) {
  return () => {
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** CSS's cubic-bezier(x1, y1, x2, y2) as a function of time (0 to 1). */
function bezier(x1: number, y1: number, x2: number, y2: number) {
  const at = (a: number, b: number, t: number) =>
    3 * a * (1 - t) ** 2 * t + 3 * b * (1 - t) * t ** 2 + t ** 3;
  return (x: number) => {
    let lo = 0;
    let hi = 1;
    for (let i = 0; i < 24; i++) {
      const mid = (lo + hi) / 2;
      if (at(x1, x2, mid) < x) lo = mid;
      else hi = mid;
    }
    return at(y1, y2, (lo + hi) / 2);
  };
}
const riseEase = bezier(0.3, 0.6, 0.25, 1);
const floatEase = bezier(0.42, 0, 0.58, 1);

/** A value through keyframes (offsets 0 to 1, each [offset, value]), straight between them. */
function through(frames: readonly (readonly [number, number])[], p: number) {
  for (let i = 1; i < frames.length; i++) {
    const [o1, v1] = frames[i];
    if (p <= o1) {
      const [o0, v0] = frames[i - 1];
      return v0 + ((v1 - v0) * (p - o0)) / (o1 - o0 || 1);
    }
  }
  return frames[frames.length - 1][1];
}

type Flake = {
  sheet: readonly number[];
  /** Its centre in the painting (fractions). */
  cx: number;
  cy: number;
  w: number;
  h: number;
  big: boolean;
  // Rising: from (sx, sy) (fractions, from its place), swaying out by `sway`, turned r0 and ry0.
  sx: number;
  sy: number;
  sway: number;
  r0: number;
  ry0: number;
  rise: number;
  delay: number;
  // Floating, after it settles: x then y (fractions), turns (radians), its own slow period.
  fx1: number;
  fx2: number;
  amp: number;
  fr: number;
  fry: number;
  float: number;
  floatDelay: number;
};

/** Every flake's motion, from the painting's own size (the amplitudes are in pixels at 440px). */
function plan(): Flake[] {
  const r = seeded(7);
  const R = (a: number, b: number) => a + r() * (b - a);
  const deg = Math.PI / 180;
  return flakes.map((f, i) => {
    const [, , , , x, y, w, h] = f;
    const big = i < BIG;
    const cx = x + w / 2;
    const cy = y + h / 2;
    const tip = tips.reduce((a, b) => (Math.abs(b[0] - cx) < Math.abs(a[0] - cx) ? b : a));
    const px = 1 / 440;
    const amp = (big ? R(3, 6) : R(4, 9)) * px;
    return {
      sheet: f,
      cx,
      cy,
      w,
      h,
      big,
      sx: tip[0] + R(-0.03, 0.03) - cx,
      sy: tip[1] + R(0, 0.02) - cy,
      sway: R(-0.06, 0.06),
      r0: R(-70, 70) * deg,
      ry0: R(-160, 160) * deg,
      rise: big ? R(3000, 3800) : R(2200, 3400),
      delay: R(0, 1400) + (1 - y) * 400,
      fx1: R(-amp, amp),
      fx2: R(-amp, amp),
      amp,
      fr: R(3, 8) * (r() < 0.5 ? -1 : 1) * deg,
      fry: (big ? R(16, 28) : R(24, 44)) * deg,
      float: big ? R(7000, 11000) : R(5000, 9000),
      floatDelay: R(0, 600),
    };
  });
}

/** Where a flake is at `t` ms since the rise began: offset (fractions), scale, turns, light, opacity. */
function pose(f: Flake, t: number) {
  const local = (t - f.delay) / f.rise;
  if (local < 0) return null;
  if (local < 1) {
    const p = riseEase(local);
    return {
      x: through(
        [
          [0, f.sx],
          [0.58, f.sx * 0.35 + f.sway],
          [1, 0],
        ],
        p,
      ),
      y: through(
        [
          [0, f.sy],
          [0.58, f.sy * 0.42],
          [1, 0],
        ],
        p,
      ),
      scale: through(
        [
          [0, 0.25],
          [0.58, 0.85],
          [1, 1],
        ],
        p,
      ),
      r: through(
        [
          [0, f.r0],
          [0.58, f.r0 * 0.35],
          [1, 0],
        ],
        p,
      ),
      ry: through(
        [
          [0, f.ry0],
          [0.58, f.ry0 * 0.3],
          [1, 0],
        ],
        p,
      ),
      light: through(
        [
          [0, 1],
          [0.58, 1.35],
          [1, 1],
        ],
        p,
      ),
      opacity: Math.min(1, p / 0.14),
    };
  }
  const u = t - f.delay - f.rise - f.floatDelay;
  if (u < 0) return { x: 0, y: 0, scale: 1, r: 0, ry: 0, light: 1, opacity: 1 };
  const p = floatEase((u % f.float) / f.float);
  return {
    x: through(
      [
        [0, 0],
        [0.4, f.fx1],
        [0.78, f.fx2],
        [1, 0],
      ],
      p,
    ),
    y: through(
      [
        [0, 0],
        [0.4, -f.amp],
        [0.78, f.amp * 0.4],
        [1, 0],
      ],
      p,
    ),
    scale: 1,
    r: through(
      [
        [0, 0],
        [0.4, f.fr],
        [0.78, -f.fr * 0.6],
        [1, 0],
      ],
      p,
    ),
    ry: through(
      [
        [0, 0],
        [0.4, f.fry],
        [0.78, -f.fry * 0.7],
        [1, 0],
      ],
      p,
    ),
    light: through(
      [
        [0, 1],
        [0.4, 1.28],
        [0.78, 0.86],
        [1, 1],
      ],
      p,
    ),
    opacity: 1,
  };
}

/** The flakes over the painting: the still leaf, or the canvas that moves it. */
export function NuricellLeaf({ motion }: { motion: boolean }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  // The still leaf stays until the canvas has its sheet and draws (so the gold is never missing).
  const [drawing, setDrawing] = useState(false);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d");
    if (!canvas || !ctx || !motion) return;
    const all = plan();
    const sheet = new window.Image();
    let ready = false;
    let started = -1;
    // The rise's clock runs only while the painting is in view, so the leaf never jumps.
    let clock = 0;
    let last = 0;
    let frame = 0;
    let visible = false;

    const size = () => {
      const ratio = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(canvas.clientWidth * ratio);
      canvas.height = Math.round(canvas.clientHeight * ratio);
    };
    const draw = (now: number) => {
      frame = 0;
      if (!visible) return;
      if (last) clock += Math.min(now - last, 100);
      last = now;
      const W = canvas.width;
      const H = canvas.height;
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, W, H);
      const t = started < 0 ? -1 : clock - started;
      for (const f of all) {
        const at = t < 0 ? null : pose(f, t);
        if (!at || at.opacity <= 0) continue;
        const [sx, sy, sw, sh] = f.sheet;
        const dw = f.w * W;
        const dh = f.h * H;
        const turn = Math.cos(at.ry);
        ctx.setTransform(1, 0, 0, 1, (f.cx + at.x) * W, (f.cy + at.y) * H);
        ctx.rotate(at.r);
        ctx.scale(
          at.scale * (Math.abs(turn) < 0.04 ? 0.04 * Math.sign(turn || 1) : turn),
          at.scale,
        );
        ctx.globalAlpha = at.opacity;
        ctx.drawImage(sheet, sx, sy, sw, sh, -dw / 2, -dh / 2, dw, dh);
        // Light between the sheet's bands: lit above 1, turned away below it.
        const light = f.big ? at.light : 1;
        const blend = light > 1 ? (light - 1) / (LIT - 1) : (1 - light) / (1 - DARK);
        if (blend > 0.02) {
          ctx.globalAlpha = at.opacity * Math.min(1, blend);
          const band = light > 1 ? 1 : 2;
          ctx.drawImage(sheet, sx, sy + band * leaf.band, sw, sh, -dw / 2, -dh / 2, dw, dh);
        }
      }
      ctx.globalAlpha = 1;
      frame = requestAnimationFrame(draw);
    };
    const wake = () => {
      if (ready && visible && !frame) {
        last = 0;
        frame = requestAnimationFrame(draw);
      }
    };

    // In view: draw. Half in view (once): the rise begins, a moment into the painting's bloom.
    const seen = new IntersectionObserver(
      ([entry]) => {
        visible = entry.isIntersecting;
        if (entry.isIntersecting && started < 0 && entry.intersectionRatio >= 0.35)
          started = clock + 450;
        wake();
      },
      { threshold: [0, 0.35] },
    );
    const resize = new ResizeObserver(() => size());
    sheet.onload = () => {
      ready = true;
      size();
      setDrawing(true);
      wake();
    };
    sheet.src = leaf.src;
    seen.observe(canvas);
    resize.observe(canvas);
    return () => {
      seen.disconnect();
      resize.disconnect();
      cancelAnimationFrame(frame);
      sheet.onload = null;
      setDrawing(false);
    };
  }, [motion]);

  const { gold } = nuricellGold.capsule;
  return (
    <>
      <Image
        className={styles.goldStill}
        src={gold.src}
        alt=""
        width={gold.width}
        height={gold.height}
        sizes="(max-width: 959px) 88vw, 440px"
        data-bloom="waiting"
        data-gold-still={drawing ? "moving" : "still"}
      />
      {motion ? (
        <canvas ref={canvasRef} className={styles.leaf} aria-hidden="true" data-leaf="" />
      ) : null}
    </>
  );
}
