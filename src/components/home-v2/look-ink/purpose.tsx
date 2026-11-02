"use client";

import Image from "next/image";
import { ArrowDown, ArrowRight } from "lucide-react";
import { ProductAction } from "@/components/home/product-action";
import { useCopy } from "@/i18n/use-copy";
import { purpose } from "../content";
import { useSiteDialogs } from "@/components/ink/dialogs";
import {
  gold,
  purposeEndings,
  purposePainting,
  purposePelicans,
  type PurposeEnding,
} from "./assets";
import base from "@/components/ink/ink.module.css";
import styles from "./purpose.module.css";
import { useTint } from "./ink-color";

// The close, a bookend to the morning sequoias: the Big Sur coast at evening, an older couple and
// their dog on the cliff-top trail, the gold-leaf sun setting on the Pacific, five brown pelicans
// flying home (on their own layer: they fly toward the sun as the painting comes into view); the
// purpose sits in its open sky, and the brush line lifts off in the painting. Below it, on paper:
// why we do it and the three standards we keep.
// `ending` is one of the two richer closes Mo is comparing (/home-1, /home-3; assets.ts): its
// painting, its sun's gold mask and its frame on one column.
export function Purpose({ ending }: { ending?: PurposeEnding }) {
  const tint = useTint();
  const copy = useCopy();
  const dialogs = useSiteDialogs();
  const scene = ending ? purposeEndings[ending] : null;
  const land = scene ? scene.land : purposePainting;
  const birds = purposePelicans;

  return (
    <section
      id="purpose"
      className={styles.purpose}
      aria-labelledby="purpose-title"
      data-brush="purpose"
    >
      <div className={styles.scene}>
        {/* The painting with its layers (the light on the sun's leaf, the pelicans). On two
            columns it is the scene itself; on one column it is a frame of its own, so a phone
            sees the walkers, the pelicans and the sun (purpose.module.css). */}
        <div
          className={styles.plate}
          style={
            scene
              ? {
                  ["--pw" as string]: `min(${scene.phone.width}vw, 1500px)`,
                  ["--shift" as string]: `clamp(0px, ${scene.phone.left} * var(--pw), var(--pw) - 100vw)`,
                }
              : undefined
          }
        >
          <Image
            className={`${base.ink} ${styles.painting}`}
            src={tint(land.src)}
            alt=""
            width={land.width}
            height={land.height}
            sizes="(max-width: 899px) min(165vw, 1500px), 100vw"
            data-bloom=""
            data-brush="purpose-painting"
          />
          <span
            className={`${base.gold} ${styles.sunLight}`}
            style={{
              ["--gold" as string]: `url(${scene ? scene.gold : gold.purpose})`,
              aspectRatio: `${land.width} / ${land.height}`,
            }}
          />
          <span
            className={styles.flight}
            style={{
              left: `${birds.box.left * 100}%`,
              top: `${birds.box.top * 100}%`,
              width: `${birds.box.width * 100}%`,
              aspectRatio: `${birds.width} / ${birds.height}`,
            }}
          >
            <Image
              className={`${base.ink} ${styles.birds}`}
              src={tint(birds.src)}
              alt=""
              width={birds.width}
              height={birds.height}
              sizes="(max-width: 899px) 30vw, 18vw"
              data-bloom=""
              style={{ ["--bloom-delay" as string]: 500 }}
            />
          </span>
        </div>
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
          {purpose.standards.map((item, i) => (
            <li key={item.title} data-brush={`standard-${i}`}>
              <h3 className={styles.standardTitle}>{copy(item.title)}</h3>
              <p className={base.body}>{copy(item.text)}</p>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
