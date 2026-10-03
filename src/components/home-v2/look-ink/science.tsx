"use client";

import { ArrowRight, ArrowUpRight } from "lucide-react";
import { useRef, useState, type KeyboardEvent } from "react";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { science, scienceArticles, scienceFacts } from "../content";
import { useHomeDialogs } from "../dialogs";
import { mito } from "./assets";
import base from "./look-ink.module.css";
import styles from "./science.module.css";

// "Make sense of the science." Three topics beside the SAME ink mitochondrion: close in on its two
// gold-leaf folds, where energy is made (mitochondria); whole, with a frayed edge and a few
// dry-brush flicks breaking away (free radicals, kept in balance); and, for aging cells, the young
// and the older organelle (registered onto each other) blended by an age slider, with the honesty
// line "Illustration, not a measurement".
const AGE_MIN = 30;
const AGE_MAX = 80;

export function Science() {
  const copy = useCopy();
  const dialogs = useHomeDialogs();
  const [topic, setTopic] = useState(0);
  const [age, setAge] = useState(45);
  const tabs = useRef<(HTMLButtonElement | null)[]>([]);
  const article = scienceArticles[topic];
  const aged = (age - AGE_MIN) / (AGE_MAX - AGE_MIN);

  const onKey = (event: KeyboardEvent<HTMLButtonElement>, index: number) => {
    const step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[event.key];
    if (!step) return;
    event.preventDefault();
    const next = (index + step + 3) % 3;
    setTopic(next);
    tabs.current[next]?.focus();
  };

  return (
    <section
      id="science"
      className={styles.science}
      aria-labelledby="science-title"
      data-brush="science"
    >
      <div className={`${base.wrap} ${styles.layout}`}>
        <div className={styles.copy}>
          <h2 id="science-title" className={base.display}>
            {copy(science.title)}
          </h2>
          <p className={`${base.body} ${styles.intro}`}>{copy(science.text)}</p>

          <div className={styles.tabs} role="tablist" aria-label={copy(science.title)}>
            {science.topics.map((name, i) => (
              <button
                key={name}
                ref={(node) => {
                  tabs.current[i] = node;
                }}
                type="button"
                role="tab"
                id={`ink-topic-${i}`}
                aria-selected={topic === i}
                aria-controls="ink-topic-panel"
                tabIndex={topic === i ? 0 : -1}
                className={styles.tab}
                onClick={() => setTopic(i)}
                onKeyDown={(event) => onKey(event, i)}
              >
                {copy(name)}
              </button>
            ))}
          </div>

          <div
            key={topic}
            id="ink-topic-panel"
            role="tabpanel"
            aria-labelledby={`ink-topic-${topic}`}
            className={styles.panel}
          >
            <h3 className={styles.articleTitle}>{copy(article.title)}</h3>
            <p className={base.body}>{copy(article.preview)}</p>
            <ul className={styles.facts}>
              {scienceFacts[topic].map((fact) => (
                <li key={fact}>{copy(fact)}</li>
              ))}
            </ul>
            <div className={styles.actions}>
              <Link href="/science" className={base.pill}>
                {copy(science.button)} <ArrowRight size={18} aria-hidden="true" />
              </Link>
              <button
                type="button"
                className={base.textLink}
                onClick={() => dialogs.openArticle(topic)}
              >
                {copy(science.explainer)} <ArrowUpRight size={18} aria-hidden="true" />
              </button>
            </div>
          </div>
        </div>

        <figure className={styles.figure} data-topic={topic} data-brush="science-mito">
          <div className={styles.stage} data-bloom="">
            {/* eslint-disable-next-line @next/next/no-img-element -- a layer of one painting */}
            <img
              className={`${base.ink} ${styles.layer}`}
              src={mito.closeup.src}
              alt=""
              loading="lazy"
              data-on={topic === 0}
            />
            {/* eslint-disable-next-line @next/next/no-img-element -- a layer of one painting */}
            <img
              className={`${base.ink} ${styles.layer}`}
              src={mito.glow.src}
              alt=""
              loading="lazy"
              data-on={topic === 2}
              style={topic === 2 ? { opacity: 1 - aged } : undefined}
            />
            {/* eslint-disable-next-line @next/next/no-img-element -- a layer of one painting */}
            <img
              className={`${base.ink} ${styles.layer}`}
              src={mito.radicals.src}
              alt=""
              loading="lazy"
              data-on={topic === 1}
            />
            {/* eslint-disable-next-line @next/next/no-img-element -- a layer of one painting */}
            <img
              className={`${base.ink} ${styles.layer} ${styles.aged}`}
              src={mito.aged.src}
              alt=""
              loading="lazy"
              data-on={topic === 2}
              style={{ ["--aged" as string]: aged }}
            />
          </div>
          <figcaption className={`${base.caption} ${styles.caption}`}>
            {copy("Illustrations")}
          </figcaption>

          <div className={styles.age} data-on={topic === 2} inert={topic !== 2}>
            <label className={styles.ageLabel} htmlFor="ink-age">
              <span>{copy("Age")}</span>
              <strong>{age}</strong>
            </label>
            <input
              id="ink-age"
              type="range"
              min={AGE_MIN}
              max={AGE_MAX}
              step={1}
              value={age}
              onChange={(event) => setAge(Number(event.target.value))}
              className={styles.range}
              style={{ ["--fill" as string]: `${aged * 100}%` }}
            />
            <p className={styles.honesty}>{copy(science.ageLabel)}</p>
          </div>
        </figure>
      </div>
    </section>
  );
}
