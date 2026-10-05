"use client";

import Image from "next/image";
import { ArrowRight, ChevronDown, X } from "lucide-react";
import { useLocale } from "next-intl";
import {
  useEffect,
  useLayoutEffect,
  useRef,
  useState,
  type CSSProperties,
  type KeyboardEvent,
} from "react";
import { HeaderUtilities } from "@/components/home/header-utilities";
import { Link } from "@/i18n/navigation";
import copyKeys from "@/i18n/copy-keys.json";
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
import styles from "./nav-stone.module.css";

// Menu bar option B, "Ink stone" (October 5, 2026): an ink stone resting on the paper.
//
// The stone is there from the first screen: the big ink mark stands on the paper at the left,
// over the opening's words, and the links already rest in a pill of sumi ink at the column's right
// edge, the same family as the opening's solid "Discover NuriCell" pill (the two ink pills balance
// the painting between them). Once the page moves (the shared `solid`, 48px) the mark slides into
// the stone's left end, turning white as it reaches the ink, and the stone glides to the centre:
// one calm move, reversed at the top. Its edge is a hairline of rice paper, never a shadow or a
// glow; the page's words simply pass under it.
// Products and Science open one rounded ink panel under the stone: the five bottles lit on the
// ink, each on a pale pool of light, or the Science page's four parts, each painting on its own
// rice-paper leaf. Switching between them changes the panel's size, not the panel.
// Narrow windows: a clear bar with the mark and a "Menu" button; once scrolled, a small ink pill
// at the bottom centre, in thumb reach. Either opens an ink sheet that rises from the bottom.

const tightLocales = new Set(["jp", "cns", "hken"]);

