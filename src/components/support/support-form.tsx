"use client";

import Image from "next/image";
import { ArrowRight } from "lucide-react";
import {
  useEffect,
  useRef,
  useState,
  useSyncExternalStore,
  type CSSProperties,
  type FormEvent,
} from "react";
import { flushSync } from "react-dom";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { useSteamGate, useWordsLang } from "./spread";
import { cup } from "./support-art";
import { SENDING_LIVE, support } from "./support-content";
import {
  checkFields,
  checkPhoto,
  ticketNumber,
  type FieldName,
  type Problems,
} from "./support-rules";
import page from "./support-page.module.css";

// The Support form (spec "The form", "The moment", "Honesty"): writing lines on the paper, never
// boxes; checks on Send in plain words beside each field, focus to the first; on Send the form
// gives way to the cup, its gold steam rising again, and a ticket number. It sends nothing until
// SENDING_LIVE: the preview tag and the thank-you's preview line say so.

const ORDER: FieldName[] = ["name", "email", "topic", "message", "photo"];
const FOCUS: Record<FieldName, string> = {
  name: "support-name",
  email: "support-email",
  topic: "support-topic-0",
  message: "support-message",
  photo: "support-photo",
};

// True on the client once it has hydrated, false on the server and for the hydrating render itself
// (so the two always match), without a state update in an effect.
const subscribe = () => () => {};
const useMounted = () =>
  useSyncExternalStore(
    subscribe,
    () => true,
    () => false,
  );

export function SupportForm() {
  const copy = useCopy();
  const mounted = useMounted();
  const [ticket, setTicket] = useState<string | null>(null);
  // Each "Write another message" is a fresh form (the key), and only that one takes focus: the
  // page's first form never grabs it.
  const [round, setRound] = useState(0);
  // Without script, or before it has loaded, there is no form: Send would be a GET with the name, the
  // email and a possible health report in the address (and a page that looks as if it sent). The
  // page says how to write instead, with real links; the form replaces the line once it is alive.
  if (!mounted) {
    return (
      <p className={`${page.body} ${page.fallback}`} data-fallback="">
        {reach(copy(support.write.fallback), true)}
      </p>
    );
  }
  if (ticket) {
    return (
      <Thanks
        ticket={ticket}
        onAgain={() => {
          setTicket(null);
          setRound((r) => r + 1);
        }}
      />
    );
  }
  return <Message key={round} focusName={round > 0} onSent={setTicket} />;
}

