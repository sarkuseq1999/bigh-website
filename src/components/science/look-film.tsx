"use client";

import Image, { getImageProps } from "next/image";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { SplitText } from "gsap/SplitText";
import { ArrowRight, ArrowUpRight, Minus, Plus } from "lucide-react";
import { useEffect, useRef, useState, type CSSProperties } from "react";
import { researchItems } from "@/components/home/research-data";
import { useCopy } from "@/i18n/use-copy";
import { MARKS, OPENING, SHOTS, createFilm, frameAt, type FilmScene } from "./film-scene";
import type { LookProps, LookTheme } from "./look-types";
import { ResearchGroups } from "./research-library";
import {
  ask,
  formulas,
  formulasLine,
  health,
  iris,
  liu,
  liuNumbers,
  opening,
  pathStops,
  questions,
  research,
} from "./science-content";
import styles from "./look-film.module.css";

// Look B, "Scroll film" (Mo's pick, September 28, 2026). The page opens on a film that plays as
// you scroll: the scroll bar is the playhead. It is made in code from stills (film-scene.ts): the
// opening picture, a push into its bright point, through the light onto the glass cell, a pull back
// into a field of cells. Then a dark, warm-lit page: Dr. Liu's portrait as a print under a picture
// lamp, his record in big numbers, his path as a film strip, the five formulas on a lit stage, the
// research as end credits, health in three chapters, and the questions as subtitles.
// Type: Switzer for everything, as on the NuriCell page (loaded once in the locale layout).
// Phones and reduced motion: the film's key frames as stacked stills with their captions.

export const filmTheme: LookTheme = {
  tokens: {
    "--paper": "#05070d",
    "--paper-deep": "#0a0f1c",
    "--ink": "#f3eee5",
    "--muted": "#aaa59b",
    "--body": "#d9d3c8",
    "--line": "#1f2431",
    "--rule": "#3a4050",
    "--blue": "#e9b872",
    "--gold": "#e9b872",
    "--gold-light": "#f4d9a8",
    "--lime": "#e2ed94",
    "--navy": "#05070d",
    "--card-bg": "#0c111d",
    "--card-line": "#232a3a",
    "--door-bg": "#0c111d",
    // The shared header, footer and story panel follow this look's type and corners.
    "--display-font": '"Switzer", var(--font-dm-sans)',
    "--text-font": '"Switzer", var(--font-dm-sans)',
    "--panel-radius": "6px",
    // Eyebrows in the shared story panel: the same warm gold as the page's own eyebrows.
    "--eyebrow": "#e6b877",
    // The header: a quiet dark bar over the page, and over the film only a shadow falling from
    // the top edge (the stage is marked data-tone="film" while the film plays).
    "--header-dark": "rgba(5, 7, 13, 0.76)",
    "--header-dark-blur": "blur(14px)",
    "--header-dark-line": "rgba(246, 240, 230, 0.05)",
    // (no-repeat: the header's transparent hairline would otherwise repeat the gradient's dark top).
    "--header-film":
      "linear-gradient(180deg, rgba(5, 7, 13, 0.66) 0%, rgba(5, 7, 13, 0) 100%) no-repeat",
    "--header-film-blur": "none",
    "--header-film-line": "transparent",
  } as CSSProperties,
  footerTone: "dark",
};

// DRAFT captions for the film, built only from approved facts: the cell's job (health.doors[0],
// the homepage's "tiny power plants") and the subject of Dr. Liu's research (liu.intro).
const CAPTIONS = {
  cell: { lead: "Inside your cells,", accent: "tiny power plants.", note: questions[0].text },
  field: {
    lead: "Cellular energy, nutrition,",
    accent: "and how we age.",
    note: "The connections at the heart of Dr. Liu’s research.",
  },
};

// Alt texts are DRAFT. The film's pictures are AI illustrations (one discreet label for the film).
// The first two shots come from OPENING in film-scene.ts (swap them there).
const FILM_SHOTS = [
  OPENING.still,
  OPENING.macro,
  {
    ...SHOTS.cell,
    alt: "Illustration: a mitochondrion drawn as gold glass, glowing on deep navy.",
  },
  { ...SHOTS.field, alt: "Illustration: a field of glowing cells in the dark." },
];

