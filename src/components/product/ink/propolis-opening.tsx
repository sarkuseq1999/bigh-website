"use client";

import Image from "next/image";
import type { MouseEvent } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { AddToCart } from "../add-to-cart";
import type { InkProduct } from "../product-types";
import { anchorId } from "../template-chapters-model";
import { keepTogether } from "./ink-chapter";
import styles from "./propolis.module.css";

const CHAPTERS = [
  ["why", "Why green propolis"],
  ["inside", "What’s inside"],
  ["research", "The research"],
  ["daily", "How to take it"],
] as const;

/** A keyboard focus or browser auto-scroll can move the page ahead of the shared smooth-scroll
 * clock. Use the actual document position for these local links, then hand focus to the heading. */
function followChapter(event: MouseEvent<HTMLAnchorElement>) {
  if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0)
    return;
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const touch = window.matchMedia("(pointer: coarse)").matches;
  // The shared scroll controller handles this opt-in link on a mouse/keyboard device.
  // Touch and reduced motion use the browser because the controller is disabled there.
  if (!reduced && !touch) return;
  const hash = event.currentTarget.hash;
  const section = document.getElementById(hash.slice(1));
  const heading = section?.querySelector<HTMLElement>("h2");
  if (!heading) return;
  event.preventDefault();
  event.stopPropagation();
  const top = heading.getBoundingClientRect().top + window.scrollY - 120;
  heading.tabIndex = -1;
  heading.dataset.inkJumpTarget = "";
  heading.focus({ preventScroll: true });
  window.history.pushState(null, "", hash);
  window.scrollTo({
    top,
    behavior: reduced ? "instant" : "smooth",
  });
}

/** Mo's preferred composition: Green / the real bottle / Bee Propolis.
 * Phones put the same name arrangement above the bottle so every word stays readable. */
export function PropolisOpening({ product }: { product: InkProduct }) {
  const copy = useCopy();
  return (
    <section
      id={anchorId("overview")}
      className={styles.hero}
      data-chapter="overview"
      aria-labelledby="product-name"
    >
      <div className={base.wrap}>
        <h1 id="product-name" className={styles.name} lang="en" aria-label={product.name}>
          <span className={styles.nameLeft} data-name-left aria-hidden="true">
            Green
          </span>
          <span className={styles.bottleStand} aria-hidden="true">
            <Image
              className={styles.heroBottle}
              src={product.bottle.src}
              alt=""
              width={product.bottle.width}
              height={product.bottle.height}
              sizes="(max-width: 959px) 76vw, (max-width: 1468px) 32vw, 470px"
              loading="eager"
              fetchPriority="high"
            />
          </span>
          <span className={styles.nameRight} data-name-right aria-hidden="true">
            <span>Bee</span>
            <span>Propolis</span>
          </span>
        </h1>
        <div className={styles.heroDetails}>
          <div className={styles.description}>
            <p className={styles.lead}>
              {product.headlineLines.map((line, i) => (
                <span key={line}>
                  {i > 0 ? " " : null}
                  {copy(line)}
                </span>
              ))}
            </p>
            <p className={styles.purpose}>{copy(product.purpose)}</p>
          </div>
          <div className={styles.purchase}>
            <ul className={styles.provenance}>
              {product.highlights.map((item) => (
                <li key={item}>{copy(item)}</li>
              ))}
            </ul>
            <p className={styles.supply}>{keepTogether(copy(product.serving.supply))}</p>
            <AddToCart wide />
            <p className={styles.promise}>
              {copy("45 days to decide.")} {copy("Not right for you? Send it back for a refund.")}
            </p>
          </div>
        </div>
        <nav className={styles.chapterNav} aria-label={product.name}>
          {CHAPTERS.map(([id, label], index) => (
            <a key={id} href={`#${anchorId(id)}`} data-scroll-heading="" onClick={followChapter}>
              <span className={styles.chapterNumber} aria-hidden="true">
                {String(index + 1).padStart(2, "0")}
              </span>
              <span>{copy(label)}</span>
              <span className={styles.navArrow} aria-hidden="true">
                ↓
              </span>
            </a>
          ))}
        </nav>
      </div>
    </section>
  );
}
