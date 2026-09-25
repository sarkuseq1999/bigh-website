"use client";

import Image from "next/image";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ArrowDown } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useCopy } from "@/i18n/use-copy";
import { articles, images, intro, type ScienceDesignProps } from "./science-data";
import styles from "./science-table.module.css";
import { useReducedMotion } from "./use-reduced-motion";

// Kitchen table (after Timeline's science story): one sunlit overhead photograph fills the screen.
// As the visitor scrolls, the "camera" glides from the light bulb to the apple halves and lemon,
// then to the tree-ring board, pulling focus on each, while one short sentence at a time sits
// centered above it. Positions are fractions of the photo, measured on the image.
const ratio = images.table.width / images.table.height;
const subjectY = 0.64; // the subject sits low in the frame, under the words
// x, y: the subject's center; span, rise: its width and height, all as fractions of the photo.
const stops = [
  { x: 0.186, y: 0.445, span: 0.1, rise: 0.36 }, // the bulb on its napkin
  { x: 0.49, y: 0.44, span: 0.3, rise: 0.3 }, // browned apple, fresh apple, lemon
  { x: 0.845, y: 0.47, span: 0.26, rise: 0.56 }, // tree-ring board and tea
];
const notes = [
  { text: "Air only", x: 0.397, y: 0.6, chapter: 1 },
  { text: "With lemon juice", x: 0.514, y: 0.6, chapter: 1 },
  { text: "One ring a year", x: 0.84, y: 0.8, chapter: 2 },
];

