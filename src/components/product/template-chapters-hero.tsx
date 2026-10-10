"use client";

import Image from "next/image";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { SplitText } from "gsap/SplitText";
import { Check, ChevronDown } from "lucide-react";
import { useEffect, useId, useRef, useState, type CSSProperties, type RefObject } from "react";
import { useCopy } from "@/i18n/use-copy";
import { AddToCart } from "./add-to-cart";
import type { ProductPage } from "./product-types";
import type { HeroScene } from "./signature/hero-scene";
import { bottles } from "./template-object-bottle";
import { anchorId, wordClass, type Chapter, type ChapterId } from "./template-chapters-kit";
import chapterStyles from "./template-chapters.module.css";
import styles from "./template-chapters-hero.module.css";

// Chapter 1, the overview: "Big name" (Mo picked it on September 28, 2026, from three openings).
// The product's name is set huge across the screen, parted where its words meet, and the real
// bottle in 3D (the approved photo's own label on a turned model) turns in the gap, so it hides
// no letter. On phones the whole name sits above the bottle. Products without a 3D bottle yet
// show their approved photo in the same place.

type Props = {
  product: ProductPage;
  chapter: Chapter;
  chapters: Chapter[];
  reduced: boolean;
  onJump: (id: ChapterId) => void;
};

/** Where the giant name parts for the bottle: at the word break nearest the middle ("Nuri|Cell",
 *  "Green Bee|Propolis"), or in the middle of a single word. */
export function splitName(name: string): [string, string] {
  const middle = name.length / 2;
  const breaks = [...name.matchAll(/ |(?<=[a-z])(?=[A-Z])/g)].map((match) => match.index);
  if (breaks.length === 0) {
    const half = Math.ceil(middle);
    return [name.slice(0, half), name.slice(half)];
  }
  const at = breaks.reduce((best, cut) =>
    Math.abs(cut - middle) < Math.abs(best - middle) ? cut : best,
  );
  return [name.slice(0, at).trim(), name.slice(at).trim()];
}

/** Build and run the 3D stage; `ready` turns true once its first real frame is drawn. */
function useHeroStage(
  product: ProductPage,
  refs: {
    section: RefObject<HTMLElement | null>;
    stage: RefObject<HTMLDivElement | null>;
    canvas: RefObject<HTMLCanvasElement | null>;
  },
  reduced: boolean,
) {
  const model = bottles[product.slug];
  const [status, setStatus] = useState<"loading" | "ready" | "flat">(model ? "loading" : "flat");

  useEffect(() => {
    const section = refs.section.current;
    const stage = refs.stage.current;
    const canvas = refs.canvas.current;
    if (!model || !section || !stage || !canvas) return;
    let cancelled = false;
    let scene: HeroScene | null = null;
    let context: gsap.Context | null = null;

    Promise.all([import("three"), import("./signature/hero-scene")])
      .then(([three, { createHeroScene }]) => {
        if (cancelled) return;
        scene = createHeroScene(three, canvas, stage, model, { still: reduced });
        const { state } = scene;
        if (reduced) state.enter = 1;
        void scene.ready.then(() => {
          if (cancelled) return;
          setStatus("ready");
          if (reduced) return;
          gsap.registerPlugin(ScrollTrigger);
          context = gsap.context(() => {
            gsap.to(state, { enter: 1, duration: 2.6, ease: "power2.out", delay: 0.1 });
            ScrollTrigger.create({
              trigger: section,
              start: "top top",
              end: "bottom top",
              onUpdate: (self) => {
                state.scroll = self.progress;
              },
            });
          }, section);
          // Settle failsafe: a background tab may never play the arrival.
          window.setTimeout(() => {
            if (!cancelled && state.enter < 1) state.enter = 1;
          }, 4000);
        });
      })
      .catch(() => {
        if (!cancelled) setStatus("flat");
      });

    return () => {
      cancelled = true;
      context?.revert();
      scene?.dispose();
    };
  }, [model, reduced, refs.section, refs.stage, refs.canvas]);

  return status;
}

