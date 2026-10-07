"use client";

import Image from "next/image";
import type { CSSProperties } from "react";
import { ArrowRight } from "lucide-react";
import { liu } from "@/components/home-v2/look-ink/assets";
import { useSiteDialogs } from "@/components/ink/dialogs";
import { InkPage } from "@/components/ink/ink-page";
import base from "@/components/ink/ink.module.css";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { about, routes } from "./about-content";
import { dots, enso, glasses, hills, pool, seedling, sequoia } from "./about-art";
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
  seedling:
    "An oak seedling growing from an acorn, painted in ink; a gold acorn lies among its roots",
  sequoia: "An ancient giant sequoia rising from mist beside a young sequoia, painted in ink",
  glasses: "Reading glasses resting on an open notebook, painted in ink",
} as const;

const HALF = "(max-width: 959px) 90vw, 46vw";
// The brush's wet head lies about 26 degrees before its gold leaf (about-art.ts enso.startDeg), so
// the circle's sweep starts there and the blackest part of the stroke is drawn first.
const SWEEP_FROM = `${(enso.startDeg - 26).toFixed(1)}deg`;

function sentences(text: string) {
  return text.match(/[^.!?。！？]+[.!?。！？]*\s*/gu)?.map((part) => part.trim()) ?? [text];
}

function Opening() {
  const copy = useCopy();
  return (
    <section
      className={`${page.opening} ${styles.opening}`}
      data-part="opening"
      aria-labelledby="about-title"
    >
      <div className={`${base.wrap} ${styles.openingWords}`}>
        <span className={styles.enso} data-enso="" aria-hidden="true">
          <Image
            className={`${base.ink} ${styles.paint}`}
            src={enso.src}
            alt=""
            width={enso.width}
            height={enso.height}
            sizes="(max-width: 833px) 200px, (max-width: 1499px) 24vw, 360px"
            priority
            style={{ "--start": SWEEP_FROM } as CSSProperties}
          />
          <Image
            className={styles.dot}
            src={enso.dot.src}
            alt=""
            width={enso.dot.width}
            height={enso.dot.height}
            sizes="56px"
            priority
            data-dot=""
            style={{
              left: `${enso.dot.left * 100}%`,
              top: `${enso.dot.top * 100}%`,
              width: `${enso.dot.size * 100}%`,
            }}
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
      {/* Loaded at once, not preloaded: the hills reach into the first screen, and lazy they were
          the window's largest painting with reduced motion (Next's LCP warning, 1440x900). */}
      <Image
        className={`${base.ink} ${styles.hills}`}
        src={hills.src}
        alt=""
        width={hills.width}
        height={hills.height}
        sizes="100vw"
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
      picture={
        <Painting
          art={seedling}
          alt={ALT.seedling}
          sizes={HALF}
          gold={seedling.gold}
          caption
          eager
        />
      }
    >
      <p className={`${base.label} ${page.label}`} data-label="">
        {copy(about.purpose.label)}
      </p>
      <h2 id="purpose-title" className={`${base.display} ${page.heading}`}>
        {about.purpose.lines.map((line) => (
          <span key={line}>{copy(line)}</span>
        ))}
      </h2>
      <p className={page.body}>{copy(about.purpose.mission)}</p>
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
        <Painting art={sequoia} alt={ALT.sequoia} sizes={HALF} gold={sequoia.gold} caption />
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
      picture={<Painting art={glasses} alt={ALT.glasses} sizes={HALF} caption />}
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
