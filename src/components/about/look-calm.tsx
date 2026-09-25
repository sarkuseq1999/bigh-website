"use client";

import Image from "next/image";
import { ArrowRight } from "lucide-react";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { about, media, routes } from "./about-content";
import type { LookProps } from "./about-page";
import { Sentences } from "./sentences";
import { useScrollProgress } from "./use-scroll-progress";
import styles from "./look-calm.module.css";

// Look A, "Calm": Timeline's About page (Design Vault #014, #015). One centered idea per screen on
// paper; the one bold move is the rounded coastal photo that comes into focus as you scroll.
// Its sections are exported one by one so the "A then B" mix can borrow them.
export function LookCalm({ onAsk }: LookProps) {
  return (
    <>
      <CalmHero />
      <CalmPurpose />
      <CalmRoots />
      <CalmExperience />
      <CalmPromise />
      <CalmClosing onAsk={onAsk} />
    </>
  );
}

export function CalmHero() {
  const copy = useCopy();
  const photo = useScrollProgress<HTMLDivElement>();
  return (
    <section className={styles.hero} aria-labelledby="about-title">
      <p className={styles.label}>{copy(about.hero.label)}</p>
      <h1 id="about-title" className={styles.title}>
        {copy(about.hero.title)}
      </h1>
      <p className={styles.lead}>
        <Sentences text={copy(about.hero.lead)} />
      </p>
      <div ref={photo} className={styles.photo}>
        <Image
          src={media.coast}
          alt={copy("A woman smiling on a coastal trail in California")}
          fill
          preload
          sizes="(max-width: 1340px) 100vw, 1280px"
          className={styles.photoImage}
        />
      </div>
    </section>
  );
}

function CalmPurpose() {
  const copy = useCopy();
  return (
    <section id="purpose" className={styles.purpose} aria-labelledby="purpose-title">
      <p className={styles.label}>{copy(about.purpose.label)}</p>
      <h2 id="purpose-title" className={styles.statement}>
        {about.purpose.lines.map((line) => (
          <span key={line}>{copy(line)}</span>
        ))}
      </h2>
      <p className={styles.mission}>{copy(about.purpose.mission)}</p>
    </section>
  );
}

export function CalmRoots() {
  const copy = useCopy();
  return (
    <section id="roots" className={styles.roots} aria-labelledby="roots-title">
      <div className={styles.portrait}>
        <Image
          src={about.roots.photo.src}
          alt={copy(about.roots.photo.alt)}
          fill
          sizes="(max-width: 900px) 90vw, 520px"
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
          <span className={styles.statValue}>{about.roots.stat.value}</span>
          <span className={styles.statLabel}>{copy(about.roots.stat.label)}</span>
        </p>
        <Link href={routes.scientists} className={styles.textLink}>
          {copy(about.roots.link)} <ArrowRight size={20} aria-hidden="true" />
        </Link>
      </div>
    </section>
  );
}

function CalmExperience() {
  const copy = useCopy();
  return (
    <section id="experience" className={styles.experience} aria-labelledby="experience-title">
      <p className={styles.label}>{copy(about.experience.label)}</p>
      <h2 id="experience-title" className={styles.heading}>
        {copy(about.experience.title)}
      </h2>
      <ul className={styles.stats}>
        {about.experience.stats.map((stat) => (
          <li key={stat.value}>
            <span className={styles.bigNumber}>
              {stat.value}
              {stat.unit && <span className={styles.unit}>{` ${copy(stat.unit)}`}</span>}
            </span>
            <span className={styles.statLabel}>{copy(stat.label)}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}

export function CalmPromise() {
  const copy = useCopy();
  return (
    <section id="promise" className={styles.promise} aria-labelledby="promise-title">
      <p className={styles.label}>{copy(about.promise.label)}</p>
      <h2 id="promise-title" className={styles.heading}>
        {copy(about.promise.title)}
      </h2>
      <ul className={styles.promises}>
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

export function CalmClosing({ onAsk }: LookProps) {
  const copy = useCopy();
  return (
    <section className={styles.closing} aria-labelledby="closing-title">
      <div className={styles.closingCard}>
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
      </div>
    </section>
  );
}
