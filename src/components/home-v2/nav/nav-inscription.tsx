"use client";

import Image from "next/image";
import { ArrowRight, ChevronDown, X } from "lucide-react";
import { useLocale } from "next-intl";
import { useEffect, useRef, useState, type CSSProperties, type ReactNode } from "react";
import { HeaderUtilities } from "@/components/home/header-utilities";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import type { HeaderProps } from "../chrome";
import { useHomeDialogs } from "../dialogs";
import {
  navProducts,
  navProductsIntro,
  navScience,
  navScienceIntro,
  type NavPanelId,
} from "./nav-data";
import { NavLogo } from "./nav-logo";
import { useNav } from "./use-nav";
import styles from "./nav-inscription.module.css";

// Menu bar option C, "Inscription" (October 5, 2026). A Chinese hanging scroll carries its title
// centred above the painting; this bar does the same over the crane. The BiGH mark stands in the
// middle, large, with two links on each side of it (Products, Science | About, Support) set as one
// balanced line; the language at the far left, Log in and Sign up at the far right. Over the
// opening painting the bar is clear; once the page moves on it settles a little smaller on rice
// paper, and its edge is a long, fine, dry brush line instead of a hairline.
// Products and Science let down a sheet of rice paper from under the bar, the way a hanging scroll
// unrolls: revealed top to bottom, its leading edge torn rice paper, over a faint ink wash on the
// page. Everything on it is centred, like the bar. Moving from one to the other keeps the scroll
// down and changes only what is written on it. On a narrow window: "Menu", the mark, the
// language; the menu is a full-height scroll let down the same way.
// Each drop-down's links follow its button in the page, so Tab goes from the button into them.

