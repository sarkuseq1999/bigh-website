"use client";

import type { ReactNode } from "react";
import { Clock3, Mail, Phone, Sun } from "lucide-react";
import { InkPage } from "@/components/ink/ink-page";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { book, mailbox, parcel, porch } from "./support-california-art";
import { ALT, support } from "./support-content";
import { Painting, Spread, useWordsLang } from "./spread";
import { SupportForm } from "./support-form";
import page from "./support-page.module.css";
import studio from "./support-california.module.css";

// Approved California composition, retaining native navigation, copy and the Support form.
function Opening() {
  const copy = useCopy();
  const o = support.opening;
  const title = copy(o.lead);
  const split = title.indexOf(". ");
  return (
    <section className={studio.opening} data-part="opening" aria-labelledby="support-title">
      <div className={studio.scene}>
        <Painting
          art={porch}
          alt={copy(ALT.porch)}
          sizes="(max-width: 700px) 100vw, 75vw"
          preload
        />
      </div>
      <div className={[base.wrap, studio.hero].join(" ")}>
        <div className={studio.heroCopy}>
          <p className={studio.eyebrow}>
            <Sun aria-hidden="true" />
            {copy(o.eyebrow)}
          </p>
          <h1 id="support-title" className={studio.title}>
            {split < 0 ? (
              title
            ) : (
              <>
                {title.slice(0, split + 1)}
                <br />
                {title.slice(split + 2)}
              </>
            )}
          </h1>
          <p className={studio.lede}>{copy(o.description)}</p>
          <div className={studio.actions}>
            <a className={base.pill} href="#write">
              <Mail size={19} aria-hidden="true" />
              {copy(support.write.label)}
            </a>
            <a className={studio.textLink} href="#questions">
              {copy(o.browse)}
            </a>
          </div>
        </div>
      </div>
      <div className={studio.reach}>
        <dl className={[base.wrap, studio.contact].join(" ")}>
          <div>
            <Phone aria-hidden="true" />
            <div>
              <dt>{copy(o.call.label)}</dt>
              <dd>
                <a href={o.call.href}>{o.call.value}</a>
              </dd>
            </div>
          </div>
          <div>
            <Mail aria-hidden="true" />
            <div>
              <dt>{copy(o.email.label)}</dt>
              <dd>
                <a href={o.email.href}>{o.email.value}</a>
              </dd>
            </div>
          </div>
          <div>
            <Clock3 aria-hidden="true" />
            <div>
              <dt>{copy(o.hours.label)}</dt>
              <dd>{copy(o.hours.value)}</dd>
            </div>
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
function Write({ children, live }: { children?: ReactNode; live: boolean }) {
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
      <p className={page.body}>{copy(live ? w.lead : w.previewLead)}</p>
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
      <p className={page.label}>{copy(q.title)}</p>
      <h2 id="questions-title" className={page.heading}>
        {copy(support.opening.title)}
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
      {/* Ask BiGH Science goes through this page's own form (Mo, November 16, 2026): the button
          reloads the page with the form's science topic chosen, at the form. A plain link, so the
          form starts again and reads its topic. */}
      <a
        href="?topic=science#write"
        lang={lang(q.ask)}
        className={`${base.pill} ${base.pillGhost}`}
      >
        {copy(q.ask)}
      </a>
    </Spread>
  );
}

// The page's own words have no translations yet, so its content is marked English (a screen reader
// then reads it in English on /kr and the rest); the shared menu and footer, outside it, keep the
// locale's language, and so do the few words that are translated (useWordsLang).
export function SupportInk({ titleFont, live }: { titleFont: string; live: boolean }) {
  return (
    <InkPage current="support" className={`${page.supportPage} ${titleFont}`}>
      {() => (
        <div data-support="porch" lang="en">
          <Opening />
          <Questions />
          <Returns />
          <Write live={live}>
            <SupportForm live={live} />
          </Write>
        </div>
      )}
    </InkPage>
  );
}
