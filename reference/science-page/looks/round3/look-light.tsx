"use client";

import Image from "next/image";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { SplitText } from "gsap/SplitText";
import { ArrowRight, ArrowUpRight, Minus, Plus } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { researchItems } from "@/components/home/research-data";
import { useCopy } from "@/i18n/use-copy";
import { hostGrotesk, lightStack } from "./light-fonts";
import type { Light, LightPreset, LightView } from "./light-scene";
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
  research,
} from "./science-content";
import styles from "./look-light.module.css";

// Look A, "Liquid light" (round 3, September 28, 2026). After Altos Labs: a full-bleed field of
// flowing light behind one large, calm, left-aligned headline, then clean paper pages with
// confident type and almost no decoration. BiGH's version: the light is deep ultramarine to ice
// blue, with one thin thread of molten gold (energy).
//   1. The hero: the liquid light full screen (light-scene.ts); the pointer stirs it; scrolling
//      away deepens and slows it. The headline rises line by line, word by word.
//   2. Dr. Liu: his name set huge across the grid, resting on the top of his sharp portrait
//      (which comes into focus), a thin band of the light beside him; the words fit one screen.
//   3. His record: three large numerals filled with the same light.
//   4. His path: pinned on wide screens, it slides sideways; the light runs along a thin river as
//      you go and fills each year as it arrives. Phones and reduced motion: top to bottom, the years
//      holding one still frame of the light.
//   5. The formulas: NuriCell alone on a pale studio sweep with its approved line and credit, then
//      the other four in a quieter row on the same sweep, each with its credit.
//   6. The research: three key studies as a numbered list; all 36 on request.
//   7. Health explained: three rows, each render in the same framed studio sweep; the row that
//      is hovered or reached catches the light.
//   8. Ask BiGH Science: dark, over a slower, calmer light.

export const lightTheme: LookTheme = {
  tokens: {
    "--paper": "#f5f7fb",
    "--paper-deep": "#eceff6",
    "--ink": "#0b1533",
    "--muted": "#56607a",
    "--body": "#2b3552",
    "--line": "#d9deea",
    "--rule": "#c9d0de",
    "--blue": "#2149a3",
    "--lime": "#e4ebf8",
    "--card-bg": "#ffffff",
    "--card-line": "#d9deea",
    "--gutter": "clamp(20px, 4.45vw, 64px)",
    "--wide": "1312px",
    // One typeface for the whole page, the shared header, footer and panels included.
    "--font-sans": lightStack,
    "--font-instrument": lightStack,
    "--text-font": lightStack,
    "--display-font": lightStack,
    "--panel-radius": "0px",
    // Over the liquid light the header stays see-through instead of a heavy navy band.
    "--header-dark": "rgba(8, 16, 58, 0.22)",
  } as LookTheme["tokens"],
  footerTone: "light",
};

// The renders under Health explained are AI illustrations made for BiGH (one caption for the
// group). Alt texts are DRAFT.
const HEALTH_ALT = [
  "Illustration: a glass mitochondrion glowing gold inside.",
  "Illustration: a clear green droplet.",
  "Illustration: the same glass mitochondrion, clouded with age.",
];

const pad = (index: number) => String(index + 1).padStart(2, "0");

