"use client";

import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useCallback, useEffect, useMemo, useRef, useState, useSyncExternalStore } from "react";
import { useReducedMotion } from "@/components/home/use-reduced-motion";
import type { TemplateProps } from "./product-page";
import type { ProductPage } from "./product-types";
import { BuyChapter } from "./template-chapters-buy";
import { DailyChapter } from "./template-chapters-daily";
import { HeroChapter } from "./template-chapters-hero";
import { chaptersFixture } from "./template-chapters-fixtures";
import { ChapterIndex } from "./template-chapters-index";
import { InsideChapter } from "./template-chapters-inside";
import { anchorId, type Chapter, type ChapterId, type Tone } from "./template-chapters-kit";
import { PeopleChapter } from "./template-chapters-people";
import { ResearchChapter } from "./template-chapters-research";
import { WhyChapter } from "./template-chapters-why";
import styles from "./template-chapters.module.css";

// Template 2, "Chapters" (September 25, 2026): the guided story. The product page as a short film
// you scroll, one idea per screen, with a big chapter index so every visitor knows where they are
// and can jump. Timeline's science pages applied to a product (Design Vault #007, #009, #011), with
// Seed's chapter navigation (#041). Everything comes from the product's data: a chapter whose data
// is missing simply is not there, and the index renumbers.

type Plan = { id: ChapterId; name: string; present: (product: ProductPage) => boolean };

const plan: Plan[] = [
  { id: "overview", name: "Overview", present: () => true },
  { id: "why", name: "Why it matters", present: (p) => Boolean(p.why || p.photo) },
  {
    id: "inside",
    name: "What’s inside",
    present: (p) => p.ingredients.length > 0 || Boolean(p.signature),
  },
  { id: "research", name: "The research", present: (p) => p.studies.length > 0 },
  { id: "people", name: "The people", present: (p) => p.people.length > 0 },
  { id: "daily", name: "How to take it", present: () => true },
  { id: "buy", name: "Buy", present: () => true },
];

/**
 * The page eases between paper and the product's tint from chapter to chapter. A few are fixed: the
 * overview and buying sit on the tint (the bottle on its own colour), a signature moment sits on
 * paper (the capsule's warm light reads best there), and "why" is night when it has its dark photo
 * (paper otherwise). The rest alternate.
 */
function toneFor(id: ChapterId, product: ProductPage, previous: Tone | null): Tone {
  if (id === "overview" || id === "buy") return "tint";
  if (id === "why") return product.why?.visual ? "night" : "paper";
  if (id === "inside" && product.signature) return "paper";
  return previous === "tint" ? "paper" : "tint";
}

export function buildChapters(product: ProductPage): Chapter[] {
  let previous: Tone | null = null;
  return plan
    .filter((entry) => entry.present(product))
    .map((entry, index) => {
      const tone = toneFor(entry.id, product, previous);
      previous = tone;
      return { id: entry.id, name: entry.name, tone, number: index + 1 };
    });
}

// Development only: ?chapters-fixture=lean|full reshapes the data for layout checks (see
// template-chapters-fixtures.ts). Production builds always render the product as given.
const noSubscription = () => () => {};
function useFixtureName() {
  return useSyncExternalStore(
    noSubscription,
    () =>
      process.env.NODE_ENV === "production"
        ? null
        : new URLSearchParams(window.location.search).get("chapters-fixture"),
    () => null,
  );
}

type View = { index: number; tone: Tone; shown: boolean };

