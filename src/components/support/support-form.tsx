"use client";

import Image from "next/image";
import { ArrowRight } from "lucide-react";
import { useEffect, useRef, useState, type CSSProperties, type FormEvent } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { useSteamGate } from "./spread";
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

export function SupportForm() {
  const [ticket, setTicket] = useState<string | null>(null);
  // Each "Write another message" is a fresh form (the key), and only that one takes focus: the
  // page's first form never grabs it.
  const [round, setRound] = useState(0);
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

  useEffect(() => {
    if (focusName) nameInput.current?.focus();
  }, [focusName]);

  const send = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const found = checkFields({ name, email, topic, message, photo });
    setProblems(found);
    const first = ORDER.find((field) => found[field]);
    if (first) {
      document.getElementById(FOCUS[first])?.focus();
      return;
    }
    onSent(ticketNumber());
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

  const removePhoto = () => {
    setPhoto(null);
    if (photoInput.current) photoInput.current.value = "";
  };

  const error = (field: FieldName) =>
    problems[field] ? (
      <p id={`support-${field}-error`} className={page.error} data-error="">
        {copy(problems[field]!)}
      </p>
    ) : null;
  const described = (field: FieldName) => (problems[field] ? `support-${field}-error` : undefined);

  return (
    <form className={page.form} onSubmit={send} noValidate data-support-form="">
      <div className={page.field}>
        <label htmlFor="support-name">{copy(w.name)}</label>
        <input
          ref={nameInput}
          id="support-name"
          name="name"
          autoComplete="name"
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

// A phone number or an address never breaks across two lines: the words around them wrap, they stay.
function whole(text: string) {
  return text.split(/(\d{3}-\d{3}-\d{4}|\S+@\S+[a-z])/).map((part, i) =>
    i % 2 ? (
      <span key={i} className={page.nowrap}>
        {part}
      </span>
    ) : (
      part
    ),
  );
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
          sizes="182px"
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
          sizes="120px"
          loading="eager"
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
      <p className={page.sentLabel}>{copy(s.ticket)}</p>
      <p className={page.ticket} data-ticket="">
        {ticket}
      </p>
      <p className={page.body}>{copy(s.reply)}</p>
      {SENDING_LIVE ? null : (
        <p className={page.previewLine} data-honesty="">
          {whole(copy(s.preview))}
        </p>
      )}
      <button type="button" className={base.textLink} onClick={onAgain}>
        {copy(s.again)}
      </button>
    </div>
  );
}
