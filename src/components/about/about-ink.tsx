"use client";

import Image from "next/image";
import { ArrowRight } from "lucide-react";
import { gold, halo, inkstone, liu, mito } from "@/components/home-v2/look-ink/assets";
import { useSiteDialogs } from "@/components/ink/dialogs";
import { InkPage } from "@/components/ink/ink-page";
import base from "@/components/ink/ink.module.css";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { about, drafts, routes } from "./about-content";
import { aboutRoute } from "./about-route";
import { Acronym } from "./acronym";
import { CountUp } from "./count-up";
import { Greetings } from "./greetings";
import styles from "./about-ink.module.css";

// The About page in the Ink & Gold look (October 5, 2026; Mo approved the mockup
// reference/ink-pages/mockups/about.jpg; the words are the locked ones in about-content.ts).
// "Be in Good Health." beside the ink cell (the homepage's painting), whose gold leaf comes up as
// the page opens; then four parts down the brush line (purpose, scientific roots, experience,
// promise) and the page's one centred pause, Ask BiGH Science, under the inkstone.

const CELL_ALT = "A mitochondrion, painted in ink, with two gold folds where energy is made";

function sentences(text: string) {
  return text.match(/[^.!?。！？]+[.!?。！？]*\s*/gu)?.map((part) => part.trim()) ?? [text];
}

// A station waits for the brush from the first paint (the purpose's stands in the first screen
// on a large window, where it would otherwise show, fade out as the line starts, and come back).
function Station({ id, label }: { id: string; label: string }) {
  return (
    <p
      className={`${base.station} ${styles.station}`}
      data-station=""
      data-side="left"
      data-brush={`st-${id}`}
      data-reached="false"
    >
      {label}
    </p>
  );
}

// The opening carries no "opening" brush anchor: About has no approved opening stroke to keep, so
// the brush paints its whole line as the page's line (about-route.ts).
function Opening() {
  const copy = useCopy();
  return (
    <section className={styles.opening} aria-labelledby="about-title">
      <div className={`${base.wrap} ${styles.openingGrid}`}>
        <div className={styles.openingWords}>
          <p className={styles.kicker}>{copy(about.hero.label)}</p>
          <Acronym className={styles.title} />
          <p className={styles.lead}>
            {sentences(copy(about.hero.lead)).map((sentence) => (
              <span key={sentence}>{sentence}</span>
            ))}
          </p>
        </div>
        <figure className={styles.cell} data-brush="about-cell">
          <span className={styles.cellBody}>
            <Image
              className={base.ink}
              src={mito.glow.src}
              alt={copy(CELL_ALT)}
              width={mito.glow.width}
              height={mito.glow.height}
              sizes="(max-width: 899px) 100vw, 52vw"
              priority
              data-bloom="waiting"
            />
            <span
              className={`${base.gold} ${styles.leaf}`}
              style={{ ["--gold" as string]: `url(${gold.mito})` }}
            />
            <span
              className={styles.charge}
              data-charge=""
              style={{ ["--gold" as string]: `url(${gold.mito})` }}
            />
          </span>
          <figcaption className={base.caption}>{copy(drafts.illustration)}</figcaption>
        </figure>
      </div>
    </section>
  );
}

function Purpose() {
  const copy = useCopy();
  return (
    <section id="purpose" className={styles.part} aria-labelledby="purpose-title">
      <div className={`${base.wrap} ${styles.partGrid}`}>
        <Station id="purpose" label={copy(about.purpose.label)} />
        <div className={styles.content}>
          <h2 id="purpose-title" className={`${base.display} ${styles.statement}`}>
            {about.purpose.lines.map((line) => (
              <span key={line}>{copy(line)}</span>
            ))}
          </h2>
          <p className={styles.body} data-brush="purpose-body">
            {copy(about.purpose.mission)}
          </p>
        </div>
      </div>
    </section>
  );
}

function Roots() {
  const copy = useCopy();
  return (
    <section id="roots" className={styles.part} aria-labelledby="roots-title">
      <div className={`${base.wrap} ${styles.partGrid}`}>
        <Station id="roots" label={copy(about.roots.label)} />
        <div className={`${styles.content} ${styles.roots}`} data-brush="roots">
          <figure className={styles.print}>
            <Image
              className={`${base.ink} ${styles.halo}`}
              src={halo.src}
              alt=""
              width={halo.width}
              height={halo.height}
              sizes="560px"
              data-bloom=""
            />
            <span className={styles.mount}>
              <Image
                src={liu.src}
                alt={copy(about.roots.photo.alt)}
                width={liu.width}
                height={liu.height}
                sizes="(max-width: 899px) 220px, 300px"
              />
            </span>
          </figure>
          <div className={styles.rootsWords}>
            <h2 id="roots-title" className={`${base.display} ${styles.heading}`}>
              {copy(about.roots.title)}
            </h2>
            <p className={styles.body}>{copy(about.roots.text)}</p>
            <Link href={routes.scientists} className={`${base.pill} ${base.pillGhost}`}>
              {copy(about.roots.link)} <ArrowRight size={18} aria-hidden="true" />
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

function Experience() {
  const copy = useCopy();
  const years = copy(about.experience.stats[1].unit);
  return (
    <section id="experience" className={styles.part} aria-labelledby="experience-title">
      <div className={`${base.wrap} ${styles.partGrid}`}>
        <Station id="experience" label={copy(about.experience.label)} />
        <div className={styles.content}>
          <h2 id="experience-title" className={`${base.display} ${styles.heading}`}>
            {copy(about.experience.title)}
          </h2>
          <dl className={styles.figures} data-brush="figures">
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
      </div>
    </section>
  );
}

function Promises() {
  const copy = useCopy();
  return (
    <section id="promise" className={styles.part} aria-labelledby="promise-title">
      <div className={`${base.wrap} ${styles.partGrid}`}>
        <Station id="promise" label={copy(about.promise.label)} />
        <div className={`${styles.content} ${styles.promise}`}>
          <h2 id="promise-title" className={`${base.display} ${styles.heading}`}>
            {copy(about.promise.title)}
          </h2>
          <ul className={styles.promises}>
            {about.promise.items.map((item, i) => (
              <li key={item.title} data-brush={`promise-${i}`}>
                <h3>{copy(item.title)}</h3>
                <p>{copy(item.text)}</p>
                {i === 3 && <Greetings className={styles.greetings} />}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}

function Closing() {
  const copy = useCopy();
  const dialogs = useSiteDialogs();
  return (
    <section id="closing" className={styles.closing} aria-labelledby="closing-title">
      <div className={`${base.wrap} ${styles.pause}`}>
        <figure className={styles.inkstone}>
          <Image
            className={base.ink}
            src={inkstone.src}
            alt=""
            width={inkstone.width}
            height={inkstone.height}
            sizes="(max-width: 720px) 70vw, min(26vw, 400px)"
            data-bloom=""
          />
          <figcaption className={base.caption}>{copy(drafts.illustration)}</figcaption>
        </figure>
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
    <InkPage current="about" route={aboutRoute}>
      {() => (
        <>
          <Opening />
          <Purpose />
          <Roots />
          <Experience />
          <Promises />
          <Closing />
        </>
      )}
    </InkPage>
  );
}
