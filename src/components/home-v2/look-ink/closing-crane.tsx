"use client";

import Image from "next/image";
import { craneRest } from "./assets";
import base from "./look-ink.module.css";

// The page's last picture: the crane that opened the page in flight, now at rest. It stands
// beside the footer's promise, on the closing brush stroke (brush-route.ts `promise`).
export function ClosingCrane() {
  return (
    <Image
      className={`${base.ink} ${base.rest}`}
      src={craneRest.src}
      alt=""
      width={craneRest.width}
      height={craneRest.height}
      sizes="140px"
      data-bloom=""
      style={{ ["--bloom-delay" as string]: 300 }}
    />
  );
}
