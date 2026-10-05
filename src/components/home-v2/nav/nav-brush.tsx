"use client";

import Image from "next/image";
import { useLocale } from "next-intl";
import { ArrowRight, X } from "lucide-react";
import {
  useEffect,
  useLayoutEffect,
  useRef,
  useState,
  type CSSProperties,
  type KeyboardEvent,
  type ReactNode,
} from "react";
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
import styles from "./nav-brush.module.css";

// Menu bar option A, "Brush" (October 5, 2026): the bar you know, painted in ink. One calm line,
// the BiGH mark at the left and the links at the right, clear over the opening painting and rice
// paper once the page moves. What makes it ours is the brush: the link you point at (or reach
// with the keyboard, or whose drop-down is open) gets a real sumi stroke under it, painted in from
// left to right as if the brush were moving, each link its own stroke. Products and Science open
// a full-width sheet of the same paper under the bar (Timeline's drop-down, Design Vault #004):
// the five bottles standing on one painted ground, or the Science page's four parts beside their
// paintings. Under 1101px the links are a full paper sheet whose last line is the crane at rest,
// standing on its stroke beside Log in and Sign up, the way the homepage's footer ends.

const pool = { src: "/images/home-v2/ink/pool.webp", width: 900, height: 482 };
const contact = { src: "/images/home-v2/ink/pool-foot.webp", width: 600, height: 170 };
const craneRest = { src: "/images/home-v2/ink/crane-rest-v2.webp", width: 560, height: 864 };

/** From this width (a tablet held upright) the narrow sheet opens with Products unfolded. */
const FOLD_OPEN_QUERY = "(min-width: 700px)";

/** The seven brush strokes, so neighbouring links never repeat one. */
type Stroke = 1 | 2 | 3 | 4 | 5 | 6 | 7;
const strokeClass = (n: Stroke) => styles[`s${n}`];

/** Two captions are two of the homepage's lines set as one (their translations are per line). */
const captionParts: Record<string, [string, string]> = {
  "Good science. Real people.": ["Good science.", "Real people."],
  "Curiosity, with references.": ["Curiosity,", "with references."],
};

/** A painted word: the stroke under it paints in when its link is pointed at or focused. */
function Word({ children, stroke }: { children: ReactNode; stroke: Stroke }) {
  return <span className={`${styles.word} ${strokeClass(stroke)}`}>{children}</span>;
}

