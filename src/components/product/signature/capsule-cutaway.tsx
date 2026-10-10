"use client";

import { useEffect, useRef, useState, type CSSProperties } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "@/components/home/use-reduced-motion";
import { useCopy } from "@/i18n/use-copy";
import type { ProductPage } from "../product-types";
import { WORDS } from "../template-chapters-kit";
import { cutawayScript, type CutawayScene } from "./capsule-cutaway-scene";
import styles from "./capsule-cutaway.module.css";

// NuriCell's signature moment, the cutaway (see capsule-cutaway-scene.ts): the capsule opens on a
// dark stage, its fill shown as one layer per ingredient in proportion to the serving, and each
// layer is met on its own with its amount set large. Draft lines; the approved ones are the
// product's own (credit, serving).

/** Layer colours only tell the ingredients apart. ALA really is pale yellow; the rest are white. */
const COLOURS: Record<string, string> = {
  alcar: "#f4eee3",
  creatine: "#d9e3f2",
  ala: "#f0d77a",
  choline: "#d6e48a",
};
const FALLBACK = ["#f4eee3", "#d9e3f2", "#f0d77a", "#d6e48a", "#f3c9a0", "#c9dccb"];

export function colourFor(key: string, index: number) {
  return COLOURS[key] ?? FALLBACK[index % FALLBACK.length];
}

function capitalise(word: string) {
  return word.charAt(0).toUpperCase() + word.slice(1);
}

