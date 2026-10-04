/**
 * Stops the page scrolling under an open sheet or the open menu, and returns the undo.
 * Where the window has a classic scrollbar, hiding it would widen the page and make it jump
 * sideways; its width is kept as padding while it is gone.
 */
export function lockPageScroll(): () => void {
  const { body, documentElement } = document;
  const overflow = body.style.overflow;
  const padding = body.style.paddingRight;
  const scrollbar = window.innerWidth - documentElement.clientWidth;
  body.style.overflow = "hidden";
  if (scrollbar > 0) body.style.paddingRight = `${scrollbar}px`;
  return () => {
    body.style.overflow = overflow;
    body.style.paddingRight = padding;
  };
}
