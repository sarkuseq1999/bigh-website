"use client";

import Image from "next/image";
import { ArrowUp, Menu, X } from "lucide-react";
import { Fragment, useEffect, useRef, useState, type FocusEvent, type ReactNode } from "react";
import { HeaderUtilities } from "@/components/home/header-utilities";
import { ProductAction } from "@/components/home/product-action";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { footer, products } from "./content";
import { useHomeDialogs } from "./dialogs";
import { lockPageScroll } from "./lock-scroll";
import styles from "./chrome.module.css";

// Header and footer for the redesigned homepage. Same shape, sizes and links as the About and
// Science pages' chrome (large navigation for older readers, Design Vault #045), so the whole site
// reads as one. A look can start the header transparent over a full-bleed opening (`overlay`) and
// pick light or dark ink for that state (`tone`); it turns solid paper once the page scrolls.
// On a narrow window the links are a menu: a full sheet of the page's paper under the bar. Its
// button comes before it in the page, so Tab goes from the button into the links; Escape closes
// it and hands focus back to the button; tabbing out of it closes it.

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
          sizes="136px"
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
  const menuButton = useRef<HTMLButtonElement>(null);
  const close = () => setOpen(false);

  useEffect(() => {
    if (!overlay) return;
    const update = () => setSolid(window.scrollY > solidAfter);
    update();
    window.addEventListener("scroll", update, { passive: true });
    return () => window.removeEventListener("scroll", update);
  }, [overlay, solidAfter]);

  // While the menu is open the page under it stays put, Escape closes it, and it closes by
  // itself when the window grows into the desktop bar.
  useEffect(() => {
    if (!open) return;
    const onKey = (event: KeyboardEvent) => {
      if (event.key !== "Escape") return;
      // The open language list closes first, on its own Escape.
      const target = event.target;
      if (target instanceof HTMLOptionElement) return;
      if (target instanceof HTMLSelectElement && CSS.supports("selector(:open)")) {
        if (target.matches(":open")) return;
      }
      setOpen(false);
      menuButton.current?.focus();
    };
    const desktop = window.matchMedia("(min-width: 1101px)");
    const onDesktop = () => {
      if (desktop.matches) setOpen(false);
    };
    document.addEventListener("keydown", onKey);
    desktop.addEventListener("change", onDesktop);
    const unlock = lockPageScroll();
    return () => {
      document.removeEventListener("keydown", onKey);
      desktop.removeEventListener("change", onDesktop);
      unlock();
    };
  }, [open]);

  // Tabbing past the menu's last control closes it: focus is never on the page hidden under it.
  const onBlur = (event: FocusEvent<HTMLElement>) => {
    const next = event.relatedTarget;
    if (open && next instanceof Node && !event.currentTarget.contains(next)) setOpen(false);
  };

  const clear = overlay && !solid && !open;
  const lightLogo = clear && tone === "dark";

  return (
    <header
      className={`${styles.header} ${open ? styles.open : ""} ${clear ? styles.clear : ""}`}
      data-tone={clear ? tone : "light"}
      onBlur={onBlur}
    >
      <div className={styles.bar}>
        <Logo light={lightLogo} />
        <button
          ref={menuButton}
          type="button"
          className={styles.menuButton}
          aria-label={copy(open ? "Close menu" : "Open menu")}
          aria-expanded={open}
          aria-controls="home-navigation"
          onClick={() => setOpen(!open)}
        >
          {open ? <X size={26} aria-hidden="true" /> : <Menu size={26} aria-hidden="true" />}
        </button>
        <nav
          id="home-navigation"
          aria-label={copy("Main navigation")}
          className={styles.nav}
          // The open menu scrolls by itself; Lenis leaves the wheel alone over it.
          data-lenis-prevent={open ? "" : undefined}
        >
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
              // From the menu, focus goes to the menu's button first: the sheet hands focus back
              // to where it was when it closes, and this link is gone by then.
              if (open) menuButton.current?.focus();
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
      </div>
    </header>
  );
}

