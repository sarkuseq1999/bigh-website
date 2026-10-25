"use client";

import { ArrowRight, ArrowUpRight } from "lucide-react";
import { useCallback, useEffect, useRef, useState, type KeyboardEvent } from "react";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { science, scienceArticles, scienceFacts } from "../content";
import { useSiteDialogs } from "@/components/ink/dialogs";
import { sciencePaintings } from "./assets";
import base from "@/components/ink/ink.module.css";
import styles from "./science.module.css";

// "Make sense of the science." Three topics, each picture showing what its words say, with a line
// under it that ties it to them. Mitochondria (Mo, October 22, 2026: pick D, after the October 21
// steam engine): an old powerhouse with its front left open, a worker feeding the gold fire whose
// steam turns the wheel, power running out along the wire. Free radicals (Mo, October 23: show
// the harm): its chimney opened up, the screen on top holding most of the sparks, the few that
// slip past burning black holes in the roof. Aging cells (Mo, October 22: the
// engine did not relate to the slider): one brain cell up close, young, middle-aged and old,
// its branches thinning and its gold power plants going out, chosen by an age slider, with the
// honesty line "Illustration, not a measurement". The slider shows one cell at a time, never two
// blended into a ghost.
//
// Round 7 (October 4): from 900px up, with motion, the block is a scroll story, one idea per
// screen, as Timeline explains its science. The painting is pinned (sticky) beside the words, the
// three topics follow one another down the page under the index (the tabs, now a progress index
// that stays at the top of the words), and as each topic reaches the reading line the painting
// blooms into that topic's state. Phones and reduced motion keep the three tabs; in one column
// (under 900px) the tabs sit right above the picture and the words follow it (Mo, October 23),
// and the three topics, each with its picture, line and words, sit side by side in a strip the
// finger swipes, snapping to one topic at a time (Mo, October 24: "swipe from one part of that
// section to another"). A tab glides the strip to its topic; a swipe moves the tabs' line.
const AGE_MIN = 30;
const AGE_MAX = 80;
/** The ages at which the slider moves the cell on to its next painting (young until 43, middle-
 *  aged until 68, then old): the slider opens at 45 on the middle-aged one. */
const TREE_FROM = [43, 68];
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

