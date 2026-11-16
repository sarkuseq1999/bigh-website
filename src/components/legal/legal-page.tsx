"use client";

import { Fragment, type ReactNode } from "react";
import { InkPage } from "@/components/ink/ink-page";
import { Link } from "@/i18n/navigation";
import { legalDocs, type LegalBlock, type LegalDoc } from "./legal-content";
import styles from "./legal.module.css";

// The Privacy, Terms and Returns pages: the site's paper, menu bar and footer, and one quiet
// column to read in. No paintings (a legal page is read, not looked at), the title in the site's
// title face, the date it was last updated, and links between the three. English only, like
// Support (the column is marked lang="en").

const ORDER: LegalDoc["slug"][] = ["privacy", "terms", "returns"];

const LINKS: Record<LegalDoc["slug"], string> = {
  privacy: "Privacy Notice",
  terms: "Terms and Conditions",
  returns: "Return Policy",
};

/** Emails and phone numbers in a line become real links; nothing else changes. */
function linked(text: string): ReactNode {
  return text.split(/(support@bighnow\.com|800-919-2089|www\.bighnow\.com)/).map((part, i) => {
    if (i % 2 === 0) return <Fragment key={i}>{part}</Fragment>;
    if (part.startsWith("www")) return <Fragment key={i}>{part}</Fragment>;
    const href = part.includes("@") ? `mailto:${part}` : `tel:+1${part.replaceAll("-", "")}`;
    return (
      <a key={i} href={href} className={styles.nowrap}>
        {part}
      </a>
    );
  });
}

function Block({ block }: { block: LegalBlock }) {
  if (block.kind === "p") return <p>{linked(block.text)}</p>;
  if (block.kind === "list")
    return (
      <ul>
        {block.items.map((item) => (
          <li key={item}>{linked(item)}</li>
        ))}
      </ul>
    );
  return (
    <address className={styles.address}>
      {block.lines.map((line) => (
        <span key={line}>{linked(line)}</span>
      ))}
    </address>
  );
}

export function LegalPage({ slug, titleFont }: { slug: LegalDoc["slug"]; titleFont: string }) {
  const doc = legalDocs[slug];
  return (
    <InkPage current="legal" className={`${styles.legalPage} ${titleFont}`}>
      {() => (
        <article className={styles.article} lang="en" aria-labelledby="legal-title">
          <header className={styles.head}>
            <h1 id="legal-title" className={styles.title}>
              {doc.title}
            </h1>
            <p className={styles.updated}>Last updated {doc.updated}</p>
          </header>
          {doc.sections.map((section, index) => (
            <section key={section.heading ?? index} className={styles.section}>
              {section.heading ? <h2>{section.heading}</h2> : null}
              {section.blocks.map((block, i) => (
                <Block key={i} block={block} />
              ))}
            </section>
          ))}
          <nav className={styles.others} aria-label="Policies">
            {ORDER.filter((other) => other !== slug).map((other) => (
              <Link key={other} href={`/${other}`}>
                {LINKS[other]}
              </Link>
            ))}
            <Link href="/support">Support</Link>
          </nav>
        </article>
      )}
    </InkPage>
  );
}
