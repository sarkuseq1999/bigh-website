"use client";

import Image from "next/image";
import { quailSign } from "@/components/home-v2/look-ink/assets";
import base from "./ink.module.css";

// The page's last painting: two California quail, the state bird, at the end of the trail in the
// grass beside the FDA park sign, one keeping watch, the other bending to look at the sign's
// California poppy (Mo picked A1, November 3, 2026; it replaced the crane at rest, which read as
// Chinese). The footer stands it by the sign (fda-statement.tsx). Its bloom is the page's arrival.
export function ClosingQuail() {
  return (
    <Image
      className={`${base.ink} ${base.rest}`}
      src={quailSign.src}
      alt=""
      width={quailSign.width}
      height={quailSign.height}
      sizes="(max-width: 720px) 160px, 220px"
      // It blooms once all of it is in the window, spreading from the birds' bodies.
      data-bloom=""
      data-bloom-whole=""
      style={{ ["--bloom-delay" as string]: 250, ["--bloom-origin" as string]: "55% 50%" }}
    />
  );
}
