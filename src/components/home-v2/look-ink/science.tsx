"use client";

import { ArrowRight, ArrowUpRight } from "lucide-react";
import { useCallback, useEffect, useRef, useState, type KeyboardEvent } from "react";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { science, scienceArticles, scienceFacts } from "../content";
import { useHomeDialogs } from "../dialogs";
import { gold, mito } from "./assets";
import base from "./look-ink.module.css";
import styles from "./science.module.css";

// "Make sense of the science." Three topics beside the SAME ink mitochondrion: close in on its two
// gold-leaf folds, where energy is made (mitochondria); whole, with a frayed edge and a few
// dry-brush flicks breaking away (free radicals, kept in balance); and, for aging cells, the young
// and the older organelle (registered onto each other) blended by an age slider, with the honesty
// line "Illustration, not a measurement".
//
// Round 7 (October 4): from 900px up, with motion, the block is a scroll story, one idea per
// screen, as Timeline explains its science. The painting is pinned (sticky) beside the words, the
// three topics follow one another down the page under the index (the tabs, now a progress index
// that stays at the top of the words), and as each topic reaches the reading line the painting
// blooms into that topic's state. Phones and reduced motion keep the three tabs.
const AGE_MIN = 30;
const AGE_MAX = 80;
/** Paper between the index and a topic's first line when the topic has arrived. */
const LEAD = 48;
/** The reading line, as far down the window as the brush line draws (brush.tsx). */
const READ = 0.78;
/** How far a leaving topic travels while it dissolves (science.module.css). */
const DISSOLVE = 60;

/** The scroll story runs from 900px up and only with motion; the tabs otherwise. */
function useScrollStory() {
  const [story, setStory] = useState(false);
  useEffect(() => {
    const wide = window.matchMedia("(min-width: 900px)");
    const still = window.matchMedia("(prefers-reduced-motion: reduce)");
    const update = () => setStory(wide.matches && !still.matches);
    update();
    wide.addEventListener("change", update);
    still.addEventListener("change", update);
    return () => {
      wide.removeEventListener("change", update);
      still.removeEventListener("change", update);
    };
  }, []);
  return story;
}

/** Where a topic would not fit the room under the pinned index (round 10: a narrow window such
 *  as 1024x768), the block is the tabbed one instead of a story whose index scrolls away. The
 *  story measures itself and gives way; it is tried again when the window's width changes or it
 *  grows tall enough that the topic could fit (not when a tablet's toolbar slides in or out). */
type Shortfall = { width: number; height: number; need: number };

function useStoryFits(wanted: boolean) {
  const [short, setShort] = useState<Shortfall | null>(null);
  useEffect(() => {
    if (!wanted || !short) return;
    // (once the window has stopped changing, so a drag does not flip the block back and forth)
    let timer = 0;
    const retry = () => {
      window.clearTimeout(timer);
      timer = window.setTimeout(() => {
        if (window.innerWidth !== short.width || window.innerHeight >= short.height + short.need) {
          setShort(null);
        }
      }, 300);
    };
    window.addEventListener("resize", retry);
    return () => {
      window.removeEventListener("resize", retry);
      window.clearTimeout(timer);
    };
  }, [wanted, short]);
  return { fits: !short, giveWay: setShort };
}

