"use client";

import Image from "next/image";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ArrowRight, ArrowUpRight } from "lucide-react";
import { useEffect, useRef } from "react";
import { useCopy } from "@/i18n/use-copy";
import { formulas, iris, liu, opening, pathStops } from "./science-content";
import type { OpeningProps } from "./science-page";
import styles from "./look-path.module.css";

// Look B, "Life's work": Dr. Liu's career as a path you scroll sideways (Mo liked the function of
// Timeline's horizontal history, Design Vault #016, "could look better"). A gold line fills as you
// go; each stop lights when it reaches the middle of the screen and carries its source. The path
// ends on the formulas he made with Dr. Iris Wang (words only). Phones and reduced motion get the
// same stops as a vertical list.
export function LookPath({ onStory }: OpeningProps) {
  const copy = useCopy();
  const root = useRef<HTMLElement>(null);

  useEffect(() => {
    const element = root.current;
    if (!element) return;
    gsap.registerPlugin(ScrollTrigger);
    const media = gsap.matchMedia();
    media.add("(min-width: 901px) and (prefers-reduced-motion: no-preference)", () => {
      const journey = element.querySelector<HTMLElement>("[data-journey]");
      const track = element.querySelector<HTMLElement>("[data-track]");
      const fill = element.querySelector<HTMLElement>("[data-fill]");
      if (!journey || !track || !fill) return;
      const distance = () => Math.max(0, track.scrollWidth - journey.clientWidth);
      // The fill's end stays at the middle of the screen while the path slides under it.
      const reach = (progress: number) =>
        (progress * distance() + journey.clientWidth / 2) / track.scrollWidth;

      const slide = gsap.to(track, {
        x: () => -distance(),
        ease: "none",
        scrollTrigger: {
          trigger: journey,
          start: "top top",
          end: () => `+=${distance()}`,
          pin: true,
          scrub: 0.8,
          invalidateOnRefresh: true,
          onUpdate: (self) => gsap.set(fill, { scaleX: reach(self.progress) }),
          onRefresh: (self) => gsap.set(fill, { scaleX: reach(self.progress) }),
        },
      });
      element.querySelectorAll<HTMLElement>("[data-stop]").forEach((stop) => {
        ScrollTrigger.create({
          trigger: stop,
          containerAnimation: slide,
          start: "left 55%",
          onEnter: () => (stop.dataset.lit = "true"),
          onLeaveBack: () => delete stop.dataset.lit,
        });
      });
    });
    return () => media.revert();
  }, []);

  return (
    <section id="scientists" ref={root} className={styles.path} data-tone="light">
      <div className={styles.opening}>
        <div className={styles.openingCopy}>
          <p className={styles.eyebrow}>{copy(opening.eyebrow)}</p>
          <h1 className={styles.title}>{copy(opening.title)}</h1>
          <div className={styles.person}>
            <p className={styles.name}>{copy(liu.name)}</p>
            <p className={styles.role}>{copy(liu.role)}</p>
          </div>
          <p className={styles.statement}>{copy(liu.headline)}</p>
          <p className={styles.body}>{copy(liu.intro)}</p>
          <button type="button" className={styles.storyButton} onClick={onStory}>
            {copy(liu.button)} <ArrowRight size={20} />
          </button>
        </div>
        <figure className={styles.arch}>
          <Image
            src={liu.photo.src}
            alt={copy(liu.name)}
            fill
            priority
            sizes="(max-width: 900px) 70vw, 420px"
          />
        </figure>
      </div>

      <div className={styles.journey} data-journey>
        <div className={styles.track} data-track>
          <div className={styles.line} aria-hidden="true">
            <div className={styles.fill} data-fill />
          </div>
          <div className={styles.lead}>
            <div className={styles.above}>
              <p className={styles.eyebrow}>{copy("His path")}</p>
              <h2 className={styles.leadTitle}>{copy("A life in cell science.")}</h2>
            </div>
            <p className={`${styles.below} ${styles.hint}`}>
              {copy("Scroll to follow it")} <ArrowRight size={18} />
            </p>
          </div>
          {pathStops.map((stop) => (
            <article key={stop.mark} className={styles.stop} data-stop>
              <p className={`${styles.above} ${styles.mark}`}>{copy(stop.mark)}</p>
              <span className={styles.dot} aria-hidden="true" />
              <div className={styles.below}>
                <h3 className={styles.stopTitle}>{copy(stop.title)}</h3>
                <p className={styles.stopText}>{copy(stop.text)}</p>
                {stop.url && (
                  <a href={stop.url} target="_blank" rel="noreferrer" className={styles.source}>
                    {copy(stop.link)} <ArrowUpRight size={16} />
                  </a>
                )}
              </div>
            </article>
          ))}
          <div className={styles.together} data-stop>
            <span className={styles.dot} aria-hidden="true" />
            <div className={`${styles.below} ${styles.iris}`}>
              <p className={styles.eyebrow}>{copy(iris.role)}</p>
              <h3 className={styles.irisName}>{copy(iris.name)}</h3>
              <p className={styles.stopText}>{copy(iris.text)}</p>
            </div>
            <div className={`${styles.above} ${styles.formulas}`}>
              {formulas.map((formula) => (
                <figure key={formula.name} className={styles.formula}>
                  <div className={styles.bottle}>
                    <Image
                      src={formula.image}
                      alt={copy("{name} bottle", { name: formula.name })}
                      fill
                      sizes="(max-width: 900px) 40vw, 200px"
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
        </div>
      </div>
    </section>
  );
}
