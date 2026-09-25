"use client";

import { X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useCopy } from "@/i18n/use-copy";
import type { Look } from "./about-content";
import { LookBold } from "./look-bold";
import { LookCalm } from "./look-calm";
import { LookMix } from "./look-mix";
import { LookSpace } from "./look-space";
import { AboutFooter, AboutHeader } from "./site-chrome";
import styles from "./about-page.module.css";

export type LookProps = { onAsk: () => void };
type Panel = "ask" | "support" | null;

// The About page. Mo picked look A, "Calm", on September 25, 2026; it is what /about shows.
// The other looks stay reachable at ?look=b|ab|c only until the review copies are cleaned up.
export function AboutPage({ look }: { look: Look }) {
  const copy = useCopy();
  const dialog = useRef<HTMLDialogElement>(null);
  const [panel, setPanel] = useState<Panel>(null);

  useEffect(() => {
    const element = dialog.current;
    if (!element) return;
    if (panel && !element.open) element.showModal();
    if (!panel && element.open) element.close();
  }, [panel]);

  const Body = { a: LookCalm, b: LookSpace, c: LookBold, ab: LookMix }[look];
  const close = () => setPanel(null);

  return (
    <div className={styles.page} data-look={look}>
      <a href="#about-main" className={styles.skipLink}>
        {copy("Skip to content")}
      </a>
      {/* Keyed by look so switching looks starts the header fresh. B starts dark; B and the mix
          follow the tone of whatever section is under the header. */}
      <AboutHeader
        key={look}
        startsDark={look === "b"}
        adaptive={look === "b" || look === "ab"}
        onSupport={() => setPanel("support")}
      />
      <main id="about-main">
        <Body onAsk={() => setPanel("ask")} />
      </main>
      <AboutFooter onAsk={() => setPanel("ask")} onSupport={() => setPanel("support")} />

      <dialog
        ref={dialog}
        className={styles.dialog}
        aria-labelledby="about-dialog-title"
        onClose={close}
        onClick={(event) => {
          if (event.target === event.currentTarget) close();
        }}
      >
        {panel && (
          <div className={styles.dialogInner}>
            <div className={styles.dialogHeader}>
              <div>
                <p className={styles.dialogEyebrow}>
                  {copy(panel === "ask" ? "A planned customer benefit" : "Here to help")}
                </p>
                <h2 id="about-dialog-title" className={styles.dialogTitle}>
                  {copy(panel === "ask" ? "Ask BiGH Science" : "BiGH support")}
                </h2>
              </div>
              <button
                type="button"
                className={styles.closeButton}
                onClick={close}
                aria-label={copy("Close details")}
                autoFocus
              >
                <X size={24} />
              </button>
            </div>
            {panel === "ask" ? (
              <div className={styles.dialogBody}>
                <p>
                  {copy(
                    "Good questions deserve clear explanations. We are developing a way for BiGH customers to explore broader health and science questions with input from participating scientists.",
                  )}
                </p>
                <ol className={styles.steps}>
                  <li>
                    {copy(
                      "Start with a question about topics such as cellular health, nutrition, or healthy aging.",
                    )}
                  </li>
                  <li>
                    {copy(
                      "BiGH explains what the research says and involves scientific advisors when deeper input is needed.",
                    )}
                  </li>
                  <li>
                    {copy(
                      "Each answer identifies its contributors and where the science remains uncertain.",
                    )}
                  </li>
                </ol>
                <div className={styles.draftNote}>
                  <strong>{copy("In development")}</strong>
                  <p>
                    {copy(
                      "The question service is not accepting submissions yet. Eligibility and response arrangements are still being agreed. This will be general science education, not personal medical care.",
                    )}
                  </p>
                </div>
              </div>
            ) : (
              <div className={styles.dialogBody}>
                <p>
                  {copy(
                    "This is a preview of the new BiGH website. You can explore the range and science, but purchases and account services are not connected yet.",
                  )}
                </p>
                <p>
                  {copy(
                    "Ask BiGH Science is in development. It will explain research in everyday language. For personal treatment or medication questions, speak with your healthcare professional.",
                  )}
                </p>
              </div>
            )}
          </div>
        )}
      </dialog>
    </div>
  );
}
