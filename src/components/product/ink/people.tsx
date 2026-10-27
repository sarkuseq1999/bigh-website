"use client";

import Image from "next/image";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { InkProduct } from "../product-types";
import { CAPTIONS, InkChapter, InkFigure, titleId } from "./ink-chapter";
import { isNuricell, NURICELL_PEOPLE_PHONE_SIZES, nuricellSizes } from "./nuricell-layout";
import styles from "./product-ink.module.css";

// Chapter 5: the person behind the formula. Dr. Liu as a painting in ink and colour (Mo's call,
// October 9, 2026; never black-and-white: in Asia that signals a person has died); a person
// without a painting keeps their photo on its mat; anyone else is text only, under the first. A
// painting of the person's work rather than of them (Dr. Wang's mortar) is captioned "Illustration".
// NuriCell's (Mo picked A2, October 26, 2026): his portrait in the view west, one painting across
// the page with the words in its sky, framed again for phones; no label over his name, a lead line
// in ink and a note saying what kind of study it was.
export function People({ product }: { product: InkProduct }) {
  const copy = useCopy();
  const [lead, ...others] = product.people;
  if (!lead) return null;
  const picture = lead.painting ? (
    <InkFigure
      art={lead.painting}
      alt={lead.painting.alt}
      caption={lead.paintingOf === "work" ? CAPTIONS.illustration : CAPTIONS.portrait}
      sizes={nuricellSizes(product, "people", lead.painting)}
      phone={
        lead.paintingPhone
          ? { art: lead.paintingPhone, sizes: NURICELL_PEOPLE_PHONE_SIZES }
          : undefined
      }
    />
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
      {isNuricell(product) ? null : (
        <p className={`${base.label} ${styles.label}`}>{copy("The people behind the formula")}</p>
      )}
      <h2 id={titleId("people")} className={`${base.display} ${styles.heading}`}>
        {copy(lead.name)}
      </h2>
      <p className={styles.role}>{copy(lead.title)}</p>
      {lead.lead ? <p className={styles.personLead}>{copy(lead.lead)}</p> : null}
      {lead.lines.map((line) => (
        <p key={line} className={styles.text}>
          {copy(line)}
        </p>
      ))}
      {lead.note ? (
        <p className={`${styles.small} ${styles.personNote}`}>{copy(lead.note)}</p>
      ) : null}
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
