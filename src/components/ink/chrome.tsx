"use client";

import Image from "next/image";
import { ArrowUp } from "lucide-react";
import { Fragment, useEffect, useRef, type ReactNode } from "react";
import { ProductAction } from "@/components/home/product-action";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { footer, products } from "@/components/home-v2/content";
import { useSiteDialogs } from "./dialogs";
import { NavInscription, type NavCurrent } from "./nav/nav-inscription";
import styles from "./chrome.module.css";

// Header and footer for every ink page (the homepage first, October 2; shared October 5, 2026).
// The header is the menu bar Mo picked on October 5, 2026, "Inscription" (nav/nav-inscription.tsx):
// the BiGH mark centred like the title over a scroll painting, Products and Science opening the
// five bottles and the Science page's parts. Clear over a page's opening picture (`overlay`, with
// light or dark ink by `tone`), it settles on rice paper once the page scrolls. The page's own link
// carries aria-current. The footer keeps the About and Science pages' shape (large type for older
// readers, Design Vault #045), so the whole site reads as one.

function Logo() {
  const copy = useCopy();
  return (
    <Link href="/" aria-label={copy("BiGH home")} className={styles.footerLogo}>
      <span className={styles.logoCrop}>
        <Image
          src="/images/brand/bigh-logo-black-green.png"
          alt={copy("BiGH")}
          width={1448}
          height={811}
          sizes="136px"
          loading="lazy"
          className={styles.logoImage}
        />
      </span>
    </Link>
  );
}

/** Which page the header is on: its link is marked as the current page. */
export type Current = NavCurrent;

/** The site's menu bar (see nav/nav-inscription.tsx). */
export function SiteHeader({
  current,
  overlay = false,
  tone = "light",
  solidAfter = 80,
}: {
  /** The page this header is on. */
  current: Current;
  /** Start transparent over the opening picture. */
  overlay?: boolean;
  /** Ink over the opening: "light" = dark ink on a pale opening, "dark" = white ink on a dark one. */
  tone?: "light" | "dark";
  /** Scroll distance (px) after which the header turns solid. */
  solidAfter?: number;
}) {
  return <NavInscription current={current} overlay={overlay} tone={tone} solidAfter={solidAfter} />;
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

export function SiteFooter({
  closing,
}: {
  /** What the look closes on, set beside the promise (the Ink look: its crane at rest). */
  closing?: ReactNode;
} = {}) {
  const copy = useCopy();
  const dialogs = useSiteDialogs();
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
          <Logo />
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
