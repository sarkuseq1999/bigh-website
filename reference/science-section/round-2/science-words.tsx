"use client";

import Image from "next/image";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ArrowDown } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useCopy } from "@/i18n/use-copy";
import { articles, images, intro, type ScienceDesignProps } from "./science-data";
import styles from "./science-words.module.css";
import { useReducedMotion } from "./use-reduced-motion";

// Picture words (after Timeline's "supplement [pill] that changes how cells age" headline): each
// idea is one large centered sentence with the everyday thing that explains it set right into the
// words. Scrolling plays the idea: the bulb switches on, the apple browns, the tree slice turns.
// Pointing at an object shows a close-up that follows the pointer.
type Thing = "bulb" | "apple" | "lemon" | "wood";
type Part = string | Thing;

const things: readonly string[] = ["bulb", "apple", "lemon", "wood"];
const sentences: Part[][][] = [
  [["Your cells run on tiny", "bulb", "power plants."]],
  [
    ["A cut apple", "apple", "browns in the air."],
    ["A squeeze of lemon", "lemon", "slows it down."],
  ],
  [["Like the rings of a tree,", "wood", "your cells change with time."]],
];

const closeUps: Record<Thing, string> = {
  bulb: images.filament.src,
  apple: images.apple.src,
  lemon: images.lemon.src,
  wood: images.rings.src,
};

const pictures: Record<Thing, { src: string; width: number; height: number }[]> = {
  bulb: [images.bulbOff, images.bulbOn],
  apple: [images.appleFresh, images.appleBrown],
  lemon: [images.lemonHalf],
  wood: [images.wood],
};

function Everyday({ thing }: { thing: Thing }) {
  return (
    <span className={styles.object} data-object={thing} aria-hidden="true">
      <span className={styles.lift} data-lift>
        {pictures[thing].map((image, index) => (
          <Image
            key={image.src}
            {...image}
            alt=""
            sizes="160px"
            data-after={index === 1 ? "" : undefined}
          />
        ))}
      </span>
    </span>
  );
}

export function ScienceWords({ onOpenArticle }: ScienceDesignProps) {
  const copy = useCopy();
  const reducedMotion = useReducedMotion();
  const root = useRef<HTMLDivElement>(null);
  const [closeUp, setCloseUp] = useState<string | null>(null);

  // Each sentence plays its idea as it rises into the middle of the screen.
  useEffect(() => {
    const element = root.current;
    if (!element || reducedMotion) return;
    gsap.registerPlugin(ScrollTrigger);
    const context = gsap.context(() => {
      gsap.utils.toArray<HTMLElement>("[data-sentence]").forEach((sentence) => {
        const timeline = gsap.timeline({
          defaults: { ease: "none" },
          scrollTrigger: { trigger: sentence, start: "top 88%", end: "center 42%", scrub: 0.6 },
        });
        timeline.from(sentence.querySelectorAll("[data-lift]"), {
          scale: 0.5,
          rotation: -16,
          yPercent: 30,
          duration: 0.45,
          ease: "power3.out",
          stagger: 0.12,
        });
        const after = sentence.querySelectorAll("[data-after]");
        if (after.length) {
          timeline.fromTo(after, { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.45);
        }
        const wood = sentence.querySelector('[data-object="wood"] [data-lift]');
        if (wood) timeline.fromTo(wood, { rotation: -70 }, { rotation: 0, duration: 0.85 }, 0);
      });
    }, element);
    const refresh = () => ScrollTrigger.refresh();
    window.addEventListener("load", refresh);
    return () => {
      window.removeEventListener("load", refresh);
      context.revert();
    };
  }, [reducedMotion]);

  // Pointing at an object shows a close-up print that follows the pointer.
  useEffect(() => {
    const element = root.current;
    if (!element || reducedMotion) return;
    const float = element.querySelector<HTMLElement>("[data-float]");
    if (!float) return;
    const moveX = gsap.quickTo(float, "x", { duration: 0.5, ease: "power3.out" });
    const moveY = gsap.quickTo(float, "y", { duration: 0.5, ease: "power3.out" });
    function over(event: PointerEvent) {
      const thing = (event.target as HTMLElement).closest<HTMLElement>("[data-object]");
      if (!thing || event.pointerType === "touch") return;
      setCloseUp(closeUps[thing.dataset.object as Thing]);
    }
    function out(event: PointerEvent) {
      const thing = (event.target as HTMLElement).closest("[data-object]");
      if (thing && !thing.contains(event.relatedTarget as Node)) setCloseUp(null);
    }
    // The print sits above and to the right of the pointer, clear of the line being read.
    function move(event: PointerEvent) {
      moveX(event.clientX + 24);
      moveY(Math.max(12, event.clientY - 320));
    }
    element.addEventListener("pointerover", over);
    element.addEventListener("pointerout", out);
    window.addEventListener("pointermove", move, { passive: true });
    return () => {
      element.removeEventListener("pointerover", over);
      element.removeEventListener("pointerout", out);
      window.removeEventListener("pointermove", move);
    };
  }, [reducedMotion]);

  return (
    <div ref={root} className={styles.words} data-reduced={reducedMotion}>
      <header className={styles.head}>
        <h2 id="science-title" className={styles.heading}>
          {copy(intro.title)}
        </h2>
        <p>{copy(intro.text)}</p>
      </header>

      <ol className={styles.list}>
        {sentences.map((sentence, index) => {
          const article = articles[index];
          return (
            <li key={article.id} className={styles.item}>
              <p className={styles.sentence} data-sentence>
                {sentence.map((line) => (
                  <span key={line.join()} className={styles.line}>
                    {line.map((part) =>
                      things.includes(part) ? (
                        <Everyday key={part} thing={part as Thing} />
                      ) : (
                        <span key={part}>{copy(part)}</span>
                      ),
                    )}
                  </span>
                ))}
              </p>
              <div className={styles.details}>
                <h3 className={styles.title}>
                  <button type="button" onClick={() => onOpenArticle(index)}>
                    <span>{copy(article.title)}</span>
                  </button>
                </h3>
                <p className={styles.preview}>{copy(article.preview)}</p>
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

      <div className={styles.float} data-float data-visible={closeUp !== null} aria-hidden="true">
        {closeUp && <Image src={closeUp} width={900} height={900} alt="" sizes="300px" />}
      </div>
    </div>
  );
}