export function Science() {
  const copy = useCopy();
  const dialogs = useHomeDialogs();
  const wanted = useScrollStory();
  const { fits, giveWay } = useStoryFits(wanted);
  const story = wanted && fits;
  const [topic, setTopic] = useState(0);
  const [age, setAge] = useState(45);
  const tabs = useRef<(HTMLButtonElement | null)[]>([]);
  const section = useRef<HTMLElement>(null);
  const figure = useRef<HTMLElement>(null);
  const index = useRef<HTMLElement>(null);
  const steps = useRef<(HTMLDivElement | null)[]>([]);
  /** Where a topic's box stands once it has arrived: just under the pinned index. */
  const landing = useRef(0);
  /** While the page glides to a topic, the topic is already chosen (no passing through). */
  const gliding = useRef<(() => void) | null>(null);
  const article = scienceArticles[topic];
  const aged = (age - AGE_MIN) / (AGE_MAX - AGE_MIN);

  const onKey = (event: KeyboardEvent<HTMLButtonElement>, index: number) => {
    const step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[event.key];
    if (!step) return;
    event.preventDefault();
    const next = (index + step + 3) % 3;
    setTopic(next);
    tabs.current[next]?.focus();
  };

  // The story's measures: the painting is pinned centred in the window under the header, the
  // index level with its top; each topic stands under the index with the next just below, and
  // the last one ends level with the painting, so the index, the last topic and the painting
  // leave together.
  useEffect(() => {
    const root = section.current;
    const stage = figure.current;
    const bar = index.current;
    if (!story || !root || !stage || !bar) return;
    let line = 0;
    let frame = 0;
    /** The story gives way to the tabs only on a measure made with the page's own fonts (the
     *  first one once they have loaded), and afterwards only when the window's width changes (a
     *  height change keeps the story, its index static). */
    let judging = false;
    let judged = false;
    const width = window.innerWidth;
    const follow = () => {
      frame = 0;
      if (gliding.current) return;
      let next = 0;
      steps.current.forEach((step, i) => {
        if (step && step.getBoundingClientRect().top < line) next = i;
      });
      setTopic(next);
    };
    const measure = () => {
      const header = document.querySelector("header")?.getBoundingClientRect().height ?? 84;
      const view = window.innerHeight;
      const pin = Math.round(header + Math.max(24, (view - header - stage.offsetHeight) / 2));
      landing.current = pin + bar.offsetHeight;
      const tallest = Math.max(
        ...steps.current.map((step) => {
          const first = step?.firstElementChild as HTMLElement | null;
          const last = step?.lastElementChild as HTMLElement | null;
          return first && last ? last.offsetTop + last.offsetHeight - first.offsetTop : 0;
        }),
      );
      // A topic changes as its heading reaches the reading line. The next topic waits just
      // below, so its heading reaches the line as the last one has dissolved (it peeks in at
      // the foot of the window while a topic is read): the words are never gone, and never
      // without their heading.
      const read = view * READ;
      line = read - LEAD;
      const area = Math.round(read - LEAD + 6 + DISSOLVE - landing.current);
      root.style.setProperty("--pin", `${pin}px`);
      root.style.setProperty("--area", `${Math.max(area, tallest + LEAD + 64)}px`);
      root.style.setProperty("--last", `${stage.offsetHeight - bar.offsetHeight}px`);
      root.style.setProperty("--fade", `${landing.current + LEAD - 6}px`);
      // A topic taller than the room under the index could only be read by passing under it:
      // there the block gives way to the tabs. (If only the window's height has changed since,
      // the index stays where it is instead and nothing dissolves: science.module.css.)
      const need = tallest - (view - landing.current - LEAD);
      if (need > 0 && (judging || (judged && window.innerWidth !== width))) {
        giveWay({ width: window.innerWidth, height: view, need });
        return;
      }
      root.dataset.cramped = String(need > 0);
      follow();
    };
    const onScroll = () => {
      if (!frame) frame = requestAnimationFrame(follow);
    };
    const observer = new ResizeObserver(measure);
    observer.observe(stage);
    observer.observe(bar);
    window.addEventListener("resize", measure);
    window.addEventListener("scroll", onScroll, { passive: true });
    measure();
    let live = true;
    const settle = () => {
      if (!live) return;
      judging = true;
      measure();
      judging = false;
      judged = true;
    };
    if (document.fonts) document.fonts.ready.then(settle);
    else settle();
    return () => {
      live = false;
      observer.disconnect();
      window.removeEventListener("resize", measure);
      window.removeEventListener("scroll", onScroll);
      cancelAnimationFrame(frame);
      gliding.current?.();
      for (const name of ["--pin", "--area", "--last", "--fade"]) root.style.removeProperty(name);
      delete root.dataset.cramped;
    };
  }, [story, giveWay]);

  /** Glide the page until topic i has arrived under the index (the topic is chosen at once). */
  const go = useCallback((i: number) => {
    const step = steps.current[i];
    if (!step) return;
    gliding.current?.();
    setTopic(i);
    const from = window.scrollY;
    const distance = step.getBoundingClientRect().top - landing.current;
    const duration = Math.min(1600, Math.max(900, Math.abs(distance) * 0.55));
    const start = performance.now();
    let frame = 0;
    const stop = () => {
      cancelAnimationFrame(frame);
      for (const type of ["wheel", "touchstart", "keydown"]) window.removeEventListener(type, stop);
      gliding.current = null;
    };
    const tick = (now: number) => {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      window.scrollTo({ top: from + distance * eased, behavior: "instant" });
      if (t < 1) frame = requestAnimationFrame(tick);
      else stop();
    };
    for (const type of ["wheel", "touchstart", "keydown"]) {
      window.addEventListener(type, stop, { passive: true });
    }
    gliding.current = stop;
    frame = requestAnimationFrame(tick);
  }, []);

  /** Keyboard focus on a topic's links brings the topic to its place under the index (not a
   *  pointer's focus: the page must not move under a click). */
  const onStepFocus = (target: HTMLElement, i: number) => {
    if (!target.matches(":focus-visible")) return;
    const box = target.getBoundingClientRect();
    if (box.top < landing.current + LEAD - 2 || box.bottom > window.innerHeight) go(i);
  };

  const actions = (i: number) => (
    <div className={styles.actions}>
      <Link
        href="/science"
        className={base.pill}
        aria-describedby={story ? `ink-step-title-${i}` : undefined}
      >
        {copy(science.button)} <ArrowRight size={18} aria-hidden="true" />
      </Link>
      <button type="button" className={base.textLink} onClick={() => dialogs.openArticle(i)}>
        {copy(science.explainer)} <ArrowUpRight size={18} aria-hidden="true" />
      </button>
    </div>
  );

  const step = (i: number) => (
    <div
      key={i}
      ref={(node) => {
        steps.current[i] = node;
      }}
      id={`ink-step-${i}`}
      className={styles.step}
      data-step={i}
      onFocus={(event) => onStepFocus(event.target as HTMLElement, i)}
    >
      <h3 id={`ink-step-title-${i}`} className={styles.articleTitle}>
        {copy(scienceArticles[i].title)}
      </h3>
      <p className={base.body}>{copy(scienceArticles[i].preview)}</p>
      <ul className={styles.facts}>
        {scienceFacts[i].map((fact) => (
          <li key={fact}>{copy(fact)}</li>
        ))}
      </ul>
      {actions(i)}
    </div>
  );

  return (
    <section
      ref={section}
      id="science"
      className={`${styles.science} ${story ? styles.story : ""}`}
      aria-labelledby="science-title"
      data-brush="science"
      data-story={story}
    >
      <div className={`${base.wrap} ${styles.layout}`}>
        <div className={styles.copy} data-brush="science-copy">
          <h2 id="science-title" className={base.display}>
            {copy(science.title)}
          </h2>
          <p className={`${base.body} ${styles.intro}`}>{copy(science.text)}</p>

          {story ? (
            <>
              <div className={styles.track}>
                <nav ref={index} className={styles.tabs} aria-label={copy(science.title)}>
                  {science.topics.map((name, i) => (
                    <button
                      key={name}
                      type="button"
                      className={styles.tab}
                      aria-controls={`ink-step-${i}`}
                      aria-current={topic === i ? "step" : undefined}
                      onClick={() => go(i)}
                    >
                      {copy(name)}
                    </button>
                  ))}
                </nav>
                {step(0)}
                {step(1)}
              </div>
              {step(2)}
            </>
          ) : (
            <>
              <div className={styles.tabs} role="tablist" aria-label={copy(science.title)}>
                {science.topics.map((name, i) => (
                  <button
                    key={name}
                    ref={(node) => {
                      tabs.current[i] = node;
                    }}
                    type="button"
                    role="tab"
                    id={`ink-topic-${i}`}
                    aria-selected={topic === i}
                    aria-controls="ink-topic-panel"
                    tabIndex={topic === i ? 0 : -1}
                    className={styles.tab}
                    onClick={() => setTopic(i)}
                    onKeyDown={(event) => onKey(event, i)}
                  >
                    {copy(name)}
                  </button>
                ))}
              </div>

              <div
                key={topic}
                id="ink-topic-panel"
                role="tabpanel"
                aria-labelledby={`ink-topic-${topic}`}
                className={styles.panel}
              >
                <h3 className={styles.articleTitle}>{copy(article.title)}</h3>
                <p className={base.body}>{copy(article.preview)}</p>
                <ul className={styles.facts}>
                  {scienceFacts[topic].map((fact) => (
                    <li key={fact}>{copy(fact)}</li>
                  ))}
                </ul>
                {actions(topic)}
              </div>
            </>
          )}
        </div>

        <div className={styles.rail} data-brush="science-rail">
          <figure
            ref={figure}
            className={styles.figure}
            data-topic={topic}
            data-brush="science-mito"
          >
            <div className={styles.stage} data-bloom="">
              {/* eslint-disable-next-line @next/next/no-img-element -- a layer of one painting */}
              <img
                className={`${base.ink} ${styles.layer}`}
                src={mito.closeup.src}
                alt=""
                loading="lazy"
                data-on={topic === 0}
              />
              {/* eslint-disable-next-line @next/next/no-img-element -- a layer of one painting */}
              <img
                className={`${base.ink} ${styles.layer}`}
                src={mito.glow.src}
                alt=""
                loading="lazy"
                data-on={topic === 2}
                style={topic === 2 ? { opacity: 1 - aged } : undefined}
              />
              {/* eslint-disable-next-line @next/next/no-img-element -- a layer of one painting */}
              <img
                className={`${base.ink} ${styles.layer}`}
                src={mito.radicals.src}
                alt=""
                loading="lazy"
                data-on={topic === 1}
              />
              {/* eslint-disable-next-line @next/next/no-img-element -- a layer of one painting */}
              <img
                className={`${base.ink} ${styles.layer} ${styles.aged}`}
                src={mito.aged.src}
                alt=""
                loading="lazy"
                data-on={topic === 2}
                style={{ ["--aged" as string]: aged }}
              />
              <span
                className={`${base.gold} ${styles.leafLight}`}
                data-on={topic === 0}
                style={{ ["--gold" as string]: `url(${gold.closeup})` }}
              />
            </div>
            <figcaption className={`${base.caption} ${styles.caption}`}>
              {copy("Illustrations")}
            </figcaption>

            <div className={styles.age} data-on={topic === 2} inert={topic !== 2}>
              <label className={styles.ageLabel} htmlFor="ink-age">
                <span>{copy("Age")}</span>
                <strong>{age}</strong>
              </label>
              <input
                id="ink-age"
                type="range"
                min={AGE_MIN}
                max={AGE_MAX}
                step={1}
                value={age}
                onChange={(event) => setAge(Number(event.target.value))}
                className={styles.range}
                style={{ ["--fill" as string]: `${aged * 100}%` }}
              />
              <p className={styles.honesty}>{copy(science.ageLabel)}</p>
            </div>
          </figure>
        </div>
      </div>
    </section>
  );
}
