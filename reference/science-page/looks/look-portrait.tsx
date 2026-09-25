"use client";

import Image from "next/image";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ArrowDown, ArrowRight, ArrowUpRight } from "lucide-react";
import { useEffect, useRef } from "react";
import { useReducedMotion } from "@/components/home/use-reduced-motion";
import { useCopy } from "@/i18n/use-copy";
import { formulas, iris, liu, liuNumbers, opening } from "./science-content";
import type { OpeningProps } from "./science-page";
import styles from "./look-portrait.module.css";

// Look A, "Portrait": Timeline's calm (Design Vault #005, #014, #015). One centered sentence, then
// Dr. Liu's photograph in a big rounded frame that comes into focus as it scrolls into place, his
// record as three large numbers, and the formulas he made with Dr. Iris Wang (words only).
export function LookPortrait({ onStory }: OpeningProps) {
  const copy = useCopy();
  const root = useRef<HTMLElement>(null);
  const reduced = useReducedMotion();

  useEffect(() => {
    const element = root.current;
    if (!element || reduced) return;
    gsap.registerPlugin(ScrollTrigger);
    const context = gsap.context(() => {
      // The focus pull: the photograph comes into focus as it arrives (at once if it is already in
      // view), so his face is never left blurred while someone reads.
      gsap.fromTo(
        "[data-photo]",
        { filter: "blur(16px) saturate(0.7)", scale: 1.1 },
        {
          filter: "blur(0px) saturate(1)",
          scale: 1,
          duration: 1.8,
          ease: "power2.out",
          scrollTrigger: { trigger: "[data-frame]", start: "top 88%", once: true },
        },
      );
      gsap.from("[data-feature-copy] > *", {
        y: 26,
        opacity: 0,
        duration: 0.9,
        ease: "power2.out",
        stagger: 0.08,
        scrollTrigger: { trigger: "[data-feature-copy]", start: "top 78%" },
      });
      // 280 counts up; the years stay as they are.
      element.querySelectorAll<HTMLElement>("[data-count]").forEach((node) => {
        const target = Number(node.dataset.count);
        const state = { value: 0 };
        gsap.to(state, {
          value: target,
          duration: 1.6,
          ease: "power2.out",
          scrollTrigger: { trigger: node, start: "top 85%" },
          onUpdate: () => {
            node.textContent = String(Math.round(state.value));
          },
        });
      });
      gsap.from("[data-number]", {
        y: 30,
        opacity: 0,
        duration: 0.9,
        ease: "power2.out",
        stagger: 0.12,
        scrollTrigger: { trigger: "[data-numbers]", start: "top 80%" },
      });
      gsap.from("[data-bottle]", {
        y: 60,
        opacity: 0,
        duration: 1.1,
        ease: "power3.out",
        stagger: 0.15,
        scrollTrigger: { trigger: "[data-together]", start: "top 72%" },
      });
    }, element);
    return () => context.revert();
  }, [reduced]);

  return (
    <section id="scientists" ref={root} className={styles.portrait} data-tone="light">
      {/* Like Timeline's About page (#014): the sentence, then the picture rising into view. */}
      <div className={styles.opening}>
        <p className={styles.eyebrow}>{copy(opening.eyebrow)}</p>
        <h1 className={styles.title}>{copy(opening.title)}</h1>
      </div>

      <figure id="dr-liu" className={styles.frame} data-frame>
        <Image
          src={liu.photo.src}
          alt={copy(liu.name)}
          fill
          priority
          sizes="(max-width: 900px) 80vw, 460px"
          className={styles.photo}
          data-photo
        />
        <a href="#dr-liu-intro" className={styles.cue} aria-label={copy(liu.name)}>
          <ArrowDown size={20} />
        </a>
      </figure>

      <div id="dr-liu-intro" className={styles.featureCopy} data-feature-copy>
        <p className={styles.eyebrow}>{copy(liu.role)}</p>
        <h2 className={styles.name}>{copy(liu.name)}</h2>
        <p className={styles.statement}>{copy(liu.headline)}</p>
        <p className={styles.body}>{copy(liu.intro)}</p>
        <p className={styles.body}>{copy(liu.purpose)}</p>
        <button type="button" className={styles.storyButton} onClick={onStory}>
          {copy(liu.button)} <ArrowRight size={20} />
        </button>
      </div>

      <div className={styles.numbers} data-numbers>
        {liuNumbers.map((item) => (
          <div key={item.value} className={styles.number} data-number>
            <p className={styles.value}>
              <span data-count={item.suffix ? item.value : undefined}>{item.value}</span>
              {item.suffix}
            </p>
            <p className={styles.label}>{copy(item.label)}</p>
            <a href={item.url} target="_blank" rel="noreferrer" className={styles.source}>
              {copy("Source")} <ArrowUpRight size={16} />
            </a>
          </div>
        ))}
      </div>
      <p className={styles.tribute}>
        {copy(liu.highlights[2].text)}{" "}
        <a href={liu.highlights[2].url} target="_blank" rel="noreferrer">
          {copy(liu.highlights[2].link)} <ArrowUpRight size={16} />
        </a>
      </p>

      <div className={styles.together} data-together>
        <div className={styles.iris}>
          <p className={styles.eyebrow}>{copy(iris.role)}</p>
          <h2 className={styles.irisName}>{copy(iris.name)}</h2>
          <p className={styles.body}>{copy(iris.text)}</p>
        </div>
        <div className={styles.formulas}>
          {formulas.map((formula) => (
            <figure key={formula.name} className={styles.formula} data-bottle>
              <div className={styles.bottle}>
                <Image
                  src={formula.image}
                  alt={copy("{name} bottle", { name: formula.name })}
                  fill
                  sizes="(max-width: 900px) 40vw, 220px"
                />
              </div>
              <figcaption>
                <strong>{formula.name}</strong>
                <span>{copy(formula.credit)}</span>
              </figcaption>
            </figure>
          ))}
        </div>
      </div>
    </section>
  );
}
