import { support } from "@/components/support/support-content";
import { PHOTO_MAX, ticketNumber } from "@/components/support/support-rules";
import { SUPPORT_INBOX, sendMail, supportMailConfigured } from "@/lib/support-mail";

// The Support form's sending (support-form.tsx posts here). Two emails per message: the message
// itself to BiGH's support inbox (reply-to the visitor, the photo attached, a reaction report
// marked urgent in its subject), and a short confirmation to the visitor with the ticket number.
// The ticket number is made here, so the one on the page is the one in both emails.

export const runtime = "nodejs";

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const TOPICS = new Set<string>(support.write.topics);
const REACTION = "I had a reaction";
const LIMITS = { name: 120, email: 200, order: 60, message: 6000 };

const clean = (value: FormDataEntryValue | null, max: number) =>
  typeof value === "string" ? value.replace(/\r\n?/g, "\n").trim().slice(0, max) : "";

export async function POST(request: Request) {
  if (!supportMailConfigured()) {
    return Response.json({ error: "not-configured" }, { status: 503 });
  }

  let form: FormData;
  try {
    form = await request.formData();
  } catch {
    return Response.json({ error: "bad-request" }, { status: 400 });
  }

  // A field people never see: a filled one is a robot. Answer as if sent, send nothing.
  if (clean(form.get("website"), 200)) {
    return Response.json({ ticket: ticketNumber() });
  }

  const name = clean(form.get("name"), LIMITS.name);
  const email = clean(form.get("email"), LIMITS.email);
  const order = clean(form.get("order"), LIMITS.order);
  const topic = clean(form.get("topic"), 80);
  const message = clean(form.get("message"), LIMITS.message);
  const locale = clean(form.get("locale"), 8) || "en";
  const photo = form.get("photo");

  if (!name || !EMAIL.test(email) || !TOPICS.has(topic) || !message) {
    return Response.json({ error: "invalid" }, { status: 422 });
  }

  const attachments = [];
  if (photo instanceof File && photo.size > 0) {
    if (photo.size > PHOTO_MAX || !/^image\//.test(photo.type || "image/")) {
      return Response.json({ error: "photo" }, { status: 422 });
    }
    const bytes = Buffer.from(await photo.arrayBuffer());
    attachments.push({
      filename: photo.name.replace(/[^\w.\- ]+/g, "_").slice(0, 80) || "photo.jpg",
      content: bytes.toString("base64"),
      ...(photo.type ? { content_type: photo.type } : {}),
    });
  }

  const ticket = ticketNumber();
  const urgent = topic === REACTION;
  const inbox = process.env.SUPPORT_EMAIL_TO || SUPPORT_INBOX;

  const lines = [
    `Ticket: ${ticket}`,
    `Topic: ${topic}${urgent ? " (PLEASE READ FIRST)" : ""}`,
    `Name: ${name}`,
    `Email: ${email}`,
    order ? `Order number: ${order}` : null,
    `Site language: ${locale}`,
    "",
    message,
    "",
    attachments.length ? "A photo is attached." : null,
    "Sent from the Support page on the BiGH website. Reply to this email to answer the customer.",
  ].filter((line): line is string => line !== null);

  try {
    await sendMail({
      to: inbox,
      replyTo: email,
      subject: `${urgent ? "URGENT reaction report — " : ""}${topic} — ${name} [${ticket}]`,
      text: lines.join("\n"),
      attachments,
    });
  } catch (error) {
    console.error("support: message not sent", error);
    return Response.json({ error: "send-failed" }, { status: 502 });
  }

  // The visitor's copy. A failure here does not undo the message BiGH already has.
  try {
    await sendMail({
      to: email,
      replyTo: inbox,
      subject: `We have your message [${ticket}]`,
      text: [
        `Hello ${name},`,
        "",
        "Thank you for writing to BiGH. We have your message and will reply by email within 1–2 business days.",
        "",
        `Your ticket number is ${ticket}. If you write again or call us, mention it and we will find your message right away.`,
        "",
        urgent
          ? "You told us you had a reaction to a product. A person on our team reads these first. If you feel unwell, please contact your doctor. In an emergency, call 911.\n"
          : null,
        "Your message:",
        message,
        "",
        "BiGH Support",
        "800-919-2089 · Monday to Friday, 9am to 6pm Pacific",
        "support@bighnow.com",
      ]
        .filter((line) => line !== null)
        .join("\n"),
    });
  } catch (error) {
    console.error("support: confirmation not sent", error);
  }

  return Response.json({ ticket });
}
