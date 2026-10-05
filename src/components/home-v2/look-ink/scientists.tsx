"use client";

import Image from "next/image";
import { ArrowRight } from "lucide-react";
import { useCopy } from "@/i18n/use-copy";
import { facts, scientists } from "../content";
import { useSiteDialogs } from "@/components/ink/dialogs";
import { halo, inkstone, liu } from "./assets";
import base from "@/components/ink/ink.module.css";
import styles from "./scientists.module.css";

/** A fact's number is set large and any words around it small ("20+ years", "20년 이상", "Hơn 20
 *  năm"), in every language. */
function Figure({ value }: { value: string }) {
  const match = value.match(/^(.*?)(\d[\d.,]*\+?)(.*)$/);
  if (!match) return <>{value}</>;
  const [, before, number, after] = match;
  return (
    <>
      {before && <span className={styles.unit}>{before}</span>}
      {number}
      {after && <span className={styles.unit}>{after}</span>}
    </>
  );
}

// "Good science. Real people." Dr. Liu's real photograph, large, in a white mat laid down on one
// breath of ink as it blooms, his name set as a name under it; as the crane comp shows, the
// headline sits to the right of the photograph, above his record in large thin numerals, which
// ends on the mat's lower edge. Then what his work asks and Dr. Iris Wang in words only, on two
// columns with the brush line running down between them, beside the print and never under it.
// Last, Ask BiGH Science is the page's one centred pause (round 6): a small painting of a brush
// at rest on its inkstone, the headline, words and button centred under it on open paper, the
// brush line passing it in the margin.
export function Scientists() {
  const copy = useCopy();
  const dialogs = useSiteDialogs();

  return (
    <section
      id="scientists"
      className={styles.scientists}
      aria-labelledby="scientists-title"
      data-brush="scientists"
    >
      <div className={`${base.wrap} ${styles.top}`}>
        <header className={styles.head}>
          <p
            className={`${base.station} ${styles.station}`}
            data-station=""
            data-side="left"
            data-brush="st-scientists"
          >
            {copy(scientists.eyebrow)}
          </p>
          <h2 id="scientists-title" className={`${base.display} ${styles.title}`}>
            {scientists.title.map((line) => (
              <span key={line}>{copy(line)} </span>
            ))}
          </h2>
          <p className={`${base.body} ${styles.intro}`}>
            {scientists.intro.map((line) => (
              <span key={line}>{copy(line)} </span>
            ))}
          </p>
        </header>

        <figure className={styles.portrait}>
          <span className={styles.print} data-brush="liu">
            <Image
              className={`${base.ink} ${styles.halo}`}
              src={halo.src}
              alt=""
              width={halo.width}
              height={halo.height}
              sizes="(max-width: 899px) 100vw, 740px"
              data-bloom=""
            />
            <span className={styles.mat}>
              <Image
                className={styles.photo}
                src={liu.src}
                alt={copy(scientists.name)}
                width={liu.width}
                height={liu.height}
                sizes="(max-width: 899px) 260px, 380px"
              />
            </span>
          </span>
          <figcaption className={styles.who}>
            <span className={styles.name}>{copy(scientists.name)}</span>
            <span>{copy(scientists.role)}</span>
            <span>{copy(scientists.specialty)}</span>
          </figcaption>
        </figure>

        <dl className={styles.facts} data-brush="facts">
          {facts.map((fact) => (
            <div key={fact.value}>
              <dt>
                <Figure value={copy(fact.value)} />
              </dt>
              <dd>{copy(fact.label)}</dd>
            </div>
          ))}
        </dl>
      </div>

      <div className={`${base.wrap} ${styles.work}`}>
        <div className={styles.workHead}>
          <h3 className={styles.heading}>{copy(scientists.heading)}</h3>
          <p
            className={`${base.station} ${styles.station}`}
            data-station=""
            data-side="left"
            data-brush="st-work"
          >
            {copy(scientists.kicker)}
          </p>
        </div>
        <div className={styles.workMain} data-brush="work-main">
          <p className={base.body}>{copy(scientists.text)}</p>
          <button
            type="button"
            className={`${base.pill} ${base.pillGhost} ${styles.more}`}
            onClick={dialogs.openScientist}
          >
            {copy(scientists.link)} <ArrowRight size={18} aria-hidden="true" />
          </button>
          <div className={styles.iris}>
            <p className={styles.irisName}>{copy(scientists.iris.name)}</p>
            <p className={base.body}>{copy(scientists.iris.text)}</p>
          </div>
        </div>
      </div>

      <div className={`${base.wrap} ${styles.ask}`} data-brush="ask">
        <figure className={styles.askArt} aria-hidden="true" data-brush="ask-art">
          <Image
            className={`${base.ink} ${styles.inkstone}`}
            src={inkstone.src}
            alt=""
            width={inkstone.width}
            height={inkstone.height}
            sizes="(max-width: 899px) 70vw, 400px"
            data-bloom=""
          />
          <figcaption className={base.caption}>{copy("Illustration")}</figcaption>
        </figure>
        <h3 className={`${base.display} ${styles.askTitle}`} data-brush="ask-title">
          {copy(scientists.ask.title)}
        </h3>
        <p className={`${base.body} ${styles.askText}`} data-brush="ask-text">
          {copy(scientists.ask.text)}
        </p>
        <button
          type="button"
          className={`${base.pill} ${styles.askButton}`}
          onClick={dialogs.openAsk}
        >
          {copy(scientists.ask.link)} <ArrowRight size={18} aria-hidden="true" />
        </button>
      </div>
    </section>
  );
}
