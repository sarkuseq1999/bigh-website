"use client";

import Image from "next/image";
import { useSyncExternalStore, type CSSProperties } from "react";
import { ArrowRight } from "lucide-react";
import base from "@/components/ink/ink.module.css";
import { Link } from "@/i18n/navigation";
import page from "./about-page.module.css";
import { plantsArt as art } from "./plants-art";
import mock from "./plants-mockups.module.css";
import { Painting, Spread } from "./spread";

// MOCKUPS for Mo (November 6, 2026): three ideas for "Each plant, from where it grows best.",
// shown with /about?plants=a|b|c. English only; the places other than Minas Gerais are stand-ins
// until Mo confirms where BiGH's turmeric, grape seed and pine bark come from. The page's blooms
// are found once, on mount, so the paintings of an idea picked after it show whole, unbloomed.

type Key = "propolis" | "turmeric" | "grape" | "pine";

const PLANTS: {
  key: Key;
  plant: string;
  place: string;
  product: string;
  home: "minas" | "turmeric" | "grape" | "pine";
}[] = [
  {
    key: "propolis",
    plant: "Green propolis",
    place: "Minas Gerais, Brazil",
    product: "Green Bee Propolis",
    home: "minas",
  },
  { key: "turmeric", plant: "Turmeric", place: "India", product: "Turmerific", home: "turmeric" },
  {
    key: "grape",
    plant: "Grape seed",
    place: "Italy",
    product: "Advanced OPC Formula",
    home: "grape",
  },
  {
    key: "pine",
    plant: "Pine bark",
    place: "France",
    product: "Advanced OPC Formula",
    home: "pine",
  },
];

// Where each plant's painting and words stand on the map (its centre, in the 1536 x 1024 frame
// render_land.py drew the land in), clear of the other plants and of the route lines.
const PIN: Record<Key, [number, number]> = {
  propolis: [820, 770],
  turmeric: [1400, 745],
  grape: [1185, 170],
  pine: [770, 430],
};

function Words({ title }: { title: string }) {
  return (
    <>
      <p className={`${base.label} ${page.label}`} data-label="">
        Our ingredients
      </p>
      <h2 id="plants-title" className={`${base.display} ${page.heading}`}>
        {title}
      </h2>
    </>
  );
}

// A: the map. The world painted in ink, each plant at its place, a gold route home to California.
function MapIdea() {
  const places = art.map.places;
  const [hx, hy] = places.california;
  const route = (key: Key) => {
    const [x, y] = places[key];
    const x0 = hx * 1536;
    const y0 = hy * 1024;
    const x1 = x * 1536;
    const y1 = y * 1024;
    const lift = Math.hypot(x1 - x0, y1 - y0) * 0.28;
    return `M${x1} ${y1} Q${(x0 + x1) / 2} ${Math.min(y0, y1) - lift} ${x0} ${y0}`;
  };
  return (
    <section
      id="plants"
      className={`${page.part} ${mock.mapPart}`}
      data-part="plants"
      data-idea="a"
      aria-labelledby="plants-title"
    >
      <div className={base.wrap}>
        <div className={mock.mapWords}>
          <Words title="Each plant, from where it grows best." />
          <p className={page.body}>
            We look around the world for our plants, and bring each one home from the place it grows
            best.
          </p>
        </div>
        <figure className={mock.map} data-picture="">
          <span className={mock.mapBody}>
            <Image
              className={base.ink}
              src={art.map.src}
              alt="A map of the world painted in ink, from California to India"
              width={art.map.width}
              height={art.map.height}
              sizes="(max-width: 1440px) 86vw, 1300px"
            />
            <svg className={mock.routes} viewBox="0 0 1536 1024" aria-hidden="true">
              {PLANTS.map((p) => (
                <path key={p.key} d={route(p.key)} />
              ))}
            </svg>
            <span
              className={mock.dot}
              data-home=""
              style={{ left: `${hx * 100}%`, top: `${hy * 100}%` } as CSSProperties}
            />
            <span
              className={mock.homeLabel}
              style={{ left: `${hx * 100}%`, top: `${hy * 100}%` } as CSSProperties}
            >
              <b>California</b>
              <span>where we make them</span>
            </span>
            {PLANTS.map((p) => {
              const [x, y] = places[p.key];
              const [px, py] = PIN[p.key];
              const pic = art[`plant-${p.key}`];
              return (
                <span key={p.key}>
                  <span
                    className={mock.dot}
                    style={{ left: `${x * 100}%`, top: `${y * 100}%` } as CSSProperties}
                  />
                  <span
                    className={mock.pin}
                    data-plant={p.key}
                    style={{
                      left: `${((px - art.map.crop[0]) / art.map.width) * 100}%`,
                      top: `${((py - art.map.crop[1]) / art.map.height) * 100}%`,
                    }}
                  >
                    <Image
                      className={base.ink}
                      src={pic.src}
                      alt=""
                      width={pic.width}
                      height={pic.height}
                      sizes="140px"
                    />
                    <span className={mock.pinWords}>
                      <b>{p.plant}</b>
                      <span>{p.place}</span>
                    </span>
                  </span>
                </span>
              );
            })}
          </span>
          <figcaption className={base.caption}>Illustration</figcaption>
        </figure>
        {/* Phones: the map is too small for its plants, so they are listed under it. */}
        <ul className={mock.mapList}>
          {PLANTS.map((p) => {
            const pic = art[`plant-${p.key}`];
            return (
              <li key={p.key}>
                <Image
                  className={base.ink}
                  src={pic.src}
                  alt=""
                  width={pic.width}
                  height={pic.height}
                  sizes="72px"
                />
                <span>
                  <b>{p.plant}</b>
                  <span>{p.place}</span>
                </span>
              </li>
            );
          })}
        </ul>
      </div>
    </section>
  );
}

