"use client";

import Image from "next/image";
import { ArrowRight } from "lucide-react";
import { useReducedMotion } from "@/components/home/use-reduced-motion";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { about, media, routes } from "./about-content";
import type { LookProps } from "./about-page";
import { Sentences } from "./sentences";
import { useReveal } from "./use-reveal";
import { useStickyProgress } from "./use-sticky-progress";
import styles from "./look-space.module.css";

// Look B, "Deep space": the homepage's navy world. The one bold move is the dive: scrolling
// from the cloud of cells (the constellation Mo liked for the set-aside closing block) into a
// single cell, the way Timeline's "How it works" changes its picture one step at a time
// (Design Vault #019–#029). Both pictures are the approved renders, shown as they are.
export function LookSpace({ onAsk }: LookProps) {
  const copy = useCopy();
  const reducedMotion = useReducedMotion();

  return (
    <>
      {reducedMotion ? <StillOpening /> : <Dive />}
      <Roots />
      <SpaceExperience />
      <PromiseSection />
      <section className={styles.closing} data-tone="light" aria-labelledby="closing-title">
        <h2 id="closing-title" className={styles.closingTitle}>
          {copy(about.closing.title)}
        </h2>
        <p className={styles.closingText}>{copy(about.closing.text)}</p>
        <div className={styles.actions}>
          <button type="button" className={styles.primary} onClick={onAsk}>
            {copy(about.closing.primary)}
          </button>
          <Link href={routes.products} className={styles.secondary}>
            {copy(about.closing.secondary)}
          </Link>
        </div>
      </section>
    </>
  );
}

function OpeningWords() {
  const copy = useCopy();
  return (
    <>
      <p className={styles.label}>{copy(about.hero.label)}</p>
      <h1 id="about-title" className={styles.title}>
        {copy(about.hero.title)}
      </h1>
      <p className={styles.lead}>
        <Sentences text={copy(about.hero.lead)} />
      </p>
    </>
  );
}

function PurposeWords() {
  const copy = useCopy();
  return (
    <>
      <p className={styles.label}>{copy(about.purpose.label)}</p>
      <h2 id="purpose-title" className={styles.statement}>
        {about.purpose.lines.map((line) => (
          <span key={line}>{copy(line)}</span>
        ))}
      </h2>
      <p className={styles.mission}>{copy(about.purpose.mission)}</p>
    </>
  );
}

// The scroll story: a tall section with a sticky stage. --p runs 0 → 1 while it scrolls past.
function Dive() {
  const stage = useStickyProgress<HTMLElement>();
  return (
    <section ref={stage} className={styles.dive} data-tone="dark" aria-labelledby="about-title">
      <span id="purpose" className={styles.purposeAnchor} />
      <div className={styles.stage}>
        {/* next/image's fill needs a relative/absolute parent; the sticky stage doesn't count. */}
        <div className={styles.layers}>
          <Image
            src={media.cells}
            alt=""
            fill
            preload
            sizes="100vw"
            className={`${styles.layer} ${styles.cluster}`}
          />
          <Image
            src={media.cellStill}
            alt=""
            fill
            sizes="100vw"
            className={`${styles.layer} ${styles.single}`}
          />
        </div>
        <div className={styles.shade} />
        <div className={styles.openingWords}>
          <OpeningWords />
        </div>
        <div className={styles.purposeWords}>
          <PurposeWords />
        </div>
      </div>
    </section>
  );
}

// With reduced motion: the same two scenes, one after the other, with nothing moving.
function StillOpening() {
  return (
    <>
      <section
        className={`${styles.still} ${styles.stillOpening}`}
        data-tone="dark"
        aria-labelledby="about-title"
      >
        <Image
          src={media.cells}
          alt=""
          fill
          preload
          sizes="100vw"
          className={`${styles.layer} ${styles.stillCluster}`}
        />
        <div className={styles.openingWords}>
          <OpeningWords />
        </div>
      </section>
      <section
        id="purpose"
        className={styles.still}
        data-tone="dark"
        aria-labelledby="purpose-title"
      >
        <Image src={media.cellStill} alt="" fill sizes="100vw" className={styles.layer} />
        <div className={styles.shade} />
        <div className={styles.purposeWords}>
          <PurposeWords />
        </div>
      </section>
    </>
  );
}

// The "A then B" mix's purpose: the same dive, telling the two lines in order. "A full life has
// many parts." sits over the cloud of many cells; diving into one cell brings "We focus on one you
// can't see: your cells." The heading for screen readers carries both lines at once; the two
// visual lines are hidden from them so nothing is read twice.
// Two separate components on purpose: the page first renders the still version (the server can't
// know the visitor's motion setting), and the moving one must mount fresh so its scroll tracking
// starts with the section in place.
export function PurposeDive() {
  const reducedMotion = useReducedMotion();
  return reducedMotion ? <StillPurpose /> : <MovingPurpose />;
}

