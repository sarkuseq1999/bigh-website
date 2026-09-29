"use client";

import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { looks, type Look } from "./science-content";
import styles from "./look-switcher.module.css";

// Review control for Mo: switches between the round-3 looks. Removed after the pick.
export function LookSwitcher({ current }: { current: Look }) {
  const copy = useCopy();
  return (
    <nav className={styles.switcher} aria-label={copy("Design options")}>
      <span className={styles.label}>{copy("Design")}</span>
      {looks.map((look) => (
        <Link
          key={look.id}
          href={{ pathname: "/science", query: { look: look.id } }}
          aria-current={current === look.id ? "true" : undefined}
          className={styles.option}
        >
          <span className={styles.letter}>{look.letter}</span>
          <span className={styles.name}>{copy(look.name)}</span>
        </Link>
      ))}
    </nav>
  );
}
