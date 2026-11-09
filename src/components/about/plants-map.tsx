"use client";

import Image from "next/image";
import { useEffect, useRef, useState, type CSSProperties } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { about, drafts } from "./about-content";
import page from "./about-page.module.css";
import { plantsArt as art } from "./plants-art";
import styles from "./plants-map.module.css";

// Our ingredients, "Each plant, from where it grows best." (Mo picked the map on November 6,
// 2026, then, with no place named, B, the globe, on November 9; mockups
// reference/ink-pages/mockups/about-plants/). A globe painted in ink over the real land
// (reference/ink-pages/about-plants/render_globe.py), California facing you; the four plants stand
// just past its rim, all round it, each with the kind of place it thrives in, never a country.
// A trail of gold-leaf dabs runs from each plant over the globe home to California, where we make
// them: laid dab by dab, one plant after another, once, as the globe comes into view; reduced
// motion and no script show them laid. Phones list the plants under the globe, and the trails
// start at its rim, as if from its far side.

type Key = (typeof about.plants.items)[number]["key"];

const W = art.globe.width;
const H = art.globe.height;

// California on the globe (render_globe.py: centre 768, 512, radius 440 on 1536 x 1024).
const HOME: [number, number] = [636, 404];

// Where each plant stands (its centre, in the globe's pixels): just past the rim, spread round it.
const RIM: Record<Key, [number, number]> = {
  pine: [215, 430],
  grape: [1190, 175],
  turmeric: [1305, 640],
  propolis: [370, 830],
};

// How high each trail arcs, as a share of its length: different, so they fan out.
const LIFT: Record<Key, number> = { pine: 0.15, grape: 0.18, turmeric: 0.2, propolis: 0.12 };

// The trail's dabs: one every STEP pixels of the picture, a little irregular, as a brush lays them.
const STEP = 13;

function random(seed: number) {
  let s = seed;
  return () => {
    s = (s * 16807) % 2147483647;
    return s / 2147483647;
  };
}

type Dab = { x: number; y: number; a: number; r: number; tone: number };

// A trail of dabs from (x1, y1) to (x0, y0): a low arc (lifted `lift` of its length), sampled
// finely and walked at an even step. It stops a dab short of its end (the home mark).
function layTrail(x1: number, y1: number, x0: number, y0: number, lift: number, seed: number) {
  const cx = (x0 + x1) / 2;
  const cy = Math.min(y0, y1) - Math.hypot(x1 - x0, y1 - y0) * lift;
  const at = (t: number) => {
    const u = 1 - t;
    return [u * u * x1 + 2 * u * t * cx + t * t * x0, u * u * y1 + 2 * u * t * cy + t * t * y0];
  };
  const rand = random(seed);
  const dabs: Dab[] = [];
  let [px, py] = at(0);
  let next = STEP * 0.6;
  let walked = 0;
  for (let i = 1; i <= 2000; i += 1) {
    const [x, y] = at(i / 2000);
    walked += Math.hypot(x - px, y - py);
    if (walked >= next) {
      dabs.push({
        x: Math.round(x * 10) / 10,
        y: Math.round(y * 10) / 10,
        a: Math.round((Math.atan2(y - py, x - px) * 180) / Math.PI),
        r: Math.round((2.6 + rand() * 1.2) * 10) / 10,
        tone: Math.floor(rand() * 3),
      });
      next += STEP + (rand() - 0.5) * 4;
    }
    [px, py] = [x, y];
  }
  return dabs.slice(0, -1);
}

// Each trail leaves from a little above its plant's centre (under the painting, so it seems to
// come out of the plant).
const TRAILS = about.plants.items.map((item, i) => {
  const [x, y] = RIM[item.key];
  return {
    key: item.key,
    dabs: layTrail(x, y - 20, HOME[0], HOME[1], LIFT[item.key], 23 + i * 89),
  };
});

