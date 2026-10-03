"use client";

import Image from "next/image";
import { ArrowRight } from "lucide-react";
import { useCopy } from "@/i18n/use-copy";
import { facts, scientists } from "../content";
import { useHomeDialogs } from "../dialogs";
import { halo, liu } from "./assets";
import base from "./look-ink.module.css";
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

// "Good science. Real people." Dr. Liu's real photograph in a white mat, resting on one breath of
// ink (his name and field under it), and his record in large thin numerals; as the crane comp
// shows, the headline sits to the right of the photograph, beside the record. Then what his work asks, Dr. Iris Wang in words
// only, and Ask BiGH Science, on two columns with the brush line running down between them.
export function Scientists() {
  const copy = useCopy();
  const dialogs = useHomeDialogs();

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

        <figure className={styles.portrait} data-brush="liu">
          <Image
            className={`${base.ink} ${styles.halo}`}
            src={halo.src}
            alt=""
            width={halo.width}
            height={halo.height}
            sizes="(max-width: 900px) 80vw, 34vw"
            data-bloom=""
          />
          <span className={styles.mat}>
            <Image
              className={styles.photo}
              src={liu.src}
              alt={copy(scientists.name)}
              width={liu.width}
              height={liu.height}
              sizes="270px"
            />
          </span>
          <figcaption className={styles.who}>
            <span>{copy(scientists.name)},</span> <span>{copy(scientists.role)}</span>
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
        <h3 className={`${base.display} ${styles.askTitle}`}>{copy(scientists.ask.title)}</h3>
        <div className={styles.askBody} data-brush="ask-body">
          <p className={`${base.body} ${styles.askText}`}>{copy(scientists.ask.text)}</p>
          <button type="button" className={base.pill} onClick={dialogs.openAsk}>
            {copy(scientists.ask.link)} <ArrowRight size={18} aria-hidden="true" />
          </button>
        </div>
      </div>
    </section>
  );
}
