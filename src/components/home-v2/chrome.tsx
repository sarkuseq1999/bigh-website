"use client";

import Image from "next/image";
import { ArrowUp, Menu, X } from "lucide-react";
import { useEffect, useState } from "react";
import { HeaderUtilities } from "@/components/home/header-utilities";
import { ProductAction } from "@/components/home/product-action";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { footer, products } from "./content";
import { useHomeDialogs } from "./dialogs";
import styles from "./chrome.module.css";

// Header and footer for the redesigned homepage. Same shape, sizes and links as the About and
// Science pages' chrome (large navigation for older readers, Design Vault #045), so the whole site
// reads as one. A look can start the header transparent over a full-bleed opening (`overlay`) and
// pick light or dark ink for that state (`tone`); it turns solid paper once the page scrolls.

function Logo({ footer: isFooter = false, light = false }: { footer?: boolean; light?: boolean }) {
  const copy = useCopy();
  return (
    <Link
      href="/"
      aria-label={copy("BiGH home")}
      className={isFooter ? styles.footerLogo : styles.logo}
    >
      <span className={styles.logoCrop}>
        <Image
          src={
            light ? "/images/brand/bigh-logo-white.png" : "/images/brand/bigh-logo-black-green.png"
          }
          alt={copy("BiGH")}
          width={1448}
          height={811}
          sizes={isFooter ? "170px" : "136px"}
          loading={isFooter ? "lazy" : "eager"}
          className={styles.logoImage}
        />
      </span>
    </Link>
  );
}

export function HomeHeader({
  overlay = false,
  tone = "light",
  solidAfter = 80,
}: {
  /** Start transparent over the opening picture. */
  overlay?: boolean;
  /** Ink over the opening: "light" = dark ink on a pale opening, "dark" = white ink on a dark one. */
  tone?: "light" | "dark";
  /** Scroll distance (px) after which the header turns solid. */
  solidAfter?: number;
}) {
  const copy = useCopy();
  const dialogs = useHomeDialogs();
  const [open, setOpen] = useState(false);
  const [solid, setSolid] = useState(!overlay);
  const close = () => setOpen(false);

  useEffect(() => {
    if (!overlay) return;
    const update = () => setSolid(window.scrollY > solidAfter);
    update();
    window.addEventListener("scroll", update, { passive: true });
    return () => window.removeEventListener("scroll", update);
  }, [overlay, solidAfter]);

  const clear = overlay && !solid && !open;
  const lightLogo = clear && tone === "dark";

  return (
    <header
      className={`${styles.header} ${open ? styles.open : ""} ${clear ? styles.clear : ""}`}
      data-tone={clear ? tone : "light"}
    >
      <div className={styles.bar}>
        <Logo light={lightLogo} />
        <nav id="home-navigation" aria-label={copy("Main navigation")} className={styles.nav}>
          <Link href="/" aria-current="page" onClick={close}>
            {copy("Home")}
          </Link>
          <a href="#products" onClick={close}>
            {copy("Products")}
          </a>
          <Link href="/science" onClick={close}>
            {copy("Science")}
          </Link>
          <Link href="/about" onClick={close}>
            {copy("About")}
          </Link>
          <button
            type="button"
            onClick={() => {
              close();
              dialogs.openSupport();
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
          aria-controls="home-navigation"
          onClick={() => setOpen(!open)}
        >
          {open ? <X size={26} /> : <Menu size={26} />}
        </button>
      </div>
    </header>
  );
}

export function HomeFooter() {
  const copy = useCopy();
  const dialogs = useHomeDialogs();
  return (
    <footer className={styles.footer}>
      <div className={styles.footerTop}>
        <div>
          <Logo footer />
          <p className={styles.footerMessage}>
            <span data-brush="footer-tagline">{copy(footer.tagline)}</span>
          </p>
        </div>
        <div className={styles.footerColumns}>
          <div>
            <h2>{copy("Products")}</h2>
            {products.map((product) => (
              <ProductAction
                key={product.name}
                name={product.name}
                onOpen={() => dialogs.openProduct(product.index)}
              >
                {product.name}
              </ProductAction>
            ))}
          </div>
          <div>
            <h2>{copy("Science")}</h2>
            <Link href="/science#scientists">{copy("Our scientists")}</Link>
            <Link href="/science#health">{copy("Cellular health")}</Link>
            <Link href="/science#research">{copy("Research library")}</Link>
            <Link href="/science#ask">{copy("Ask BiGH Science")}</Link>
          </div>
          <div>
            <h2>{copy("Here for you")}</h2>
            <Link href="/about">{copy("About BiGH")}</Link>
            <button type="button" onClick={dialogs.openSupport}>
              {copy("Support & FAQs")}
            </button>
            <Link href="/science#health">{copy("Health, explained")}</Link>
          </div>
        </div>
      </div>
      <div className={styles.footerBottom}>
        <span>
          © {new Date().getFullYear()} {copy("BiGH. Be in Good Health.")}
        </span>
        <a href="#top">
          {copy("Back to top")} <ArrowUp size={16} />
        </a>
      </div>
      <p className={styles.footerNote}>{copy(footer.note)}</p>
    </footer>
  );
}
