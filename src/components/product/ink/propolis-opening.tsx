"use client";

import Image from "next/image";
import type { MouseEvent } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { AddToCart } from "../add-to-cart";
import type { InkProduct } from "../product-types";
import { anchorId } from "../template-chapters-model";
import { keepTogether } from "./ink-chapter";
import card from "./product-ink.module.css";
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
 * Mobile uses Mo's selected Editorial pair: the whole name left, the bottle right. */
export function PropolisOpening({ product }: { product: InkProduct }) {
  const copy = useCopy();
  return (
    <section
      id={anchorId("overview")}
      className={styles.hero}
      data-chapter="overview"
      aria-labelledby="product-name"
    >
      <div className={`${base.wrap} ${styles.heroWrap}`}>
        <h1 id="product-name" className={styles.name} lang="en" aria-label={product.name}>
          <span className={styles.mobileName} data-mobile-name aria-hidden="true">
            <span>Green</span>
            <span>Bee</span>
            <span>Propolis</span>
          </span>
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
              sizes="(max-width: 599px) 244px, (max-width: 959px) 360px, (max-width: 1920px) 28vw, 530px"
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
            <div className={`${card.bottleCard} ${styles.bottleCard}`} data-purchase-card="">
              {product.ink.supply ? (
                <Image
                  className={card.bottleCardPicture}
                  src={product.ink.supply.src}
                  alt=""
                  width={product.ink.supply.width}
                  height={product.ink.supply.height}
                  sizes="72px"
                />
              ) : null}
              <p className={card.bottleCardName}>{copy("One bottle")}</p>
              <p className={`${card.bottleCardSupply} ${styles.cardSupply}`}>
                {copy(product.serving.supply)
                  .split(" · ")
                  .map((fact) => (
                    <span key={fact}>{keepTogether(fact)}</span>
                  ))}
              </p>
              <p className={card.bottleCardDaily}>
                {copy("{count} a day", { count: product.serving.capsules })}
              </p>
              <p className={`${card.promise} ${styles.cardPromise}`} data-purchase-promise="">
                <svg
                  viewBox="0 0 20 20"
                  width="15"
                  height="15"
                  aria-hidden="true"
                  focusable="false"
                >
                  <circle
                    cx="10"
                    cy="10"
                    r="8.2"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.6"
                  />
                  <path
                    d="M6.2 10.3l2.5 2.5 5-5.4"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
                {copy("45 days to decide.").replace(/[.。]$/, "")}
              </p>
            </div>
            <AddToCart wide align="center" />
            <p className={card.refund}>{copy("Not right for you? Send it back for a refund.")}</p>
          </div>
          <div className={styles.mobileStory} data-mobile-story>
            <p className={styles.purpose}>{copy(product.purpose)}</p>
            <ul className={styles.provenance}>
              {product.highlights.map((item) => (
                <li key={item}>{copy(item)}</li>
              ))}
            </ul>
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
