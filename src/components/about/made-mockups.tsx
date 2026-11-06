"use client";

import Image from "next/image";
import { useEffect, useRef, useState, useSyncExternalStore, type ReactNode } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { about, drafts } from "./about-content";
import page from "./about-page.module.css";
import more from "./chapters.module.css";
import { madeArt as art } from "./made-art";
import mock from "./made-mockups.module.css";

// MOCKUPS for Mo (November 6, 2026): three ideas for "Proudly made in California." without the
// bottles (Mo: "I'd rather not have the product bottle there"), shown with /about?made=a|b|c.
// English only; the words are the draft's. The page's blooms are found once, on mount, so these
// paintings (picked after it) show whole, unbloomed. Pictures: reference/ink-pages/about-made/.

const SIZES = "(max-width: 959px) 92vw, 620px";

function Words({ children }: { children?: ReactNode }) {
  const copy = useCopy();
  return (
    <>
      <p className={`${base.label} ${page.label}`} data-label="">
        {copy(about.home.label)}
      </p>
      <h2 id="home-title" className={`${base.display} ${page.heading}`}>
        {copy(about.home.title)}
      </h2>
      {children}
    </>
  );
}

function Rules() {
  const copy = useCopy();
  return (
    <>
      <p className={`${page.body} ${more.lead}`}>{copy(about.home.text)}</p>
      <p className={more.gmp}>{copy(about.home.gmp)}</p>
      <ul className={more.rules}>
        {about.home.rules.map((rule) => (
          <li key={rule}>{copy(rule)}</li>
        ))}
      </ul>
    </>
  );
}

function Part({ idea, children }: { idea: string; children: ReactNode }) {
  return (
    <section
      id="home"
      className={page.part}
      data-part="home"
      data-made={idea}
      aria-labelledby="home-title"
    >
      {children}
    </section>
  );
}

// A: the crate label. An old California fruit crate's label (an orange grove under the Sierra, a
// gold-leaf sun), our name in its banner, the way California's growers named what they packed.
function CrateIdea() {
  const copy = useCopy();
  return (
    <Part idea="a">
      <div className={`${base.wrap} ${page.spread}`} data-side="right">
        <figure className={`${page.painting} ${mock.crate}`} data-picture="">
          <span className={`${page.paintingBody} ${mock.crateBody}`}>
            <Image
              className={base.ink}
              src={art.crate.src}
              alt="An old wooden fruit crate from California, its label painted with an orange grove under the snowy Sierra Nevada and a gold sun"
              width={art.crate.width}
              height={art.crate.height}
              sizes={SIZES}
            />
            <svg
              className={mock.over}
              viewBox={`0 0 ${art.crate.width} ${art.crate.height}`}
              aria-hidden="true"
            >
              <text className={mock.banner} x="723" y="222" textAnchor="middle">
                Be in Good Health
              </text>
            </svg>
          </span>
          <figcaption className={base.caption}>{copy(drafts.illustration)}</figcaption>
        </figure>
        <div className={page.words} data-words="">
          <Words>
            <Rules />
          </Words>
        </div>
      </div>
    </Part>
  );
}

// The book's ruled lines (their height on the 1536 x 1024 painting, found by
// reference/ink-pages/about-made/ and checked by eye), and what is written on them: the lead and
// GMP on the left page, the three rules on the right, a blank line between. English only, broken
// by hand for the mockup. `n` is the order they are written in.
const RULED = [212, 288, 362, 436, 512, 586, 660, 733];
const LINES = [
  { page: "left", row: 0, n: 0, text: "Every bottle we sell is made" },
  { page: "left", row: 1, n: 0, text: "here, by GMP-certified" },
  { page: "left", row: 2, n: 0, text: "manufacturers." },
  { page: "left", row: 4, n: 1, text: "GMP means Good Manufacturing" },
  { page: "left", row: 5, n: 1, text: "Practice: the rules for making" },
  { page: "left", row: 6, n: 1, text: "supplements with care." },
  { page: "right", row: 0, n: 2, text: "Every ingredient is checked" },
  { page: "right", row: 1, n: 2, text: "before it’s used." },
  { page: "right", row: 3, n: 3, text: "Every batch follows a" },
  { page: "right", row: 4, n: 3, text: "written recipe." },
  { page: "right", row: 6, n: 4, text: "Every batch is recorded," },
  { page: "right", row: 7, n: 4, text: "so it can be traced." },
] as const;

