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
import { about, drafts, routes } from "./about-content";
import { Acronym } from "./acronym";
import { ChapterWord } from "./chapter-word";
import { CountUp } from "./count-up";
import { Greetings } from "./greetings";
import { band, dots, pool, rings, word } from "./letter-art";
import styles from "./about-letter.module.css";

// The About page, "The name, on a folded letter" (Mo approved design D on October 6, 2026; mockup
// reference/ink-pages/mockups/about-d.png; spec docs/superpowers/specs/2026-10-05-ink-pages-design.md).
// One sheet of slightly aged paper, folded like a letter and opened again: BiGH written by hand at
// the top, then one brushed letter opening each part (Be, in, Good, Health), the parts alternating
// sides of the middle fold. The words are the locked ones in about-content.ts. No brush line here:
// the folds divide the page (the brush line is the homepage's signature).

export const RINGS_ALT =
  "Tree rings in ink. A gold ring marks 2016, when BiGH began; the rings inside it are the years the formula is older.";

function sentences(text: string) {
  return text.match(/[^.!?。！？]+[.!?。！？]*\s*/gu)?.map((part) => part.trim()) ?? [text];
}

function Opening() {
  const copy = useCopy();
  return (
    <section className={styles.opening} aria-labelledby="about-title">
      <div className={`${base.wrap} ${styles.openingWords}`}>
        <span className={styles.word} data-word="" aria-hidden="true">
          <Image
            className={`${base.ink} ${styles.paint}`}
            src={word.src}
            alt=""
            width={word.width}
            height={word.height}
            sizes="(max-width: 899px) 86vw, min(50vw, 780px)"
            priority
          />
          <Image
            className={styles.dot}
            src={word.dot.src}
            alt=""
            width={word.dot.width}
            height={word.dot.height}
            sizes="64px"
            priority
            data-dot=""
            style={{
              left: `${word.dot.left * 100}%`,
              top: `${word.dot.top * 100}%`,
              width: `${word.dot.size * 100}%`,
            }}
          />
        </span>
        <p className={styles.kicker}>{copy(about.hero.label)}</p>
        <Acronym className={styles.title} delay={2700} />
        <p className={styles.lead}>
          {sentences(copy(about.hero.lead)).map((sentence) => (
            <span key={sentence}>{sentence}</span>
          ))}
        </p>
      </div>
      {/* From 900px the band starts in the first screen and is its largest painting (LCP). */}
      <Image
        className={`${base.ink} ${styles.band}`}
        src={band.src}
        alt=""
        width={band.width}
        height={band.height}
        sizes="100vw"
        loading="eager"
        data-band=""
        data-bloom="waiting"
      />
    </section>
  );
}

function Purpose() {
  const copy = useCopy();
  return (
    <section
      id="purpose"
      className={styles.part}
      data-part="purpose"
      aria-labelledby="purpose-title"
    >
      <div className={`${base.wrap} ${styles.grid}`}>
        <ChapterWord initial="B" rest="e" className={styles.areaLetter} />
        <div className={styles.areaWords}>
          <p className={`${base.label} ${styles.label}`} data-label="">
            {copy(about.purpose.label)}
          </p>
          <h2 id="purpose-title" className={`${base.display} ${styles.heading}`}>
            {about.purpose.lines.map((line) => (
              <span key={line}>{copy(line)}</span>
            ))}
          </h2>
          <p className={styles.body}>{copy(about.purpose.mission)}</p>
        </div>
      </div>
    </section>
  );
}

function Roots() {
  const copy = useCopy();
  return (
    <section id="roots" className={styles.part} data-part="roots" aria-labelledby="roots-title">
      <div className={`${base.wrap} ${styles.grid}`}>
        <ChapterWord initial="i" rest="n" className={styles.areaLetter} />
        <div className={styles.areaWords}>
          <p className={`${base.label} ${styles.label}`} data-label="">
            {copy(about.roots.label)}
          </p>
          <h2 id="roots-title" className={`${base.display} ${styles.heading}`}>
            {copy(about.roots.title)}
          </h2>
          <p className={styles.body}>{copy(about.roots.text)}</p>
          <Link
            href={routes.scientists}
            className={`${base.pill} ${base.pillGhost} ${styles.more}`}
          >
            {copy(about.roots.link)} <ArrowRight size={18} aria-hidden="true" />
          </Link>
        </div>
        <figure className={`${styles.print} ${styles.areaArt}`} data-print="">
          <Image
            className={`${base.ink} ${styles.pool}`}
            src={pool.src}
            alt=""
            width={pool.width}
            height={pool.height}
            sizes="(max-width: 899px) 90vw, 560px"
            data-pool=""
            data-bloom=""
          />
          <span className={styles.mount} data-mount="">
            <Image
              src={liu.src}
              alt={copy(about.roots.photo.alt)}
              width={liu.width}
              height={liu.height}
              sizes="(max-width: 899px) 220px, 260px"
            />
          </span>
        </figure>
      </div>
    </section>
  );
}