export function CapsuleCutaway({ product }: { product: ProductPage }) {
  const copy = useCopy();
  const reduced = useReducedMotion();
  const root = useRef<HTMLElement>(null);
  const stage = useRef<HTMLDivElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  const labels = useRef<(HTMLDivElement | null)[]>([]);
  const [ready, setReady] = useState(false);
  const count = product.ingredients.length;
  const total = product.ingredients.reduce((sum, item) => sum + item.amount, 0);
  // How the ingredients work together, as pairs of ingredient positions (unknown keys dropped).
  const synergy = product.synergy;
  const pairs = (synergy?.links ?? [])
    .map((link) => ({
      link,
      from: product.ingredients.findIndex((item) => item.key === link.from),
      to: product.ingredients.findIndex((item) => item.key === link.to),
    }))
    .filter((pair) => pair.from >= 0 && pair.to >= 0 && pair.from !== pair.to);
  const pairCount = pairs.length;
  const script = cutawayScript(count, pairCount);
  const nameOf = (index: number) => copy(product.ingredients[index].name);

  useEffect(() => {
    if (reduced) return;
    let cancelled = false;
    let scene: CutawayScene | null = null;
    let context: gsap.Context | null = null;
    const { length, focusStart, FOCUS, together, trio, ring, linkStart, LINK } = cutawayScript(
      count,
      pairCount,
    );
    const linkIndexes = pairs.map(({ from, to }) => ({ from, to }));

    Promise.all([import("three"), import("./capsule-cutaway-scene")])
      .then(([three, { createCutawayScene }]) => {
        const section = root.current;
        if (cancelled || !section || !stage.current || !canvas.current) return;
        scene = createCutawayScene(
          three,
          canvas.current,
          stage.current,
          product.ingredients.map((item, index) => ({
            key: item.key,
            amount: item.amount,
            colour: colourFor(item.key, index),
          })),
          labels.current,
          linkIndexes,
        );
        setReady(true);
        const { state } = scene;
        const beat = (name: string) => section.querySelector<HTMLElement>(`[data-beat="${name}"]`);

        gsap.registerPlugin(ScrollTrigger);
        context = gsap.context(() => {
          gsap.set(section.querySelectorAll("[data-beat]"), { opacity: 0, y: 30 });
          const timeline = gsap.timeline({
            defaults: { ease: "none" },
            scrollTrigger: {
              trigger: section,
              start: "top top",
              end: "bottom bottom",
              scrub: 0.7,
              onUpdate: (self) => {
                state.time = self.progress * length;
              },
            },
          });
          const show = (name: string, at: number, stay: number | null) => {
            const element = beat(name);
            if (!element) return;
            timeline.to(element, { opacity: 1, y: 0, duration: 0.26, ease: "power2.out" }, at);
            if (stay !== null) {
              timeline.to(
                element,
                { opacity: 0, y: -30, duration: 0.22, ease: "power1.in" },
                at + stay,
              );
            }
          };
          show("intro", 0.08, 1.2);
          show("open", 1.6, 0.95);
          product.ingredients.forEach((_, index) => {
            show(`focus-${index}`, focusStart + index * FOCUS + 0.12, FOCUS - 0.34);
          });
          if (linkIndexes.length) {
            show("synergy", ring[0] + 0.05, linkStart - ring[0] - 0.12);
            linkIndexes.forEach((_, index) => {
              show(`link-${index}`, linkStart + index * LINK + 0.1, LINK - 0.3);
            });
          }
          show("together", together + 0.05, 0.85);
          show("close", trio[0], null);
          timeline.to({}, { duration: 0.01 }, length - 0.01);
        }, section);
        ScrollTrigger.refresh();
      })
      .catch(() => setReady(false));

    return () => {
      cancelled = true;
      context?.revert();
      scene?.dispose();
    };
    // The pairs come from the product's data, which never changes while the page is open.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [reduced, product.ingredients, count, pairCount]);

  const intro = copy("Inside every capsule, {count} ingredients.", {
    count: copy(WORDS[count] ?? String(count)),
  });
  const proportion = copy(
    "Each layer is as long as its share of one serving. The colours only tell them apart.",
  );

  if (reduced) {
    // Still: the same idea as a bar, one band per ingredient, in proportion.
    return (
      <section
        className={`${styles.cutaway} ${styles.still}`}
        aria-label={copy("Inside the capsule")}
      >
        <div className={styles.stillInner}>
          <p className={styles.stillIntro}>{intro}</p>
          <div className={styles.bar} aria-hidden="true">
            {product.ingredients.map((item, index) => (
              <span
                key={item.key}
                style={
                  {
                    "--share": item.amount / total,
                    "--colour": colourFor(item.key, index),
                  } as CSSProperties
                }
              />
            ))}
          </div>
          <ul className={styles.legend}>
            {product.ingredients.map((item, index) => (
              <li
                key={item.key}
                style={{ "--colour": colourFor(item.key, index) } as CSSProperties}
              >
                <span className={styles.figure}>
                  {item.amount}
                  <small>{item.unit}</small>
                </span>
                <span className={styles.legendName}>{copy(item.name)}</span>
              </li>
            ))}
          </ul>
          <p className={styles.note}>{proportion}</p>
          {synergy && pairCount > 0 && (
            <div className={styles.stillSynergy}>
              <h3 className={styles.stillIntro}>{copy(synergy.title)}</h3>
              <ol className={styles.stillLinks}>
                {pairs.map(({ link, from, to }) => (
                  <li key={`${link.from}-${link.to}`}>
                    <p className={styles.pair}>
                      {nameOf(from)} <span aria-hidden="true">+</span> {nameOf(to)}
                    </p>
                    <h4 className={styles.linkTitle}>{copy(link.title)}</h4>
                    <p className={styles.linkLine}>{copy(link.line)}</p>
                    {link.evidence && <p className={styles.evidence}>{copy(link.evidence)}</p>}
                  </li>
                ))}
              </ol>
              <p className={styles.note}>{copy(synergy.note)}</p>
            </div>
          )}
        </div>
      </section>
    );
  }

  return (
    <section
      ref={root}
      className={styles.cutaway}
      data-tone="night"
      style={{ height: `${(script.length + 1) * 100}svh` }}
      data-ready={ready ? "true" : undefined}
      aria-label={copy("Inside the capsule")}
    >
      <div ref={stage} className={styles.stage}>
        <canvas ref={canvas} className={styles.canvas} aria-hidden="true" />
        <div className={styles.labels} aria-hidden="true">
          {product.ingredients.map((item, index) => (
            <div
              key={item.key}
              ref={(element) => {
                labels.current[index] = element;
              }}
              className={styles.label}
              data-label
              style={{ "--colour": colourFor(item.key, index) } as CSSProperties}
            >
              <span className={styles.leader} />
              <span className={styles.labelText} data-label-text>
                <b>
                  {item.amount} {item.unit}
                </b>
                {copy(item.name)}
              </span>
            </div>
          ))}
        </div>

        <div data-beat="intro" className={`${styles.beat} ${styles.statement}`}>
          <p>{intro}</p>
        </div>
        <div data-beat="open" className={`${styles.beat} ${styles.aside}`}>
          <p>{proportion}</p>
        </div>
        {product.ingredients.map((item, index) => (
          <div
            key={item.key}
            data-beat={`focus-${index}`}
            className={`${styles.beat} ${styles.focus}`}
            style={{ "--colour": colourFor(item.key, index) } as CSSProperties}
          >
            <p className={styles.count}>
              <span className={styles.swatch} aria-hidden="true" />
              {index + 1} / {count}
            </p>
            <p className={styles.figure}>
              {item.amount}
              <small>{item.unit}</small>
            </p>
            <h3 className={styles.name}>{copy(item.name)}</h3>
            {item.role && <p className={styles.role}>{copy(item.role)}</p>}
          </div>
        ))}
        {synergy && pairCount > 0 && (
          <>
            <div data-beat="synergy" className={`${styles.beat} ${styles.statement}`}>
              <p>{copy(synergy.title)}</p>
            </div>
            {pairs.map(({ link, from, to }, index) => (
              <div
                key={`${link.from}-${link.to}`}
                data-beat={`link-${index}`}
                className={`${styles.beat} ${styles.link}`}
              >
                <p className={styles.count}>
                  {copy(synergy.title)} · {index + 1} / {pairCount}
                </p>
                <p className={styles.pair}>
                  {nameOf(from)} <span aria-hidden="true">+</span> {nameOf(to)}
                </p>
                <h3 className={styles.linkTitle}>{copy(link.title)}</h3>
                <p className={styles.linkLine}>{copy(link.line)}</p>
                {link.evidence && <p className={styles.evidence}>{copy(link.evidence)}</p>}
                <p className={styles.fine}>{copy(synergy.note)}</p>
              </div>
            ))}
          </>
        )}
        <div data-beat="together" className={`${styles.beat} ${styles.statement}`}>
          <p>
            {copy("{count} ingredients.", {
              count: copy(capitalise(WORDS[count] ?? String(count))),
            })}{" "}
            {copy("One formula.")}
          </p>
          {product.credit && <p className={styles.credit}>{copy(product.credit)}</p>}
        </div>
        <div data-beat="close" className={`${styles.beat} ${styles.statement} ${styles.closing}`}>
          <p>{copy(product.serving.use)}</p>
        </div>
      </div>
    </section>
  );
}
