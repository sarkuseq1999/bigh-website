"use client";

import Image from "next/image";
import { useLocale } from "next-intl";
import {
  useEffect,
  useRef,
  useState,
  type CSSProperties,
  type ReactNode,
  type SyntheticEvent,
} from "react";
import base from "@/components/ink/ink.module.css";
import copyKeys from "@/i18n/copy-keys.json";
import type { Art, Steam } from "./support-art";
import page from "./support-page.module.css";

// The document's language tag for each locale, as src/app/[locale]/layout.tsx sets it on <html>.
const TAGS: Record<string, string> = {
  en: "en",
  kr: "ko",
  jp: "ja",
  cns: "zh-Hans",
  hken: "zh-Hant-HK",
  vn: "vi",
};

/** The page's own words are English until their translations land, so its content is marked
 *  lang="en" (support-ink.tsx) while the shared menu and footer keep the locale's language. The few
 *  words that already have a translation (a copy key: "Your name", "45 days to decide.", "Ask BiGH
 *  Science") show in the locale's language: `lang(source)` gives their element its tag back. */
export function useWordsLang() {
  const tag = TAGS[useLocale()] ?? "en";
  return (source: string) => (tag !== "en" && source in copyKeys ? tag : undefined);
}

// The Support page's one rhythm (as About's, kept here so the live About page is untouched): one
// painting, its words beside it, the sides taking turns from 960px; on one column the painting
// comes first. Paintings multiply onto the page's paper and bloom in as they arrive (the kit's
// useBloom); the server marks them "waiting" so none paints whole first.
//
// The gold steam never shows alone over bare paper (as About's circle, Mo): the kit opens a
// painting's bloom as soon as its box is on screen, picture or not, so the steam is keyed to the
// pictures too. The server renders it data-steam="waiting"; once the painting's picture and the
// steam's own are both in, script marks it "ready", and only then, with the bloom open, does the
// stylesheet let it rise (with reduced motion: be there at all). A picture that fails never marks
// it. The steam also loads at low priority (no preload), so the painting's request goes first.

/** The gold steam's gate, for the porch and for the thank-you's cup alike. A picture is "in" on its
 *  onLoad (Next calls it for a picture already complete when it hydrates, a broken one too, hence
 *  the width) or, on mount, when it is already complete. A failed picture is never in. Spread
 *  `ink` and `gold` onto the two <Image>s; `steam` is the steam's data-steam ("ready" once both
 *  are in) and `inkIn` says the painting's own picture is. */
export function useSteamGate() {
  const inkImg = useRef<HTMLImageElement>(null);
  const goldImg = useRef<HTMLImageElement>(null);
  const [inkIn, setInkIn] = useState(false);
  const [goldIn, setGoldIn] = useState(false);
  useEffect(() => {
    if (inkImg.current?.complete && inkImg.current.naturalWidth) setInkIn(true);
    if (goldImg.current?.complete && goldImg.current.naturalWidth) setGoldIn(true);
  }, []);
  const loaded = (set: (value: boolean) => void) => (event: SyntheticEvent<HTMLImageElement>) => {
    if (event.currentTarget.naturalWidth) set(true);
  };
  return {
    ink: { ref: inkImg, onLoad: loaded(setInkIn) },
    gold: { ref: goldImg, onLoad: loaded(setGoldIn) },
    inkIn,
    steam: inkIn && goldIn ? "ready" : "waiting",
  } as const;
}

export function Painting({
  art,
  alt,
  sizes,
  eager = false,
  preload = false,
  steam,
  className = "",
}: {
  art: Art;
  alt: string;
  sizes: string;
  /** Reaches into the first screen on some windows: loading="eager" (so Next's dev check never
   *  calls it a lazy LCP), but fetchPriority="low": React then writes no preload for it, and it
   *  does not race the first screen's main painting. */
  eager?: boolean;
  /** The first screen's main painting: Next's preload and fetchPriority="high". */
  preload?: boolean;
  /** The gold steam over this painting (support-art.ts), which rises after the bloom. */
  steam?: Steam;
  className?: string;
}) {
  const gate = useSteamGate();
  return (
    <figure className={`${page.painting} ${className}`} data-picture="">
      <span className={page.paintingBody}>
        <Image
          {...gate.ink}
          className={base.ink}
          src={art.src}
          alt={alt}
          width={art.width}
          height={art.height}
          sizes={sizes}
          preload={preload}
          fetchPriority={preload ? "high" : eager ? "low" : undefined}
          loading={eager && !preload ? "eager" : undefined}
          data-bloom="waiting"
        />
        {steam ? (
          <Image
            {...gate.gold}
            className={page.steam}
            src={steam.src}
            alt=""
            width={steam.width}
            height={steam.height}
            sizes="200px"
            loading="eager"
            fetchPriority="low"
            data-steam={gate.steam}
            style={
              {
                left: `${(steam.left * 100).toFixed(2)}%`,
                top: `${(steam.top * 100).toFixed(2)}%`,
                width: `${(steam.size * 100).toFixed(2)}%`,
              } as CSSProperties
            }
          />
        ) : null}
      </span>
    </figure>
  );
}

export function Spread({
  id,
  part,
  side,
  labelledBy,
  picture,
  children,
}: {
  id: string;
  part: string;
  /** Where the painting stands from 960px. */
  side: "left" | "right";
  labelledBy: string;
  picture: ReactNode;
  children: ReactNode;
}) {
  return (
    <section id={id} className={page.part} data-part={part} aria-labelledby={labelledBy}>
      <div className={`${base.wrap} ${page.spread}`} data-side={side}>
        {picture}
        <div className={page.words} data-words="">
          {children}
        </div>
      </div>
    </section>
  );
}
