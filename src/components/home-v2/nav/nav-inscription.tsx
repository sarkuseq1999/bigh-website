"use client";

import Image from "next/image";
import { ArrowRight, ChevronDown, X } from "lucide-react";
import { useLocale } from "next-intl";
import { useEffect, useRef, useState, type CSSProperties, type ReactNode } from "react";
import { HeaderUtilities } from "@/components/home/header-utilities";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
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

// The menu bar, "Inscription" (Mo's pick, October 5, 2026). A Chinese hanging scroll carries its title
// centred above the painting; this bar does the same over the crane. The BiGH mark stands in the
// middle, large, with two links on each side of it (Products, Science | About, Support) set as one
// balanced line; the language at the far left, Log in and Sign up at the far right. Over the
// opening painting the bar is clear; once the page moves on it settles a little smaller on rice
// paper, and its edge is a real painted brush line instead of a hairline, laid by the reader's
// scroll.
// Products and Science let down a sheet of rice paper from under the bar, the way a hanging scroll
// unrolls: revealed top to bottom, its leading edge torn rice paper, over a faint ink wash on the
// page. What is on it is centred under the bar. Both are showrooms, two pages of one book: the
// names large at the left, each a link, and the picture of the one pointed at (or reached by
// keyboard) standing large at the right, in the same place on both (round 4: the five products and
// their bottles; round 5: the Science page's four parts, Dr. Liu's print and three ink paintings
// set at one weight). Moving from one drop-down to the other keeps the scroll down and changes only
// what is written on it. On a narrow window: "Menu", the mark, the
// language; the menu is a full-height scroll let down the same way.
// Each drop-down's links follow its button in the page, so Tab goes from the button into them.
// Where you are is written in ink (round 6): the current page's word carries a short painted brush
// stroke under it (inscription/current-stroke.webp, cut by reference/nav/make_current_stroke.py from
// a real painted stroke), laid from the left as the page opens; pointing at a word draws only a
// fine line. On the homepage, which has no link of its own, the stroke follows the reader: while a
// part of the page that belongs to Products or Science is being read, that word carries it.

/** Which page the bar is on (its link is marked as the current page); the homepage marks none. */
export type NavCurrent = "home" | "products" | "science" | "about";

/** The homepage's parts that belong to each drop-down (the ids of their sections). */
export type NavFollow = Partial<Record<NavPanelId, readonly string[]>>;

export type NavInscriptionProps = {
  /** The page the bar is on. */
  current?: NavCurrent;
  /** On the homepage: while one of these parts is being read, its drop-down's word carries the
   *  painted stroke (it paints in as the part arrives and lifts as it leaves). */
  follow?: NavFollow;
  /** Start clear over the page's opening picture; it turns to paper once the page scrolls. */
  overlay?: boolean;
  /** Ink over the opening: "light" = dark ink on a pale opening, "dark" = white ink on a dark one. */
  tone?: "light" | "dark";
  /** Scroll distance (px) after which the bar settles on paper. */
  solidAfter?: number;
};

