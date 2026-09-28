"use client";

import Image from "next/image";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { SplitText } from "gsap/SplitText";
import { useEffect, useId, useRef, type CSSProperties } from "react";
import { useCopy } from "@/i18n/use-copy";
import type { ProductPage, ProductWhy } from "./product-types";
import { anchorId, lineClass, wordClass, type Chapter, type Tone } from "./template-chapters-kit";
import shared from "./template-chapters.module.css";
import styles from "./template-chapters-why.module.css";

// Chapter 2, why it matters. With a night photo (NuriCell: a light bulb, off, then on) the chapter
// turns dark and tells its story over the picture, one idea per screen: the figures, the light
// coming on as the second one counts up, one familiar comparison, the approved lines, and last the
// title. Without one, the lines arrive on paper beside a quiet list. Scroll drives both; nothing
// snaps. A product photo, when there is one, comes first, softening under its line.
export function WhyChapter({
  product,
  chapter,
  reduced,
}: {
  product: ProductPage;
  chapter: Chapter;
  reduced: boolean;
}) {
  const copy = useCopy();
  const titleId = useId();
  const why = product.why;
  const night = Boolean(why?.visual);
  return (
    <section
      id={anchorId(chapter.id)}
      data-chapter={chapter.id}
      // A night chapter marks where its night begins itself (see NightStage).
      data-tone={night ? undefined : chapter.tone}
      tabIndex={-1}
      aria-labelledby={titleId}
      className={shared.chapter}
    >
      {product.photo && <PhotoMoment photo={product.photo} reduced={reduced} />}
      {why?.visual ? (
        <NightStage
          why={why}
          visual={why.visual}
          tone={chapter.tone}
          titleId={titleId}
          reduced={reduced}
        />
      ) : why ? (
        <PaperStage why={why} titleId={titleId} reduced={reduced} />
      ) : (
        <h2 id={titleId} className={shared.srOnly}>
          {copy(chapter.name)}
        </h2>
      )}
    </section>
  );
}

/* ─── The night stage ─── */

/** Scrolling per unit of story time, in svh. The track is 100svh plus this for every unit. */
const BEAT = 30;
/** Story time: a moment resting, one moment handing over to the next, the light coming on, and the
 * title's rest before the stage lets go. */
const HOLD = 1;
const CHANGE = 0.8;
const SWITCH = 1.7;
const REST = 1.1;

/** When each hand-over starts and how long it takes, and the story's whole length. The track's
 * height and the timeline both come from here, so scroll and story always line up. */
function story(count: number, lit: boolean) {
  const changes: { at: number; span: number; lightsOn: boolean }[] = [];
  let at = HOLD;
  for (let index = 1; index < count; index += 1) {
    const lightsOn = lit && index === 1;
    const span = lightsOn ? SWITCH : CHANGE;
    changes.push({ at, span, lightsOn });
    at += span + (index === count - 1 ? REST : HOLD);
  }
  return { changes, total: count > 1 ? at : HOLD + REST };
}

