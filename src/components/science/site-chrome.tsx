"use client";

import Image from "next/image";
import { ArrowUp, Menu, X } from "lucide-react";
import { useState } from "react";
import { HeaderUtilities } from "@/components/home/header-utilities";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import styles from "./site-chrome.module.css";

// Header and footer for the Science page. The product pages (branch nuricell-page) grow their own
// shared header; the two become one component when both branches land.

function Logo({ light, footer = false }: { light: boolean; footer?: boolean }) {
  const copy = useCopy();
  return (
    <Link
      href="/"
      aria-label={copy("BiGH home")}
      className={footer ? styles.footerLogo : styles.logo}
    >
      <span className={styles.logoCrop}>
        <Image
          src={
            light ? "/images/brand/bigh-logo-white.png" : "/images/brand/bigh-logo-black-green.png"
          }
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

// Looks C and E (now in reference/science-page/looks/) also turned this header dark over dark
// sections; bringing one back means adding that again (the .dark styles are still in the CSS).
export function ScienceHeader({ onSupport }: { onSupport: () => void }) {
  const copy = useCopy();
  const [open, setOpen] = useState(false);
  const close = () => setOpen(false);

  return (
    <header className={`${styles.header} ${styles.light} ${open ? styles.open : ""}`}>
      <div className={styles.bar}>
        <Logo light={false} />
        <nav id="science-navigation" aria-label={copy("Main navigation")} className={styles.nav}>
          <Link href="/" onClick={close}>
            {copy("Home")}
          </Link>
          <Link href="/#products" onClick={close}>
            {copy("Products")}
          </Link>
          <Link href="/science" aria-current="page" onClick={close}>
            {copy("Science")}
          </Link>
          <Link href="/#about" onClick={close}>
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
          aria-controls="science-navigation"
          onClick={() => setOpen(!open)}
        >
          {open ? <X size={26} /> : <Menu size={26} />}
        </button>
      </div>
    </header>
  );
}

export function ScienceFooter({ onSupport }: { onSupport: () => void }) {
  const copy = useCopy();
  return (
    <footer className={styles.footer} data-tone="light">
      <div className={styles.footerTop}>
        <div>
          <Logo light={false} footer />
          <p className={styles.footerMessage}>{copy("Stay sharp. Live fully.")}</p>
        </div>
        <div className={styles.footerColumns}>
          <div>
            <h2>{copy("Science")}</h2>
            <a href="#scientists">{copy("Our scientists")}</a>
            <a href="#research">{copy("Research library")}</a>
            <a href="#health">{copy("Health, explained")}</a>
            <a href="#ask">{copy("Ask BiGH Science")}</a>
          </div>
          <div>
            <h2>{copy("Here for you")}</h2>
            <Link href="/#products">{copy("Products")}</Link>
            <Link href="/#about">{copy("About BiGH")}</Link>
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
        <a href="#science-main">
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