const at = ([x, y]: readonly number[]) =>
  ({ left: `${(x / W) * 100}%`, top: `${(y / H) * 100}%` }) as CSSProperties;

export function PlantsMap() {
  const copy = useCopy();
  const globe = useRef<HTMLElement>(null);
  const [draw, setDraw] = useState<"waiting" | "on">("waiting");
  useEffect(() => {
    const figure = globe.current;
    if (!figure) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        observer.disconnect();
        setDraw("on");
      },
      { threshold: 0.35 },
    );
    observer.observe(figure);
    return () => observer.disconnect();
  }, []);
  return (
    <section
      id="plants"
      className={`${page.part} ${styles.part}`}
      data-part="plants"
      aria-labelledby="plants-title"
    >
      <div className={base.wrap}>
        <div className={styles.words} data-words="">
          <p className={`${base.label} ${page.label}`} data-label="">
            {copy(about.plants.label)}
          </p>
          <h2 id="plants-title" className={`${base.display} ${page.heading}`}>
            {copy(about.plants.title)}
          </h2>
          <p className={page.body}>{copy(about.plants.text)}</p>
        </div>
        <figure ref={globe} className={styles.globe} data-picture="" data-draw={draw}>
          <span className={styles.body}>
            <Image
              className={base.ink}
              src={art.globe.src}
              alt={copy(about.plants.alt)}
              width={W}
              height={H}
              sizes="(max-width: 1440px) 86vw, 1180px"
              data-bloom="waiting"
            />
            <svg className={styles.trails} viewBox={`0 0 ${W} ${H}`} aria-hidden="true">
              {TRAILS.map((t, r) => (
                <g key={t.key} data-trail={t.key} style={{ "--r": r } as CSSProperties}>
                  {t.dabs.map((d, i) => (
                    <g key={i} transform={`translate(${d.x} ${d.y}) rotate(${d.a})`}>
                      <ellipse
                        className={styles.dab}
                        data-tone={d.tone}
                        rx={d.r * 1.3}
                        ry={d.r * 0.85}
                        style={{ "--i": i } as CSSProperties}
                      />
                    </g>
                  ))}
                </g>
              ))}
            </svg>
            <span className={styles.dot} data-home="" style={at(HOME)} />
            <span className={styles.homeLabel} style={at(HOME)}>
              <b>{copy(about.plants.home.name)}</b>
              <span>{copy(about.plants.home.note)}</span>
            </span>
            {about.plants.items.map((item, r) => {
              const pic = art[`plant-${item.key}`];
              return (
                <span
                  key={item.key}
                  className={styles.pin}
                  data-plant={item.key}
                  style={at(RIM[item.key])}
                >
                  <Image
                    className={base.ink}
                    src={pic.src}
                    alt=""
                    width={pic.width}
                    height={pic.height}
                    sizes="140px"
                    data-bloom="waiting"
                    style={{ "--bloom-delay": 300 + r * 250 } as CSSProperties}
                  />
                  <span className={styles.pinWords}>
                    <b>{copy(item.plant)}</b>
                    <span>{copy(item.grows)}</span>
                  </span>
                </span>
              );
            })}
          </span>
          <figcaption className={base.caption}>{copy(drafts.illustration)}</figcaption>
        </figure>
        {/* Phones: the plants are too small beside the globe, so they are listed under it. */}
        <ul className={styles.list}>
          {about.plants.items.map((item, r) => {
            const pic = art[`plant-${item.key}`];
            return (
              <li key={item.key}>
                <Image
                  className={base.ink}
                  src={pic.src}
                  alt=""
                  width={pic.width}
                  height={pic.height}
                  sizes="72px"
                  data-bloom="waiting"
                  style={{ "--bloom-delay": r * 200 } as CSSProperties}
                />
                <span>
                  <b>{copy(item.plant)}</b>
                  <span>{copy(item.grows)}</span>
                </span>
              </li>
            );
          })}
        </ul>
      </div>
    </section>
  );
}
