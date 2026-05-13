"use client";

import Image from "next/image";
import { motion } from "motion/react";
import { useTranslations } from "next-intl";
import { ArrowRight } from "lucide-react";

const ease = [0.2, 0.7, 0.2, 1] as const;

type ProductKey = "nuricell" | "nuriclear" | "nuricalm";

const PRODUCTS: { key: ProductKey; image: string }[] = [
  { key: "nuricell", image: "/products/nuricell.jpg" },
  { key: "nuriclear", image: "/products/nuriclear.jpg" },
  { key: "nuricalm", image: "/products/nuricalm.jpg" },
];

export function TheSystem() {
  const t = useTranslations("System");

  return (
    <section className="relative overflow-hidden" style={{ backgroundColor: "#EBD2B7" }}>
      {/* Top white→peach gradient for smooth transition from previous white section */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-x-0 top-0 h-32"
        style={{
          background:
            "linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(255,255,255,0.4) 55%, rgba(255,255,255,0) 100%)",
        }}
      />

      {/* Subtle warm radial glow in center for depth */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0"
        style={{
          background:
            "radial-gradient(ellipse 55% 45% at 50% 38%, rgba(255,255,255,0.25) 0%, rgba(255,255,255,0) 75%)",
        }}
      />

      <div className="relative mx-auto max-w-[1320px] px-6 pt-32 pb-32 md:px-12 md:pt-48 md:pb-44">
        {/* ─────────── EYEBROW ─────────── */}
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.7, ease }}
          className="flex justify-center"
        >
          <div className="inline-flex items-center gap-3">
            <span className="bg-espresso block size-1 rounded-full" />
            <p className="text-espresso/65 font-display text-[0.7rem] font-medium tracking-[0.32em] uppercase">
              {t("eyebrow")}
            </p>
            <span className="bg-espresso block size-1 rounded-full" />
          </div>
        </motion.div>

        {/* ─────────── HEADLINE ─────────── */}
        <motion.h2
          initial={{ opacity: 0, y: 18 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 1.05, delay: 0.15, ease }}
          className="font-display text-espresso mx-auto mt-10 max-w-[16ch] text-center text-[clamp(2.75rem,7vw,6rem)] font-light leading-[1.02] tracking-[-0.022em] md:mt-14"
          style={{ fontVariationSettings: '"opsz" 144, "SOFT" 30' }}
        >
          {t("headlineBefore")}
          <em className="text-sienna font-light italic">
            {t("headlineEmphasis")}
          </em>
          {t("headlineAfter")}
        </motion.h2>

        {/* ─────────── INTRO ─────────── */}
        <motion.p
          initial={{ opacity: 0, y: 14 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 1, delay: 0.3, ease }}
          className="text-espresso/75 mx-auto mt-14 max-w-[680px] text-center text-[clamp(1.0625rem,1.3vw,1.25rem)] leading-[1.7] md:mt-20"
        >
          {t("intro")}
        </motion.p>

        {/* ─────────── PRODUCT GRID ─────────── */}
        <div className="mx-auto mt-24 grid max-w-[1140px] grid-cols-1 gap-12 md:mt-36 md:grid-cols-3 md:gap-8">
          {PRODUCTS.map((product, idx) => (
            <ProductCard
              key={product.key}
              image={product.image}
              name={t(`products.${product.key}.name`)}
              role={t(`products.${product.key}.role`)}
              tagline={t(`products.${product.key}.tagline`)}
              body={t(`products.${product.key}.body`)}
              number={idx + 1}
              delay={idx * 0.15}
            />
          ))}
        </div>

        {/* ─────────── CTA ─────────── */}
        <motion.div
          initial={{ opacity: 0, y: 14 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-40px" }}
          transition={{ duration: 0.95, delay: 0.25, ease }}
          className="mt-24 flex justify-center md:mt-32"
        >
          <a
            href="#"
            className="group bg-espresso text-cream-50 hover:bg-sienna inline-flex items-center gap-3 rounded-full px-7 py-4 text-sm font-medium tracking-[0.02em] transition-all duration-300 ease-out hover:gap-5"
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

function ProductCard({
  image,
  name,
  role,
  tagline,
  body,
  number,
  delay,
}: {
  image: string;
  name: string;
  role: string;
  tagline: string;
  body: string;
  number: number;
  delay: number;
}) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 1, delay, ease }}
      className="group flex flex-col"
    >
      {/* Bottle image */}
      <div className="relative aspect-[4/5] w-full overflow-hidden">
        <Image
          src={image}
          alt={`${name} — ${role}`}
          fill
          sizes="(max-width: 768px) 100vw, 33vw"
          className="object-cover transition-transform duration-[1400ms] ease-out group-hover:scale-[1.025]"
        />
      </div>

      {/* Tiny number + hairline + role row */}
      <div className="mt-7 flex items-center gap-4">
        <span
          className="font-display text-sienna text-base leading-none font-light"
          style={{ fontVariationSettings: '"opsz" 24' }}
        >
          0{number}
        </span>
        <span className="border-espresso/20 block h-px flex-1 border-t" />
        <span className="text-espresso/60 font-display text-[0.7rem] tracking-[0.28em] uppercase">
          {role}
        </span>
      </div>

      {/* Product name */}
      <h3
        className="font-display text-espresso mt-5 text-[clamp(2rem,2.8vw,2.5rem)] leading-[1.1] font-light tracking-[-0.015em]"
        style={{ fontVariationSettings: '"opsz" 96, "SOFT" 40' }}
      >
        {name}
      </h3>

      {/* Italic tagline */}
      <p
        className="font-display text-espresso/70 mt-3 text-base leading-[1.45] font-light italic"
        style={{ fontVariationSettings: '"opsz" 24' }}
      >
        {tagline}
      </p>

      {/* Body description */}
      <p className="text-espresso/65 mt-5 text-[0.95rem] leading-[1.7]">
        {body}
      </p>

      {/* Small "Discover" link */}
      <a
        href="#"
        className="group/link mt-7 inline-flex items-center gap-2 self-start text-sm font-medium text-espresso transition-colors hover:text-sienna"
      >
        <span className="border-espresso/40 group-hover/link:border-sienna border-b pb-0.5 transition-colors">
          Discover {name}
        </span>
        <ArrowRight className="size-3.5 transition-transform duration-300 group-hover/link:translate-x-0.5" />
      </a>
    </motion.article>
  );
}