// B: the record book. GMP's own record, open on a redwood table, a pressed poppy in its gutter:
// the chapter's words are written into it, a line at a time, as it comes into view.
function BookIdea() {
  const copy = useCopy();
  const book = useRef<HTMLElement>(null);
  const [write, setWrite] = useState<"waiting" | "on">("waiting");
  useEffect(() => {
    const figure = book.current;
    if (!figure) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        observer.disconnect();
        setWrite("on");
      },
      { threshold: 0.45 },
    );
    observer.observe(figure);
    return () => observer.disconnect();
  }, []);
  return (
    <Part idea="b">
      <div className={`${base.wrap} ${mock.bookWrap}`}>
        <div className={mock.bookWords}>
          <Words>
            {/* Under 900px the book shows its right page only; these lines stand above it. */}
            <div className={mock.outside}>
              <p className={`${page.body} ${more.lead}`}>{copy(about.home.text)}</p>
              <p className={more.gmp}>{copy(about.home.gmp)}</p>
            </div>
          </Words>
        </div>
        <figure ref={book} className={mock.book} data-picture="" data-write={write}>
          <span className={mock.bookBody}>
            <Image
              className={base.ink}
              src={art.ledger.src}
              alt="An open record book on a redwood table, a pressed California poppy in its gutter and a gold ribbon"
              width={art.ledger.width}
              height={art.ledger.height}
              sizes="(max-width: 899px) 240vw, 1100px"
            />
            <svg className={mock.over} viewBox="0 0 1536 1024" aria-hidden="true">
              {LINES.map((line) => (
                <text
                  key={line.text}
                  className={mock.line}
                  x={line.page === "left" ? 200 : 852}
                  y={RULED[line.row] - 12}
                  style={{ ["--n" as string]: line.n }}
                >
                  {line.text}
                </text>
              ))}
            </svg>
          </span>
          <figcaption className={base.caption}>{copy(drafts.illustration)}</figcaption>
        </figure>
        {/* What the book says, for screen readers (the book's own lines are drawn). */}
        <ul className={mock.unseen}>
          {about.home.rules.map((rule) => (
            <li key={rule}>{copy(rule)}</li>
          ))}
        </ul>
      </div>
    </Part>
  );
}

// C: the Golden State. California painted alone over its real outline, the Central Valley laid in
// gold leaf: the place the map's trails end, up close.
function StateIdea() {
  const copy = useCopy();
  return (
    <Part idea="c">
      <div className={`${base.wrap} ${page.spread}`} data-side="right">
        <figure className={`${page.painting} ${mock.state}`} data-picture="">
          <span className={page.paintingBody}>
            <Image
              className={base.ink}
              src={art.state.src}
              alt="The state of California painted in ink and watercolour: fog on the coast, the Sierra's snow, the desert, and the Central Valley in gold"
              width={art.state.width}
              height={art.state.height}
              sizes={SIZES}
            />
          </span>
          <figcaption className={base.caption}>{copy(drafts.illustration)}</figcaption>
        </figure>
        <div className={page.words} data-words="">
          <Words>
            <Rules />
          </Words>
        </div>
      </div>
    </Part>
  );
}

export function MadeMockup({ fallback }: { fallback: ReactNode }) {
  const idea = useSyncExternalStore(
    () => () => {},
    () => new URLSearchParams(window.location.search).get("made"),
    () => null,
  );
  if (idea === "a") return <CrateIdea />;
  if (idea === "b") return <BookIdea />;
  if (idea === "c") return <StateIdea />;
  return <>{fallback}</>;
}
