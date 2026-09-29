"use client";

import Image from "next/image";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ArrowDown, ArrowRight, ArrowUpRight } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useReducedMotion } from "@/components/home/use-reduced-motion";
import { useCopy } from "@/i18n/use-copy";
import { formulas, iris, liu, liuNumbers, opening, pathStops } from "./science-content";
import type { OpeningProps } from "./science-page";
import type { Sky, SkyMode, SkyView } from "./sky-scene";
import styles from "./look-sky.module.css";

// Each star sits a little above or below the middle, so the path reads as a constellation. The
// steps stay small enough that a line never crosses the words under or above a star.
const LIFT = [18, -14, 20, -22, 4];
// The line draws itself up to this point of the screen; a stop lights when the line reaches it.
const HEAD = 0.56;
const PHONE = "(max-width: 900px)";
const PAPERS_AT = pathStops.findIndex((stop) => stop.mark === "2025");
const papers = liuNumbers[0];

// Look E, "Night sky": standing under a clear sky. A real WebGL starfield (sky-scene.ts) stays
// behind the whole opening: the hero words with one warm planet, Dr. Liu's portrait coming into
// focus out of the dark (look A's idea), then his career as a constellation that slides sideways
// (look B's idea). The line draws itself from star to star, and as it goes, new small stars fill
// the sky: an illustration of his papers. Only the one reported number is shown, 280+, at 2025.
// The path ends on the two formulas and Dr. Iris Wang (words only). Phones and reduced motion get
// the same stops top to bottom under a still sky.
export function LookSky({ onStory }: OpeningProps) {
  const copy = useCopy();
  const root = useRef<HTMLElement>(null);
  const holder = useRef<HTMLDivElement>(null);
  const reduced = useReducedMotion();
  const reducedRef = useRef(reduced);
  const skyRef = useRef<Sky | null>(null);
  const pinRef = useRef<ScrollTrigger | null>(null);
  const papersRef = useRef(0);
  const [mode, setMode] = useState<SkyMode | "none">("none");

  useEffect(() => {
    reducedRef.current = reduced;
    skyRef.current?.refresh();
  }, [reduced]);

  // The sky: WebGL loads only here. Without it, the CSS night gradient stays.
  useEffect(() => {
    const element = root.current;
    const frame = holder.current;
    if (!element || !frame) return;
    let disposed = false;
    const phone = window.matchMedia(PHONE);
    const view = (): SkyView => {
      const y = window.scrollY;
      const pin = pinRef.current;
      const track = element.querySelector<HTMLElement>("[data-track]");
      const inside = pin ? Math.min(Math.max(y - pin.start, 0), pin.end - pin.start) : 0;
      const slid = pin && track ? -Number(gsap.getProperty(track, "x")) || 0 : 0;
      return { x: slid, y: y - inside, papers: papersRef.current };
    };
    // The planet's place on the page, from layout offsets (they ignore the words' rise-in motion).
    const placePlanet = () => {
      const anchor = element.querySelector<HTMLElement>("[data-planet]");
      if (!anchor || !skyRef.current) return;
      let x = anchor.offsetWidth / 2;
      let y = anchor.offsetHeight / 2;
      for (
        let node: HTMLElement | null = anchor;
        node;
        node = node.offsetParent as HTMLElement | null
      ) {
        x += node.offsetLeft;
        y += node.offsetTop;
      }
      skyRef.current.setPlanet(x, y);
    };
    const refresh = () => {
      placePlanet();
      skyRef.current?.refresh();
    };
    Promise.all([import("three"), import("./sky-scene")])
      .then(([THREE, { createSky }]) => {
        if (disposed) return;
        try {
          skyRef.current = createSky(THREE, frame, element, {
            view,
            still: () => reducedRef.current || phone.matches,
            onReady: (ready) => setMode(ready),
          });
          placePlanet();
          document.fonts?.ready.then(() => {
            if (!disposed) placePlanet();
          });
        } catch {
          skyRef.current = null;
        }
      })
      .catch(() => undefined);
    phone.addEventListener("change", refresh);
    window.addEventListener("resize", placePlanet);
    return () => {
      disposed = true;
      phone.removeEventListener("change", refresh);
      window.removeEventListener("resize", placePlanet);
      skyRef.current?.dispose();
      skyRef.current = null;
    };
  }, []);

  useEffect(() => {
    const element = root.current;
    if (!element) return;
    gsap.registerPlugin(ScrollTrigger);
    const media = gsap.matchMedia();
    media.add(
      { motion: "(prefers-reduced-motion: no-preference)", wide: "(min-width: 901px)" },
      (context) => {
        const { motion, wide } = context.conditions ?? {};
        if (!motion) return;

        gsap.from("[data-rise]", {
          y: 28,
          opacity: 0,
          duration: 1.5,
          ease: "power3.out",
          stagger: 0.16,
          delay: 0.35,
        });
        // Dr. Liu comes into focus out of the dark as his portrait rises into place (the whole
        // frame: nothing on his face changes but focus and light).
        gsap.fromTo(
          "[data-photo]",
          { filter: "blur(16px) brightness(0.3)", scale: 1.08 },
          {
            filter: "blur(0px) brightness(1)",
            scale: 1,
            ease: "none",
            scrollTrigger: {
              trigger: "[data-frame]",
              start: "top bottom",
              end: "top 55%",
              scrub: 0.6,
            },
          },
        );
        gsap.from("[data-intro] > *", {
          y: 26,
          opacity: 0,
          duration: 1,
          ease: "power2.out",
          stagger: 0.09,
          scrollTrigger: { trigger: "[data-intro]", start: "top 84%" },
        });
        if (!wide) return;

        // The constellation: pinned, it slides sideways; the line draws itself from star to star.
        const journey = element.querySelector<HTMLElement>("[data-journey]");
        const track = element.querySelector<HTMLElement>("[data-track]");
        const clip = element.querySelector<HTMLElement>("[data-lit-line]");
        const pen = element.querySelector<HTMLElement>("[data-pen]");
        const together = element.querySelector<HTMLElement>("[data-together]");
        const stops = [...element.querySelectorAll<HTMLElement>("[data-stop]")];
        if (!journey || !track || !clip || !pen || !together) return;
        let stars: { x: number; y: number }[] = [];
        let width = 0;

        const measure = () => {
          const box = track.getBoundingClientRect();
          width = track.scrollWidth;
          stars = stops.map((stop) => {
            const star = stop.querySelector<HTMLElement>("[data-star]");
            const at = star ? star.getBoundingClientRect() : box;
            return { x: at.left - box.left + at.width / 2, y: at.top - box.top + at.height / 2 };
          });
          const d = `M${stars.map((p) => `${p.x.toFixed(1)} ${p.y.toFixed(1)}`).join(" L")}`;
          element.querySelectorAll<SVGSVGElement>("[data-lines]").forEach((svg) => {
            svg.setAttribute("viewBox", `0 0 ${width} ${track.offsetHeight}`);
            svg.style.width = `${width}px`;
            svg.style.height = `${track.offsetHeight}px`;
            svg.querySelector("path")?.setAttribute("d", d);
          });
        };

        const update = () => {
          if (!stars.length) return;
          const head = -Number(gsap.getProperty(track, "x")) + journey.clientWidth * HEAD;
          clip.style.clipPath = `inset(0 ${Math.max(0, width - head).toFixed(1)}px 0 0)`;
          stops.forEach((stop, index) => {
            if (head >= stars[index].x - 1) stop.dataset.lit = "true";
            else delete stop.dataset.lit;
          });
          if (head >= together.offsetLeft + 40) together.dataset.lit = "true";
          else delete together.dataset.lit;
          const first = stars[0];
          const last = stars[stars.length - 1];
          let y = first.y;
          for (let i = 0; i < stars.length - 1; i += 1) {
            if (head >= stars[i].x && head <= stars[i + 1].x) {
              const share = (head - stars[i].x) / (stars[i + 1].x - stars[i].x);
              y = stars[i].y + (stars[i + 1].y - stars[i].y) * share;
            }
          }
          pen.style.opacity = head > first.x && head < last.x ? "1" : "0";
          pen.style.transform = `translate(${head.toFixed(1)}px, ${y.toFixed(1)}px)`;
          const end = stars[PAPERS_AT].x;
          const share = Math.min(1, Math.max(0, (head - first.x) / (end - first.x)));
          papersRef.current = share;
          element.dataset.papers = share.toFixed(3);
        };

        const distance = () => Math.max(0, track.scrollWidth - journey.clientWidth);
        gsap.to(track, {
          x: () => -distance(),
          ease: "none",
          onUpdate: update,
          scrollTrigger: {
            trigger: journey,
            start: "top top",
            end: () => `+=${distance()}`,
            pin: true,
            scrub: 0.9,
            invalidateOnRefresh: true,
            onRefresh: (self) => {
              pinRef.current = self;
              measure();
              update();
            },
          },
        });
        measure();
        update();
        return () => {
          pinRef.current = null;
          papersRef.current = 0;
          delete element.dataset.papers;
          stops.forEach((stop) => delete stop.dataset.lit);
          delete together.dataset.lit;
          clip.style.clipPath = "";
          pen.style.transform = "";
          pen.style.opacity = "";
        };
      },
      element,
    );
    return () => media.revert();
  }, []);

  return (
    <section id="scientists" ref={root} className={styles.sky} data-tone="dark" data-sky={mode}>
      {/* The sky's own layer spans the section; the sky sticks to the screen inside it. */}
      <div className={styles.heavensTrack} aria-hidden="true">
        <div ref={holder} className={styles.heavens} />
      </div>

      <div className={styles.hero}>
        <p className={styles.eyebrow} data-rise>
          {copy(opening.eyebrow)}
        </p>
        <h1 className={styles.title}>
          <span className={styles.titleLead} data-rise>
            {copy(opening.titleLead)}
            <span className={styles.planet} data-planet aria-hidden="true" />
          </span>{" "}
          <span className={styles.accent} data-rise>
            {copy(opening.titleAccent)}
          </span>
        </h1>
        <a href="#dr-liu" className={styles.cue} data-rise>
          <span>{copy(liu.name)}</span>
          <ArrowDown size={20} aria-hidden="true" />
        </a>
      </div>

      <div id="dr-liu" className={styles.portrait}>
        <figure className={styles.frame} data-frame>
          <Image
            src={liu.photo.src}
            alt={copy(liu.name)}
            fill
            sizes="(max-width: 900px) 78vw, 440px"
            className={styles.photo}
            data-photo
          />
        </figure>
        <div className={styles.intro} data-intro>
          <p className={styles.eyebrow}>{copy(liu.role)}</p>
          <h2 className={styles.name}>{copy(liu.name)}</h2>
          <p className={styles.statement}>{copy(liu.headline)}</p>
          <p className={styles.body}>{copy(liu.intro)}</p>
          <button type="button" className={styles.storyButton} onClick={onStory}>
            {copy(liu.button)} <ArrowRight size={20} aria-hidden="true" />
          </button>
        </div>
      </div>

      <div className={styles.journey} data-journey>
        <div className={styles.track} data-track>
          <svg className={styles.guide} data-lines aria-hidden="true">
            <path />
          </svg>
          <div className={styles.litLine} data-lit-line aria-hidden="true">
            <svg data-lines>
              <path />
            </svg>
          </div>
          <span className={styles.pen} data-pen aria-hidden="true" />

          <div className={styles.leadIn}>
            <div className={styles.leadTop}>
              <p className={styles.eyebrow}>{copy("His path")}</p>
              <h2 className={styles.leadTitle}>{copy("A life in cell science.")}</h2>
            </div>
            {/* DRAFT: the sky's new stars are an illustration of his papers, not a count. */}
            <p className={styles.hint}>
              {copy("As you go, his papers fill the sky.")}{" "}
              <ArrowRight size={18} aria-hidden="true" />
            </p>
          </div>

          {pathStops.map((stop, index) => (
            <article
              key={stop.mark}
              className={styles.stop}
              style={{ "--dy": `${LIFT[index] ?? 0}px` } as React.CSSProperties}
              data-stop
            >
              <p className={styles.mark}>{copy(stop.mark)}</p>
              <span className={styles.star} data-star aria-hidden="true" />
              <div className={styles.below}>
                <h3 className={styles.stopTitle}>{copy(stop.title)}</h3>
                <p className={styles.stopText}>{copy(stop.text)}</p>
                {index === PAPERS_AT && (
                  <p className={styles.papers} data-papers-label>
                    <span className={styles.papersValue}>
                      {papers.value}
                      {papers.suffix}
                    </span>
                    <span className={styles.papersLabel}>{copy(papers.label)}</span>
                  </p>
                )}
                {stop.url && (
                  <a href={stop.url} target="_blank" rel="noreferrer" className={styles.source}>
                    {copy(stop.link)} <ArrowUpRight size={16} aria-hidden="true" />
                  </a>
                )}
              </div>
            </article>
          ))}

          <div className={styles.together} data-together>
            {formulas.map((formula) => (
              <figure key={formula.name} className={styles.formula}>
                <div className={styles.bottle}>
                  <Image
                    src={formula.image}
                    alt={copy("{name} bottle", { name: formula.name })}
                    fill
                    sizes="(max-width: 900px) 42vw, 200px"
                  />
                </div>
                <figcaption>
                  <strong>{formula.name}</strong>
                  <span>{copy(formula.credit)}</span>
                </figcaption>
              </figure>
            ))}
            <div className={styles.iris}>
              <p className={styles.eyebrow}>{copy(iris.role)}</p>
              <h3 className={styles.irisName}>{copy(iris.name)}</h3>
              <p className={styles.irisText}>{copy(iris.text)}</p>
            </div>
          </div>
        </div>
      </div>
      <div className={styles.horizon} aria-hidden="true" />
    </section>
  );
}
