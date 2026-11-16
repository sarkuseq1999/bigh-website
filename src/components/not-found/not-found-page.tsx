"use client";

import { ArrowRight } from "lucide-react";
import { InkPage } from "@/components/ink/ink-page";
import base from "@/components/ink/ink.module.css";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import styles from "./not-found.module.css";

// The site's "not found" page (November 16, 2026, for launch): the menu bar, a short honest line
// and the ways on, then the footer, whose park sign reads as the trail's end. No painting of its
// own: the page is a moment, and the sign below finishes it.

const WAYS = [
  { href: "/products/nuricell", label: "NuriCell, our flagship formula" },
  { href: "/science", label: "Our science" },
  { href: "/about", label: "About BiGH" },
  { href: "/support", label: "Support" },
] as const;

export function NotFoundPage() {
  const copy = useCopy();
  return (
    <InkPage current="legal" className={styles.page}>
      {() => (
        <section className={styles.lost} aria-labelledby="lost-title">
          <p className={styles.code}>404</p>
          <h1 id="lost-title" className={styles.title}>
            {copy("This trail ends here.")}
          </h1>
          <p className={styles.lead}>
            {copy(
              "The page you’re looking for isn’t here. It may have moved, or the address may have a small typo.",
            )}
          </p>
          <p className={styles.actions}>
            <Link className={base.pill} href="/">
              {copy("Back to the homepage")} <ArrowRight size={18} aria-hidden="true" />
            </Link>
          </p>
          <nav className={styles.ways} aria-label={copy("Where to go next")}>
            {WAYS.map((way) => (
              <Link key={way.href} href={way.href}>
                {copy(way.label)}
              </Link>
            ))}
          </nav>
        </section>
      )}
    </InkPage>
  );
}
