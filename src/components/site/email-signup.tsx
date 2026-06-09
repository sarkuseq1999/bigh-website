"use client";

import { AnimatePresence, motion } from "motion/react";
import { useReducedMotionSafe } from "@/components/site/use-reduced-motion-safe";
import { useTranslations } from "next-intl";
import { useState } from "react";
import { Reveal } from "@/components/site/reveal";

const EASE = [0.2, 0.7, 0.2, 1] as const;
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
type FormState = "idle" | "submitting" | "success" | "error";

// Subtle attention pulse for the Quiz CTA button
function QuizCta({ label }: { label: string }) {
  const reduce = useReducedMotionSafe();

  if (reduce) {
    return (
      <a
        href="#"
        className="inline-flex min-h-[52px] items-center justify-center rounded-full bg-amber px-10 py-4 font-display text-[1.125rem] font-medium tracking-[-0.01em] text-ink transition-colors duration-200 hover:bg-amber-hi focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-amber"
      >
        {label}
      </a>
    );
  }

  return (
    <motion.a
      href="#"
      animate={{
        scale: [1, 1.02, 1],
        boxShadow: [
          "0 4px 24px 0 rgba(194,138,58,0.18)",
          "0 6px 36px 4px rgba(194,138,58,0.32)",
          "0 4px 24px 0 rgba(194,138,58,0.18)",
        ],
      }}
      transition={{
        duration: 2.8,
        repeat: Infinity,
        ease: "easeInOut",
        repeatType: "loop",
      }}
      className="inline-flex min-h-[52px] items-center justify-center rounded-full bg-amber px-10 py-4 font-display text-[1.125rem] font-medium tracking-[-0.01em] text-ink transition-colors duration-200 hover:bg-amber-hi focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-amber"
    >
      {label}
    </motion.a>
  );
}

/* ─────────────────────────────────────────────────────────────────────────
   Sample Brain Age report — the artifact the quiz promises, shown honestly
   as a sample. Pure SVG: an arc gauge with a serif score.
───────────────────────────────────────────────────────────────────────── */
function BrainAgeSample({
  label,
  value,
  actual,
  note,
}: {
  label: string;
  value: string;
  actual: string;
  note: string;
}) {
  // Arc geometry: a 270° gauge, amber progress ~62%
  const r = 84;
  const c = 2 * Math.PI * r;
  const arcFrac = 0.75; // 270° of the circle is the track
  const progress = 0.62;

  return (
    <div className="relative">
      {/* Deliberate signal ripple — crisp concentric strokes, not a smudge */}
      <svg
        aria-hidden="true"
        viewBox="0 0 480 480"
        className="pointer-events-none absolute left-1/2 top-1/2 -z-10 size-[150%] -translate-x-1/2 -translate-y-1/2"
      >
        {[120, 165, 210].map((rr, i) => (
          <circle
            key={rr}
            cx="240"
            cy="240"
            r={rr}
            fill="none"
            stroke="var(--amber)"
            strokeOpacity={0.22 - i * 0.06}
            strokeWidth="1"
          />
        ))}
      </svg>

      <div className="rounded-2xl border border-line bg-paper px-10 py-9 shadow-[0_8px_40px_rgba(27,26,23,0.07)]">
        <p className="font-mono text-[0.6875rem] uppercase tracking-[0.2em] text-ink-soft text-center">
          {label}
        </p>

        <div className="relative mx-auto mt-4 size-[200px]">
          <svg viewBox="0 0 200 200" className="size-full -rotate-[225deg]">
            {/* track */}
            <circle
              cx="100"
              cy="100"
              r={r}
              fill="none"
              stroke="var(--line)"
              strokeWidth="6"
              strokeLinecap="round"
              strokeDasharray={`${c * arcFrac} ${c}`}
            />
            {/* progress */}
            <circle
              cx="100"
              cy="100"
              r={r}
              fill="none"
              stroke="var(--amber)"
              strokeWidth="6"
              strokeLinecap="round"
              strokeDasharray={`${c * arcFrac * progress} ${c}`}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="font-display text-[4rem] font-light leading-none tracking-[-0.02em] text-ink">
              {value}
            </span>
            <span className="mt-2 font-mono text-[0.6875rem] uppercase tracking-[0.16em] text-ink-soft">
              {actual}
            </span>
          </div>
        </div>

        <p className="mt-5 text-center font-mono text-[0.625rem] uppercase tracking-[0.2em] text-ink-soft/80">
          {note}
        </p>
      </div>
    </div>
  );
}

