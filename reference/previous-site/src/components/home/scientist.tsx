import { Reveal } from "@/components/clone/reveal";
import { Link } from "@/i18n/navigation";

// Screen 3 · MEET DR. LIU — the trust moment. Photo slot stays a quiet
// placeholder until Mo supplies an approved portrait (featuring a living
// scientist needs his written permission — pre-launch gate).
// COMPLIANCE: factual biography only, no endorsement phrasing; the EASA
// honor is quoted exactly; Iris Wang is not named publicly by her choice.
export function Scientist({
  kicker,
  name,
  honor,
  body,
  quote,
  cta,
}: {
  kicker: string;
  name: string;
  honor: string;
  body: string;
  quote: string;
  cta: string;
}) {
  return (
    <section
      id="scientist"
      className="relative scroll-mt-24 border-t border-[color:var(--gh-line)] px-6 py-28 sm:px-12 sm:py-36"
    >
      <div className="mx-auto grid max-w-6xl items-center gap-12 md:grid-cols-[0.85fr_1.15fr] md:gap-16">
        {/* portrait slot — replaced with the approved photo before launch */}
        <Reveal>
          <figure className="relative mx-auto aspect-[4/5] w-full max-w-[26rem] overflow-hidden rounded-lg border border-[color:var(--gh-line)] bg-gradient-to-b from-[#0a1220] to-[#050a12]">
            <svg
              aria-hidden
              viewBox="0 0 100 125"
              className="absolute inset-0 h-full w-full text-[#16222f]"
              fill="currentColor"
            >
              <circle cx="50" cy="46" r="20" />
              <path d="M14 125c2-26 17-38 36-38s34 12 36 38z" />
            </svg>
            <figcaption className="absolute inset-x-0 bottom-0 border-t border-[color:var(--gh-line)] bg-[#04080f]/70 px-5 py-3 text-[11px] uppercase tracking-[0.22em] text-[color:var(--gh-faint)] backdrop-blur-sm">
              {name}
            </figcaption>
          </figure>
        </Reveal>

        <div>
          <Reveal>
            <p className="font-mono text-[12px] uppercase tracking-[0.24em] text-[color:var(--gh-faint)]">
              {kicker}
            </p>
          </Reveal>
          <Reveal delay={60}>
            <h2 className="gh-serif mt-6 text-[clamp(2.4rem,4.6vw,3.8rem)] leading-[1.05]">
              {name}
            </h2>
          </Reveal>
          <Reveal delay={120}>
            <p className="mt-4 text-[14px] uppercase tracking-[0.14em] text-[color:var(--gh-ember)]">
              {honor}
            </p>
          </Reveal>
          <Reveal delay={180}>
            <p className="mt-7 max-w-xl text-[17px] leading-[1.8] text-[color:var(--gh-muted)]">
              {body}
            </p>
          </Reveal>
          <Reveal delay={240}>
            <blockquote className="gh-serif mt-9 max-w-xl border-l border-[color:var(--gh-ember)] pl-6 text-[clamp(1.3rem,2.2vw,1.7rem)] italic leading-[1.5] text-[color:var(--gh-fg)]">
              {quote}
            </blockquote>
          </Reveal>
          <Reveal delay={300}>
            <Link
              href="/science"
              className="group mt-10 inline-flex w-fit items-center gap-3 font-mono text-[13px] uppercase tracking-[0.22em]"
            >
              <span className="border-b border-[color:var(--gh-fg)] pb-1 transition-colors group-hover:border-[color:var(--gh-ember)] group-hover:text-[color:var(--gh-ember)]">
                {cta}
              </span>
              <span className="transition-transform duration-300 group-hover:translate-x-1.5">
                →
              </span>
            </Link>
          </Reveal>
        </div>
      </div>
    </section>
  );
}
