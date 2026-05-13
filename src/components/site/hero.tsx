"use client";

import Image from "next/image";
import { motion } from "motion/react";
import { useTranslations } from "next-intl";

import { Button } from "@/components/ui/button";

const ease = [0.2, 0.7, 0.2, 1] as const;

export function Hero() {
  const t = useTranslations("Hero");

  return (
    <section className="relative isolate min-h-screen overflow-hidden bg-cream-50">
      <motion.div
        initial={{ scale: 1, x: 0 }}
        animate={{ scale: 1.045, x: "-1%" }}
        transition={{
          duration: 26,
          repeat: Infinity,
          repeatType: "mirror",
          ease: "easeInOut",
        }}
        className="absolute inset-0 -z-10"
      >
        <Image
          src="/hero/hero-76-star-trails-ridge.jpg"
          alt={t("imageAlt")}
          fill
          priority
          sizes="100vw"
          className="object-cover object-right"
        />
      </motion.div>

      <div
        aria-hidden="true"
        className="absolute inset-0 -z-10 hidden md:block"
        style={{
          background:
            "linear-gradient(100deg, rgba(250,246,239,0.96) 0%, rgba(250,246,239,0.92) 28%, rgba(250,246,239,0.55) 48%, rgba(250,246,239,0.10) 62%, rgba(250,246,239,0.00) 78%)",
        }}
      />
      <div
        aria-hidden="true"
        className="absolute inset-0 -z-10 md:hidden"
        style={{
          background:
            "linear-gradient(180deg, rgba(250,246,239,0.97) 0%, rgba(250,246,239,0.92) 32%, rgba(250,246,239,0.50) 56%, rgba(250,246,239,0.05) 78%)",
        }}
      />

      <div className="relative mx-auto grid min-h-[calc(100vh-6rem)] max-w-[1320px] grid-cols-1 items-center gap-14 px-6 py-16 md:grid-cols-2 md:px-14 md:py-24">
        <div className="max-w-[540px]">
          <motion.h1
            initial={{ opacity: 0, y: 14 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.9, delay: 0.32, ease }}
            className="font-display text-espresso m-0 text-[clamp(2.5rem,5.6vw,4.875rem)] font-light leading-[1.02] tracking-[-0.018em]"
            style={{ fontVariationSettings: '"opsz" 144, "SOFT" 40' }}
          >
            {t.rich("headline", {
              br: () => <br />,
              em: (chunks) => (
                <em className="text-sienna font-light not-italic [font-style:italic]">
                  {chunks}
                </em>
              ),
            })}
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.9, delay: 0.58, ease }}
            className="text-espresso-60 mt-7 max-w-[480px] text-[clamp(1.125rem,1.35vw,1.3125rem)] leading-[1.6]"
          >
            {t("subhead")}
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.9, delay: 0.82, ease }}
            className="mt-9 flex flex-wrap items-center gap-5"
          >
            <Button
              size="lg"
              className="bg-espresso text-cream-50 hover:bg-sienna h-auto rounded-full px-7 py-3.5 text-sm font-medium tracking-[0.01em]"
            >
              {t("cta")}
            </Button>
            <Button
              variant="ghost"
              size="lg"
              className="text-espresso hover:text-sienna group h-auto rounded-full px-1 py-3.5 text-sm font-medium tracking-[0.01em] hover:bg-transparent"
            >
              {t("ctaSecondary")}
              <span
                aria-hidden="true"
                className="ml-1 inline-block transition-transform duration-200 group-hover:translate-x-1"
              >
                →
              </span>
            </Button>
          </motion.div>
        </div>

        <div aria-hidden="true" />
      </div>
    </section>
  );
}
