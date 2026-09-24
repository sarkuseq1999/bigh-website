"use client";

import { useCopy } from "@/i18n/use-copy";

import Image from "next/image";
import { useEffect, useId, useRef, useState, type ReactNode } from "react";
import {
  ArrowDown,
  ArrowUpRight,
  ChevronDown,
  Globe2,
  Menu,
  MessageCircle,
  Plus,
  X,
} from "lucide-react";
import styles from "./homepage.module.css";
import { DeepSpaceHero } from "./hero-comparison";
import { CellularHealthComparison } from "./cellular-health-comparison";
import { ProductsSection } from "./products-section";
import { CustomerStories } from "./customer-stories";
import { HeaderUtilities } from "./header-utilities";
import { useLocale } from "next-intl";

const products = [
  {
    name: "NuriCell",
    image: "nuricell",
    category: "Our flagship formula",
    tone: "blue",
    description:
      "The starting point for the BiGH range and our focus on cellular health and mental energy.",
    ingredients: "Acetyl-L-carnitine, creatine, alpha-lipoic acid, and choline.",
    detail:
      "NuriCell brings four ingredients together in one capsule formula. Explore the ingredients and the research behind the thinking, with a clear distinction between ingredient studies and evidence for the finished product.",
  },
  {
    name: "Green Bee Propolis",
    image: "green-bee-propolis",
    category: "Brazilian green propolis",
    tone: "sage",
    description: "A formula centered on green bee propolis extract.",
    ingredients: "Green bee propolis extract.",
    detail:
      "Propolis is a resinous material collected by bees. Its composition varies with its botanical source. Research on one standardized extract does not automatically apply to every propolis product.",
  },
  {
    name: "Advanced OPC Formula",
    image: "advanced-opc",
    category: "Botanical & nutrient blend",
    tone: "rose",
    description: "Plant extracts paired with vitamins and other nutrients.",
    ingredients:
      "Includes grape seed and pine bark extracts, vitamins C and E, and other nutrients.",
    detail:
      "A multi-ingredient formula. Each ingredient has its own research background, and the amounts and preparation used in a study matter when interpreting its findings.",
  },
  {
    name: "Turmerific",
    image: "turmerific",
    category: "Curcumin formula",
    tone: "apricot",
    description: "A curcumin formula featuring Longvida® extract.",
    ingredients: "Longvida® Optimized Curcumin Extract.",
    detail:
      "Curcumin is a compound found in turmeric. Different curcumin preparations are not interchangeable. Research findings depend on the preparation, dose, people studied, and outcome measured.",
  },
  {
    name: "Nature Calm",
    image: "nature-calm",
    category: "Multi-ingredient formula",
    tone: "lavender",
    description: "A combination of vitamins, nutrients, and plant compounds.",
    ingredients: "Includes CoQ10, theanine, phosphatidylserine, vitamins, and other nutrients.",
    detail:
      "Nature Calm combines several ingredients in one formula. Its name is not a sleep or treatment claim. The full current label and product-specific evidence will guide the final product information.",
  },
];

const scienceSteps = [
  {
    title: "Energy starts small.",
    label: "Cellular energy",
    text: "Inside most of your cells are mitochondria. They turn energy from food into a form your cells can use. Think of them as tiny energy converters.",
    note: "A small part of a cell. A big part of how it works.",
    source: "https://www.genome.gov/genetics-glossary/Mitochondria",
    sourceLabel: "National Human Genome Research Institute",
    illustration: "energy",
  },
  {
    title: "Balance matters.",
    label: "Cellular defenses",
    text: "Normal cell activity produces reactive molecules. Your body has defenses that help keep them in balance. Too much oxidative stress can damage cells.",
    note: "More antioxidants do not automatically mean better health.",
    source: "https://www.nccih.nih.gov/health/antioxidant-supplements-what-you-need-to-know",
    sourceLabel: "National Center for Complementary and Integrative Health",
    illustration: "balance",
  },
  {
    title: "Aging is a bigger story.",
    label: "Healthy aging",
    text: "As we age, many processes in our cells change. Mitochondrial function is one part of that story. No single ingredient explains all of healthy aging.",
    note: "Understand the whole picture, one idea at a time.",
    source: "https://pubmed.ncbi.nlm.nih.gov/36599349/",
    sourceLabel: "Hallmarks of Aging, Cell, 2023",
    illustration: "aging",
  },
];

