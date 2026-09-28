"use client";

import Image from "next/image";
import { useId, useRef } from "react";
import { useCopy } from "@/i18n/use-copy";
import type { ProductPage } from "./product-types";
import { anchorId, useArrivals, type Chapter } from "./template-chapters-kit";
import styles from "./template-chapters.module.css";

// Chapter 5, the people (Design Vault #005: a portrait beside a few plain lines). Only people who
// agreed to a photograph have one; everyone else is text only, continuing in the text column.
// Their lines are introductions, not quotes, so they carry no quotation marks.
export function PeopleChapter({
  product,
  chapter,
  reduced,
}: {
  product: ProductPage;
  chapter: Chapter;
  reduced: boolean;
}) {
  const copy = useCopy();
  const root = useRef<HTMLElement>(null);
  const titleId = useId();
  useArrivals(root, reduced);

  const pictured = product.people.filter((person) => person.photo);
  const plain = product.people.filter((person) => !person.photo);

  return (
    <section
      ref={root}
      id={anchorId(chapter.id)}
      data-chapter={chapter.id}
      data-tone={chapter.tone}
      tabIndex={-1}
      aria-labelledby={titleId}
      className={`${styles.chapter} ${styles.people}`}
    >
      <header className={styles.chapterHead}>
        <h2 id={titleId} className={styles.statement} data-heading>
          {copy("The people behind the formula")}
        </h2>
      </header>

      {pictured.map((person) => (
        <article key={person.name} className={styles.person}>
          {person.photo && (
            <figure className={styles.portrait} data-reveal>
              <Image
                src={person.photo.src}
                width={person.photo.width}
                height={person.photo.height}
                alt={copy(person.photo.alt)}
                sizes="(max-width: 860px) 92vw, 440px"
              />
            </figure>
          )}
          <div>
            <h3 className={styles.personName} data-reveal>
              {copy(person.name)}
            </h3>
            <p className={styles.personTitle} data-reveal>
              {copy(person.title)}
            </p>
            {person.lines.map((line, index) => (
              <p
                key={index}
                className={index === 0 ? styles.personLead : styles.personLine}
                data-reveal
              >
                {copy(line)}
              </p>
            ))}
          </div>
        </article>
      ))}

      {plain.length > 0 && (
        <div className={styles.plainPeople} data-alone={pictured.length === 0}>
          <div className={styles.plainList}>
            {plain.map((person) => (
              <article key={person.name} className={styles.plainPerson} data-reveal>
                <h3 className={styles.personName}>{copy(person.name)}</h3>
                <p className={styles.personTitle}>{copy(person.title)}</p>
                {person.lines.map((line, index) => (
                  <p key={index} className={styles.personLine}>
                    {copy(line)}
                  </p>
                ))}
              </article>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
