"use client";

import Image from "next/image";
import { ArrowDown, ArrowRight } from "lucide-react";
import { ProductAction } from "@/components/home/product-action";
import { useCopy } from "@/i18n/use-copy";
import { purpose } from "../content";
import { useHomeDialogs } from "../dialogs";
import { gold, purposeCranes, purposePainting } from "./assets";
import base from "./look-ink.module.css";
import styles from "./purpose.module.css";

// The close, a bookend to the crane: an old pine over a sea of mist, the gold-leaf sun low on the
// horizon, two cranes flying home (on their own layer: they fly toward the sun as the painting
// comes into view); the purpose sits in its open sky, and the brush line lifts off in the
// painting. Below it, on paper: why we do it and the three standards we keep.
export function Purpose() {
  const copy = useCopy();
  const dialogs = useHomeDialogs();

  return (
    <section
      id="purpose"
      className={styles.purpose}
      aria-labelledby="purpose-title"
      data-brush="purpose"
    >
      <div className={styles.scene}>
        <Image
          className={`${base.ink} ${styles.painting}`}
          src={purposePainting.src}
          alt=""
          width={purposePainting.width}
          height={purposePainting.height}
          sizes="100vw"
          data-bloom=""
          data-brush="purpose-painting"
        />
        <span
          className={`${base.gold} ${styles.sunLight}`}
          style={{ ["--gold" as string]: `url(${gold.purpose})` }}
        />
        <span
          className={styles.flight}
          style={{
            left: `${purposeCranes.box.left * 100}%`,
            top: `${purposeCranes.box.top * 100}%`,
            width: `${purposeCranes.box.width * 100}%`,
          }}
        >
          <Image
            className={`${base.ink} ${styles.cranes}`}
            src={purposeCranes.src}
            alt=""
            width={purposeCranes.width}
            height={purposeCranes.height}
            sizes="(max-width: 979px) 1px, 14vw"
            data-bloom=""
            style={{ ["--bloom-delay" as string]: 500 }}
          />
        </span>
        <div className={`${base.wrap} ${styles.statement}`}>
          <div className={styles.titleBox}>
            <h2 id="purpose-title" className={styles.title}>
              {purpose.title.map((line) => (
                <span key={line}>{copy(line)}</span>
              ))}
            </h2>
            <p
              className={`${base.station} ${styles.station}`}
              data-station=""
              data-side="right"
              data-brush="st-purpose"
            >
              {copy(purpose.eyebrow)}
            </p>
          </div>
        </div>
        <p className={`${base.caption} ${styles.tag}`}>{copy("Illustration")}</p>
      </div>

      <div className={`${base.wrap} ${styles.body}`}>
        <div className={styles.columns}>
          <div className={styles.opening}>
            <p className={styles.graphic}>
              {purpose.graphic.map((line) => (
                <span key={line}>{copy(line)}</span>
              ))}
            </p>
            <p className={styles.lead}>{copy(purpose.lead)}</p>
          </div>
          <div className={styles.text}>
            {purpose.body.map((paragraph) => (
              <p key={paragraph} className={`${base.body} ${styles.paragraph}`}>
                {copy(paragraph)}
              </p>
            ))}
            <div className={styles.links}>
              <ProductAction
                name="NuriCell"
                onOpen={() => dialogs.openProduct(0)}
                className={base.pill}
              >
                {copy(purpose.links.product)} <ArrowRight size={18} aria-hidden="true" />
              </ProductAction>
              <a href="#ink-standards" className={base.textLink}>
                {copy(purpose.links.standards)} <ArrowDown size={18} aria-hidden="true" />
              </a>
            </div>
          </div>
        </div>

        <ul id="ink-standards" className={styles.standards}>
          {purpose.standards.map((item) => (
            <li key={item.title}>
              <h3 className={styles.standardTitle}>{copy(item.title)}</h3>
              <p className={base.body}>{copy(item.text)}</p>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