// His path: the four earlier stops are graded as film memories (one warm archival grade in CSS);
// Today, the film's own opening picture, stays in full color.
type PathPicture = {
  src: string;
  alt: string;
  position?: string;
  // A tighter crop inside the frame: a scale and the point it scales toward.
  crop?: { scale: number; origin: string };
};
const PATH_PICTURES: Record<string, PathPicture> = {
  Okayama: {
    src: "/images/science-page/golden-okayama.webp",
    alt: "Illustration: a study desk at dusk with old books and an open brain atlas.",
  },
  // A Berkeley office window in late light, eucalyptus and golden hills outside (no glassware;
  // made September 28 to replace the soft 2.5x crop of the lab bench). DRAFT alt text.
  "1994": {
    src: "/images/science-page/film/berkeley-window.webp",
    alt: "Illustration: late light through an office window, eucalyptus trees and golden hills outside.",
  },
  "2002": {
    src: "/images/science-page/golden-journal.webp",
    alt: "Illustration: an open science journal with reading glasses and a cup of tea.",
  },
  "2025": {
    src: "/images/science-page/golden-academy.webp",
    alt: "Illustration: a grand academy hall with sunlight falling through tall windows.",
  },
  // Today closes the loop: the film's opening picture.
  Today: {
    src: OPENING.still.src,
    alt: OPENING.still.alt,
    position: OPENING.still.today,
  },
};

// Health explained, on the dark page: the same three topics with renders that sit on dark (the
// glass cell on navy and the droplet are the site's renders; the aged cell was re-rendered on navy
// for this look).
// Each is scaled so its subject spans about the same share of the frame.
const CHAPTER_IMAGES = [
  { src: SHOTS.cell.src, drop: false, scale: 1.12 },
  { src: "/images/science/antioxidant.webp", drop: true, scale: 1 },
  { src: "/images/science-page/film/aged-cell-dark.webp", drop: false, scale: 0.86 },
];

// The opening title's words rise one by one in CSS (no flash before the script runs).
function Words({ text, from = 0 }: { text: string; from?: number }) {
  return text.split(" ").map((word, index) => (
    <span key={`${word}-${index}`}>
      {index > 0 && " "}
      <span className={styles.word} style={{ "--w": from + index } as CSSProperties}>
        {word}
      </span>
    </span>
  ));
}

