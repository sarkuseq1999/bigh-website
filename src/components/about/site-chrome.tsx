"use client";

import Image from "next/image";
import { ArrowUp, Menu, X } from "lucide-react";
import { useState } from "react";
import { HeaderUtilities } from "@/components/home/header-utilities";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { about, routes } from "./about-content";
import styles from "./site-chrome.module.css";

// Header and footer for the About page. They copy the Science page's chrome (branch science-page,
// site-chrome.tsx) so the two pages match; the product pages (branch nuricell-page) grow their own.
// All of them become one shared component when the branches land.

function Logo({ footer = false }: { footer?: boolean }) {
  const copy = useCopy();
  return (
    <Link
      href="/"
      aria-label={copy("BiGH home")}
      className={footer ? styles.footerLogo : styles.logo}
    >
      <span className={styles.logoCrop}>
        <Image
          src="/images/brand/bigh-logo-black-green.png"
          alt={copy("BiGH")}
          width={1448}
          height={811}
          sizes={footer ? "170px" : "136px"}
          loading={footer ? "lazy" : "eager"}
          className={styles.logoImage}
        />
      </span>
    </Link>
  );
}

// Always light: look A runs on paper throughout. (Science's copy also turns dark over dark
// sections; the shared header will need that when the branches merge.)
export function AboutHeader({ onSupport }: { onSupport: () => void }) {
  const copy = useCopy();
  const [open, setOpen] = useState(false);
  const close = () => setOpen(false);

  return (
    <header className={`${styles.header} ${styles.light} ${open ? styles.open : ""}`}>
      <div className={styles.bar}>
        <Logo />
        <nav id="about-navigation" aria-label={copy("Main navigation")} className={styles.nav}>
          <Link href="/" onClick={close}>
            {copy("Home")}
          </Link>
          <Link href={routes.products} onClick={close}>
            {copy("Products")}
          </Link>
          <Link href={routes.scientists} onClick={close}>
            {copy("Science")}
          </Link>
          <Link href="/about" aria-current="page" onClick={close}>
            {copy("About")}
          </Link>
          <button
            type="button"
            onClick={() => {
              close();
              onSupport();
            }}
          >
            {copy("Support")}
          </button>
          <div className={styles.utilities}>
            <HeaderUtilities />
          </div>
        </nav>
        <button
          type="button"
          className={styles.menuButton}
          aria-label={copy(open ? "Close menu" : "Open menu")}
          aria-expanded={open}
          aria-controls="about-navigation"
          onClick={() => setOpen(!open)}
        >
          {open ? <X size={26} /> : <Menu size={26} />}
        </button>
      </div>
    </header>
  );
}

export function AboutFooter({ onAsk, onSupport }: { onAsk: () => void; onSupport: () => void }) {
  const copy = useCopy();
  return (
    <footer className={styles.footer} data-tone="light">
      <div className={styles.footerTop}>
        <div>
          <Logo footer />
          <p className={styles.footerMessage}>{copy("Stay sharp. Live fully.")}</p>
        </div>
        <div className={styles.footerColumns}>
          <div>
            <h2>{copy("About BiGH")}</h2>
            <a href="#purpose">{copy(about.purpose.label)}</a>
            <a href="#roots">{copy(about.roots.label)}</a>
            <a href="#experience">{copy(about.experience.label)}</a>
            <a href="#promise">{copy(about.promise.label)}</a>
          </div>
          <div>
            <h2>{copy("Here for you")}</h2>
            <Link href={routes.products}>{copy("Products")}</Link>
            <button type="button" onClick={onAsk}>
              {copy("Ask BiGH Science")}
            </button>
            <button type="button" onClick={onSupport}>
              {copy("Support & FAQs")}
            </button>
          </div>
        </div>
      </div>
      <div className={styles.footerBottom}>
        <span>
          © {new Date().getFullYear()} {copy("BiGH. Be in Good Health.")}
        </span>
        <a href="#about-main">
          {copy("Back to top")} <ArrowUp size={16} />
        </a>
      </div>
      <p className={styles.footerNote}>
        {copy(
          "Educational content is for general information. Product details and packaging are subject to confirmation. Purchases and question submissions are not available in this preview. Lifestyle imagery is illustrative.",
        )}
      </p>
    </footer>
  );
}