function Message({ focusName, onSent }: { focusName: boolean; onSent: (ticket: string) => void }) {
  const copy = useCopy();
  const lang = useWordsLang();
  const w = support.write;
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [order, setOrder] = useState("");
  const [topic, setTopic] = useState("");
  const [message, setMessage] = useState("");
  const [photo, setPhoto] = useState<File | null>(null);
  const [problems, setProblems] = useState<Problems>({});
  const photoInput = useRef<HTMLInputElement>(null);
  const nameInput = useRef<HTMLInputElement>(null);
  // Spec "The moment": on Send the form fades out (0.3s), then the thank-you comes. `sending` is
  // a ref, not just state: a second submit in the same task (a double click, requestSubmit twice)
  // must find it already set. `leaving` holds the ticket while the form fades.
  const sending = useRef(false);
  const [leaving, setLeaving] = useState<string | null>(null);

  useEffect(() => {
    if (focusName) nameInput.current?.focus();
  }, [focusName]);

  useEffect(() => {
    if (!leaving) return;
    const timer = setTimeout(() => onSent(leaving), 300);
    return () => clearTimeout(timer);
  }, [leaving, onSent]);

  const send = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (sending.current) return; // one thank-you, one number
    const found = checkFields({ name, email, topic, message, photo });
    // The messages must be on the page before focus moves: a screen reader reads a field's
    // aria-invalid and its description once, as focus lands (set later, they are never heard).
    flushSync(() => setProblems(found));
    const first = ORDER.find((field) => found[field]);
    if (first) {
      document.getElementById(FOCUS[first])?.focus();
      return;
    }
    sending.current = true;
    const ticket = ticketNumber();
    // Reduced motion: no fade, the thank-you at once.
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) onSent(ticket);
    else setLeaving(ticket);
  };

  const choosePhoto = (file: File | undefined) => {
    if (!file) return;
    const problem = checkPhoto(file);
    if (problem) {
      setPhoto(null);
      if (photoInput.current) photoInput.current.value = "";
      setProblems((p) => ({ ...p, photo: problem }));
      return;
    }
    setPhoto(file);
    setProblems((p) => ({ ...p, photo: undefined }));
  };

  // A field's message goes as soon as it is touched: never a "choose one" beside a chip chosen.
  const touched = (field: FieldName) =>
    setProblems((p) => (p[field] ? { ...p, [field]: undefined } : p));

  // "Remove photo" goes away with the photo, so focus goes to the photo's own control (its label
  // shows the ring), never lost to the page.
  const removePhoto = () => {
    setPhoto(null);
    if (photoInput.current) {
      photoInput.current.value = "";
      photoInput.current.focus();
    }
  };

  const error = (field: FieldName) =>
    problems[field] ? (
      <p id={`support-${field}-error`} className={page.error} data-error="">
        {copy(problems[field]!)}
      </p>
    ) : null;
  const described = (field: FieldName) => (problems[field] ? `support-${field}-error` : undefined);

  return (
    <form
      className={page.form}
      method="post"
      onSubmit={send}
      noValidate
      inert={leaving ? true : undefined}
      data-leaving={leaving ? "" : undefined}
      data-support-form=""
    >
      <div className={page.field}>
        <label htmlFor="support-name" lang={lang(w.name)}>
          {copy(w.name)}
        </label>
        <input
          ref={nameInput}
          id="support-name"
          name="name"
          autoComplete="name"
          aria-required="true"
          value={name}
          onChange={(e) => {
            setName(e.target.value);
            touched("name");
          }}
          aria-invalid={problems.name ? true : undefined}
          aria-describedby={described("name")}
        />
        {error("name")}
      </div>
      <div className={page.field}>
        <label htmlFor="support-email">{copy(w.email)}</label>
        <input
          id="support-email"
          name="email"
          type="email"
          autoComplete="email"
          inputMode="email"
          aria-required="true"
          value={email}
          onChange={(e) => {
            setEmail(e.target.value);
            touched("email");
          }}
          aria-invalid={problems.email ? true : undefined}
          aria-describedby={described("email")}
        />
        {error("email")}
      </div>
      <div className={page.field}>
        <label htmlFor="support-order">{copy(w.order)}</label>
        <input
          id="support-order"
          name="order"
          value={order}
          onChange={(e) => setOrder(e.target.value)}
        />
      </div>
      <fieldset
        className={page.field}
        role="radiogroup"
        aria-required="true"
        aria-invalid={problems.topic ? true : undefined}
        aria-describedby={described("topic")}
      >
        <legend>{copy(w.topic)}</legend>
        <div className={page.topics} data-topics="">
          {w.topics.map((t, i) => (
            <span key={t} className={page.topicChoice}>
              <input
                id={`support-topic-${i}`}
                type="radio"
                name="topic"
                value={t}
                checked={topic === t}
                onChange={() => {
                  setTopic(t);
                  touched("topic");
                }}
              />
              <label htmlFor={`support-topic-${i}`}>{copy(t)}</label>
            </span>
          ))}
        </div>
        {error("topic")}
      </fieldset>
      <div className={page.field}>
        <label htmlFor="support-message">{copy(w.message)}</label>
        <textarea
          id="support-message"
          name="message"
          rows={4}
          aria-required="true"
          value={message}
          onChange={(e) => {
            setMessage(e.target.value);
            touched("message");
          }}
          aria-invalid={problems.message ? true : undefined}
          aria-describedby={described("message")}
        />
        {error("message")}
      </div>
      <div className={page.photo}>
        <input
          ref={photoInput}
          id="support-photo"
          className={base.visuallyHidden}
          type="file"
          accept="image/*"
          onChange={(e) => choosePhoto(e.target.files?.[0])}
          aria-describedby={described("photo")}
        />
        <label htmlFor="support-photo" className={base.textLink}>
          {copy(w.photo)}
        </label>
        {photo ? (
          <p className={page.photoName}>
            <span>{photo.name}</span>
            <button type="button" className={base.textLink} onClick={removePhoto}>
              {copy(w.removePhoto)}
            </button>
          </p>
        ) : null}
        {error("photo")}
      </div>
      <div className={page.sendRow}>
        <button type="submit" className={base.pill}>
          {copy(w.send)} <ArrowRight size={18} aria-hidden="true" />
        </button>
        {SENDING_LIVE ? null : (
          <span className={page.honesty} data-honesty="">
            {copy(w.preview)}
          </span>
        )}
      </div>
      <p className={page.note}>{copy(w.reaction)}</p>
    </form>
  );
}

