# Interaction Tiers

Pick a tier for each page section in Phase A2. Sections can differ (a hero can be L3 while the blog is L1), but the spec must say which section uses which tier.

## Questions to ask per tier

- **L1 Micro:** Which controls need feedback? (buttons, links, inputs, toggles)
- **L2 Choreographed:** Which surfaces enter and leave? (modal, drawer, toast, list, route) Should lists stagger? Should loaders animate?
- **L3 Scroll story:** Which sections are pinned or scroll-linked? Is parallax wanted? Are GSAP and ScrollTrigger allowed? (At most two pins per page.)

## L1 Micro

CSS transitions only. No JavaScript.

```css
.btn {
  background-color: var(--color-accent);
  transform: translateY(0);
  transition:
    background-color var(--motion-duration-fast) var(--motion-ease-standard),
    transform var(--motion-duration-fast) var(--motion-ease-standard);
}
.btn:hover { background-color: var(--color-accent-hover); transform: translateY(-1px); }
.btn:active { transform: translateY(0) scale(0.98); transition-duration: var(--motion-duration-instant); }
.btn:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
```

Rules:
- Transition only the properties you change. Never write `transition: all`.
- Every hover effect has a `:focus-visible` equivalent.
- Touch devices have no hover. Make the `:active` state clear.

## L2 Choreographed

Use CSS keyframes for one-shot entrances. Use the Web Animations API for JavaScript-triggered motion you need to control. Use GSAP for multi-step sequences.

```css
@keyframes panel-in {
  from { opacity: 0; transform: translateY(var(--motion-distance-md)) scale(0.98); }
  to   { opacity: 1; transform: none; }
}
.panel { animation: panel-in var(--motion-duration-base) var(--motion-ease-enter) both; }
```

```js
// Web Animations API: controllable, no library needed
const anim = el.animate(
  [{ opacity: 0, transform: 'translateY(8px)' }, { opacity: 1, transform: 'none' }],
  { duration: 240, easing: 'cubic-bezier(0, 0, 0.2, 1)', fill: 'both' }
);
await anim.finished;
```

Keep the JavaScript values in one module, mirrored from the CSS tokens, so the two never drift apart. Or read them at start-up with `getComputedStyle(document.documentElement).getPropertyValue('--motion-duration-base')`.

**Exit before removal:** play the exit, then remove the element.

```js
await el.animate(exitFrames, { duration: 160, easing: 'cubic-bezier(0.4, 0, 1, 1)' }).finished;
el.remove();
```

**Reduced motion:** keep the fade or colour change, remove the movement, or remove the element at once.

## L3 Scroll story

GSAP with ScrollTrigger, or CSS scroll-driven animations with a fallback. See `scroll-patterns.md` and `gsap-recipes.md`.

Limits:
- At most two pinned sections per page.
- Every L3 effect has a mobile version (simplified or off) and a reduced-motion version (static).
- Content in every scroll section is visible without JavaScript.

## Tier summary

| | L1 Micro | L2 Choreographed | L3 Scroll story |
|-|----------|------------------|-----------------|
| Triggers | hover, focus, press | state change, mount, route | scroll position |
| Dependencies | none | none (GSAP optional) | GSAP + ScrollTrigger, or CSS scroll-driven |
| Pinned sections | none | none | at most 2 |
| Mobile | tap feedback | simplified | simplified or off |
| Reduced motion | colour and opacity only | fades only | static layout |