export function NavStone({ overlay = false, solidAfter = 80 }: HeaderProps) {
  const copy = useCopy();
  const locale = useLocale();
  const dialogs = useHomeDialogs();
  const nav = useNav({ overlay, solidAfter });
  const { solid, panel, menuOpen, setMenuOpen, menuButton } = nav;
  const mode = solid ? "stone" : "bar";

  const root = useRef<HTMLElement>(null);
  const barRow = useRef<HTMLDivElement>(null);
  const stone = useRef<HTMLDivElement>(null);
  const stoneLinks = useRef<HTMLElement>(null);
  const frame = useRef<HTMLDivElement>(null);
  const lastPanel = useRef<NavPanelId | null>(null);
  const closeButton = useRef<HTMLButtonElement>(null);
  const [fold, setFold] = useState<Record<NavPanelId, boolean>>({
    products: false,
    science: false,
  });

  /** A caption the site keeps in two pieces ("Good science." + "Real people.") reads as one. */
  const say = (text: string) => {
    if ((copyKeys as Record<string, string>)[text]) return copy(text);
    const parts = text.split(/(?<=[.,])\s+/);
    return parts.map((part) => copy(part)).join(tightLocales.has(locale) ? "" : " ");
  };

  // The stone's own width comes from its links (and changes with the language): measured once
  // they are set, so the stylesheet can stand it at the column's right edge or at the centre and
  // glide between the two. Until then it stands at the column's edge by itself, still.
  useLayoutEffect(() => {
    const header = root.current;
    const links = stoneLinks.current;
    if (!header || !links) return;
    let frameId = 0;
    const measure = () => {
      header.style.setProperty("--nav-w", `${Math.ceil(links.offsetWidth)}px`);
      if (!header.dataset.placed) {
        frameId = requestAnimationFrame(() => {
          header.dataset.placed = "";
        });
      }
    };
    measure();
    const observer = new ResizeObserver(measure);
    observer.observe(links);
    return () => {
      observer.disconnect();
      cancelAnimationFrame(frameId);
    };
  }, []);

  // The panel hangs under the stone: at the column's right edge, flush with the stone, at the top
  // of the page; centred under it once it has moved to the centre. It is placed where the stone
  // comes to rest (not where it is mid-glide). Opening sets its place and size at once; going
  // from Products to Science while it is open moves and resizes the same panel.
  useLayoutEffect(() => {
    const box = frame.current;
    const previous = lastPanel.current;
    lastPanel.current = panel;
    if (!box || !panel) return;
    const section = box.querySelector<HTMLElement>(`[data-nav-panel="${panel}"]`);
    if (!section) return;
    if (previous && previous !== panel) box.dataset.moving = "";
    else delete box.dataset.moving;

    const place = () => {
      let width = section.offsetWidth;
      const height = section.offsetHeight;
      const view = document.documentElement.clientWidth;
      let left: number;
      const pill = stone.current;
      const row = barRow.current;
      if (!pill || !row) return;
      const style = getComputedStyle(pill);
      const read = (name: string) => parseFloat(style.getPropertyValue(name)) || 0;
      const base =
        (stoneLinks.current?.offsetWidth ?? 0) + read("--pad-start") + read("--pad-end") + 2;
      const top = read("--stone-top") + read("--stone-h") + 12;
      if (solid) {
        const pillWidth = base + read("--mark-room");
        // A panel nearly as wide as the stone takes its width exactly, so their edges line up
        // instead of missing by a few pixels.
        if (width < pillWidth) width = pillWidth;
        left = view / 2 - width / 2;
      } else {
        // Flush with the stone's right edge, never past the page column's left edge.
        const rowStyle = getComputedStyle(row);
        const start = row.getBoundingClientRect().left + parseFloat(rowStyle.paddingLeft);
        const end = pill.getBoundingClientRect().right;
        if (width < base) width = base;
        left = Math.max(end - width, start);
      }
      left = Math.max(12, Math.min(left, view - width - 12));
      box.style.setProperty("--x", `${Math.round(left)}px`);
      box.style.setProperty("--y", `${Math.round(top)}px`);
      box.style.setProperty("--w", `${width}px`);
      box.style.setProperty("--h", `${height}px`);
    };
    place();
    const observer = new ResizeObserver(place);
    observer.observe(section);
    window.addEventListener("resize", place);
    return () => {
      observer.disconnect();
      window.removeEventListener("resize", place);
    };
  }, [panel, solid]);

  // The sheet: focus goes to its first control as it opens.
  useEffect(() => {
    if (menuOpen) closeButton.current?.focus({ preventScroll: true });
  }, [menuOpen]);

  /** The sheet opens with its disclosures folded. */
  const openSheet = () => {
    if (!menuOpen) setFold({ products: false, science: false });
    setMenuOpen(!menuOpen);
  };

  const closeSheet = (returnFocus = true) => {
    if (returnFocus) menuButton.current?.focus({ preventScroll: true });
    setMenuOpen(false);
  };

  // Keyboard: Tab from an open drop-down's button goes into its panel, and Tab from the panel's
  // last link goes on to the control after that button (the panel sits later in the page).
  const onTriggerKey = (id: NavPanelId) => (event: KeyboardEvent<HTMLButtonElement>) => {
    if (event.key !== "Tab" || event.shiftKey || panel !== id) return;
    const first = frame.current?.querySelector<HTMLElement>(`[data-nav-panel="${id}"] a[href]`);
    if (!first) return;
    event.preventDefault();
    first.focus();
  };

  const onPanelKey = (id: NavPanelId) => (event: KeyboardEvent<HTMLElement>) => {
    if (event.key !== "Tab") return;
    const links = [...event.currentTarget.querySelectorAll<HTMLElement>("a[href]")];
    const trigger = document.querySelector<HTMLElement>(
      `#site-navigation [data-nav-trigger="${id}"]`,
    );
    if (!trigger) return;
    if (event.shiftKey && event.target === links[0]) {
      event.preventDefault();
      trigger.focus();
    } else if (!event.shiftKey && event.target === links[links.length - 1]) {
      const controls = [
        ...(trigger
          .closest("nav")
          ?.querySelectorAll<HTMLElement>("a[href], button:not([disabled]), select") ?? []),
      ];
      const next = controls[controls.indexOf(trigger) + 1];
      if (!next) return;
      event.preventDefault();
      next.focus();
    }
  };

  const openSupport = () => {
    nav.closePanel();
    if (menuOpen) closeSheet();
    dialogs.openSupport();
  };

  /** The stone's links. */
  const links = () => {
    const trigger = (id: NavPanelId, label: string) => (
      <button
        {...nav.triggerProps(id)}
        data-nav-trigger={id}
        className={styles.link}
        onKeyDown={onTriggerKey(id)}
      >
        <span className={styles.word}>{copy(label)}</span>
        <ChevronDown className={styles.chevron} size={16} strokeWidth={1.75} aria-hidden="true" />
      </button>
    );
    return (
      <>
        {trigger("products", "Products")}
        {trigger("science", "Science")}
        <Link href="/about" className={styles.link} onClick={() => nav.closePanel()}>
          <span className={styles.word}>{copy("About")}</span>
        </Link>
        <button type="button" className={styles.link} onClick={openSupport}>
          <span className={styles.word}>{copy("Support")}</span>
        </button>
        <span className={styles.divider} aria-hidden="true" />
        <div className={styles.utilities}>
          <HeaderUtilities />
        </div>
      </>
    );
  };

  const panelSection = (id: NavPanelId) => {
    // The panel's frame owns the pointer (it holds both contents); the contents take the rest.
    const { onPointerEnter, onPointerLeave, ...props } = nav.panelProps(id);
    void onPointerEnter;
    void onPointerLeave;
    return {
      ...props,
      "data-nav-panel": id,
      className: styles.section,
      onKeyDown: onPanelKey(id),
    };
  };
  const framePointer = nav.panelProps(panel ?? "products");

  return (
    <header
      ref={root}
      className={styles.root}
      data-mode={mode}
      data-menu={menuOpen ? "" : undefined}
      onBlur={nav.onHeaderBlur}
    >
      {/* Narrow windows, at the top: a clear bar, the mark and the menu's button. */}
      <div
        className={styles.bar}
        data-show={mode === "bar" ? "" : undefined}
        inert={mode !== "bar"}
      >
        <div ref={barRow} className={styles.barRow}>
          <NavLogo className={styles.barLogo} />
          <button
            ref={mode === "bar" ? menuButton : undefined}
            type="button"
            data-nav-menu-button=""
            className={styles.menuTop}
            aria-expanded={menuOpen}
            aria-controls="site-navigation-sheet"
            onClick={openSheet}
          >
            <span className={styles.menuGlyph} aria-hidden="true" />
            {copy("Menu")}
          </button>
        </div>
      </div>

      {/* The mark: ink on the paper at the top, white in the stone's left end once it has moved. */}
      <Link href="/" aria-label={copy("BiGH home")} className={styles.mark} data-nav-logo="">
        <span className={styles.markCrop}>
          <Image
            src="/images/brand/bigh-logo-black-green.png"
            alt=""
            width={1448}
            height={811}
            sizes="120px"
            loading="eager"
            className={`${styles.markImage} ${styles.markInk}`}
          />
          <Image
            src="/images/brand/bigh-logo-white.png"
            alt=""
            width={1448}
            height={811}
            sizes="120px"
            loading="eager"
            className={`${styles.markImage} ${styles.markLight}`}
          />
        </span>
      </Link>

      {/* The ink stone: at the column's edge at the top, at the centre once the page moves. */}
      <div ref={stone} className={styles.stone}>
        <nav
          ref={stoneLinks}
          id="site-navigation"
          aria-label={copy("Main navigation")}
          className={styles.stoneLinks}
        >
          {links()}
        </nav>
      </div>

      {/* The drop-down: one ink panel, two contents. */}
      <div
        ref={frame}
        className={styles.frame}
        data-open={panel ? "" : undefined}
        onPointerEnter={framePointer.onPointerEnter}
        onPointerLeave={framePointer.onPointerLeave}
      >
        <div className={styles.frameInk}>
          <section {...panelSection("products")} aria-label={copy("Products")}>
            <ul className={styles.shelf}>
              {navProducts.map((product, i) => (
                <li key={product.slug} style={{ "--i": i } as CSSProperties}>
                  <Link
                    href={product.href}
                    className={styles.product}
                    onClick={() => nav.closePanel()}
                  >
                    <span className={styles.stand}>
                      <span className={styles.pool} aria-hidden="true" />
                      <Image
                        src={product.bottle.src}
                        alt=""
                        width={product.bottle.width}
                        height={product.bottle.height}
                        sizes="150px"
                        className={styles.bottle}
                      />
                    </span>
                    <span className={styles.name}>{copy(product.name)}</span>
                    <span className={styles.focus}>{copy(product.focus)}</span>
                  </Link>
                </li>
              ))}
            </ul>
            <div className={styles.panelFoot}>
              <Link
                href={navProductsIntro.allLink}
                className={styles.more}
                onClick={() => nav.closePanel()}
              >
                <span>{copy(navProductsIntro.title)}</span>
                <ArrowRight size={18} aria-hidden="true" />
              </Link>
            </div>
          </section>

          <section {...panelSection("science")} aria-label={copy("Science")}>
            <ul className={styles.parts}>
              {navScience.map((part, i) => (
                <li key={part.href} style={{ "--i": i } as CSSProperties}>
                  <Link href={part.href} className={styles.part} onClick={() => nav.closePanel()}>
                    <Leaf image={part.image} />
                    <span className={styles.partText}>
                      <span className={styles.partLabel}>
                        <span className={styles.word}>{copy(part.label)}</span>
                        <ArrowRight size={18} aria-hidden="true" />
                      </span>
                      <span className={styles.caption}>{say(part.caption)}</span>
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
            <div className={styles.panelFoot}>
              <Link
                href={navScienceIntro.href}
                className={styles.more}
                onClick={() => nav.closePanel()}
              >
                <span>{copy(navScienceIntro.link)}</span>
                <ArrowRight size={18} aria-hidden="true" />
              </Link>
            </div>
          </section>
        </div>
      </div>

      {/* Narrow windows, once scrolled: the menu in thumb reach. */}
      <button
        ref={mode === "stone" ? menuButton : undefined}
        type="button"
        data-nav-menu-button=""
        className={styles.pebble}
        data-show={mode === "stone" ? "" : undefined}
        inert={mode !== "stone"}
        aria-expanded={menuOpen}
        aria-controls="site-navigation-sheet"
        onClick={openSheet}
      >
        <span className={styles.menuGlyph} aria-hidden="true" />
        {copy("Menu")}
      </button>

      {/* The ink sheet, rising from the bottom. */}
      <div className={styles.sheetLayer} data-open={menuOpen ? "" : undefined}>
        <div className={styles.wash} aria-hidden="true" onClick={() => closeSheet(false)} />
        <div
          id="site-navigation-sheet"
          className={styles.sheet}
          data-nav-sheet=""
          role="dialog"
          aria-modal="true"
          aria-label={copy("Main navigation")}
          inert={!menuOpen}
          data-lenis-prevent={menuOpen ? "" : undefined}
        >
          <div className={styles.sheetTop}>
            <NavLogo light className={styles.sheetLogo} />
            <button
              ref={closeButton}
              type="button"
              className={styles.close}
              onClick={() => closeSheet()}
            >
              <X size={20} strokeWidth={1.75} aria-hidden="true" />
              {copy("Close menu")}
            </button>
          </div>

          <nav aria-label={copy("Main navigation")} className={styles.sheetLinks}>
            <div className={styles.group}>
              <button
                type="button"
                className={styles.big}
                data-nav-sheet-toggle="products"
                aria-expanded={fold.products}
                aria-controls="sheet-products"
                onClick={() => setFold((value) => ({ ...value, products: !value.products }))}
              >
                {copy("Products")}
                <ChevronDown
                  className={styles.chevron}
                  size={26}
                  strokeWidth={1.5}
                  aria-hidden="true"
                />
              </button>
              <div
                id="sheet-products"
                className={styles.fold}
                data-open={fold.products ? "" : undefined}
              >
                <div className={styles.foldInner} inert={!fold.products}>
                  <ul className={styles.row} data-lenis-prevent="">
                    {navProducts.map((product) => (
                      <li key={product.slug}>
                        <Link
                          href={product.href}
                          className={styles.rowProduct}
                          onClick={() => closeSheet(false)}
                        >
                          <span className={styles.rowStand}>
                            <span className={styles.pool} aria-hidden="true" />
                            <Image
                              src={product.bottle.src}
                              alt=""
                              width={product.bottle.width}
                              height={product.bottle.height}
                              sizes="128px"
                              className={styles.bottle}
                            />
                          </span>
                          <span className={styles.name}>{copy(product.name)}</span>
                          <span className={styles.focus}>{copy(product.focus)}</span>
                        </Link>
                      </li>
                    ))}
                  </ul>
                  <Link
                    href={navProductsIntro.allLink}
                    className={styles.more}
                    onClick={() => closeSheet(false)}
                  >
                    <span>{copy(navProductsIntro.title)}</span>
                    <ArrowRight size={18} aria-hidden="true" />
                  </Link>
                </div>
              </div>
            </div>

            <div className={styles.group}>
              <button
                type="button"
                className={styles.big}
                data-nav-sheet-toggle="science"
                aria-expanded={fold.science}
                aria-controls="sheet-science"
                onClick={() => setFold((value) => ({ ...value, science: !value.science }))}
              >
                {copy("Science")}
                <ChevronDown
                  className={styles.chevron}
                  size={26}
                  strokeWidth={1.5}
                  aria-hidden="true"
                />
              </button>
              <div
                id="sheet-science"
                className={styles.fold}
                data-open={fold.science ? "" : undefined}
              >
                <div className={styles.foldInner} inert={!fold.science}>
                  <ul className={styles.sheetParts}>
                    {navScience.map((part) => (
                      <li key={part.href}>
                        <Link
                          href={part.href}
                          className={styles.sheetPart}
                          onClick={() => closeSheet(false)}
                        >
                          <Leaf image={part.image} small />
                          <span className={styles.partText}>
                            <span className={styles.partLabel}>{copy(part.label)}</span>
                            <span className={styles.caption}>{say(part.caption)}</span>
                          </span>
                        </Link>
                      </li>
                    ))}
                  </ul>
                  <Link
                    href={navScienceIntro.href}
                    className={styles.more}
                    onClick={() => closeSheet(false)}
                  >
                    <span>{copy(navScienceIntro.link)}</span>
                    <ArrowRight size={18} aria-hidden="true" />
                  </Link>
                </div>
              </div>
            </div>

            <Link href="/about" className={styles.big} onClick={() => closeSheet(false)}>
              {copy("About")}
            </Link>
            <button type="button" className={styles.big} onClick={openSupport}>
              {copy("Support")}
            </button>
          </nav>

          <div className={styles.sheetFoot}>
            <div className={styles.utilities}>
              <HeaderUtilities />
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

/** A painting on its own rice-paper leaf (ink needs paper under it on the dark panel); Dr. Liu's
 *  real photograph on the leaf as on a paper mat, never multiplied. */
function Leaf({
  image,
  small = false,
}: {
  image: (typeof navScience)[number]["image"];
  small?: boolean;
}) {
  const name = image.src.split("/").pop()?.split(".")[0];
  return (
    <span
      className={`${styles.plate} ${image.photo ? styles.photo : ""} ${small ? styles.small : ""}`}
      data-plate={name}
      aria-hidden="true"
    >
      <span className={styles.platePicture}>
        <span className={styles.platePrint}>
          <Image
            src={image.src}
            alt=""
            fill
            sizes={small ? "80px" : "160px"}
            className={styles.plateImage}
          />
        </span>
      </span>
    </span>
  );
}
