"use client";

import { useRef } from "react";
import Image from "next/image";
import { motion, useReducedMotion } from "motion/react";
import { useTranslations } from "next-intl";
import { ArrowRight } from "lucide-react";

const ease = [0.2, 0.7, 0.2, 1] as const;

/* ──────────────────────────────────────────────────────────────────────── */
/* AuroraBackground — looping aurora video with a still fallback under      */
/* reduced motion. The still also serves as the video's poster (visible     */
/* during initial fetch). A dark gradient overlay sits above the media for  */
/* type legibility on the lower-left content stack.                          */
/* ──────────────────────────────────────────────────────────────────────── */

function AuroraBackground({
  reduce,
  imageAlt,
}: {
  reduce: boolean;
  imageAlt: string;
}) {
  return (
    <>
      {reduce ? (
        <Image
          src="/hero/candidate-aurora.jpg"
          alt={imageAlt}
          fill
          priority
          sizes="100vw"
          className="absolute inset-0 -z-10 object-cover"
        />
      ) : (
        <video
          autoPlay
          muted
          loop
          playsInline
          preload="auto"
          poster="/hero/candidate-aurora.jpg"
          aria-hidden="true"
          className="absolute inset-0 -z-10 h-full w-full object-cover"
        >
          <source src="/hero/aurora-loop-1.5x.mp4" type="video/mp4" />
        </video>
      )}

      {/* Dark gradient overlay for legibility — z-0 so it sits above the
          media (which is -z-10) but below the content (which is z-10).     */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 z-0"
        style={{
          background:
            "linear-gradient(95deg, rgba(15,10,25,0.85) 0%, rgba(15,10,25,0.55) 28%, rgba(15,10,25,0.12) 52%, transparent 72%), linear-gradient(180deg, transparent 50%, rgba(15,10,25,0.55) 100%)",
        }}
      />
    </>
  );
}

/* ──────────────────────────────────────────────────────────────────────── */
/* ScrollCue — small uppercase label + hairline at the bottom-center.       */
/* Hidden under reduced motion (the cue implies motion).                     */
/* ──────────────────────────────────────────────────────────────────────── */

function ScrollCue({ label, reduce }: { label: string; reduce: boolean }) {
  if (reduce) return null;
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.9, delay: 1.4, ease }}
      className="absolute bottom-6 left-1/2 z-10 -translate-x-1/2 text-center"
      aria-hidden="true"
    >
      <span className="text-cream-50/50 text-[10px] tracking-[0.32em] uppercase">
        {label}
      </span>
      <span className="bg-cream-50/35 mx-auto mt-2 block h-[18px] w-px" />
    </motion.div>
  );
}

/* ──────────────────────────────────────────────────────────────────────── */
/* Hero — homepage section 1. Brand-statement manifesto with looping aurora */
/* video background and a lower-left content stack revealed in sequence on  */
/* mount. The CTA scrolls smoothly to the YourMind section (`#yourmind`).    */
/*                                                                          */
/* `data-dark-context` is read by SiteHeader (via IntersectionObserver) to  */
/* switch the header into its dark-context visual mode while the hero is in */
/* view.                                                                     */
/* ──────────────────────────────────────────────────────────────────────── */

export function Hero() {
  const t = useTranslations("Hero");
  const reduce = useReducedMotion() ?? false;
  const sectionRef = useRef<HTMLElement>(null);

  /* Motion props for a fade-and-rise element revealed `delay` seconds in.
     Under reduced motion this is empty, so the element renders statically. */
  const reveal = (delay: number) =>
    reduce
      ? {}
      : {
          initial: { opacity: 0, y: 16 },
          animate: { opacity: 1, y: 0 },
          transition: { duration: 0.9, delay, ease },
        };

  const scrollToNext = () => {
    const target = document.getElementById("yourmind");
    const behavior: ScrollBehavior = reduce ? "auto" : "smooth";
    if (target) {
      target.scrollIntoView({ behavior, block: "start" });
    } else {
      window.scrollTo({ top: window.innerHeight, behavior });
    }
  };

  return (
    <section
      ref={sectionRef}
      data-dark-context
      className="relative isolate min-h-[100dvh] overflow-hidden bg-[#0a0a1a]"
    >
      <AuroraBackground reduce={reduce} imageAlt={t("imageAlt")} />

      {/* Lower-left content stack. flex justify-end pushes content to the
          bottom of the section; max-width keeps it from spreading across
          the brightest aurora area.                                       */}
      <div className="relative z-10 mx-auto flex min-h-[100dvh] max-w-[1320px] flex-col justify-end px-6 pt-24 pb-20 md:px-14 md:pt-32 md:pb-24">
        <div className="max-w-[640px] md:max-w-[58%]">
          <motion.h1
            {...reveal(0.3)}
            className="font-display text-cream-50 m-0 text-[clamp(2.5rem,6.4vw,4.875rem)] leading-[1.02] font-light tracking-[-0.025em] text-balance"
          >
            {t.rich("headline", {
              em: (chunks) => (
                <em className="text-sienna font-normal not-italic [font-style:italic]">
                  {chunks}
                </em>
              ),
            })}
          </motion.h1>

          <motion.p
            {...reveal(0.7)}
            className="text-cream-50/80 mt-8 max-w-[560px] text-[clamp(0.95rem,1.2vw,1.125rem)] leading-[1.62]"
          >
            {t("subhead")}
          </motion.p>

          <motion.div {...reveal(1.0)} className="mt-9">
            <button
              type="button"
              onClick={scrollToNext}
              className="group bg-cream-50 text-espresso hover:bg-sienna hover:text-cream-50 inline-flex items-center gap-2.5 rounded-full px-7 py-3.5 text-sm font-medium tracking-[0.01em] transition-all duration-300 ease-out hover:-translate-y-px active:translate-y-0 active:scale-[0.98]"
            >
              {t("cta")}
              <ArrowRight
                className="size-4 transition-transform duration-300 group-hover:translate-x-0.5"
                strokeWidth={1.5}
              />
            </button>
          </motion.div>
        </div>
      </div>

      <ScrollCue label={t("scrollCue")} reduce={reduce} />
    </section>
  );
}