function StillPurpose() {
  return (
    <section id="purpose" className={styles.still} data-tone="dark" aria-labelledby="purpose-title">
      <Image src={media.cellStill} alt="" fill sizes="100vw" className={styles.layer} />
      <div className={styles.shade} />
      <div className={styles.purposeWords}>
        <PurposeWords />
      </div>
    </section>
  );
}

function MovingPurpose() {
  const copy = useCopy();
  const stage = useStickyProgress<HTMLElement>();
  const [first, second] = about.purpose.lines;

  return (
    <section
      id="purpose"
      ref={stage}
      className={`${styles.dive} ${styles.purposeDive}`}
      data-tone="dark"
      aria-labelledby="purpose-title"
    >
      <h2 id="purpose-title" className={styles.srOnly}>
        {copy(first)} {copy(second)}
      </h2>
      <div className={styles.stage}>
        <div className={styles.layers}>
          <Image
            src={media.cells}
            alt=""
            fill
            sizes="100vw"
            className={`${styles.layer} ${styles.cluster}`}
          />
          <Image
            src={media.cellStill}
            alt=""
            fill
            sizes="100vw"
            className={`${styles.layer} ${styles.single}`}
          />
        </div>
        <div className={styles.shade} />
        <div className={styles.openingWords} aria-hidden="true">
          <p className={styles.label}>{copy(about.purpose.label)}</p>
          <p className={styles.lineOne}>{copy(first)}</p>
        </div>
        <div className={styles.purposeWords}>
          <p className={styles.statement} aria-hidden="true">
            {copy(second)}
          </p>
          <p className={styles.mission}>{copy(about.purpose.mission)}</p>
        </div>
      </div>
    </section>
  );
}

function Roots() {
  const copy = useCopy();
  const reveal = useReveal<HTMLDivElement>(0.3);
  return (
    <section id="roots" className={styles.roots} data-tone="dark" aria-labelledby="roots-title">
      <div ref={reveal} className={`${styles.reveal} ${styles.rootsInner}`}>
        <div className={styles.portrait}>
          <Image
            src={about.roots.photo.src}
            alt={copy(about.roots.photo.alt)}
            fill
            sizes="(max-width: 900px) 80vw, 460px"
            className={styles.portraitImage}
          />
        </div>
        <div>
          <p className={styles.label}>{copy(about.roots.label)}</p>
          <h2 id="roots-title" className={styles.heading}>
            {copy(about.roots.title)}
          </h2>
          <p className={styles.body}>{copy(about.roots.text)}</p>
          <p className={styles.stat}>
            <span className={styles.goldNumber}>{about.roots.stat.value}</span>
            <span className={styles.statLabel}>{copy(about.roots.stat.label)}</span>
          </p>
          <Link href={routes.scientists} className={styles.textLink}>
            {copy(about.roots.link)} <ArrowRight size={20} aria-hidden="true" />
          </Link>
        </div>
      </div>
    </section>
  );
}

// afterLight: in the "A then B" mix this dark section follows a light one, so it keeps its full
// top padding (in look B it follows another dark section and pads less).
export function SpaceExperience({ afterLight = false }: { afterLight?: boolean }) {
  const copy = useCopy();
  const reveal = useReveal<HTMLDivElement>(0.3);
  return (
    <section
      id="experience"
      className={`${styles.experience} ${afterLight ? styles.afterLight : ""}`}
      data-tone="dark"
      aria-labelledby="experience-title"
    >
      <div ref={reveal} className={styles.reveal}>
        <p className={styles.label}>{copy(about.experience.label)}</p>
        <h2 id="experience-title" className={styles.heading}>
          {copy(about.experience.title)}
        </h2>
        <ul className={styles.stats}>
          {about.experience.stats.map((stat) => (
            <li key={stat.value}>
              <span className={styles.goldNumber}>
                {stat.value}
                {stat.unit && <span className={styles.unit}>{` ${copy(stat.unit)}`}</span>}
              </span>
              <span className={styles.statLabel}>{copy(stat.label)}</span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

function PromiseSection() {
  const copy = useCopy();
  const reveal = useReveal<HTMLUListElement>(0.15);
  return (
    <section
      id="promise"
      className={styles.promise}
      data-tone="dark"
      aria-labelledby="promise-title"
    >
      <div className={styles.promiseHead}>
        <p className={styles.label}>{copy(about.promise.label)}</p>
        <h2 id="promise-title" className={styles.heading}>
          {copy(about.promise.title)}
        </h2>
      </div>
      <ul ref={reveal} className={`${styles.reveal} ${styles.promises}`}>
        {about.promise.items.map((item) => (
          <li key={item.title}>
            <h3>{copy(item.title)}</h3>
            <p>{copy(item.text)}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
