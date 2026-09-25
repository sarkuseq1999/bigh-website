"use client";

import Image from "next/image";
import { ArrowRight } from "lucide-react";
import type { ReactNode } from "react";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { about, media, routes } from "./about-content";
import type { LookProps } from "./about-page";
import { Sentences } from "./sentences";
import { useReveal } from "./use-reveal";
import styles from "./look-bold.module.css";

// Look C, "Bold": BiGH's cobalt and lime in full color blocks. The one bold move is Timeline's
// picture-inside-the-headline (Design Vault #006, which Mo loved): small rounded pictures open up
// between the words. The pictures are decoration only; the words read the same without them.

function Pill({
  src,
  position = "50% 50%",
  zoom = 1,
}: {
  src: string;
  position?: string;
  zoom?: number;
}) {
  return (
    <span className={styles.pill} aria-hidden="true">
      <Image
        src={src}
        alt=""
        fill
        sizes="260px"
        className={styles.pillImage}
        style={{ objectPosition: position, transform: zoom === 1 ? undefined : `scale(${zoom})` }}
      />
    </span>
  );
}

// Puts a picture before `anchor` inside a translated line. Where a translation doesn't contain
// the English anchor, the line simply shows without the picture.
function withPill(text: string, anchor: string, pill: ReactNode) {
  const at = text.indexOf(anchor);
  if (at < 1) return text;
  return (
    <>
      {text.slice(0, at).trimEnd()} {pill} {text.slice(at)}
    </>
  );
}

export function LookBold({ onAsk }: LookProps) {
  const copy = useCopy();
  const hero = useReveal<HTMLHeadingElement>(0.4);
  // Waits until the line is well inside the window, so phones see the pictures open.
  const purpose = useReveal<HTMLHeadingElement>(0.2, "0px 0px -30% 0px");
  const [firstLine, secondLine] = about.purpose.lines;

  return (
    <>
      <section className={styles.hero} aria-labelledby="about-title">
        <p className={styles.label}>{copy(about.hero.label)}</p>
        <h1 ref={hero} id="about-title" className={styles.title}>
          {withPill(
            copy(about.hero.title),
            "Good Health.",
            <Pill src={media.mitochondrion} zoom={1.45} />,
          )}
        </h1>
        <p className={styles.lead}>
          <Sentences text={copy(about.hero.lead)} />
        </p>
      </section>

      <section id="purpose" className={styles.purpose} aria-labelledby="purpose-title">
        <p className={styles.label}>{copy(about.purpose.label)}</p>
        <h2 ref={purpose} id="purpose-title" className={styles.statement}>
          <span>
            {withPill(copy(firstLine), "parts.", <Pill src={media.coast} position="58% 30%" />)}
          </span>
          <span>
            {withPill(
              copy(secondLine),
              "cells.",
              <Pill src={media.cellStill} position="72% 50%" />,
            )}
          </span>
        </h2>
        <p className={styles.mission}>{copy(about.purpose.mission)}</p>
      </section>

      <section id="roots" className={styles.roots} aria-labelledby="roots-title">
        <p className={styles.giantStat}>
          <span className={styles.giant}>{about.roots.stat.value}</span>
          <span className={styles.giantLabel}>{copy(about.roots.stat.label)}</span>
        </p>
        <div>
          <p className={styles.label}>{copy(about.roots.label)}</p>
          <h2 id="roots-title" className={styles.heading}>
            {copy(about.roots.title)}
          </h2>
          <p className={styles.body}>{copy(about.roots.text)}</p>
          <div className={styles.person}>
            <span className={styles.face}>
              <Image
                src={about.roots.photo.src}
                alt={copy(about.roots.photo.alt)}
                fill
                sizes="92px"
                className={styles.faceImage}
              />
            </span>
            <Link href={routes.scientists} className={styles.textLink}>
              {copy(about.roots.link)} <ArrowRight size={20} aria-hidden="true" />
            </Link>
          </div>
        </div>
      </section>

      <section id="experience" className={styles.experience} aria-labelledby="experience-title">
        <div>
          <p className={styles.label}>{copy(about.experience.label)}</p>
          <h2 id="experience-title" className={styles.big}>
            {copy(about.experience.title)}
          </h2>
          <ul className={styles.stats}>
            {about.experience.stats.map((stat) => (
              <li key={stat.value}>
                <span className={styles.number}>
                  {stat.value}
                  {stat.unit && <span className={styles.unit}>{` ${copy(stat.unit)}`}</span>}
                </span>
                <span className={styles.statLabel}>{copy(stat.label)}</span>
              </li>
            ))}
          </ul>
        </div>
        <div className={styles.bottle}>
          <Image
            src={media.nuricell}
            alt={copy("{name} bottle", { name: "NuriCell" })}
            fill
            sizes="(max-width: 900px) 70vw, 440px"
            className={styles.bottleImage}
          />
        </div>
      </section>

      <section id="promise" className={styles.promise} aria-labelledby="promise-title">
        <p className={styles.label}>{copy(about.promise.label)}</p>
        <h2 id="promise-title" className={styles.big}>
          {copy(about.promise.title)}
        </h2>
        <ul className={styles.promises}>
          {about.promise.items.map((item) => (
            <li key={item.title}>
              <span className={styles.dot} aria-hidden="true" />
              <h3>{copy(item.title)}</h3>
              <p>{copy(item.text)}</p>
            </li>
          ))}
        </ul>
      </section>

      <section className={styles.closing} aria-labelledby="closing-title">
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