export function LookFilm({ onStory }: LookProps) {
  const copy = useCopy();
  const root = useRef<HTMLDivElement>(null);
  const [all, setAll] = useState(false);
  const keyStudies = research.key
    .map((url) => researchItems.find((item) => item.url === url))
    .filter((item) => item !== undefined);

  useEffect(() => {
    const element = root.current;
    if (!element) return;
    gsap.registerPlugin(ScrollTrigger, SplitText);
    const q = (selector: string) => [...element.querySelectorAll<HTMLElement>(selector)];
    const one = (selector: string) => element.querySelector<HTMLElement>(selector);
    const media = gsap.matchMedia();
    let alive = true;

    media.add(
      {
        motion: "(prefers-reduced-motion: no-preference)",
        wide: "(min-width: 901px)",
      },
      (context) => {
        const { motion, wide } = context.conditions ?? {};
        if (!motion) return;
        const cleanups: (() => void)[] = [];

        // ---- 1. The film (wide screens with motion). -----------------------------------------
        const reel = one("[data-reel]");
        const stage = one("[data-stage]");
        const holder = one("[data-canvas]");
        if (wide && reel && stage && holder) {
          const state = { p: 0 };
          const layers = q("[data-shot-media]");
          // While the film plays, the header over it is only a shadow (see filmTheme).
          stage.dataset.tone = "film";
          cleanups.push(() => delete stage.dataset.tone);
          const flash = one("[data-flash]");
          const shade = one("[data-shade]");
          // Without WebGL the same choreography moves the stills (no zoom blur, no bloom).
          const still = (p: number) => {
            if (!reel.dataset.fallback) return;
            const aspect = stage.clientWidth / Math.max(1, stage.clientHeight);
            const f = frameAt(p, aspect);
            f.layers.forEach((layer, index) => {
              const node = layers[index];
              if (!node) return;
              const tx = (-(layer.cx - 0.5) * layer.zoom) / layer.sx;
              const ty = (-(layer.cy - 0.5) * layer.zoom) / layer.sy;
              node.style.opacity = String(layer.alpha);
              node.style.transform = `translate(${(tx * 100).toFixed(3)}%, ${(ty * 100).toFixed(3)}%) scale(${layer.zoom.toFixed(4)})`;
            });
            if (flash) flash.style.opacity = String(f.flash);
            if (shade) shade.style.opacity = String(1 - f.dim);
            // The cells show inside the lens first, then everywhere.
            const bridge = layers[1]?.parentElement;
            if (bridge) {
              const radius = f.lens[2] * stage.clientHeight * (1 + 4 * f.lensOpen);
              bridge.style.clipPath = `circle(${radius.toFixed(1)}px at ${(f.lens[0] * 100).toFixed(2)}% ${(f.lens[1] * 100).toFixed(2)}%)`;
            }
          };

          // The film plays while the stage is held; its last screen is the curtain (Dr. Liu's
          // section rising over the final frame).
          const length = () => Math.max(1, reel.offsetHeight - 2 * window.innerHeight);
          const film = gsap.timeline({
            defaults: { ease: "none" },
            scrollTrigger: {
              trigger: reel,
              start: "top top",
              end: () => `+=${length()}`,
              scrub: 1,
              invalidateOnRefresh: true,
            },
            onUpdate: () => still(state.p),
          });
          gsap.set(q("[data-fill]"), { scaleX: 0, transformOrigin: "0 50%" });
          film
            .to(state, { p: 1, duration: 1 }, 0)
            .to(q("[data-fill]"), { scaleX: 1, duration: 1 }, 0)
            .to(q("[data-cue]"), { autoAlpha: 0, duration: 0.03 }, 0)
            // The grade behind the words lifts while there are no words (and the light floods).
            .to(q("[data-scrim]"), { autoAlpha: 0, duration: 0.08 }, 0.12)
            .to(q("[data-scrim]"), { autoAlpha: 1, duration: 0.06 }, MARKS.cellCaption[0] - 0.02)
            .to(
              q("[data-title]"),
              {
                y: -64,
                autoAlpha: 0,
                filter: "blur(10px)",
                duration: MARKS.titleOut[1] - MARKS.titleOut[0],
                ease: "power1.in",
              },
              MARKS.titleOut[0],
            );

          // The curtain: as Dr. Liu's section rises, the last frame and its words go dark.
          const liuSection = one("#dr-liu");
          const curtain = one("[data-curtain]");
          if (liuSection && curtain) {
            gsap.set(curtain, { autoAlpha: 0 });
            gsap.to(curtain, {
              autoAlpha: 0.94,
              ease: "none",
              scrollTrigger: {
                trigger: liuSection,
                start: "top bottom",
                end: "top 35%",
                scrub: true,
              },
            });
          }

          // WebGL loads only here; on failure the stills play the film.
          let scene: FilmScene | null = null;
          let cancelled = false;
          const fallback = () => {
            reel.dataset.fallback = "true";
            still(state.p);
          };
          // No WebGL at all: go straight to the stills (three.js would only log errors).
          const probe = document.createElement("canvas");
          const webgl = !!(probe.getContext("webgl2") || probe.getContext("webgl"));
          if (!webgl) fallback();
          (webgl ? import("three") : Promise.reject(new Error("no WebGL")))
            .then((THREE) => {
              if (cancelled) return;
              try {
                scene = createFilm(THREE, holder, stage, {
                  progress: () => state.p,
                  onReady: (mode) => {
                    reel.dataset.film = mode;
                  },
                  onFail: () => {
                    scene?.dispose();
                    scene = null;
                    fallback();
                  },
                });
              } catch {
                scene = null;
                fallback();
              }
            })
            .catch(() => {
              if (!cancelled && !reel.dataset.fallback) fallback();
            });
          cleanups.push(() => {
            cancelled = true;
            scene?.dispose();
            scene = null;
            delete reel.dataset.film;
            delete reel.dataset.fallback;
            layers.forEach((node) => {
              node.style.opacity = "";
              node.style.transform = "";
            });
            if (layers[1]?.parentElement) layers[1].parentElement.style.clipPath = "";
          });

          // The captions rise word by word (SplitText, once the fonts are in), on the same
          // playhead as the film.
          document.fonts.ready.then(() => {
            if (!alive) return;
            context.add(() => {
              const words = gsap.timeline({
                defaults: { ease: "power2.out" },
                scrollTrigger: {
                  trigger: reel,
                  start: "top top",
                  end: () => `+=${length()}`,
                  scrub: 1,
                  invalidateOnRefresh: true,
                },
              });
              const scenes: [string, readonly number[]][] = [
                ["cell", MARKS.cellCaption],
                ["field", MARKS.fieldCaption],
              ];
              scenes.forEach(([name, marks]) => {
                const caption = one(`[data-caption="${name}"]`);
                if (!caption) return;
                const split = SplitText.create(caption.querySelectorAll("[data-split]"), {
                  type: "lines,words",
                  mask: "lines",
                  // Spans keep the paragraph valid, and screen readers read the words as they are.
                  tag: "span",
                  aria: "none",
                  linesClass: styles.splitLine,
                  wordsClass: styles.splitWord,
                });
                const note = caption.querySelector("[data-note]");
                gsap.set(caption, { autoAlpha: 1 });
                gsap.set(split.words, { yPercent: 110 });
                gsap.set(note, { autoAlpha: 0, y: 18 });
                const span = marks[1] - marks[0];
                words
                  .to(
                    split.words,
                    { yPercent: 0, duration: span * 0.6, stagger: span * 0.07 },
                    marks[0],
                  )
                  .to(note, { autoAlpha: 1, y: 0, duration: span * 0.5 }, marks[0] + span * 0.5);
                if (marks.length > 2) {
                  words.to(
                    caption,
                    {
                      autoAlpha: 0,
                      y: -40,
                      filter: "blur(8px)",
                      duration: marks[3] - marks[2],
                      ease: "power1.in",
                    },
                    marks[2],
                  );
                }
              });
              // Keep the timeline exactly one playhead long.
              words.set({}, {}, 1);
            });
          });
        }

        // ---- 2. Dr. Liu: the lamp comes on and his photograph comes into focus. -------------
        const portrait = one("[data-portrait]");
        if (portrait) {
          gsap.set(q("[data-photo]"), { filter: "blur(16px) brightness(0.7)" });
          gsap.set(q("[data-lamp]"), { autoAlpha: 0 });
          gsap
            .timeline({ scrollTrigger: { trigger: portrait, start: "top 80%", once: true } })
            .to(q("[data-photo]"), {
              filter: "blur(0px) brightness(1)",
              duration: 1.8,
              ease: "power2.out",
              clearProps: "filter",
            })
            .to(q("[data-lamp]"), { autoAlpha: 1, duration: 2.4, ease: "sine.out" }, 0);
        }
        gsap.set(q("[data-rise]"), { autoAlpha: 0, y: 26 });
        ScrollTrigger.batch(q("[data-rise]"), {
          start: "top 90%",
          once: true,
          onEnter: (batch) =>
            gsap.to(batch, {
              autoAlpha: 1,
              y: 0,
              duration: 0.9,
              ease: "power2.out",
              stagger: 0.08,
              overwrite: true,
            }),
        });

        // His record: 280 counts up (the years stay as they are).
        q("[data-count]").forEach((node) => {
          const target = Number(node.dataset.count);
          const counter = { value: 0 };
          node.textContent = "0";
          gsap.to(counter, {
            value: target,
            duration: 1.8,
            ease: "power2.out",
            scrollTrigger: { trigger: node, start: "top 90%", once: true },
            onUpdate: () => {
              node.textContent = String(Math.round(counter.value));
            },
          });
          cleanups.push(() => {
            node.textContent = String(target);
          });
        });

        // ---- 3. His path: a film strip, pinned on wide screens. -------------------------------
        const path = one("[data-path]");
        const track = one("[data-track]");
        const fill = one("[data-path-fill]");
        if (path && track) {
          if (!wide) {
            q("[data-frame-media]").forEach((node) => {
              gsap.set(node, { filter: "blur(10px) brightness(0.75)" });
              gsap.to(node, {
                filter: "blur(0px) brightness(1)",
                duration: 1.5,
                ease: "power2.out",
                clearProps: "filter",
                scrollTrigger: { trigger: node, start: "top 85%", once: true },
              });
            });
          } else {
            const distance = () => Math.max(0, track.scrollWidth - path.clientWidth);
            if (fill) gsap.set(fill, { scaleX: 0, transformOrigin: "0 50%" });
            const slide = gsap.to(track, {
              x: () => -distance(),
              ease: "none",
              scrollTrigger: {
                trigger: path,
                start: "top top",
                end: () => `+=${distance()}`,
                pin: true,
                scrub: 0.8,
                invalidateOnRefresh: true,
                onUpdate: (self) => {
                  if (fill) gsap.set(fill, { scaleX: self.progress });
                },
              },
            });
            // Each frame is soft at the sides and sharp in the middle; its year lights with it.
            q("[data-stop]").forEach((stop) => {
              const frame = stop.querySelector("[data-frame-media]");
              const year = stop.querySelector("[data-year]");
              gsap.set(frame, { filter: "blur(10px) brightness(0.55)", scale: 1.08 });
              gsap.set(year, { opacity: 0.28 });
              gsap
                .timeline({
                  scrollTrigger: {
                    trigger: stop,
                    containerAnimation: slide,
                    start: "left right",
                    end: "right left",
                    scrub: true,
                  },
                })
                .to(frame, {
                  filter: "blur(0px) brightness(1)",
                  scale: 1,
                  duration: 1,
                  ease: "sine.out",
                })
                .to(year, { opacity: 1, duration: 1, ease: "sine.out" }, 0)
                .to(frame, { duration: 0.5 })
                .to(frame, {
                  filter: "blur(8px) brightness(0.6)",
                  scale: 1.04,
                  duration: 1,
                  ease: "sine.in",
                })
                .to(year, { opacity: 0.28, duration: 1, ease: "sine.in" }, "<");
            });
          }
        }

        // ---- 4. The formulas: the stage lights come up, one pool at a time. -------------------
        const lineup = one("[data-lineup]");
        if (lineup) {
          // Before the lights: each bottle stands in shadow (a dark layer in its own outline).
          gsap.set(q("[data-pool]"), { autoAlpha: 0 });
          gsap.set(q("[data-unlit]"), { autoAlpha: 1 });
          const lights = gsap.timeline({
            scrollTrigger: { trigger: lineup, start: "top 72%", once: true },
          });
          q("[data-bottle-item]").forEach((item, index) => {
            const at = index === 0 ? 0 : 0.5 + index * 0.18;
            lights
              .to(
                item.querySelectorAll("[data-pool]"),
                { autoAlpha: 1, duration: 1.2, ease: "sine.out" },
                at,
              )
              .to(
                item.querySelector("[data-unlit]"),
                { autoAlpha: 0, duration: 1.2, ease: "sine.out" },
                at,
              );
          });
        }

        // ---- 5. Health: each chapter still comes into focus. ---------------------------------
        q("[data-chapter-media]").forEach((node) => {
          gsap.set(node, { filter: "blur(10px) brightness(0.6)" });
          gsap.to(node, {
            filter: "blur(0px) brightness(1)",
            duration: 1.6,
            ease: "power2.out",
            clearProps: "filter",
            scrollTrigger: { trigger: node, start: "top 85%", once: true },
          });
        });

        // ---- 6. Ask: the questions play like subtitles as the screen passes. ------------------
        const screen = one("[data-screen]");
        const lines = q("[data-subtitle]");
        if (screen && lines.length) {
          screen.dataset.cycle = "true";
          const show = (index: number) =>
            lines.forEach((line, i) => line.toggleAttribute("data-on", i === index));
          show(0);
          ScrollTrigger.create({
            trigger: screen,
            start: "top 75%",
            end: "bottom 30%",
            onUpdate: (self) =>
              show(Math.min(lines.length - 1, Math.floor(self.progress * lines.length))),
          });
          cleanups.push(() => {
            delete screen.dataset.cycle;
            lines.forEach((line) => line.removeAttribute("data-on"));
          });
        }

        return () => cleanups.forEach((cleanup) => cleanup());
      },
    );

    return () => {
      alive = false;
      media.revert();
    };
  }, []);

  // Opening the full list moves everything below it.
  useEffect(() => {
    ScrollTrigger.refresh();
  }, [all]);

  const stops = [
    ...pathStops.filter((stop) => stop.mark !== "Today"),
    ...pathStops.filter((stop) => stop.mark === "Today"),
  ];

  // The formulas: a credit shared by several products is set once, as one line under them.
  const sharedCredit = formulas.find(
    (formula, index) => formulas.findIndex((other) => other.credit === formula.credit) !== index,
  )?.credit;
  const sharedNames = formulas.filter((formula) => formula.credit === sharedCredit);

  // One bottle on the stage: its pool of light, its reflection, the bottle, the light falling
  // across it (a shadow in its own outline, so the label colors stay true), and its credit.
  const bottle = (formula: (typeof formulas)[number], index: number) => {
    const lead = index === 0;
    const sizes = lead ? "(max-width: 900px) 70vw, 440px" : "(max-width: 900px) 42vw, 220px";
    const shared = formula.credit === sharedCredit;
    const outline = getImageProps({ src: formula.image, alt: "", width: 256, height: 266 }).props
      .src;
    return (
      <figure
        key={formula.name}
        className={`${styles.product} ${lead ? styles.leadProduct : ""}`}
        style={{ "--col": index } as CSSProperties}
        data-bottle-item
      >
        <div className={styles.set} style={{ "--outline": `url("${outline}")` } as CSSProperties}>
          {lead && <span className={styles.spot} data-pool aria-hidden="true" />}
          <span className={styles.pool} data-pool aria-hidden="true" />
          <div className={styles.reflection} aria-hidden="true">
            <Image src={formula.image} alt="" fill sizes={sizes} />
          </div>
          <div className={styles.bottle}>
            <Image
              src={formula.image}
              alt={copy("{name} bottle", { name: formula.name })}
              fill
              sizes={sizes}
            />
          </div>
          <span className={styles.falloff} aria-hidden="true" />
          <span className={styles.unlit} data-unlit aria-hidden="true" />
        </div>
        <figcaption className={styles.credit}>
          <strong className={styles.productName}>{formula.name}</strong>
          <span className={shared ? styles.srOnly : styles.creditText}>{copy(formula.credit)}</span>
        </figcaption>
      </figure>
    );
  };

  return (
    <div ref={root} className={styles.film}>
      <section id="scientists" className={styles.scientists} data-tone="dark">
        {/* ---- The film. ---- */}
        <div className={styles.reel} data-reel>
          <div
            className={styles.stage}
            data-stage
            style={{ "--phone-crop": OPENING.still.phone ?? "50% 50%" } as CSSProperties}
          >
            {FILM_SHOTS.map((shot, index) => {
              const caption = index === 2 ? CAPTIONS.cell : index === 3 ? CAPTIONS.field : null;
              return (
                <div
                  key={shot.src}
                  className={styles.shot}
                  data-shot={index === 1 ? "bridge" : String(index)}
                >
                  <div className={styles.shotMedia} data-shot-media>
                    <Image
                      src={shot.src}
                      alt={shot.alt ? copy(shot.alt) : ""}
                      fill
                      // Phones crop the wide stills: the opening fills the screen's height.
                      sizes={
                        index === 0
                          ? "(max-width: 900px) 180vh, 100vw"
                          : "(max-width: 900px) 140vw, 100vw"
                      }
                      loading={index === 0 ? "eager" : "lazy"}
                      fetchPriority={index === 0 ? "high" : undefined}
                      className={styles.shotImage}
                    />
                  </div>
                  {index === 0 && (
                    <div className={styles.titleBlock} data-title>
                      <h1 className={styles.title}>
                        <span className={styles.titleLead}>
                          <Words text={copy(opening.titleLead)} />
                        </span>{" "}
                        <span className={styles.titleAccent}>
                          <Words text={copy(opening.titleAccent)} from={3} />
                        </span>
                      </h1>
                    </div>
                  )}
                  {caption && (
                    <div className={styles.caption} data-caption={index === 2 ? "cell" : "field"}>
                      <p className={styles.captionLine}>
                        <span className={styles.captionLead} data-split>
                          {copy(caption.lead)}
                        </span>{" "}
                        <span className={styles.captionAccent} data-split>
                          {copy(caption.accent)}
                        </span>
                      </p>
                      <p className={styles.captionNote} data-note>
                        {copy(caption.note)}
                      </p>
                    </div>
                  )}
                </div>
              );
            })}
            <div className={styles.canvas} data-canvas aria-hidden="true" />
            <span className={styles.flash} data-flash aria-hidden="true" />
            <span className={styles.shade} data-shade aria-hidden="true" />
            <span className={styles.scrim} data-scrim aria-hidden="true" />
            <span className={styles.curtain} data-curtain aria-hidden="true" />
            <span className={styles.fadeIn} aria-hidden="true" />
            <div className={styles.filmBar} aria-hidden="true">
              <span className={styles.label}>{copy("Illustration")}</span>
              <span className={styles.filmLine}>
                <span className={styles.filmFill} data-fill />
              </span>
            </div>
            <a href="#dr-liu" className={`${styles.cue} ${styles.label}`} data-cue>
              <span className={styles.cueLine} aria-hidden="true" />
              {copy("Scroll to play") /* DRAFT */}
            </a>
          </div>
        </div>

        {/* ---- Dr. Liu: a print on a dark wall, under a picture lamp. ---- */}
        <div id="dr-liu" className={styles.liu}>
          <div className={styles.liuInner}>
            <figure className={styles.portrait} data-portrait>
              <span className={styles.lamp} data-lamp aria-hidden="true" />
              <div className={styles.print}>
                <div className={styles.photoFrame}>
                  <Image
                    src={liu.photo.src}
                    alt={copy(liu.name)}
                    fill
                    sizes="(max-width: 900px) 80vw, 440px"
                    className={styles.photo}
                    data-photo
                  />
                </div>
              </div>
            </figure>
            <div className={styles.liuCopy}>
              <p className={`${styles.label} ${styles.eyebrow}`} data-rise>
                {copy(liu.role)}
              </p>
              <h2 className={styles.name} data-rise>
                {copy(liu.name)}
              </h2>
              <p className={styles.headline} data-rise>
                {copy(liu.headline)}
              </p>
              <p className={styles.intro} data-rise>
                {copy(liu.intro)}
              </p>
              <button type="button" className={styles.textButton} onClick={onStory} data-rise>
                {copy(liu.button)} <ArrowRight size={20} aria-hidden="true" />
              </button>
            </div>
          </div>

          {/* His record, as big numbers. */}
          <div className={styles.record} data-record>
            {liuNumbers.map((item) => (
              <div key={item.value} className={styles.figure} data-rise>
                <p className={styles.value}>
                  <span data-count={item.suffix ? item.value : undefined}>{item.value}</span>
                  {item.suffix && <span className={styles.suffix}>{item.suffix}</span>}
                </p>
                <p className={styles.figureLabel}>{copy(item.label)}</p>
                <a
                  href={item.url}
                  target="_blank"
                  rel="noreferrer"
                  className={`${styles.source} ${styles.label}`}
                >
                  {copy("Source")} <ArrowUpRight size={16} aria-hidden="true" />
                </a>
              </div>
            ))}
          </div>
        </div>

        {/* ---- His path: a film strip. ---- */}
        <div className={styles.path} data-path>
          <div className={styles.track} data-track>
            <div className={styles.pathLead}>
              <h2 className={styles.sectionTitle}>{copy("A life in cell science.") /* DRAFT */}</h2>
              <p className={styles.sectionText}>
                {copy("From Okayama to Berkeley, and from the lab to BiGH.") /* DRAFT */}
              </p>
            </div>
            {stops.map((stop) => {
              const picture = PATH_PICTURES[stop.mark];
              return (
                <article key={stop.mark} className={styles.stop} data-stop>
                  <p className={styles.year} data-year>
                    {copy(stop.mark)}
                  </p>
                  <div
                    className={`${styles.frame} ${stop.mark === "Today" ? "" : styles.archival}`}
                  >
                    <div className={styles.frameMedia} data-frame-media>
                      <Image
                        src={picture.src}
                        alt={copy(picture.alt)}
                        fill
                        // A cropped picture needs the full file to stay sharp.
                        sizes={picture.crop ? "1200px" : "(max-width: 900px) 88vw, 420px"}
                        style={{
                          objectPosition: picture.position,
                          transform: picture.crop ? `scale(${picture.crop.scale})` : undefined,
                          transformOrigin: picture.crop?.origin,
                        }}
                      />
                    </div>
                  </div>
                  <div className={styles.stopWords}>
                    <h3 className={styles.itemTitle}>{copy(stop.title)}</h3>
                    <p className={styles.stopText}>{copy(stop.text)}</p>
                    {stop.url && (
                      <a
                        href={stop.url}
                        target="_blank"
                        rel="noreferrer"
                        className={`${styles.source} ${styles.label}`}
                      >
                        {copy(stop.link)} <ArrowUpRight size={16} aria-hidden="true" />
                      </a>
                    )}
                  </div>
                </article>
              );
            })}
          </div>
          <div className={styles.pathBar} aria-hidden="true">
            <span className={styles.label}>{copy("Illustration")}</span>
            <span className={styles.filmLine}>
              <span className={styles.filmFill} data-path-fill />
            </span>
          </div>
        </div>
      </section>

      {/* ---- The formulas, on a lit stage. ---- */}
      <section className={styles.formulas} data-tone="dark" aria-labelledby="film-formulas">
        <h2 id="film-formulas" className={styles.formulasLine} data-rise>
          {copy(formulasLine)}
        </h2>
        {/* NuriCell forward in the key light; the four others set back on the floor behind. */}
        <div className={styles.lineup} data-lineup>
          {bottle(formulas[0], 0)}
          <div className={styles.backRow}>
            <span className={styles.floor} aria-hidden="true" />
            {formulas.slice(1).map((formula, index) => bottle(formula, index + 1))}
            {sharedCredit && (
              <p className={styles.sharedCredit} aria-hidden="true" data-rise>
                <span className={styles.sharedNames}>
                  {sharedNames.map((formula) => formula.name).join(" · ")}
                </span>
                <span className={styles.creditText}>{copy(sharedCredit)}</span>
              </p>
            )}
          </div>
        </div>
        {/* End credits. Dr. Iris Wang appears in words only. */}
        <dl className={styles.endCredits}>
          <div className={styles.creditRow} data-rise>
            <dt className={styles.label}>{copy(liu.role)}</dt>
            <dd>{copy(liu.name)}</dd>
          </div>
          <div className={styles.creditRow} data-rise>
            <dt className={styles.label}>{copy(iris.role)}</dt>
            <dd>
              {copy(iris.name)}
              <span>{copy(iris.text)}</span>
            </dd>
          </div>
        </dl>
      </section>

      {/* ---- The research, set like a film's end credits. ---- */}
      <section id="research" className={styles.research} data-tone="dark">
        <div className={styles.creditsHead}>
          <h2 className={styles.sectionTitle} data-rise>
            {copy(research.title)}
          </h2>
          <p className={styles.sectionText} data-rise>
            {copy(research.text)}
          </p>
        </div>
        <ol className={styles.studies}>
          {keyStudies.map((item) => (
            <li key={item.url} className={styles.study} data-key-study data-rise>
              <p className={styles.label}>
                {copy(item.category)} · {copy(item.year)} · {item.journal}
              </p>
              <h3 className={styles.studyTitle}>{copy(item.title)}</h3>
              {research.byLiu.includes(item.url) && (
                <p className={styles.studyTag}>{copy(research.tag)}</p>
              )}
              <p className={styles.studyText}>{copy(item.text)}</p>
              <a
                href={item.url}
                target="_blank"
                rel="noreferrer"
                className={`${styles.source} ${styles.label}`}
              >
                {copy("Read original source")} <ArrowUpRight size={16} aria-hidden="true" />
              </a>
            </li>
          ))}
        </ol>
        <div className={styles.seeAllRow}>
          <button
            type="button"
            className={styles.textButton}
            aria-expanded={all}
            onClick={() => setAll(!all)}
          >
            {/* A string without a catalog key comes back as written, so fill {count} here too. */}
            {all
              ? copy(research.hideAll)
              : copy(research.seeAll, { count: researchItems.length }).replace(
                  "{count}",
                  String(researchItems.length),
                )}
            {all ? <Minus size={18} aria-hidden="true" /> : <Plus size={18} aria-hidden="true" />}
          </button>
        </div>
        {all && (
          <div className={styles.all}>
            <ResearchGroups everything />
          </div>
        )}
        <p className={styles.note}>{copy(research.note)}</p>
      </section>

      {/* ---- Health, explained: three chapters. ---- */}
      <section id="health" className={styles.health} data-tone="dark">
        <div className={styles.healthHead}>
          <h2 className={styles.sectionTitle} data-rise>
            {copy(health.title)}
          </h2>
          <p className={styles.sectionText} data-rise>
            {copy(health.text)}
          </p>
        </div>
        <div className={styles.chapters}>
          {health.doors.map((door, index) => {
            const picture = CHAPTER_IMAGES[index];
            return (
              <article key={door.topic} className={styles.chapter} data-rise>
                <div className={styles.chapterFrame}>
                  <div
                    className={`${styles.chapterMedia} ${picture.drop ? styles.dropMedia : ""}`}
                    style={{ "--fit": picture.scale } as CSSProperties}
                    data-chapter-media
                  >
                    <Image
                      src={picture.src}
                      alt=""
                      fill
                      sizes={picture.drop ? "300px" : "(max-width: 900px) 88vw, 440px"}
                    />
                  </div>
                </div>
                <p className={`${styles.label} ${styles.eyebrow}`}>
                  <span className={styles.chapterNumber}>{String(index + 1).padStart(2, "0")}</span>{" "}
                  {copy(door.topic)}
                </p>
                <h3 className={styles.itemTitle}>{copy(door.title)}</h3>
                <p className={styles.chapterText}>{copy(door.preview)}</p>
                <p className={`${styles.label} ${styles.soon}`}>{copy(health.soon)}</p>
              </article>
            );
          })}
        </div>
        <p className={`${styles.label} ${styles.illustrations}`}>
          {copy("Illustrations") /* DRAFT */}
        </p>
      </section>

      {/* ---- Ask BiGH Science: a title card and the questions as subtitles, on a dark screen. ---- */}
      <section id="ask" className={styles.ask} data-tone="dark">
        <div className={styles.screen} data-screen>
          {/* The film's last frame returns, dimmed, behind the questions. */}
          <div className={styles.screenShot} aria-hidden="true">
            <Image src={SHOTS.field.src} alt="" fill sizes="100vw" />
          </div>
          <div className={styles.askHead}>
            <h2 className={styles.askTitle} data-rise>
              {copy(ask.title)}
            </h2>
            <p className={styles.lead} data-rise>
              {copy(ask.lead)}
            </p>
          </div>
          <div className={styles.subtitleArea}>
            <p className={`${styles.label} ${styles.eyebrow}`}>{copy(ask.examplesLabel)}</p>
            <ul className={styles.subtitles}>
              {ask.examples.map((question) => (
                <li key={question} data-subtitle>
                  {copy(question)}
                </li>
              ))}
            </ul>
          </div>
        </div>
        <div className={styles.askBody}>
          <div className={styles.askIntro}>
            <p className={styles.lead} data-rise>
              {copy(ask.text)}
            </p>
            <div className={styles.status} data-rise>
              <p className={`${styles.label} ${styles.eyebrow} ${styles.statusLabel}`}>
                {copy(ask.status)}
              </p>
              <p className={styles.statusNote}>{copy(ask.note)}</p>
            </div>
          </div>
          <ol className={styles.steps}>
            {ask.steps.map((step, index) => (
              <li key={step} data-rise>
                <span className={styles.stepNumber}>{index + 1}</span>
                <p>{copy(step)}</p>
              </li>
            ))}
          </ol>
        </div>
      </section>
    </div>
  );
}
