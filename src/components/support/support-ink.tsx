"use client";

import type { ReactNode } from "react";
import { useSiteDialogs } from "@/components/ink/dialogs";
import { InkPage } from "@/components/ink/ink-page";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { book, mailbox, parcel, porch } from "./support-art";
import { ALT, SENDING_LIVE, support } from "./support-content";
import { Painting, Spread, useWordsLang } from "./spread";
import { SupportForm } from "./support-form";
import page from "./support-page.module.css";

// Support, "Pull up a chair" (Mo, October 14, 2026; mockup reference/ink-pages/mockups/support/;
// spec docs/superpowers/specs/2026-10-14-support-page-design.md). A California porch opens the
// page; its cup's gold steam rises once the porch has bloomed (support-page.module.css), and again
// when a message is sent. Then Write to us, Returns and Questions, one painting each, sides taking
// turns. No brush line.

function Opening() {
  const copy = useCopy();
  const o = support.opening;
  return (
    <section className={page.opening} data-part="opening" aria-labelledby="support-title">
      <div className={base.wrap}>
        <Painting
          art={porch}
          alt={copy(ALT.porch)}
          sizes="(max-width: 599px) 92vw, 720px"
          preload
          steam={porch.steam}
          className={page.porch}
        />
        <h1 id="support-title" className={page.title}>
          {copy(o.title)}
        </h1>
        <p className={page.lead}>{copy(o.lead)}</p>
        <dl className={page.contact}>
          <div>
            <dt>{copy(o.call.label)}</dt>
            <dd>
              <a className={page.number} href={o.call.href}>
                {o.call.value}
              </a>
            </dd>
          </div>
          <div>
            <dt>{copy(o.email.label)}</dt>
            <dd>
              <a href={o.email.href}>{o.email.value}</a>
            </dd>
          </div>
          <div>
            <dt>{copy(o.hours.label)}</dt>
            <dd>{copy(o.hours.value)}</dd>
          </div>
        </dl>
      </div>
    </section>
  );
}

// What each painting asks the server for follows the width it is drawn at (support-page.module.css):
// its share of the column (about 85vw on a phone, a third of the window from 960px), up to its cap.
const MAILBOX = "(max-width: 599px) 58vw, (max-width: 959px) 354px, min(23vw, 354px)";
const PARCEL = "(max-width: 599px) 73vw, (max-width: 959px) 447px, min(29vw, 447px)";
const BOOK = "(max-width: 599px) 85vw, (max-width: 959px) 520px, min(34vw, 520px)";

// The mailbox is the one painting that can reach the first screen (a tall phone, a short opening),
// so it loads eagerly, at low priority behind the porch (no preload of its own); the other two sit
// well below it. The form comes in through children.
function Write({ children }: { children?: ReactNode }) {
  const copy = useCopy();
  const w = support.write;
  return (
    <Spread
      id="write"
      part="write"
      side="left"
      labelledBy="write-title"
      picture={
        <Painting
          art={mailbox}
          alt={copy(ALT.mailbox)}
          sizes={MAILBOX}
          eager
          className={page.mailbox}
        />
      }
    >
      <p className={page.label}>{copy(w.label)}</p>
      <h2 id="write-title" className={page.heading}>
        {copy(w.title)}
      </h2>
      <p className={page.body}>{copy(SENDING_LIVE ? w.lead : w.previewLead)}</p>
      {children}
    </Spread>
  );
}

function Returns() {
  const copy = useCopy();
  const lang = useWordsLang();
  const r = support.returns;
  return (
    <Spread
      id="returns"
      part="returns"
      side="right"
      labelledBy="returns-title"
      picture={
        <Painting art={parcel} alt={copy(ALT.parcel)} sizes={PARCEL} className={page.parcel} />
      }
    >
      <p className={page.label}>{copy(r.label)}</p>
      <h2 id="returns-title" lang={lang(r.title)} className={page.heading}>
        {copy(r.title)}
      </h2>
      <p className={page.body}>{copy(r.lead)}</p>
      <p className={page.body}>{copy(r.after)}</p>
      <p className={page.address}>
        <span>{copy(r.to)}</span>
        {r.address.map((line) => (
          <span key={line}>{line}</span>
        ))}
      </p>
      <hr className={page.rule} />
      <p className={page.label}>{copy(r.ordersLabel)}</p>
      <p className={page.body}>{copy(r.orders)}</p>
    </Spread>
  );
}

function Questions() {
  const copy = useCopy();
  const dialogs = useSiteDialogs();
  const lang = useWordsLang();
  const q = support.questions;
  return (
    <Spread
      id="questions"
      part="questions"
      side="left"
      labelledBy="questions-title"
      picture={<Painting art={book} alt={copy(ALT.book)} sizes={BOOK} className={page.book} />}
    >
      <p className={page.label}>{copy(q.label)}</p>
      <h2 id="questions-title" className={page.heading}>
        {copy(q.title)}
      </h2>
      <div className={page.faq}>
        {q.items.map((item, i) => (
          <details key={item.q} name="support-questions" open={i === 0}>
            <summary>
              <span>{copy(item.q)}</span>
              <span className={page.toggle} aria-hidden="true" />
            </summary>
            <p className={page.answer}>{copy(item.a)}</p>
          </details>
        ))}
      </div>
      <p className={page.more}>{copy(q.more)}</p>
      <button
        type="button"
        lang={lang(q.ask)}
        className={`${base.pill} ${base.pillGhost}`}
        onClick={dialogs.openAsk}
      >
        {copy(q.ask)}
      </button>
    </Spread>
  );
}

// The page's own words have no translations yet, so its content is marked English (a screen reader
// then reads it in English on /kr and the rest); the shared menu and footer, outside it, keep the
// locale's language, and so do the few words that are translated (useWordsLang).
export function SupportInk({ titleFont }: { titleFont: string }) {
  return (
    <InkPage current="support" className={`${page.supportPage} ${titleFont}`}>
      {() => (
        <div data-support="porch" lang="en">
          <Opening />
          <Write>
            <SupportForm />
          </Write>
          <Returns />
          <Questions />
        </div>
      )}
    </InkPage>
  );
}
