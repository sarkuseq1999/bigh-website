"use client";

import Image from "next/image";
import { useEffect, useRef, useState } from "react";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { useReducedMotion } from "@/components/home/use-reduced-motion";
import { about, drafts, media, routes } from "./about-content";
import type { LookProps } from "./about-page";
import { Acronym } from "./acronym";
import { CountUp } from "./count-up";
import { Greetings } from "./greetings";
import type { BatteryScene } from "./look-glass-scene";
import styles from "./look-glass.module.css";

// The About page's body, "Glass" (Mo's pick, Sept 28, 2026), after Timeline's cellular battery
// with its small fact list. The approved glass mitochondrion (the cell's battery) is drawn live by
// a shader (look-glass-scene.ts). It opens set in the name like a word ("Be in Good / Health."
// and the glass), then docks at the top of the window and stays there while the chapters pass
// beneath it, one idea per screen. Chapter by chapter it fills with golden light, and each
// chapter's number joins the spec list beside it as the chapter slides away. At the close the
// battery is full and the list complete.
//
// The system: Switzer for everything (as on main), graphite ink on warm paper, and one accent, the
// render's own honey, used only where something fills (the promise bars). Everything sits on a
// 12-column grid that lines up with the header. Desktop: each chapter holds still in the band
// under the battery while you read it, then slides up under the battery's paper. Phone: the name
// on top and the glass under it, then the same chapters in one column, without the hold.
// Reduced motion or no WebGL: the still render, and the page in plain order.

// Where the battery's charge stands when each chapter holds in the band.
const CHARGE = [0.22, 0.36, 0.52, 0.68, 0.85, 1];
// The still (before the shader is ready, without WebGL, with reduced motion): the same approved
// render with its white ground already turned to transparency, so it sits in the paper as the
// shader's picture does, and its soft shadow lifted to sit just under the glass, as the shader
// lifts it (reference/about/originals/glass-battery-lifted.json).
const STILL = "/images/about/glass-battery-lifted.webp";

// Where the glass sits in the render (1600 x 905 still, 1920 x 1086 shader picture): x 19.4-80.7%
// of its width, y 22.8-73% of its height; the render's height is 0.5656 of its width.
const GLASS = { left: 0.194, width: 0.613, top: 0.228, height: 0.502, aspect: 0.5656 };
// The glass's height over its width, and the footprint (glass, lifted shadow and caption) under
// its top, in glass widths.
const GLASS_RATIO = (GLASS.height * GLASS.aspect) / GLASS.width;
const FOOTPRINT = 0.56;

type Fact = { id: string; value: string; label: string };