// A phone number or an address in a line of words never breaks across two lines: the words around
// them wrap, they stay. In a line that invites a message (links) each is also the real link.
function reach(text: string, links: boolean) {
  return text.split(/(\d{3}-\d{3}-\d{4}|\S+@\S+[a-z])/).map((part, i) => {
    if (i % 2 === 0) return part;
    if (!links)
      return (
        <span key={i} className={page.nowrap}>
          {part}
        </span>
      );
    const href = part.includes("@") ? `mailto:${part}` : `tel:+1${part.replaceAll("-", "")}`;
    return (
      <a key={i} className={page.nowrap} href={href}>
        {part}
      </a>
    );
  });
}

// The moment: the cup, its steam rising again, the number. The cup's pictures load only now, so
// the steam is gated like the porch's (spread.tsx useSteamGate): it rises only once the cup's
// picture and its own are in, never alone over bare paper.
function Thanks({ ticket, onAgain }: { ticket: string; onAgain: () => void }) {
  const copy = useCopy();
  const s = support.sent;
  const gate = useSteamGate();
  const root = useRef<HTMLDivElement>(null);
  const title = useRef<HTMLHeadingElement>(null);

  // Focus goes to "Thank you." (for a screen reader), but the page is brought to the cup, not to
  // the heading: the form was taller than this, and focus alone would leave the cup above the fold.
  useEffect(() => {
    title.current?.focus({ preventScroll: true });
    root.current?.scrollIntoView({ block: "start" });
  }, []);

  return (
    <div ref={root} className={page.sent} data-sent="" aria-live="polite">
      <span className={page.cup}>
        <Image
          {...gate.ink}
          className={`${base.ink} ${page.cupInk}`}
          src={cup.src}
          alt=""
          width={cup.width}
          height={cup.height}
          sizes="220px"
          loading="eager"
          data-cup={gate.inkIn ? "in" : "waiting"}
        />
        <Image
          {...gate.gold}
          className={page.steam}
          src={cup.steam.src}
          alt=""
          width={cup.steam.width}
          height={cup.steam.height}
          sizes="100px"
          loading="eager"
          fetchPriority="low"
          data-steam={gate.steam}
          style={
            {
              left: `${(cup.steam.left * 100).toFixed(2)}%`,
              top: `${(cup.steam.top * 100).toFixed(2)}%`,
              width: `${(cup.steam.size * 100).toFixed(2)}%`,
            } as CSSProperties
          }
        />
      </span>
      <h3 id="sent-title" ref={title} tabIndex={-1} className={page.sentTitle}>
        {copy(s.title)}
      </h3>
      {/* While nothing is sent (Ruling 16): first, straight under "Thank you.", that nothing was
          sent and how to reach us today, with real links; no reply is promised. */}
      {SENDING_LIVE ? null : (
        <p className={page.previewLine} data-honesty="">
          {reach(copy(s.preview), true)}
        </p>
      )}
      <p className={page.sentLabel}>{copy(s.ticket)}</p>
      <p className={page.ticket} data-ticket="">
        {ticket}
      </p>
      {SENDING_LIVE ? <p className={page.body}>{copy(s.reply)}</p> : null}
      <button type="button" className={base.textLink} onClick={onAgain}>
        {copy(s.again)}
      </button>
    </div>
  );
}
