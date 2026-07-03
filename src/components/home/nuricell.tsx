import Image from "next/image";

import { Reveal } from "@/components/clone/reveal";
import { Link } from "@/i18n/navigation";
import { imageDims } from "@/lib/images";

// The measured legacy bottle render — same asset the clone home used.
const BOTTLE = "/original/uploads/2019/03/1140_1183_nuri1-987x1024.png";

// Screen 4 · NURICELL — the hero product, introduced only after the trust
// moment. Stacked story: pedigree → the golden ratio (dose as a virtue) →
// familiar ingredients → 20-year heritage.
// COMPLIANCE: heritage is a market track record ("trusted"), never proof;
// dose language never implies under-dosing or medical results.
export function Nuricell({
  name,
  lead,
  dose,
  doseBody,
  ingredients,
  heritage,
  cta,
}: {
  name: string;
  lead: string;
  dose: string;
  doseBody: string;
  ingredients: string;
  heritage: string;
  cta: string;
}) {
  return (
    <section
      id="nuricell"
      className="relative scroll-mt-24 border-t border-[color:var(--gh-line)] px-6 py-28 sm:px-12 sm:py-36"
    >
      <div className="mx-auto grid max-w-6xl items-center gap-12 md:grid-cols-[1.15fr_0.85fr] md:gap-16">
        <div>
          <Reveal>
            <p className="font-mono text-[12px] uppercase tracking-[0.24em] text-[color:var(--gh-faint)]">
              {lead}
            </p>
          </Reveal>
          <Reveal delay={60}>
            <h2 className="gh-serif mt-6 text-[clamp(2.6rem,5vw,4.2rem)] leading-[1.02]">
              {name}
            </h2>
          </Reveal>
          <Reveal delay={120}>
            <p className="gh-serif mt-9 max-w-xl text-[clamp(1.5rem,2.8vw,2.2rem)] leading-[1.3] text-[color:var(--gh-fg)]">
              {dose}
            </p>
          </Reveal>
          <Reveal delay={180}>
            <p className="mt-5 max-w-xl text-[17px] leading-[1.8] text-[color:var(--gh-muted)]">
              {doseBody}
            </p>
          </Reveal>
          <Reveal delay={240}>
            <p className="mt-5 max-w-xl text-[17px] leading-[1.8] text-[color:var(--gh-muted)]">
              {ingredients}
            </p>
          </Reveal>
          <Reveal delay={300}>
            <p className="mt-9 inline-block border border-[color:var(--gh-line)] px-4 py-2 text-[12px] uppercase tracking-[0.2em] text-[color:var(--gh-ember)]">
              {heritage}
            </p>
          </Reveal>
          <Reveal delay={360}>
            <div>
              <Link
                href="/nuricell"
                className="group mt-10 inline-flex w-fit items-center gap-3 font-mono text-[13px] uppercase tracking-[0.22em]"
              >
                <span className="border-b border-[color:var(--gh-fg)] pb-1 transition-colors group-hover:border-[color:var(--gh-ember)] group-hover:text-[color:var(--gh-ember)]">
                  {cta}
                </span>
                <span className="transition-transform duration-300 group-hover:translate-x-1.5">
                  →
                </span>
              </Link>
            </div>
          </Reveal>
        </div>

        {/* bottle, lifted on a warm glow */}
        <Reveal delay={150}>
          <div className="relative mx-auto w-full max-w-[22rem]">
            <div
              aria-hidden
              className="absolute inset-0 -z-10 rounded-full bg-[radial-gradient(closest-side,rgba(233,148,106,0.18),transparent)] blur-2xl"
            />
            <Image
              src={BOTTLE}
              alt={name}
              {...imageDims(BOTTLE)}
              className="h-auto w-full drop-shadow-[0_24px_48px_rgba(0,0,0,0.55)]"
              sizes="(max-width: 768px) 70vw, 350px"
            />
          </div>
        </Reveal>
      </div>
    </section>
  );
}