function NightStage({
  why,
  visual,
  tone,
  titleId,
  reduced,
}: {
  why: ProductWhy;
  visual: NonNullable<ProductWhy["visual"]>;
  tone: Tone;
  titleId: string;
  reduced: boolean;
}) {
  const copy = useCopy();
  const track = useRef<HTMLDivElement>(null);
  const lit = visual.lit;
  const facts = why.facts ?? [];
  const count = facts.length + (why.comparison ? 1 : 0) + why.lines.length + 1;
  const { total } = story(count, Boolean(lit));

  // One scrubbed timeline over a tall track with a sticky stage (only in windows tall enough to
  // hold it; shorter ones, and reduced motion, get the still layout from the CSS). Every moment
  // takes its turn in the same place: the one before fades up and away, the next rises out of a
  // soft blur. The light comes on during the first hand-over, while the figure counts up.
  useEffect(() => {
    const element = track.current;
    if (reduced || !element) return;
    gsap.registerPlugin(ScrollTrigger, SplitText);
    let cancelled = false;
    const mm = gsap.matchMedia(element);
    void document.fonts.ready.then(() => {
      if (cancelled) return;
      mm.add(
        {
          tall: "(min-height: 561px)",
          // A change of layout (picture beside the words, or above them) rebuilds the timeline.
          side: "(min-width: 900px) and (min-aspect-ratio: 5/4)",
        },
        (context) => {
          if (!context.conditions?.tall) return;
          const q = gsap.utils.selector(element);
          const moments = q("[data-why-moment]") as HTMLElement[];
          const litPhoto = q("[data-why-lit]")[0] as HTMLElement | undefined;
          const glow = q("[data-why-glow]")[0] as HTMLElement | undefined;
          const title = q("[data-why-title]")[0] as HTMLElement | undefined;
          const split = title
            ? SplitText.create(title, { type: "lines", mask: "lines", linesClass: lineClass })
            : null;
          const counters: { node: Text; original: string }[] = [];
          const plan = story(moments.length, Boolean(litPhoto));

          // The stage rises into place with the picture settling and the first moment arriving,
          // so it never arrives empty.
          gsap
            .timeline({
              defaults: { ease: "none" },
              scrollTrigger: { trigger: element, start: "top 80%", end: "top top", scrub: 0.8 },
            })
            .fromTo("[data-why-picture]", { scale: 1.07 }, { scale: 1 }, 0)
            .fromTo("[data-why-copy]", { opacity: 0, y: 56 }, { opacity: 1, y: 0 }, 0.35);

          const timeline = gsap.timeline({
            defaults: { ease: "power2.out" },
            scrollTrigger: { trigger: element, start: "top top", end: "bottom bottom", scrub: 0.8 },
          });
          // A slow push in on the picture across the whole story.
          timeline.fromTo(
            "[data-why-frame]",
            { scale: 1 },
            { scale: 1.06, ease: "none", duration: plan.total },
            0,
          );

          plan.changes.forEach(({ at, span, lightsOn }, index) => {
            const previous = moments[index];
            const current = moments[index + 1];
            if (lightsOn && litPhoto) {
              // Warming up: slow at first, then the filament is bright and the room glows.
              timeline.fromTo(
                litPhoto,
                { opacity: 0 },
                { opacity: 1, duration: span * 0.72, ease: "power2.inOut" },
                at + span * 0.08,
              );
              if (glow) {
                timeline.fromTo(
                  glow,
                  { opacity: 0, scale: 0.55 },
                  { opacity: 1, scale: 1, duration: span * 0.8, ease: "power1.out" },
                  at + span * 0.2,
                );
              }
            }

            const from = previous.dataset.figure;
            const to = current.dataset.figure;
            const counting =
              from !== undefined &&
              to !== undefined &&
              previous.dataset.unit === current.dataset.unit;
            if (counting) {
              // Figure to figure: the same number in the same place swaps without a seam, then
              // counts up while the words beneath change.
              const count = current.querySelector("[data-why-count]")?.firstChild;
              const figure = current.querySelector("[data-why-figure]");
              const words = current.querySelector("[data-why-fact-line]");
              const before = previous.querySelector("[data-why-fact-line]");
              timeline
                .fromTo(current, { opacity: 0 }, { opacity: 1, duration: 0.01, ease: "none" }, at)
                .to(previous.querySelector("[data-why-figure]"), { opacity: 0, duration: 0.01 }, at)
                .to(
                  before,
                  {
                    opacity: 0,
                    y: -16,
                    filter: "blur(5px)",
                    duration: span * 0.4,
                    ease: "power1.in",
                  },
                  at,
                )
                .fromTo(
                  words,
                  { opacity: 0, y: 20, filter: "blur(6px)" },
                  { opacity: 1, y: 0, filter: "blur(0px)", duration: span * 0.5 },
                  at + span * 0.42,
                );
              if (count instanceof Text && figure) {
                counters.push({ node: count, original: count.data });
                const start = Number(from);
                const counter = { value: start };
                count.data = String(start);
                timeline.fromTo(
                  counter,
                  { value: start },
                  {
                    value: Number(to),
                    duration: span * 0.78,
                    ease: "power1.inOut",
                    onUpdate: () => {
                      count.data = String(Math.round(counter.value));
                    },
                  },
                  at + span * 0.06,
                );
              }
              return;
            }

            timeline.to(
              previous,
              { opacity: 0, y: -22, filter: "blur(6px)", duration: span * 0.45, ease: "power1.in" },
              at,
            );
            if (current === title && split) {
              // The title rises line by line behind masks, last of all.
              timeline
                .fromTo(
                  current,
                  { opacity: 0 },
                  { opacity: 1, duration: 0.01, ease: "none" },
                  at + span * 0.4,
                )
                .fromTo(
                  split.lines,
                  { yPercent: 130 },
                  { yPercent: 0, duration: span * 0.7, stagger: 0.12, ease: "power3.out" },
                  at + span * 0.4,
                );
            } else {
              timeline.fromTo(
                current,
                { opacity: 0, y: 26, filter: "blur(8px)" },
                { opacity: 1, y: 0, filter: "blur(0px)", duration: span * 0.6 },
                at + span * 0.4,
              );
            }
          });
          // The title's rest: the story ends where the track does.
          timeline.set({}, {}, plan.total);

          return () => {
            counters.forEach(({ node, original }) => {
              node.data = original;
            });
          };
        },
      );
    });
    return () => {
      cancelled = true;
      mm.revert();
    };
  }, [reduced]);

  const picture = (source: { src: string; width: number; height: number }) => ({
    src: source.src,
    width: source.width,
    height: source.height,
    // The originals, untouched: the chapter's night is sampled from their pixels, and re-encoding
    // would shift the colour enough to show an edge. They are small (dark photos compress well).
    unoptimized: true,
    className: styles.photo,
  });

  return (
    <div
      ref={track}
      className={styles.night}
      data-motion={reduced ? "off" : "on"}
      style={
        {
          "--beats": total,
          "--beat": `${BEAT}svh`,
          "--ratio": visual.width / visual.height,
        } as CSSProperties
      }
    >
      <div className={styles.stage}>
        <div className={styles.picture} data-why-picture>
          <div className={styles.frame} data-why-frame>
            <Image {...picture(visual)} alt={copy(visual.alt)} />
            {lit && (
              <>
                {/* The same picture with its light on, over the first; it shares the description. */}
                <Image {...picture(lit)} alt="" data-why-lit />
                <span className={styles.glow} aria-hidden="true" data-why-glow />
              </>
            )}
          </div>
        </div>
        <div className={styles.copy} data-why-copy>
          <p className={styles.label}>{copy(why.label)}</p>
          <div className={styles.moments}>
            {facts.length > 0 && (
              <div className={styles.facts}>
                {facts.map((fact, index) => (
                  <p
                    key={index}
                    className={styles.fact}
                    data-why-moment
                    data-figure={fact.figure}
                    data-unit={fact.unit}
                    data-lit={Boolean(lit) && index > 0}
                  >
                    {/* The line says the figure in words; the big figure is for the eye. */}
                    <span className={styles.figure} aria-hidden="true" data-why-figure>
                      <span data-why-count>{fact.figure}</span>
                      <span className={styles.unit}>{fact.unit}</span>
                    </span>
                    <span className={styles.factLine} data-why-fact-line>
                      {copy(fact.line)}
                    </span>
                  </p>
                ))}
              </div>
            )}
            {why.comparison && (
              <p className={styles.comparison} data-why-moment>
                {copy(why.comparison)}
              </p>
            )}
            {why.lines.map((line, index) => (
              <p key={index} className={styles.line} data-why-moment data-why-line>
                {copy(line)}
              </p>
            ))}
            <h2 id={titleId} className={styles.title} data-why-moment data-why-title>
              {copy(why.title)}
            </h2>
          </div>
        </div>
        {why.source && <p className={styles.source}>{copy(why.source)}</p>}
      </div>
      {/* The page's index turns light from here: once the night fills the screen. */}
      <span className={styles.marker} data-tone={tone} aria-hidden="true" />
    </div>
  );
}

