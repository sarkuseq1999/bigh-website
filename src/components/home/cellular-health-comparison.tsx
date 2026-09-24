"use client";

import { useCopy } from "@/i18n/use-copy";

import Image from "next/image";
import { ArrowRight } from "lucide-react";
import { useEffect, useRef, useState, type KeyboardEvent } from "react";
import styles from "./cellular-health-comparison.module.css";
import { MitochondriaGlow } from "./mitochondria-glow";

const designs = [
  {
    id: 1,
    name: "Inside the cell",
    image: "01-inside-cell-white-left-v2",
    alt: "A translucent blue mitochondrion with amber inner folds, sculpted against white.",
  },
  {
    id: 2,
    name: "Living microscope",
    image: "02-living-microscope-white-left-v2",
    alt: "A translucent green cell above a connected, enlarged mitochondrion on white.",
  },
  {
    id: 3,
    name: "Sculpted energy",
    image: "03-sculpted-energy-white-left-v2",
    alt: "Sculptural copper folds of a mitochondrial membrane against a bright white background.",
  },
  {
    id: 4,
    name: "Pearl sculpture",
    image: "04-pearl-sculpture",
    alt: "A large pearl-blue mitochondrion with champagne-colored inner folds on white.",
  },
  {
    id: 5,
    name: "A closer look",
    image: "05-white-zoom",
    alt: "A translucent blue cell on white, with one small mitochondrion connected to a larger cutaway view.",
  },
  {
    id: 6,
    name: "Ivory editorial",
    image: "06-ivory-editorial",
    alt: "An enlarged view of soft pink and pearl mitochondrial folds on ivory.",
  },
] as const;

const originalDesign = {
  id: "original",
  name: "Inside the cell",
  image: "01-inside-cell",
  alt: "A blue mitochondrion with glowing amber inner folds inside a dark cellular environment.",
} as const;

export function CellularHealthComparison({
  onExplore,
  variant = "comparison",
}: {
  onExplore: () => void;
  variant?: "comparison" | "original";
}) {
  const copy = useCopy();
  const [selected, setSelected] = useState(1);
  const [inView, setInView] = useState(false);
  const [hasEntered, setHasEntered] = useState(false);
  const section = useRef<HTMLElement>(null);
  const controls = useRef<HTMLDivElement>(null);
  const isComparison = variant === "comparison";
  const design = isComparison ? designs[selected - 1] : originalDesign;
  const visibleDesigns = isComparison
    ? designs.filter((item) => hasEntered || item.id === selected)
    : [originalDesign];
  const artImages = visibleDesigns.map((item) => (
    <Image
      key={item.id}
      src={`/images/science/comparison/${item.image}.webp`}
      alt={item.id === design.id ? copy(item.alt) : ""}
      aria-hidden={item.id !== design.id}
      fill
      unoptimized
      sizes="100vw"
      loading="eager"
      className={styles.artImage}
      data-active={item.id === design.id}
    />
  ));

  useEffect(() => {
    if (!isComparison) return;
    const element = section.current;
    if (!element) return;
    let frame = 0;
    const measure = () => {
      frame = 0;
      const bounds = element.getBoundingClientRect();
      const visible = bounds.bottom > 120 && bounds.top < window.innerHeight - 100;
      setInView(visible);
      if (visible) setHasEntered(true);
    };
    const scheduleMeasure = () => {
      if (!frame) frame = window.requestAnimationFrame(measure);
    };
    // Design changes can resize the section without crossing an intersection threshold.
    const observer = new ResizeObserver(scheduleMeasure);
    observer.observe(element);
    window.addEventListener("scroll", scheduleMeasure, { passive: true });
    window.addEventListener("resize", scheduleMeasure);
    scheduleMeasure();
    return () => {
      observer.disconnect();
      window.cancelAnimationFrame(frame);
      window.removeEventListener("scroll", scheduleMeasure);
      window.removeEventListener("resize", scheduleMeasure);
    };
  }, [isComparison]);

  function choose(id: number) {
    setSelected(id);
  }

  function navigateDesigns(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    let next: number;
    if (event.key === "ArrowRight") next = (index + 1) % designs.length;
    else if (event.key === "ArrowLeft") next = (index + designs.length - 1) % designs.length;
    else if (event.key === "Home") next = 0;
    else if (event.key === "End") next = designs.length - 1;
    else return;
    event.preventDefault();
    choose(designs[next].id);
    controls.current?.querySelectorAll<HTMLButtonElement>("button")[next]?.focus();
  }

  return (
    <section
      ref={section}
      id="cellular-health"
      aria-labelledby="cellular-health-title"
      data-design={design.id}
      data-art-side={isComparison && selected <= 3 ? "left" : undefined}
      className={styles.section}
    >
      <div className={styles.scene}>
        <div className={styles.art}>
          {isComparison ? artImages : <MitochondriaGlow>{artImages}</MitochondriaGlow>}
        </div>
        <div className={styles.shade} aria-hidden="true" />
        <div className={styles.layout}>
          <header className={styles.heading}>
            <p className={styles.eyebrow}>{copy("WHY CELLULAR HEALTH MATTERS")}</p>
            <h2 id="cellular-health-title" className={styles.title}>
              {copy("Tiny power plants.")}
              <span>{copy("A big part of your health.")}</span>
            </h2>
          </header>
          <div className={styles.visualSpace} aria-hidden="true" />
          <div className={styles.content}>
            <p className={styles.opening}>
              {copy(
                "Inside many of your body’s cells are mitochondria—tiny power plants that turn energy from food into a form your cells can use.",
              )}
            </p>
            <div className={styles.benefits}>
              <p>
                {copy(
                  "That energy helps your brain think, your heart beat, and your muscles move.",
                )}
              </p>
              <p>{copy("It’s one reason good health starts with your cells.")}</p>
            </div>
            <button type="button" className={styles.action} onClick={onExplore}>
              {copy("Explore cellular health")} <ArrowRight size={21} aria-hidden="true" />
            </button>
          </div>
        </div>
        <p className={styles.caption}>{copy("Illustrative view")}</p>
      </div>
      {isComparison && inView && (
        <aside className={styles.switcher} aria-label={copy("Design comparison")}>
          <div className={styles.switcherLabel}>
            <span aria-live="polite" aria-atomic="true">
              {selected} / {design.name}
            </span>
            <span>{copy("Compare")}</span>
          </div>
          <div
            ref={controls}
            className={styles.options}
            role="group"
            aria-label={copy("Compare cellular-health designs")}
          >
            {designs.map((item, index) => (
              <button
                key={item.id}
                type="button"
                aria-label={`Design ${item.id}: ${item.name}`}
                aria-pressed={selected === item.id}
                title={item.name}
                onClick={() => choose(item.id)}
                onKeyDown={(event) => navigateDesigns(event, index)}
              >
                {item.id}
              </button>
            ))}
          </div>
        </aside>
      )}
    </section>
  );
}
