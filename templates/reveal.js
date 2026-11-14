/*
  reveal.js - scroll reveal with IntersectionObserver. No dependencies.

  Pairs with the [data-reveal] rules in templates/motion-tokens.css.

  Usage:
    import { initReveal } from './reveal.js';
    const stop = initReveal();          // reveals every [data-reveal] element
    // when the page or component is torn down:
    stop();

  Reduced motion, or no IntersectionObserver support: every item is shown at once.
*/

const reduceQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

export function initReveal(selector = '[data-reveal]', { root = document, threshold = 0.15 } = {}) {
  const items = Array.from(root.querySelectorAll(selector));
  if (items.length === 0) return () => {};

  if (reduceQuery.matches || !('IntersectionObserver' in window)) {
    items.forEach((el) => el.classList.add('is-revealed'));
    return () => {};
  }

  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        entry.target.classList.add('is-revealed');
        observer.unobserve(entry.target); // reveal once; do not hide again on scroll back
      }
    },
    { threshold, rootMargin: '0px 0px -10% 0px' }
  );

  items.forEach((el) => observer.observe(el));
  return () => observer.disconnect();
}