export function TemplateChapters({ product: given }: TemplateProps) {
  const fixture = useFixtureName();
  const product = useMemo(() => chaptersFixture(given, fixture), [given, fixture]);
  const reduced = useReducedMotion();
  const root = useRef<HTMLDivElement>(null);
  const chapters = useMemo(() => buildChapters(product), [product]);
  const [view, setView] = useState<View>({ index: 0, tone: "tint", shown: false });
  const active = Math.min(view.index, chapters.length - 1);

  // Which chapter is on screen (the last one whose top has passed 45% of the window), which colour
  // the page should wear (the same test over every part with a tone), and whether the index shows
  // (after the first screen, until the footer). A plain scroll listener, so it works without motion.
  useEffect(() => {
    const element = root.current;
    if (!element) return;
    let frame = 0;
    const measure = () => {
      frame = 0;
      const line = window.innerHeight * 0.45;
      let index = 0;
      element.querySelectorAll<HTMLElement>("[data-chapter]").forEach((section, i) => {
        if (section.getBoundingClientRect().top <= line) index = i;
      });
      let tone: Tone = "tint";
      element.querySelectorAll<HTMLElement>("[data-tone]").forEach((zone) => {
        const value = zone.dataset.tone;
        if (zone.getBoundingClientRect().top <= line)
          tone = value === "paper" || value === "night" ? value : "tint";
      });
      const shown =
        window.scrollY > window.innerHeight * 0.6 &&
        element.getBoundingClientRect().bottom > window.innerHeight * 0.8;
      setView((current) =>
        current.index === index && current.tone === tone && current.shown === shown
          ? current
          : { index, tone, shown },
      );
    };
    const schedule = () => {
      if (!frame) frame = requestAnimationFrame(measure);
    };
    schedule();
    // A list opening moves the chapters below it without any scrolling; measure then too.
    const observer = typeof ResizeObserver === "undefined" ? null : new ResizeObserver(schedule);
    observer?.observe(element);
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", schedule);
    return () => {
      cancelAnimationFrame(frame);
      observer?.disconnect();
      window.removeEventListener("scroll", schedule);
      window.removeEventListener("resize", schedule);
    };
  }, [chapters]);

  // Scroll effects measure the page once. When its height really changes later (a list opening,
  // the signature moment settling), measure them again. Tiny changes are ignored, and ScrollTrigger
  // itself waits for scrolling to stop before it measures, so a flick is never interrupted.
  useEffect(() => {
    const element = root.current;
    if (reduced || !element || typeof ResizeObserver === "undefined") return;
    gsap.registerPlugin(ScrollTrigger);
    let timer = 0;
    let height = element.offsetHeight;
    const observer = new ResizeObserver(() => {
      if (Math.abs(element.offsetHeight - height) < 24) return;
      height = element.offsetHeight;
      window.clearTimeout(timer);
      timer = window.setTimeout(() => ScrollTrigger.refresh(), 200);
    });
    observer.observe(element);
    return () => {
      observer.disconnect();
      window.clearTimeout(timer);
    };
  }, [reduced]);

  // Jump to a chapter: a smooth glide (instant with reduced motion), then focus moves there so the
  // keyboard carries on from the chapter.
  const jump = useCallback(
    (id: ChapterId) => {
      const target = document.getElementById(anchorId(id));
      if (!target) return;
      const top = target.getBoundingClientRect().top + window.scrollY;
      window.scrollTo({ top, behavior: reduced ? "instant" : "smooth" });
      target.focus({ preventScroll: true });
    },
    [reduced],
  );

  const find = (id: ChapterId) => chapters.find((chapter) => chapter.id === id);
  const why = find("why");
  const inside = find("inside");
  const research = find("research");
  const people = find("people");
  const daily = find("daily");
  const buy = find("buy");

  return (
    <div
      ref={root}
      className={styles.chapters}
      data-motion={reduced ? "off" : "on"}
      data-tone={view.tone}
      data-active={chapters[active].id}
    >
      <ChapterIndex chapters={chapters} active={active} shown={view.shown} onJump={jump} />
      <HeroChapter
        product={product}
        chapter={chapters[0]}
        chapters={chapters}
        reduced={reduced}
        onJump={jump}
      />
      {why && <WhyChapter product={product} chapter={why} reduced={reduced} />}
      {inside && <InsideChapter product={product} chapter={inside} reduced={reduced} />}
      {research && <ResearchChapter product={product} chapter={research} reduced={reduced} />}
      {people && <PeopleChapter product={product} chapter={people} reduced={reduced} />}
      {daily && <DailyChapter product={product} chapter={daily} reduced={reduced} />}
      {buy && <BuyChapter product={product} chapter={buy} reduced={reduced} />}
    </div>
  );
}
