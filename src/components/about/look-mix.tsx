"use client";

import type { LookProps } from "./about-page";
import { CalmClosing, CalmHero, CalmPromise, CalmRoots } from "./look-calm";
import { PurposeDive, SpaceExperience } from "./look-space";

// "A then B" (Mo, Sept 25: "do an A look and then a B look"). Light and dark alternate, as on the
// homepage: A's light opening with the coastal photo, B's dive telling the purpose, A's
// scientist section, B's gold numbers, then A's promise and closing card.
export function LookMix({ onAsk }: LookProps) {
  return (
    <>
      <CalmHero />
      <PurposeDive />
      <CalmRoots />
      <SpaceExperience afterLight />
      <CalmPromise />
      <CalmClosing onAsk={onAsk} />
    </>
  );
}
