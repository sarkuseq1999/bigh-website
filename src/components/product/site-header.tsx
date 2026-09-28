"use client";

import Image from "next/image";
import { HeaderUtilities } from "@/components/home/header-utilities";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import styles from "./site-header.module.css";

// Header for product pages. Once a template is chosen, the homepage header and this one
// become one shared component.
export function SiteHeader({ tone }: { tone: "light" | "dark" }) {
  const copy = useCopy();
  return (
    <header className={`${styles.header} ${tone === "dark" ? styles.dark : styles.light}`}>
      <Link href="/" aria-label={copy("BiGH home")} className={styles.brand}>
        <span className={styles.crop}>
          <Image
            src={
              tone === "dark"
                ? "/images/brand/bigh-logo-white.png"
                : "/images/brand/bigh-logo-black-green.png"
            }
            alt={copy("BiGH")}
            width={1448}
            height={811}
            sizes="(max-width: 900px) 108px, 124px"
            loading="eager"
            className={styles.logo}
          />
        </span>
      </Link>
      <nav aria-label={copy("Main navigation")} className={styles.nav}>
        <Link href="/">{copy("Home")}</Link>
        <Link href="/#products" aria-current="page">
          {copy("Products")}
        </Link>
        <Link href="/#learn">{copy("Science")}</Link>
        <Link href="/about">{copy("About")}</Link>
      </nav>
      <div className={styles.utilities}>
        <HeaderUtilities />
      </div>
    </header>
  );
}