export function LookGlass({ onAsk }: LookProps) {
  const copy = useCopy();
  const reducedMotion = useReducedMotion();
  const root = useRef<HTMLDivElement>(null);
  const holder = useRef<HTMLDivElement>(null);
  const batteryRef = useRef<HTMLDivElement>(null);
  const [ready, setReady] = useState(false);

  // "45 days to decide." becomes "45 days" beside "to decide." in the spec list.
  const refund = copy(about.promise.items[2].title);
  const split = /^(\d+\s+\S+)\s+(.+)$/.exec(refund);
  const facts: Fact[] = [
    { id: "papers", value: about.roots.stat.value, label: copy(about.roots.stat.label) },
    {
      id: "founded",
      value: about.experience.stats[0].value,
      label: copy(about.experience.stats[0].label),
    },
    {
      id: "formula",
      value: `${about.experience.stats[1].value} ${copy(about.experience.stats[1].unit)}`,
      label: copy(about.experience.stats[1].label),
    },
    { id: "refund", value: split ? split[1] : "45", label: split ? split[2] : refund },
  ];

  // The glass battery: WebGL loads only with motion allowed; until then (and on failure) the
  // still render shows.
  const scene = useRef<BatteryScene | null>(null);
  useEffect(() => {
    const element = holder.current;
    if (!element || reducedMotion || !canDrawWebGL()) return;
    let disposed = false;
    import("./look-glass-scene")
      .then(async ({ createBatteryScene }) => {
        const THREE = await import("three");
        if (disposed) return;
        try {
          scene.current = createBatteryScene(THREE, element, {
            canvasClass: styles.canvas,
            image: media.mitochondrion,
            depth: media.mitochondrionDepth,
            onReady: () => {
              if (!disposed) setReady(true);
            },
          });
          root.current?.setAttribute("data-renderer", scene.current.software ? "software" : "gpu");
          root.current?.dispatchEvent(new Event("glass:wake"));
        } catch {
          scene.current = null;
        }
      })
      .catch(() => undefined);
    return () => {
      disposed = true;
      scene.current?.dispose();
      scene.current = null;
      setReady(false);
    };
  }, [reducedMotion]);

  // Where the glass opens: on desktop, set in the name like a word: as tall as the capitals, on
  // the baseline of "Health.", one word space after it; on phones and tablets, fitted into the
  // slot under the lead. Measured from the real font, never guessed, so it holds in every window;
  // written as --open-x, --open-y and --open-s, which the battery's transform blends into its dock
  // as it rises. Runs with reduced motion too (it is layout).
  useEffect(() => {
    const element = root.current;
    const battery = batteryRef.current;
    if (!element || !battery) return;
    let frame = 0;
    function place() {
      frame = 0;
      const box = openingGlass(element!);
      const stage = battery!.parentElement;
      if (!box || !stage) return;
      const origin = element!.getBoundingClientRect().top + window.scrollY;
      const width = battery!.offsetWidth;
      const scale = box.width / (GLASS.width * width);
      const stageBox = stage.getBoundingClientRect();
      const centerX = box.left + box.width / 2 - (stageBox.left + stage.clientWidth / 2);
      // The transform turns about the render's point at 47.6% of its height; the glass's middle
      // sits at 47.9%.
      const anchor =
        battery!.offsetTop + (GLASS.top + GLASS.height / 2 - 0.476) * battery!.offsetHeight * scale;
      const centerY = box.top - origin + (box.width * GLASS_RATIO) / 2 - anchor;
      element!.style.setProperty("--open-x", `${centerX.toFixed(1)}px`);
      element!.style.setProperty("--open-y", `${centerY.toFixed(1)}px`);
      element!.style.setProperty("--open-s", scale.toFixed(4));
      element!.dataset.placed = "true";
    }
    const queue = () => {
      if (!frame) frame = requestAnimationFrame(place);
    };
    place();
    // Also when the slot or the title change size, and whenever a font finishes loading (Switzer
    // arrives from Fontshare's stylesheet, possibly after the first paint).
    const resize = new ResizeObserver(queue);
    resize.observe(element);
    element.querySelectorAll("[data-slot], h1").forEach((target) => resize.observe(target));
    window.addEventListener("resize", queue);
    document.fonts?.addEventListener("loadingdone", queue);
    document.fonts?.ready.then(queue).catch(() => undefined);
    return () => {
      cancelAnimationFrame(frame);
      resize.disconnect();
      window.removeEventListener("resize", queue);
      document.fonts?.removeEventListener("loadingdone", queue);
    };
  }, []);

  // The choreography, all from the scroll position. The battery rises from under the title to its
  // dock and charges chapter by chapter. The chapters take turns: each fades in as it rises into
  // the band, holds still while it is read, then fades as it slides up under the battery, and the
  // next one only appears once the last is gone, so two chapters' words never share the window.
  // Between them the battery has the screen to itself for a moment. A chapter's number joins the
  // spec list as the chapter fades, and the promise bars fill while the promise holds. One loop
  // draws it all; it sleeps when nothing moves and while offscreen.
  useEffect(() => {
    const element = root.current;
    if (!element || reducedMotion) return;
    const chapters = [...element.querySelectorAll<HTMLElement>("[data-chapter]")];
    const bars = [...element.querySelectorAll<HTMLElement>("[data-pill]")];
    const factItems = [...element.querySelectorAll<HTMLElement>("[data-fact]")];
    const bandMark = element.querySelector<HTMLElement>("[data-band]");
    const promiseIndex = chapters.findIndex((chapter) => chapter.id === "promise");
    // What fades: the opening's words, or each chapter's frame.
    const faders = chapters.map(
      (chapter) =>
        chapter.querySelector<HTMLElement>("[data-frame]") ??
        chapter.querySelector<HTMLElement>("[data-fade]") ??
        chapter,
    );

    type Plan = {
      holdStart: number;
      holdEnd: number;
      inStart: number;
      inEnd: number;
      outStart: number;
      outEnd: number;
    };
    const always: Plan = {
      holdStart: 0,
      holdEnd: 0,
      inStart: -2,
      inEnd: -1,
      outStart: Infinity,
      outEnd: Infinity,
    };
    let view = window.innerHeight;
    let plans: Plan[] = chapters.map(() => always);
    let marks: number[] = [];
    let riseStart = 0;
    let riseEnd = 1;
    let barTops: number[] = [];
    let factAt: number[] = [];
    const shown = chapters.map(() => "");
    const entered = chapters.map(() => false);

    function measure() {
      view = window.innerHeight;
      const y = window.scrollY;
      // Landscape phones hide the battery: then the chapters simply scroll.
      const staged = Boolean(bandMark && bandMark.offsetParent);
      const band = staged ? bandMark!.offsetTop : 0;
      const bandH = view - band;
      // A chapter taller than the band cannot hold still under the battery; it scrolls instead.
      chapters.forEach((chapter, i) => {
        if (i === 0) return;
        const content = chapter.querySelector<HTMLElement>("[data-frame] > *");
        chapter.dataset.fits = String(staged && (!content || content.offsetHeight + 16 <= bandH));
      });
      plans = chapters.map((chapter, i) => {
        const frame = chapter.querySelector<HTMLElement>("[data-frame]");
        if (i === 0 || !frame || !staged) return always;
        const sticky = getComputedStyle(frame).position === "sticky";
        const holdStart = chapter.getBoundingClientRect().top + y - band;
        const holdEnd = sticky ? holdStart + chapter.offsetHeight - frame.offsetHeight : holdStart;
        const contentH = (frame.firstElementChild as HTMLElement | null)?.offsetHeight ?? 0;
        // Without a hold, it starts to fade once its last line is halfway up the band.
        const outStart = sticky ? holdEnd : Math.max(holdStart, holdStart + contentH - bandH * 0.5);
        return {
          holdStart,
          holdEnd,
          inStart: holdStart - bandH * 0.34,
          inEnd: holdStart - bandH * 0.04,
          outStart,
          outEnd: outStart + bandH * (sticky ? 0.3 : 0.25),
        };
      });
      if (staged && plans.length > 1) {
        // The opening's words are gone before the glass starts to lift away from them.
        const first = plans[1].holdStart;
        plans[0] = { ...always, outStart: first * 0.02, outEnd: first * 0.22 };
        // Never two at once: a chapter starts to appear only once the one before is gone.
        for (let i = 1; i < plans.length; i++) {
          const earliest = plans[i - 1].outEnd + bandH * 0.05;
          const plan = plans[i];
          if (plan.inStart < earliest) {
            plans[i] = {
              ...plan,
              inStart: earliest,
              inEnd: earliest + (plan.inEnd - plan.inStart),
            };
          }
        }
        // The closing ends the page: it never fades.
        plans[plans.length - 1] = {
          ...plans[plans.length - 1],
          outStart: Infinity,
          outEnd: Infinity,
        };
      }
      // The charge reaches each chapter's value in the middle of its hold.
      marks = plans.map((plan, i) => (i === 0 ? 0 : (plan.holdStart + plan.holdEnd) / 2));
      // The battery is docked a little before the first chapter reaches the band.
      // Until then it rides with the page, exactly where the opening set it.
      riseStart = (plans[1]?.holdStart ?? view) * 0.16;
      riseEnd = Math.max(riseStart + 1, (plans[1]?.holdStart ?? view) * 0.82);
      // Phone: the closing is taller than the band, so the battery lets go of the window as soon
      // as the closing (its list first) sits under it; the rest of the page scrolls plainly.
      const closing = chapters[chapters.length - 1];
      const closingFrame = closing.querySelector<HTMLElement>("[data-frame]");
      let cut = 0;
      if (staged && closingFrame && getComputedStyle(closingFrame).position !== "sticky") {
        const lookBottom = element!.getBoundingClientRect().bottom + y;
        const release = closing.getBoundingClientRect().top + y - band + view;
        cut = Math.max(0, lookBottom - release);
      }
      element!.style.setProperty("--track-cut", `${Math.round(cut)}px`);
      barTops = bars.map((bar) => bar.getBoundingClientRect().top + y);
      // A chapter's number joins the spec list halfway through the chapter's fade.
      factAt = factItems.map((fact) => {
        const source = element!.querySelector<HTMLElement>(`[data-source="${fact.dataset.fact}"]`);
        const index = source
          ? chapters.indexOf(source.closest<HTMLElement>("[data-chapter]")!)
          : -1;
        const plan = plans[index];
        if (!plan || !Number.isFinite(plan.outEnd)) return Infinity;
        return (plan.outStart + plan.outEnd) / 2;
      });
    }

    const state = {
      charge: 0,
      rise: 0,
      time: 0,
      tiltX: 0,
      tiltY: 0,
      aimX: 0,
      aimY: 0,
      pulse: 0,
    };
    const docked = factItems.map(() => false);
    const start = performance.now();
    let lastActive = start;
    let lastPointer = -1e9;
    let lastScroll = window.scrollY;
    let lean = 0;
    let frame = 0;
    let last = start;
    let visible = true;
    let written = "";

    function chargeAt(y: number) {
      if (y <= marks[0]) return CHARGE[0];
      for (let i = 1; i < marks.length; i++) {
        if (y <= marks[i]) {
          const t = (y - marks[i - 1]) / Math.max(1, marks[i] - marks[i - 1]);
          return CHARGE[i - 1] + (CHARGE[i] - CHARGE[i - 1]) * t;
        }
      }
      return CHARGE[CHARGE.length - 1];
    }

    function barFill(i: number, y: number) {
      // Held still: the four bars fill one after another while the promise holds.
      const plan = plans[promiseIndex];
      if (plan && plan.holdEnd > plan.holdStart) {
        const p = (y - plan.holdStart) / (plan.holdEnd - plan.holdStart);
        return clamp01((p - i * 0.16) / 0.3);
      }
      // Scrolling: each bar fills as it comes up into the window.
      return clamp01((y + view * 0.84 - barTops[i]) / (view * 0.26));
    }

    function opacityAt(plan: Plan, y: number) {
      const fadeIn = clamp01((y - plan.inStart) / Math.max(1, plan.inEnd - plan.inStart));
      const fadeOut = Number.isFinite(plan.outStart)
        ? 1 - clamp01((y - plan.outStart) / Math.max(1, plan.outEnd - plan.outStart))
        : 1;
      return Math.min(fadeIn, fadeOut);
    }

    function tick(now: number) {
      frame = 0;
      const dt = Math.min((now - last) / 1000, 0.05);
      last = now;
      const y = window.scrollY;

      // Scroll speed leans the glass a little; it settles when the page stops.
      const speed = (y - lastScroll) / Math.max(dt, 0.001);
      lastScroll = y;
      lean += (Math.max(-1, Math.min(1, speed / 2400)) - lean) * (1 - Math.exp(-dt * 6));

      // The first glimmer waits until the title has unfolded.
      const target = now - start < 1100 ? 0 : chargeAt(y);
      const rise = smooth(clamp01((y - riseStart) / (riseEnd - riseStart)));
      const pointerFresh = now - lastPointer < 2500;
      const aimX = pointerFresh ? state.aimX : 0;
      const aimY = (pointerFresh ? state.aimY : 0) - lean * 0.7;

      const ease = (rate: number) => 1 - Math.exp(-dt * rate);
      state.charge += (target - state.charge) * ease(3.2);
      state.rise += (rise - state.rise) * ease(12);
      state.tiltX += (aimX - state.tiltX) * ease(3.5);
      state.tiltY += (aimY - state.tiltY) * ease(3.5);
      // The shimmer's clock runs while the visitor scrolls or points, then winds down.
      const energy = Math.max(0, 1 - (now - lastActive) / 3200);
      state.time += dt * (0.2 + 0.8 * energy) * (energy > 0 ? 1 : 0);

      const values = `${state.rise.toFixed(4)}|${state.charge.toFixed(4)}|${Math.round(y)}`;
      if (values !== written) {
        written = values;
        element!.style.setProperty("--rise", state.rise.toFixed(4));
        element!.style.setProperty("--charge", state.charge.toFixed(4));
        // Until it docks, the glass also travels with the page, so it leaves with the words.
        element!.style.setProperty("--follow", `${Math.round(y)}px`);
        element!.dataset.charge = state.charge.toFixed(3);
      }
      bars.forEach((bar, i) => {
        const fill = barFill(i, y);
        bar.style.setProperty("--fill", fill.toFixed(3));
        bar.dataset.done = String(fill >= 1);
      });
      // The chapters take turns (see measure()). A chapter's first appearance plays its heading.
      faders.forEach((fader, i) => {
        const opacity = opacityAt(plans[i], y);
        const value = opacity >= 1 ? "" : opacity.toFixed(3);
        if (value !== shown[i]) {
          shown[i] = value;
          fader.style.opacity = value;
        }
        if (opacity > 0 && !entered[i]) {
          entered[i] = true;
          chapters[i].dataset.entered = "true";
          chapters[i].dispatchEvent(new Event("glass:enter"));
        }
      });
      // Each fact that joins the list sends a brief swell of light through the glass.
      state.pulse *= Math.exp(-dt * 1.8);
      factItems.forEach((fact, i) => {
        const on = y >= factAt[i];
        if (on !== docked[i]) {
          docked[i] = on;
          fact.dataset.docked = String(on);
          if (on && now - start > 1500) state.pulse = 1;
        }
      });

      scene.current?.render({
        charge: state.charge,
        pulse: state.pulse,
        time: state.time,
        tiltX: state.tiltX,
        tiltY: state.tiltY,
      });

      const settling =
        Math.abs(target - state.charge) > 0.0005 ||
        Math.abs(rise - state.rise) > 0.0005 ||
        Math.abs(aimX - state.tiltX) > 0.002 ||
        Math.abs(aimY - state.tiltY) > 0.002 ||
        Math.abs(lean) > 0.002 ||
        state.pulse > 0.01 ||
        energy > 0 ||
        now - start < 1400;
      if (settling && visible) frame = requestAnimationFrame(tick);
      else element!.dataset.awake = "false";
    }

    function wake() {
      lastActive = performance.now();
      if (!frame && visible) {
        last = performance.now();
        frame = requestAnimationFrame(tick);
        element!.dataset.awake = "true";
      }
    }
    function point(event: PointerEvent) {
      if (event.pointerType !== "mouse") return;
      state.aimX = (event.clientX / window.innerWidth - 0.5) * 2;
      state.aimY = -(event.clientY / window.innerHeight - 0.5) * 2;
      lastPointer = performance.now();
      wake();
    }
    function remeasure() {
      measure();
      wake();
    }

    measure();
    wake();
    const resize = new ResizeObserver(remeasure);
    resize.observe(element);
    const visibility = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      if (visible) wake();
      else if (frame) {
        cancelAnimationFrame(frame);
        frame = 0;
        element!.dataset.awake = "false";
      }
    });
    visibility.observe(element);
    window.addEventListener("scroll", wake, { passive: true });
    window.addEventListener("resize", remeasure);
    window.addEventListener("pointermove", point, { passive: true });
    element.addEventListener("glass:wake", wake);
    document.fonts?.addEventListener("loadingdone", remeasure);
    document.fonts?.ready.then(remeasure).catch(() => undefined);
    return () => {
      cancelAnimationFrame(frame);
      resize.disconnect();
      visibility.disconnect();
      document.fonts?.removeEventListener("loadingdone", remeasure);
      window.removeEventListener("scroll", wake);
      window.removeEventListener("resize", remeasure);
      window.removeEventListener("pointermove", point);
      element.removeEventListener("glass:wake", wake);
      faders.forEach((fader) => (fader.style.opacity = ""));
      chapters.forEach((chapter) => delete chapter.dataset.fits);
    };
  }, [reducedMotion]);

  // Wake the loop once the textures are in, so the first frame is drawn.
  useEffect(() => {
    if (ready) root.current?.dispatchEvent(new Event("glass:wake"));
  }, [ready]);

  // The one text treatment: each chapter heading rises into place line by line, behind a mask,
  // as its chapter first appears. Body text never moves by itself.
  useEffect(() => {
    const element = root.current;
    if (!element || reducedMotion) return;
    let cancelled = false;
    const undo: (() => void)[] = [];
    (async () => {
      const [{ default: gsap }, { SplitText }] = await Promise.all([
        import("gsap"),
        import("gsap/SplitText"),
      ]);
      await document.fonts?.ready;
      if (cancelled) return;
      gsap.registerPlugin(SplitText);
      element.querySelectorAll<HTMLElement>("[data-reveal]").forEach((target) => {
        const chapter = target.closest<HTMLElement>("[data-chapter]");
        let shown = chapter?.dataset.entered === "true";
        let lines: Element[] = [];
        // Lines only (words stay whole), so the split text still reads as plain text to screen
        // readers; no aria-label on the spans (a label on a span is not reliably read).
        const splitter = SplitText.create(target, {
          type: "lines",
          mask: "lines",
          aria: "none",
          autoSplit: true,
          onSplit(self) {
            lines = self.lines;
            gsap.set(lines, { yPercent: shown ? 0 : 108 });
          },
        });
        target.dataset.split = "true";
        const play = () => {
          if (shown) return;
          shown = true;
          target.dataset.revealed = "true";
          gsap.to(lines, { yPercent: 0, duration: 1.15, ease: "expo.out", stagger: 0.09 });
        };
        chapter?.addEventListener("glass:enter", play);
        if (shown) target.dataset.revealed = "true";
        undo.push(() => {
          chapter?.removeEventListener("glass:enter", play);
          gsap.killTweensOf(lines);
          splitter.revert();
          delete target.dataset.split;
        });
      });
    })().catch(() => undefined);
    return () => {
      cancelled = true;
      undo.forEach((fn) => fn());
    };
  }, [reducedMotion]);

  return (
    <div ref={root} className={styles.glass} data-ready={ready} data-motion={!reducedMotion}>
      {/* The pinned battery and its spec list. Decorative: every word here is also in the
          chapters below. The track spans the whole look, so the pinned stage stops at the look's
          end instead of riding over the footer. */}
      <div className={styles.track} aria-hidden="true">
        <div className={styles.stage}>
          <div className={styles.cap} />
          <div className={styles.bandMark} data-band />
          <div ref={batteryRef} className={styles.battery}>
            {/* Warm light on the paper behind the glass, growing with the charge. */}
            <div className={styles.glow} />
            <div ref={holder} className={styles.cell}>
              <Image
                src={STILL}
                alt=""
                width={1600}
                height={905}
                preload
                sizes="(max-width: 1099px) 150vw, 1300px"
                className={styles.still}
              />
            </div>
            <span className={styles.illustration}>{copy(drafts.illustration)}</span>
          </div>
          <div className={`${styles.grid} ${styles.specs}`}>
            <ol className={styles.facts}>
              {facts.map((fact) => (
                <FactItem key={fact.id} fact={fact} />
              ))}
            </ol>
          </div>
        </div>
      </div>

      {/* The opening: "Be in Good / Health." with the glass after it like a word (desktop). On
          phones and tablets the glass opens in the slot under the lead instead. */}
      <section className={styles.opening} data-chapter="opening" aria-labelledby="about-title">
        <div className={`${styles.grid} ${styles.hero}`} data-fade>
          <p className={styles.kicker}>{copy(about.hero.label)}</p>
          <Acronym className={styles.title} />
          <p className={styles.lead}>
            {sentences(copy(about.hero.lead)).map((sentence) => (
              <span key={sentence} className={styles.leadLine}>
                {sentence}
              </span>
            ))}
          </p>
          <div className={styles.slot} data-slot aria-hidden="true" />
        </div>
      </section>

      <section
        id="purpose"
        className={styles.chapter}
        data-chapter="purpose"
        aria-labelledby="purpose-title"
      >
        <div className={styles.frame} data-frame>
          <div className={`${styles.grid} ${styles.purpose}`}>
            <div className={styles.head}>
              <p className={styles.label}>{copy(about.purpose.label)}</p>
              <h2 id="purpose-title" className={styles.statement}>
                {about.purpose.lines.map((line) => (
                  <span key={line} data-reveal>
                    {copy(line)}
                  </span>
                ))}
              </h2>
            </div>
            <p className={`${styles.side} ${styles.voice}`}>{copy(about.purpose.mission)}</p>
          </div>
        </div>
        <div className={styles.hold} />
      </section>

      <section
        id="roots"
        className={styles.chapter}
        data-chapter="roots"
        aria-labelledby="roots-title"
      >
        <div className={styles.frame} data-frame>
          <div className={`${styles.grid} ${styles.roots}`}>
            <div className={styles.head}>
              <p className={styles.label}>{copy(about.roots.label)}</p>
              <h2 id="roots-title" className={styles.heading} data-reveal>
                {copy(about.roots.title)}
              </h2>
            </div>
            <div className={styles.side}>
              <p className={styles.body}>{copy(about.roots.text)}</p>
              <Link href={routes.scientists} className={styles.textLink}>
                {copy(about.roots.link)}
              </Link>
            </div>
            {/* Desktop: portrait and papers go to their own grid cells; phone: side by side. */}
            <div className={styles.who}>
              <figure className={styles.portrait}>
                <Image
                  src={about.roots.photo.src}
                  alt={copy(about.roots.photo.alt)}
                  width={512}
                  height={768}
                  sizes="(max-width: 1099px) 120px, 240px"
                  className={styles.portraitImage}
                />
              </figure>
              <p className={styles.stat} data-source="papers">
                <CountUp to={280} suffix="+" className={styles.statValue} />
                <span className={styles.statLabel}>{copy(about.roots.stat.label)}</span>
              </p>
            </div>
          </div>
        </div>
        <div className={styles.hold} />
      </section>

      <section
        id="experience"
        className={styles.chapter}
        data-chapter="experience"
        aria-labelledby="experience-title"
      >
        <div className={styles.frame} data-frame>
          <div className={`${styles.grid} ${styles.experience}`}>
            <div className={styles.head}>
              <p className={styles.label}>{copy(about.experience.label)}</p>
              <h2 id="experience-title" className={styles.heading} data-reveal>
                {copy(about.experience.title)}
              </h2>
            </div>
            <ul className={styles.numbers}>
              <li data-source="founded">
                <span className={styles.number}>{about.experience.stats[0].value}</span>
                <span className={styles.numberLabel}>{copy(about.experience.stats[0].label)}</span>
              </li>
              <li data-source="formula">
                <span className={styles.number}>
                  <CountUp to={20} suffix="+" />{" "}
                  <span className={styles.unit}>{copy(about.experience.stats[1].unit)}</span>
                </span>
                <span className={styles.numberLabel}>{copy(about.experience.stats[1].label)}</span>
              </li>
            </ul>
          </div>
        </div>
        <div className={styles.hold} />
      </section>

      <section
        id="promise"
        className={styles.chapter}
        data-chapter="promise"
        aria-labelledby="promise-title"
      >
        <div className={styles.frame} data-frame>
          <div className={`${styles.grid} ${styles.promise}`}>
            <div className={styles.head}>
              <p className={styles.label}>{copy(about.promise.label)}</p>
              <h2 id="promise-title" className={styles.heading} data-reveal>
                {copy(about.promise.title)}
              </h2>
            </div>
            <ul className={styles.promises}>
              {about.promise.items.map((item, index) => (
                <li
                  key={item.title}
                  className={styles.item}
                  data-pill
                  data-source={index === 2 ? "refund" : undefined}
                >
                  <span className={styles.bar} aria-hidden="true" />
                  <h3 className={styles.itemTitle}>{copy(item.title)}</h3>
                  <p className={styles.itemText}>{copy(item.text)}</p>
                  {index === 3 && <Greetings className={styles.hello} />}
                </li>
              ))}
            </ul>
          </div>
        </div>
        <div className={styles.hold} />
      </section>

      <section
        className={`${styles.chapter} ${styles.closingChapter}`}
        data-chapter="closing"
        aria-labelledby="closing-title"
      >
        <div className={styles.frame} data-frame>
          <div className={`${styles.grid} ${styles.closing}`}>
            {/* Phone and reduced motion: the spec list, complete, under the full battery. */}
            <ol className={`${styles.facts} ${styles.recap}`} aria-hidden="true">
              {facts.map((fact) => (
                <FactItem key={fact.id} fact={fact} />
              ))}
            </ol>
            <div className={styles.head}>
              <h2 id="closing-title" className={styles.closingTitle} data-reveal>
                {copy(about.closing.title)}
              </h2>
            </div>
            <div className={styles.side}>
              <p className={styles.body}>{copy(about.closing.text)}</p>
              <div className={styles.actions}>
                <button type="button" className={styles.primary} onClick={onAsk}>
                  {copy(about.closing.primary)}
                </button>
                <Link href={routes.products} className={styles.secondary}>
                  {copy(about.closing.secondary)}
                </Link>
              </div>
            </div>
          </div>
        </div>
        <div className={styles.hold} />
      </section>
    </div>
  );
}

