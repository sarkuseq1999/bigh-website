// The Support form's rules (spec "The form"): what must be filled, what a photo may be, and the
// ticket number. Plain functions, no React, so the form and its checks read the same rules. (Named
// support-rules, not support-form: a support-form.ts beside support-form.tsx would be the module
// "./support-form" resolves to, hiding the form.)
import { support } from "./support-content";

export type Fields = {
  name: string;
  email: string;
  topic: string;
  message: string;
  photo: File | null;
};
export type FieldName = "name" | "email" | "topic" | "message" | "photo";
export type Problems = Partial<Record<FieldName, string>>;

export const PHOTO_MAX = 4 * 1024 * 1024;
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const PICTURE = /^image\/(jpeg|png|heic|heif|webp|gif)$/;
const errors = support.write.errors;

/** A photo's problem (an English source for copy()), or null when it may be kept. */
export function checkPhoto(file: File): string | null {
  if (!PICTURE.test(file.type) && !/\.(jpe?g|png|heic|heif|webp|gif)$/i.test(file.name))
    return errors.photoType;
  if (file.size > PHOTO_MAX) return errors.photoSize;
  return null;
}

/** Every field's problem, in the form's order (an empty object when it may be sent). */
export function checkFields(fields: Fields): Problems {
  const problems: Problems = {};
  if (!fields.name.trim()) problems.name = errors.name;
  if (!EMAIL.test(fields.email.trim())) problems.email = errors.email;
  if (!fields.topic) problems.topic = errors.topic;
  if (!fields.message.trim()) problems.message = errors.message;
  if (fields.photo) {
    const photo = checkPhoto(fields.photo);
    if (photo) problems.photo = photo;
  }
  return problems;
}

// No 0/O, 1/I/L: a number read over the phone is never mistaken.
const SIGNS = "ABCDEFGHJKMNPQRSTUVWXYZ23456789";

/** BH- + the month and day + four signs, e.g. BH-1014-7K3Q. Until real sending, the page makes it
 *  up; the email service will issue it then (spec "Not in this spec"). */
export function ticketNumber(now = new Date(), random: () => number = Math.random): string {
  const mmdd = `${String(now.getMonth() + 1).padStart(2, "0")}${String(now.getDate()).padStart(2, "0")}`;
  let tail = "";
  for (let i = 0; i < 4; i += 1) tail += SIGNS[Math.floor(random() * SIGNS.length)];
  return `BH-${mmdd}-${tail}`;
}
