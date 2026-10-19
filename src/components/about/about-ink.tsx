"use client";

import Image from "next/image";
import { useEffect, useRef, useState, type CSSProperties } from "react";
import { ArrowRight } from "lucide-react";
import { liu } from "@/components/home-v2/look-ink/assets";
import { useSiteDialogs } from "@/components/ink/dialogs";
import { InkPage } from "@/components/ink/ink-page";
import base from "@/components/ink/ink.module.css";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { about, routes } from "./about-content";
import { dots, enso, glasses, hills, oak, pool, sequoia } from "./about-art";
import { CountUp } from "./count-up";
import { Greetings } from "./greetings";
import { Painting, Spread } from "./spread";
import page from "./about-page.module.css";
import styles from "./circle.module.css";

// About C, "The circle" (Mo, October 7, 2026; mockup reference/ink-pages/mockups/about-c.png; spec
// docs/superpowers/specs/2026-10-05-ink-pages-design.md, "About (stage 1), October 7"). One circle
// brushed in a single stroke (a whole, complete life) opens the page, once only; then the same
// rhythm as the album: one picture beside its words, the sides swapping. California, not zen. The
// name once (the logo, then the title). The words are the locked ones in about-content.ts.

export const ALT = {
  oak: "A great valley oak with a rope swing, painted in ink; below the ground, a gold light glows among its roots",
  sequoia: "An ancient giant sequoia rising from mist beside a young sequoia, painted in ink",
  glasses: "Reading glasses resting on an open notebook, painted in ink",
} as const;

// What each painting asks the server for follows the width it is drawn at (circle.module.css: its
// height a multiple of one plain height, --h, and its width that height times its shape; --h is
// 330px or 0.6 of the column's width, whichever is less, 300px or 0.7 of it under 960px, and 300px
// for the sequoia and the glasses from 960 to 1279px; measured in css px at 360 to 2560px). Up to
// 505px the column is 0.846 of the window; from 506 to 959px --h caps at 300px; from 960px the
// column is 0.394 of the window up to 1395px, where --h caps at 330px (300px for the sequoia and
// the glasses from 960 to 1279px, so they fill the column up to 1025px and 1083px). A shared
// half-window figure asked for 1.5 to 2.3 times too many pixels at 1440px (662px for paintings
// drawn at 327 to 470px). The oak stands taller than the rest (a plain height of 1.72): it fills
// its column up to 559px, is 475px wide from there to 959px, 0.373 of the window from 960px and
// 521px from 1395px.
const OAK = "(max-width: 559px) 85vw, (max-width: 959px) 475px, (max-width: 1395px) 38vw, 521px";
const SEQUOIA =
  "(max-width: 505px) 80vw, (max-width: 959px) 405px, (max-width: 1025px) 40vw, (max-width: 1279px) 405px, (max-width: 1395px) 32vw, 445px";
const GLASSES =
  "(max-width: 505px) 85vw, (max-width: 959px) 427px, (max-width: 1083px) 40vw, (max-width: 1279px) 427px, (max-width: 1395px) 34vw, 470px";
// The brush's wet head lies about 26 degrees before its gold leaf (about-art.ts enso.startDeg), so
// the circle's sweep starts there and the blackest part of the stroke is drawn first.
const SWEEP_FROM = `${(enso.startDeg - 26).toFixed(1)}deg`;

// Where the light that runs the circle goes (circle.module.css), as shares of the stroke's box:
// the stroke's centre, its spark's start at 12 o'clock on the stroke's middle line (the radii's
// mean, as a share of the box's height), and the leaf's centre, where its glow, its stars and its
// band of light stand.
const pct = (share: number) => `${(share * 100).toFixed(2)}%`;
const [CX, CY] = enso.ink.centre;
const RADIUS = enso.ink.radii.slice(0, -1).reduce((a, b) => a + b, 0) / (enso.ink.radii.length - 1);
const SPARK_TOP = CY - (RADIUS * enso.width) / enso.height;
const LEAF_X = enso.dot.left + enso.dot.size / 2;
const LEAF_Y =
  enso.dot.top +
  (enso.dot.size * enso.dot.height * enso.width) / (enso.dot.width * enso.height) / 2;
const LEAF_BOX = {
  left: pct(enso.dot.left),
  top: pct(enso.dot.top),
  width: pct(enso.dot.size),
};

function sentences(text: string) {
  return text.match(/[^.!?。！？]+[.!?。！？]*\s*/gu)?.map((part) => part.trim()) ?? [text];
}

