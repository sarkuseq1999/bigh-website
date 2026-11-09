"use client";

import Image from "next/image";
import {
  useEffect,
  useRef,
  useState,
  useSyncExternalStore,
  type CSSProperties,
  type ReactNode,
} from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { about, drafts } from "./about-content";
import page from "./about-page.module.css";
import mock from "./map-mockups.module.css";
import { plantsArt as art } from "./plants-art";
import { Dabs, layTrail } from "./plants-map";
import styles from "./plants-map.module.css";

// MOCKUPS for Mo (November 9, 2026): the plants map without named places. Mo is still finding out
// where the pine bark and grape seed come from, and asked that the map only give the feeling that
// each plant comes from the part of the world best for its natural growth. Shown with
// /about?map=a|b|c; plain /about keeps the built map (stand-in places). English only. Each plant
// gets the kind of place it thrives in, in a few words, never a country: true of the plant
// itself, whatever farm it comes from.

type Key = (typeof about.plants.items)[number]["key"];

const PLANTS: { key: Key; plant: string; grows: string }[] = [
  { key: "propolis", plant: "Green propolis", grows: "Warm, wild hillsides" },
  { key: "turmeric", plant: "Turmeric", grows: "Hot, rainy fields" },
  { key: "grape", plant: "Grape seed", grows: "Sunny slopes" },
  { key: "pine", plant: "Pine bark", grows: "Old pine forests" },
];

function useArrive<T extends HTMLElement>(share: number) {
  const ref = useRef<T>(null);
  const [state, setState] = useState<"waiting" | "on">("waiting");
  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        observer.disconnect();
        setState("on");
      },
      { threshold: share },
    );
    observer.observe(element);
    return () => observer.disconnect();
  }, [share]);
  return [ref, state] as const;
}

function Part({ idea, children }: { idea: string; children: ReactNode }) {
  const copy = useCopy();
  return (
    <section
      id="plants"
      className={`${page.part} ${styles.part}`}
      data-part="plants"
      data-map={idea}
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
        {children}
      </div>
    </section>
  );
}

function Home({ x, y }: { x: number; y: number }) {
  const copy = useCopy();
  const style = { left: `${x}%`, top: `${y}%` } as CSSProperties;
  return (
    <>
      <span className={styles.dot} data-home="" style={style} />
      <span className={styles.homeLabel} style={style}>
        <b>{copy(about.plants.home.name)}</b>
        <span>{copy(about.plants.home.note)}</span>
      </span>
    </>
  );
}

function Pin({ plant, x, y }: { plant: (typeof PLANTS)[number]; x: number; y: number }) {
  const pic = art[`plant-${plant.key}`];
  return (
    <span
      className={`${styles.pin} ${mock.pin}`}
      data-plant={plant.key}
      style={{ left: `${x}%`, top: `${y}%` } as CSSProperties}
    >
      <Image
        className={base.ink}
        src={pic.src}
        alt=""
        width={pic.width}
        height={pic.height}
        sizes="140px"
      />
      <span className={`${styles.pinWords} ${mock.words}`}>
        <b>{plant.plant}</b>
        <span>{plant.grows}</span>
      </span>
    </span>
  );
}

// Phones: the picture is too small for its plants, so they are listed under it.
function List() {
  return (
    <ul className={styles.list}>
      {PLANTS.map((plant) => {
        const pic = art[`plant-${plant.key}`];
        return (
          <li key={plant.key}>
            <Image
              className={base.ink}
              src={pic.src}
              alt=""
              width={pic.width}
              height={pic.height}
              sizes="72px"
            />
            <span>
              <b>{plant.plant}</b>
              <span>{plant.grows}</span>
            </span>
          </li>
        );
      })}
    </ul>
  );
}

// ---- A: the map, plants at sea ----------------------------------------------------------------

// Each plant afloat in a different sea round the world (frame pixels of the 1536 x 1024 land
// guide), never on a country: the Pacific, the North and South Atlantic, the Indian Ocean.
const SEA: Record<Key, [number, number]> = {
  pine: [300, 745],
  grape: [720, 350],
  propolis: [828, 770],
  turmeric: [1400, 725],
};
const SEA_LIFT: Record<Key, number> = { pine: 0.12, grape: 0.12, propolis: 0.22, turmeric: 0.26 };

function SeaIdea() {
  const copy = useCopy();
  const [map, draw] = useArrive<HTMLElement>(0.35);
  const W = art.map.width;
  const H = art.map.height;
  const [hx, hy] = art.map.places.california;
  const pin = (key: Key) => [SEA[key][0] - art.map.crop[0], SEA[key][1] - art.map.crop[1]];
  const trails = PLANTS.map((p, i) => {
    const [x, y] = pin(p.key);
    return { key: p.key, dabs: layTrail(x, y - 20, hx * W, hy * H, SEA_LIFT[p.key], 11 + i * 97) };
  });
  return (
    <Part idea="a">
      <figure ref={map} className={styles.map} data-picture="" data-draw={draw}>
        <span className={styles.body}>
          <Image
            className={base.ink}
            src={art.map.src}
            alt="A map of the world painted in ink and watercolour; each plant stands in a different sea, and a gold dotted line runs from each to California"
            width={W}
            height={H}
            sizes="(max-width: 1440px) 86vw, 1240px"
          />
          <svg className={styles.trails} viewBox={`0 0 ${W} ${H}`} aria-hidden="true">
            <Dabs trails={trails} />
          </svg>
          <Home x={hx * 100} y={hy * 100} />
          {PLANTS.map((p) => {
            const [x, y] = pin(p.key);
            return <Pin key={p.key} plant={p} x={(x / W) * 100} y={(y / H) * 100} />;
          })}
        </span>
        <figcaption className={base.caption}>{copy(drafts.illustration)}</figcaption>
      </figure>
      <List />
    </Part>
  );
}

