"use client";

import { useState } from "react";

// Contact form matching the original support page's fields exactly
// (Your Name*, Customer ID, Email*, Phone, Subject*, Message*, full-width
// green Send). Submissions are delivered by formsubmit.co to the BiGH inbox.
const ENDPOINT = "https://formsubmit.co/ajax/mo@bighnow.com";

interface Labels {
  title: string;
  name: string;
  namePh: string;
  customerId: string;
  customerIdPh: string;
  email: string;
  phone: string;
  phonePh: string;
  subject: string;
  subjectPh: string;
  message: string;
  send: string;
  sent: string;
  failed: string;
}

const inputCls =
  "w-full rounded border border-line bg-white px-3 py-2.5 text-[15px] text-heading outline-none focus:border-green";
const labelCls = "mb-1 mt-5 block text-[15px] font-medium text-heading";

export function SupportForm({ labels }: { labels: Labels }) {
  const [status, setStatus] = useState<"idle" | "sending" | "sent" | "failed">("idle");

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    setStatus("sending");
    try {
      const data = Object.fromEntries(new FormData(form).entries());
      const res = await fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          ...data,
          _subject: `[bighnow.com support] ${data.subject ?? ""}`,
          _template: "table",
        }),
      });
      if (!res.ok) throw new Error(String(res.status));
      form.reset();
      setStatus("sent");
    } catch {
      setStatus("failed");
    }
  }

  return (
    <section className="mx-auto max-w-6xl px-4 pb-16 sm:px-6">
      <h2 className="mt-12 text-center text-[clamp(2rem,3.8vw,3.4rem)] font-semibold text-black/60">
        {labels.title}
      </h2>
      <form onSubmit={onSubmit} className="mx-auto mt-6 max-w-6xl">
        <label className={labelCls} htmlFor="sf-name">
          {labels.name} <span aria-hidden className="text-red-500">*</span>
        </label>
        <input id="sf-name" name="name" type="text" required placeholder={labels.namePh} className={inputCls} />

        <label className={labelCls} htmlFor="sf-customer">
          {labels.customerId}
        </label>
        <input
          id="sf-customer"
          name="customer_id"
          type="text"
          inputMode="numeric"
          placeholder={labels.customerIdPh}
          className={inputCls}
        />

        <label className={labelCls} htmlFor="sf-email">
          {labels.email} <span aria-hidden className="text-red-500">*</span>
        </label>
        <input id="sf-email" name="email" type="email" required placeholder={labels.email} className={inputCls} />

        <label className={labelCls} htmlFor="sf-phone">
          {labels.phone}
        </label>
        <input
          id="sf-phone"
          name="phone"
          type="text"
          inputMode="tel"
          placeholder={labels.phonePh}
          className={inputCls}
        />

        <label className={labelCls} htmlFor="sf-subject">
          {labels.subject} <span aria-hidden className="text-red-500">*</span>
        </label>
        <input id="sf-subject" name="subject" type="text" required placeholder={labels.subjectPh} className={inputCls} />

        <label className={labelCls} htmlFor="sf-message">
          {labels.message} <span aria-hidden className="text-red-500">*</span>
        </label>
        <textarea id="sf-message" name="message" required rows={4} placeholder={labels.message} className={inputCls} />

        <button
          type="submit"
          disabled={status === "sending"}
          className="mt-7 w-full rounded bg-green py-4 text-lg font-medium text-white transition-colors hover:bg-green-dark disabled:opacity-60"
        >
          {labels.send}
        </button>

        {status === "sent" && (
          <p role="status" className="mt-4 text-center font-medium text-green-dark">
            {labels.sent}
          </p>
        )}
        {status === "failed" && (
          <p role="alert" className="mt-4 text-center font-medium text-red-600">
            {labels.failed}
          </p>
        )}
      </form>
    </section>
  );
}
