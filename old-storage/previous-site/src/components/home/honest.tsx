import { Reveal } from "@/components/clone/reveal";

// Screen 7 · HONEST BY DESIGN — three pledges. In a category full of hype,
// restraint is the pitch.
export function Honest({
  kicker,
  title,
  pledges,
}: {
  kicker: string;
  title: string;
  pledges: { title: string; body: string }[];
}) {
  return (
    <section
      id="honest"
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

        <div className="mt-16 grid gap-10 md:grid-cols-3 md:gap-6">
          {pledges.map((p, i) => (
            <Reveal key={p.title} delay={i * 90}>
              <div className="border-t border-[color:var(--gh-ember)]/50 pt-6">
                <h3 className="gh-serif text-[22px]">{p.title}</h3>
                <p className="mt-3 text-[15px] leading-[1.75] text-[color:var(--gh-muted)]">
                  {p.body}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
