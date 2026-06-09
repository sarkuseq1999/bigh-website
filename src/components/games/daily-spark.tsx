"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Delete } from "lucide-react";

const WORDS = [
  "SPARK", "BRAIN", "POWER", "FOCUS", "SMART", "CRISP", "ALERT", "SHINE",
  "LIGHT", "BRISK", "QUICK", "SHARP", "CLEAR", "SWIFT", "BLOOM", "PULSE",
  "BLAZE", "NERVE", "SENSE", "PRIME", "GUIDE", "BUILD", "TRUST", "VITAL",
  "DREAM", "GRACE", "CHARM", "MIGHT", "HONOR", "NOBLE", "FIELD", "RIVER",
  "OCEAN", "CLOUD", "STORM", "SPACE", "TRACE", "STILL", "AGILE", "ARISE",
] as const;

const KEYBOARD_ROWS: string[][] = [
  ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
  ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
  ["ENTER", "Z", "X", "C", "V", "B", "N", "M", "BACK"],
];

const MAX_GUESSES = 6;
type Eval = "correct" | "present" | "absent";

function getTodayIndex(): number {
  const start = new Date(2026, 0, 1);
  start.setHours(0, 0, 0, 0);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const days = Math.floor((today.getTime() - start.getTime()) / 86400000);
  return ((days % WORDS.length) + WORDS.length) % WORDS.length;
}