export function NavBrush({ overlay = false, tone = "light", solidAfter = 48 }: HeaderProps) {
  const copy = useCopy();
  const locale = useLocale();
  const dialogs = useHomeDialogs();
  const nav = useNav({ overlay, solidAfter });
  const { panel, menuOpen, setMenuOpen, menuButton, closePanel } = nav;
  // Which of the Science sheet's parts is pointed at (its painting comes forward).
  const [part, setPart] = useState<number | null>(null);
  // The narrow sheet's two disclosures.
  const [fold, setFold] = useState<NavPanelId | null>(null);
  // The part of the homepage being read: its link in the bar carries its stroke, no pointer
  // needed (Products over the products; Science over the cell, the scientists, the science and
  // the research). Nothing at the opening, the stories or the purpose.
  const [reading, setReading] = useState<NavPanelId | null>(null);
  useEffect(() => {
    const order = [
      "top",
      "cellular",
      "scientists",
      "products",
      "stories",
      "science",
      "research",
      "purpose",
    ];
    const part: Record<string, NavPanelId> = {
      cellular: "science",
      scientists: "science",
      products: "products",
      science: "science",
      research: "science",
    };
    const sections = order
      .map((id) => document.getElementById(id))
      .filter((node): node is HTMLElement => node !== null);
    if (!sections.length) return;
    // A thin reading band a little above the window's middle: the part crossing it is the one
    // being read.
    const crossing = new Set<string>();
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) crossing.add(entry.target.id);
          else crossing.delete(entry.target.id);
        }
        const current = order.find((id) => crossing.has(id));
        setReading(current ? (part[current] ?? null) : null);
      },
      { rootMargin: "-38% 0px -60% 0px" },
    );
    sections.forEach((section) => observer.observe(section));
    return () => observer.disconnect();
  }, []);

  // The sheet is as tall as the panel on it. The last panel shown stays on it while the sheet
  // fades out; moving from one panel to the other, the sheet's edge glides to the new height.
  const [shown, setShown] = useState<NavPanelId>("products");
  if (panel && panel !== shown) setShown(panel);
  const stack = useRef<HTMLDivElement>(null);
  const lastPanel = useRef<NavPanelId | null>(null);
  useLayoutEffect(() => {
    const box = stack.current;
    const current = document.getElementById(`nav-panel-${shown}`);
    if (!box || !current) return;
    const glide = lastPanel.current !== null && panel !== null && lastPanel.current !== panel;
    box.style.transition = glide ? "height 0.55s var(--ease)" : "none";
    box.style.height = `${current.offsetHeight}px`;
    lastPanel.current = panel;
  }, [panel, shown]);
  useEffect(() => {
    const box = stack.current;
    const current = document.getElementById(`nav-panel-${shown}`);
    if (!box || !current) return;
    const observer = new ResizeObserver(() => {
      box.style.transition = "none";
      box.style.height = `${current.offsetHeight}px`;
    });
    observer.observe(current);
    return () => observer.disconnect();
  }, [shown]);

  const joined = (source: string) => {
    const parts = captionParts[source];
    if (!parts) return copy(source);
    const gap = locale === "jp" || locale === "cns" || locale === "hken" ? "" : " ";
    return `${copy(parts[0])}${gap}${copy(parts[1])}`;
  };

  const clear = overlay && !nav.solid && !panel && !menuOpen;
  const state = menuOpen || panel ? "open" : clear ? "clear" : "solid";

  const focusables = (root: Element | null | undefined) =>
    Array.from(
      root?.querySelectorAll<HTMLElement>(
        'a[href]:not([tabindex="-1"]), button:not([disabled]), select',
      ) ?? [],
    );

  /** A drop-down's button: the shared manners, plus Tab from an open button stepping into its
   *  panel (the panel follows the bar in the page, after all the links). */
  const trigger = (id: NavPanelId) => {
    const props = nav.triggerProps(id);
    return {
      ...props,
      "data-nav-trigger": id,
      "data-reading": reading === id ? "" : undefined,
      onKeyDown: (event: KeyboardEvent<HTMLButtonElement>) => {
        if (event.key !== "Tab" || event.shiftKey || panel !== id) return;
        const first = focusables(document.getElementById(`nav-panel-${id}`))[0];
        if (!first) return;
        event.preventDefault();
        first.focus();
      },
    };
  };

  /** Inside an open panel: Shift+Tab from its first link goes back to its button; Tab from its
   *  last link goes on to whatever follows the button in the bar, and the panel closes. */
  const panelKeys = (id: NavPanelId) => (event: KeyboardEvent<HTMLDivElement>) => {
    if (event.key !== "Tab") return;
    const items = focusables(event.currentTarget);
    const button = document.querySelector<HTMLElement>(`[data-nav-trigger="${id}"]`);
    if (!button || !items.length) return;
    if (event.shiftKey && event.target === items[0]) {
      event.preventDefault();
      button.focus();
    } else if (!event.shiftKey && event.target === items[items.length - 1]) {
      const bar = focusables(button.closest("nav"));
      const next = bar[bar.indexOf(button) + 1];
      if (!next) return;
      event.preventDefault();
      closePanel();
      next.focus();
    }
  };

  const panelProps = (id: NavPanelId) => ({
    ...nav.panelProps(id),
    "data-nav-panel": id,
    onKeyDown: panelKeys(id),
  });

  const openSupport = () => {
    // From the menu, focus goes to the menu's button first: the sheet hands focus back to where
    // it was when it closes, and this line is gone by then.
    if (menuOpen) menuButton.current?.focus();
    setMenuOpen(false);
    closePanel();
    dialogs.openSupport();
  };

  const closeAll = () => {
    closePanel();
    setMenuOpen(false);
  };

  return (
    <header
      className={styles.header}
      data-state={state}
      data-tone={clear ? tone : "light"}
      onBlur={nav.onHeaderBlur}
    >
      {/* The bar's paper: clear over the opening, 93% rice paper once scrolled, whole while a
          sheet is open under it. */}
      <div className={styles.ground} aria-hidden="true" />
      {/* The faint ink wash over the page while a drop-down is open; a click on it closes. */}
      <div
        className={styles.wash}
        data-open={panel ? "" : undefined}
        aria-hidden="true"
        onPointerDown={() => closePanel()}
      />

      <div className={styles.bar}>
        <NavLogo className={styles.logo} light={clear && tone === "dark"} />

        <nav id="site-navigation" aria-label={copy("Main navigation")} className={styles.links}>
          <button className={styles.link} {...trigger("products")}>
            <Word stroke={7}>{copy("Products")}</Word>
            <span className={`${styles.chev} ${styles.tick}`} aria-hidden="true" />
          </button>
          <button className={styles.link} {...trigger("science")}>
            <Word stroke={5}>{copy("Science")}</Word>
            <span className={`${styles.chev} ${styles.tick}`} aria-hidden="true" />
          </button>
          <Link href="/about" className={styles.link} onClick={closeAll}>
            <Word stroke={1}>{copy("About")}</Word>
          </Link>
          <button type="button" className={styles.link} onClick={openSupport}>
            <Word stroke={4}>{copy("Support")}</Word>
          </button>
          <div className={styles.utilities}>
            <HeaderUtilities />
          </div>
        </nav>

        <button
          ref={menuButton}
          type="button"
          className={styles.menuButton}
          data-nav-menu-button=""
          aria-label={copy(menuOpen ? "Close menu" : "Open menu")}
          aria-expanded={menuOpen}
          aria-controls="nav-sheet"
          onClick={() => {
            // On a tablet the sheet opens with Products unfolded, the five bottles filling the
            // paper above the crane; on a phone every line starts folded.
            if (!menuOpen) setFold(window.matchMedia(FOLD_OPEN_QUERY).matches ? "products" : null);
            setMenuOpen(!menuOpen);
          }}
        >
          {menuOpen && <X size={22} strokeWidth={1.75} aria-hidden="true" />}
          {/* "Menu" and "Close" (m585, m586): draft translations, reference/nav/translations-brush.cjs. */}
          <Word stroke={menuOpen ? 2 : 7}>{menuOpen ? copy("Close") : copy("Menu")}</Word>
        </button>
      </div>

      {/* The drop-down sheet: one sheet of paper under the bar for both panels, so moving from
          Products to Science changes what is on it without closing it. */}
      <div className={styles.sheet} data-open={panel ? "" : undefined}>
        <div ref={stack} className={styles.stack}>
          <div className={styles.panel} {...panelProps("products")}>
            <div className={`${styles.column} ${styles.productsPanel}`}>
              <div className={styles.lede}>
                <p className={`${styles.headline} ${styles.rise}`}>
                  {copy(navProductsIntro.headline)}
                </p>
                <Link
                  href={navProductsIntro.allLink}
                  className={`${styles.textLink} ${styles.rise}`}
                  onClick={() => closePanel()}
                >
                  <Word stroke={3}>{copy("Explore all products")}</Word>
                  <ArrowRight className={styles.arrow} size={18} aria-hidden="true" />
                </Link>
              </div>
              {/* The five stand on one painted ground, at low ink. */}
              <ul className={styles.shelf}>
                {navProducts.map((product, i) => (
                  <li key={product.slug} style={{ "--i": i } as CSSProperties}>
                    <Link href={product.href} className={styles.product} onClick={closeAll}>
                      <span className={styles.stand}>
                        <Image
                          className={`${styles.pool} ${styles.rise}`}
                          src={pool.src}
                          alt=""
                          width={pool.width}
                          height={pool.height}
                          sizes="120px"
                        />
                        <Image
                          className={`${styles.contact} ${styles.rise}`}
                          src={contact.src}
                          alt=""
                          width={contact.width}
                          height={contact.height}
                          sizes="100px"
                        />
                        <Image
                          className={`${styles.bottle} ${styles.rise}`}
                          src={product.bottle.src}
                          alt=""
                          width={product.bottle.width}
                          height={product.bottle.height}
                          sizes="180px"
                        />
                      </span>
                      <span className={`${styles.name} ${styles.rise}`}>
                        <Word stroke={([1, 2, 4, 7, 5] as const)[i]}>{copy(product.name)}</Word>
                      </span>
                      <span className={`${styles.focus} ${styles.rise}`}>
                        {copy(product.focus)}
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className={styles.panel} {...panelProps("science")}>
            <div
              className={`${styles.column} ${styles.sciencePanel}`}
              data-part={part ?? undefined}
              onPointerLeave={() => setPart(null)}
            >
              <div className={styles.lede}>
                <ul className={styles.parts}>
                  {navScience.map((item, i) => (
                    <li
                      key={item.href}
                      className={styles.rise}
                      style={{ "--i": i } as CSSProperties}
                    >
                      <Link
                        href={item.href}
                        className={styles.part}
                        data-on={part === i ? "" : undefined}
                        onPointerEnter={() => setPart(i)}
                        onFocus={() => setPart(i)}
                        onBlur={() => setPart(null)}
                        onClick={closeAll}
                      >
                        <Word stroke={([7, 1, 5, 3] as const)[i]}>{copy(item.label)}</Word>
                        <ArrowRight className={styles.arrow} size={22} aria-hidden="true" />
                      </Link>
                    </li>
                  ))}
                </ul>
                <Link
                  href={navScienceIntro.href}
                  className={`${styles.textLink} ${styles.rise}`}
                  onClick={() => closePanel()}
                >
                  <Word stroke={4}>{copy(navScienceIntro.link)}</Word>
                  <ArrowRight className={styles.arrow} size={18} aria-hidden="true" />
                </Link>
              </div>
              <div className={styles.figures}>
                {navScience.map((item, i) => (
                  // The list says the same; the pictures are for the pointer, not a second set of
                  // Tab stops.
                  <Link
                    key={item.href}
                    href={item.href}
                    tabIndex={-1}
                    className={styles.figure}
                    data-on={part === i ? "" : undefined}
                    data-photo={item.image.photo ? "" : undefined}
                    style={{ "--i": i } as CSSProperties}
                    onPointerEnter={() => setPart(i)}
                    onClick={closeAll}
                  >
                    <span className={styles.pic}>
                      {item.image.photo ? (
                        <span className={`${styles.mat} ${styles.rise}`}>
                          <Image
                            src={item.image.src}
                            alt=""
                            width={item.image.width}
                            height={item.image.height}
                            sizes="160px"
                          />
                        </span>
                      ) : (
                        <Image
                          className={`${styles.painting} ${styles.rise}`}
                          // The still life keeps its paper's edge: cropped and dissolved, as on
                          // the homepage.
                          data-still={item.image.src.includes("/story-") ? "" : undefined}
                          src={item.image.src}
                          alt=""
                          fill
                          sizes="280px"
                        />
                      )}
                    </span>
                    <span className={`${styles.caption} ${styles.rise}`}>
                      {joined(item.caption)}
                      <ArrowRight className={styles.arrow} size={16} aria-hidden="true" />
                    </span>
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* The narrow window's menu: a full sheet of the page's paper under the bar. */}
      {menuOpen && (
        <nav
          id="nav-sheet"
          aria-label={copy("Main navigation")}
          className={styles.menu}
          data-nav-sheet=""
          // The open menu scrolls by itself; Lenis leaves the wheel alone over it.
          data-lenis-prevent=""
        >
          <ul className={styles.lines}>
            <li style={{ "--n": 1 } as CSSProperties}>
              <Fold
                id="products"
                label={copy("Products")}
                open={fold === "products"}
                onToggle={() => setFold(fold === "products" ? null : "products")}
              >
                <ul className={styles.row} aria-label={copy("BiGH products")}>
                  {navProducts.map((product) => (
                    <li key={product.slug}>
                      <Link href={product.href} className={styles.mini} onClick={closeAll}>
                        <span className={styles.stand}>
                          <Image
                            className={styles.pool}
                            src={pool.src}
                            alt=""
                            width={pool.width}
                            height={pool.height}
                            sizes="90px"
                            loading="eager"
                          />
                          <Image
                            className={styles.contact}
                            src={contact.src}
                            alt=""
                            width={contact.width}
                            height={contact.height}
                            sizes="70px"
                            loading="eager"
                          />
                          <Image
                            className={styles.bottle}
                            src={product.bottle.src}
                            alt=""
                            width={product.bottle.width}
                            height={product.bottle.height}
                            sizes="130px"
                            loading="eager"
                          />
                        </span>
                        <span className={styles.miniName}>{copy(product.name)}</span>
                      </Link>
                    </li>
                  ))}
                </ul>
                <Link
                  href={navProductsIntro.allLink}
                  className={styles.foldLink}
                  onClick={closeAll}
                >
                  {copy("Explore all products")}
                  <ArrowRight size={20} aria-hidden="true" />
                </Link>
              </Fold>
            </li>
            <li style={{ "--n": 2 } as CSSProperties}>
              <Fold
                id="science"
                label={copy("Science")}
                open={fold === "science"}
                onToggle={() => setFold(fold === "science" ? null : "science")}
              >
                <ul className={styles.foldList}>
                  {navScience.map((item) => (
                    <li key={item.href}>
                      <Link href={item.href} className={styles.foldLink} onClick={closeAll}>
                        {copy(item.label)}
                        <ArrowRight size={20} aria-hidden="true" />
                      </Link>
                    </li>
                  ))}
                  <li>
                    <Link
                      href={navScienceIntro.href}
                      className={styles.foldLink}
                      onClick={closeAll}
                    >
                      {copy(navScienceIntro.link)}
                      <ArrowRight size={20} aria-hidden="true" />
                    </Link>
                  </li>
                </ul>
              </Fold>
            </li>
            <li style={{ "--n": 3 } as CSSProperties}>
              <Link href="/about" className={styles.line} onClick={closeAll}>
                {copy("About")}
              </Link>
            </li>
            <li style={{ "--n": 4 } as CSSProperties}>
              <button type="button" className={styles.line} onClick={openSupport}>
                {copy("Support")}
              </button>
            </li>
          </ul>

          {/* The sheet ends the way the homepage does: the crane at rest on its stroke, beside
              Log in, Sign up and the language. */}
          <div className={styles.foot} style={{ "--n": 5.5 } as CSSProperties}>
            <div className={styles.footUtilities}>
              <HeaderUtilities />
            </div>
            <Image
              className={styles.crane}
              src={craneRest.src}
              alt=""
              width={craneRest.width}
              height={craneRest.height}
              sizes="120px"
              loading="eager"
            />
            <span className={styles.footStroke} aria-hidden="true" />
          </div>
        </nav>
      )}
    </header>
  );
}

/** One of the narrow sheet's big lines that unfolds (Products, Science). */
function Fold({
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
    <>
      <button
        type="button"
        className={styles.line}
        aria-expanded={open}
        aria-controls={`nav-fold-${id}`}
        data-nav-sheet-toggle={id}
        onClick={onToggle}
      >
        {label}
        <span className={`${styles.chev} ${styles.tick}`} aria-hidden="true" />
      </button>
      <div
        id={`nav-fold-${id}`}
        className={styles.fold}
        data-open={open ? "" : undefined}
        inert={!open}
      >
        <div className={styles.foldInner}>{children}</div>
      </div>
    </>
  );
}
