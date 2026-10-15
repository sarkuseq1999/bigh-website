"use client";

import { ArrowRight, ArrowUpRight, Minus, Plus } from "lucide-react";
import Image from "next/image";
import { useState } from "react";
import { researchItems } from "@/components/home/research-data";
import { useSiteDialogs } from "@/components/ink/dialogs";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { ask, health, ink, research } from "../science-content";
import { scienceArt } from "./science-art";
import { Strip } from "./strip";
import styles from "./explore.module.css";

const KEY = research.key.map((url) => researchItems.find((item) => item.url === url)!);

/** A line of small facts ("2002 · Animal study · PNAS"): each part stays whole, with its dot. */
function Meta({ parts }: { parts: string[] }) {
  return (
    <p className={styles.meta}>
      {parts.map((part, index) => (
        <span key={index}>
          {index ? " " : null}
          <span className={styles.part}>{index < parts.length - 1 ? `${part} ·` : part}</span>
        </span>
      ))}
    </p>
  );
}

/** A dash never starts a line: "What are mitochondria—and why do they matter?" breaks after it. */
const keepDash = (text: string) => text.replace(/\s*—/g, "\u2060—");

/** The research: the scroll rack, the three key studies, then all 36 sources on request. */
export function Research() {
  const copy = useCopy();
  const [all, setAll] = useState(false);
  return (
    <Strip
      id="research"
      label={research.eyebrow}
      title={research.title}
      lead={research.text}
      art={scienceArt.scrolls}
      phone={scienceArt.scrolls.phone}
      alt={ink.scrollsAlt}
    >
      <ul className={`${styles.cols} ${styles.rows}`}>
        {KEY.map((item) => (
          <li key={item.url} className={styles.col}>
            {/* year · kind · journal: the kind is the first part of the category */}
            <Meta parts={[copy(item.year), copy(item.category).split(" · ")[0], item.journal]} />
            <h3 className={styles.colTitle}>{copy(item.title)}</h3>
            <p className={styles.text}>{copy(item.text)}</p>
            <div className={styles.links}>
              <a className={styles.go} href={item.url} target="_blank" rel="noreferrer">
                {copy(ink.readStudy)} <ArrowUpRight size={16} aria-hidden="true" />
              </a>
              {research.byLiu.includes(item.url) ? (
                <span className={styles.tag}>{copy(research.tag)}</span>
              ) : null}
            </div>
          </li>
        ))}
      </ul>
      <div className={styles.after}>
        <button
          type="button"
          className={`${base.pill} ${base.pillGhost}`}
          aria-expanded={all}
          aria-controls="research-all"
          onClick={() => setAll(!all)}
        >
          {all ? copy(research.hideAll) : copy(research.seeAll, { count: researchItems.length })}
          {all ? <Minus size={18} aria-hidden="true" /> : <Plus size={18} aria-hidden="true" />}
        </button>
        <p className={styles.note}>{copy(research.note)}</p>
      </div>
      <div id="research-all" className={styles.groups} hidden={!all}>
        {all
          ? research.groups.map((group) => (
              <div key={group.type} className={styles.group}>
                <h3 className={styles.groupTitle}>{copy(group.title)}</h3>
                <p className={styles.text}>{copy(group.text)}</p>
                {researchItems
                  .filter((item) => item.type === group.type)
                  .map((item) => (
                    <details key={item.url} className={styles.row}>
                      <summary>
                        <span className={styles.meta}>{copy(item.year)}</span>
                        <span>
                          {copy(item.title)}
                          {research.byLiu.includes(item.url) ? (
                            <span className={`${styles.tag} ${styles.rowTag}`}>
                              {copy(research.tag)}
                            </span>
                          ) : null}
                        </span>
                        <Plus className={styles.plus} size={22} aria-hidden="true" />
                      </summary>
                      <div className={styles.rowBody}>
                        <p className={styles.text}>{copy(item.text)}</p>
                        <a className={styles.go} href={item.url} target="_blank" rel="noreferrer">
                          {copy("Read original source")}{" "}
                          <ArrowUpRight size={16} aria-hidden="true" />
                        </a>
                      </div>
                    </details>
                  ))}
              </div>
            ))
          : null}
      </div>
    </Strip>
  );
}

/** Health explained: one painting of three scenes over the three articles (on phones, each scene
 *  over its own article); each opens the kit's short explainer sheet. */
export function Health() {
  const copy = useCopy();
  const dialogs = useSiteDialogs();
  return (
    <Strip
      id="health"
      label={health.eyebrow}
      title={health.title}
      lead={health.text}
      art={scienceArt.health}
      alt={ink.healthAlt}
      wideOnly
    >
      <ul className={`${styles.cols} ${styles.rows}`}>
        {health.doors.map((door, index) => {
          const scene = scienceArt.health.scenes[index];
          return (
            <li key={door.topic} className={styles.col} data-scene="">
              <figure className={styles.sceneFigure}>
                <Image
                  className={`${base.ink} ${styles.scene}`}
                  src={scene.src}
                  width={scene.width}
                  height={scene.height}
                  alt={copy(ink.sceneAlts[index])}
                  sizes="360px"
                  data-bloom="waiting"
                />
                <figcaption className={base.caption}>{copy(ink.illustration)}</figcaption>
              </figure>
              <p className={styles.meta}>{copy(door.topic)}</p>
              <h3 id={`health-title-${index}`} className={styles.colTitle}>
                {keepDash(copy(door.title))}
              </h3>
              <p className={styles.text}>{copy(door.preview)}</p>
              {/* Three buttons with one name: each is described by its own article's title. */}
              <button
                type="button"
                className={styles.go}
                aria-describedby={`health-title-${index}`}
                onClick={() => dialogs.openArticle(index)}
              >
                {copy(ink.explainer)} <ArrowRight size={16} aria-hidden="true" />
              </button>
            </li>
          );
        })}
      </ul>
    </Strip>
  );
}

/** Ask BiGH Science: two mugs on a table, the three steps, its status. */
export function Ask() {
  const copy = useCopy();
  return (
    <Strip
      id="ask"
      label={ask.eyebrow}
      title={ask.title}
      lead={`${copy(ask.lead)} ${copy(ask.text)}`}
      art={scienceArt.mugs}
      phone={scienceArt.mugs.phone}
      alt={ink.mugsAlt}
    >
      <ol className={styles.cols}>
        {ask.steps.map((step, index) => (
          <li key={step} className={styles.col}>
            <span className={styles.number}>{index + 1}</span>
            <p className={styles.text}>{copy(step)}</p>
          </li>
        ))}
      </ol>
      <div className={`${styles.after} ${styles.last}`}>
        <span className={styles.status}>{copy(ask.status)}</span>
        <p className={styles.note}>{copy(ask.note)}</p>
      </div>
    </Strip>
  );
}