export function ScienceTable({ onOpenArticle }: ScienceDesignProps) {
  const copy = useCopy();
  const reducedMotion = useReducedMotion();
  const root = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const view = useRef<HTMLDivElement>(null);
  const [chapter, setChapter] = useState(0);

  useEffect(() => {
    const element = root.current;
    const frame = view.current;
    const rail = track.current;
    if (!element || !frame || !rail || reducedMotion) return;
    gsap.registerPlugin(ScrollTrigger);

    // Where the camera sits to frame one stop, kept inside the photo's edges.
    function shot(index: number) {
      const width = frame!.clientWidth;
      const height = frame!.clientHeight;
      const photoWidth = height * ratio;
      const stop = stops[index];
      // Big enough to fill the frame; small enough that the subject fits under the words. On a
      // narrow phone the wide photo becomes a band along the bottom, under words set on paper.
      const narrow = width < 700;
      const scale = Math.max(
        narrow ? 0.6 : 1.12,
        Math.min(((narrow ? 0.9 : 0.56) * width) / (stop.span * photoWidth), 0.56 / stop.rise, 3),
      );
      const x = Math.min(
        0,
        Math.max(width - scale * photoWidth, width / 2 - scale * stop.x * photoWidth),
      );
      // The photo may sit a little low: its top edge hides under the paper wash behind the words.
      const lowest = height - scale * height;
      const y =
        scale < 1
          ? lowest
          : Math.min(height * 0.18, Math.max(lowest, height * subjectY - scale * stop.y * height));
      // Where the subject lands in the frame, so focus can follow it when an edge stops the camera.
      const fx = (x + scale * stop.x * photoWidth) / width;
      const fy = (y + scale * stop.y * height) / height;
      return { x, y, scale, fx, fy };
    }

    const context = gsap.context(() => {
      const layers = gsap.utils.toArray<HTMLElement>("[data-camera]");
      const soft = frame.querySelector<HTMLElement>("[data-soft]");
      const labels = gsap.utils.toArray<HTMLElement>("[data-note]");
      const place = () => {
        const x = Number(gsap.getProperty(layers[0], "x"));
        const y = Number(gsap.getProperty(layers[0], "y"));
        const scale = Number(gsap.getProperty(layers[0], "scale"));
        const height = frame.clientHeight;
        labels.forEach((label, index) => {
          const note = notes[index];
          label.style.left = `${x + scale * note.x * height * ratio}px`;
          label.style.top = `${y + scale * note.y * height}px`;
        });
      };
      const to = (index: number) => ({
        x: () => shot(index).x,
        y: () => shot(index).y,
        scale: () => shot(index).scale,
      });
      const focus = (index: number) => ({
        "--fx": () => shot(index).fx,
        "--fy": () => shot(index).fy,
      });
      gsap.set(layers, { transformOrigin: "0 0", ...to(0) });
      gsap.set(soft, focus(0));
      gsap
        .timeline({
          defaults: { ease: "power2.inOut" },
          onUpdate: place,
          scrollTrigger: {
            trigger: rail,
            start: "top top",
            end: "bottom bottom",
            scrub: 0.8,
            invalidateOnRefresh: true,
            onRefresh: place,
            onUpdate: (self) => {
              element.style.setProperty("--progress", self.progress.toFixed(4));
              setChapter(self.progress < 0.34 ? 0 : self.progress < 0.68 ? 1 : 2);
            },
          },
        })
        .to({}, { duration: 0.28 })
        .to(layers, { ...to(1), duration: 0.12 })
        .to(soft, { ...focus(1), duration: 0.12 }, "<")
        .to({}, { duration: 0.22 })
        .to(layers, { ...to(2), duration: 0.12 })
        .to(soft, { ...focus(2), duration: 0.12 }, "<")
        .to({}, { duration: 0.26 })
        // Focus pulls: the whole frame softens while the camera travels, then the subject sharpens.
        .fromTo(soft, { "--focus": 34 }, { "--focus": 0, duration: 0.05, ease: "none" }, 0.28)
        .to(soft, { "--focus": 34, duration: 0.06, ease: "none" }, 0.35)
        .to(soft, { "--focus": 0, duration: 0.05, ease: "none" }, 0.62)
        .to(soft, { "--focus": 34, duration: 0.06, ease: "none" }, 0.69);
      place();
    }, element);
    const refresh = () => ScrollTrigger.refresh();
    window.addEventListener("load", refresh);
    const settle = window.setTimeout(refresh, 1500);
    return () => {
      window.removeEventListener("load", refresh);
      window.clearTimeout(settle);
      context.revert();
    };
  }, [reducedMotion]);

  function goTo(index: number) {
    const element = track.current;
    if (!element) return;
    const top = element.getBoundingClientRect().top + window.scrollY;
    const travel = element.offsetHeight - window.innerHeight;
    const holds = [0.14, 0.5, 0.86];
    window.scrollTo({
      top: top + travel * holds[index],
      behavior: reducedMotion ? "auto" : "smooth",
    });
  }

  return (
    <div ref={root} className={styles.table} data-chapter={chapter} data-reduced={reducedMotion}>
      <header className={styles.head}>
        <h2 id="science-title" className={styles.heading}>
          {copy(intro.title)}
        </h2>
        <p>{copy(intro.text)}</p>
      </header>

      <div ref={track} className={styles.track}>
        <div className={styles.stage}>
          <div ref={view} className={styles.view}>
            <div className={styles.scene} aria-hidden="true">
              <div className={styles.photo} data-camera>
                <Image {...images.table} alt="" sizes="(max-width: 899px) 300vw, 160vw" />
              </div>
              <div className={styles.soft} data-soft>
                <div className={styles.photo} data-camera>
                  <Image
                    src="/images/science/kitchen-table-soft.webp"
                    width={960}
                    height={412}
                    alt=""
                    unoptimized
                  />
                </div>
              </div>
              <span className={styles.sun} />
              {notes.map((note) => (
                <span
                  key={note.text}
                  className={styles.note}
                  data-note
                  data-visible={chapter === note.chapter}
                >
                  {copy(note.text)}
                </span>
              ))}
            </div>
            <span className={styles.scrim} aria-hidden="true" />

            <div className={styles.copy}>
              {articles.map((article, index) => (
                <article
                  key={article.id}
                  className={styles.chapter}
                  data-active={reducedMotion || index === chapter}
                  inert={!reducedMotion && index !== chapter}
                >
                  <p className={styles.line}>{copy(article.analogy)}</p>
                  <h3 className={styles.title}>
                    <button type="button" onClick={() => onOpenArticle(index)}>
                      <span>{copy(article.title)}</span>
                    </button>
                  </h3>
                  <p className={styles.preview}>{copy(article.preview)}</p>
                </article>
              ))}
            </div>

            <nav className={styles.rail} aria-label={copy("Chapters")}>
              <span className={styles.meter} aria-hidden="true">
                <span />
              </span>
              {articles.map((article, index) => (
                <button
                  type="button"
                  key={article.id}
                  aria-current={index === chapter ? "step" : undefined}
                  onClick={() => goTo(index)}
                >
                  <span className={styles.step}>{index + 1}</span>
                  {copy(article.chapter)}
                </button>
              ))}
            </nav>
          </div>
        </div>
      </div>

      <div className={styles.foot}>
        <a href="#research" className={styles.explore}>
          {copy(intro.button)} <ArrowDown size={19} aria-hidden="true" />
        </a>
      </div>
    </div>
  );
}