type ModalContent = { eyebrow: string; title: string; body: ReactNode };

function Brand({ footer = false, light = false }: { footer?: boolean; light?: boolean }) {
  const copy = useCopy();
  return (
    <a
      href="#home"
      aria-label={copy("BiGH home")}
      className={`${styles.brand} ${footer ? styles.brandFooter : ""}`}
    >
      <span className={styles.logoCrop}>
        <Image
          src={
            light ? "/images/brand/bigh-logo-white.png" : "/images/brand/bigh-logo-black-green.png"
          }
          alt={copy("BiGH")}
          width={1448}
          height={811}
          sizes={footer ? "160px" : "(max-width: 760px) 108px, 116px"}
          loading={footer ? "lazy" : "eager"}
          className={styles.brandImage}
        />
      </span>
    </a>
  );
}

function CellDiagram({ variant }: { variant: string }) {
  const id = useId().replaceAll(":", "");
  return (
    <svg className={styles.cellDiagram} viewBox="0 0 500 500" aria-hidden="true">
      <defs>
        <radialGradient id={`${id}-cell`} cx="35%" cy="30%">
          <stop offset="0" stopColor="#fff" />
          <stop offset=".6" stopColor="#cbd8ff" />
          <stop offset="1" stopColor="#7498ef" />
        </radialGradient>
        <linearGradient id={`${id}-mito`} x1="0" x2="1" y1="0" y2="1">
          <stop stopColor="#fcf7ab" />
          <stop offset=".5" stopColor="#e4eb62" />
          <stop offset="1" stopColor="#b5c637" />
        </linearGradient>
      </defs>
      <g className={styles.diagramOrbit} fill="none" stroke="currentColor" opacity=".16">
        <circle cx="250" cy="250" r="224" />
        <circle cx="250" cy="250" r="184" />
        <path d="M15 250h470M250 15v470" />
      </g>
      {variant === "aging" ? (
        <g>
          <path d="M250 118L130 330h240Z" fill="none" stroke="#7796e5" strokeWidth="2" />
          {[
            [250, 118],
            [130, 330],
            [370, 330],
          ].map(([x, y], i) => (
            <g key={i}>
              <circle
                cx={x}
                cy={y}
                r="76"
                fill={`url(#${id}-cell)`}
                stroke="#fff"
                strokeWidth="3"
              />
              <circle cx={x - 8} cy={y - 6} r="31" fill="#456bc6" opacity=".6" />
              <circle cx={x - 15} cy={y - 15} r="13" fill="#b9caff" />
            </g>
          ))}
          <circle cx="250" cy="250" r="27" fill="#edf07f" />
        </g>
      ) : (
        <g>
          <ellipse
            className={styles.cellMembrane}
            cx="250"
            cy="250"
            rx="180"
            ry="184"
            fill={`url(#${id}-cell)`}
            stroke="#f7f9ff"
            strokeWidth="7"
          />
          <ellipse cx="210" cy="219" rx="70" ry="65" fill="#526fcc" opacity=".65" />
          <ellipse cx="200" cy="205" rx="32" ry="31" fill="#b8cafa" />
          <g className={`${styles.mitoGroup} ${variant === "balance" ? styles.mitoZoom : ""}`}>
            <rect
              x="275"
              y="280"
              width="115"
              height="61"
              rx="30"
              transform="rotate(-32 332 310)"
              fill={`url(#${id}-mito)`}
              stroke="#fafad3"
              strokeWidth="3"
            />
            <path
              d="M290 323q-5-15 6-16t10-12 11-10 10-7 12-9 13-8 12 9"
              fill="none"
              stroke="#6f8331"
              strokeWidth="4"
              strokeLinecap="round"
            />
          </g>
          <g fill="#edf394" stroke="#fff" strokeWidth="2">
            <ellipse cx="147" cy="300" rx="26" ry="13" transform="rotate(40 147 300)" />
            <ellipse cx="309" cy="159" rx="29" ry="14" transform="rotate(-20 309 159)" />
          </g>
          <g fill="#6089d9">
            {[
              [153, 166],
              [264, 340],
              [318, 225],
              [218, 357],
              [365, 260],
              [134, 238],
              [262, 139],
              [207, 285],
            ].map(([x, y], i) => (
              <circle key={i} cx={x} cy={y} r="4" />
            ))}
          </g>
        </g>
      )}
    </svg>
  );
}

