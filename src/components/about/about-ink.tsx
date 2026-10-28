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
import { dots, glasses, oak, pool, sequoia } from "./about-art";
import { CountUp } from "./count-up";
import { Greetings } from "./greetings";
import { meadow } from "./meadow-art";
import { Painting, Spread } from "./spread";
import page from "./about-page.module.css";
import styles from "./circle.module.css";
import field from "./meadow.module.css";

// About C (Mo, October 7, 2026; mockup reference/ink-pages/mockups/about-c.png; spec
// docs/superpowers/specs/2026-10-05-ink-pages-design.md, "About (stage 1), October 7"). The poppy
// meadow opens the page (October 28, 2026: it replaced the ink circle, which reminded Mo of the
// film The Ring); then the same rhythm as the album: one picture beside its words, the sides
// swapping. California, not zen. The name once (the logo, then the title). The words are the
// locked ones in about-content.ts.

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
// The meadow is drawn as wide as the window, or 1.5 times its height on a tall window
// (meadow.module.css).
const MEADOW = "(max-aspect-ratio: 3/2) 150vh, 100vw";

function sentences(text: string) {
  return text.match(/[^.!?。！？]+[.!?。！？]*\s*/gu)?.map((part) => part.trim()) ?? [text];
}

// The poppy meadow fills the first screen, the words in its sky, and thins out into the paper
// before Our purpose (meadow.module.css). Its gold waits for the gold's picture, then arrives:
// [data-light="ready"] once the picture is in (Next's onLoad, which also reports a picture in
// before hydration, and a check on mount). No timer. Both pictures are the backdrop of the title
// (alt=""), loaded at once: the painting is the first screen's largest.
function Opening() {
  const copy = useCopy();
  const gold = useRef<HTMLImageElement>(null);
  const [ready, setReady] = useState(false);
  useEffect(() => {
    const img = gold.current;
    if (img?.complete && img.naturalWidth) setReady(true);
  }, []);
  return (
    <section
      data-part="opening"
      data-meadow=""
      data-light={ready ? "ready" : undefined}
      aria-labelledby="about-title"
      style={{ "--foot": meadow.foot / meadow.height } as CSSProperties}
    >
      <div className={field.picture}>
        <Image
          src={meadow.src}
          alt=""
          width={meadow.width}
          height={meadow.height}
          sizes={MEADOW}
          preload
          fetchPriority="high"
        />
        <Image
          ref={gold}
          onLoad={(event) => {
            if (event.currentTarget.naturalWidth) setReady(true);
          }}
          className={field.gold}
          src={meadow.gold}
          alt=""
          width={meadow.width}
          height={meadow.height}
          sizes={MEADOW}
          loading="eager"
        />
      </div>
      <div className={`${base.wrap} ${field.words}`}>
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
      picture={<Painting art={oak} alt={ALT.oak} sizes={OAK} gold={oak.gold} caption />}
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
    <InkPage current="about" className={`${page.aboutPage} ${styles.circle} ${field.root}`}>
      {() => (
        <div data-about="meadow">
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
