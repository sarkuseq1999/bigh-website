// The Support page's words (Mo, October 13-14, 2026; spec
// docs/superpowers/specs/2026-10-14-support-page-design.md). The contact and return details are the
// 2016 ones, which Mo confirmed are still true on October 13. English only for now: none of these
// has a copy key, so every language shows them in English (useCopy returns the source when a
// string has no key). Mo approved the spec, the four answers included, on October 14 ("yes").

/** Real sending: the form posts to /api/support, which emails the message through Resend
 *  (src/lib/support-mail.ts) once its environment variables are set on Vercel (Mo picked an email
 *  service, November 16, 2026). The Support page reads that on the server and passes `live` to the
 *  form. Until then the form sends nothing and says so: the placeholder tag beside Send and the
 *  thank-you's line, and the page promises nothing it cannot keep (no ticket by email, no reply
 *  to a message that went nowhere). Once live, the spec's words come back: the lead's ticket line,
 *  the thank-you's "We'll reply by email", both placeholder lines gone. */

export const support = {
  opening: {
    title: "How can we help?",
    lead: "Pull up a chair. We’re listening.",
    call: { label: "Call us", value: "800-919-2089", href: "tel:+18009192089" },
    email: { label: "Email us", value: "support@bighnow.com", href: "mailto:support@bighnow.com" },
    hours: { label: "Hours", value: "Monday to Friday, 9am to 6pm Pacific" },
  },
  write: {
    label: "Write to us",
    title: "Send us a message.",
    lead: "We reply within 1–2 business days. Your ticket number comes by email.",
    // While SENDING_LIVE is false: the reply time is true of the phone and the email, the ticket by
    // email is not (Ruling 16).
    previewLead: "We reply within 1–2 business days.",
    name: "Your name",
    email: "Email",
    order: "Order number (optional)",
    topic: "What is it about?",
    topics: [
      "An order",
      "A return",
      "A product question",
      "A health or science question",
      "I had a reaction",
      "Something else",
    ],
    // Ask BiGH Science's buttons open the form with this topic chosen (/support?topic=science#write).
    scienceTopic: "A health or science question",
    message: "Your message",
    photo: "Add a photo (optional)",
    removePhoto: "Remove photo",
    send: "Send message",
    reaction:
      "Had a reaction to a product? Choose “I had a reaction” and a person reads it first. In an emergency, call 911.",
    preview: "Preview: messages aren’t sent yet",
    // When sending fails (the service is down): the message is not lost silently.
    failed:
      "We couldn’t send your message just now. Please try again, or email support@bighnow.com or call 800-919-2089.",
    sending: "Sending…",
    // Shown instead of the form until script has run (and for anyone without it): the form's Send
    // would otherwise be a GET with the message in the address.
    fallback: "To write to us, email support@bighnow.com or call 800-919-2089.",
    errors: {
      name: "Please add your name.",
      email: "Please add an email we can reply to.",
      topic: "Please choose what it’s about.",
      message: "Please write your message.",
      photoSize: "Photos up to 4 MB, please.",
      photoType: "Please choose a photo (JPG, PNG or HEIC).",
    },
  },
  sent: {
    title: "Thank you.",
    ticket: "Your ticket number",
    // Only once SENDING_LIVE: nothing was sent in the preview, so no reply is promised.
    reply: "We’ll reply by email within 1–2 business days.",
    // Straight under "Thank you." while SENDING_LIVE is false, its phone and email real links.
    preview:
      "This is a preview, so nothing was sent. To reach us today, call 800-919-2089 or email support@bighnow.com.",
    again: "Write another message",
  },
  returns: {
    label: "Returns",
    title: "45 days to decide.",
    lead: "Not happy with a product? Send it back within 45 days for a full refund, no questions asked. Shipping costs aren’t refunded.",
    after: "After 45 days, unopened bottles can still be returned for up to a year.",
    to: "Send returns to",
    address: ["BiGH, 2200 E Route 66, Suite 103", "Glendora, CA 91740"],
    ordersLabel: "Orders and shipping",
    orders:
      "Our online shop opens soon. Until then, call or email us with any order question and we’ll help.",
  },
  questions: {
    label: "Questions",
    title: "Common questions.",
    items: [
      {
        q: "How do I take my supplements?",
        a: "Follow the directions on your bottle’s label. For questions about your own health, ask your doctor or pharmacist.",
      },
      {
        q: "Can I take them with my medicines?",
        a: "Please ask your doctor or pharmacist first. They know your medicines and your health.",
      },
      {
        q: "Where is my order?",
        a: "Call 800-919-2089 or email support@bighnow.com with your name and order number, and we’ll look it up for you.",
      },
      {
        q: "Is this site in my language?",
        a: "Choose English, Chinese, Korean, Vietnamese or Japanese at the top of any page. Write to us in any of them, and we’ll reply in yours.",
      },
    ],
    more: "A question about health or science?",
    // Has a copy key already (the homepage's and About's button).
    ask: "Ask BiGH Science",
  },
} as const;

export const ALT = {
  porch:
    "Two empty wooden chairs on a California porch, a cup of coffee on a small table between them, its steam in gold leaf, painted in ink",
  mailbox: "A rural mailbox on a wooden post in tall dry grass, its flag raised, painted in ink",
  parcel: "A parcel tied with twine on wooden porch steps, painted in ink",
  book: "An open book on a porch rail, its pages lifting in a breeze, painted in ink",
} as const;