const researchItems = [
  {
    year: "2002",
    type: "Research",
    category: "Animal study · Ingredients",
    title: "Mitochondrial nutrients and the aging cell",
    journal: "PNAS",
    text: "Liu and colleagues studied acetyl-L-carnitine and R-alpha-lipoic acid in old rats. This is part of the scientific background behind our interest in cellular health. It is not a clinical trial of NuriCell or evidence of a benefit in people.",
    url: "https://pubmed.ncbi.nlm.nih.gov/11854529/",
  },
  {
    year: "2023",
    type: "Research",
    category: "Review · Biology of aging",
    title: "Healthy aging has many moving parts",
    journal: "Cell",
    text: "The Hallmarks of Aging review describes interconnected biological processes, including mitochondrial dysfunction. It provides a framework for learning about aging, not proof that a supplement slows it.",
    url: "https://pubmed.ncbi.nlm.nih.gov/36599349/",
  },
  {
    year: "GUIDE",
    type: "Education",
    category: "Science explained",
    title: "What are mitochondria?",
    journal: "NHGRI",
    text: "A short introduction from the National Human Genome Research Institute. Mitochondria are structures in cells that help turn energy from food into energy that cells can use.",
    url: "https://www.genome.gov/genetics-glossary/Mitochondria",
  },
  {
    year: "GUIDE",
    type: "Education",
    category: "Evidence overview",
    title: "Antioxidants: what the evidence says",
    journal: "NCCIH",
    text: "The National Center for Complementary and Integrative Health explains what is known about antioxidant supplements and where the evidence is uncertain. The role of a nutrient in the body does not automatically establish a benefit from supplementation.",
    url: "https://www.nccih.nih.gov/health/antioxidant-supplements-what-you-need-to-know",
  },
];