function Opening() {
  const copy = useCopy();
  // The circle waits for its picture (circle.module.css): its stroke and gold hold until the
  // stroke's picture is in. Before hydration the page's inline script lets them go (about/page.tsx);
  // this is the hydrated key: [data-stroke="ready"] once the picture is in (Next's onLoad, which
  // also reports a picture in before hydration, and a check on mount). No timer, and a failed
  // picture never lets them go: the gold must not rise alone on bare paper.
  const stroke = useRef<HTMLImageElement>(null);
  const [ready, setReady] = useState(false);
  useEffect(() => {
    const img = stroke.current;
    if (img?.complete && img.naturalWidth) setReady(true);
  }, []);
  return (
    <section
      className={`${page.opening} ${styles.opening}`}
      data-part="opening"
      aria-labelledby="about-title"
    >
      <div className={`${base.wrap} ${styles.openingWords}`}>
        <span
          className={styles.enso}
          data-enso=""
          data-stroke={ready ? "ready" : undefined}
          aria-hidden="true"
          style={
            {
              "--start": SWEEP_FROM,
              "--cx": pct(CX),
              "--cy": pct(CY),
              "--ink": `url(${enso.ink.src})`,
              "--leaf": `url(${enso.dot.src})`,
            } as CSSProperties
          }
        >
          <Image
            ref={stroke}
            // Next calls onLoad for any img already complete when it hydrates, a broken one too.
            onLoad={(event) => {
              if (event.currentTarget.naturalWidth) setReady(true);
            }}
            className={`${base.ink} ${styles.paint}`}
            src={enso.src}
            alt=""
            width={enso.width}
            height={enso.height}
            sizes="(max-width: 833px) 200px, (max-width: 1499px) 24vw, 360px"
            preload
            fetchPriority="high"
          />
          {/* The light that runs the circle once the brush closes (circle.module.css): the stroke's
              ink lit gold through a window that travels round it, the spark at the window's head,
              then the glow at the leaf as the light gathers into it. */}
          <span className={styles.run} data-run="" />
          <span className={styles.orbit} data-orbit="">
            <span className={styles.spark} data-spark="" style={{ top: pct(SPARK_TOP) }} />
          </span>
          <span
            className={styles.glow}
            data-glow=""
            style={{ left: pct(LEAF_X), top: pct(LEAF_Y) }}
          />
          {/* The gold start loads at once but is not preloaded, and asks for low priority (React's
              server render writes a preload link for every img that is not lazy unless its
              fetchPriority is low). Preloaded, the 2KB leaf won the race on a slow link and rose
              alone on bare paper at about 3s, then the circle snapped in. This orders the
              requests, the circle first; the hold above ties the two: the gold rises a breath
              after the stroke's picture is in, however late it comes. */}
          <Image
            className={styles.dot}
            src={enso.dot.src}
            alt=""
            width={enso.dot.width}
            height={enso.dot.height}
            sizes="56px"
            loading="eager"
            fetchPriority="low"
            data-dot=""
            style={LEAF_BOX}
          />
          {/* As the light lands, a band of light crosses the leaf (only the leaf: its own picture is
              the band's mask) and two small stars of light flash beside it; the band and the larger
              star come back now and then while the page is open. */}
          <span className={styles.sheen} data-sheen="" style={LEAF_BOX} />
          <span
            className={styles.star}
            data-star=""
            style={{ left: pct(LEAF_X + 0.033), top: pct(LEAF_Y - 0.045) }}
          />
          <span
            className={`${styles.star} ${styles.starSmall}`}
            data-star=""
            style={{ left: pct(LEAF_X - 0.112), top: pct(LEAF_Y + 0.03) }}
          />
        </span>
        <p className={page.kicker}>{copy(about.hero.label)}</p>
        <h1 id="about-title" lang="en" className={page.title}>
          {about.hero.title}
        </h1>
        <p className={page.lead}>
          {sentences(copy(about.hero.lead)).map((sentence) => (
            <span key={sentence}>{sentence}</span>
          ))}
        </p>
      </div>
      {/* Loaded at once (loading="eager"): the hills reach into the first screen, and lazy they
          were the window's largest painting with reduced motion (Next's LCP warning, 1440x900).
          Next adds no preload for them; React's server render writes one, as for every img that
          is not lazy, without the circle's high priority. On a phone they run 1.8 times the
          window's width (circle.module.css). */}
      <Image
        className={`${base.ink} ${styles.hills}`}
        src={hills.src}
        alt=""
        width={hills.width}
        height={hills.height}
        sizes="(max-width: 599px) 180vw, 100vw"
        loading="eager"
        data-bloom="waiting"
        data-picture-band=""
      />
    </section>
  );
}

function Purpose() {
  const copy = useCopy();
  return (
    <Spread
      id="purpose"
      part="purpose"
      side="left"
      labelledBy="purpose-title"
      picture={<Painting art={oak} alt={ALT.oak} sizes={OAK} gold={oak.gold} caption eager />}
    >
      <p className={`${base.label} ${page.label}`} data-label="">
        {copy(about.purpose.label)}
      </p>
      <h2 id="purpose-title" className={`${base.display} ${page.heading}`}>
        {about.purpose.lines.map((line) => (
          <span key={line}>{copy(line)}</span>
        ))}
      </h2>
      {/* The mission stands a step under the heading, in ink (circle.module.css). */}
      <p className={page.body} data-mission="">
        {copy(about.purpose.mission)}
      </p>
    </Spread>
  );
}

