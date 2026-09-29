"use client";

import Image from "next/image";
import { useCopy } from "@/i18n/use-copy";
import { health } from "./science-content";
import styles from "./health-doors.module.css";
import { useReveal } from "./use-reveal";

// Health explained: three round doors, one per planned article (after Seed's circles, Design Vault
// #042). Each circle is a crop of a render the homepage already uses. The articles are not written
// yet, so each door says so.
export function HealthDoors() {
  const copy = useCopy();
  const ref = useReveal<HTMLDivElement>();

  return (
    <section id="health" className={styles.health} data-tone="light">
      <div className={styles.head}>
        <p className={styles.eyebrow}>{copy(health.eyebrow)}</p>
        <h2 className={styles.title}>{copy(health.title)}</h2>
        <p className={styles.text}>{copy(health.text)}</p>
      </div>
      <div ref={ref} className={styles.doors}>
        {health.doors.map((door, index) => (
          <article
            key={door.topic}
            className={styles.door}
            style={{ "--i": index } as React.CSSProperties}
          >
            <div className={`${styles.circle} ${index === 1 ? styles.drop : ""}`}>
              <Image src={door.image} alt="" fill sizes="(max-width: 760px) 70vw, 300px" />
            </div>
            <p className={styles.topic}>
              <span>{String(index + 1).padStart(2, "0")}</span> {copy(door.topic)}
            </p>
            <h3 className={styles.doorTitle}>{copy(door.title)}</h3>
            <p className={styles.preview}>{copy(door.preview)}</p>
            <span className={styles.soon}>{copy(health.soon)}</span>
          </article>
        ))}
      </div>
    </section>
  );
}
