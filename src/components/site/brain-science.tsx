"use client";

import Image from "next/image";
import { animate, motion, useInView, useMotionValue, useTransform } from "motion/react";
import { useTranslations } from "next-intl";
import { useEffect, useRef } from "react";
import { ArrowRight } from "lucide-react";

const ease = [0.2, 0.7, 0.2, 1] as const;

export function BrainScience() {
  const t = useTranslations("Science");

  return (
    <section id="science" className="relative overflow-hidden bg-[#0a0a1a] scroll-mt-24">
      {/* ── Cosmic space background image ── */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0"
        style={{
          backgroundImage: "url('/science/section-background-cosmos.jpg')",
          backgroundSize: "cover",
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat",
        }}
      />

      {/* ── Top fade-in: pure white at the seam with section 2, easing into cosmos ── */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-x-0 top-0 h-[55%]"
        style={{
          background:
            "linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(255,255,255,0.92) 12%, rgba(255,255,255,0.55) 32%, rgba(255,255,255,0.18) 62%, rgba(255,255,255,0) 100%)",
        }}
      />

      {/* ── Bottom fade-out: ease back to white before next section ── */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-x-0 bottom-0 h-[32%]"
        style={{
          background:
            "linear-gradient(0deg, rgba(255,255,255,1) 0%, rgba(255,255,255,0.82) 30%, rgba(255,255,255,0.35) 65%, rgba(255,255,255,0) 100%)",
        }}
      />

      <div className="relative mx-auto max-w-[1240px] px-6 pt-28 pb-32 md:px-12 md:pt-44 md:pb-44">
        {/* ─────────── EYEBROW ─────────── */}
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.7, ease }}
          className="flex justify-center"
        >
          <div className="inline-flex items-center gap-3">
            <span className="bg-sienna-soft block size-1 rounded-full" />
            <p className="text-cream-50/70 font-display text-[0.7rem] font-medium tracking-[0.32em] uppercase">
              {t("eyebrow")}
            </p>
            <span className="bg-sienna-soft block size-1 rounded-full" />
          </div>
        </motion.div>

        {/* ─────────── HEADLINE ─────────── */}
        <motion.h2
          initial={{ opacity: 0, y: 18 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 1.05, delay: 0.15, ease }}
          className="font-display text-cream-50 mx-auto mt-10 max-w-[14ch] text-center text-[clamp(2.875rem,7vw,6.5rem)] font-light leading-[0.98] tracking-[-0.022em] md:mt-14"
          style={{ fontVariationSettings: '"opsz" 144, "SOFT" 30' }}
        >
          {t.rich("headline", {
            br: () => <br />,
            em: (chunks) => (
              <em className="text-sienna-soft font-light italic">{chunks}</em>
            ),
          })}
        </motion.h2>

        {/* ─────────── MITOCHONDRION CENTERPIECE (burning / energized) ─────────── */}
        <MitochondrionStage />

        {/* ─────────── COUNT-UP NUMBER ─────────── */}
        <CountUpBlock
          target={1000}
          suffix={t("countSuffix")}
          label={t("countLabel")}
        />

        {/* ─────────── STATEMENT ─────────── */}
        <motion.p
          initial={{ opacity: 0, y: 14 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 1, delay: 0.2, ease }}
          className="font-display text-cream-50 mx-auto mt-20 max-w-[760px] text-center text-[clamp(1.375rem,2.2vw,1.875rem)] leading-[1.4] font-light tracking-[-0.012em] md:mt-28"
          style={{ fontVariationSettings: '"opsz" 96, "SOFT" 40' }}
        >
          {t("statementBefore")}
          <em className="text-sienna-soft font-light italic">
            {t("statementEmphasis")}
          </em>
          {t("statementAfter")}
        </motion.p>

        {/* ─────────── TWO CONSEQUENCE LINES ─────────── */}
        <div className="mx-auto mt-24 grid max-w-[920px] grid-cols-1 gap-12 md:mt-32 md:grid-cols-2 md:gap-16">
          <ConsequenceBlock
            kind="fuel"
            label={t("fuelLabel")}
            body={t("fuelBody")}
          />
          <ConsequenceBlock
            kind="waste"
            label={t("wasteLabel")}
            body={t("wasteBody")}
          />
        </div>

        {/* ─────────── CTA ─────────── */}
        <motion.div
          initial={{ opacity: 0, y: 14 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-40px" }}
          transition={{ duration: 0.9, delay: 0.25, ease }}
          className="mt-24 flex justify-center md:mt-32"
        >
          <a
            href="#"
            className="group bg-cream-50 text-espresso hover:bg-sienna hover:text-cream-50 inline-flex items-center gap-3 rounded-full px-7 py-4 text-sm font-medium tracking-[0.02em] transition-all duration-300 ease-out hover:gap-5"
          >
            {t("cta")}
            <ArrowRight className="size-4 transition-transform duration-300 group-hover:translate-x-0.5" />
          </a>
        </motion.div>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────────────────────────────── */
/* Mitochondrion with multi-layer burning / energized animation            */
/* ─────────────────────────────────────────────────────────────────────── */

function MitochondrionStage() {
  // 12 particles emitting outward from center at evenly-spaced angles
  const emittingParticles = Array.from({ length: 12 }, (_, i) => ({
    angle: (i / 12) * Math.PI * 2,
    delay: i * 0.35,
  }));

  return (
    <motion.figure
      initial={{ opacity: 0, scale: 0.96 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 1.6, delay: 0.4, ease }}
      className="relative mx-auto mt-20 w-full max-w-[920px] md:mt-28"
    >
      {/* Layer 1: Slow outer breathing aura (life-force rhythm) */}
      <motion.div
        animate={{
          scale: [1, 1.08, 1],
          opacity: [0.55, 0.85, 0.55],
        }}
        transition={{
          duration: 6.5,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 -z-30"
        style={{
          background:
            "radial-gradient(ellipse 75% 65% at 50% 50%, rgba(217,128,92,0.55) 0%, rgba(184,84,38,0.20) 35%, transparent 75%)",
          filter: "blur(48px)",
        }}
      />

      {/* Layer 2: Mid-tier flame-flicker glow (combustion rhythm) */}
      <motion.div
        animate={{
          scale: [0.98, 1.04, 0.995, 1.025, 0.98],
          opacity: [0.4, 0.7, 0.5, 0.65, 0.4],
        }}
        transition={{
          duration: 2.4,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 -z-20"
        style={{
          background:
            "radial-gradient(ellipse 55% 45% at 50% 50%, rgba(255,165,90,0.55) 0%, rgba(217,128,92,0.15) 45%, transparent 70%)",
          filter: "blur(30px)",
        }}
      />

      {/* Layer 3: Inner hot core (close to mitochondrion) */}
      <motion.div
        animate={{
          scale: [0.95, 1.02, 0.97, 1, 0.95],
          opacity: [0.45, 0.75, 0.55, 0.7, 0.45],
        }}
        transition={{
          duration: 1.8,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 -z-10"
        style={{
          background:
            "radial-gradient(ellipse 35% 30% at 50% 50%, rgba(255,210,150,0.45) 0%, rgba(255,165,90,0.18) 50%, transparent 75%)",
          filter: "blur(18px)",
        }}
      />

      {/* The mitochondrion image with brightness flicker (suggests active combustion) */}
      <motion.div
        animate={{
          filter: [
            "brightness(1) saturate(1)",
            "brightness(1.2) saturate(1.18)",
            "brightness(1.05) saturate(1.05)",
            "brightness(1.22) saturate(1.15)",
            "brightness(1) saturate(1)",
          ],
          scale: [1, 1.01, 1.005, 1.015, 1],
        }}
        transition={{
          duration: 3.4,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="relative aspect-video w-full"
      >
        <Image
          src="/science/mitochondrion-hero.jpg"
          alt=""
          fill
          sizes="(max-width: 768px) 100vw, 920px"
          className="object-contain mix-blend-screen"
          priority={false}
        />
      </motion.div>

      {/* Emitting energy particles — radiate outward from center */}
      {emittingParticles.map(({ angle, delay }, i) => (
        <EmittingParticle key={i} angle={angle} delay={delay} />
      ))}
    </motion.figure>
  );
}

/* ─────────────────────────────────────────────────────────────────────── */

function EmittingParticle({ angle, delay }: { angle: number; delay: number }) {
  // Particle starts at center, drifts outward along its angle, then fades
  const dx = Math.cos(angle);
  const dy = Math.sin(angle);
  const travelPx = 220; // how far the particle travels before fading

  return (
    <motion.span
      animate={{
        x: [0, dx * travelPx],
        y: [0, dy * travelPx],
        opacity: [0, 0.9, 0],
        scale: [0.6, 1.1, 0.4],
      }}
      transition={{
        duration: 3.4,
        repeat: Infinity,
        delay,
        ease: "easeOut",
      }}
      aria-hidden="true"
      className="bg-sienna-soft pointer-events-none absolute top-1/2 left-1/2 size-1 rounded-full shadow-[0_0_8px_rgba(217,128,92,0.8)]"
    />
  );
}

/* ─────────────────────────────────────────────────────────────────────── */

function CountUpBlock({
  target,
  suffix,
  label,
}: {
  target: number;
  suffix: string;
  label: string;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-100px" });
  const count = useMotionValue(0);
  const rounded = useTransform(count, (v) => Math.round(v).toLocaleString());

  useEffect(() => {
    if (inView) {
      const controls = animate(count, target, {
        duration: 2.4,
        ease: [0.2, 0.7, 0.2, 1],
      });
      return controls.stop;
    }
  }, [inView, count, target]);

  return (
    <div ref={ref} className="mt-12 flex flex-col items-center md:mt-16">
      <div
        className="font-display text-cream-50 flex items-baseline text-[clamp(4.5rem,11vw,9rem)] leading-none font-light tracking-[-0.035em]"
        style={{ fontVariationSettings: '"opsz" 144, "SOFT" 30' }}
      >
        <motion.span>{rounded}</motion.span>
        <span className="text-sienna-soft ml-1">{suffix}</span>
      </div>
      <motion.p
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true, margin: "-100px" }}
        transition={{ duration: 0.8, delay: 1.8, ease }}
        className="text-cream-50/45 font-display mt-5 text-[0.7rem] tracking-[0.32em] uppercase"
      >
        {label}
      </motion.p>
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────────────── */

function ConsequenceBlock({
  kind,
  label,
  body,
}: {
  kind: "fuel" | "waste";
  label: string;
  body: string;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-60px" }}
      transition={{
        duration: 1,
        delay: kind === "fuel" ? 0.1 : 0.25,
        ease,
      }}
      className="relative flex flex-col items-center text-center md:items-start md:text-left"
    >
      {/* Visual indicator */}
      {kind === "fuel" ? <FuelIndicator /> : <WasteIndicator />}

      <p className="text-cream-50/55 font-display mt-6 text-[0.7rem] font-medium tracking-[0.28em] uppercase">
        {label}
      </p>
      <p
        className="font-display text-cream-50 mt-3 text-[clamp(1.5rem,2.2vw,1.875rem)] leading-tight font-light tracking-[-0.012em]"
        style={{ fontVariationSettings: '"opsz" 96, "SOFT" 40' }}
      >
        {body}
      </p>
    </motion.div>
  );
}

/* ─────────────────────────────────────────────────────────────────────── */

function FuelIndicator() {
  return (
    <div className="flex h-8 items-end gap-1.5">
      {[0.3, 0.45, 0.6, 0.75, 1].map((h, i) => (
        <motion.span
          key={i}
          initial={{ scaleY: 0 }}
          whileInView={{ scaleY: 1 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.5, delay: 0.4 + i * 0.08, ease }}
          className={`block w-1.5 origin-bottom rounded-sm ${
            i === 0 ? "bg-sienna-soft" : "bg-cream-50/15"
          }`}
          style={{ height: `${h * 2}rem` }}
        />
      ))}
    </div>
  );
}

function WasteIndicator() {
  return (
    <div className="relative h-8 w-12">
      {[
        { x: 6, y: 22, d: 0 },
        { x: 18, y: 14, d: 0.2 },
        { x: 30, y: 24, d: 0.4 },
        { x: 24, y: 6, d: 0.6 },
        { x: 38, y: 18, d: 0.8 },
        { x: 12, y: 2, d: 1.0 },
      ].map(({ x, y, d }, i) => (
        <motion.span
          key={i}
          initial={{ opacity: 0, y: 8 }}
          whileInView={{ opacity: [0, 0.65, 0.4], y: [8, y, y - 4] }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 1.6, delay: 0.4 + d, ease, repeat: 0 }}
          className="bg-sienna-soft absolute size-1 rounded-full"
          style={{ left: `${x}px`, top: `${y}px` }}
        />
      ))}
    </div>
  );
}
