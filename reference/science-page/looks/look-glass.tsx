"use client";

import Image from "next/image";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ArrowDown, ArrowRight, ArrowUpRight } from "lucide-react";
import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { useReducedMotion } from "@/components/home/use-reduced-motion";
import { useCopy } from "@/i18n/use-copy";
import type { GlassCell } from "./glass-scene";
import { formulas, iris, liu, opening, pathStops } from "./science-content";
import type { OpeningProps } from "./science-page";
import styles from "./look-glass.module.css";

// The still render's object spans this share of the picture's width (x 375 to 1550 of 1920). The live
// cell is framed to the same width, so the still turns into the live one without a jump.
const STILL_SHARE = 1175 / 1920;
// Each stop sits a little above or below the line and a little nearer or farther (desktop path).
const DEPTHS = [
  { lift: -64, depth: "far" },
  { lift: 56, depth: "near" },
  { lift: -36, depth: "far" },
  { lift: 70, depth: "near" },
];
const stops = pathStops.slice(0, -1);
const today = pathStops[pathStops.length - 1];

// Look F, "Glass": the brand's glass mitochondrion, live in three.js, on a pearl page with iridescent
// light. Dr. Liu's portrait comes into focus through a frosted pane (look A's portrait), then his
// career runs sideways on frosted glass cards (look B's path) and ends on the two formulas standing on
// glass plinths, with Dr. Iris Wang in words. Without WebGL, with reduced motion or while loading, the
// still render sits in the same place, its white ground multiplied into the pearl page.
export function LookGlass({ onStory }: OpeningProps) {
  const copy = useCopy();
  const reduced = useReducedMotion();
  const root = useRef<HTMLElement>(null);
  const hero = useRef<HTMLDivElement>(null);
  const still = useRef<HTMLImageElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  const lineA = useRef<HTMLSpanElement>(null);
  const lineB = useRef<HTMLSpanElement>(null);
  const [live, setLive] = useState(false);

  // Center the cell in the gap between the headline's two lines.
  useLayoutEffect(() => {
    const element = hero.current;
    const top = lineA.current;
    const bottom = lineB.current;
    if (!element || !top || !bottom) return;
    const place = () => {
      // Layout positions (offsetTop), so the lines' scroll drift does not move the cell.
      let a = top.offsetTop + top.offsetHeight;
      let b = bottom.offsetTop;
      for (let node = top.offsetParent as HTMLElement | null; node && node !== element; ) {
        a += node.offsetTop;
        b += node.offsetTop;
        node = node.offsetParent as HTMLElement | null;
      }
      element.style.setProperty("--cy", `${Math.round((a + b) / 2)}px`);
    };
    place();
    const observer = new ResizeObserver(place);
    observer.observe(element);
    observer.observe(top);
    return () => observer.disconnect();
  }, []);

  // The live glass cell.
  useEffect(() => {
    const element = hero.current;
    const surface = canvas.current;
    const picture = still.current;
    if (!element || !surface || !picture || reduced) return;
    let cell: GlassCell | null = null;
    let disposed = false;
    import("./glass-scene")
      .then(({ mountGlassCell }) =>
        mountGlassCell(surface, {
          objectWidth: () => picture.offsetWidth * STILL_SHARE,
          onReady: () => {
            if (!disposed) setLive(true);
          },
        }),
      )
      .then((made) => {
        if (disposed) made?.dispose();
        else if (made) {
          cell = made;
          // For the QA script: frames drawn and the GPU in use.
          (surface as HTMLCanvasElement & { glassStats?: unknown }).glassStats = made.stats;
        }
      })
      .catch(() => undefined);

    const onPointer = (event: PointerEvent) => {
      cell?.setPointer(
        (event.clientX / window.innerWidth) * 2 - 1,
        (event.clientY / window.innerHeight) * 2 - 1,
      );
    };
    window.addEventListener("pointermove", onPointer, { passive: true });
    gsap.registerPlugin(ScrollTrigger);
    const turn = ScrollTrigger.create({
      trigger: element,
      start: "top top",
      end: "bottom top",
      onUpdate: (self) => cell?.setScroll(self.progress),
    });
    return () => {
      disposed = true;
      window.removeEventListener("pointermove", onPointer);
      turn.kill();
      cell?.dispose();
      setLive(false);
    };
  }, [reduced]);

  // Scroll scenes.
  useEffect(() => {
    const element = root.current;
    if (!element) return;
    gsap.registerPlugin(ScrollTrigger);
    const media = gsap.matchMedia();

    media.add("(prefers-reduced-motion: no-preference)", () => {
      // The headline rises in once; the cell drifts up and the lines part as the page scrolls.
      gsap.from("[data-rise]", {
        y: 30,
        opacity: 0,
        duration: 1.2,
        ease: "power3.out",
        stagger: 0.12,
        delay: 0.1,
      });
      const heroScroll = {
        trigger: "[data-hero]",
        start: "top top",
        end: "bottom top",
        scrub: 0.6,
      };
      gsap.to("[data-visual]", {
        yPercent: -10,
        scale: 0.94,
        ease: "none",
        scrollTrigger: heroScroll,
      });
      gsap.to("[data-line-a]", { y: -50, ease: "none", scrollTrigger: heroScroll });
      gsap.to("[data-line-b]", { y: 40, ease: "none", scrollTrigger: heroScroll });

      // The portrait comes into focus through the glass: the pane is frosted while the photograph is
      // low on the screen and clears as it settles, so he is never left blurred while someone reads.
      const settle = {
        trigger: "[data-portrait]",
        start: "top 100%",
        end: "center 74%",
        scrub: 0.5,
      };
      const pane = element.querySelector<HTMLElement>("[data-pane]");
      if (pane) {
        gsap.set(pane, { "--frost": "22px", "--tint": 0.4, "--edge": "40deg" });
        gsap.to(pane, {
          "--frost": "0px",
          "--tint": 0,
          "--edge": "250deg",
          ease: "none",
          scrollTrigger: settle,
        });
      }
      gsap.set("[data-photo]", { scale: 1.08 });
      gsap.to("[data-photo]", { scale: 1, ease: "none", scrollTrigger: settle });
      gsap.from("[data-liu-copy] > *", {
        y: 26,
        opacity: 0,
        duration: 0.9,
        ease: "power2.out",
        stagger: 0.08,
        scrollTrigger: { trigger: "[data-liu-copy]", start: "top 82%" },
      });
    });

    // Wide screens: the path is pinned and slides sideways under a gold line that fills.
    media.add("(min-width: 901px) and (prefers-reduced-motion: no-preference)", () => {
      const journey = element.querySelector<HTMLElement>("[data-journey]");
      const track = element.querySelector<HTMLElement>("[data-track]");
      const fill = element.querySelector<HTMLElement>("[data-fill]");
      const light = element.querySelector<HTMLElement>("[data-journey-light]");
      if (!journey || !track || !fill) return;
      const distance = () => Math.max(0, track.scrollWidth - journey.clientWidth);
      // The fill's end starts just past the middle of the screen and reaches the path's end with the
      // last scroll, so the whole line is gold when the formulas arrive.
      const reach = (progress: number) =>
        Math.min(
          1,
          (progress * distance() + journey.clientWidth * (0.58 + 0.42 * progress)) /
            track.scrollWidth,
        );
      const pin = {
        trigger: journey,
        start: "top top",
        end: () => `+=${distance()}`,
        scrub: 0.8,
        invalidateOnRefresh: true,
      };
      const slide = gsap.to(track, {
        x: () => -distance(),
        ease: "none",
        scrollTrigger: {
          ...pin,
          pin: true,
          onUpdate: (self) => gsap.set(fill, { scaleX: reach(self.progress) }),
          onRefresh: (self) => gsap.set(fill, { scaleX: reach(self.progress) }),
        },
      });
      // The light behind the glass moves slower than the cards: depth.
      if (light) {
        gsap.to(light, { x: () => -distance() * 0.35, ease: "none", scrollTrigger: pin });
      }
      element.querySelectorAll<HTMLElement>("[data-stop]").forEach((stop) => {
        const near = stop.dataset.depth === "near";
        gsap.set(stop, { x: near ? 60 : 24 });
        gsap.to(stop, {
          x: near ? -60 : -24,
          ease: "none",
          scrollTrigger: {
            trigger: stop,
            containerAnimation: slide,
            start: "left right",
            end: "right left",
            scrub: true,
          },
        });
        ScrollTrigger.create({
          trigger: stop,
          containerAnimation: slide,
          start: "left 58%",
          onEnter: () => (stop.dataset.lit = "true"),
          onLeaveBack: () => delete stop.dataset.lit,
        });
      });
    });

    // Phones: the same path top to bottom; the line fills as you read down.
    media.add("(max-width: 900px) and (prefers-reduced-motion: no-preference)", () => {
      gsap.set("[data-fill]", { scaleY: 0 });
      gsap.to("[data-fill]", {
        scaleY: 1,
        ease: "none",
        scrollTrigger: {
          trigger: "[data-track]",
          start: "top 70%",
          end: "bottom 70%",
          scrub: 0.5,
        },
      });
      element.querySelectorAll<HTMLElement>("[data-stop]").forEach((stop) => {
        ScrollTrigger.create({
          trigger: stop,
          start: "top 72%",
          onEnter: () => (stop.dataset.lit = "true"),
          onLeaveBack: () => delete stop.dataset.lit,
        });
      });
    });

    return () => media.revert();
  }, []);

  return (
    <section
      id="scientists"
      ref={root}
      className={styles.glass}
      data-tone="light"
      data-live={live || undefined}
    >
      {/* 1. The glass cell between the headline's two lines. */}
      <div className={styles.hero} ref={hero} data-hero>
        <div className={styles.aura} aria-hidden="true">
          <span />
          <span />
          <span />
        </div>
        <Image
          ref={still}
          src="/images/science/glass-cell.webp"
          alt=""
          width={1920}
          height={1086}
          priority
          sizes="(max-width: 700px) 150vw, min(94vw, 1560px)"
          className={styles.still}
          data-visual
        />
        <span className={styles.shadow} aria-hidden="true" data-visual />
        <canvas
          ref={canvas}
          className={styles.canvas}
          aria-hidden="true"
          data-visual
          data-glass-canvas
        />
        <div className={styles.heroCopy}>
          <p className={styles.eyebrow} data-rise>
            {copy(opening.eyebrow)}
          </p>
          <h1 className={styles.title}>
            <span className={styles.lineA} ref={lineA} data-line-a>
              <span data-rise>{copy(opening.titleLead)}</span>
            </span>{" "}
            <span className={styles.lineB} ref={lineB} data-line-b>
              <span data-rise>{copy(opening.titleAccent)}</span>
            </span>
          </h1>
        </div>
        <p className={styles.label}>{copy("Illustration")}</p>
        <a href="#dr-liu" className={styles.cue} aria-label={copy(liu.name)}>
          <ArrowDown size={20} />
        </a>
      </div>

      {/* 2. Dr. Liu, in focus through a frosted glass pane. */}
      <div id="dr-liu" className={styles.liu}>
        <div className={styles.portrait} data-portrait>
          <div className={styles.photo}>
            <Image
              src={liu.photo.src}
              alt={copy(liu.name)}
              fill
              loading="eager"
              sizes="(max-width: 900px) 78vw, 460px"
              data-photo
            />
          </div>
          <div className={styles.pane} aria-hidden="true" data-pane />
        </div>
        <div className={styles.liuCopy} data-liu-copy>
          <p className={styles.eyebrow}>{copy(liu.role)}</p>
          <h2 className={styles.name}>{copy(liu.name)}</h2>
          <p className={styles.statement}>{copy(liu.headline)}</p>
          <p className={styles.body}>{copy(liu.intro)}</p>
          <button type="button" className={styles.storyButton} onClick={onStory}>
            {copy(liu.button)} <ArrowRight size={20} />
          </button>
        </div>
      </div>

      {/* 3. His path on glass, ending on the two formulas. */}
      <div className={styles.journey} data-journey>
        <div className={styles.journeyLight} aria-hidden="true" data-journey-light />
        <div className={styles.track} data-track>
          <div className={styles.line} aria-hidden="true">
            <div className={styles.fill} data-fill />
          </div>
          <div className={styles.lead}>
            <div className={styles.leadTop}>
              <p className={styles.eyebrow}>{copy("His path")}</p>
              <h2 className={styles.leadTitle}>{copy("A life in cell science.")}</h2>
            </div>
            <p className={styles.hint}>
              {copy("Scroll to follow it")} <ArrowRight size={18} />
            </p>
          </div>
          {stops.map((stop, index) => {
            const place = DEPTHS[index % DEPTHS.length];
            return (
              <article
                key={stop.mark}
                className={styles.stop}
                data-stop
                data-depth={place.depth}
                style={{ "--lift": `${place.lift}px` } as React.CSSProperties}
              >
                <div className={styles.card}>
                  <p className={styles.mark}>{copy(stop.mark)}</p>
                  <h3 className={styles.stopTitle}>{copy(stop.title)}</h3>
                  <p className={styles.stopText}>{copy(stop.text)}</p>
                  {stop.url && (
                    <a href={stop.url} target="_blank" rel="noreferrer" className={styles.source}>
                      {copy(stop.link)} <ArrowUpRight size={16} />
                    </a>
                  )}
                </div>
              </article>
            );
          })}
          <div className={styles.finale} data-stop data-depth="near">
            <article className={`${styles.card} ${styles.todayCard}`}>
              <p className={styles.mark}>{copy(today.mark)}</p>
              <h3 className={styles.stopTitle}>{copy(today.title)}</h3>
              <p className={styles.stopText}>{copy(today.text)}</p>
            </article>
            <div className={styles.formulas}>
              {formulas.map((formula) => (
                <figure key={formula.name} className={styles.formula}>
                  <div className={styles.stand}>
                    <div className={styles.plinth} aria-hidden="true" />
                    <div className={styles.reflection} aria-hidden="true">
                      <Image
                        src={formula.image}
                        alt=""
                        fill
                        sizes="(max-width: 900px) 40vw, 240px"
                      />
                    </div>
                    <div className={styles.bottle}>
                      <Image
                        src={formula.image}
                        alt={copy("{name} bottle", { name: formula.name })}
                        fill
                        sizes="(max-width: 900px) 40vw, 240px"
                      />
                    </div>
                  </div>
                  <figcaption>
                    <strong>{formula.name}</strong>
                    <span>{copy(formula.credit)}</span>
                  </figcaption>
                </figure>
              ))}
            </div>
            <article className={`${styles.card} ${styles.irisCard}`}>
              <p className={styles.eyebrow}>{copy(iris.role)}</p>
              <h3 className={styles.irisName}>{copy(iris.name)}</h3>
              <p className={styles.stopText}>{copy(iris.text)}</p>
            </article>
          </div>
        </div>
      </div>
    </section>
  );
}
