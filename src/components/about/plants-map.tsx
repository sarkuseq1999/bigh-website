"use client";

import Image from "next/image";
import { useEffect, useRef, useState, type CSSProperties } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { about, drafts } from "./about-content";
import page from "./about-page.module.css";
import { plantsArt as art } from "./plants-art";
import styles from "./plants-map.module.css";

// Our ingredients, "Each plant, from where it grows best." (Mo picked A, the map, November 6,
// 2026; mockups reference/ink-pages/mockups/about-plants/). The world painted in ink over the
// real land (reference/ink-pages/about-plants/), each plant standing where it grows, and a trail
// of gold-leaf dabs that carries each one home to California, where we make them. The trails are
// laid dab by dab, one after another, once, as the map comes into view; reduced motion and no
// script show them laid. Phones list the plants under the map. Every place but Minas Gerais is
// a STAND-IN until Mo gives the real one (about-content.ts).

type Key = (typeof about.plants.items)[number]["key"];

const W = art.map.width;
const H = art.map.height;

// Where each plant's painting stands (its centre, in the 1536 x 1024 frame render_land.py drew
// the land in): in open sea beside its place, clear of the coasts and of the trails. The two
// European plants stand one over the other in the North Atlantic, west of their places (side by
// side, the grapes stood on Morocco).
const PIN: Record<Key, [number, number]> = {
  propolis: [828, 760],
  turmeric: [1400, 725],
  grape: [742, 528],
  pine: [720, 348],
};

// How high each trail arcs, as a share of its length: different, so the three from Europe and
// India fan out instead of running home as one rope.
const LIFT: Record<Key, number> = { propolis: 0.22, turmeric: 0.25, grape: 0.17, pine: 0.1 };

// The trail's dabs: one every STEP units of the map, a little irregular, as a brush lays them.
const STEP = 13;

function random(seed: number) {
  let s = seed;
  return () => {
    s = (s * 16807) % 2147483647;
    return s / 2147483647;
  };
}

type Dab = { x: number; y: number; a: number; r: number; tone: number };

// A trail from the plant's place home to California: a low arc (lifted `lift` of its length),
// sampled finely and walked at an even step.
function trail(from: readonly number[], to: readonly number[], lift: number, seed: number): Dab[] {
  const [x1, y1] = [from[0] * W, from[1] * H];
  const [x0, y0] = [to[0] * W, to[1] * H];
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
  // The last dabs run into California's own mark: stop short of it.
  return dabs.slice(0, -1);
}

const TRAILS = about.plants.items.map((item, i) => ({
  key: item.key,
  dabs: trail(art.map.places[item.key], art.map.places.california, LIFT[item.key], 7 + i * 131),
}));

const at = (point: readonly number[]) =>
  ({ left: `${point[0] * 100}%`, top: `${point[1] * 100}%` }) as CSSProperties;

export function PlantsMap() {
  const copy = useCopy();
  const map = useRef<HTMLElement>(null);
  const [draw, setDraw] = useState<"waiting" | "on">("waiting");
  useEffect(() => {
    const figure = map.current;
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
  const home = art.map.places.california;
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
        <figure ref={map} className={styles.map} data-picture="" data-draw={draw}>
          <span className={styles.body}>
            <Image
              className={base.ink}
              src={art.map.src}
              alt={copy(about.plants.alt)}
              width={W}
              height={H}
              sizes="(max-width: 1440px) 86vw, 1240px"
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
            {about.plants.items.map((item, r) => (
              <span
                key={item.key}
                className={styles.dot}
                data-place={item.key}
                style={{ ...at(art.map.places[item.key]), "--r": r } as CSSProperties}
              />
            ))}
            <span className={styles.dot} data-home="" style={at(home)} />
            <span className={styles.homeLabel} style={at(home)}>
              <b>{copy(about.plants.home.name)}</b>
              <span>{copy(about.plants.home.note)}</span>
            </span>
            {about.plants.items.map((item, r) => {
              const [px, py] = PIN[item.key];
              const pic = art[`plant-${item.key}`];
              return (
                <span
                  key={item.key}
                  className={styles.pin}
                  data-plant={item.key}
                  style={{
                    left: `${((px - art.map.crop[0]) / W) * 100}%`,
                    top: `${((py - art.map.crop[1]) / H) * 100}%`,
                  }}
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
                    <span>{copy(item.place)}</span>
                  </span>
                </span>
              );
            })}
          </span>
          <figcaption className={base.caption}>{copy(drafts.illustration)}</figcaption>
        </figure>
        {/* Phones: the map is too small for its plants, so they are listed under it. */}
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
                  <span>{copy(item.place)}</span>
                </span>
              </li>
            );
          })}
        </ul>
      </div>
    </section>
  );
}