function getTodayKey(): string {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

function getYesterdayKey(): string {
  const d = new Date();
  d.setDate(d.getDate() - 1);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

function evaluate(guess: string, target: string): Eval[] {
  const result: Eval[] = Array(5).fill("absent") as Eval[];
  const remaining = target.split("");
  for (let i = 0; i < 5; i++) {
    if (guess[i] === target[i]) {
      result[i] = "correct";
      remaining[i] = "";
    }
  }
  for (let i = 0; i < 5; i++) {
    if (result[i] === "correct") continue;
    const idx = remaining.indexOf(guess[i]);
    if (idx !== -1) {
      result[i] = "present";
      remaining[idx] = "";
    }
  }
  return result;
}

function msUntilMidnight(): number {
  const now = new Date();
  const tomorrow = new Date(now);
  tomorrow.setDate(now.getDate() + 1);
  tomorrow.setHours(0, 0, 0, 0);
  return tomorrow.getTime() - now.getTime();
}

function formatCountdown(ms: number): string {
  const total = Math.max(0, Math.floor(ms / 1000));
  const h = Math.floor(total / 3600);
  const m = Math.floor((total % 3600) / 60);
  const s = total % 60;
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

const tileColor: Record<Eval, string> = {
  correct: "bg-[#171717] text-white border-[#171717]",
  present: "bg-[#525252] text-white border-[#525252]",
  absent: "bg-muted-foreground/80 text-white border-muted-foreground/80",
};

const keyColor: Record<Eval, string> = {
  correct: "bg-[#171717] text-white",
  present: "bg-[#525252] text-white",
  absent: "bg-muted-foreground/40 text-white/70",
};

export function DailySpark() {
  const target = useMemo(() => WORDS[getTodayIndex()], []);
  const dateKey = useMemo(() => getTodayKey(), []);

  const [hydrated, setHydrated] = useState(false);
  const [guesses, setGuesses] = useState<string[]>([]);
  const [current, setCurrent] = useState("");
  const [status, setStatus] = useState<"playing" | "won" | "lost">("playing");
  const [streak, setStreak] = useState(0);
  const [shake, setShake] = useState(false);
  const [toast, setToast] = useState<string | null>(null);
  const [shareCopied, setShareCopied] = useState(false);
  const [countdown, setCountdown] = useState("");
  const [revealRow, setRevealRow] = useState(-1);
  const toastTimer = useRef<number | null>(null);

  useEffect(() => {
    try {
      const saved = localStorage.getItem(`bigh-spark-${dateKey}`);
      if (saved) {
        const parsed = JSON.parse(saved) as { guesses?: string[]; status?: "playing" | "won" | "lost" };
        if (parsed.guesses?.length) {
          setGuesses(parsed.guesses);
          setRevealRow(parsed.guesses.length - 1);
        }
        if (parsed.status) setStatus(parsed.status);
      }
      const savedStreak = localStorage.getItem("bigh-spark-streak");
      const lastWin = localStorage.getItem("bigh-spark-lastWin");
      if (savedStreak && (lastWin === dateKey || lastWin === getYesterdayKey())) {
        setStreak(parseInt(savedStreak, 10) || 0);
      } else {
        setStreak(0);
      }
    } catch {}
    setHydrated(true);
  }, [dateKey]);

  useEffect(() => {
    if (!hydrated) return;
    localStorage.setItem(`bigh-spark-${dateKey}`, JSON.stringify({ guesses, status }));
  }, [hydrated, guesses, status, dateKey]);

  useEffect(() => {
    if (status === "playing") return;
    const update = () => setCountdown(formatCountdown(msUntilMidnight()));
    update();
    const i = window.setInterval(update, 1000);
    return () => window.clearInterval(i);
  }, [status]);

  const showToast = useCallback((msg: string) => {
    setToast(msg);
    if (toastTimer.current) window.clearTimeout(toastTimer.current);
    toastTimer.current = window.setTimeout(() => setToast(null), 1500);
  }, []);

  const submitGuess = useCallback(() => {
    if (current.length !== 5) {
      setShake(true);
      window.setTimeout(() => setShake(false), 450);
      showToast("Need 5 letters");
      return;
    }
    const next = [...guesses, current];
    setGuesses(next);
    setRevealRow(next.length - 1);
    setCurrent("");
    if (current === target) {
      window.setTimeout(() => {
        setStatus("won");
        const lastWin = localStorage.getItem("bigh-spark-lastWin");
        let newStreak = 1;
        if (lastWin === getYesterdayKey()) newStreak = streak + 1;
        else if (lastWin === dateKey) newStreak = streak;
        setStreak(newStreak);
        localStorage.setItem("bigh-spark-streak", String(newStreak));
        localStorage.setItem("bigh-spark-lastWin", dateKey);
      }, 1700);
    } else if (next.length >= MAX_GUESSES) {
      window.setTimeout(() => setStatus("lost"), 1700);
    }
  }, [current, guesses, target, streak, dateKey, showToast]);

  const handleKey = useCallback(
    (key: string) => {
      if (status !== "playing") return;
      if (key === "ENTER") submitGuess();
      else if (key === "BACK") setCurrent((c) => c.slice(0, -1));
      else if (current.length < 5 && /^[A-Z]$/.test(key)) setCurrent((c) => c + key);
    },
    [current.length, status, submitGuess],
  );

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === "Enter") handleKey("ENTER");
      else if (e.key === "Backspace") handleKey("BACK");
      else if (/^[a-zA-Z]$/.test(e.key)) handleKey(e.key.toUpperCase());
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [handleKey]);

  const letterStates = useMemo(() => {
    const map = new Map<string, Eval>();
    const priority: Record<Eval, number> = { absent: 0, present: 1, correct: 2 };
    guesses.forEach((g) => {
      const evals = evaluate(g, target);
      g.split("").forEach((l, i) => {
        const prev = map.get(l);
        if (!prev || priority[evals[i]] > priority[prev]) map.set(l, evals[i]);
      });
    });
    return map;
  }, [guesses, target]);

  const handleShare = () => {
    const grid = guesses
      .map((g) =>
        evaluate(g, target)
          .map((e) => (e === "correct" ? "🟧" : e === "present" ? "🟪" : "⬛"))
          .join(""),
      )
      .join("\n");
    const score = status === "won" ? `${guesses.length}/${MAX_GUESSES}` : `X/${MAX_GUESSES}`;
    const text = `BiGH Daily Spark · ${score}\n\n${grid}\n\nbigh.example/games/daily-spark`;
    navigator.clipboard
      .writeText(text)
      .then(() => {
        setShareCopied(true);
        window.setTimeout(() => setShareCopied(false), 2200);
      })
      .catch(() => showToast("Copy failed"));
  };

  return (
    <div className="mx-auto flex max-w-md flex-col items-center px-5 pb-10">
      <div className="mt-2 mb-4 flex w-full items-center justify-between">
        <div className="text-muted-foreground text-xs tracking-[0.25em] uppercase">
          Daily Spark
        </div>
        {streak > 0 && hydrated && (
          <div className="bg-foreground/10 text-foreground inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-medium">
            <span>🔥</span>
            <span>{streak} day{streak === 1 ? "" : "s"}</span>
          </div>
        )}
      </div>

      <AnimatePresence>
        {toast && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="bg-foreground pointer-events-none fixed top-32 left-1/2 z-50 -translate-x-1/2 rounded-md px-4 py-2 text-sm text-white shadow-lg"
          >
            {toast}
          </motion.div>
        )}
      </AnimatePresence>

      <motion.div
        animate={shake ? { x: [-8, 8, -6, 6, -3, 3, 0] } : { x: 0 }}
        transition={{ duration: 0.4 }}
        className="grid grid-rows-6 gap-1.5"
      >
        {Array.from({ length: MAX_GUESSES }).map((_, rowIdx) => {
          const guess = guesses[rowIdx];
          const isCurrent = rowIdx === guesses.length && status === "playing";
          const isRevealing = rowIdx === revealRow;
          const evals = guess ? evaluate(guess, target) : null;
          const letters = guess
            ? guess.split("")
            : isCurrent
              ? current.padEnd(5).split("")
              : Array(5).fill("");
          return (
            <div key={rowIdx} className="grid grid-cols-5 gap-1.5">
              {letters.map((letter, i) => {
                const filled = letter && letter !== " ";
                const showEval = evals !== null;
                return (
                  <motion.div
                    key={i}
                    initial={false}
                    animate={
                      isCurrent && filled
                        ? { scale: [1, 1.08, 1] }
                        : showEval && isRevealing
                          ? { rotateX: [0, 90, 0] }
                          : {}
                    }
                    transition={
                      showEval && isRevealing
                        ? { delay: i * 0.28, duration: 0.5 }
                        : { duration: 0.12 }
                    }
                    className={`flex h-14 w-14 items-center justify-center rounded-md border-2 text-2xl font-semibold uppercase select-none sm:h-16 sm:w-16 sm:text-3xl ${
                      showEval
                        ? tileColor[evals![i]]
                        : filled
                          ? "border-foreground/40 bg-muted text-foreground"
                          : "border-foreground/15 bg-transparent"
                    }`}
                  >
                    {letter && letter !== " " ? letter : ""}
                  </motion.div>
                );
              })}
            </div>
          );
        })}
      </motion.div>

      {status !== "playing" && (
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-muted mt-7 w-full rounded-2xl px-6 py-5 text-center"
        >
          <p className="font-display text-foreground text-2xl font-light">
            {status === "won" ? "Bright spark." : "Tomorrow."}
          </p>
          <p className="text-muted-foreground mt-1 text-sm">
            {status === "won"
              ? `Solved in ${guesses.length}/${MAX_GUESSES}.`
              : `Today's word was ${target}.`}
          </p>
          <div className="text-muted-foreground mt-4 text-xs tracking-[0.2em] uppercase">
            Next puzzle in
          </div>
          <div className="text-foreground font-mono text-lg tracking-wider tabular-nums">
            {countdown}
          </div>
          <button
            onClick={handleShare}
            className="bg-foreground hover:bg-foreground/90 mt-5 inline-flex items-center justify-center rounded-full px-7 py-2.5 text-sm font-medium text-white transition-colors"
          >
            {shareCopied ? "Copied to clipboard" : "Share result"}
          </button>
        </motion.div>
      )}

      {status === "playing" && (
        <div className="mt-7 grid w-full gap-1.5">
          {KEYBOARD_ROWS.map((row, ri) => (
            <div key={ri} className="flex justify-center gap-1.5">
              {row.map((key) => {
                const state = letterStates.get(key);
                const isAction = key === "ENTER" || key === "BACK";
                return (
                  <button
                    key={key}
                    onClick={() => handleKey(key)}
                    className={`flex h-12 items-center justify-center rounded-md text-sm font-semibold uppercase transition-colors sm:h-14 ${
                      isAction ? "w-14 text-xs sm:w-16" : "w-8 sm:w-9"
                    } ${
                      state
                        ? keyColor[state]
                        : "bg-foreground/8 text-foreground hover:bg-foreground/15"
                    }`}
                    aria-label={key === "BACK" ? "Backspace" : key}
                  >
                    {key === "BACK" ? <Delete className="h-4 w-4" /> : key}
                  </button>
                );
              })}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
