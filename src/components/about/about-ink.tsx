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
import { book, desk, lamp, seedling, sequoia, vignettes } from "./about-art";
import { CountUp } from "./count-up";
import { Greetings } from "./greetings";
import { Painting, Spread } from "./spread";
import page from "./about-page.module.css";
import styles from "./album.module.css";

// About B, "The album" (Mo, October 7, 2026; mockup reference/ink-pages/mockups/about-b.png; spec
// docs/superpowers/specs/2026-10-05-ink-pages-design.md, "About (stage 1), October 7"). An old
// painting album: every part a spread, one painting beside its words, the sides swapping. The name
// once (the logo, then the title). California, not zen. The words are the locked ones in
// about-content.ts.

export const ALT = {
  book: "An old open book, painted in ink, with a gold ribbon bookmark",
  seedling:
    "An oak seedling growing from an acorn, painted in ink; a gold acorn lies among its roots",
  desk: "A scientist's desk in ink: a brush on its rest, a microscope and a stack of books",
  sequoia: "An ancient giant sequoia rising from mist beside a young sequoia, painted in ink",
  lamp: "A desk lamp casting gold light onto an open journal, painted in ink",
} as const;

const PROMISE_ART = [vignettes.palms, vignettes.bee, vignettes.moon, vignettes.letter];
const HALF = "(max-width: 959px) 90vw, 46vw";

function sentences(text: string) {
  return text.match(/[^.!?。！？]+[.!?。！？]*\s*/gu)?.map((part) => part.trim()) ?? [text];
}

function Opening() {
  const copy = useCopy();
  return (
    <section className={page.opening} data-part="opening" aria-labelledby="about-title">
      <div className={`${base.wrap} ${page.spread}`} data-side="right">
        <Painting art={book} alt={ALT.book} sizes={HALF} gold={book.gold} caption preload waiting />
        <div className={page.words} data-words="">
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
      picture={<Painting art={desk} alt={ALT.desk} sizes={HALF} caption />}
    >
      <p className={`${base.label} ${page.label}`} data-label="">
        {copy(about.roots.label)}
      </p>
      <h2 id="roots-title" className={`${base.display} ${page.heading}`}>
        {copy(about.roots.title)}
      </h2>
      <div className={styles.rootsBody}>
        <span className={page.mount} data-mount="">
          <Image
            src={liu.src}
            alt={copy(about.roots.photo.alt)}
            width={liu.width}
            height={liu.height}
            sizes="168px"
          />
        </span>
        <div>
          <p className={page.body}>{copy(about.roots.text)}</p>
          <Link href={routes.scientists} className={`${base.pill} ${base.pillGhost} ${page.more}`}>
            {copy(about.roots.link)} <ArrowRight size={18} aria-hidden="true" />
          </Link>
        </div>
      </div>
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
                className={`${base.ink} ${styles.vignette}`}
                src={PROMISE_ART[i].src}
                alt=""
                width={PROMISE_ART[i].width}
                height={PROMISE_ART[i].height}
                sizes="208px"
                data-bloom="waiting"
                style={{ "--bloom-delay": i * 220 } as CSSProperties}
              />
              <h3>{copy(item.title)}</h3>
              <p>{copy(item.text)}</p>
              {i === 3 && <Greetings className={page.greetings} />}
            </li>
          ))}
        </ul>
        <p className={`${base.caption} ${styles.rowCaption}`} data-row-caption="">
          {copy("Illustrations")}
        </p>
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
      picture={<Painting art={lamp} alt={ALT.lamp} sizes={HALF} gold={lamp.gold} caption />}
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
    <InkPage current="about" className={`${page.aboutPage} ${styles.album}`}>
      {() => (
        <div data-about="album">
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