/* ─── A product photo, and the paper stage for products without a night photo ─── */

function PhotoMoment({
  photo,
  reduced,
}: {
  photo: NonNullable<ProductPage["photo"]>;
  reduced: boolean;
}) {
  const copy = useCopy();
  const track = useRef<HTMLDivElement>(null);

  // Sharp as it arrives; once it fills the screen it softens, darkens a little, and the line rises.
  useEffect(() => {
    const element = track.current;
    if (reduced || !element) return;
    gsap.registerPlugin(ScrollTrigger, SplitText);
    let cancelled = false;
    const ctx = gsap.context(() => {}, element);
    void document.fonts.ready.then(() => {
      if (cancelled) return;
      ctx.add(() => {
        const split = SplitText.create(element.querySelector("[data-photo-line]"), {
          type: "words",
          mask: "words",
          wordsClass: wordClass,
        });
        gsap
          .timeline({
            defaults: { ease: "none" },
            scrollTrigger: { trigger: element, start: "top top", end: "bottom bottom", scrub: 0.7 },
          })
          .fromTo(
            "[data-photo]",
            { scale: 1.06, filter: "blur(0px)" },
            { scale: 1, filter: "blur(9px)", duration: 1 },
            0,
          )
          .fromTo("[data-photo-shade]", { opacity: 0.15 }, { opacity: 1, duration: 0.7 }, 0.05)
          .fromTo(
            split.words,
            { yPercent: 130 },
            { yPercent: 0, duration: 0.45, stagger: 0.05, ease: "power2.out" },
            0.28,
          )
          .to({}, { duration: 0.25 });
      });
    });
    return () => {
      cancelled = true;
      ctx.revert();
    };
  }, [reduced]);

  return (
    <div ref={track} className={shared.photoTrack}>
      <div className={shared.photoStage}>
        <figure className={shared.photoFrame}>
          <Image
            src={photo.src}
            width={photo.width}
            height={photo.height}
            alt={copy(photo.alt)}
            sizes="(min-width: 1100px) 72vw, 100vw"
            data-photo
          />
          <span className={shared.photoShade} aria-hidden="true" data-photo-shade />
          <figcaption className={shared.photoLine} data-photo-line>
            {copy(photo.line)}
          </figcaption>
        </figure>
      </div>
    </div>
  );
}

