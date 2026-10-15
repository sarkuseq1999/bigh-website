"use client";

import Image from "next/image";
import type { CSSProperties, ReactNode } from "react";
import { contactShadow } from "@/components/home-v2/look-ink/assets";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { AddToCart } from "../add-to-cart";
import type { InkProduct, InkScene } from "../product-types";
import { CAPTIONS, InkChapter, keepTogether, titleId } from "./ink-chapter";
import styles from "./product-ink.module.css";

const EYEBROW_ID = `${titleId("buy")}-eyebrow`;

// Chapter 7: the real bottle standing on one bold brush stroke (Mo, round 6), or, for Green Bee
// Propolis (Mo, October 14, 2026), inside a painted scene: the same real bottle photo, never
// redrawn. The paintings and the contact shadow multiply onto the paper; the bottle photo never
// does, so this figure is not a blend group (data-stand) and not sticky. The heading is the
// product's name, which the opening's region is named after too, so this region is named by the
// eyebrow and the heading together ("Our flagship formula NuriCell"): one landmark name each.
export function Buy({ product }: { product: InkProduct }) {
  const copy = useCopy();
  const buy = product.ink.buy;
  const bottle = (
    <Image
      className={styles.buyBottle}
      src={product.bottle.src}
      alt={copy("{name} bottle", { name: product.name })}
      width={product.bottle.width}
      height={product.bottle.height}
      sizes={"scene" in buy ? "(max-width: 959px) 56vw, 340px" : "(max-width: 959px) 80vw, 470px"}
    />
  );
  return (
    <InkChapter
      id="buy"
      labelledBy={`${EYEBROW_ID} ${titleId("buy")}`}
      picture={
        "scene" in buy ? (
          <SceneStand scene={buy.scene} bottle={bottle} />
        ) : (
          <figure className={styles.buyStand} data-picture="" data-stand="">
            <Image
              className={`${base.ink} ${styles.stroke}`}
              src={buy.stroke.src}
              alt=""
              width={buy.stroke.width}
              height={buy.stroke.height}
              sizes="(max-width: 959px) 88vw, 560px"
              data-bloom="waiting"
            />
            <Image
              className={`${base.ink} ${styles.buyContact}`}
              src={contactShadow.src}
              alt=""
              width={contactShadow.width}
              height={contactShadow.height}
              sizes="200px"
            />
            {bottle}
          </figure>
        )
      }
    >
      <p id={EYEBROW_ID} className={`${base.label} ${styles.label}`}>
        {copy(product.eyebrow)}
      </p>
      <h2 id={titleId("buy")} className={`${base.display} ${styles.buyName}`}>
        {product.name}
      </h2>
      <p className={styles.focus}>{copy(product.focus)}</p>
      <dl className={styles.rows}>
        <div>
          <dt>{copy("How to take it")}</dt>
          <dd>{copy(product.serving.use)}</dd>
        </div>
        <div>
          <dt>{copy("In each bottle")}</dt>
          <dd>{keepTogether(copy(product.serving.supply))}</dd>
        </div>
      </dl>
      <AddToCart wide />
      {product.credit ? <p className={styles.small}>{copy(product.credit)}</p> : null}
    </InkChapter>
  );
}

/**
 * The real bottle inside a painted scene: the painting, the bottle where the scene leaves room for
 * it, then `front` over the bottle's foot: the painting's lowest band cut to the bottle's shape by
 * the build script (white elsewhere), so a blossom stands in front of the bottle and nothing beside
 * it is painted twice. Both paintings bloom and multiply; the bottle photo does not. The scene is
 * an illustration, captioned as every painting on the page is.
 */
function SceneStand({ scene, bottle }: { scene: InkScene; bottle: ReactNode }) {
  const copy = useCopy();
  const picture = {
    width: scene.width,
    height: scene.height,
    sizes: "(max-width: 959px) 88vw, 560px",
  };
  return (
    <figure
      className={`${styles.buyStand} ${styles.buyScene}`}
      data-picture=""
      data-stand=""
      data-scene=""
      style={
        {
          ["--aspect" as string]: scene.width / scene.height,
          ["--bottle-width" as string]: `${(scene.bottle.width * 100).toFixed(2)}%`,
          ["--bottle-bottom" as string]: `${(scene.bottle.bottom * 100).toFixed(2)}%`,
        } as CSSProperties
      }
    >
      <span className={styles.sceneStage}>
        <Image
          className={`${base.ink} ${styles.sceneArt}`}
          src={scene.src}
          alt={copy(scene.alt)}
          {...picture}
          data-bloom="waiting"
        />
        {bottle}
        <Image
          className={`${base.ink} ${styles.sceneArt} ${styles.sceneFront}`}
          src={scene.front}
          alt=""
          aria-hidden="true"
          {...picture}
          data-bloom="waiting"
          data-scene-front=""
        />
      </span>
      <figcaption className={`${base.caption} ${styles.caption}`}>
        {copy(CAPTIONS.illustration)}
      </figcaption>
    </figure>
  );
}
