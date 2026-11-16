import { notFound } from "next/navigation";

// Any address that is no page of the site shows the site's own "not found" page
// ([locale]/not-found.tsx), in the visitor's language, inside the site's menu bar and footer.
export default function CatchAll() {
  notFound();
}
