"use client";

import Image from "next/image";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { InkProduct } from "../product-types";
import { CAPTIONS, InkChapter, InkFigure, titleId } from "./ink-chapter";
import styles from "./product-ink.module.css";

// Chapter 5: the person behind the formula. Dr. Liu as a painting in ink and colour (Mo's call,
// October 9, 2026; never black-and-white: in Asia that signals a person has died); a person
// without a painting keeps their photo on its mat; anyone else is text only, under the first.
export function People({ product }: { product: InkProduct }) {
  const copy = useCopy();
  const [lead, ...others] = product.people;
  if (!lead) return null;
  const picture = lead.painting ? (
    <InkFigure art={lead.painting} alt={lead.painting.alt} caption={CAPTIONS.portrait} />
  ) : lead.photo ? (
    <figure className={styles.photo} data-picture="" data-stand="">
      <Image
        src={lead.photo.src}
        alt={copy(lead.photo.alt)}
        width={lead.photo.width}
        height={lead.photo.height}
        sizes="320px"
      />
    </figure>
  ) : null;
  return (
    <InkChapter id="people" picture={picture}>
      <p className={`${base.label} ${styles.label}`}>{copy("The people behind the formula")}</p>
      <h2 id={titleId("people")} className={`${base.display} ${styles.heading}`}>
        {copy(lead.name)}
      </h2>
      <p className={styles.role}>{copy(lead.title)}</p>
      {lead.lines.map((line) => (
        <p key={line} className={styles.text}>
          {copy(line)}
        </p>
      ))}
      {others.map((person) => (
        <div key={person.name} className={styles.otherPerson}>
          <h3 className={styles.subheading}>{copy(person.name)}</h3>
          <p className={styles.role}>{copy(person.title)}</p>
          {person.lines.map((line) => (
            <p key={line} className={styles.text}>
              {copy(line)}
            </p>
          ))}
        </div>
      ))}
    </InkChapter>
  );
}
