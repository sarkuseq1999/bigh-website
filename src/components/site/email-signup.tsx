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
    <section id="quiz" className="bg-paper-2 py-24 md:py-40">
      {/* Faint warm amber-tint radial — no glow, just warmth */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-x-0 h-full"
        style={{
          background:
            "radial-gradient(ellipse 60% 55% at 50% 50%, rgba(194,138,58,0.07) 0%, transparent 70%)",
          position: "absolute",
        }}
      />

      <div className="relative mx-auto max-w-[800px] px-6 text-center">
        {/* ── Eyebrow ── */}
        <Reveal>
          <p className="font-mono text-[0.7rem] uppercase tracking-[0.2em] text-ink-soft">
            {t("eyebrow")}
          </p>
        </Reveal>

        {/* ── Headline ── */}
        <Reveal delay={0.1}>
          <h2 className="mt-6 font-display text-[clamp(2.25rem,4vw,3.75rem)] font-light leading-[1.08] tracking-[-0.02em] text-ink">
            {t("headline")}
          </h2>
        </Reveal>

        {/* ── Subhead ── */}
        <Reveal delay={0.2}>
          <p className="mx-auto mt-6 max-w-[560px] text-[1.125rem] leading-[1.7] text-ink-soft">
            {t("subhead")}
          </p>
        </Reveal>

        {/* ── Quiz CTA — the hero element ── */}
        <Reveal delay={0.3} className="mt-12">
          <QuizCta label={t("quizCta")} />
        </Reveal>

        {/* ── Newsletter block — subordinate ── */}
        <Reveal delay={0.45} className="mt-20">
          <div className="mx-auto max-w-[480px] rounded-2xl border border-ink/10 bg-paper-2 px-8 py-8">
            {/* Newsletter title */}
            <p className="font-display text-[1.125rem] font-medium text-ink">
              {t("newsletter.title")}
            </p>
            {/* Reassurance line */}
            <p className="mt-1 font-mono text-[0.7rem] uppercase tracking-[0.15em] text-ink-soft">
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
                      className={`min-h-[48px] flex-1 rounded-xl border bg-paper px-4 text-[1rem] text-ink placeholder:text-ink-soft/60 outline-none transition-colors duration-200 focus-visible:border-amber focus-visible:ring-2 focus-visible:ring-amber/30 ${
                        state === "error"
                          ? "border-amber"
                          : "border-ink/15"
                      }`}
                    />
                    <button
                      type="submit"
                      disabled={state === "submitting"}
                      className="min-h-[48px] rounded-xl bg-amber px-6 text-[1rem] font-medium text-ink transition-colors duration-200 hover:bg-amber-hi focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-amber disabled:opacity-60"
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