/** The promise breaks only between its sentences ("Stay sharp." / "Live fully."), in every
 *  language: each sentence is one unbroken piece unless it is too long for the line. (The
 *  products' headlines are set the same way.) */
export function Sentences({ text }: { text: string }) {
  const parts = text.match(/[^.!?。！？]+[.!?。！？]*\s*/gu) ?? [text];
  return (
    <>
      {parts.map((part, i) => (
        <Fragment key={part}>
          <span className={styles.sentence}>{part.trimEnd()}</span>
          {i < parts.length - 1 && (/\s$/.test(part) ? " " : <wbr />)}
        </Fragment>
      ))}
    </>
  );
}

export function HomeFooter({
  closing,
}: {
  /** What the look closes on, set beside the promise (the Ink look: its crane at rest). */
  closing?: ReactNode;
} = {}) {
  const copy = useCopy();
  const dialogs = useHomeDialogs();
  const message = useRef<HTMLParagraphElement>(null);
  const hasClosing = Boolean(closing);

  // A paragraph that wraps keeps its full width, however short its lines are. With a closing
  // picture beside it, the promise is narrowed to its longest line, so the picture stands next
  // to the words and not across a gap.
  useEffect(() => {
    const paragraph = message.current;
    const words = paragraph?.firstElementChild;
    // The finale's band, whose width decides where the lines break.
    const column = paragraph?.parentElement?.parentElement;
    if (!paragraph || !words || !column || !hasClosing) return;
    // The words' own line boxes (text only: a sentence that wraps inside its inline block still
    // reports the block's full width, so the blocks themselves are not measured).
    const boxes = () => {
      const found: DOMRect[] = [];
      const walker = document.createTreeWalker(words, NodeFilter.SHOW_TEXT);
      const range = document.createRange();
      while (walker.nextNode()) {
        range.selectNodeContents(walker.currentNode);
        found.push(...range.getClientRects());
      }
      return found.filter((box) => box.width > 0);
    };
    const lines = () => new Set(boxes().map((box) => Math.round(box.top))).size;
    const fit = () => {
      paragraph.style.width = "";
      const natural = lines();
      const text = boxes();
      if (!text.length) return;
      const left = Math.min(...text.map((box) => box.left));
      const right = Math.max(...text.map((box) => box.right));
      let width = Math.ceil(right - left) + 1;
      paragraph.style.width = `${width}px`;
      // Never let the fitted width push a word onto a line of its own.
      for (let i = 0; i < 12 && lines() > natural; i++) {
        width += 4;
        paragraph.style.width = `${width}px`;
      }
    };
    fit();
    const observer = new ResizeObserver(fit);
    observer.observe(column);
    // A face that arrives late (Vietnamese, the CJK fallbacks) changes the lines' widths.
    document.fonts?.ready.then(fit);
    document.fonts?.addEventListener("loadingdone", fit);
    return () => {
      observer.disconnect();
      document.fonts?.removeEventListener("loadingdone", fit);
      paragraph.style.width = "";
    };
  }, [hasClosing]);

  // The finale first: the promise in its own band, large, with the look's closing picture beside
  // it. Under a hairline, the logo, the links and the legal lines are a calmer second tier (on
  // two columns the copyright line and "Back to top" sit under the logo, level with the last
  // link; on one column they follow the links).
  return (
    <footer className={styles.footer}>
      <div className={styles.finale}>
        <div className={styles.promise} data-brush="footer-promise">
          <p ref={message} className={styles.footerMessage}>
            <span data-brush="footer-tagline">
              <Sentences text={copy(footer.tagline)} />
            </span>
          </p>
          {closing}
        </div>
      </div>
      <div className={styles.footerTop}>
        <div className={styles.footerBrand}>
          <Logo footer />
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
        <div className={styles.footerBottom}>
          <span>
            © {new Date().getFullYear()} {copy("BiGH. Be in Good Health.")}
          </span>
          <a href="#top">
            {copy("Back to top")} <ArrowUp size={16} />
          </a>
        </div>
      </div>
      <p className={styles.footerNote}>{copy(footer.note)}</p>
    </footer>
  );
}
