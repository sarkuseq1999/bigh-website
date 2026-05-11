"use client";

import { motion } from "motion/react";
import { useTranslations } from "next-intl";

import { Button } from "@/components/ui/button";

export function Hero() {
  const t = useTranslations("Hero");

  return (
    <section className="relative overflow-hidden">
      <div className="mx-auto max-w-4xl px-6 py-24 text-center sm:py-32 md:py-40">
        <motion.h1
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
          className="text-4xl font-semibold tracking-tight text-balance sm:text-5xl md:text-6xl"
        >
          {t("headline")}
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.12, ease: [0.22, 1, 0.36, 1] }}
          className="text-foreground/65 mx-auto mt-6 max-w-xl text-base text-balance sm:text-lg"
        >
          {t("subhead")}
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.24, ease: [0.22, 1, 0.36, 1] }}
          className="mt-10"
        >
          <Button size="lg" className="h-11 px-6 text-base">
            {t("cta")}
          </Button>
        </motion.div>
      </div>
    </section>
  );
}
