"use client";

import Image from "next/image";
import { cranePoppy } from "@/components/home-v2/look-ink/assets";
import base from "./ink.module.css";
import { useTint } from "@/components/home-v2/look-ink/ink-color";

// The page's last painting: the crane that opened the page in flight, now at rest at the end of
// the trail, in the grass beside the FDA park sign, bending to look at the sign's California poppy
// (Mo picked C, October 26, 2026). The footer stands it by the sign (fda-statement.tsx). Its bloom
// is the page's arrival.
export function ClosingCrane() {
  const tint = useTint();
  return (
    <Image
      className={`${base.ink} ${base.rest}`}
      src={tint(cranePoppy.src)}
      alt=""
      width={cranePoppy.width}
      height={cranePoppy.height}
      sizes="(max-width: 720px) 140px, 250px"
      // It blooms once all of it is in the window, spreading from the bird's body.
      data-bloom=""
      data-bloom-whole=""
      style={{ ["--bloom-delay" as string]: 250, ["--bloom-origin" as string]: "50% 40%" }}
    />
  );
}
