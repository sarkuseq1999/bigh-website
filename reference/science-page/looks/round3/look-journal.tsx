"use client";

import Image from "next/image";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ArrowDownRight, ArrowRight, ArrowUpRight, Minus, Plus } from "lucide-react";
import { useEffect, useRef, useState, type CSSProperties } from "react";
import { researchItems } from "@/components/home/research-data";
import { useCopy } from "@/i18n/use-copy";
import { Cite, CiteProvider, journalRefs } from "./journal-cite";
import { newsreader, schibsted } from "./journal-fonts";
import { startJournalMotion } from "./journal-motion";
import type { LookProps, LookTheme } from "./look-types";
import { ResearchGroups } from "./research-library";
import {
  ask,
  formulas,
  formulasLine,
  health,
  iris,
  liu,
  liuNumbers,
  opening,
  pathStops,
  questions,
  research,
} from "./science-content";
import styles from "./look-journal.module.css";

// Look C, "Journal" (round 3, September 28, 2026): the Science page as a science magazine
// feature. Warm newsprint, one cobalt accent, Newsreader and Schibsted Grotesk, figure plates with
// numbered captions, and a real journal convention: inline citations that link to the three key
// studies, set as numbered references. The one moving moment is the cover (headline rising line by
// line while the plate is wiped open) and the chronology sliding sideways (journal-motion.ts).
export const journalTheme: LookTheme = {
  tokens: {
    "--paper": "#f4f1ea",
    "--paper-deep": "#ebe6db",
    "--ink": "#16181d",
    "--muted": "#5f5e58",
    "--body": "#2b2c30",
    "--line": "#d6d0c3",
    "--rule": "#c9c1b0",
    "--blue": "#2149a3",
    "--gold": "#2149a3",
    "--lime": "#dfe4ef",
    "--card-bg": "#faf8f3",
    "--card-line": "#d6d0c3",
    "--door-bg": "#faf8f3",
    // The shared header, footer and story panel sit outside this look's root, so they get the
    // font families themselves (the @font-face rules are global), not the root's CSS variables.
    "--display-font": newsreader.style.fontFamily,
    "--text-font": schibsted.style.fontFamily,
    "--panel-radius": "2px",
  } as CSSProperties,
  footerTone: "light",
};

// DRAFT: the cover's contents, each a link to its part of the page.
const CONTENTS = [
  { href: "#dr-liu", label: "Dr. Jiankang Liu" },
  { href: "#chronology", label: "Chronology" },
  { href: "#formulations", label: "Formulations" },
  { href: "#research", label: "References" },
  { href: "#health", label: "Further reading" },
  { href: "#ask", label: "Letters" },
];

// The golden-hour stills for the chronology (AI illustrations; one caption covers the group).
// Alt texts are DRAFT.
const PLATES: Record<string, { src: string; alt: string }> = {
  Okayama: {
    src: "/images/science-page/golden-okayama.webp",
    alt: "Illustration: a study desk at dusk with old books and an open brain atlas.",
  },
  "1994": {
    src: "/images/science-page/golden-berkeley.webp",
    alt: "Illustration: a laboratory bench with test tubes in evening light, trees outside.",
  },
  "2002": {
    src: "/images/science-page/golden-journal.webp",
    alt: "Illustration: an open science journal with reading glasses and a cup of tea.",
  },
  "2025": {
    src: "/images/science-page/golden-academy.webp",
    alt: "Illustration: a grand academy hall with sunlight falling through tall windows.",
  },
};

const pad = (value: number) => String(value).padStart(2, "0");

