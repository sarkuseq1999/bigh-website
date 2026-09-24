"use client";

import { useEffect, useRef, useState, type KeyboardEvent } from "react";
import { useCopy } from "@/i18n/use-copy";
import styles from "./products-lineup-intro.module.css";

const options = [
  {
    name: "Cells",
    first: "Small cells.",
    second: "Big possibilities.",
    description:
      "Good health starts small. Meet NuriCell, our flagship for cellular health and mental energy, and explore four more formulas with distinctive stories in science and nature.",
  },
  {
    name: "Life",
    first: "Your life is full.",
    second: "Keep it that way.",
    description:
      "From NuriCell’s focus on cellular health and mental energy to plant-based antioxidant support, explore five formulas made for everyday wellbeing.",
  },
  {
    name: "Science",
    first: "The science runs deep.",
    second: "The purpose is you.",
    description:
      "Our flagship NuriCell was formulated by Dr. Jian Kang Liu and Dr. Iris Wang. Discover it alongside four distinctive formulas, united by BiGH’s focus on everyday wellbeing.",
  },
] as const;

export function ProductsLineupIntro({
  selected,
  onSelect,
}: {
  selected: number;
  onSelect: (index: number) => void;
}) {
  const copy = useCopy();
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
    onSelect(index);
    // Measure after the new design is laid out so scroll anchoring cannot clip the heading.
    requestAnimationFrame(() => {
      const bounds = intro.current?.getBoundingClientRect();
      if (bounds && (bounds.top < 100 || bounds.bottom > window.innerHeight - 100)) {
        window.scrollTo({ top: window.scrollY + bounds.top - 120, behavior: "instant" });
      }
    });
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
          <span className={styles.second}>{copy(option.second)}</span>
        </h2>
        <p className={styles.description}>{copy(option.description)}</p>
      </header>
      {inView && (
        <aside className={styles.switcher} aria-label={copy("Compare headline options")}>
          <div className={styles.switcherLabel}>
            <span aria-live="polite" aria-atomic="true">
              {selected + 1} / {copy(option.name)}
            </span>
            <span>{copy("Headline options")}</span>
          </div>
          <div
            ref={controls}
            className={styles.options}
            role="group"
            aria-label={copy("Compare headline options")}
          >
            {options.map((item, index) => (
              <button
                key={item.name}
                type="button"
                aria-label={copy("Headline option {number}: {name}", {
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
