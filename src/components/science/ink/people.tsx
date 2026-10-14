"use client";

import Image from "next/image";
import { ArrowRight, ArrowUpRight } from "lucide-react";
import { useProductPage } from "@/components/home/product-action";
import { useSiteDialogs } from "@/components/ink/dialogs";
import base from "@/components/ink/ink.module.css";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { formulas, formulasLine, ink, iris, liu, liuNumbers } from "../science-content";
import styles from "./people.module.css";

const BOTTLE = { width: 1230, height: 1278 };

/** Dr. Liu: his real photograph on its mat, his record with its sources, his story sheet. */
export function Liu() {
  const copy = useCopy();
  const dialogs = useSiteDialogs();
  return (
    <section id="liu" className={styles.liu} aria-labelledby="liu-name">
      <div className={`${base.wrap} ${styles.liuGrid}`}>
        <figure className={styles.mount}>
          <Image
            src={liu.photo.src}
            width={liu.photo.width}
            height={liu.photo.height}
            alt={copy(liu.name)}
            sizes="(max-width: 959px) 70vw, 300px"
          />
        </figure>
        <div>
          <p className={base.caption}>{copy(liu.role)}</p>
          <h2 id="liu-name" className={styles.name}>
            {copy(liu.name)}
          </h2>
          <p className={styles.headline}>{copy(liu.headline)}</p>
          <p className={`${base.body} ${styles.intro}`}>{copy(liu.intro)}</p>
          <dl className={styles.numbers}>
            {liuNumbers.map((n) => (
              <div key={n.value}>
                <dt>
                  {n.value}
                  {n.suffix}
                </dt>
                <dd>
                  {copy(n.label)}{" "}
                  <a href={n.url} target="_blank" rel="noreferrer">
                    {copy(ink.source)} <ArrowUpRight size={14} aria-hidden="true" />
                  </a>
                </dd>
              </div>
            ))}
          </dl>
          <button
            type="button"
            className={`${base.textLink} ${styles.story}`}
            onClick={dialogs.openScientist}
          >
            {copy(liu.button)} <ArrowRight size={18} aria-hidden="true" />
          </button>
        </div>
      </div>
    </section>
  );
}

/** The five formulas: who developed each one, each bottle linking to its own page. */
export function Formulas() {
  const copy = useCopy();
  const pageOf = useProductPage();
  return (
    <section id="formulas" className={styles.formulas} aria-labelledby="formulas-title">
      <div className={base.wrap}>
        <header className={styles.head}>
          <div>
            <p className={base.caption}>{copy(ink.formulasLabel)}</p>
            <h2 id="formulas-title" className={styles.title}>
              {copy(formulasLine)}
            </h2>
          </div>
          <p className={base.body}>{copy(iris.text)}</p>
        </header>
        <ul className={styles.bottles}>
          {formulas.map((formula, index) => {
            const href = pageOf(formula.name);
            const body = (
              <>
                <Image
                  src={formula.image}
                  width={BOTTLE.width}
                  height={BOTTLE.height}
                  alt=""
                  sizes="(max-width: 959px) 40vw, 240px"
                />
                <span className={styles.bottleName}>{copy(formula.name)}</span>
              </>
            );
            return (
              <li key={formula.name} data-lead={index === 0 ? "" : undefined}>
                {href ? (
                  <Link href={href} className={styles.bottleLink}>
                    {body}
                  </Link>
                ) : (
                  <div className={styles.bottleLink}>{body}</div>
                )}
                <p className={styles.credit}>{copy(formula.credit)}</p>
              </li>
            );
          })}
        </ul>
      </div>
    </section>
  );
}