export function LookJournal({ onStory }: LookProps) {
  const copy = useCopy();
  const root = useRef<HTMLDivElement>(null);
  const [all, setAll] = useState(false);
  const opened = useRef(false);

  useEffect(() => {
    const element = root.current;
    if (!element) return;
    return startJournalMotion(element);
  }, []);

  // Opening or closing the full list changes the page's height below the chronology.
  useEffect(() => {
    if (!opened.current) {
      opened.current = true;
      return;
    }
    ScrollTrigger.refresh();
  }, [all]);

  const count = String(researchItems.length);
  const seeAll = copy(research.seeAll, { count }).replace("{count}", count);

  return (
    <div ref={root} className={`${styles.journal} ${newsreader.variable} ${schibsted.variable}`}>
      <CiteProvider>
        {/* The cover and Dr. Liu's feature. */}
        <section id="scientists" className={styles.scientists} data-tone="light">
          <div className={styles.cover} data-cover>
            <div className={styles.folio}>
              <span className={styles.folioName} data-folio-text>
                {copy("BiGH Science") /* DRAFT */}
              </span>
              <span className={styles.folioMid} data-folio-text>
                {copy("A feature in six parts") /* DRAFT */}
              </span>
              <span className={styles.folioDate} data-folio-text>
                {copy("Draft edition · September 2026") /* DRAFT */}
              </span>
              <span className={styles.folioRule} aria-hidden="true" data-folio-rule />
            </div>

            <h1 className={styles.coverTitle} data-cover-title>
              <span className={styles.titleLead}>{copy(opening.titleLead)}</span>{" "}
              <span className={styles.titleAccent}>{copy(opening.titleAccent)}</span>
            </h1>

            <div className={styles.coverBody}>
              <div className={styles.coverSide}>
                <p className={styles.standfirst} data-folio-text>
                  {
                    copy(
                      "A feature on Dr. Jiankang Liu: his research, his path from Okayama to Berkeley, and the five formulas behind BiGH.",
                    ) /* DRAFT */
                  }
                </p>
                <nav className={styles.contents} aria-label={copy("Contents")} data-contents>
                  <p className={styles.contentsHead} data-contents-head>
                    {copy("Contents") /* DRAFT */}
                  </p>
                  <ol>
                    {CONTENTS.map((item, index) => (
                      <li key={item.href}>
                        <a href={item.href}>
                          <span className={styles.contentsNo}>{pad(index + 1)}</span>
                          <span className={styles.contentsLabel}>{copy(item.label)}</span>
                          <ArrowDownRight size={17} aria-hidden="true" />
                        </a>
                      </li>
                    ))}
                  </ol>
                </nav>
              </div>

              <figure className={styles.coverFigure}>
                <div className={styles.coverPlate} data-cover-plate>
                  <div className={styles.coverDrift} data-cover-drift>
                    <Image
                      src="/images/science/glass-cell.webp"
                      alt={copy(
                        "Illustration: a mitochondrion rendered in gold glass, its folded inner membrane glowing.", // DRAFT
                      )}
                      fill
                      priority
                      sizes="(max-width: 900px) 92vw, 72vw"
                      className={styles.coverImage}
                      data-cover-image
                    />
                  </div>
                </div>
                <figcaption className={styles.caption} data-cover-caption>
                  <span className={styles.figNo}>{copy("Fig. 1")}</span>
                  {
                    copy(
                      "A mitochondrion, rendered in glass: the part of the cell that turns food into energy.",
                    ) /* DRAFT */
                  }{" "}
                  <span className={styles.illus}>{copy("Illustration.")}</span>
                </figcaption>
              </figure>
            </div>
          </div>

          {/* Dr. Liu's feature: portrait plate, drop cap, pull line, sidebar. */}
          <article id="dr-liu" className={styles.feature}>
            <figure className={styles.portrait} data-portrait>
              <div className={styles.portraitFrame}>
                <Image
                  src={liu.photo.src}
                  alt={copy(liu.name)}
                  fill
                  sizes="(max-width: 900px) 88vw, 440px"
                  className={styles.portraitImage}
                  data-portrait-image
                />
              </div>
              <figcaption className={styles.caption}>
                <span className={styles.figNo}>{copy("Fig. 2")}</span>
                {copy(liu.name)}, {copy(liu.role)}.
              </figcaption>
            </figure>

            <div className={styles.featureText}>
              <h2 className={styles.featureName} data-reveal>
                {copy(liu.name)}
              </h2>
              <p className={styles.featureRole} data-reveal>
                {copy(liu.role)}
              </p>
              <div className={styles.featureBody} data-reveal>
                <p className={styles.dropCap}>
                  {copy(liu.intro)}
                  <Cite n={[1, 2]} />
                </p>
                <p>{copy(liu.purpose)}</p>
              </div>
              <button type="button" className={styles.storyLink} onClick={onStory} data-reveal>
                {copy(liu.button)} <ArrowRight size={19} aria-hidden="true" />
              </button>
            </div>
          </article>

          {/* The approved headline as a display line, not as a quote from him. */}
          <div className={styles.pull} data-reveal>
            <p>{copy(liu.headline)}</p>
          </div>

          <div className={styles.glanceRow}>
            <aside className={styles.glance} aria-labelledby="journal-glance" data-reveal>
              <h3 id="journal-glance" className={styles.glanceHead}>
                {copy("At a glance") /* DRAFT */}
              </h3>
              <dl className={styles.glanceList}>
                {liuNumbers.map((item) => (
                  <div key={item.value} className={styles.glanceItem}>
                    <dt className={styles.glanceValue}>
                      {item.value}
                      {item.suffix}
                    </dt>
                    <dd className={styles.glanceSource}>
                      <a href={item.url} target="_blank" rel="noreferrer" className={styles.source}>
                        {copy("Source")}
                        <ArrowUpRight size={15} aria-hidden="true" />
                      </a>
                    </dd>
                    <dd className={styles.glanceLabel}>{copy(item.label)}</dd>
                  </div>
                ))}
              </dl>
              <p className={styles.glanceNote}>
                {copy(liu.highlights[2].text)}{" "}
                <a
                  href={liu.highlights[2].url}
                  target="_blank"
                  rel="noreferrer"
                  className={styles.source}
                >
                  {copy(liu.highlights[2].link)}
                  <ArrowUpRight size={15} aria-hidden="true" />
                </a>
              </p>
            </aside>

            <figure className={styles.agedFigure} data-reveal>
              <div className={styles.agedPlate}>
                <Image
                  src="/images/science/glass-cell-aged.webp"
                  alt={copy(
                    "Illustration: the same glass mitochondrion, clouded and cracked with age.", // DRAFT
                  )}
                  fill
                  sizes="(max-width: 900px) 92vw, 60vw"
                  className={styles.agedImage}
                />
              </div>
              <figcaption className={styles.caption}>
                <span className={styles.figNo}>{copy("Fig. 3")}</span>
                {copy("The same mitochondrion, aged.") /* DRAFT */} {copy(questions[2].text)}
                <Cite n={3} /> <span className={styles.illus}>{copy("Illustration.")}</span>
              </figcaption>
            </figure>
          </div>
        </section>

        {/* His path, as a chronology: pinned and sliding sideways on wide screens. */}
        <section
          id="chronology"
          className={styles.chron}
          data-tone="light"
          data-chron
          aria-labelledby="journal-chronology"
        >
          {/* The section head stays still above the band; only the stops slide. */}
          <div className={styles.chronHead}>
            <h2 id="journal-chronology" className={styles.chronTitle}>
              {copy("Chronology") /* DRAFT */}
            </h2>
            <p className={styles.chronDeck}>
              {
                copy(
                  "From a doctorate in Japan to a laboratory in California, and on to BiGH.",
                ) /* DRAFT */
              }
            </p>
            <div className={styles.chronAside}>
              <p className={styles.chronNote}>
                {copy("The small plates are illustrations.") /* DRAFT */}
              </p>
              <p className={styles.chronHint} aria-hidden="true">
                {copy("Keep scrolling to follow his path") /* DRAFT */}
                <ArrowRight size={17} />
              </p>
            </div>
          </div>

          <div className={styles.chronTrack} data-chron-track>
            <div className={styles.chronLine} aria-hidden="true">
              <span className={styles.chronFill} data-chron-fill />
            </div>

            {pathStops.map((stop) => {
              const plate = PLATES[stop.mark];
              const year = /^\d+$/.test(stop.mark);
              return (
                <article key={stop.mark} className={styles.stop} data-stop>
                  {plate ? (
                    <div className={styles.stopPlate} data-stop-plate>
                      <Image
                        src={plate.src}
                        alt={copy(plate.alt)}
                        fill
                        sizes="(max-width: 900px) 30vw, 200px"
                      />
                    </div>
                  ) : (
                    <div className={styles.stopPlateSpace} aria-hidden="true" />
                  )}
                  <p className={`${styles.stopMark} ${year ? "" : styles.stopWord}`} data-stop-mark>
                    {copy(stop.mark)}
                  </p>
                  <div className={styles.stopTickSpace} aria-hidden="true">
                    <span className={styles.stopTick} />
                  </div>
                  <h3 className={styles.stopTitle}>{copy(stop.title)}</h3>
                  <p className={styles.stopText}>
                    {copy(stop.text)}
                    {stop.mark === "2002" && <Cite n={1} />}
                  </p>
                  {stop.url ? (
                    <a href={stop.url} target="_blank" rel="noreferrer" className={styles.source}>
                      {copy(stop.link)}
                      <ArrowUpRight size={15} aria-hidden="true" />
                    </a>
                  ) : (
                    <a href="#formulations" className={styles.source}>
                      {copy("Continued in Formulations") /* DRAFT */}
                      <ArrowDownRight size={15} aria-hidden="true" />
                    </a>
                  )}
                </article>
              );
            })}
          </div>
        </section>

        {/* The five formulas as a typographic table, with their credits exactly as approved. */}
        <section id="formulations" className={styles.formulations} data-tone="light">
          <div className={styles.formHead}>
            <h2 className={styles.sectionTitle} data-reveal>
              {copy("Formulations") /* DRAFT */}
            </h2>
            <p className={styles.formLine} data-reveal>
              {copy(formulasLine)}
            </p>
            <div className={styles.contributor} data-reveal>
              <p className={styles.contributorLabel}>{copy("Contributor") /* DRAFT */}</p>
              <p className={styles.contributorName}>{copy(iris.name)}</p>
              <p className={styles.contributorRole}>{copy(iris.role)}</p>
              <p className={styles.contributorText}>{copy(iris.text)}</p>
            </div>
          </div>

          <table className={styles.table}>
            <thead>
              <tr>
                <th scope="col" className={styles.colNo}>
                  {copy("No.") /* DRAFT */}
                </th>
                <th scope="col">{copy("Formula") /* DRAFT */}</th>
                <th scope="col">{copy("Credit") /* DRAFT */}</th>
              </tr>
            </thead>
            <tbody>
              {formulas.map((formula, index) => (
                <tr key={formula.name} data-reveal>
                  <td className={styles.colNo}>{pad(index + 1)}</td>
                  <th scope="row" className={styles.formulaCell}>
                    <span className={styles.formulaInner}>
                      <span className={styles.bottle}>
                        <Image
                          src={formula.image}
                          alt={copy("{name} bottle", { name: formula.name })}
                          fill
                          sizes="112px"
                        />
                      </span>
                      <span className={styles.formulaName}>{formula.name}</span>
                    </span>
                  </th>
                  <td className={styles.credit}>{copy(formula.credit)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        {/* Fig. 4: the one dark plate, full bleed. */}
        <figure className={styles.spread} data-tone="dark" data-spread>
          <div className={styles.spreadMedia} data-spread-media>
            <Image
              src="/images/science-page/dark-cell.webp"
              alt={copy(
                "Illustration: the same glass mitochondrion, glowing gold on deep navy.", // DRAFT
              )}
              fill
              sizes="100vw"
              className={styles.spreadImage}
            />
          </div>
          <figcaption className={styles.spreadCaption}>
            <span className={styles.figNo}>{copy("Fig. 4")}</span>
            <span className={styles.spreadLine}>
              {copy("The same mitochondrion, lit from within.") /* DRAFT */}{" "}
              {copy(questions[0].text)}
            </span>
            <span className={styles.illus}>{copy("Illustration.")}</span>
          </figcaption>
        </figure>

        {/* The three key studies as numbered references; the full list opens on request. */}
        <section id="research" className={styles.references} data-tone="light">
          {/* The sticky heading stays inside this block, so it never rides over the full list. */}
          <div className={styles.refTop}>
            <div className={styles.refHead}>
              <h2 className={styles.refTitle} data-reveal>
                {copy("References") /* DRAFT */}
              </h2>
              <p className={styles.refDeck} data-reveal>
                {copy(research.title)}
              </p>
              <p className={styles.refIntro} data-reveal>
                {copy(research.text)}
              </p>
            </div>

            <ol className={styles.refList}>
              {journalRefs.map((item, index) => (
                <li key={item.url} id={`ref-${index + 1}`} className={styles.refItem} data-reveal>
                  <span className={styles.refNo}>{index + 1}</span>
                  <div>
                    <p className={styles.refCitation}>
                      {copy(item.title)}. <em>{item.journal}</em>, {copy(item.year)}.
                    </p>
                    <p className={styles.refMeta}>
                      {copy(item.category)}
                      {research.byLiu.includes(item.url) && (
                        <span className={styles.refTag}>{copy(research.tag)}</span>
                      )}
                    </p>
                    <p className={styles.refText}>{copy(item.text)}</p>
                    <a href={item.url} target="_blank" rel="noreferrer" className={styles.source}>
                      {copy("Read original source")}
                      <ArrowUpRight size={15} aria-hidden="true" />
                    </a>
                  </div>
                </li>
              ))}
            </ol>

            <div className={styles.refMore}>
              <button
                type="button"
                aria-expanded={all}
                onClick={() => setAll(!all)}
                className={styles.moreButton}
              >
                {all ? copy(research.hideAll) : seeAll}
                {all ? <Minus size={18} /> : <Plus size={18} />}
              </button>
            </div>
          </div>

          {all && (
            <div className={styles.allSources}>
              <ResearchGroups everything />
            </div>
          )}

          <p className={styles.refNote}>{copy(research.note)}</p>
        </section>

        {/* Health explained: the three planned articles as a table of contents. */}
        <section id="health" className={styles.reading} data-tone="light">
          <div className={styles.readingHead}>
            <h2 className={styles.sectionTitle} data-reveal>
              {copy("Further reading") /* DRAFT */}
            </h2>
            <div className={styles.readingIntro} data-reveal>
              <p className={styles.readingDeck}>{copy(health.title)}</p>
              <p>{copy(health.text)}</p>
            </div>
          </div>
          <ol className={styles.toc}>
            {health.doors.map((door, index) => (
              <li key={door.title} data-reveal>
                <article className={styles.tocRow}>
                  <span className={styles.tocNo}>{pad(index + 1)}</span>
                  <div className={styles.tocWords}>
                    <p className={styles.tocTopic}>{copy(door.topic)}</p>
                    <h3 className={styles.tocTitle}>{copy(door.title)}</h3>
                    <p className={styles.tocText}>{copy(door.preview)}</p>
                    <p className={styles.tocSoon}>{copy(health.soon)}</p>
                  </div>
                  <div className={styles.tocPlate} data-kind={index === 1 ? "drop" : "cell"}>
                    <Image src={door.image} alt="" fill sizes="(max-width: 900px) 40vw, 260px" />
                  </div>
                </article>
              </li>
            ))}
          </ol>
        </section>

        {/* Ask BiGH Science, as the magazine's letters page: example letters in three columns,
            how answers are made in a narrow sidebar, the status as an editor's note. No form: it
            is not open yet. */}
        <section id="ask" className={styles.letters} data-tone="light">
          <div className={styles.lettersHead}>
            <p className={styles.lettersWord} data-reveal>
              {copy("Letters") /* DRAFT */}
            </p>
            <div className={styles.lettersStand} data-reveal>
              <h2 className={styles.lettersName}>{copy(ask.title)}</h2>
              <p className={styles.lettersDeck}>{copy(ask.lead)}</p>
              <p className={styles.lettersText}>{copy(ask.text)}</p>
            </div>
          </div>

          <div className={styles.lettersBody}>
            <div className={styles.lettersMain}>
              <div className={styles.lettersBar}>
                <p>{copy(ask.examplesLabel)}</p>
                <p>{copy("These are examples, not letters from readers.") /* DRAFT */}</p>
              </div>
              <div className={styles.letterGrid}>
                {ask.examples.map((question, index) => (
                  <article key={question} className={styles.letter} data-reveal>
                    <p className={styles.letterLabel}>
                      {copy("Example") /* DRAFT */} {index + 1}
                    </p>
                    <p className={styles.letterText}>{copy(question)}</p>
                  </article>
                ))}
              </div>
              <div className={styles.editorNote} data-reveal>
                <p className={styles.editorLabel}>{copy("Editor’s note") /* DRAFT */}</p>
                <p className={styles.editorText}>
                  <strong>{copy(ask.status)}.</strong> {copy(ask.note)}
                </p>
              </div>
            </div>

            <aside className={styles.method} aria-labelledby="journal-method" data-reveal>
              <h3 id="journal-method" className={styles.methodTitle}>
                {copy("How answers are made") /* DRAFT */}
              </h3>
              <ol className={styles.methodSteps}>
                {ask.steps.map((step, index) => (
                  <li key={step}>
                    <span className={styles.methodNo}>{index + 1}</span>
                    <p>{copy(step)}</p>
                  </li>
                ))}
              </ol>
            </aside>
          </div>
        </section>
      </CiteProvider>
    </div>
  );
}
