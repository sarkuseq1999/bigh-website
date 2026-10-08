"use client";

import { useSyncExternalStore } from "react";

const still = () => () => {};

/**
 * An inline script that runs where the parser reaches it in the server's HTML, before React
 * hydrates, and that React never creates on the client. A plain <script> in the page's tree runs
 * the same on a first load, but after a client-side navigation (the menu bar's About) React
 * builds it afresh, never runs it, and in development logs "Encountered a script tag while
 * rendering React component". useSyncExternalStore's server snapshot is used only on the server
 * and while hydrating, so the script is rendered there (it hydrates the server's own element, no
 * mismatch) and nowhere else: once hydrated React drops it (it has already run), and a page
 * reached by navigation never has it.
 */
export function BeforeHydration({ code }: { code: string }) {
  const fromServer = useSyncExternalStore(
    still,
    () => false,
    () => true,
  );
  return fromServer ? <script dangerouslySetInnerHTML={{ __html: code }} /> : null;
}