export function LookLight({ onStory }: LookProps) {
  const copy = useCopy();
  const root = useRef<HTMLDivElement>(null);
  const [all, setAll] = useState(false);
  const key = research.key
    .map((url) => researchItems.find((item) => item.url === url))
    .filter((item) => item !== undefined);
  const today = pathStops[pathStops.length - 1];

  // The liquid light: one canvas per view, each paused while off screen.
  useEffect(() => {
    const element = root.current;
    if (!element) return;
    let disposed = false;
    const lights: Light[] = [];
    const reduced = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const hero = element.querySelector<HTMLElement>("[data-hero]");

    import("./light-scene").then(({ createLight, snapshot }) => {
      if (disposed) return;
      // Phones and reduced motion read his path top to bottom, without the moving river: the years
      // still carry the light, as one still frame of it clipped to their letters.
      const path = element.querySelector<HTMLElement>("[data-path]");
      const still = "(max-width: 900px), (prefers-reduced-motion: reduce)";
      if (path && window.matchMedia(still).matches) {
        const url = snapshot("fill", 960, 320, 3.3);
        if (url) {
          path.style.setProperty("--still-light", `url(${url})`);
          path.setAttribute("data-still", "");
        }
      }
      const add = (
        canvas: HTMLCanvasElement | null,
        preset: LightPreset,
        extra: Partial<LightView> = {},
      ) => {
        if (!canvas) return;
        const light = createLight({ canvas, preset, still: reduced, ...extra });
        if (light) lights.push(light);
        else canvas.dataset.light = "none";
      };
      add(element.querySelector("[data-hero-light]"), "hero", {
        depth: () => (hero ? gsap.utils.clamp(0, 1, window.scrollY / hero.offsetHeight) : 0),
        onReady: () => hero?.setAttribute("data-lit", ""),
      });
      // The three numerals are windows onto one flow: each passes its place on the page.
      element.querySelectorAll<HTMLCanvasElement>("[data-fill]").forEach((canvas) => {
        add(canvas, "fill", {
          seed: 2.4,
          offset: () => {
            const box = canvas.getBoundingClientRect();
            return [box.left, box.top + window.scrollY];
          },
        });
      });
      add(element.querySelector("[data-strip-light]"), "strip", { seed: 1.7 });
      add(element.querySelector("[data-river-light]"), "river", { seed: 5.1 });
      add(element.querySelector("[data-ask-light]"), "ask", { seed: 8.7 });
    });

    return () => {
      disposed = true;
      lights.forEach((light) => light.dispose());
    };
  }, []);

  // Motion: the headline, focus pulls, the sideways path, the health rows.
  useEffect(() => {
    const element = root.current;
    if (!element) return;
    gsap.registerPlugin(ScrollTrigger, SplitText);
    const q = (selector: string) => [...element.querySelectorAll<HTMLElement>(selector)];
    const one = (selector: string) => element.querySelector<HTMLElement>(selector);
    const title = one("[data-hero-title]");
    const media = gsap.matchMedia();

    media.add(
      { motion: "(prefers-reduced-motion: no-preference)", wide: "(min-width: 901px)" },
      (context) => {
        const { motion, wide } = context.conditions ?? {};
        if (!motion) {
          title?.setAttribute("data-split", "done");
          return;
        }
        let live = true;

        // 1. The headline: masked lines, the words rising in turn (after the font has loaded, so
        // the lines break where they will stay).
        document.fonts.ready.then(() => {
          if (!live || !title) return;
          context.add(() => {
            const split = SplitText.create(title, {
              type: "lines,words",
              mask: "lines",
              linesClass: styles.heroLine,
            });
            title.setAttribute("data-split", "done");
            gsap.set(split.words, { yPercent: 118 });
            gsap.to(split.words, {
              yPercent: 0,
              duration: 1.35,
              ease: "expo.out",
              stagger: 0.075,
              delay: 0.35,
            });
            gsap.set(q("[data-hero-foot]"), { opacity: 0, y: 14 });
            gsap.to(q("[data-hero-foot]"), {
              opacity: 1,
              y: 0,
              duration: 1,
              ease: "power2.out",
              delay: 1.5,
              stagger: 0.12,
            });
          });
        });

        // Scrolling away: the words drift up and dim a little (the light deepens in its shader).
        gsap.to(q("[data-hero-copy]"), {
          y: -110,
          opacity: 0.25,
          ease: "none",
          scrollTrigger: {
            trigger: one("[data-hero]"),
            start: "top top",
            end: "bottom top",
            scrub: true,
          },
        });

        // 2. Dr. Liu: his photograph comes into focus as it arrives; his name and words follow.
        const portrait = one("[data-portrait]");
        gsap.set(q("[data-photo]"), { filter: "blur(16px)", scale: 1.06 });
        gsap.to(q("[data-photo]"), {
          filter: "blur(0px)",
          scale: 1,
          duration: 1.6,
          ease: "power2.out",
          clearProps: "filter",
          scrollTrigger: { trigger: portrait, start: "top 85%", once: true },
        });
        q("[data-rise]").forEach((node) => {
          gsap.set(node, { opacity: 0, y: 26 });
          gsap.to(node, {
            opacity: 1,
            y: 0,
            duration: 0.9,
            ease: "power2.out",
            scrollTrigger: { trigger: node, start: "top 90%", once: true },
          });
        });

        // 3. The record: 280 counts up once (the years stay as they are).
        q("[data-count]").forEach((node) => {
          const target = Number(node.dataset.count);
          const state = { value: 0 };
          node.textContent = "0";
          gsap.to(state, {
            value: target,
            duration: 1.8,
            ease: "power2.out",
            scrollTrigger: { trigger: node, start: "top 85%", once: true },
            onUpdate: () => {
              node.textContent = String(Math.round(state.value));
            },
            onComplete: () => {
              node.textContent = String(target);
            },
          });
        });

        // 4. His path, sideways (wide screens only).
        const pin = one("[data-pin]");
        const track = one("[data-track]");
        const stops = q("[data-stop]");
        const first = stops[0];
        const last = stops[stops.length - 1];
        if (wide && pin && track && first && last) {
          const distance = () => Math.max(0, track.scrollWidth - pin.clientWidth);
          // The light runs along the river as you go, from his first stop to Today; each year
          // fills with it as the light arrives.
          const place = () => {
            const x = Number(gsap.getProperty(track, "x")) || 0;
            const span = distance();
            const progress = span ? gsap.utils.clamp(0, 1, -x / span) : 1;
            const length = last.offsetLeft + last.offsetWidth - first.offsetLeft;
            const reach = 90 + progress * (length - 90);
            track.style.setProperty("--reach", `${reach}px`);
            stops.forEach((stop) => {
              stop.toggleAttribute("data-dim", stop.offsetLeft - first.offsetLeft > reach - 60);
            });
          };
          element.setAttribute("data-sideways", "");
          gsap.to(track, {
            x: () => -distance(),
            ease: "none",
            onUpdate: place,
            scrollTrigger: {
              trigger: pin,
              start: "top top",
              end: () => `+=${distance()}`,
              pin: true,
              scrub: 0.8,
              invalidateOnRefresh: true,
              onRefresh: place,
            },
          });
          place();
        }

        // 7. Health explained: the row that is hovered, or else the one in the middle of the
        // screen, opens its render.
        const rows = q("[data-door]");
        const list = one("[data-doors]");
        let hovered = -1;
        let reached = 0;
        const show = () => {
          const active = hovered >= 0 ? hovered : reached;
          rows.forEach((row, index) => row.toggleAttribute("data-active", index === active));
        };
        list?.setAttribute("data-armed", "");
        const listeners: [HTMLElement, () => void, () => void][] = [];
        rows.forEach((row, index) => {
          ScrollTrigger.create({
            trigger: row,
            start: "top 62%",
            end: "bottom 38%",
            onToggle: (self) => {
              if (self.isActive) {
                reached = index;
                show();
              }
            },
          });
          const enter = () => {
            hovered = index;
            show();
          };
          const leave = () => {
            hovered = -1;
            show();
          };
          row.addEventListener("pointerenter", enter);
          row.addEventListener("pointerleave", leave);
          listeners.push([row, enter, leave]);
        });
        show();

        return () => {
          live = false;
          listeners.forEach(([row, enter, leave]) => {
            row.removeEventListener("pointerenter", enter);
            row.removeEventListener("pointerleave", leave);
          });
          list?.removeAttribute("data-armed");
          rows.forEach((row) => row.removeAttribute("data-active"));
          element.removeAttribute("data-sideways");
          track?.style.removeProperty("--reach");
          stops.forEach((stop) => stop.removeAttribute("data-dim"));
        };
      },
    );

    // Fonts and pictures change the page's height: measure again once they are in.
    let refresh = 0;
    const later = () => {
      window.clearTimeout(refresh);
      refresh = window.setTimeout(() => ScrollTrigger.refresh(), 150);
    };
    document.fonts.ready.then(later);
    window.addEventListener("load", later);

    return () => {
      window.clearTimeout(refresh);
      window.removeEventListener("load", later);
      media.revert();
    };
  }, []);

  return (
    <div ref={root} className={`${styles.light} ${hostGrotesk.variable}`}>
      <section id="scientists" className={styles.scientists} data-tone="light">
        {/* 1. The hero: the liquid light, full screen. */}
        <div className={styles.hero} data-hero data-tone="dark">
          <canvas className={styles.heroLight} data-hero-light aria-hidden="true" />
          <span className={styles.heroShade} aria-hidden="true" />
          <div className={`${styles.grid} ${styles.heroGrid}`} data-hero-copy>
            <h1 className={styles.heroTitle} data-hero-title data-split="pending">
              {copy(opening.title)}
            </h1>
            <div className={styles.heroFoot}>
              <a href="#dr-liu" className={styles.cue} data-hero-foot>
                <span className={styles.cueLine} aria-hidden="true" />
                {copy("Scroll") /* DRAFT */}
              </a>
              <p className={styles.heroNames} data-hero-foot>
                <span>{copy(liu.name)}</span>
                <span>{copy(iris.name)}</span>
              </p>
            </div>
          </div>
        </div>

        {/* 2. Dr. Liu: his name across the grid, its foot resting on the top of his photograph; a
            thin band of the hero's light runs down beside him. */}
        <div id="dr-liu" className={`${styles.grid} ${styles.liu}`}>
          <h2 className={styles.name} data-rise>
            {copy(liu.name)}
          </h2>
          <div className={styles.portraitWrap}>
            <figure className={styles.portrait} data-portrait>
              <Image
                src={liu.photo.src}
                alt={copy(liu.name)}
                fill
                sizes="(max-width: 900px) 80vw, 400px"
                className={styles.photo}
                data-photo
              />
            </figure>
            <span className={styles.strip} aria-hidden="true">
              <canvas data-strip-light />
            </span>
          </div>
          <div className={styles.liuBody}>
            <p className={styles.role} data-rise>
              {copy(liu.role)}
            </p>
            <p className={styles.liuHeadline} data-rise>
              {copy(liu.headline)}
            </p>
            <p className={styles.bodyText} data-rise>
              {copy(liu.intro)}
            </p>
            <div data-rise>
              <button type="button" className={styles.storyButton} onClick={onStory}>
                {copy(liu.button)}
                <ArrowRight size={20} aria-hidden="true" />
              </button>
            </div>
          </div>
        </div>

        {/* 3. His record: three numerals filled with the light. */}
        <div className={`${styles.grid} ${styles.record}`}>
          <h2 className={styles.hidden}>{copy("His record") /* DRAFT */}</h2>
          {liuNumbers.map((item) => (
            <div key={item.value} className={styles.figure} data-rise>
              <div className={styles.numeral}>
                <canvas className={styles.fill} data-fill aria-hidden="true" />
                <p className={styles.numeralText}>
                  <span data-count={item.suffix ? item.value : undefined}>{item.value}</span>
                  {item.suffix}
                </p>
              </div>
              <p className={styles.figureLabel}>{copy(item.label)}</p>
              <a href={item.url} target="_blank" rel="noreferrer" className={styles.source}>
                {copy("Source")} <ArrowUpRight size={16} aria-hidden="true" />
              </a>
            </div>
          ))}
          <p className={styles.tribute} data-rise>
            {copy(liu.highlights[2].text)}{" "}
            <a
              href={liu.highlights[2].url}
              target="_blank"
              rel="noreferrer"
              className={styles.inlineLink}
            >
              {copy(liu.highlights[2].link)}
              <ArrowUpRight size={18} aria-hidden="true" />
            </a>
          </p>
        </div>

        {/* 4. His path, along a river of the light. */}
        <div className={styles.path} aria-labelledby="light-path-title" data-path>
          <div className={styles.pin} data-pin>
            <div className={`${styles.grid} ${styles.pathHead}`}>
              <h2 id="light-path-title" className={styles.pathTitle}>
                {copy("From Okayama to Berkeley to BiGH.") /* DRAFT */}
              </h2>
              <p className={styles.pathHint} aria-hidden="true">
                {copy("His path") /* DRAFT */}
                <ArrowRight size={18} />
              </p>
            </div>
            <div className={styles.track} data-track>
              {/* Wide screens: the years and the river are windows onto one flow of light. */}
              <span className={styles.band} aria-hidden="true">
                <canvas data-river-light />
              </span>
              {pathStops.map((stop) => (
                <article
                  key={stop.mark}
                  className={`${styles.stop} ${stop === today ? styles.today : ""}`}
                  data-stop
                >
                  <div className={styles.markBlock}>
                    <p className={styles.mark}>{copy(stop.mark)}</p>
                    <span className={styles.riverBar} aria-hidden="true" />
                  </div>
                  <span className={styles.tick} aria-hidden="true" />
                  <div className={styles.stopBody}>
                    <h3 className={styles.stopTitle}>{copy(stop.title)}</h3>
                    <p className={styles.stopText}>{copy(stop.text)}</p>
                    {stop.url && (
                      <a href={stop.url} target="_blank" rel="noreferrer" className={styles.source}>
                        {copy(stop.link)} <ArrowUpRight size={16} aria-hidden="true" />
                      </a>
                    )}
                  </div>
                </article>
              ))}
              <span className={styles.curtain} aria-hidden="true" />
            </div>
          </div>
        </div>
      </section>

      {/* 5. The formulas. */}
      <section className={`${styles.grid} ${styles.formulas}`} data-tone="light">
        <h2 className={styles.statement} data-rise>
          {copy(formulasLine)}
        </h2>
        <dl className={styles.team} data-rise>
          <div>
            <dt>{copy(liu.name)}</dt>
            <dd>{copy(liu.role)}</dd>
          </div>
          <div>
            <dt>{copy(iris.name)}</dt>
            <dd>
              {copy(iris.role)}. {copy(iris.text)}
            </dd>
          </div>
        </dl>
        {/* NuriCell alone on a pale studio sweep, lit from the upper left, standing on a soft
            reflection; the other four in a quieter row on the same sweep below. */}
        <div className={styles.studio} data-studio data-rise>
          <figure className={styles.nuri}>
            <div className={styles.lightPool} aria-hidden="true" />
            <div className={`${styles.bottle} ${styles.heroBottle}`}>
              <Image
                src={formulas[0].image}
                alt={copy("{name} bottle", { name: formulas[0].name })}
                fill
                sizes="(max-width: 900px) 60vw, 320px"
              />
              <span className={styles.reflection} aria-hidden="true">
                <Image src={formulas[0].image} alt="" fill sizes="(max-width: 900px) 60vw, 320px" />
              </span>
            </div>
            <figcaption className={styles.nuriWords}>
              <strong className={styles.nuriName}>{formulas[0].name}</strong>
              {/* Approved September 21, 2026 (homepage NuriCell introduction). */}
              <span className={styles.nuriLine}>
                {copy(
                  "Our flagship supplement focuses on the health of your mitochondria—the tiny power plants that supply energy for your brain and body.",
                )}
              </span>
              <span className={styles.nuriCredit}>{copy(formulas[0].credit)}</span>
            </figcaption>
          </figure>
        </div>
        <div className={styles.shelf} data-rise>
          {formulas.slice(1).map((formula) => (
            <figure key={formula.name} className={styles.formula}>
              <div className={styles.tile}>
                <div className={styles.bottle}>
                  <Image
                    src={formula.image}
                    alt={copy("{name} bottle", { name: formula.name })}
                    fill
                    sizes="(max-width: 900px) 40vw, 200px"
                  />
                  <span className={styles.reflection} aria-hidden="true">
                    <Image src={formula.image} alt="" fill sizes="(max-width: 900px) 40vw, 200px" />
                  </span>
                </div>
              </div>
              <figcaption className={styles.credit}>
                <strong>{formula.name}</strong>
                <span>{copy(formula.credit)}</span>
              </figcaption>
            </figure>
          ))}
        </div>
      </section>

      {/* 6. The research. */}
      <section id="research" className={`${styles.grid} ${styles.research}`} data-tone="light">
        <h2 className={styles.statement} data-rise>
          {copy(research.title)}
        </h2>
        <p className={`${styles.bodyText} ${styles.researchText}`} data-rise>
          {copy(research.text)}
        </p>
        <ol className={styles.studies}>
          {key.map((item, index) => (
            <li key={item.url} className={styles.study} data-rise>
              <span className={styles.studyIndex} aria-hidden="true">
                {pad(index)}
              </span>
              <div className={styles.studyMain}>
                <p className={styles.studyMeta}>
                  {copy(item.category)}
                  {research.byLiu.includes(item.url) && (
                    <span className={styles.studyTag}>{copy(research.tag)}</span>
                  )}
                </p>
                <h3 className={styles.studyTitle}>{copy(item.title)}</h3>
                <p className={styles.studyText}>{copy(item.text)}</p>
              </div>
              <div className={styles.studySource}>
                <p>
                  <span className={styles.journal}>{item.journal}</span>
                  <span className={styles.year}>{copy(item.year)}</span>
                </p>
                <a href={item.url} target="_blank" rel="noreferrer" className={styles.source}>
                  {copy("Read original source")} <ArrowUpRight size={16} aria-hidden="true" />
                </a>
              </div>
            </li>
          ))}
        </ol>
        <button
          type="button"
          className={styles.more}
          aria-expanded={all}
          onClick={() => setAll(!all)}
        >
          <span>
            {/* A string without a catalog key comes back as written, so fill {count} here too. */}
            {all
              ? copy(research.hideAll)
              : copy(research.seeAll, { count: researchItems.length }).replace(
                  "{count}",
                  String(researchItems.length),
                )}
          </span>
          {all ? <Minus size={22} aria-hidden="true" /> : <Plus size={22} aria-hidden="true" />}
        </button>
        {all && (
          <div className={styles.library}>
            <ResearchGroups everything />
          </div>
        )}
        <p className={styles.note}>{copy(research.note)}</p>
      </section>

      {/* 7. Health explained. */}
      <section id="health" className={`${styles.grid} ${styles.health}`} data-tone="light">
        <h2 className={styles.statement} data-rise>
          {copy(health.title)}
        </h2>
        <p className={`${styles.bodyText} ${styles.healthText}`} data-rise>
          {copy(health.text)}
        </p>
        <div className={styles.doors} data-doors>
          {health.doors.map((door, index) => (
            <article key={door.title} className={styles.door} data-door>
              <p className={styles.doorTopic}>
                <span aria-hidden="true">{pad(index)}</span>
                {copy(door.topic)}
              </p>
              <div className={styles.doorWords}>
                <h3 className={styles.doorTitle}>{copy(door.title)}</h3>
                <p className={styles.doorPreview}>{copy(door.preview)}</p>
                <p className={styles.soon}>{copy(health.soon)}</p>
              </div>
              <div className={styles.doorMedia}>
                <span className={styles.doorLight} aria-hidden="true" />
                <Image
                  src={door.image}
                  alt={copy(HEALTH_ALT[index])}
                  fill
                  sizes="(max-width: 900px) 90vw, 540px"
                  className={index === 1 ? styles.droplet : styles.cell}
                />
              </div>
            </article>
          ))}
        </div>
        <p className={styles.caption}>{copy("Illustrations") /* DRAFT */}</p>
      </section>

      {/* 8. Ask BiGH Science. */}
      <section id="ask" className={styles.ask} data-tone="dark">
        <canvas className={styles.askLight} data-ask-light aria-hidden="true" />
        <span className={styles.askShade} aria-hidden="true" />
        <div className={`${styles.grid} ${styles.askGrid}`}>
          <h2 className={styles.askTitle} data-rise>
            {copy(ask.title)}
          </h2>
          <div className={styles.askIntro} data-rise>
            <p className={styles.askLead}>{copy(ask.lead)}</p>
            <p className={styles.askText}>{copy(ask.text)}</p>
          </div>
          <div className={styles.examples} data-rise>
            <p className={styles.examplesLabel}>{copy(ask.examplesLabel)}</p>
            <ul>
              {ask.examples.map((example) => (
                <li key={example}>{copy(example)}</li>
              ))}
            </ul>
          </div>
          <ol className={styles.steps}>
            {ask.steps.map((step, index) => (
              <li key={step} data-rise>
                <span className={styles.stepIndex} aria-hidden="true">
                  {pad(index)}
                </span>
                <p>{copy(step)}</p>
              </li>
            ))}
          </ol>
          <p className={styles.status} data-rise>
            <strong>{copy(ask.status)}</strong>
            <span>{copy(ask.note)}</span>
          </p>
        </div>
      </section>
    </div>
  );
}
