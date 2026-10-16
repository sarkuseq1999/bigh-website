"use client";

import { ArrowUpRight, Minus, Plus } from "lucide-react";
import { useState } from "react";
import { researchItems } from "@/components/home/research-data";
import { useCopy } from "@/i18n/use-copy";
import { research } from "./science-content";
import styles from "./research-library.module.css";

const SHOWN = 5;

// The full list of 36 sources, laid out like Timeline's "Our Studies" page (Design Vault
// #031–#033): a year, a title, the source and a plus to read what each source says. Same sources as
// the homepage. The page shows three key studies first and opens this list on request (key-studies).
export function ResearchGroups({ everything = false }: { everything?: boolean }) {
  const copy = useCopy();
  const [open, setOpen] = useState<Record<string, boolean>>({});

  return (
    <>
      {research.groups.map((group) => {
        const items = researchItems.filter((item) => item.type === group.type);
        const expanded = everything || (open[group.type] ?? false);
        return (
          <div key={group.type} className={styles.group}>
            <div className={styles.groupHead}>
              <h3>{copy(group.title)}</h3>
              <p>{copy(group.text)}</p>
            </div>
            <div className={styles.columns} aria-hidden="true">
              <span>{copy("Year")}</span>
              <span>{copy("Title")}</span>
              <span>{copy("Source")}</span>
            </div>
            <div>
              {items.slice(0, expanded ? undefined : SHOWN).map((item) => (
                <details key={item.url} className={styles.row}>
                  <summary>
                    <span className={styles.year}>{copy(item.year)}</span>
                    <span className={styles.rowTitle}>
                      <small>
                        {copy(item.category)}
                        {research.byLiu.includes(item.url) && (
                          <span className={styles.tag}>{copy(research.tag)}</span>
                        )}
                      </small>
                      <span>{copy(item.title)}</span>
                    </span>
                    <span className={styles.journal}>{item.journal}</span>
                    <Plus className={styles.plus} size={24} aria-hidden="true" />
                  </summary>
                  <div className={styles.body}>
                    <p>{copy(item.text)}</p>
                    <a href={item.url} target="_blank" rel="noreferrer" className={styles.link}>
                      {copy("Read original source")} <ArrowUpRight size={18} />
                    </a>
                  </div>
                </details>
              ))}
            </div>
            {!everything && items.length > SHOWN && (
              <button
                type="button"
                className={styles.more}
                aria-expanded={expanded}
                onClick={() => setOpen({ ...open, [group.type]: !expanded })}
              >
                {expanded ? copy("Show fewer") : `${copy("Show all sources")} (${items.length})`}
                {expanded ? <Minus size={18} /> : <Plus size={18} />}
              </button>
            )}
          </div>
        );
      })}
    </>
  );
}