export function NavInscription({
  current = "home",
  follow,
  overlay = false,
  tone = "light",
  solidAfter = 80,
}: NavInscriptionProps) {
  const copy = useCopy();
  const locale = useLocale();
  const dialogs = useHomeDialogs();
  const nav = useNav({ overlay, solidAfter });
  const { solid, panel, closePanel, menuOpen, setMenuOpen, menuButton } = nav;
  const cjk = locale === "jp" || locale === "cns" || locale === "hken";

  // The painted stroke: under the current page's word ("here"), or on the homepage under the word
  // whose part of the page is being read ("reading"). A page with a link of its own never follows
  // the reader, so there is only ever one stroke.
  const reading = useReading(current === "home" ? follow : undefined);
  const inked = (id: NavCurrent) =>
    current === id ? "here" : current === "home" && reading === id ? "reading" : undefined;

  // The drop-downs' pictures load once the visitor reaches for the bar (the pointer on it, focus
  // in it, a tap on Menu), so the bottles are there as the scroll unrolls, without loading them on
  // every visit to the page.
  const [warm, setWarm] = useState(false);
  const loading = warm ? "eager" : "lazy";
  const reach = () => setWarm(true);

  // The scroll keeps showing the last drop-down while it rolls back up. Moving straight across from
  // one drop-down to the other (the scroll stays down) is a swap: the new writing is laid over the
  // old instead of settling onto a fresh scroll.
  const [shown, setShown] = useState<NavPanelId>("products");
  const [swap, setSwap] = useState(false);
  const [lastPanel, setLastPanel] = useState<NavPanelId | null>(panel);
  if (panel !== lastPanel) {
    setLastPanel(panel);
    if (panel) {
      setSwap(lastPanel !== null);
      if (panel !== shown) setShown(panel);
    }
  }

  // Both drop-downs are showrooms (rounds 4 and 5), two pages of one book: the names large at the
  // left, and the picture of the one pointed at (or reached by keyboard) standing large at the
  // right; the first shown first.
  const products = useShowroom(panel !== null);
  const science = useShowroom(panel !== null);
  const product = navProducts[products.pick];
  const part = navScience[science.pick];

  // The narrow window's menu: one of its two parts (Products, Science) is unfolded at a time.
  // On a tablet (700px and wider) it opens with Products unfolded: the five fit in one row.
  const [fold, setFold] = useState<NavPanelId | null>(null);
  const [wasOpen, setWasOpen] = useState(menuOpen);
  if (menuOpen !== wasOpen) {
    setWasOpen(menuOpen);
    if (!menuOpen) setFold(null);
  }

  // The scroll is as long as the taller of the two drop-downs, so it never changes length when
  // you move from one to the other. And the two showrooms share one page layout: their names
  // columns are as wide, and their rows as tall, as the larger of the two, so the names start on
  // the same edge and line, the pictures stand in the same place, and the links under them share
  // a line. Measured from what is written (each name, link and stand at its own size), never from
  // the stretched columns, so it follows the window both ways.
  const productsInner = useRef<HTMLDivElement>(null);
  const scienceInner = useRef<HTMLDivElement>(null);
  const [layout, setLayout] = useState({ panel: 0, row: 0, names: 0 });
  useEffect(() => {
    const inners = [productsInner.current, scienceInner.current].filter(
      (node): node is HTMLDivElement => Boolean(node),
    );
    const columns = inners.flatMap((inner) => [
      ...inner.querySelectorAll<HTMLElement>("[data-showroom]"),
    ]);
    const pieces = columns.flatMap((column) => [
      ...column.querySelectorAll<HTMLElement>(":scope > *, :scope li > a"),
    ]);
    const outer = (node: Element) => {
      const style = getComputedStyle(node);
      return (
        node.getBoundingClientRect().height +
        parseFloat(style.marginTop) +
        parseFloat(style.marginBottom)
      );
    };
    const measure = () => {
      const row = Math.max(
        0,
        ...columns.map((column) => [...column.children].reduce((sum, c) => sum + outer(c), 0)),
      );
      const names = Math.max(
        0,
        ...columns
          .filter((column) => column.dataset.showroom === "names")
          .flatMap((column) => [...column.querySelectorAll<HTMLElement>(":scope > a, li > a")])
          .map((link) => Math.ceil(link.getBoundingClientRect().width)),
      );
      const panel = Math.max(0, ...inners.map((node) => node.offsetHeight));
      setLayout((now) =>
        now.panel === Math.ceil(panel) && now.row === Math.ceil(row) && now.names === names
          ? now
          : { panel: Math.ceil(panel), row: Math.ceil(row), names },
      );
    };
    measure();
    const observer = new ResizeObserver(measure);
    [...inners, ...pieces].forEach((node) => observer.observe(node));
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
      menuButton.current?.focus({ preventScroll: true });
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
      data-overlay={overlay ? "" : undefined}
      data-unrolled={panel ? "" : undefined}
      data-swap={swap ? "" : undefined}
      data-menu={menuOpen ? "" : undefined}
      style={
        {
          "--insc-panel-h": `${layout.panel}px`,
          "--insc-row-h": `${layout.row}px`,
          "--insc-names-w": `${layout.names}px`,
        } as CSSProperties
      }
      onBlur={nav.onHeaderBlur}
      onFocus={reach}
    >
      <span className={styles.ground} aria-hidden="true" />
      <span className={styles.rule} aria-hidden="true" />

      <nav
        id="site-navigation"
        aria-label={copy("Main navigation")}
        className={styles.bar}
        onPointerEnter={reach}
      >
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
            onPointerDown={reach}
            onClick={() => {
              if (!menuOpen) {
                setFold(window.matchMedia("(min-width: 700px)").matches ? "products" : null);
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
              data-current={current === "products" ? "" : undefined}
              data-ink={inked("products")}
            >
              <span className={styles.word}>
                {copy("Products")}
                <Ink />
              </span>
              <ChevronDown className={styles.chevron} size={14} aria-hidden="true" />
            </button>
            <div
              {...nav.panelProps("products")}
              className={styles.panel}
              data-nav-panel="products"
              data-shown={shown === "products" ? "" : undefined}
            >
              <div ref={productsInner} className={styles.panelInner}>
                <Showroom
                  room={products}
                  items={navProducts.map((item) => ({
                    href: item.href,
                    name: copy(item.name),
                    line: copy(item.focus),
                  }))}
                  more={{ href: navProductsIntro.allLink, text: copy(navProductsIntro.title) }}
                  link={{
                    href: product.href,
                    text: copy("Discover {name}", { name: copy(product.name) }),
                  }}
                  onGo={() => closePanel()}
                >
                  <Image
                    key={`pool-${products.pick}`}
                    className={styles.stagePool}
                    src="/images/home-v2/ink/pool.webp"
                    alt=""
                    width={900}
                    height={482}
                    sizes="240px"
                    loading={loading}
                  />
                  <Image
                    className={styles.stageContact}
                    src="/images/home-v2/ink/pool-foot.webp"
                    alt=""
                    width={600}
                    height={170}
                    sizes="200px"
                    loading={loading}
                  />
                  {navProducts.map((item, i) => (
                    <Image
                      key={item.slug}
                      className={styles.big}
                      data-shown={products.pick === i ? "" : undefined}
                      src={item.bottle.src}
                      alt=""
                      width={1230}
                      height={1278}
                      sizes="(min-width: 1652px) 366px, (min-width: 1218px) 22.2vw, 270px"
                      loading={loading}
                    />
                  ))}
                </Showroom>
              </div>
            </div>
            <button
              {...nav.triggerProps("science")}
              className={styles.link}
              data-nav-trigger="science"
              data-current={current === "science" ? "" : undefined}
              data-ink={inked("science")}
            >
              <span className={styles.word}>
                {copy("Science")}
                <Ink />
              </span>
              <ChevronDown className={styles.chevron} size={14} aria-hidden="true" />
            </button>
            <div
              {...nav.panelProps("science")}
              className={styles.panel}
              data-nav-panel="science"
              data-shown={shown === "science" ? "" : undefined}
            >
              <div ref={scienceInner} className={styles.panelInner}>
                <Showroom
                  room={science}
                  items={navScience.map((item) => ({
                    href: item.href,
                    name: copy(item.label),
                    line: caption(item.caption),
                  }))}
                  more={{ href: navScienceIntro.href, text: copy(navScienceIntro.link) }}
                  link={{ href: part.href, text: copy(part.link) }}
                  onGo={() => closePanel()}
                >
                  {navScience.map((item, i) =>
                    item.image.plate === "print" ? (
                      <span
                        key={item.href}
                        className={styles.plate}
                        data-plate="print"
                        data-shown={science.pick === i ? "" : undefined}
                      >
                        <Image
                          className={styles.photo}
                          src={item.image.src}
                          alt=""
                          width={item.image.width}
                          height={item.image.height}
                          sizes="(min-width: 1652px) 192px, (min-width: 1218px) 11.6vw, 140px"
                          loading={loading}
                        />
                      </span>
                    ) : (
                      <Image
                        key={item.href}
                        className={styles.plate}
                        data-plate={item.image.plate}
                        data-shown={science.pick === i ? "" : undefined}
                        src={item.image.src}
                        alt=""
                        width={item.image.width}
                        height={item.image.height}
                        sizes="(min-width: 1652px) 470px, (min-width: 1218px) 28.4vw, 350px"
                        loading={loading}
                      />
                    ),
                  )}
                </Showroom>
              </div>
            </div>
          </div>
        </div>

        <NavLogo className={styles.mark} light={clear && tone === "dark"} />

        <div className={styles.right}>
          <div className={styles.links}>
            <Link
              href="/about"
              className={styles.link}
              aria-current={current === "about" ? "page" : undefined}
              data-ink={inked("about")}
            >
              <span className={styles.word}>
                {copy("About")}
                <Ink />
              </span>
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
            here={current === "products"}
            open={fold === "products"}
            onToggle={() => setFold(fold === "products" ? null : "products")}
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
                      <Bottle
                        src={product.bottle.src}
                        sizes="(max-width: 699px) 34vw, 150px"
                        loading={loading}
                      />
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
            here={current === "science"}
            open={fold === "science"}
            onToggle={() => setFold(fold === "science" ? null : "science")}
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
          <Link
            href="/about"
            className={styles.sheetLink}
            aria-current={current === "about" ? "page" : undefined}
            onClick={() => setMenuOpen(false)}
          >
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

/** The painted stroke under a word (shown by its link's `data-ink`: "here" for the current page,
 *  "reading" for the homepage's part being read). */
function Ink() {
  return <span className={styles.ink} data-nav-ink="" aria-hidden="true" />;
}

/** Which drop-down's part of the homepage is being read: the part that crosses a thin band a
 *  little above the window's middle (where the eye rests while reading down), or none. */
function useReading(follow: NavFollow | undefined) {
  const [reading, setReading] = useState<NavPanelId | null>(null);
  useEffect(() => {
    if (!follow) return;
    const parts = (Object.entries(follow) as [NavPanelId, readonly string[]][]).flatMap(
      ([id, sections]) =>
        sections.flatMap((section) => {
          const node = document.getElementById(section);
          return node ? [{ id, node }] : [];
        }),
    );
    if (!parts.length) return;
    const inBand = new Set<Element>();
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) inBand.add(entry.target);
          else inBand.delete(entry.target);
        }
        // At a seam two parts can share the band for a moment: the one further down the page is
        // the one arriving.
        const hit = parts
          .filter((part) => inBand.has(part.node))
          .sort((a, b) =>
            a.node.compareDocumentPosition(b.node) & Node.DOCUMENT_POSITION_FOLLOWING ? 1 : -1,
          )[0];
        setReading(hit ? hit.id : null);
      },
      { rootMargin: "-40% 0px -58% 0px" },
    );
    parts.forEach((part) => observer.observe(part.node));
    return () => {
      observer.disconnect();
      setReading(null);
    };
  }, [follow]);
  return reading;
}

/** Which of a showroom's names is shown: the one a pointer rests on (about a tenth of a second,
 *  so passing over other names on the way across to the link under the picture changes nothing)
 *  or the keyboard reaches. `moved` is set once the visitor has changed it, so from then on the
 *  picture only cross-fades (it settled in with the scroll). Once the scroll has rolled back up
 *  it is the first again for the next time. */
function useShowroom(open: boolean) {
  const [state, setState] = useState({ pick: 0, moved: false });
  const timer = useRef<number | undefined>(undefined);
  const show = (i: number) => setState((now) => (now.pick === i ? now : { pick: i, moved: true }));
  const pointAt = (i: number) => {
    window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => show(i), 110);
  };
  const pointAway = () => window.clearTimeout(timer.current);
  useEffect(() => {
    if (open) return;
    window.clearTimeout(timer.current);
    const reset = window.setTimeout(() => setState({ pick: 0, moved: false }), 420);
    return () => window.clearTimeout(reset);
  }, [open]);
  return { ...state, show, pointAt, pointAway };
}

/** One drop-down as a showroom: the names large at the left, each a link with its line under it,
 *  and the link to all of them; at the right the shown one's picture (the children, stacked) with
 *  its own link under it, on the same line. */
function Showroom({
  room,
  items,
  more,
  link,
  onGo,
  children,
}: {
  room: ReturnType<typeof useShowroom>;
  items: { href: string; name: string; line: string }[];
  more: { href: string; text: string };
  link: { href: string; text: string };
  onGo: () => void;
  children: ReactNode;
}) {
  return (
    <div className={styles.showroom}>
      <div className={styles.names} data-showroom="names">
        <ul className={styles.nameList}>
          {items.map((item, i) => (
            <li key={item.href} style={{ "--i": i } as CSSProperties}>
              <Link
                href={item.href}
                className={styles.nameLink}
                data-shown={room.pick === i ? "" : undefined}
                onPointerEnter={(event) => {
                  if (event.pointerType === "mouse") room.pointAt(i);
                }}
                onPointerLeave={room.pointAway}
                onFocus={(event) => {
                  if (event.currentTarget.matches(":focus-visible")) room.show(i);
                }}
                onClick={onGo}
              >
                <span className={styles.nameText}>{item.name}</span>
                <span className={styles.nameFocus}>{item.line}</span>
              </Link>
            </li>
          ))}
        </ul>
        <Link href={more.href} className={styles.more} onClick={onGo}>
          {more.text}
          <ArrowRight size={18} aria-hidden="true" />
        </Link>
      </div>
      <div className={styles.stage} data-showroom="stage" data-moved={room.moved ? "" : undefined}>
        <Link
          href={link.href}
          className={styles.stageStand}
          tabIndex={-1}
          aria-hidden="true"
          onClick={onGo}
        >
          {children}
        </Link>
        <Link href={link.href} className={styles.more} onClick={onGo}>
          {link.text}
          <ArrowRight size={18} aria-hidden="true" />
        </Link>
      </div>
    </div>
  );
}

/** A product photograph standing on its pale ink pool. */
function Bottle({
  src,
  sizes,
  loading,
}: {
  src: string;
  sizes: string;
  loading: "eager" | "lazy";
}) {
  return (
    <span className={styles.stand}>
      <Image
        className={styles.pool}
        src="/images/home-v2/ink/pool.webp"
        alt=""
        width={900}
        height={482}
        sizes="120px"
        loading={loading}
      />
      <Image
        className={styles.contact}
        src="/images/home-v2/ink/pool-foot.webp"
        alt=""
        width={600}
        height={170}
        sizes="100px"
        loading={loading}
      />
      <Image
        className={styles.bottle}
        src={src}
        alt=""
        width={1230}
        height={1278}
        sizes={sizes}
        loading={loading}
      />
    </span>
  );
}

/** One of the menu's two folding parts: its word, and under it what it holds. `here`: the page the
 *  menu is open on is one of its parts (its word keeps the ink underline). */
function SheetPart({
  id,
  label,
  here,
  open,
  onToggle,
  children,
}: {
  id: NavPanelId;
  label: string;
  here: boolean;
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
        data-current={here ? "" : undefined}
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
