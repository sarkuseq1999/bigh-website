"use client";

import type { ReactNode } from "react";
import { useCopy } from "@/i18n/use-copy";
import styles from "./fda-statement.module.css";

// The FDA statement every page closes on, routed into a painted California trail sign (Mo's pick,
// October 13, 2026: "I", after the label strip she found plain). The sign is one picture drawn as
// the paragraph's border (fda-statement.module.css), so the words stay real text: read aloud,
// translated, and fitted by the browser. Only the sign's face stretches around them; the posts, the
// grass and the oak keep their shape. The parent footer places it (margins), and may stand a
// painting in the grass at the sign's right (`beside`: the crane at rest, Mo, October 26, 2026).
export const FDA_STATEMENT =
  "These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease.";

export function FdaStatement({ className, beside }: { className?: string; beside?: ReactNode }) {
  const copy = useCopy();
  return (
    <div className={className ? `${styles.fda} ${className}` : styles.fda} data-fda="">
      <p className={styles.text}>
        <span className={styles.words}>{copy(FDA_STATEMENT)}</span>
      </p>
      {beside}
    </div>
  );
}
