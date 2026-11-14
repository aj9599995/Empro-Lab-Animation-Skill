# GSAP Recipes

Use GSAP for timelines, sequencing and ScrollTrigger. Do not use it for hover effects that CSS handles. Check `package.json` first and use what is already installed.

## Setup (once per app)

```bash
npm install gsap
```

```js
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);
```

## Respect reduced motion with matchMedia

`gsap.matchMedia()` runs the block only while the query matches, and reverts everything when the query stops matching.

```js
const mm = gsap.matchMedia();

mm.add('(prefers-reduced-motion: no-preference)', () => {
  // Hidden start states live here, not in CSS. Reduced-motion users never get hidden content.
  gsap.from('[data-stagger] > *', {
    opacity: 0,
    y: 16,
    duration: 0.4,
    ease: 'power2.out',
    stagger: 0.06,
    scrollTrigger: { trigger: '[data-stagger]', start: 'top 80%', once: true },
  });
});
```

Rule: put the hidden start state in the GSAP block, not in the stylesheet. If the CSS hides the element and JavaScript fails or the user has reduced motion, the content stays hidden.

## Hero timeline

```js
const tl = gsap.timeline({ defaults: { duration: 0.4, ease: 'power2.out' } });

tl.from('.hero-title', { yPercent: 40, opacity: 0 })
  .from('.hero-sub', { y: 16, opacity: 0 }, '-=0.2')
  .from('.hero-cta', { y: 8, opacity: 0 }, '-=0.2');
```

Wrap the timeline in the `mm.add` block above so it does not run under reduced motion. Reduced-motion users see the final layout.

## Scroll progress (scrubbed)

```js
mm.add('(prefers-reduced-motion: no-preference)', () => {
  gsap.fromTo('.progress', { scaleX: 0 }, {
    scaleX: 1,
    ease: 'none',
    transformOrigin: 'left center',
    scrollTrigger: { trigger: document.body, start: 'top top', end: 'bottom bottom', scrub: true },
  });
});
```

Under reduced motion the bar is simply not shown, or it can show the static final state. Decide that in ANIMATION.md.

## Pinned section (maximum two per page)

```js
mm.add('(min-width: 768px) and (prefers-reduced-motion: no-preference)', () => {
  ScrollTrigger.create({
    trigger: '.pin-section',
    start: 'top top',
    end: '+=100%',
    pin: true,
    scrub: 0.6,
    // animate inside the scrub with a timeline if needed
  });
});
```

Below 768 px the section is not pinned. It scrolls normally, and its content must still read in order.

## Refresh after layout changes

Fonts and images change the height of the page. Refresh ScrollTrigger once they settle.

```js
document.fonts.ready.then(() => ScrollTrigger.refresh());
window.addEventListener('load', () => ScrollTrigger.refresh());
```

## React: clean up with useGSAP

```jsx
import { useRef } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';

export function Features() {
  const scope = useRef(null);

  useGSAP(() => {
    gsap.from('.feature', { opacity: 0, y: 12, stagger: 0.06, duration: 0.4 });
  }, { scope });

  return <section ref={scope}>{/* .feature items */}</section>;
}
```

`useGSAP` reverts the tweens and ScrollTriggers when the component unmounts. Use `scope` so selectors only match inside this component. Put the reduced-motion check inside the callback, as in the `matchMedia` examples above.

## Vue or Svelte

Create the animations in `onMounted` (Vue) or `onMount` (Svelte). Kill them in `onUnmounted` or the function returned from `onMount`. Or use `gsap.context()`:

```js
const ctx = gsap.context(() => {
  gsap.from('.item', { opacity: 0, duration: 0.4 });
}, rootEl);

// on unmount
ctx.revert();
```

## Gotchas

- `gsap.from()` on an element that is not rendered yet reads the wrong position. Animate after mount.
- Do not transition the same property in CSS and GSAP. The two fight each other.
- `to()` tweens do not render their start state until they run. Use `from()` or `fromTo()` for entrances.
- ScrollTrigger `once: true` stops a reveal from playing again when the user scrolls back up.
- Kill everything on route changes in single-page apps. Leftover ScrollTriggers keep pins in the wrong place.
- Import only the plugins you use. Do not import every GSAP plugin into a page that uses one.
