"use client";

import Image from "next/image";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ArrowDown, ArrowUpRight } from "lucide-react";
import { useEffect, useRef } from "react";
import { useCopy } from "@/i18n/use-copy";
import { articles, images, intro, type ScienceDesignProps } from "./science-data";
import styles from "./science-kitchen.module.css";
import { useReducedMotion } from "./use-reduced-motion";

// Kitchen science: each idea is explained by something from the kitchen, and the picture changes as
// you scroll. The bulb lights up, a cut apple browns while its lemon-juiced twin stays fresh, and a
// tree's rings grow outward. The CSS default is the finished picture (used for reduced motion).
const analogies = [
  "Cells need power, like a bulb. Mitochondria help make it.",
  "Air browns a cut apple. Lemon juice slows it down. Cells have defenses, too.",
  "A tree adds a ring each year. Cells change with time, too.",
];

function EnergyStage() {
  return (
    <div className={`${styles.stage} ${styles.energy}`} data-stage aria-hidden="true">
      <span className={styles.room} data-room />
      <div className={styles.bulb}>
        <span className={styles.glow} data-glow />
        <Image {...images.bulbOff} alt="" sizes="(max-width: 899px) 40vw, 18vw" />
        <Image {...images.bulbOn} alt="" sizes="(max-width: 899px) 40vw, 18vw" data-on />
      </div>
    </div>
  );
}

function BalanceStage() {
  const copy = useCopy();
  return (
    <div className={`${styles.stage} ${styles.balance}`} data-stage aria-hidden="true">
      <figure className={styles.apple}>
        <span className={styles.shadow} />
        <Image {...images.appleFresh} alt="" sizes="(max-width: 899px) 42vw, 22vw" />
        <Image
          {...images.appleBrown}
          alt=""
          sizes="(max-width: 899px) 42vw, 22vw"
          className={styles.brown}
          data-brown
        />
        <figcaption>{copy("Air only")}</figcaption>
      </figure>
      <figure className={`${styles.apple} ${styles.protected}`}>
        <span className={styles.shadow} />
        <Image {...images.appleFresh} alt="" sizes="(max-width: 899px) 42vw, 22vw" />
        <figcaption>{copy("With lemon juice")}</figcaption>
      </figure>
      <Image
        {...images.lemon}
        alt=""
        sizes="(max-width: 899px) 26vw, 13vw"
        className={styles.lemon}
        data-lemon
      />
    </div>
  );
}

function AgingStage() {
  return (
    <div className={`${styles.stage} ${styles.aging}`} data-stage aria-hidden="true">
      <div className={styles.slice} data-wood>
        <span className={styles.shadow} />
        <Image
          {...images.wood}
          alt=""
          sizes="(max-width: 899px) 70vw, 32vw"
          className={styles.ghost}
        />
        <Image
          {...images.wood}
          alt=""
          sizes="(max-width: 899px) 70vw, 32vw"
          className={styles.rings}
        />
      </div>
    </div>
  );
}

const stages = [EnergyStage, BalanceStage, AgingStage];

export function ScienceKitchen({ onOpenArticle }: ScienceDesignProps) {
  const copy = useCopy();
  const reducedMotion = useReducedMotion();
  const root = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const element = root.current;
    if (!element || reducedMotion) return;
    gsap.registerPlugin(ScrollTrigger);
    const context = gsap.context(() => {
      const scrub = (id: string) => ({
        trigger: `[data-row="${id}"] [data-stage]`,
        start: "top 85%",
        end: "center 45%",
        scrub: 0.7,
      });
      // The light comes on: the warm bulb fades in, its glow blooms, and the dark room warms.
      gsap
        .timeline({ scrollTrigger: scrub("energy") })
        .fromTo("[data-on]", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.6, ease: "power2.in" })
        .fromTo(
          "[data-glow]",
          { autoAlpha: 0, scale: 0.4 },
          { autoAlpha: 1, scale: 1, duration: 0.8, ease: "power2.out" },
          0.25,
        )
        .fromTo("[data-room]", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.75 }, 0.3);
      // The lemon arrives first; then the unprotected apple browns from its edges inward.
      gsap
        .timeline({ scrollTrigger: scrub("balance") })
        .fromTo(
          "[data-lemon]",
          { xPercent: 70, yPercent: -30, rotation: 38, autoAlpha: 0 },
          {
            xPercent: 0,
            yPercent: 0,
            rotation: 0,
            autoAlpha: 1,
            duration: 0.3,
            ease: "power3.out",
          },
        )
        .fromTo(
          "[data-brown]",
          { "--edge": 100 },
          { "--edge": -25, duration: 1, ease: "none" },
          0.15,
        );
      // Rings grow outward from the heart of the tree.
      gsap
        .timeline({ scrollTrigger: scrub("aging") })
        .fromTo(
          "[data-wood]",
          { "--ring": 0 },
          { "--ring": 104, duration: 1, ease: "power1.inOut" },
        );
    }, element);
    // Images higher on the page can shift these rows as they load; re-measure once they settle.
    const refresh = () => ScrollTrigger.refresh();
    window.addEventListener("load", refresh);
    const settle = window.setTimeout(refresh, 1500);
    return () => {
      window.removeEventListener("load", refresh);
      window.clearTimeout(settle);
      context.revert();
    };
  }, [reducedMotion]);

  return (
    <div ref={root} className={styles.kitchen}>
      <header className={styles.head}>
        <h2 id="science-title" className={styles.heading}>
          {copy(intro.title)}
        </h2>
        <p>{copy(intro.text)}</p>
      </header>

      <ol className={styles.rows}>
        {articles.map((article, index) => {
          const Stage = stages[index];
          return (
            <li key={article.id} className={styles.row} data-row={article.id}>
              <Stage />
              <div className={styles.text}>
                <h3 className={styles.title}>{copy(article.title)}</h3>
                <p className={styles.preview}>{copy(article.preview)}</p>
                <p className={styles.analogy}>{copy(analogies[index])}</p>
                <button type="button" className={styles.read} onClick={() => onOpenArticle(index)}>
                  {copy("Read a quick explainer")} <ArrowUpRight size={19} aria-hidden="true" />
                </button>
              </div>
            </li>
          );
        })}
      </ol>

      <div className={styles.foot}>
        <a href="#research" className={styles.explore}>
          {copy(intro.button)} <ArrowDown size={19} aria-hidden="true" />
        </a>
      </div>
    </div>
  );
}
