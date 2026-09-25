"use client";

import Image from "next/image";
import gsap from "gsap";
import { ArrowDown, ArrowUpRight, MessageCircleQuestion } from "lucide-react";
import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { useCopy } from "@/i18n/use-copy";
import { articles, images, intro, type ScienceDesignProps } from "./science-data";
import styles from "./science-chat.module.css";
import { useReducedMotion } from "./use-reduced-motion";

// Chat: tap a question and BiGH answers in plain words, like a message thread. The answers are the
// explainer's approved lines; nothing is attributed to a named scientist.

// Hide the new answer before the browser paints it, so it can arrive line by line without a flash.
const useBeforePaint = typeof window === "undefined" ? useEffect : useLayoutEffect;
function Picture({ index }: { index: number }) {
  const copy = useCopy();
  if (index === 1) {
    return (
      <div className={`${styles.picture} ${styles.kitchenTest}`}>
        <figure>
          <Image {...images.appleBrown} alt="" sizes="160px" />
          <figcaption>{copy("Air only")}</figcaption>
        </figure>
        <figure>
          <Image {...images.appleFresh} alt="" sizes="160px" />
          <figcaption>{copy("With lemon juice")}</figcaption>
        </figure>
      </div>
    );
  }
  const image = index === 0 ? images.bulbOn : images.wood;
  return (
    <div className={`${styles.picture} ${index === 0 ? styles.night : styles.sage}`}>
      <Image {...image} alt="" sizes="220px" />
    </div>
  );
}

export function ScienceChat({ onOpenArticle, onAsk }: ScienceDesignProps) {
  const copy = useCopy();
  const reducedMotion = useReducedMotion();
  const [selected, setSelected] = useState(0);
  const [asked, setAsked] = useState(false);
  const thread = useRef<HTMLDivElement>(null);
  const phone = useRef<HTMLDivElement>(null);
  const article = articles[selected];

  // A new question: it slides in from the right, BiGH "types", then the answer arrives line by line.
  // The first answer is already on screen when the page loads.
  useBeforePaint(() => {
    const element = thread.current;
    if (!element || !asked || reducedMotion) return;
    const context = gsap.context(() => {
      const timeline = gsap
        .timeline()
        .from("[data-asked]", { x: 36, autoAlpha: 0, duration: 0.4, ease: "power3.out" })
        .set("[data-typing]", { display: "flex" })
        .from("[data-typing]", { autoAlpha: 0, y: 8, duration: 0.2 })
        .to("[data-typing]", { autoAlpha: 0, duration: 0.15 }, "+=0.85")
        .set("[data-typing]", { display: "none" })
        .from("[data-reply]", {
          y: 14,
          autoAlpha: 0,
          duration: 0.45,
          ease: "power3.out",
          stagger: 0.3,
        });
      // Failsafe: a throttled tab can stall requestAnimationFrame; show the whole answer anyway.
      const settle = window.setTimeout(() => timeline.progress(1), 4500);
      return () => window.clearTimeout(settle);
    }, element);
    return () => context.revert();
  }, [selected, asked, reducedMotion]);

  function ask(index: number) {
    setSelected(index);
    setAsked(true);
    // On phones the thread sits below the questions; bring it into view.
    const box = phone.current?.getBoundingClientRect();
    if (box && box.bottom > window.innerHeight) {
      phone.current?.scrollIntoView({ block: "end", behavior: reducedMotion ? "auto" : "smooth" });
    }
  }

  return (
    <div className={styles.chat}>
      <header className={styles.head}>
        <h2 id="science-title" className={styles.heading}>
          {copy(intro.title)}
        </h2>
        <p>{copy(intro.text)}</p>
      </header>

      <div className={styles.questions}>
        <p className={styles.label} id="science-questions">
          {copy("Tap a question.")}
        </p>
        <div className={styles.list} role="group" aria-labelledby="science-questions">
          {articles.map((item, index) => (
            <button
              type="button"
              key={item.id}
              aria-pressed={selected === index}
              aria-controls="science-thread"
              onClick={() => ask(index)}
            >
              <MessageCircleQuestion size={24} strokeWidth={1.6} aria-hidden="true" />
              <span>{copy(item.title)}</span>
            </button>
          ))}
        </div>
      </div>

      <div ref={phone} className={styles.phone}>
        <div className={styles.bar}>
          <span className={styles.avatar}>
            <Image
              src="/images/brand/bigh-logo-black-green.png"
              alt=""
              width={1448}
              height={811}
              sizes="80px"
            />
          </span>
          <span className={styles.who}>
            <strong>BiGH</strong>
            <small>{copy("Answers in plain words")}</small>
          </span>
        </div>
        <div
          ref={thread}
          key={selected}
          id="science-thread"
          className={styles.thread}
          aria-live="polite"
        >
          <p className={`${styles.bubble} ${styles.mine}`} data-asked>
            {copy(article.title)}
          </p>
          <div className={styles.typing} data-typing aria-hidden="true">
            <span />
            <span />
            <span />
          </div>
          <p className={`${styles.bubble} ${styles.theirs}`} data-reply>
            {copy(article.answer[0])}
          </p>
          <div
            className={`${styles.bubble} ${styles.theirs} ${styles.photo}`}
            data-reply
            aria-hidden="true"
          >
            <Picture index={selected} />
          </div>
          <p className={`${styles.bubble} ${styles.theirs}`} data-reply>
            {copy(article.answer[1])}
          </p>
          <div className={styles.links} data-reply>
            <button type="button" className={styles.read} onClick={() => onOpenArticle(selected)}>
              {copy("Read a quick explainer")} <ArrowUpRight size={18} aria-hidden="true" />
            </button>
            <button type="button" className={styles.ask} onClick={onAsk}>
              {copy("Discover Ask BiGH Science")}
            </button>
          </div>
        </div>
      </div>

      <div className={styles.foot}>
        <a href="#research" className={styles.explore}>
          {copy(intro.button)} <ArrowDown size={19} aria-hidden="true" />
        </a>
      </div>
    </div>
  );
}