function PaperStage({
  why,
  titleId,
  reduced,
}: {
  why: ProductWhy;
  titleId: string;
  reduced: boolean;
}) {
  const copy = useCopy();
  const track = useRef<HTMLDivElement>(null);
  const beats = why.lines.length + 1;

  // One scrubbed timeline over a tall track with a pinned (sticky) stage. Wide screens build the
  // list line by line, the earlier lines settling to a quieter colour; smaller screens show one
  // line at a time in the same place. The title comes last.
  useEffect(() => {
    const element = track.current;
    if (reduced || !element) return;
    gsap.registerPlugin(ScrollTrigger, SplitText);
    let cancelled = false;
    const mm = gsap.matchMedia(element);
    const muted = getComputedStyle(element).getPropertyValue("--muted").trim() || "#5b6672";
    void document.fonts.ready.then(() => {
      if (cancelled) return;
      // Only where the stage is pinned (see the CSS); shorter windows keep everything in view.
      const tall = "(min-height: 561px)";
      mm.add(
        { wide: `(min-width: 1100px) and ${tall}`, narrow: `(max-width: 1099px) and ${tall}` },
        (context) => {
          const wide = Boolean(context.conditions?.wide);
          const lines = gsap.utils.toArray<HTMLElement>("[data-why-line]", element);
          const title = element.querySelector<HTMLElement>("[data-why-title]");
          const split = title
            ? SplitText.create(title, { type: "lines", mask: "lines", linesClass: lineClass })
            : null;
          // It starts while the stage is still rising into place, so the stage never arrives empty.
          const timeline = gsap.timeline({
            defaults: { ease: "power2.out" },
            scrollTrigger: { trigger: element, start: "top 55%", end: "bottom bottom", scrub: 0.8 },
          });
          let at = 0;
          lines.forEach((line, index) => {
            const previous = lines[index - 1];
            if (previous && wide) timeline.to(previous, { color: muted, duration: 0.5 }, at);
            // Taking turns: the line before has fully gone before the next one arrives.
            if (previous && !wide) {
              timeline.to(previous, { opacity: 0, y: -18, duration: 0.35, ease: "power1.in" }, at);
              at += 0.4;
            }
            timeline.fromTo(line, { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: 0.7 }, at);
            at += 1.15;
          });
          if (split) {
            timeline.fromTo(
              split.lines,
              { yPercent: 130 },
              { yPercent: 0, duration: 0.8, stagger: 0.14, ease: "power3.out" },
              at,
            );
          }
          timeline.to({}, { duration: 0.7 });
        },
      );
    });
    return () => {
      cancelled = true;
      mm.revert();
    };
  }, [reduced]);

  return (
    <div ref={track} className={shared.whyTrack} style={{ "--beats": beats } as CSSProperties}>
      <div className={shared.whyStage}>
        <p className={shared.whyLabel}>{copy(why.label)}</p>
        <div className={shared.whyBody}>
          <ol className={shared.whyLines}>
            {why.lines.map((line, index) => (
              <li key={index} className={shared.whyLine} data-why-line>
                <span className={shared.whyIndex} aria-hidden="true">
                  {index + 1}
                </span>
                <p>{copy(line)}</p>
              </li>
            ))}
          </ol>
        </div>
        <h2 id={titleId} className={shared.whyTitle} data-why-title>
          {copy(why.title)}
        </h2>
      </div>
    </div>
  );
}
