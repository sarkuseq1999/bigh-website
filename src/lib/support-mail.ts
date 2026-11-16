// Support messages by email, through Resend's REST API (no SDK: one POST per email). Mo picked an
// email service for the Support form on November 16, 2026. It is switched on by three environment
// variables on Vercel (Production), then a redeploy:
//
//   RESEND_API_KEY        the Resend API key (Resend dashboard > API keys)
//   SUPPORT_EMAIL_FROM    a sender on a domain verified in Resend, e.g. "BiGH <support@bighnow.com>"
//                         (verifying bighnow.com adds its DNS records at GoDaddy)
//   SUPPORT_EMAIL_TO      where messages arrive; defaults to support@bighnow.com
//
// Until RESEND_API_KEY and SUPPORT_EMAIL_FROM are set, the form keeps its placeholder line and
// sends nothing (support-form.tsx), and the route answers 503.

export const SUPPORT_INBOX = "support@bighnow.com";

export function supportMailConfigured(): boolean {
  return Boolean(process.env.RESEND_API_KEY && process.env.SUPPORT_EMAIL_FROM);
}

type Attachment = { filename: string; content: string; content_type?: string };

export type MailInput = {
  to: string;
  subject: string;
  text: string;
  replyTo?: string;
  attachments?: Attachment[];
};

/** Sends one email. Throws with Resend's message when it is refused. */
export async function sendMail(input: MailInput): Promise<void> {
  const key = process.env.RESEND_API_KEY;
  const from = process.env.SUPPORT_EMAIL_FROM;
  if (!key || !from) throw new Error("Support email is not configured");
  // RESEND_API_BASE only for tests (a local stand-in for Resend); production leaves it unset.
  const base = process.env.RESEND_API_BASE || "https://api.resend.com";
  const response = await fetch(`${base}/emails`, {
    method: "POST",
    headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from,
      to: [input.to],
      subject: input.subject,
      text: input.text,
      ...(input.replyTo ? { reply_to: input.replyTo } : {}),
      ...(input.attachments?.length ? { attachments: input.attachments } : {}),
    }),
    signal: AbortSignal.timeout(15000),
  });
  if (!response.ok) {
    const detail = await response.text().catch(() => "");
    throw new Error(`Resend ${response.status}: ${detail.slice(0, 300)}`);
  }
}
