import { Reveal } from "@/components/clone/reveal";
import { Link } from "@/i18n/navigation";

const LOGIN_URL = "https://aeg.imatrixoffice.com";

// Screen 8 · START THE RITUAL — the soft close. A gentle invitation, no
// hard sell; primary → NuriCell, secondary → the direct-sales human path.
export function Ritual({
  title,
  body,
  primary,
  secondary,
}: {
  title: string;
  body: string;
  primary: string;
  secondary: string;
}) {
  return (
    <section
      id="ritual"
      className="relative scroll-mt-24 border-t border-[color:var(--gh-line)] px-6 py-32 text-center sm:px-12 sm:py-40"
    >
      <div className="mx-auto max-w-3xl">
        <Reveal>
          <h2 className="gh-serif text-[clamp(2rem,4.4vw,3.4rem)] leading-[1.15]">
            {title}
          </h2>
        </Reveal>
        <Reveal delay={100}>
          <p className="mx-auto mt-6 max-w-xl text-[17px] leading-[1.8] text-[color:var(--gh-muted)]">
            {body}
          </p>
        </Reveal>
        <Reveal delay={200}>
          <div className="mt-12 flex flex-col items-center justify-center gap-5 sm:flex-row sm:gap-8">
            <Link
              href="/nuricell"
              className="rounded-full border border-[color:var(--gh-ember)] px-8 py-3.5 text-[13px] uppercase tracking-[0.2em] text-[color:var(--gh-ember)] transition-colors hover:bg-[color:var(--gh-ember)] hover:text-[#04080f]"
            >
              {primary}
            </Link>
            <a
              href={LOGIN_URL}
              className="group inline-flex items-center gap-3 font-mono text-[13px] uppercase tracking-[0.2em] text-[color:var(--gh-muted)] transition-colors hover:text-[color:var(--gh-fg)]"
            >
              <span className="border-b border-[color:var(--gh-line)] pb-1">
                {secondary}
              </span>
              <span className="transition-transform duration-300 group-hover:translate-x-1.5">
                →
              </span>
            </a>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
