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

// MOCKUPS for Mo (November 6, 2026): ideas for "Proudly made in California." without the
// bottles (Mo: "I'd rather not have the product bottle there"), shown with /about?made=a..f
// (round 1 a, b, c; Mo asked for more the same day: round 2 d, e, f).
// English only; the words are the draft's. The page's blooms are found once, on mount, so these
// paintings (picked after it) show whole, unbloomed. Pictures: reference/ink-pages/about-made/.

const SIZES = "(max-width: 959px) 92vw, 620px";

// "waiting" until the element is `share` in view, then "on" (once).
function useArrive<T extends HTMLElement>(share: number) {
  const ref = useRef<T>(null);
  const [state, setState] = useState<"waiting" | "on">("waiting");
  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        observer.disconnect();
        setState("on");
      },
      { threshold: share },
    );
    observer.observe(element);
    return () => observer.disconnect();
  }, [share]);
  return [ref, state] as const;
}

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
  const [book, write] = useArrive<HTMLElement>(0.45);
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

// ---- Round 2 -----------------------------------------------------------------------------------

// D: the checks in the sun. A clipboard on a sunlit stucco wall, a palm's shadow across it: as it
// comes into view, a gold tick is brushed into each of its three boxes, one after another, one
// for each rule.
function WallIdea() {
  const copy = useCopy();
  const [wall, tick] = useArrive<HTMLElement>(0.5);
  return (
    <Part idea="d">
      <div className={`${base.wrap} ${page.spread}`} data-side="right">
        <figure
          ref={wall}
          className={`${page.painting} ${mock.wall}`}
          data-picture=""
          data-tick={tick}
        >
          <span className={`${page.paintingBody} ${mock.wallBody}`}>
            <Image
              className={base.ink}
              src={art.wall.src}
              alt="A clipboard hanging on a sunlit white stucco wall, a palm's shadow across it, three gold ticks in its boxes"
              width={art.wall.width}
              height={art.wall.height}
              sizes={SIZES}
            />
            <svg
              className={mock.over}
              viewBox={`0 0 ${art.wall.width} ${art.wall.height}`}
              aria-hidden="true"
            >
              {art.wall.boxes.map(([x, y, w, h], i) => (
                <path
                  key={i}
                  className={mock.tick}
                  pathLength={1}
                  style={{ ["--n" as string]: i, strokeWidth: w * 0.22 }}
                  d={`M${x + w * 0.1} ${y + h * 0.5} Q${x + w * 0.3} ${y + h * 0.7} ${x + w * 0.42} ${y + h * 0.92} Q${x + w * 0.75} ${y + h * 0.2} ${x + w * 1.3} ${y - h * 0.38}`}
                />
              ))}
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

// E: the gold pan. A Gold Rush pan at the edge of a Sierra creek, a few flakes of gold leaf caught
// in it: California's oldest kind of careful sorting.
function PanIdea() {
  const copy = useCopy();
  return (
    <Part idea="e">
      <div className={`${base.wrap} ${page.spread}`} data-side="right">
        <figure className={`${page.painting} ${mock.pan}`} data-picture="">
          <span className={page.paintingBody}>
            <Image
              className={base.ink}
              src={art.pan.src}
              alt="A Gold Rush pan resting at the edge of a clear Sierra Nevada creek, a few flakes of gold caught in it"
              width={art.pan.width}
              height={art.pan.height}
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

// F: the valley at dawn. One painting across the chapter, California's Central Valley in the first
// light, a few of its fields in gold leaf: the heading in its empty sky, the rules in a row under
// it.
function ValleyIdea() {
  const copy = useCopy();
  return (
    <Part idea="f">
      <div className={base.wrap}>
        <figure className={mock.valley} data-picture="">
          <span className={mock.valleyBody}>
            <Image
              className={base.ink}
              src={art.valley.src}
              alt="Early morning over California's Central Valley from a golden foothill: rows of fields, some in gold, the snowy Sierra behind"
              width={art.valley.width}
              height={art.valley.height}
              sizes="(max-width: 1440px) 92vw, 1300px"
            />
            <span className={mock.sky}>
              <Words>
                <p className={`${page.body} ${more.lead}`}>{copy(about.home.text)}</p>
              </Words>
            </span>
          </span>
          <figcaption className={base.caption}>{copy(drafts.illustration)}</figcaption>
        </figure>
        <div className={mock.row}>
          <p className={more.gmp}>{copy(about.home.gmp)}</p>
          <ul>
            {about.home.rules.map((rule) => (
              <li key={rule}>{copy(rule)}</li>
            ))}
          </ul>
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
  if (idea === "d") return <WallIdea />;
  if (idea === "e") return <PanIdea />;
  if (idea === "f") return <ValleyIdea />;
  return <>{fallback}</>;
}
