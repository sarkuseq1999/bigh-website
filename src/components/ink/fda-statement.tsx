"use client";

import { useCopy } from "@/i18n/use-copy";
import styles from "./fda-statement.module.css";

// The FDA statement every page closes on (Mo's pick, October 12, 2026: "A. Label strip"). On a
// bottle the rule (21 CFR 101.93) asks for it in bold type, set off in a box; here the box is the
// menu bar's own brush line, drawn above and below in the footer's ink, so the strip reads on the
// paper footer and on the Science page's dark one alike. The parent footer places it (margins).
export const FDA_STATEMENT =
  "These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease.";

export function FdaStatement({ className }: { className?: string }) {
  const copy = useCopy();
  return (
    <div className={className ? `${styles.fda} ${className}` : styles.fda} data-fda="">
      <p className={styles.text}>
        <span className={styles.star} aria-hidden="true">
          *
        </span>
        {copy(FDA_STATEMENT)}
      </p>
    </div>
  );
}