/** One column (under 900px): the swiped strip of topics instead of one panel beside the rail. */
function useNarrow() {
  const [narrow, setNarrow] = useState(false);
  useEffect(() => {
    const query = window.matchMedia("(max-width: 899px)");
    const update = () => setNarrow(query.matches);
    update();
    query.addEventListener("change", update);
    return () => query.removeEventListener("change", update);
  }, []);
  return narrow;
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
  const dialogs = useSiteDialogs();
  const wanted = useScrollStory();
  const { fits, giveWay } = useStoryFits(wanted);
  const story = wanted && fits;
  const narrow = useNarrow() && !story;
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
  /** One column: the strip of topics the finger swipes, its slides, and the topic a tab is
   *  gliding the strip to (the topics it passes on the way are not chosen). */
  const strip = useRef<HTMLDivElement>(null);
  const slides = useRef<(HTMLDivElement | null)[]>([]);
  const heading = useRef<number | null>(null);
  const article = scienceArticles[topic];
  const aged = (age - AGE_MIN) / (AGE_MAX - AGE_MIN);
  const tree = TREE_FROM.filter((from) => age >= from).length;

  const onKey = (event: KeyboardEvent<HTMLButtonElement>, index: number) => {
    const step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[event.key];
    if (!step) return;
    event.preventDefault();
    const next = (index + step + 3) % 3;
    choose(next);
    tabs.current[next]?.focus();
  };

  /** A tab chooses its topic; in one column it also glides the strip there. */
  const choose = (i: number) => {
    setTopic(i);
    const row = strip.current;
    if (!narrow || !row) return;
    heading.current = i;
    const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    row.scrollTo({ left: i * row.clientWidth, behavior: still ? "instant" : "smooth" });
  };

  // One column: a swipe chooses the topic the strip comes to rest on (it snaps to one), so the
  // tabs' line follows the finger; the strip opens on the chosen topic. The browser's snap did
  // not always finish after a short drag (October 24: the strip stayed 40 to 110px off a topic),
  // so once the strip has been still for a moment with no finger on it, it glides the rest of the
  // way to the nearest topic itself.
  useEffect(() => {
    const row = strip.current;
    if (!narrow || !row) return;
    row.scrollLeft = topic * row.clientWidth;
    let frame = 0;
    let settle = 0;
    let touching = false;
    const follow = () => {
      frame = 0;
      const i = Math.max(0, Math.min(2, Math.round(row.scrollLeft / row.clientWidth)));
      if (heading.current !== null) {
        if (i === heading.current) heading.current = null;
        return;
      }
      setTopic(i);
    };
    const home = () => {
      if (touching) return;
      const i = Math.max(0, Math.min(2, Math.round(row.scrollLeft / row.clientWidth)));
      if (Math.abs(row.scrollLeft - i * row.clientWidth) <= 1) return;
      const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      row.scrollTo({ left: i * row.clientWidth, behavior: still ? "instant" : "smooth" });
    };
    const later = () => {
      window.clearTimeout(settle);
      settle = window.setTimeout(home, 160);
    };
    const onScroll = () => {
      if (!frame) frame = requestAnimationFrame(follow);
      later();
    };
    // (a finger or a wheel takes over from a tab's glide)
    const takeOver = () => {
      heading.current = null;
    };
    const down = () => {
      touching = true;
      takeOver();
      window.clearTimeout(settle);
    };
    const up = () => {
      touching = false;
      later();
    };
    row.addEventListener("scroll", onScroll, { passive: true });
    row.addEventListener("pointerdown", takeOver);
    row.addEventListener("wheel", takeOver, { passive: true });
    row.addEventListener("touchstart", down, { passive: true });
    row.addEventListener("touchend", up, { passive: true });
    row.addEventListener("touchcancel", up, { passive: true });
    return () => {
      row.removeEventListener("scroll", onScroll);
      row.removeEventListener("pointerdown", takeOver);
      row.removeEventListener("wheel", takeOver);
      row.removeEventListener("touchstart", down);
      row.removeEventListener("touchend", up);
      row.removeEventListener("touchcancel", up);
      cancelAnimationFrame(frame);
      window.clearTimeout(settle);
    };
    // (only when the strip appears: the topic it opens on is the one chosen then)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [narrow]);

  // One column: the strip is as tall as the topic it rests on, so a shorter topic leaves no
  // empty paper under its words (the slides are not all the same height: Aging cells carries
  // the age slider).
  useEffect(() => {
    const row = strip.current;
    const slide = slides.current[topic];
    if (!narrow || !row || !slide) return;
    const fit = () => {
      row.style.height = `${slide.offsetHeight}px`;
    };
    fit();
    const observer = new ResizeObserver(fit);
    observer.observe(slide);
    return () => observer.disconnect();
  }, [narrow, topic]);

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

  /** The age slider and its honesty line, under the brain cell. */
  const ageControl = (on: boolean) => (
    <div className={styles.age} data-on={on} inert={!on}>
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
  );

  /** One column: one topic of the swiped strip, its picture, its line and its words (the topics
   *  beside the one at rest are inert: seen while swiping, never reached by a tab key). */
  const slide = (i: number) => (
    <div
      key={i}
      ref={(node) => {
        slides.current[i] = node;
      }}
      id={`ink-topic-panel-${i}`}
      role="tabpanel"
      aria-labelledby={`ink-topic-${i}`}
      className={styles.slide}
      inert={topic !== i}
    >
      <figure className={styles.figure}>
        <div className={styles.stage}>
          {i < 2 ? (
            // eslint-disable-next-line @next/next/no-img-element -- the topic's painting
            <img
              className={`${base.ink} ${styles.layer}`}
              src={(i === 0 ? sciencePaintings.energy : sciencePaintings.balance).src}
              alt=""
              loading={i === 0 ? "lazy" : "eager"}
              fetchPriority="low"
              data-on
            />
          ) : (
            <div className={`${base.ink} ${styles.layer}`} data-on>
              {sciencePaintings.aging.map((painting, a) => (
                // eslint-disable-next-line @next/next/no-img-element -- one age of the cell
                <img
                  key={painting.src}
                  className={styles.tree}
                  src={painting.src}
                  alt=""
                  loading="eager"
                  fetchPriority="low"
                  data-on={tree >= a}
                />
              ))}
            </div>
          )}
        </div>
        <figcaption className={`${base.caption} ${styles.caption}`}>
          {copy("Illustrations")}
        </figcaption>
        <p className={`${styles.peek} ${styles.slideLine}`} data-on>
          {copy(i === 2 ? science.peekAge[tree] : science.peek[i])}
        </p>
        {i === 2 && ageControl(true)}
      </figure>
      <div className={styles.slideWords}>
        <h3 className={styles.articleTitle}>{copy(scienceArticles[i].title)}</h3>
        <p className={base.body}>{copy(scienceArticles[i].preview)}</p>
        <ul className={styles.facts}>
          {scienceFacts[i].map((fact) => (
            <li key={fact}>{copy(fact)}</li>
          ))}
        </ul>
        {actions(i)}
      </div>
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
                    aria-controls={narrow ? `ink-topic-panel-${i}` : "ink-topic-panel"}
                    tabIndex={topic === i ? 0 : -1}
                    className={styles.tab}
                    onClick={() => choose(i)}
                    onKeyDown={(event) => onKey(event, i)}
                  >
                    {copy(name)}
                  </button>
                ))}
              </div>

              {!narrow && (
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
              )}
            </>
          )}
        </div>

        {narrow ? (
          <div ref={strip} className={styles.slides}>
            {[0, 1, 2].map(slide)}
          </div>
        ) : (
          <div className={styles.rail} data-brush="science-rail">
            <figure
              ref={figure}
              className={styles.figure}
              data-topic={topic}
              data-brush="science-painting"
            >
              <div className={styles.stage} data-bloom="">
                {/* eslint-disable-next-line @next/next/no-img-element -- a layer of the stage */}
                <img
                  className={`${base.ink} ${styles.layer}`}
                  src={sciencePaintings.energy.src}
                  alt=""
                  loading="lazy"
                  data-on={topic === 0}
                />
                {/* eslint-disable-next-line @next/next/no-img-element -- a layer of the stage */}
                <img
                  className={`${base.ink} ${styles.layer}`}
                  src={sciencePaintings.balance.src}
                  alt=""
                  loading="lazy"
                  data-on={topic === 1}
                />
                {/* The cell's three ages, one layer of the stage that multiplies as one: each
                  older one lies over the younger ones and covers them. */}
                <div className={`${base.ink} ${styles.layer}`} data-on={topic === 2}>
                  {sciencePaintings.aging.map((painting, i) => (
                    // eslint-disable-next-line @next/next/no-img-element -- one age of the cell
                    <img
                      key={painting.src}
                      className={styles.tree}
                      src={painting.src}
                      alt=""
                      loading="lazy"
                      data-on={tree >= i}
                    />
                  ))}
                </div>
              </div>
              <figcaption className={`${base.caption} ${styles.caption}`}>
                {copy("Illustrations")}
              </figcaption>
              {/* Every line is there, one over another, so the figure keeps the height of the
                longest whichever is shown (the scroll story measures the figure). */}
              <div className={styles.peeks}>
                {[...science.peek, ...science.peekAge].map((line, i) => {
                  const on = i === (topic === 2 ? 2 + tree : topic);
                  return (
                    <p key={line} className={styles.peek} data-on={on} aria-hidden={!on}>
                      {copy(line)}
                    </p>
                  );
                })}
              </div>

              {ageControl(topic === 2)}
            </figure>
          </div>
        )}
      </div>
    </section>
  );
}