export function NavInscription({ overlay = false, tone = "light", solidAfter = 80 }: HeaderProps) {
  const copy = useCopy();
  const locale = useLocale();
  const dialogs = useHomeDialogs();
  const nav = useNav({ overlay, solidAfter });
  const { solid, panel, closePanel, menuOpen, setMenuOpen, menuButton } = nav;
  const cjk = locale === "jp" || locale === "cns" || locale === "hken";

  // The scroll keeps showing the last drop-down while it rolls back up.
  const [shown, setShown] = useState<NavPanelId>("products");
  if (panel && panel !== shown) setShown(panel);

  // The narrow window's menu: one of its two parts (Products, Science) is unfolded at a time.
  // On a tablet (700px and wider) it opens with Products unfolded: the five fit in one row.
  const [part, setPart] = useState<NavPanelId | null>(null);
  const [wasOpen, setWasOpen] = useState(menuOpen);
  if (menuOpen !== wasOpen) {
    setWasOpen(menuOpen);
    if (!menuOpen) setPart(null);
  }

  // The scroll is as long as the taller of the two drop-downs, so it never changes length when
  // you move from one to the other.
  const productsInner = useRef<HTMLDivElement>(null);
  const scienceInner = useRef<HTMLDivElement>(null);
  const [panelHeight, setPanelHeight] = useState(0);
  useEffect(() => {
    const inners = [productsInner.current, scienceInner.current].filter(
      (node): node is HTMLDivElement => Boolean(node),
    );
    const measure = () =>
      setPanelHeight(Math.ceil(Math.max(0, ...inners.map((node) => node.offsetHeight))));
    measure();
    const observer = new ResizeObserver(measure);
    inners.forEach((node) => observer.observe(node));
    document.fonts?.ready.then(measure);
    return () => observer.disconnect();
  }, []);

  /** Captions the site translates in two halves ("Good science." / "Real people."). */
  const caption = (text: string) => {
    const whole = copy(text);
    if (whole !== text || locale === "en") return whole;
    const parts = text.match(/[^.,]+[.,]?\s*/g) ?? [text];
    return parts.map((piece) => copy(piece.trim())).join(cjk ? "" : " ");
  };

  const clear = overlay && !solid && !panel && !menuOpen;
  const ground = panel || menuOpen ? "paper" : clear ? "clear" : "solid";

  const openSupport = () => {
    if (menuOpen) {
      // From the menu, focus goes to its button first: the sheet hands focus back to where it
      // was when it closes, and this link is gone by then.
      menuButton.current?.focus();
      setMenuOpen(false);
    }
    closePanel();
    dialogs.openSupport();
  };

  return (
    <header
      className={styles.root}
      data-size={solid ? "small" : "tall"}
      data-ground={ground}
      data-tone={clear ? tone : "light"}
      data-unrolled={panel ? "" : undefined}
      data-menu={menuOpen ? "" : undefined}
      style={{ "--insc-panel-h": `${panelHeight}px` } as CSSProperties}
      onBlur={nav.onHeaderBlur}
    >
      <span className={styles.ground} aria-hidden="true" />
      <span className={styles.rule} aria-hidden="true" />

      <nav id="site-navigation" aria-label={copy("Main navigation")} className={styles.bar}>
        <div className={styles.left}>
          <div className={styles.language}>
            <HeaderUtilities />
          </div>
          <button
            ref={menuButton}
            type="button"
            className={styles.menuButton}
            aria-label={copy(menuOpen ? "Close menu" : "Open menu")}
            aria-expanded={menuOpen}
            aria-controls="nav-sheet"
            data-nav-menu-button=""
            onClick={() => {
              if (!menuOpen) {
                setPart(window.matchMedia("(min-width: 700px)").matches ? "products" : null);
              }
              setMenuOpen(!menuOpen);
            }}
          >
            {menuOpen && <X size={20} strokeWidth={1.75} aria-hidden="true" />}
            <span>{copy(menuOpen ? "Close" : "Menu")}</span>
          </button>
          <div className={styles.links}>
            <button
              {...nav.triggerProps("products")}
              className={styles.link}
              data-nav-trigger="products"
            >
              <span className={styles.word}>{copy("Products")}</span>
              <ChevronDown className={styles.chevron} size={14} aria-hidden="true" />
            </button>
            <div
              {...nav.panelProps("products")}
              className={styles.panel}
              data-nav-panel="products"
              data-shown={shown === "products" ? "" : undefined}
            >
              <div ref={productsInner} className={styles.panelInner}>
                <h2 className={styles.panelTitle}>{copy(navProductsIntro.headline)}</h2>
                <div className={styles.shelfWrap}>
                  <span className={styles.shelfGround} aria-hidden="true" />
                  <ul className={styles.shelf}>
                    {navProducts.map((product, i) => (
                      <li key={product.slug} style={{ "--i": i } as CSSProperties}>
                        <Link
                          href={product.href}
                          className={styles.product}
                          onClick={() => closePanel()}
                        >
                          <Bottle src={product.bottle.src} sizes="180px" />
                          <span className={styles.productName}>{copy(product.name)}</span>
                          <span className={styles.productFocus}>{copy(product.focus)}</span>
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
                <Link
                  href={navProductsIntro.allLink}
                  className={styles.more}
                  onClick={() => closePanel()}
                >
                  {copy(navProductsIntro.title)}
                  <ArrowRight size={18} aria-hidden="true" />
                </Link>
              </div>
            </div>
            <button
              {...nav.triggerProps("science")}
              className={styles.link}
              data-nav-trigger="science"
            >
              <span className={styles.word}>{copy("Science")}</span>
              <ChevronDown className={styles.chevron} size={14} aria-hidden="true" />
            </button>
            <div
              {...nav.panelProps("science")}
              className={styles.panel}
              data-nav-panel="science"
              data-shown={shown === "science" ? "" : undefined}
            >
              <div ref={scienceInner} className={styles.panelInner}>
                <h2 className={styles.panelTitle}>{copy(navScienceIntro.title)}</h2>
                <ul className={styles.gallery}>
                  {navScience.map((item, i) => (
                    <li key={item.href} style={{ "--i": i } as CSSProperties}>
                      <Link href={item.href} className={styles.part} onClick={() => closePanel()}>
                        <span className={styles.frame}>
                          {item.image.photo ? (
                            <span className={styles.mat}>
                              <Image
                                src={item.image.src}
                                alt=""
                                width={item.image.width}
                                height={item.image.height}
                                sizes="120px"
                                className={styles.photo}
                              />
                            </span>
                          ) : (
                            <Image
                              src={item.image.src}
                              alt=""
                              fill
                              sizes="280px"
                              className={styles.painting}
                              data-painting={item.image.src.split("/").pop()?.split(".")[0]}
                            />
                          )}
                        </span>
                        <span className={styles.partLabel}>{copy(item.label)}</span>
                        <span className={styles.partCaption}>{caption(item.caption)}</span>
                      </Link>
                    </li>
                  ))}
                </ul>
                <Link
                  href={navScienceIntro.href}
                  className={styles.more}
                  onClick={() => closePanel()}
                >
                  {copy(navScienceIntro.link)}
                  <ArrowRight size={18} aria-hidden="true" />
                </Link>
              </div>
            </div>
          </div>
        </div>

        <NavLogo className={styles.mark} light={clear && tone === "dark"} />

        <div className={styles.right}>
          <div className={styles.links}>
            <Link href="/about" className={styles.link}>
              <span className={styles.word}>{copy("About")}</span>
            </Link>
            <button type="button" className={styles.link} onClick={openSupport}>
              <span className={styles.word}>{copy("Support")}</span>
            </button>
          </div>
          <div className={styles.account}>
            <HeaderUtilities />
          </div>
        </div>
      </nav>

      {/* The scroll the drop-downs are written on, and the wash it is let down over. */}
      <span className={styles.paper} aria-hidden="true" />
      <span className={styles.wash} aria-hidden="true" onClick={() => closePanel()} />

      {/* The narrow window's menu: a full-height scroll let down from under the bar. */}
      <div
        id="nav-sheet"
        className={styles.sheet}
        data-nav-sheet=""
        inert={!menuOpen}
        data-lenis-prevent={menuOpen ? "" : undefined}
      >
        <div className={styles.sheetInner}>
          <SheetPart
            id="products"
            label={copy("Products")}
            open={part === "products"}
            onToggle={() => setPart(part === "products" ? null : "products")}
          >
            <div className={styles.sheetShelfWrap}>
              <span className={styles.sheetGround} aria-hidden="true" />
              <ul className={styles.sheetShelf}>
                {navProducts.map((product) => (
                  <li key={product.slug}>
                    <Link
                      href={product.href}
                      className={styles.sheetProduct}
                      onClick={() => setMenuOpen(false)}
                    >
                      <Bottle src={product.bottle.src} sizes="(max-width: 699px) 34vw, 150px" />
                      <span className={styles.sheetProductName}>{copy(product.name)}</span>
                      <span className={styles.sheetProductFocus}>{copy(product.focus)}</span>
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
            <Link
              href={navProductsIntro.allLink}
              className={styles.more}
              onClick={() => setMenuOpen(false)}
            >
              {copy(navProductsIntro.title)}
              <ArrowRight size={18} aria-hidden="true" />
            </Link>
          </SheetPart>
          <span className={styles.dab} aria-hidden="true" />
          <SheetPart
            id="science"
            label={copy("Science")}
            open={part === "science"}
            onToggle={() => setPart(part === "science" ? null : "science")}
          >
            <ul className={styles.sheetList}>
              {navScience.map((item) => (
                <li key={item.href}>
                  <Link href={item.href} onClick={() => setMenuOpen(false)}>
                    {copy(item.label)}
                  </Link>
                </li>
              ))}
            </ul>
            <Link
              href={navScienceIntro.href}
              className={styles.more}
              onClick={() => setMenuOpen(false)}
            >
              {copy(navScienceIntro.link)}
              <ArrowRight size={18} aria-hidden="true" />
            </Link>
          </SheetPart>
          <span className={styles.dab} aria-hidden="true" />
          <Link href="/about" className={styles.sheetLink} onClick={() => setMenuOpen(false)}>
            {copy("About")}
          </Link>
          <span className={styles.dab} aria-hidden="true" />
          <button type="button" className={styles.sheetLink} onClick={openSupport}>
            {copy("Support")}
          </button>
          <div className={styles.sheetPainting} aria-hidden="true">
            <Image
              className={styles.sheetCrane}
              src="/images/home-v2/ink/crane-rest-v2.webp"
              alt=""
              width={560}
              height={864}
              sizes="170px"
            />
          </div>
          <div className={styles.sheetFoot}>
            <HeaderUtilities />
          </div>
        </div>
      </div>
    </header>
  );
}

/** A product photograph standing on its pale ink pool. */
function Bottle({ src, sizes }: { src: string; sizes: string }) {
  return (
    <span className={styles.stand}>
      <Image
        className={styles.pool}
        src="/images/home-v2/ink/pool.webp"
        alt=""
        width={900}
        height={482}
        sizes="120px"
      />
      <Image
        className={styles.contact}
        src="/images/home-v2/ink/pool-foot.webp"
        alt=""
        width={600}
        height={170}
        sizes="100px"
      />
      <Image className={styles.bottle} src={src} alt="" width={1230} height={1278} sizes={sizes} />
    </span>
  );
}

/** One of the menu's two folding parts: its word, and under it what it holds. */
function SheetPart({
  id,
  label,
  open,
  onToggle,
  children,
}: {
  id: NavPanelId;
  label: string;
  open: boolean;
  onToggle: () => void;
  children: ReactNode;
}) {
  return (
    <div className={styles.sheetPart} data-open={open ? "" : undefined}>
      <button
        type="button"
        className={styles.sheetLink}
        aria-expanded={open}
        aria-controls={`nav-sheet-${id}`}
        data-nav-sheet-toggle={id}
        onClick={onToggle}
      >
        {label}
        <ChevronDown className={styles.chevron} size={24} strokeWidth={1.75} aria-hidden="true" />
      </button>
      <div id={`nav-sheet-${id}`} className={styles.sheetFold} inert={!open}>
        <div className={styles.sheetFoldInner}>{children}</div>
      </div>
    </div>
  );
}
