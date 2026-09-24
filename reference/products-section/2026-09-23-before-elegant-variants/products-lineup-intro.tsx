"use client";

import { useEffect, useRef, useState, type KeyboardEvent } from "react";
import { useCopy } from "@/i18n/use-copy";
import styles from "./products-lineup-intro.module.css";

const options = [
  {
    name: "Bold",
    first: "Good science.",
    second: "For real life.",
    description:
      "Cellular health is our starting point. Explore NuriCell and four distinctive formulas for everyday wellbeing.",
  },
  {
    name: "Elegant",
    first: "Small beginnings.",
    second: "Fuller lives.",
    description:
      "A world of care, starting with your cells. Find your place in the BiGH family of formulas.",
  },
  {
    name: "Expressive",
    first: "Your daily dose",
    second: "of possibility.",
    description:
      "Meet NuriCell and the formulas alongside it. Different stories. A shared curiosity for better living.",
  },
] as const;

export function ProductsLineupIntro() {
  const copy = useCopy();
  const [selected, setSelected] = useState(0);
  const [inView, setInView] = useState(false);
  const intro = useRef<HTMLElement>(null);
  const controls = useRef<HTMLDivElement>(null);
  const option = options[selected];

  useEffect(() => {
    const section = intro.current?.closest("section");
    if (!section) return;
    let frame = 0;
    const measure = () => {
      frame = 0;
      const bounds = section.getBoundingClientRect();
      setInView(bounds.bottom > 180 && bounds.top < window.innerHeight - 150);
    };
    const schedule = () => {
      if (!frame) frame = window.requestAnimationFrame(measure);
    };
    const observer = new ResizeObserver(schedule);
    observer.observe(section);
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", schedule);
    schedule();
    return () => {
      observer.disconnect();
      window.cancelAnimationFrame(frame);
      window.removeEventListener("scroll", schedule);
      window.removeEventListener("resize", schedule);
    };
  }, []);

  function choose(index: number) {
    setSelected(index);
    const bounds = intro.current?.getBoundingClientRect();
    // A reviewer can compare the heading even when browsing a story farther down.
    if (bounds && (bounds.top < 100 || bounds.bottom > window.innerHeight - 100)) {
      window.scrollTo({ top: window.scrollY + bounds.top - 120, behavior: "instant" });
    }
  }

  function navigate(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    const next =
      event.key === "ArrowRight"
        ? (index + 1) % options.length
        : event.key === "ArrowLeft"
          ? (index + options.length - 1) % options.length
          : event.key === "Home"
            ? 0
            : event.key === "End"
              ? options.length - 1
              : null;
    if (next === null) return;
    event.preventDefault();
    choose(next);
    controls.current
      ?.querySelectorAll<HTMLButtonElement>("button")
      [next]?.focus({ preventScroll: true });
  }

  return (
    <>
      <header ref={intro} className={styles.intro} data-heading-design={selected + 1}>
        <h2 id="collection-title">
          <span className={styles.first}>{copy(option.first)}</span>{" "}
          <span className={styles.second}>
            {copy(option.second)}
            {selected === 2 && (
              <svg className={styles.stroke} viewBox="0 0 540 35" fill="none" aria-hidden="true">
                <path d="M4 25C124 3 343 0 535 15M37 32C217 17 350 13 473 21" />
              </svg>
            )}
          </span>
        </h2>
        <p className={styles.description}>{copy(option.description)}</p>
      </header>
      {inView && (
        <aside className={styles.switcher} aria-label={copy("Compare product headings")}>
          <div className={styles.switcherLabel}>
            <span aria-live="polite" aria-atomic="true">
              {selected + 1} / {copy(option.name)}
            </span>
            <span>{copy("Heading options")}</span>
          </div>
          <div
            ref={controls}
            className={styles.options}
            role="group"
            aria-label={copy("Compare product headings")}
          >
            {options.map((item, index) => (
              <button
                key={item.name}
                type="button"
                aria-label={copy("Heading option {number}: {name}", {
                  number: index + 1,
                  name: copy(item.name),
                })}
                aria-pressed={selected === index}
                onClick={() => choose(index)}
                onKeyDown={(event) => navigate(event, index)}
              >
                {index + 1}
              </button>
            ))}
          </div>
        </aside>
      )}
    </>
  );
}
