"use client";

import { useCopy } from "@/i18n/use-copy";
import { ask } from "./science-content";
import styles from "./ask-science.module.css";
import { useReveal } from "./use-reveal";

// Ask BiGH Science: what it will be, how an answer is made, and an honest "not open yet".
// No form: the service is not accepting questions.
export function AskScience() {
  const copy = useCopy();
  const ref = useReveal<HTMLDivElement>();

  return (
    <section id="ask" className={styles.ask} data-tone="dark">
      <div className={styles.inner}>
        <div className={styles.copy}>
          <p className={styles.eyebrow}>{copy(ask.eyebrow)}</p>
          <h2 className={styles.title}>{copy(ask.title)}</h2>
          <p className={styles.lead}>{copy(ask.lead)}</p>
          <p className={styles.text}>{copy(ask.text)}</p>
          <div className={styles.status}>
            <span className={styles.pill}>{copy(ask.status)}</span>
            <p>{copy(ask.note)}</p>
          </div>
        </div>
        <div ref={ref} className={styles.side}>
          <p className={styles.examplesLabel}>{copy(ask.examplesLabel)}</p>
          <ul className={styles.examples}>
            {ask.examples.map((question, index) => (
              <li key={question} style={{ "--i": index } as React.CSSProperties}>
                {copy(question)}
              </li>
            ))}
          </ul>
          <ol className={styles.steps}>
            {ask.steps.map((step, index) => (
              <li key={step}>
                <span className={styles.number}>{index + 1}</span>
                <p>{copy(step)}</p>
              </li>
            ))}
          </ol>
        </div>
      </div>
    </section>
  );
}