function Roots() {
  const copy = useCopy();
  return (
    <Spread
      id="roots"
      part="roots"
      side="right"
      labelledBy="roots-title"
      picture={
        <figure className={styles.print} data-picture="">
          <Image
            className={`${base.ink} ${styles.pool}`}
            src={pool.src}
            alt=""
            width={pool.width}
            height={pool.height}
            sizes="(max-width: 599px) 260px, 372px"
            data-pool=""
            data-bloom="waiting"
          />
          <span className={page.mount} data-mount="">
            <Image
              src={liu.src}
              alt={copy(about.roots.photo.alt)}
              width={liu.width}
              height={liu.height}
              sizes="240px"
            />
          </span>
        </figure>
      }
    >
      <p className={`${base.label} ${page.label}`} data-label="">
        {copy(about.roots.label)}
      </p>
      <h2 id="roots-title" className={`${base.display} ${page.heading}`}>
        {copy(about.roots.title)}
      </h2>
      <p className={page.body}>{copy(about.roots.text)}</p>
      <Link href={routes.scientists} className={`${base.pill} ${base.pillGhost} ${page.more}`}>
        {copy(about.roots.link)} <ArrowRight size={18} aria-hidden="true" />
      </Link>
    </Spread>
  );
}

function Experience() {
  const copy = useCopy();
  const years = copy(about.experience.stats[1].unit);
  return (
    <Spread
      id="experience"
      part="experience"
      side="left"
      labelledBy="experience-title"
      picture={
        <Painting art={sequoia} alt={ALT.sequoia} sizes={SEQUOIA} gold={sequoia.gold} caption />
      }
    >
      <p className={`${base.label} ${page.label}`} data-label="">
        {copy(about.experience.label)}
      </p>
      <h2 id="experience-title" className={`${base.display} ${page.heading}`}>
        {copy(about.experience.title)}
      </h2>
      <dl className={page.figures}>
        <div>
          <dt>{copy(about.roots.stat.label)}</dt>
          <dd>
            <CountUp to={280} suffix="+" className={page.figure} />
          </dd>
        </div>
        <div>
          <dt>{copy(about.experience.stats[0].label)}</dt>
          <dd>
            <span className={page.figure}>{about.experience.stats[0].value}</span>
          </dd>
        </div>
        <div>
          <dt>{copy(about.experience.stats[1].label)}</dt>
          <dd>
            <CountUp to={20} suffix="+" className={page.figure} />
            <span className={page.unit}> {years}</span>
          </dd>
        </div>
      </dl>
    </Spread>
  );
}

function Promises() {
  const copy = useCopy();
  return (
    <section
      id="promise"
      className={`${page.part} ${page.promise}`}
      data-part="promise"
      aria-labelledby="promise-title"
    >
      <div className={base.wrap}>
        <p className={`${base.label} ${page.label}`} data-label="">
          {copy(about.promise.label)}
        </p>
        <h2 id="promise-title" className={`${base.display} ${page.heading}`}>
          {copy(about.promise.title)}
        </h2>
        <ul className={page.promises}>
          {about.promise.items.map((item, i) => (
            <li key={item.title} data-promise="">
              <Image
                className={`${base.ink} ${page.promiseDot}`}
                src={dots[i].src}
                alt=""
                width={dots[i].width}
                height={dots[i].height}
                sizes="132px"
                data-bloom="waiting"
                style={{ "--bloom-delay": i * 260 } as CSSProperties}
              />
              <h3>{copy(item.title)}</h3>
              <p>{copy(item.text)}</p>
              {i === 3 && <Greetings className={page.greetings} />}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

function Closing() {
  const copy = useCopy();
  const dialogs = useSiteDialogs();
  return (
    <Spread
      id="closing"
      part="closing"
      side="right"
      labelledBy="closing-title"
      picture={<Painting art={glasses} alt={ALT.glasses} sizes={GLASSES} caption />}
    >
      <h2 id="closing-title" className={`${base.display} ${page.heading}`}>
        {copy(about.closing.title)}
      </h2>
      <p className={page.body}>{copy(about.closing.text)}</p>
      <div className={page.actions}>
        <button type="button" className={base.pill} onClick={dialogs.openAsk}>
          {copy(about.closing.primary)}
        </button>
        <Link href={routes.products} className={`${base.pill} ${base.pillGhost}`}>
          {copy(about.closing.secondary)}
        </Link>
      </div>
    </Spread>
  );
}

export function AboutInk() {
  return (
    <InkPage current="about" className={`${page.aboutPage} ${styles.circle}`}>
      {() => (
        <div data-about="circle">
          <Opening />
          <Purpose />
          <Roots />
          <Experience />
          <Promises />
          <Closing />
        </div>
      )}
    </InkPage>
  );
}