// ---- B: the globe ------------------------------------------------------------------------------

// The globe (render_globe.py: centre 768, 512, radius 440 on 1536 x 1024; California at 636, 404)
// with the four plants standing just past its rim, all round it: from the far side of the world.
const GLOBE_HOME: [number, number] = [636, 404];
const RIM: Record<Key, [number, number]> = {
  pine: [215, 430],
  grape: [1190, 175],
  turmeric: [1305, 640],
  propolis: [380, 860],
};
const RIM_LIFT: Record<Key, number> = { pine: 0.15, grape: 0.18, turmeric: 0.2, propolis: 0.12 };

function GlobeIdea() {
  const copy = useCopy();
  const [globe, draw] = useArrive<HTMLElement>(0.35);
  const W = art.globe.width;
  const H = art.globe.height;
  const trails = PLANTS.map((p, i) => {
    const [x, y] = RIM[p.key];
    return {
      key: p.key,
      dabs: layTrail(x, y - 20, GLOBE_HOME[0], GLOBE_HOME[1], RIM_LIFT[p.key], 23 + i * 89),
    };
  });
  return (
    <Part idea="b">
      <figure
        ref={globe}
        className={`${styles.map} ${mock.globe}`}
        data-picture=""
        data-draw={draw}
      >
        <span className={styles.body}>
          <Image
            className={base.ink}
            src={art.globe.src}
            alt="A globe painted in ink and watercolour, the four plants standing round its rim, a gold dotted line from each over the globe to California"
            width={W}
            height={H}
            sizes="(max-width: 1440px) 86vw, 1240px"
          />
          <svg
            className={`${styles.trails} ${mock.clip}`}
            viewBox={`0 0 ${W} ${H}`}
            aria-hidden="true"
          >
            <Dabs trails={trails} />
          </svg>
          <Home x={(GLOBE_HOME[0] / W) * 100} y={(GLOBE_HOME[1] / H) * 100} />
          {PLANTS.map((p) => (
            <Pin
              key={p.key}
              plant={p}
              x={(RIM[p.key][0] / W) * 100}
              y={(RIM[p.key][1] / H) * 100}
            />
          ))}
        </span>
        <figcaption className={base.caption}>{copy(drafts.illustration)}</figcaption>
      </figure>
      <List />
    </Part>
  );
}

// ---- C: four kinds of place, one road home ------------------------------------------------------

// Each plant's kind of place painted small (the round-1 "four homes", which named countries; here
// only the kind of place), one gold trail running under all four to California.
const HOMES: Record<Key, { src: string; width: number; height: number }> = {
  propolis: { src: "/images/about-plants/home-minas-v1.webp", width: 1533, height: 999 },
  turmeric: { src: "/images/about-plants/home-turmeric-v1.webp", width: 1529, height: 1012 },
  grape: { src: "/images/about-plants/home-grape-v1.webp", width: 1501, height: 958 },
  pine: { src: "/images/about-plants/home-pine-v1.webp", width: 1526, height: 1019 },
};
const ROAD = layTrail(10, 30, 1390, 30, -0.02, 5);

function KindsIdea() {
  const copy = useCopy();
  const [row, draw] = useArrive<HTMLDivElement>(0.4);
  return (
    <Part idea="c">
      <div ref={row} className={`${styles.map} ${mock.kinds}`} data-draw={draw}>
        <ul className={mock.homes}>
          {PLANTS.map((p) => {
            const pic = HOMES[p.key];
            return (
              <li key={p.key}>
                <Image
                  className={base.ink}
                  src={pic.src}
                  alt=""
                  width={pic.width}
                  height={pic.height}
                  sizes="(max-width: 759px) 90vw, 300px"
                />
                <h3>{p.plant}</h3>
                <p>{p.grows}</p>
              </li>
            );
          })}
        </ul>
        <div className={mock.road}>
          <svg viewBox="0 0 1400 60" preserveAspectRatio="none" aria-hidden="true">
            <Dabs trails={[{ key: "road", dabs: ROAD }]} />
          </svg>
          <span className={mock.end}>
            <span className={styles.dot} data-home="" />
            <span>
              <b>{copy(about.plants.home.name)}</b> {copy(about.plants.home.note)}
            </span>
          </span>
        </div>
        <p className={`${base.caption} ${mock.caption}`}>Illustrations</p>
      </div>
    </Part>
  );
}

export function MapMockup({ fallback }: { fallback: ReactNode }) {
  const idea = useSyncExternalStore(
    () => () => {},
    () => new URLSearchParams(window.location.search).get("map"),
    () => null,
  );
  if (idea === "a") return <SeaIdea />;
  if (idea === "b") return <GlobeIdea />;
  if (idea === "c") return <KindsIdea />;
  return <>{fallback}</>;
}