export function EmailSignup() {
  const t = useTranslations("SoftEntry");
  const [email, setEmail] = useState("");
  const [state, setState] = useState<FormState>("idle");

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!EMAIL_RE.test(email)) {
      setState("error");
      return;
    }
    setState("submitting");
    window.setTimeout(() => setState("success"), 700);
  }

  return (
    <section id="quiz" className="relative overflow-hidden bg-paper-2 py-24 md:py-32">
      <div className="relative mx-auto max-w-[1100px] px-6 md:px-14">

        {/* ── Two-zone: the ask, and the artifact it buys ── */}
        <div className="grid grid-cols-1 items-center gap-14 md:grid-cols-[1.2fr_1fr] md:gap-20">

          {/* LEFT — question + CTA */}
          <div>
            <Reveal>
              <p className="font-mono text-[0.7rem] uppercase tracking-[0.2em] text-ink-soft">
                {t("eyebrow")}
              </p>
            </Reveal>

            <Reveal delay={0.1}>
              <h2 className="mt-6 font-display text-[clamp(2.25rem,4vw,3.75rem)] font-light leading-[1.08] tracking-[-0.02em] text-ink">
                {t("headline")}
              </h2>
            </Reveal>

            <Reveal delay={0.2}>
              <p className="mt-6 max-w-[46ch] text-[1.125rem] leading-[1.7] text-ink-soft">
                {t("subhead")}
              </p>
            </Reveal>

            <Reveal delay={0.3} className="mt-10">
              <QuizCta label={t("quizCta")} />
            </Reveal>

            <Reveal delay={0.38}>
              <p className="mt-4 font-mono text-[0.6875rem] uppercase tracking-[0.16em] text-ink-soft">
                {t("trust")}
              </p>
            </Reveal>
          </div>

          {/* RIGHT — the sample report */}
          <Reveal delay={0.25} className="justify-self-center md:justify-self-end">
            <BrainAgeSample
              label={t("sample.label")}
              value={t("sample.value")}
              actual={t("sample.actual")}
              note={t("sample.note")}
            />
          </Reveal>
        </div>

        {/* ── Newsletter — the "not ready yet? stay close" path ── */}
        <Reveal delay={0.2} className="mt-20 md:mt-24">
          <div className="mx-auto max-w-[560px] rounded-2xl border border-line bg-paper px-8 py-8 text-center">
            <p className="font-display text-[1.25rem] font-medium text-ink">
              {t("newsletter.title")}
            </p>
            <p className="mt-2 text-[1rem] leading-[1.6] text-ink-soft">
              {t("newsletter.line")}
            </p>

            {/* Form */}
            <form
              onSubmit={handleSubmit}
              aria-live="polite"
              className="mt-6"
              noValidate
            >
              <AnimatePresence mode="wait" initial={false}>
                {state === "success" ? (
                  <motion.div
                    key="success"
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -6 }}
                    transition={{ duration: 0.45, ease: EASE }}
                    className="flex items-center justify-center gap-2 py-3 text-[1.125rem] text-ink"
                  >
                    <span
                      aria-hidden="true"
                      className="flex size-6 shrink-0 items-center justify-center rounded-full bg-amber text-[0.75rem] text-ink"
                    >
                      ✓
                    </span>
                    <span className="font-display font-light">
                      Thanks — you&apos;re in.
                    </span>
                  </motion.div>
                ) : (
                  <motion.div
                    key="form"
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -6 }}
                    transition={{ duration: 0.45, ease: EASE }}
                    className="flex flex-col gap-3 sm:flex-row"
                  >
                    <input
                      type="email"
                      required
                      value={email}
                      onChange={(e) => {
                        setEmail(e.target.value);
                        if (state === "error") setState("idle");
                      }}
                      placeholder={t("newsletter.placeholder")}
                      aria-label={t("newsletter.cta")}
                      aria-invalid={state === "error"}
                      className={`min-h-[48px] flex-1 rounded-full border bg-paper px-5 text-[1rem] text-ink placeholder:text-ink-soft/60 outline-none transition-colors duration-200 focus-visible:border-amber focus-visible:ring-2 focus-visible:ring-amber/30 ${
                        state === "error"
                          ? "border-amber"
                          : "border-ink/15"
                      }`}
                    />
                    {/* Quiet outline button — the quiz keeps the only gold */}
                    <button
                      type="submit"
                      disabled={state === "submitting"}
                      className="min-h-[48px] rounded-full border border-ink/25 px-6 text-[1rem] font-medium text-ink transition-colors duration-200 hover:border-ink hover:bg-ink/5 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ink disabled:opacity-60"
                    >
                      {state === "submitting" ? (
                        <span
                          aria-hidden="true"
                          className="inline-block size-4 animate-spin rounded-full border-2 border-ink/30 border-t-ink"
                        />
                      ) : (
                        t("newsletter.cta")
                      )}
                    </button>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Inline error */}
              {state === "error" && (
                <p
                  role="alert"
                  className="mt-2 font-mono text-[0.7rem] uppercase tracking-[0.12em] text-ink-soft"
                >
                  Please enter a valid email address.
                </p>
              )}
            </form>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