export function HeroChapter({ product, chapter, chapters, reduced, onJump }: Props) {
  const copy = useCopy();
  const root = useRef<HTMLElement>(null);
  const stage = useRef<HTMLDivElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  const giant = useRef<HTMLParagraphElement>(null);
  const titleId = useId();
  const status = useHeroStage(product, { section: root, stage, canvas }, reduced);
  const lines = product.headlineLines.map((line) => copy(line));
  const next = chapters[1];
  const [nameFit, setNameFit] = useState<{ size: number; y: number | null } | null>(null);
  const halves = product.nameHalves ?? splitName(product.name);

  // The two halves and the bottle's gap between them fill the width. Both halves sit in
  // equal columns so the gap stays centred on the bottle; measure once the face is in. On wide
  // screens the name also stands clear of the eyebrow above and the words below, however short
  // the screen or long the translation.
  useEffect(() => {
    const element = giant.current;
    const section = root.current;
    if (!element || !section) return;
    const fit = () => {
      const probes = [...element.querySelectorAll<HTMLElement>("[data-probe]")];
      const widest = Math.max(...probes.map((probe) => probe.getBoundingClientRect().width));
      const gap = parseFloat(getComputedStyle(element).columnGap) || 0;
      const available = element.clientWidth * 0.985 - gap;
      if (!(widest > 0 && available > 0)) return;
      // 100px probes; the name's box is 0.82 of its size tall.
      let size = Math.min((100 * available) / (2 * widest), window.innerHeight * 0.32);
      let y: number | null = null;
      const top = section.querySelector<HTMLElement>("[data-name-top]");
      const foot = section.querySelector<HTMLElement>("[data-name-foot]");
      if (top && foot && getComputedStyle(element).position === "absolute") {
        const floor = foot.offsetTop - 40;
        const ceiling = top.offsetTop + top.offsetHeight + 24;
        size = Math.max(40, Math.min(size, (floor - ceiling) / 0.82));
        y = floor - size * 0.41;
      }
      setNameFit({ size, y });
    };
    void document.fonts.ready.then(fit);
    const observer = new ResizeObserver(fit);
    observer.observe(element);
    observer.observe(section);
    return () => observer.disconnect();
  }, [product.name]);

  // The arrival: words rise behind masks, then the rest. CSS keeps it hidden until this runs
  // (with a failsafe), so nothing flashes first.
  useEffect(() => {
    const element = root.current;
    if (reduced || !element) return;
    gsap.registerPlugin(SplitText, ScrollTrigger);
    let intro: gsap.core.Timeline | undefined;
    let cancelled = false;
    const ctx = gsap.context(() => {}, element);
    void document.fonts.ready.then(() => {
      if (cancelled) return;
      ctx.add(() => {
        const split = SplitText.create(element.querySelectorAll("[data-split]"), {
          type: "words",
          mask: "words",
          wordsClass: wordClass,
          aria: "none",
        });
        intro = gsap
          .timeline({ defaults: { ease: "expo.out" } })
          .from("[data-intro='eyebrow']", { opacity: 0, y: 14, duration: 1.1 }, 0.15)
          .from(split.words, { yPercent: 130, duration: 1.3, stagger: 0.07 }, 0.25)
          .from(
            "[data-intro='rest']",
            { opacity: 0, y: 22, duration: 1.2, stagger: 0.08, ease: "power3.out" },
            0.7,
          );
        const letters = SplitText.create(element.querySelectorAll("[data-giant-half]"), {
          type: "chars",
          mask: "chars",
          aria: "none",
        });
        intro.from(letters.chars, { yPercent: 110, duration: 1.5, stagger: 0.045 }, 0);
        // Scrolling away, the name opens around the bottle.
        gsap
          .timeline({
            defaults: { ease: "none" },
            scrollTrigger: { trigger: element, start: "top top", end: "bottom top", scrub: 0.6 },
          })
          .to("[data-giant-half='a']", { xPercent: -18, opacity: 0.25 }, 0)
          .to("[data-giant-half='b']", { xPercent: 18, opacity: 0.25 }, 0);
      });
      element.dataset.intro = "on";
    });
    const settle = window.setTimeout(() => intro?.progress(1), 3600);
    return () => {
      cancelled = true;
      window.clearTimeout(settle);
      ctx.revert();
      delete element.dataset.intro;
    };
  }, [reduced]);

  const headline = (
    <h1 id={titleId} className={styles.title}>
      <span className={chapterStyles.srOnly}>{`${product.name}: ${lines.join(" ")}`}</span>
      <span aria-hidden="true">
        {lines.map((line, index) => (
          <span key={index} className={styles.titleLine} data-split>
            {line}
          </span>
        ))}
      </span>
    </h1>
  );
  const eyebrow = (
    <p className={styles.eyebrow} data-intro="eyebrow">
      <b>{product.name}</b> · {copy(product.eyebrow)}
    </p>
  );
  const purpose = (
    <p className={styles.purpose} data-intro="rest">
      {copy(product.purpose)}
    </p>
  );
  const highlights = product.highlights.length > 0 && (
    <ul className={styles.highlights} data-intro="rest">
      {product.highlights.map((highlight) => (
        <li key={highlight}>
          <span className={styles.tick} aria-hidden="true">
            <Check size={15} strokeWidth={2.5} />
          </span>
          {copy(highlight)}
        </li>
      ))}
    </ul>
  );
  const cart = (
    <div className={styles.cart} data-intro="rest">
      <AddToCart />
      <p className={styles.supply}>{copy(product.serving.supply)}</p>
    </div>
  );
  const cue = next && (
    <a
      href={`#${anchorId(next.id)}`}
      className={styles.cue}
      data-intro="rest"
      onClick={(event) => {
        event.preventDefault();
        onJump(next.id);
      }}
    >
      {copy("Scroll for {count} short chapters", { count: chapters.length })}
      <span className={styles.cueIcon} aria-hidden="true">
        <ChevronDown size={20} strokeWidth={2} />
      </span>
    </a>
  );
  const flat = status === "flat" && (
    <Image
      className={styles.flat}
      src={product.bottle.src}
      width={product.bottle.width}
      height={product.bottle.height}
      alt=""
      preload
      sizes="(max-width: 700px) 60vw, 34vw"
    />
  );

  return (
    <section
      ref={root}
      id={anchorId(chapter.id)}
      data-chapter={chapter.id}
      data-tone={chapter.tone}
      tabIndex={-1}
      aria-labelledby={titleId}
      className={`${chapterStyles.chapter} ${styles.hero}`}
      style={
        nameFit
          ? ({
              "--name-size": `${nameFit.size}px`,
              ...(nameFit.y === null ? {} : { "--name-y": `${nameFit.y}px` }),
            } as CSSProperties)
          : undefined
      }
    >
      <span className={styles.glow} aria-hidden="true" />
      <p
        ref={giant}
        className={styles.giant}
        data-spaced={product.name.startsWith(`${halves[0]} `) || undefined}
        aria-hidden="true"
      >
        <span data-giant-half="a">{halves[0]}</span>
        <span data-giant-half="b">{halves[1]}</span>
        <span className={styles.probe} data-probe>
          {halves[0]}
        </span>
        <span className={styles.probe} data-probe>
          {halves[1]}
        </span>
      </p>
      <div ref={stage} className={styles.stage} data-status={status} aria-hidden="true">
        <canvas ref={canvas} className={styles.canvas} />
        {flat}
      </div>
      <div className={styles.top} data-name-top>
        {eyebrow}
      </div>
      <div className={styles.foot} data-name-foot>
        <div className={styles.lead}>
          {headline}
          {purpose}
        </div>
        <div className={styles.act}>
          {highlights}
          {cart}
        </div>
      </div>
      <div className={styles.cueRow}>{cue}</div>
    </section>
  );
}
