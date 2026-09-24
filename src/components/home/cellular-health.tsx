import Image from "next/image";
import { ArrowRight, PersonStanding } from "lucide-react";
import styles from "./cellular-health.module.css";

function CellSymbol() {
  return (
    <svg viewBox="0 0 64 64" fill="none" aria-hidden="true">
      <path
        d="M54 31c2 16-11 25-24 24C15 55 7 45 9 31 10 15 20 7 34 9c13 1 21 9 20 22Z"
        fill="#e0ebf2"
        stroke="#6e8da9"
        strokeWidth="1.4"
      />
      <circle cx="26" cy="28" r="9" fill="#a3bdd0" />
      <circle cx="24" cy="26" r="3" fill="#6e8da9" />
      <rect
        x="35"
        y="37"
        width="15"
        height="8"
        rx="4"
        transform="rotate(-30 35 37)"
        fill="#c8945d"
      />
      <rect
        x="16"
        y="40"
        width="11"
        height="6"
        rx="3"
        transform="rotate(20 16 40)"
        fill="#c8945d"
      />
    </svg>
  );
}

function MitochondrionSymbol() {
  return (
    <svg viewBox="0 0 64 64" fill="none" aria-hidden="true">
      <g transform="rotate(-25 32 32)">
        <rect
          x="8"
          y="18"
          width="48"
          height="28"
          rx="14"
          fill="#f0e0cc"
          stroke="#ab7745"
          strokeWidth="1.4"
        />
        <path
          d="M17 31c0-8 8-8 8-2v8c0 5 7 5 7 0V27c0-5 7-5 7 0v10c0 5 8 5 8-6"
          stroke="#b17b48"
          strokeWidth="2"
          strokeLinecap="round"
        />
      </g>
    </svg>
  );
}

export function CellularHealth({ onExplore }: { onExplore: () => void }) {
  return (
    <section
      id="cellular-health"
      aria-labelledby="cellular-health-title"
      className={styles.section}
    >
      <div className={styles.layout}>
        <header className={styles.heading}>
          <p className={styles.eyebrow}>01 / WHY CELLULAR HEALTH MATTERS</p>
          <h2 id="cellular-health-title" className={styles.title}>
            Tiny power plants.
            <span>A big part of your health.</span>
          </h2>
        </header>

        <figure className={styles.visual}>
          <ol
            className={styles.scalePath}
            aria-label="From your body to your cells to mitochondria"
          >
            <li>
              <PersonStanding aria-hidden="true" strokeWidth={1.15} />
              <span>Your body</span>
            </li>
            <li>
              <CellSymbol />
              <span>Your cells</span>
            </li>
            <li className={styles.currentScale}>
              <MitochondrionSymbol />
              <span>Mitochondria</span>
            </li>
          </ol>
          <div className={styles.imageWrap}>
            <Image
              src="/images/science/mitochondrion-cutaway-v1.png"
              alt="A cutaway of a mitochondrion, with a blue outer membrane surrounding warm amber folds inside."
              fill
              sizes="(max-width: 760px) 100vw, (max-width: 1100px) 48vw, 600px"
              className={styles.image}
            />
          </div>
          <figcaption className={styles.caption}>
            <span>A closer look inside a mitochondrion</span>
            <span>Simplified illustration · Not to scale</span>
          </figcaption>
        </figure>

        <div className={styles.explanation}>
          <p>
            Inside many of your body’s cells are <strong>mitochondria</strong>—tiny power plants
            that turn energy from food into a form your cells can use.
          </p>
          <p>
            That energy helps your <strong>brain think</strong>, your <strong>heart beat</strong>,
            and your <strong>muscles move</strong>.
          </p>
        </div>

        <div className={styles.ending}>
          <p>It’s one reason good health starts with your cells.</p>
          <button type="button" onClick={onExplore} className={styles.explore}>
            Explore cellular health <ArrowRight size={19} aria-hidden="true" />
          </button>
        </div>
      </div>
    </section>
  );
}
