"use client";

import { ChevronDown } from "lucide-react";
import {
  useEffect,
  useId,
  useRef,
  useState,
  type CSSProperties,
  type FocusEvent,
  type MouseEvent,
} from "react";
import { useCopy } from "@/i18n/use-copy";
import { anchorId, type Chapter, type ChapterId } from "./template-chapters-kit";
import styles from "./template-chapters.module.css";

// The chapter index (Design Vault #041, Seed's chapter navigation): on wide screens a rail at the
// left edge with every chapter's number and name, the current one filled in and a little larger;
// on smaller screens a pill at the top ("3 / 7 · What's inside") that opens the same list. It
// appears after the first screen. Each entry is a real link to the chapter's anchor.
export function ChapterIndex({
  chapters,
  active,
  shown,
  onJump,
}: {
  chapters: Chapter[];
  active: number;
  shown: boolean;
  onJump: (id: ChapterId) => void;
}) {
  const copy = useCopy();
  const [open, setOpen] = useState(false);
  const listId = useId();
  const nav = useRef<HTMLElement>(null);
  const toggle = useRef<HTMLButtonElement>(null);
  const current = chapters[Math.min(active, chapters.length - 1)];
  const expanded = open && shown;

  // The phone list closes with Escape (focus returns to the pill) or a tap anywhere else.
  useEffect(() => {
    if (!expanded) return;
    const onKey = (event: KeyboardEvent) => {
      if (event.key !== "Escape") return;
      setOpen(false);
      toggle.current?.focus();
    };
    const onPointer = (event: PointerEvent) => {
      if (!nav.current?.contains(event.target as Node)) setOpen(false);
    };
    document.addEventListener("keydown", onKey);
    document.addEventListener("pointerdown", onPointer);
    return () => {
      document.removeEventListener("keydown", onKey);
      document.removeEventListener("pointerdown", onPointer);
    };
  }, [expanded]);

  function go(event: MouseEvent<HTMLAnchorElement>, id: ChapterId) {
    event.preventDefault();
    setOpen(false);
    onJump(id);
  }

  function leave(event: FocusEvent<HTMLElement>) {
    if (!event.currentTarget.contains(event.relatedTarget as Node | null)) setOpen(false);
  }

  return (
    <nav
      ref={nav}
      aria-label={copy("Chapters")}
      className={styles.index}
      data-shown={shown}
      data-open={expanded}
      onBlur={leave}
    >
      <button
        ref={toggle}
        type="button"
        className={styles.indexToggle}
        aria-expanded={expanded}
        aria-controls={listId}
        onClick={() => setOpen((value) => !value)}
      >
        <span className={styles.srOnly}>
          {copy("Chapter {current} of {total}:", {
            current: current.number,
            total: chapters.length,
          })}
        </span>
        <span className={styles.toggleCount} aria-hidden="true">
          {current.number} / {chapters.length}
        </span>
        <span className={styles.toggleDot} aria-hidden="true">
          ·
        </span>
        <span className={styles.toggleName}>{copy(current.name)}</span>
        <ChevronDown size={20} strokeWidth={2} aria-hidden="true" className={styles.toggleIcon} />
      </button>
      <ol
        id={listId}
        className={styles.indexList}
        style={
          {
            "--progress": chapters.length > 1 ? active / (chapters.length - 1) : 0,
          } as CSSProperties
        }
      >
        {chapters.map((chapter, index) => (
          <li key={chapter.id}>
            <a
              href={`#${anchorId(chapter.id)}`}
              className={styles.indexLink}
              aria-current={index === active ? "location" : undefined}
              onClick={(event) => go(event, chapter.id)}
            >
              <span className={styles.indexNumber} aria-hidden="true">
                {chapter.number}
              </span>
              <span>{copy(chapter.name)}</span>
            </a>
          </li>
        ))}
      </ol>
    </nav>
  );
}
