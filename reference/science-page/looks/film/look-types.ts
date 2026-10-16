import type { CSSProperties, JSX } from "react";

// The contract every round-3 look follows. A look renders the whole page between the shared header
// and footer: hero, Dr. Liu, his path, the formulas, the research, health explained, Ask BiGH
// Science. The shared header, footer and story panel read the look's tokens.
export type LookProps = { onStory: () => void };

export type LookTheme = {
  // CSS custom properties set on the page root: at least --paper, --paper-deep, --ink, --muted,
  // --line, --blue (accent). The shared header, footer and story panel use them.
  tokens: CSSProperties;
  footerTone: "light" | "dark";
};

export type LookComponent = (props: LookProps) => JSX.Element;