function Good() {
  const copy = useCopy();
  const years = copy(about.experience.stats[1].unit);
  return (
    <div className={styles.part} data-part="good">
      <section
        id="experience"
        className={`${base.wrap} ${styles.grid} ${styles.experience}`}
        aria-labelledby="experience-title"
      >
        <ChapterWord initial="G" rest="ood" className={styles.areaLetter} />
        <div className={styles.areaWords}>
          <p className={`${base.label} ${styles.label}`} data-label="">
            {copy(about.experience.label)}
          </p>
          <h2 id="experience-title" className={`${base.display} ${styles.heading}`}>
            {copy(about.experience.title)}
          </h2>
          <dl className={styles.figures}>
            <div>
              <dt>{copy(about.roots.stat.label)}</dt>
              <dd>
                <CountUp to={280} suffix="+" className={styles.figure} />
              </dd>
            </div>
            <div>
              <dt>{copy(about.experience.stats[0].label)}</dt>
              <dd>
                <span className={styles.figure}>{about.experience.stats[0].value}</span>
              </dd>
            </div>
            <div>
              <dt>{copy(about.experience.stats[1].label)}</dt>
              <dd>
                <CountUp to={20} suffix="+" className={styles.figure} />
                <span className={styles.unit}> {years}</span>
              </dd>
            </div>
          </dl>
        </div>
        <figure className={`${styles.rings} ${styles.areaArt}`} data-rings="">
          <span className={styles.ringsBody}>
            <Image
              className={base.ink}
              src={rings.src}
              alt={copy(RINGS_ALT)}
              width={rings.width}
              height={rings.height}
              sizes="(max-width: 899px) 70vw, 340px"
              data-bloom=""
            />
            <span className={base.gold} style={{ ["--gold" as string]: `url(${rings.gold})` }} />
          </span>
          <figcaption className={base.caption}>{copy(drafts.illustration)}</figcaption>
        </figure>
      </section>
      <section
        id="promise"
        className={`${base.wrap} ${styles.promise}`}
        aria-labelledby="promise-title"
      >
        <p className={`${base.label} ${styles.label}`} data-label="">
          {copy(about.promise.label)}
        </p>
        <h2 id="promise-title" className={`${base.display} ${styles.heading}`}>
          {copy(about.promise.title)}
        </h2>
        <ul className={styles.promises}>
          {about.promise.items.map((item, i) => (
            <li key={item.title} data-promise="">
              <Image
                className={`${base.ink} ${styles.promiseDot}`}
                src={dots[i].src}
                alt=""
                width={dots[i].width}
                height={dots[i].height}
                sizes="92px"
                data-bloom=""
                style={{ "--bloom-delay": i * 260 } as CSSProperties}
              />
              <h3>{copy(item.title)}</h3>
              <p>{copy(item.text)}</p>
              {i === 3 && <Greetings className={styles.greetings} />}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

function Closing() {
  const copy = useCopy();
  const dialogs = useSiteDialogs();
  return (
    <section
      id="closing"
      className={`${styles.part} ${styles.closing}`}
      data-part="closing"
      aria-labelledby="closing-title"
    >
      <div className={`${base.wrap} ${styles.pause}`}>
        <ChapterWord initial="H" rest="ealth" size="closing" />
        <h2 id="closing-title" className={`${base.display} ${styles.heading}`}>
          {copy(about.closing.title)}
        </h2>
        <p className={styles.body}>{copy(about.closing.text)}</p>
        <div className={styles.actions}>
          <button type="button" className={base.pill} onClick={dialogs.openAsk}>
            {copy(about.closing.primary)}
          </button>
          <Link href={routes.products} className={`${base.pill} ${base.pillGhost}`}>
            {copy(about.closing.secondary)}
          </Link>
        </div>
      </div>
    </section>
  );
}

export function AboutInk() {
  return (
    <InkPage current="about" className={styles.letterPage}>
      {() => (
        <div className={styles.sheet} data-sheet="">
          <Opening />
          <Purpose />
          <Roots />
          <Good />
          <Closing />
        </div>
      )}
    </InkPage>
  );
}
