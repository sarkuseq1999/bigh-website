"use client";

import Image from "next/image";
import { ArrowDown, ArrowUpRight, Check, RotateCcw } from "lucide-react";
import { useRef, useState } from "react";
import { useCopy } from "@/i18n/use-copy";
import { articles, images, intro, type ScienceDesignProps } from "./science-data";
import styles from "./science-quiz.module.css";

// Myth or fact: a three-card game. Each card states a common belief; tapping Myth or Fact flips it
// to the honest answer (the explainer's approved lines) and a link to that explainer.
type Answer = "myth" | "fact";

const cards = [
  {
    statement: "Mitochondria are found in most of your cells.",
    truth: "fact",
    image: images.bulbOn,
    tone: "gold",
    explain: [articles[0].answer[0]],
  },
  {
    statement: "More antioxidants always mean better health.",
    truth: "myth",
    image: images.lemon,
    tone: "lime",
    explain: [articles[1].answer[1], articles[1].answer[0]],
  },
  {
    statement: "Healthy aging comes down to one thing.",
    truth: "myth",
    image: images.wood,
    tone: "sky",
    explain: [articles[2].answer[0]],
  },
] as const;

const unanswered = (): (Answer | null)[] => cards.map(() => null);

export function ScienceQuiz({ onOpenArticle }: ScienceDesignProps) {
  const copy = useCopy();
  const [answers, setAnswers] = useState(unanswered);
  const [revealAll, setRevealAll] = useState(false);
  const verdicts = useRef<(HTMLParagraphElement | null)[]>([]);

  const answered = answers.filter(Boolean).length;
  const score = answers.filter((answer, index) => answer === cards[index].truth).length;
  const done = answered === cards.length;

  function answer(index: number, choice: Answer) {
    setAnswers((current) => current.map((value, i) => (i === index ? choice : value)));
    // Keyboard and screen-reader users land on the answer once the card has turned.
    window.setTimeout(() => verdicts.current[index]?.focus({ preventScroll: true }), 420);
  }

  function reset() {
    setAnswers(unanswered());
    setRevealAll(false);
  }

  return (
    <div className={styles.quiz}>
      <header className={styles.head}>
        <h2 id="science-title" className={styles.heading}>
          {copy(intro.title)}
        </h2>
        <p>{copy(intro.text)}</p>
        <p className={styles.prompt}>{copy("Myth or fact? Tap your answer to flip the card.")}</p>
      </header>

      <ol className={styles.deck}>
        {cards.map((card, index) => {
          const given = answers[index];
          const flipped = given !== null || revealAll;
          const correct = given === card.truth;
          const article = articles[index];
          return (
            <li key={card.statement} className={styles.slot} data-tone={card.tone}>
              <div className={styles.card} data-flipped={flipped}>
                <div className={styles.front} inert={flipped}>
                  <div className={styles.art} aria-hidden="true">
                    <Image {...card.image} alt="" sizes="(max-width: 899px) 40vw, 12vw" />
                  </div>
                  <p className={styles.statement} id={`quiz-statement-${index}`}>
                    {copy(card.statement)}
                  </p>
                  <div
                    className={styles.choices}
                    role="group"
                    aria-labelledby={`quiz-statement-${index}`}
                  >
                    <button type="button" onClick={() => answer(index, "myth")}>
                      {copy("Myth")}
                    </button>
                    <button type="button" onClick={() => answer(index, "fact")}>
                      {copy("Fact")}
                    </button>
                  </div>
                </div>

                <div className={styles.back} inert={!flipped}>
                  <p
                    className={styles.verdict}
                    tabIndex={-1}
                    ref={(node) => {
                      verdicts.current[index] = node;
                    }}
                  >
                    <span className={styles.stamp}>
                      {copy(card.truth === "fact" ? "Fact." : "Myth.")}
                    </span>
                    {given && (
                      <span className={styles.result} data-correct={correct}>
                        {correct ? (
                          <Check size={17} aria-hidden="true" />
                        ) : (
                          <RotateCcw size={16} aria-hidden="true" />
                        )}
                        {copy(correct ? "You got it." : "Not quite.")}
                      </span>
                    )}
                  </p>
                  {card.explain.map((line) => (
                    <p key={line} className={styles.explain}>
                      {copy(line)}
                    </p>
                  ))}
                  <button
                    type="button"
                    className={styles.more}
                    onClick={() => onOpenArticle(index)}
                  >
                    <span>{copy(article.title)}</span>
                    <ArrowUpRight size={20} aria-hidden="true" />
                  </button>
                </div>
              </div>
            </li>
          );
        })}
      </ol>

      <div className={styles.tally}>
        <p aria-live="polite">
          {done
            ? copy("You got {score} of 3 right.", { score })
            : copy("Answer all three to see your score.")}
        </p>
        <div className={styles.actions}>
          {done || revealAll ? (
            <button type="button" className={styles.again} onClick={reset}>
              <RotateCcw size={18} aria-hidden="true" /> {copy("Play again")}
            </button>
          ) : (
            <button type="button" className={styles.again} onClick={() => setRevealAll(true)}>
              {copy("Show all answers")}
            </button>
          )}
          <a href="#research" className={styles.explore}>
            {copy(intro.button)} <ArrowDown size={19} aria-hidden="true" />
          </a>
        </div>
      </div>
    </div>
  );
}
