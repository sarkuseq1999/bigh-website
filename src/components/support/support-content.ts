// The Support page's words (Mo, October 13-14, 2026; spec
// docs/superpowers/specs/2026-10-14-support-page-design.md). The contact and return details are the
// 2016 ones, which Mo confirmed are still true on October 13. English only for now: none of these
// has a copy key, so every language shows them in English (useCopy returns the source when a
// string has no key). The four answers are drafts Mo approved with the spec on October 14.

/** Real sending (the email service, Resend through Vercel, and bighnow.com's DNS records at
 *  GoDaddy) comes later (Mo, October 14). Until then the form sends nothing and says so; set this
 *  to true when it does, and both preview lines go. */
export const SENDING_LIVE = false;

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
    name: "Your name",
    email: "Email",
    order: "Order number (optional)",
    topic: "What is it about?",
    topics: ["An order", "A return", "A product question", "I had a reaction", "Something else"],
    message: "Your message",
    photo: "Add a photo (optional)",
    removePhoto: "Remove photo",
    send: "Send message",
    reaction:
      "Had a reaction to a product? Choose “I had a reaction” and a person reads it first. In an emergency, call 911.",
    preview: "Preview: messages aren’t sent yet",
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
    reply: "We’ll reply by email within 1–2 business days.",
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
    orders: "Our new store opens soon. Until then, no orders or payments are taken on this site.",
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
        a: "Our new store opens soon. Until then, call or email us and we’ll help.",
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
