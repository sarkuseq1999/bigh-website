"use client";

import Image from "next/image";
import { ArrowUpRight, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useCopy } from "@/i18n/use-copy";
import { AskScience } from "./ask-science";
import { HealthDoors } from "./health-doors";
import { KeyStudies } from "./key-studies";
import { LookGolden } from "./look-golden";
import { liu, liuStory } from "./science-content";
import { ScienceFooter, ScienceHeader } from "./site-chrome";
import styles from "./science-page.module.css";

export type OpeningProps = { onStory: () => void };
type Panel = "story" | "support" | null;

// The Science page in Mo's 9/16 order: the scientists (look D, "Golden hour", his pick of
// September 25), then three key studies, health explained, and Ask BiGH Science.
export function SciencePage() {
  const copy = useCopy();
  const dialog = useRef<HTMLDialogElement>(null);
  const [panel, setPanel] = useState<Panel>(null);

  useEffect(() => {
    const element = dialog.current;
    if (!element) return;
    if (panel && !element.open) element.showModal();
    if (!panel && element.open) element.close();
  }, [panel]);

  return (
    <div className={styles.page}>
      <a href="#science-main" className={styles.skipLink}>
        {copy("Skip to content")}
      </a>
      <ScienceHeader onSupport={() => setPanel("support")} />
      <main id="science-main">
        <LookGolden onStory={() => setPanel("story")} />
        <KeyStudies />
        <HealthDoors />
        <AskScience />
      </main>
      <ScienceFooter onSupport={() => setPanel("support")} />

      <dialog
        ref={dialog}
        className={styles.dialog}
        aria-labelledby="science-dialog-title"
        onClose={() => setPanel(null)}
        onClick={(event) => {
          if (event.target === event.currentTarget) setPanel(null);
        }}
      >
        {panel === "story" && (
          <div className={styles.dialogInner}>
            <div className={styles.dialogPhoto}>
              <Image src={liu.photo.src} alt={copy(liu.name)} fill sizes="200px" />
            </div>
            <div>
              <div className={styles.dialogHeader}>
                <div>
                  <p className={styles.dialogEyebrow}>{copy(liuStory.eyebrow)}</p>
                  <h2 id="science-dialog-title" className={styles.dialogTitle}>
                    {copy(liu.name)}
                  </h2>
                  <p className={styles.dialogRole}>{copy(liu.role)}</p>
                </div>
                <button
                  type="button"
                  className={styles.closeButton}
                  onClick={() => setPanel(null)}
                  aria-label={copy("Close details")}
                  autoFocus
                >
                  <X size={24} />
                </button>
              </div>
              <div className={styles.dialogBody}>
                {liuStory.paragraphs.map((text) => (
                  <p key={text}>{copy(text)}</p>
                ))}
                <div className={styles.dialogLinks}>
                  {liuStory.sources.map((source) => (
                    <a
                      key={source.url}
                      className={styles.textLink}
                      href={source.url}
                      target="_blank"
                      rel="noreferrer"
                    >
                      {copy(source.label)} <ArrowUpRight size={18} />
                    </a>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
        {panel === "support" && (
          <div className={`${styles.dialogInner} ${styles.textOnly}`}>
            <div>
              <div className={styles.dialogHeader}>
                <div>
                  <p className={styles.dialogEyebrow}>{copy("Here to help")}</p>
                  <h2 id="science-dialog-title" className={styles.dialogTitle}>
                    {copy("BiGH support")}
                  </h2>
                </div>
                <button
                  type="button"
                  className={styles.closeButton}
                  onClick={() => setPanel(null)}
                  aria-label={copy("Close details")}
                  autoFocus
                >
                  <X size={24} />
                </button>
              </div>
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
            </div>
          </div>
        )}
      </dialog>
    </div>
  );
}
