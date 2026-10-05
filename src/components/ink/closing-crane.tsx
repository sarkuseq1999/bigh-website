"use client";

import Image from "next/image";
import { craneRest } from "@/components/home-v2/look-ink/assets";
import base from "./ink.module.css";

// The page's last painting: the crane that opened the page in flight, now at rest, large beside
// the footer's promise and facing it, on the closing brush stroke (route-kit.ts `footerEnding`).
// Its bloom is the page's arrival.
export function ClosingCrane() {
  return (
    <Image
      className={`${base.ink} ${base.rest}`}
      src={craneRest.src}
      alt=""
      width={craneRest.width}
      height={craneRest.height}
      sizes="(max-width: 720px) 23vw, 220px"
      // It blooms once all of it is in the window, spreading up from low on the bird, toward the
      // stroke it stands on (72% is as low as the blot's origin goes and still covers it whole).
      data-bloom=""
      data-bloom-whole=""
      style={{ ["--bloom-delay" as string]: 250, ["--bloom-origin" as string]: "50% 72%" }}
    />
  );
}
