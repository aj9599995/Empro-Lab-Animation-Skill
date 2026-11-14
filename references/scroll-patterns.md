# Scroll Patterns

Scroll-driven motion for L2 reveals and L3 scroll stories. Each pattern lists its fallback and its mobile rule.

## Mobile rule for every pattern

Below 768 px:
- Pinned sections are not pinned. They scroll in order.
- Parallax is off.
- Reveals stay on, but they are shorter and smaller.

Under `prefers-reduced-motion: reduce`:
- Parallax and pinned movement are off.
- Reveals show content at once, or fade only.

## 1. Reveal on enter

Content fades in when it enters the viewport. It plays once.

```html
<article class="card" data-reveal>...</article>
```

Use `templates/reveal.js` with the `[data-reveal]` rules in `templates/motion-tokens.css`. Stagger the group with a `--i` index and `--motion-stagger`.

Rules:
- `threshold` 0.15 is a good default. Use a larger `rootMargin` offset so items reveal just before they reach the centre of the screen.
- Reveal once. Do not hide content again when it leaves the viewport.
- Add the `js` class to `<html>` in the head, so content stays visible without JavaScript.

## 2. Scroll progress bar

CSS scroll-driven animation, with a JavaScript fallback.

```css
.progress {
  position: fixed; inset: 0 0 auto 0; height: 3px;
  transform-origin: left center;
  transform: scaleX(0);
}

@supports (animation-timeline: scroll()) {
  @media (prefers-reduced-motion: no-preference) {
    .progress {
      animation: grow-x linear both;
      animation-timeline: scroll(root);
    }
  }
}

@keyframes grow-x { from { transform: scaleX(0); } to { transform: scaleX(1); } }
```

```js
// Fallback: one rAF-throttled scroll listener
let ticking = false;
function update() {
  const max = document.documentElement.scrollHeight - innerHeight;
  bar.style.transform = `scaleX(${max > 0 ? scrollY / max : 0})`;
  ticking = false;
}
addEventListener('scroll', () => { if (!ticking) { requestAnimationFrame(update); ticking = true; } }, { passive: true });
```

Only run the JavaScript fallback when `CSS.supports('animation-timeline', 'scroll()')` is false.

## 3. Sticky stacking cards

No animation library. Each card sticks a little lower than the one before, so the stack appears to build up as the user scrolls.

```css
.stack-card {
  position: sticky;
  top: calc(96px + var(--i, 0) * 16px);
}
```

```html
<article class="stack-card" style="--i: 0">...</article>
<article class="stack-card" style="--i: 1">...</article>
```

Mobile: remove `position: sticky` below 768 px, so the cards scroll normally.

## 4. Parallax (light, desktop only)

Keep the movement under 40 px, and apply it to decorative elements, never to text blocks.

```js
mm.add('(min-width: 768px) and (prefers-reduced-motion: no-preference)', () => {
  gsap.to('.parallax-art', {
    y: -40,
    ease: 'none',
    scrollTrigger: { trigger: '.parallax-section', start: 'top bottom', end: 'bottom top', scrub: true },
  });
});
```

Parallax is a vestibular trigger. Keep it small, and never combine it with zoom or spin. See `accessibility.md`.

## 5. Horizontal scroll section (L3, pinned)

Counts as one of the two pins. Desktop only.

```js
mm.add('(min-width: 1024px) and (prefers-reduced-motion: no-preference)', () => {
  const track = document.querySelector('.h-track');
  gsap.to(track, {
    x: () => -(track.scrollWidth - innerWidth),
    ease: 'none',
    scrollTrigger: {
      trigger: '.h-section',
      pin: true,
      scrub: 0.6,
      end: () => '+=' + track.scrollWidth,
      invalidateOnRefresh: true,
    },
  });
});
```

Below 1024 px the track becomes a normal horizontal list with its own scroll bar, or a vertical stack. Both must be keyboard-accessible.

## 6. Section entrance with a sticky heading

The heading stays in place while the content moves past it. CSS only:

```css
.section-head { position: sticky; top: 24px; }
```

Use it for reference-style pages. Do not add motion to the heading on top of this.

## Choosing a pattern

| Goal | Pattern | Tier |
|------|---------|------|
| Content appears as the user reads | 1. Reveal on enter | L2 |
| Show how far the user has read | 2. Progress bar | L2 |
| Show a sequence of related cards | 3. Sticky stacking | L2 |
| Add depth to a hero or feature | 4. Parallax (light) | L3 |
| Walk through wide content | 5. Horizontal scroll | L3 |
