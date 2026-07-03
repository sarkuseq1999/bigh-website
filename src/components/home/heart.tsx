import { Reveal } from "@/components/clone/reveal";

// Screen 6 · MADE WITH HEART — the warmth peak. Filial care + gifting,
// the frame BiGH's real (Korean/Asian) buyers respond to. Imagery slot
// stays a warm gradient until Mo picks on-culture family photography.
export function Heart({ title, body }: { title: string; body: string }) {
  return (
    <section
      id="heart"
      className="relative scroll-mt-24 overflow-hidden border-t border-[color:var(--gh-line)]"
    >
      {/* warm imagery slot — swap for multi-generational photography */}
      <div
        aria-hidden
        className="absolute inset-0 bg-[radial-gradient(120%_90%_at_50%_110%,rgba(233,148,106,0.16),rgba(233,148,106,0.05)_45%,transparent_75%)]"
      />
      <div className="relative mx-auto max-w-4xl px-6 py-36 text-center sm:px-12 sm:py-48">
        <Reveal>
          <h2 className="gh-serif text-[clamp(2.6rem,6vw,5rem)] leading-[1.05]">
            {title}
          </h2>
        </Reveal>
        <Reveal delay={120}>
          <p className="mx-auto mt-8 max-w-xl text-[clamp(1.05rem,1.8vw,1.3rem)] leading-[1.8] text-[color:var(--gh-muted)]">
            {body}
          </p>
        </Reveal>
      </div>
    </section>
  );
}