// One sentence per line ("What our name stands for." / "What our work is for."); languages
// without ". " between sentences keep the line whole.
function sentences(text: string) {
  return text.split(/(?<=[.!?])\s+/);
}

type Box = { left: number; top: number; width: number };

// The glass's opening box (its visible glass, in page coordinates: left, top, width).
function openingGlass(root: HTMLElement): Box | null {
  const slot = root.querySelector<HTMLElement>("[data-slot]");
  const title = root.querySelector<HTMLElement>("h1");
  if (!slot || !title) return null;
  const y = window.scrollY;
  const words = [...title.querySelectorAll<HTMLElement>(":scope > span > span")];
  // Desktop: the slot is hidden, and the glass is set after "Health.".
  if (getComputedStyle(slot).display === "none" && words.length === 4) {
    const last = words[3];
    const initial = last.firstElementChild as HTMLElement | null;
    const rest = last.children[1]?.firstElementChild as HTMLElement | null;
    if (initial) {
      const style = getComputedStyle(title);
      const size = parseFloat(style.fontSize);
      const context = document.createElement("canvas").getContext("2d");
      if (context) {
        context.font = `${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
        context.letterSpacing = style.letterSpacing;
        const metrics = context.measureText("H");
        const letter = initial.getBoundingClientRect();
        // The word's final width, even before it has unfolded (its tail is clipped until then).
        const wordWidth = letter.width + (rest?.scrollWidth ?? 0);
        const baseline = letter.top + metrics.fontBoundingBoxAscent;
        const capHeight = metrics.actualBoundingBoxAscent;
        const healthRight = letter.left + wordWidth;
        const grid = title.parentElement!.getBoundingClientRect();
        const gridRight =
          grid.right - parseFloat(getComputedStyle(title.parentElement!).paddingRight);
        // As tall as the capitals. Its right end lines up with the last letter of "Good" above it
        // when that leaves a word space or so; otherwise it sits one word space after "Health.".
        const natural = capHeight / GLASS_RATIO;
        const good = words[2].firstElementChild as HTMLElement | null;
        const goodRight = good
          ? good.getBoundingClientRect().left + context.measureText("Good").actualBoundingBoxRight
          : Infinity;
        const aligned = goodRight - natural - healthRight;
        const gap = aligned >= size * 0.18 && aligned <= size * 0.5 ? aligned : size * 0.28;
        const left = healthRight + gap;
        const width = Math.min(natural, gridRight - left);
        const height = width * GLASS_RATIO;
        return { left, top: baseline - height + y, width };
      }
    }
  }
  // Otherwise: fitted into the slot, centered, with its shadow and caption inside it.
  const box = slot.getBoundingClientRect();
  if (!box.width || !box.height) return null;
  const width = Math.min(box.width, box.height / FOOTPRINT);
  return {
    left: box.left + (box.width - width) / 2,
    top: box.top + y + (box.height - width * FOOTPRINT) / 2,
    width,
  };
}

function clamp01(value: number) {
  return Math.min(1, Math.max(0, value));
}

// Ease in and out, so the battery leaves the title and settles into its dock softly.
function smooth(t: number) {
  return t * t * (3 - 2 * t);
}

// three.js needs WebGL 2. Without it the still render stays, and nothing is logged.
function canDrawWebGL() {
  try {
    const context = document.createElement("canvas").getContext("webgl2");
    context?.getExtension("WEBGL_lose_context")?.loseContext();
    return Boolean(context);
  } catch {
    return false;
  }
}

function FactItem({ fact }: { fact: Fact }) {
  return (
    <li className={styles.fact} data-fact={fact.id}>
      <span className={styles.factValue}>{fact.value}</span>
      <span className={styles.factLabel}>{fact.label}</span>
    </li>
  );
}
