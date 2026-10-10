"use client";

import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ArrowLeft, ArrowRight, ArrowUpRight } from "lucide-react";
import {
  useEffect,
  useId,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
  type FocusEvent,
} from "react";
import { useCopy } from "@/i18n/use-copy";
import type { ProductPage } from "./product-types";
import { anchorId, byYear, useArrivals, type Chapter } from "./template-chapters-kit";
import shared from "./template-chapters.module.css";
import styles from "./template-chapters-research.module.css";

/** Wide and tall enough to pin the stage: the same test as the CSS. Everything else, and reduced
 * motion, gets a list you swipe or scroll sideways. */
const PINNED = "(min-width: 901px) and (min-height: 700px)";
const LIST = "not all and (min-width: 901px) and (min-height: 700px)";
/** Shares of the pinned scroll: a rest before the timeline moves, the move, a rest at the end. */
const REST_IN = 0.06;
const REST_OUT = 0.12;
const MOVE = 1 - REST_IN - REST_OUT;

/** How many years the gold line has reached, from how far along it is (0 to 1). */
function reached(share: number, count: number) {
  if (count < 2) return count;
  return Math.min(count, Math.floor(share * (count - 1) + 0.001) + 1);
}

// Chapter 4, the research, as a timeline you scroll sideways (timeline.com/about's horizontal
// timeline, from Mo's Design Vault). The studies stand on one line, oldest first, each saying
// plainly what kind of study it was and linking to it. The heading and the line that this is
// ingredient research, not evidence for the finished product, stay at the top the whole time.
// Wide screens pin the stage and scrolling moves the timeline; a thin gold line fills along it and
// lights each year as it arrives. Phones and reduced motion get a list you swipe, the next study
// peeking in.
export function ResearchChapter({
  product,
  chapter,
  reduced,
}: {
  product: ProductPage;
  chapter: Chapter;
  reduced: boolean;
}) {
  const copy = useCopy();
  const root = useRef<HTMLElement>(null);
  const titleId = useId();
  const listId = useId();
  const studies = useMemo(() => byYear(product.studies), [product.studies]);
  const count = studies.length;
  // How many years the gold line has reached. null: all of them (the still layouts).
  const [lit, setLit] = useState<number | null>(null);
  useArrivals(root, reduced);

  useEffect(() => {
    const section = root.current;
    if (reduced || !section || count === 0) return;
    const scroller = section.querySelector<HTMLElement>("[data-window]");
    const rail = section.querySelector<HTMLElement>("[data-rail]");
    const head = section.querySelector<HTMLElement>("[data-head]");
    const fill = section.querySelector<HTMLElement>("[data-fill]");
    const items = gsap.utils.toArray<HTMLElement>("[data-study]", section);
    if (!scroller || !rail || !head || items.length === 0) return;
    gsap.registerPlugin(ScrollTrigger);
    const mm = gsap.matchMedia(section);

    // Pinned: the stage sticks for a tall section, and one scrubbed timeline slides the studies
    // from the first, at the left edge of the page's lane, to the last, at its right edge.
    mm.add(PINNED, () => {
      let travel = 0;
      // Where the page's lane begins, and each study's place on the rail before it moves.
      let lane = 0;
      let places: { left: number; width: number }[] = [];
      const measure = () => {
        const box = head.getBoundingClientRect();
        const style = getComputedStyle(head);
        const start = scroller.getBoundingClientRect().left + rail.offsetLeft;
        lane = box.left + parseFloat(style.paddingLeft);
        places = items.map((item) => ({
          left: start + item.offsetLeft,
          width: item.offsetWidth,
        }));
        const last = places[places.length - 1];
        const end = box.right - parseFloat(style.paddingRight);
        travel = Math.max(0, Math.round(last.left + last.width - end));
        section.style.setProperty("--scroll", `${Math.round(travel / MOVE)}px`);
      };
      measure();
      // Measured again before every refresh, so a new window size gets its own distance.
      ScrollTrigger.addEventListener("refreshInit", measure);

      const timeline = gsap.timeline({
        defaults: { ease: "none" },
        scrollTrigger: {
          trigger: section,
          start: "top top",
          end: "bottom bottom",
          scrub: 0.6,
          invalidateOnRefresh: true,
        },
      });
      timeline.fromTo(rail, { x: 0 }, { x: () => -travel, duration: MOVE }, REST_IN);
      if (fill) timeline.fromTo(fill, { scaleX: 0 }, { scaleX: 1, duration: MOVE }, REST_IN);
      timeline.set({}, {}, 1);
      const share = () => gsap.utils.clamp(0, 1, (timeline.time() - REST_IN) / MOVE);
      // A study leaving past the lane's edge fades as a whole, gone by the time a third of it has
      // left, so what the edge cuts is only ever faint.
      const fadeOut = () => {
        const x = Number(gsap.getProperty(rail, "x")) || 0;
        items.forEach((item, index) => {
          const place = places[index];
          const out = place ? lane - (place.left + x) : 0;
          if (out <= 0) item.style.removeProperty("opacity");
          else item.style.opacity = String(gsap.utils.clamp(0, 1, 1 - out / (place.width * 0.3)));
        });
      };
      const update = () => {
        setLit(reached(share(), count));
        fadeOut();
      };
      timeline.eventCallback("onUpdate", update);
      update();

      // The keyboard: a study's link taking focus scrolls the page to where that study is in view.
      const bring = (event: globalThis.FocusEvent) => {
        const item = (event.target as Element | null)?.closest<HTMLElement>("[data-study]");
        const trigger = timeline.scrollTrigger;
        if (!item || !trigger) return;
        const index = Number(item.dataset.study) || 0;
        const at = REST_IN + (count > 1 ? index / (count - 1) : 0) * MOVE;
        const top = Math.ceil(trigger.start + at * (trigger.end - trigger.start)) + 1;
        const go = () => {
          if (Math.abs(window.scrollY - top) > 1) window.scrollTo({ top, behavior: "instant" });
          ScrollTrigger.update();
          trigger.getTween()?.progress(1);
        };
        go();
        // Again after the browser's own scrolling for focus, which may come after this.
        requestAnimationFrame(go);
      };
      rail.addEventListener("focusin", bring);

      return () => {
        rail.removeEventListener("focusin", bring);
        ScrollTrigger.removeEventListener("refreshInit", measure);
        section.style.removeProperty("--scroll");
        items.forEach((item) => item.style.removeProperty("opacity"));
        setLit(null);
      };
    });

    // The list: the gold line follows the swiping.
    mm.add(LIST, () => {
      const follow = () => {
        const max = scroller.scrollWidth - scroller.clientWidth;
        const share = max > 1 ? gsap.utils.clamp(0, 1, scroller.scrollLeft / max) : 1;
        if (fill) gsap.set(fill, { scaleX: share });
        setLit(reached(share, count));
      };
      follow();
      scroller.addEventListener("scroll", follow, { passive: true });
      window.addEventListener("resize", follow);
      return () => {
        scroller.removeEventListener("scroll", follow);
        window.removeEventListener("resize", follow);
        setLit(null);
      };
    });

    return () => mm.revert();
  }, [reduced, count]);

  // The list: a study taking focus lines up at the start, whole (not just its link).
  const lineUp = (event: FocusEvent<HTMLOListElement>) => {
    const scroller = event.currentTarget.closest<HTMLElement>("[data-window]");
    const item = (event.target as Element).closest<HTMLElement>("[data-study]");
    if (!scroller || !item || getComputedStyle(scroller).overflowX !== "auto") return;
    const padding = parseFloat(getComputedStyle(scroller).scrollPaddingLeft) || 0;
    const left =
      item.getBoundingClientRect().left - scroller.getBoundingClientRect().left - padding;
    scroller.scrollBy({ left, behavior: "instant" });
  };

  // The list's buttons, for a mouse: one study earlier or later.
  const step = (direction: 1 | -1) => {
    const scroller = root.current?.querySelector<HTMLElement>("[data-window]");
    const item = root.current?.querySelector<HTMLElement>("[data-study]");
    if (!scroller || !item?.parentElement) return;
    const gap = parseFloat(getComputedStyle(item.parentElement).columnGap) || 0;
    scroller.scrollBy({
      left: direction * (item.offsetWidth + gap),
      behavior: reduced ? "instant" : "smooth",
    });
  };

  const opensNew = copy("(opens in a new tab)");

  return (
    <section
      ref={root}
      id={anchorId(chapter.id)}
      data-chapter={chapter.id}
      data-tone={chapter.tone}
      tabIndex={-1}
      aria-labelledby={titleId}
      className={`${shared.chapter} ${styles.research}`}
      data-motion={reduced ? "off" : "on"}
      style={{ "--count": count } as CSSProperties}
    >
      <div className={styles.stage}>
        <header className={styles.head} data-head>
          <h2 id={titleId} className={styles.heading} data-heading>
            {copy(product.researchTitle ?? "The research on the ingredients")}
          </h2>
          <p className={styles.honesty}>{copy(product.notes.research)}</p>
        </header>

        <div className={styles.window} data-window data-reveal>
          <div className={styles.rail} data-rail>
            {/* The line from the first year to the last, and the gold line that fills along it. */}
            <span className={styles.line} aria-hidden="true" />
            {count > 1 && <span className={styles.fill} aria-hidden="true" data-fill />}
            <ol id={listId} className={styles.list} onFocus={lineUp}>
              {studies.map((study, index) => {
                const titleOf = `${listId}-${index}`;
                return (
                  <li
                    key={`${index}-${study.url}`}
                    className={styles.item}
                    data-study={index}
                    data-lit={lit === null || index < lit}
                    data-current={lit !== null && index === lit - 1}
                  >
                    <p className={styles.year}>{study.year}</p>
                    <span className={styles.mark} aria-hidden="true">
                      <span className={styles.dot} />
                    </span>
                    <p className={styles.meta}>
                      <span className={styles.kind}>{copy(study.kind)}</span>
                      <span className={styles.journal}>{copy(study.journal)}</span>
                    </p>
                    <h3 id={titleOf} className={styles.title}>
                      {copy(study.title)}
                    </h3>
                    <p className={styles.note}>{copy(study.note)}</p>
                    <a
                      className={styles.link}
                      href={study.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      aria-describedby={titleOf}
                    >
                      {copy("Read the study")}
                      <ArrowUpRight size={19} strokeWidth={2} aria-hidden="true" />
                      <span className={shared.srOnly}>{opensNew}</span>
                    </a>
                  </li>
                );
              })}
            </ol>
          </div>
        </div>

        {count > 1 && (
          <div className={styles.steps}>
            <button
              type="button"
              className={styles.step}
              aria-controls={listId}
              onClick={() => step(-1)}
            >
              <ArrowLeft size={21} strokeWidth={2} aria-hidden="true" />
              <span className={shared.srOnly}>{copy("Earlier studies")}</span>
            </button>
            <button
              type="button"
              className={styles.step}
              aria-controls={listId}
              onClick={() => step(1)}
            >
              <ArrowRight size={21} strokeWidth={2} aria-hidden="true" />
              <span className={shared.srOnly}>{copy("Later studies")}</span>
            </button>
          </div>
        )}
      </div>
    </section>
  );
}
