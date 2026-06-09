"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "motion/react";

type SparkKind = "gold" | "red";

type Spark = {
  id: number;
  kind: SparkKind;
  startX: number;
  startY: number;
  endX: number;
  endY: number;
  duration: number;
  size: number;
};

const GAME_DURATION = 30;
const SPAWN_INTERVAL_START = 520;
const SPAWN_INTERVAL_END = 240;
const RED_PROBABILITY_START = 0.1;
const RED_PROBABILITY_END = 0.22;

type Phase = "intro" | "playing" | "ended";

export function CatchTheSpark() {
  const [phase, setPhase] = useState<Phase>("intro");
  const [sparks, setSparks] = useState<Spark[]>([]);
  const [score, setScore] = useState(0);
  const [hits, setHits] = useState(0);
  const [missed, setMissed] = useState(0);
  const [redTaps, setRedTaps] = useState(0);
  const [reactions, setReactions] = useState<number[]>([]);
  const [bestScore, setBestScore] = useState(0);
  const [timeLeft, setTimeLeft] = useState(GAME_DURATION);
  const [combo, setCombo] = useState(0);
  const [floaters, setFloaters] = useState<{ id: number; x: number; y: number; text: string; color: string }[]>([]);

  const idRef = useRef(0);
  const floaterIdRef = useRef(0);
  const containerRef = useRef<HTMLDivElement>(null);
  const spawnTimeRef = useRef<Map<number, number>>(new Map());
  const phaseRef = useRef<Phase>("intro");
  const timeLeftRef = useRef(GAME_DURATION);

  useEffect(() => {
    phaseRef.current = phase;
  }, [phase]);

  useEffect(() => {
    timeLeftRef.current = timeLeft;
  }, [timeLeft]);

  useEffect(() => {
    const saved = localStorage.getItem("bigh-catch-best");
    if (saved) setBestScore(parseInt(saved, 10) || 0);
  }, []);

  const startGame = useCallback(() => {
    setSparks([]);
    setScore(0);
    setHits(0);
    setMissed(0);
    setRedTaps(0);
    setReactions([]);
    setTimeLeft(GAME_DURATION);
    setCombo(0);
    setFloaters([]);
    spawnTimeRef.current.clear();
    setPhase("playing");
  }, []);

  const endGame = useCallback(() => {
    setPhase("ended");
    setSparks([]);
    setScore((s) => {
      setBestScore((b) => {
        if (s > b) {
          localStorage.setItem("bigh-catch-best", String(s));
          return s;
        }
        return b;
      });
      return s;
    });
  }, []);

  // Countdown timer
  useEffect(() => {
    if (phase !== "playing") return;
    const interval = window.setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1) {
          window.setTimeout(endGame, 0);
          return 0;
        }
        return t - 1;
      });
    }, 1000);
    return () => window.clearInterval(interval);
  }, [phase, endGame]);

  // Spark spawner
  useEffect(() => {
    if (phase !== "playing") return;
    let cancelled = false;

    const spawnOne = () => {
      if (cancelled || phaseRef.current !== "playing") return;
      const el = containerRef.current;
      if (!el) return;
      const rect = el.getBoundingClientRect();
      const w = rect.width;
      const h = rect.height;
      if (w < 50 || h < 50) return;

      const progress = 1 - timeLeftRef.current / GAME_DURATION;
      const baseDur = 4.6 - progress * 2.6;
      const duration = baseDur + Math.random() * 0.7;
      const redProb = RED_PROBABILITY_START + (RED_PROBABILITY_END - RED_PROBABILITY_START) * progress;
      const isRed = Math.random() < redProb;
      const size = isRed ? 20 + Math.random() * 14 : 16 + Math.random() * 16;

      const edge = Math.floor(Math.random() * 4);
      let startX = 0, startY = 0, endX = 0, endY = 0;
      const m = 60;
      if (edge === 0) {
        startX = Math.random() * w; startY = -m;
        endX = Math.random() * w; endY = h + m;
      } else if (edge === 1) {
        startX = w + m; startY = Math.random() * h;
        endX = -m; endY = Math.random() * h;
      } else if (edge === 2) {
        startX = Math.random() * w; startY = h + m;
        endX = Math.random() * w; endY = -m;
      } else {
        startX = -m; startY = Math.random() * h;
        endX = w + m; endY = Math.random() * h;
      }

      idRef.current += 1;
      const id = idRef.current;
      spawnTimeRef.current.set(id, performance.now());
      setSparks((prev) => [
        ...prev,
        { id, kind: isRed ? "red" : "gold", startX, startY, endX, endY, duration, size },
      ]);
    };

    let timeout: number;
    const tick = () => {
      if (cancelled) return;
      spawnOne();
      const progress = 1 - timeLeftRef.current / GAME_DURATION;
      const interval =
        SPAWN_INTERVAL_START + (SPAWN_INTERVAL_END - SPAWN_INTERVAL_START) * progress;
      timeout = window.setTimeout(tick, Math.max(180, interval + (Math.random() - 0.5) * 100));
    };
    timeout = window.setTimeout(tick, 350);

    return () => {
      cancelled = true;
      window.clearTimeout(timeout);
    };
  }, [phase]);

  const pushFloater = useCallback((x: number, y: number, text: string, color: string) => {
    floaterIdRef.current += 1;
    const id = floaterIdRef.current;
    setFloaters((f) => [...f, { id, x, y, text, color }]);
    window.setTimeout(() => {
      setFloaters((f) => f.filter((it) => it.id !== id));
    }, 900);
  }, []);

  const handleSparkClick = useCallback(
    (spark: Spark, clickX: number, clickY: number) => {
      setSparks((prev) => prev.filter((s) => s.id !== spark.id));
      const spawnedAt = spawnTimeRef.current.get(spark.id);
      spawnTimeRef.current.delete(spark.id);

      if (spark.kind === "gold") {
        const reaction = spawnedAt ? performance.now() - spawnedAt : 0;
        setReactions((r) => [...r, reaction]);
        setHits((h) => h + 1);
        setCombo((c) => {
          const nextCombo = c + 1;
          const bonus = 10 + Math.min(20, Math.floor(nextCombo / 3) * 5);
          setScore((s) => s + bonus);
          pushFloater(clickX, clickY, `+${bonus}`, "text-amber-300");
          return nextCombo;
        });
      } else {
        setRedTaps((r) => r + 1);
        setCombo(0);
        setScore((s) => Math.max(0, s - 15));
        pushFloater(clickX, clickY, "-15", "text-rose-400");
      }
    },
    [pushFloater],
  );

  const handleSparkExit = useCallback((spark: Spark) => {
    spawnTimeRef.current.delete(spark.id);
    setSparks((prev) => prev.filter((s) => s.id !== spark.id));
    if (spark.kind === "gold") {
      setMissed((m) => m + 1);
      setCombo(0);
    }
  }, []);

  const accuracy =
    hits + redTaps > 0 ? Math.round((hits / (hits + redTaps)) * 100) : 0;
  const avgReaction =
    reactions.length > 0
      ? Math.round(reactions.reduce((a, b) => a + b, 0) / reactions.length)
      : 0;

  return (
    <div className="relative mx-auto w-full max-w-5xl px-4">
      <div
        ref={containerRef}
        className="relative h-[70vh] min-h-[480px] w-full overflow-hidden rounded-3xl"
        style={{
          background:
            "radial-gradient(ellipse at 30% 20%, #2a1a3a 0%, #0a0a1a 60%, #050510 100%)",
        }}
      >
        {/* Star field */}
        <div className="pointer-events-none absolute inset-0 opacity-50">
          {Array.from({ length: 60 }).map((_, i) => (
            <div
              key={i}
              className="absolute rounded-full bg-white"
              style={{
                left: `${(i * 37) % 100}%`,
                top: `${(i * 53) % 100}%`,
                width: `${(i % 3) + 1}px`,
                height: `${(i % 3) + 1}px`,
                opacity: 0.2 + ((i % 5) / 10),
              }}
            />
          ))}
        </div>

        {/* HUD */}
        <div className="pointer-events-none absolute top-0 right-0 left-0 z-10 flex items-start justify-between p-5 text-white">
          <div>
            <div className="text-xs tracking-[0.25em] text-white/50 uppercase">Score</div>
            <div className="font-display text-3xl font-light tabular-nums">
              {score}
            </div>
            {combo >= 3 && phase === "playing" && (
              <motion.div
                key={combo}
                initial={{ scale: 1.4, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="mt-1 text-xs font-medium text-amber-300"
              >
                ×{combo} combo
              </motion.div>
            )}
          </div>
          <div className="text-right">
            <div className="text-xs tracking-[0.25em] text-white/50 uppercase">Time</div>
            <div
              className={`font-display text-3xl font-light tabular-nums ${
                timeLeft <= 5 && phase === "playing"
                  ? "text-rose-400"
                  : "text-white"
              }`}
            >
              {timeLeft}s
            </div>
          </div>
        </div>

        {/* Sparks */}
        <AnimatePresence>
          {sparks.map((spark) => (
            <motion.button
              key={spark.id}
              initial={{ x: spark.startX, y: spark.startY, scale: 0, opacity: 0 }}
              animate={{
                x: spark.endX,
                y: spark.endY,
                scale: [0, 1, 1, 0.9],
                opacity: [0, 1, 1, 0],
              }}
              transition={{
                duration: spark.duration,
                ease: "linear",
                scale: { duration: spark.duration, times: [0, 0.08, 0.85, 1] },
                opacity: { duration: spark.duration, times: [0, 0.08, 0.85, 1] },
              }}
              onAnimationComplete={() => handleSparkExit(spark)}
              onClick={(e) => {
                e.stopPropagation();
                const rect = containerRef.current?.getBoundingClientRect();
                const clickX = rect ? e.clientX - rect.left : 0;
                const clickY = rect ? e.clientY - rect.top : 0;
                handleSparkClick(spark, clickX, clickY);
              }}
              className="absolute top-0 left-0 cursor-pointer rounded-full border-0 p-0"
              style={{
                width: spark.size,
                height: spark.size,
                background:
                  spark.kind === "gold"
                    ? "radial-gradient(circle, #fff8d6 0%, #fde68a 35%, #f59e0b 70%, transparent 100%)"
                    : "radial-gradient(circle, #ffd6d6 0%, #fb7185 35%, #e11d48 70%, transparent 100%)",
                boxShadow:
                  spark.kind === "gold"
                    ? `0 0 ${spark.size * 1.2}px rgba(252, 211, 77, 0.7), 0 0 ${spark.size * 2}px rgba(252, 211, 77, 0.35)`
                    : `0 0 ${spark.size * 1.2}px rgba(251, 113, 133, 0.7), 0 0 ${spark.size * 2}px rgba(251, 113, 133, 0.35)`,
              }}
              aria-label={spark.kind === "gold" ? "Catch the spark" : "Avoid the red spark"}
            />
          ))}
        </AnimatePresence>

        {/* Score floaters */}
        <AnimatePresence>
          {floaters.map((f) => (
            <motion.div
              key={f.id}
              initial={{ opacity: 1, x: f.x, y: f.y, scale: 0.8 }}
              animate={{ opacity: 0, y: f.y - 60, scale: 1.2 }}
              transition={{ duration: 0.9, ease: "easeOut" }}
              className={`pointer-events-none absolute top-0 left-0 -translate-x-1/2 -translate-y-1/2 text-2xl font-bold ${f.color}`}
              style={{ textShadow: "0 0 12px currentColor" }}
            >
              {f.text}
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Intro overlay */}
        {phase === "intro" && (
          <div className="absolute inset-0 z-20 flex items-center justify-center bg-black/50 backdrop-blur-sm">
            <div className="mx-6 max-w-md text-center text-white">
              <h2 className="font-display text-5xl font-light leading-tight tracking-tight">
                Catch the <em className="text-amber-300">spark.</em>
              </h2>
              <p className="mt-5 text-white/80">
                Gold sparks <span className="text-amber-300">light up</span> the screen.
                Tap them. Red sparks are <span className="text-rose-400">decoys</span> — don't tap.
              </p>
              <p className="mt-2 text-sm text-white/50">
                Thirty seconds. Combo bonuses build with every catch.
              </p>
              <button
                onClick={startGame}
                className="mt-8 inline-flex items-center justify-center rounded-full bg-amber-300 px-10 py-3 text-base font-semibold text-[#0a0a1a] shadow-lg shadow-amber-500/30 transition-transform hover:scale-105 active:scale-95"
              >
                Begin
              </button>
              {bestScore > 0 && (
                <p className="mt-6 text-xs tracking-[0.25em] text-white/40 uppercase">
                  Best score · {bestScore}
                </p>
              )}
            </div>
          </div>
        )}

        {/* End overlay */}
        {phase === "ended" && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.4 }}
            className="absolute inset-0 z-20 flex items-center justify-center bg-black/70 backdrop-blur-md"
          >
            <div className="mx-6 max-w-md text-center text-white">
              <p className="text-xs tracking-[0.25em] text-white/50 uppercase">
                Round complete
              </p>
              <div className="mt-2 font-display text-7xl font-light tabular-nums text-amber-300">
                {score}
              </div>
              {score > 0 && score === bestScore && (
                <div className="mt-1 text-sm font-medium text-amber-200">
                  New personal best
                </div>
              )}
              <div className="mx-auto mt-8 grid max-w-xs grid-cols-3 gap-4 text-left">
                <Stat label="Caught" value={hits} />
                <Stat label="Missed" value={missed} />
                <Stat label="Accuracy" value={`${accuracy}%`} />
                <Stat label="Avg react" value={avgReaction ? `${avgReaction}ms` : "—"} />
                <Stat label="Red taps" value={redTaps} />
                <Stat label="Best" value={bestScore} />
              </div>
              <button
                onClick={startGame}
                className="mt-8 inline-flex items-center justify-center rounded-full bg-amber-300 px-10 py-3 text-base font-semibold text-[#0a0a1a] shadow-lg shadow-amber-500/30 transition-transform hover:scale-105 active:scale-95"
              >
                Play again
              </button>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string | number }) {
  return (
    <div>
      <div className="text-[10px] tracking-[0.2em] text-white/40 uppercase">
        {label}
      </div>
      <div className="font-display text-xl font-light tabular-nums text-white">
        {value}
      </div>
    </div>
  );
}
