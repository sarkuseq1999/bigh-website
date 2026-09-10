import Image from "next/image";

import { Reveal } from "@/components/clone/reveal";
import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { productName, type ProductSlug } from "@/data/products";
import { loadPage, productImages } from "@/lib/content";
import { imageDims } from "@/lib/images";

// The supporting cast, in design-doc order. NuriCell has its own screen.
const FAMILY: ProductSlug[] = [
  "turmerific",
  "advanced-opc-formula",
  "green-bee-propolis",
  "nature-calm",
  "deer-horn-reishi",
];

function cardImage(locale: Locale, slug: ProductSlug): string | null {
  const page = loadPage(locale, slug) ?? loadPage("en", slug);
  if (!page) return null;
  return productImages(page)[0] ?? null;
}

// Screen 5 · THE FAMILY — each product leads with its ONE honest job
// (structure/function support language only), all under aging well.
export function Family({
  locale,
  kicker,
  title,
  jobs,
}: {
  locale: Locale;
  kicker: string;
  title: string;
  jobs: Record<string, string>;
}) {
  return (
    <section
      id="family"
      className="relative scroll-mt-24 border-t border-[color:var(--gh-line)] px-6 py-28 sm:px-12 sm:py-36"
    >
      <div className="mx-auto max-w-6xl">
        <Reveal>
          <p className="font-mono text-[12px] uppercase tracking-[0.24em] text-[color:var(--gh-faint)]">
            {kicker}
          </p>
        </Reveal>
        <Reveal delay={80}>
          <h2 className="gh-serif mt-6 max-w-2xl text-[clamp(1.8rem,3.6vw,2.8rem)] leading-[1.25]">
            {title}
          </h2>
        </Reveal>

        <ul className="mt-16 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {FAMILY.map((slug, i) => {
            const img = cardImage(locale, slug);
            return (
              <li key={slug}>
                <Reveal delay={i * 70}>
                  <Link
                    href={`/${slug}`}
                    className="group flex h-full flex-col rounded-lg border border-[color:var(--gh-line)] bg-white/[0.02] p-7 transition-colors hover:border-[color:var(--gh-ember)]/60 hover:bg-white/[0.04]"
                  >
                    {img && (
                      <Image
                        src={img}
                        alt={productName(slug, locale)}
                        {...imageDims(img)}
                        className="mx-auto h-36 w-auto object-contain drop-shadow-[0_12px_24px_rgba(0,0,0,0.45)] transition-transform duration-500 group-hover:scale-[1.04]"
                        sizes="160px"
                      />
                    )}
                    <h3 className="gh-serif mt-7 text-[22px] leading-tight">
                      {productName(slug, locale)}
                    </h3>
                    <p className="mt-3 text-[14.5px] leading-[1.7] text-[color:var(--gh-muted)]">
                      {jobs[slug]}
                    </p>
                    <span
                      aria-hidden
                      className="mt-auto pt-5 font-mono text-[12px] tracking-[0.2em] text-[color:var(--gh-faint)] transition-colors group-hover:text-[color:var(--gh-ember)]"
                    >
                      →
                    </span>
                  </Link>
                </Reveal>
              </li>
            );
          })}
        </ul>
      </div>
    </section>
  );
}