export function Homepage() {
  const copy = useCopy();
  const locale = useLocale();
  const [menuOpen, setMenuOpen] = useState(false);
  const [scienceOpen, setScienceOpen] = useState(false);
  const [researchFilter, setResearchFilter] = useState("All");
  const [modal, setModal] = useState<ModalContent | null>(null);
  const dialog = useRef<HTMLDialogElement>(null);
  const header = useRef<HTMLElement>(null);

  useEffect(() => {
    const closeMenus = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setMenuOpen(false);
        setScienceOpen(false);
      }
    };
    const outside = (event: PointerEvent) => {
      if (!header.current?.contains(event.target as Node)) {
        setMenuOpen(false);
        setScienceOpen(false);
      }
    };
    window.addEventListener("keydown", closeMenus);
    window.addEventListener("pointerdown", outside);
    return () => {
      window.removeEventListener("keydown", closeMenus);
      window.removeEventListener("pointerdown", outside);
    };
  }, []);

  useEffect(() => {
    if (!modal) return;
    dialog.current?.showModal();
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = previous;
    };
  }, [modal]);

  const closeModal = () => {
    dialog.current?.close();
    setModal(null);
  };
  const openModal = (content: ModalContent) => {
    setMenuOpen(false);
    setScienceOpen(false);
    setModal(content);
  };
  const closeNav = () => {
    setMenuOpen(false);
    setScienceOpen(false);
  };

  const openProduct = (index: number) => {
    const product = products[index];
    openModal({
      eyebrow: copy(product.category),
      title: product.name,
      body: (
        <>
          <div className={`${styles.modalProduct} ${styles[product.tone]}`}>
            <Image
              src={`/images/products/${product.image}.png`}
              alt={copy("{name} bottle", { name: product.name })}
              width={260}
              height={280}
            />
          </div>
          <p>{copy(product.detail)}</p>
          <h3>{copy("Inside the formula")}</h3>
          <p>{copy(product.ingredients)}</p>
          <div className={styles.draftNote}>
            <strong>{copy("Product preview")}</strong>
            <p>
              {copy(
                "These details use the available product materials. Current labels, directions, availability, and pricing still need confirmation. Ordering is not open in this preview.",
              )}
            </p>
          </div>
          {index === 0 && (
            <a
              className={styles.textLink}
              href="https://pubmed.ncbi.nlm.nih.gov/11854529/"
              target="_blank"
              rel="noreferrer"
            >
              {copy("Explore the ingredient research")} <ArrowUpRight size={19} />
            </a>
          )}
        </>
      ),
    });
  };

  const openScientist = () =>
    openModal({
      eyebrow: copy("Meet the scientists"),
      title: copy("Dr. Jiankang Liu"),
      body: (
        <>
          <p>
            {copy(
              "Dr. Liu studies mitochondrial function, oxidative stress, and the biology of aging. His scientific background is central to BiGH’s approach to cellular health.",
            )}
          </p>
          <h3>{copy("A career in cell science")}</h3>
          <p>
            {copy(
              "He earned his doctorate at Okayama University in Japan and completed postdoctoral work in biochemistry and molecular biology at the University of California, Berkeley.",
            )}
          </p>
          <p>
            {copy(
              "In 2025, his university announced his election to the European Academy of Sciences and Arts.",
            )}
          </p>
          <h3>{copy("Read the research in context")}</h3>
          <a
            className={styles.textLink}
            href="https://www.uhrs.edu.cn/info/1050/1805.htm"
            target="_blank"
            rel="noreferrer"
          >
            {copy("University biography (Chinese)")} <ArrowUpRight size={18} />
          </a>
          <a
            className={styles.textLink}
            href="https://pubmed.ncbi.nlm.nih.gov/11854529/"
            target="_blank"
            rel="noreferrer"
          >
            {copy("Read the 2002 study")} <ArrowUpRight size={18} />
          </a>
        </>
      ),
    });

  const openAsk = () =>
    openModal({
      eyebrow: copy("A planned customer benefit"),
      title: copy("Ask BiGH Science"),
      body: (
        <>
          <p>
            {copy(
              "Good questions deserve clear explanations. We are developing a way for BiGH customers to explore broader health and science questions with input from participating scientists.",
            )}
          </p>
          <ol className={styles.modalList}>
            <li>
              {copy(
                "Start with a question about topics such as cellular health, nutrition, or healthy aging.",
              )}
            </li>
            <li>
              {copy(
                "BiGH explains what the research says and involves scientific advisors when deeper input is needed.",
              )}
            </li>
            <li>
              {copy(
                "Each answer identifies its contributors and where the science remains uncertain.",
              )}
            </li>
          </ol>
          <div className={styles.draftNote}>
            <strong>{copy("In development")}</strong>
            <p>
              {copy(
                "The question service is not accepting submissions yet. Eligibility and response arrangements are still being agreed. This will be general science education, not personal medical care.",
              )}
            </p>
          </div>
        </>
      ),
    });

  const openSupport = () =>
    openModal({
      eyebrow: copy("Here to help"),
      title: copy("BiGH support"),
      body: (
        <>
          <p>
            {copy(
              "This is a preview of the new BiGH website. You can explore the range and science, but purchases and account services are not connected yet.",
            )}
          </p>
          <div className={styles.faq}>
            <details>
              <summary>{copy("Can I place an order here?")}</summary>
              <p>
                {copy(
                  "Not yet. Ordering will be available when the new store is connected. No payments are taken in this preview.",
                )}
              </p>
            </details>
            <details>
              <summary>{copy("Where are shipping and return details?")}</summary>
              <p>
                {copy(
                  "Market-specific shipping and return information will be added before the store opens.",
                )}
              </p>
            </details>
            <details>
              <summary>{copy("Can I ask a health or science question?")}</summary>
              <p>
                {copy(
                  "Ask BiGH Science is in development. It will explain research in everyday language. For personal treatment or medication questions, speak with your healthcare professional.",
                )}
              </p>
            </details>
            <details>
              <summary>{copy("Will other languages be available?")}</summary>
              <p>
                {copy(
                  "Use the language selector at the top of the page to switch between English, Simplified Chinese, Korean, Vietnamese, and Japanese.",
                )}
              </p>
            </details>
          </div>
        </>
      ),
    });

  const openArticle = (index: number) => {
    const item = scienceSteps[index];
    openModal({
      eyebrow: copy("Health, explained simply"),
      title: copy(item.title),
      body: (
        <>
          <CellDiagram variant={item.illustration} />
          <p>{copy(item.text)}</p>
          <p>{copy(item.note)}</p>
          <p>
            {copy(
              "Understanding a biological process is a starting point. It does not tell us whether a particular supplement will change that process or improve health.",
            )}
          </p>
          <a className={styles.textLink} href={item.source} target="_blank" rel="noreferrer">
            {copy("Read the source")} <ArrowUpRight size={18} />
          </a>
          <p className={styles.small}>{copy(item.sourceLabel)}</p>
        </>
      ),
    });
  };

  return (
    <div className={styles.site} data-locale={locale} data-hero-theme="deep-space">
      <a href="#main-content" className={styles.skipLink}>
        {copy("Skip to content")}
      </a>
      <header ref={header} className={`${styles.header} ${styles.previewHeader}`}>
        <div className={styles.masthead}>
          <span className={styles.brandMeaning}>{copy("Be in Good Health.")}</span>
          <Brand light />
          <HeaderUtilities />
          <button
            className={styles.mobileMenu}
            aria-label={copy(menuOpen ? "Close menu" : "Open menu")}
            aria-expanded={menuOpen}
            aria-controls="main-navigation"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            {menuOpen ? <X /> : <Menu />}
          </button>
        </div>
        <nav
          id="main-navigation"
          aria-label={copy("Main navigation")}
          className={`${styles.navigation} ${menuOpen ? styles.navOpen : ""}`}
        >
          <a href="#home" onClick={closeNav}>
            {copy("Home")}
          </a>
          <a href="#products" onClick={closeNav}>
            {copy("Products")}
          </a>
          <button
            onClick={() => setScienceOpen(!scienceOpen)}
            aria-expanded={scienceOpen}
            aria-controls="science-navigation"
          >
            {copy("Science")} <ChevronDown size={15} />
          </button>
          <a href="#about" onClick={closeNav}>
            {copy("About")}
          </a>
          <button onClick={openSupport}>{copy("Support")}</button>
          {scienceOpen && (
            <div id="science-navigation" className={styles.dropdown}>
              <div>
                <span className={styles.eyebrow}>{copy("THE SCIENCE OF FEELING INFORMED")}</span>
                <p>{copy("Start with curiosity.")}</p>
              </div>
              <div className={styles.dropdownLinks}>
                <a href="#scientists" onClick={closeNav}>
                  {copy("Our scientists")} <ArrowUpRight size={18} />
                </a>
                <a href="#cellular-health" onClick={closeNav}>
                  {copy("Cellular health, explained")} <ArrowUpRight size={18} />
                </a>
                <a href="#research" onClick={closeNav}>
                  {copy("Explore the research")} <ArrowUpRight size={18} />
                </a>
                <button onClick={openAsk}>
                  {copy("Ask BiGH Science")} <ArrowUpRight size={18} />
                </button>
              </div>
            </div>
          )}
        </nav>
      </header>
      <main id="main-content">
        <DeepSpaceHero onDiscover={() => openProduct(0)} />

        <section id="scientists" className={`${styles.section} ${styles.scientists}`}>
          <div className={styles.sectionHeading}>
            <p className={styles.eyebrow}>{copy("02 / OUR SCIENTIFIC ROOTS")}</p>
            <h2>
              {copy("Good science.")}
              <br />
              {copy("Real people.")}
            </h2>
            <p>
              {copy("Meet the minds behind our curiosity")}
              <br className={styles.desktopBreak} /> {copy("about cellular health.")}
            </p>
          </div>
          <div className={styles.scientistFeature}>
            <button
              className={styles.scientistPortrait}
              onClick={openScientist}
              aria-label={copy("Meet Dr. Jiankang Liu")}
            >
              <Image
                src="/images/jiankang-liu.jpg"
                alt={copy("Dr. Jiankang Liu")}
                fill
                sizes="(max-width: 760px) 88vw, 38vw"
              />
              <span className={styles.portraitCaption}>
                <span>
                  {copy("Dr. Jiankang Liu")}
                  <small>{copy("Mitochondrial science & aging")}</small>
                </span>
                <span className={styles.roundArrow}>
                  <ArrowUpRight size={24} />
                </span>
              </span>
            </button>
            <div className={styles.scientistCopy}>
              <p className={styles.eyebrow}>{copy("A LIFETIME OF ASKING BETTER QUESTIONS")}</p>
              <h3>{copy("What happens inside our cells shapes the way we understand health.")}</h3>
              <p>
                {copy(
                  "Dr. Jiankang Liu’s work explores mitochondria, oxidative stress, and aging. These connections help shape BiGH’s focus on cellular health and mental energy.",
                )}
              </p>
              <button onClick={openScientist} className={styles.textLink}>
                {copy("Get to know Dr. Liu")} <ArrowUpRight size={18} />
              </button>
              <div className={styles.iris}>
                <span className={styles.initials} aria-hidden="true">
                  {copy("IW")}
                </span>
                <div>
                  <h4>{copy("Dr. Iris Wang")}</h4>
                  <p>{copy("Part of BiGH’s scientific and formulation roots.")}</p>
                </div>
              </div>
            </div>
          </div>
          <div className={styles.askStrip}>
            <MessageCircle size={29} strokeWidth={1.3} />
            <div>
              <h3>{copy("Good questions deserve clear answers.")}</h3>
              <p>{copy("Introducing Ask BiGH Science, a planned customer benefit.")}</p>
            </div>
            <button onClick={openAsk} className={styles.textLink}>
              {copy("Discover Ask BiGH Science")} <ArrowUpRight size={18} />
            </button>
          </div>
        </section>

        <CellularHealthComparison variant="original" onExplore={() => openArticle(0)} />

        <ProductsSection products={products} onOpenProduct={openProduct} design="lineup" />

        <CustomerStories onOpenProduct={openProduct} />

        <section id="research" className={`${styles.section} ${styles.researchSection}`}>
          <div className={styles.researchIntro}>
            <div>
              <p className={styles.eyebrow}>{copy("04 / FOLLOW THE EVIDENCE")}</p>
              <h2>
                {copy("Curiosity,")}
                <br />
                {copy("with references.")}
              </h2>
            </div>
            <p>
              {copy(
                "Science is most useful when you can understand it. Explore the ideas behind our approach, and see what each source actually tells us.",
              )}
            </p>
          </div>
          <div className={styles.researchFilters} aria-label={copy("Filter research")}>
            {["All", "Research", "Education"].map((filter) => (
              <button
                key={filter}
                aria-pressed={researchFilter === filter}
                onClick={() => setResearchFilter(filter)}
              >
                {filter}
                <span>{filter === "All" ? "04" : "02"}</span>
              </button>
            ))}
          </div>
          <div className={styles.studyTableHeader} aria-hidden="true">
            <span>{copy("YEAR / TYPE")}</span>
            <span>{copy("EXPLORE THE SCIENCE")}</span>
            <span>{copy("SOURCE")}</span>
            <span />
          </div>
          <div className={styles.studyList}>
            {researchItems
              .filter((item) => researchFilter === "All" || researchFilter === item.type)
              .map((item) => (
                <details key={item.title} className={styles.study}>
                  <summary>
                    <span className={styles.studyYear}>{copy(item.year)}</span>
                    <span className={styles.studyTitle}>
                      <small>{copy(item.category)}</small>
                      <span>{copy(item.title)}</span>
                    </span>
                    <span className={styles.studyJournal}>{item.journal}</span>
                    <Plus className={styles.studyPlus} size={23} />
                  </summary>
                  <div className={styles.studyBody}>
                    <p>{copy(item.text)}</p>
                    <a href={item.url} target="_blank" rel="noreferrer" className={styles.textLink}>
                      {copy("Read original source")} <ArrowUpRight size={18} />
                    </a>
                  </div>
                </details>
              ))}
          </div>
          <p className={styles.researchNote}>
            {copy(
              "Ingredient research and general science do not establish the effects of a finished BiGH product.",
            )}
          </p>
        </section>

        <section id="about" className={styles.aboutSection}>
          <div className={styles.aboutTop}>
            <p className={styles.eyebrow}>{copy("05 / BE IN GOOD HEALTH")}</p>
            <h2>
              {copy("Our purpose is simple.")}
              <br />
              {copy("Help you live fully.")}
            </h2>
          </div>
          <div className={styles.aboutBody}>
            <div className={styles.aboutGraphic} aria-hidden="true">
              <span className={`${styles.logoCrop} ${styles.aboutLogo}`}>
                <Image
                  src="/images/brand/bigh-logo-white.png"
                  alt=""
                  width={1448}
                  height={811}
                  sizes="144px"
                  className={styles.brandImage}
                />
              </span>
              <div className={styles.aboutRing} />
              <p>
                {copy("Small beginnings.")}
                <br />
                {copy("Bigger possibilities.")}
              </p>
            </div>
            <div>
              <p className={styles.serifLead}>
                {copy("We believe a fuller life starts with understanding what supports it.")}
              </p>
              <p>
                {copy(
                  "Our mission is to support cellular health and mental energy. We bring scientific curiosity to our products, and clear explanations to the people who use them.",
                )}
              </p>
              <p>
                {copy(
                  "From the first question to the details of a formula, we want you to feel informed.",
                )}
              </p>
              <a className={styles.textLink} href="#standards">
                {copy("What matters to us")} <ArrowDown size={18} />
              </a>
            </div>
          </div>
          <div id="standards" className={styles.standardsGrid}>
            {[
              {
                title: copy("Know what’s inside."),
                text: copy(
                  "Clear ingredient information and a thoughtful explanation of each formula.",
                ),
              },
              {
                title: copy("Ask how it’s made."),
                text: copy("Specific, documented information about sourcing and manufacturing."),
              },
              {
                title: copy("Keep asking questions."),
                text: copy(
                  "Research in context, honest answers, and room for what we’re still learning.",
                ),
              },
            ].map((item, index) => (
              <article key={item.title}>
                <span>0{index + 1}</span>
                <h3>{copy(item.title)}</h3>
                <p>{copy(item.text)}</p>
              </article>
            ))}
          </div>
        </section>

        <section id="learn" className={`${styles.section} ${styles.learnSection}`}>
          <div className={styles.learnHeading}>
            <div>
              <p className={styles.eyebrow}>{copy("06 / A LITTLE MORE UNDERSTANDING")}</p>
              <h2>{copy("Stay curious.")}</h2>
            </div>
            <p>{copy("Simple science. Useful perspectives.")}</p>
          </div>
          <div className={styles.learnGrid}>
            {scienceSteps.map((item, index) => (
              <button
                key={item.label}
                className={styles.learnCard}
                onClick={() => openArticle(index)}
              >
                <div className={`${styles.learnArt} ${styles[`learnArt${index}`]}`}>
                  <CellDiagram variant={item.illustration} />
                  <span className={styles.readTag}>
                    {copy("A QUICK READ")} <ArrowUpRight size={16} />
                  </span>
                </div>
                <p className={styles.eyebrow}>{copy(item.label)}</p>
                <h3>
                  {copy(
                    [
                      "The tiny structures doing big things.",
                      "Cellular balance, without the jargon.",
                      "Aging is more than one thing.",
                    ][index],
                  )}
                </h3>
              </button>
            ))}
          </div>
        </section>
      </main>
      <footer className={styles.footer}>
        <div className={styles.footerTop}>
          <p>{copy("BE IN GOOD HEALTH.")}</p>
          <h2>{copy("Stay sharp. Live fully.")}</h2>
          <a href="#products" className={styles.primaryButton}>
            {copy("Explore BiGH")} <ArrowUpRight size={20} />
          </a>
        </div>
        <div className={styles.footerNavigation}>
          <div className={styles.footerBrand}>
            <Brand footer />
            <p>
              {copy("Cellular health.")}
              <br />
              {copy("Mental energy.")}
              <br />
              {copy("Everyday possibilities.")}
            </p>
          </div>
          <div>
            <h3>{copy("Products")}</h3>
            {products.map((product, index) => (
              <button key={product.name} onClick={() => openProduct(index)}>
                {product.name}
              </button>
            ))}
          </div>
          <div>
            <h3>{copy("Science")}</h3>
            <a href="#scientists">{copy("Our scientists")}</a>
            <a href="#cellular-health">{copy("Cellular health")}</a>
            <a href="#research">{copy("Research library")}</a>
            <button onClick={openAsk}>{copy("Ask BiGH Science")}</button>
          </div>
          <div>
            <h3>{copy("Here for you")}</h3>
            <a href="#about">{copy("About BiGH")}</a>
            <button onClick={openSupport}>{copy("Support & FAQs")}</button>
            <a href="#learn">{copy("Health, explained")}</a>
            <button onClick={openSupport}>
              {copy("Language help")} <Globe2 size={16} />
            </button>
          </div>
        </div>
        <div className={styles.footerBottom}>
          <span>
            © {new Date().getFullYear()} {copy("BiGH. Be in Good Health.")}
          </span>
          <span>{copy("Homepage design preview")}</span>
          <a href="#home">{copy("Back to top ↑")}</a>
        </div>
        <p className={styles.footerNote}>
          {copy(
            "Educational content is for general information. Product details and packaging are subject to confirmation. Purchases and question submissions are not available in this preview. Lifestyle imagery is illustrative.",
          )}
        </p>
      </footer>
      <dialog
        ref={dialog}
        className={styles.dialog}
        aria-labelledby="dialog-title"
        onCancel={closeModal}
        onClose={() => setModal(null)}
        onClick={(event) => {
          if (event.target === event.currentTarget) {
            const box = event.currentTarget.getBoundingClientRect();
            if (
              event.clientX < box.left ||
              event.clientX > box.right ||
              event.clientY < box.top ||
              event.clientY > box.bottom
            )
              closeModal();
          }
        }}
      >
        {modal && (
          <>
            <div className={styles.dialogHeader}>
              <span className={styles.eyebrow}>{modal.eyebrow}</span>
              <button
                className={styles.closeButton}
                onClick={closeModal}
                aria-label={copy("Close details")}
                autoFocus
              >
                <X size={24} />
              </button>
            </div>
            <h2 id="dialog-title">{modal.title}</h2>
            <div className={styles.dialogBody}>{modal.body}</div>
          </>
        )}
      </dialog>
    </div>
  );
}