// B: four homes. One small landscape for each plant, in a row.
function HomesIdea() {
  return (
    <section
      id="plants"
      className={`${page.part} ${mock.homesPart}`}
      data-part="plants"
      data-idea="b"
      aria-labelledby="plants-title"
    >
      <div className={base.wrap}>
        <div className={mock.homesWords}>
          <Words title="Each plant, from where it grows best." />
          <p className={page.body}>
            We look around the world for our plants, and choose each one from the place it grows
            best.
          </p>
        </div>
        <ul className={mock.homes}>
          {PLANTS.map((p) => {
            const pic = art[`home-${p.home}`];
            return (
              <li key={p.key}>
                <span className={mock.homePic}>
                  <Image
                    className={base.ink}
                    src={pic.src}
                    alt=""
                    width={pic.width}
                    height={pic.height}
                    sizes="(max-width: 759px) 78vw, 300px"
                  />
                </span>
                <h3>{p.plant}</h3>
                <p className={mock.place}>{p.place}</p>
                <p className={mock.product}>In {p.product}</p>
              </li>
            );
          })}
        </ul>
        <p className={`${base.caption} ${mock.homesCaption}`}>Illustrations</p>
      </div>
    </section>
  );
}

// C: one plant, all the way. The one place on file, told whole; the others in a line.
function OneIdea() {
  return (
    <Spread
      id="plants"
      part="plants"
      side="left"
      labelledBy="plants-title"
      picture={
        <Painting
          className={mock.one}
          art={art["home-minas"]}
          alt="Honeybees at a wild alecrim shrub on the hills of Minas Gerais, Brazil, painted in ink"
          sizes="(max-width: 959px) 90vw, 640px"
          waiting={false}
          caption
        />
      }
    >
      <Words title="Each plant, from where it grows best." />
      <p className={`${page.body} ${mock.oneLead}`}>
        Our green propolis comes only from Minas Gerais, Brazil.
      </p>
      <p className={page.body}>
        Bees there gather it from one wild shrub, alecrim. We choose our turmeric, grape seed and
        pine bark the same way.
      </p>
      <Link
        href="/products/green-bee-propolis"
        className={`${base.pill} ${base.pillGhost} ${page.more}`}
      >
        See Green Bee Propolis <ArrowRight size={18} aria-hidden="true" />
      </Link>
    </Spread>
  );
}

export function PlantsMockup({ fallback }: { fallback: React.ReactNode }) {
  const idea = useSyncExternalStore(
    () => () => {},
    () => new URLSearchParams(window.location.search).get("plants"),
    () => null,
  );
  if (idea === "a") return <MapIdea />;
  if (idea === "b") return <HomesIdea />;
  if (idea === "c") return <OneIdea />;
  return <>{fallback}</>;
}
