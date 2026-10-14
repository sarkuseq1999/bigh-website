"use client";

import { InkPage } from "@/components/ink/ink-page";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { porch } from "./support-art";
import { ALT, support } from "./support-content";
import { Painting } from "./spread";
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

export function SupportInk({ titleFont }: { titleFont: string }) {
  return (
    <InkPage current="support" className={`${page.supportPage} ${titleFont}`}>
      {() => (
        <div data-support="porch">
          <Opening />
        </div>
      )}
    </InkPage>
  );
}
