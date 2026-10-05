"use client";

import Image from "next/image";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";

/**
 * The BiGH mark for the menu bar options (the tagline under it in the file is cropped away).
 * Size it with `className` (its width); `light` is the white mark for dark ground.
 */
export function NavLogo({ className, light = false }: { className?: string; light?: boolean }) {
  const copy = useCopy();
  return (
    <Link href="/" aria-label={copy("BiGH home")} className={className} data-nav-logo="">
      <span
        style={{ display: "block", width: "100%", aspectRatio: "1448 / 710", overflow: "hidden" }}
      >
        <Image
          src={
            light ? "/images/brand/bigh-logo-white.png" : "/images/brand/bigh-logo-black-green.png"
          }
          alt={copy("BiGH")}
          width={1448}
          height={811}
          sizes="180px"
          loading="eager"
          style={{ display: "block", width: "100%", height: "auto" }}
        />
      </span>
    </Link>
  );
}
