# ANIMATION.md

> Motion that confirms every action, orients the reader and never makes anyone wait. This page is the proof: it is written spec first, then built.

## 1. Motion Personality & Principles

**Personality**: Calm (default), with the Snappy, Playful and Cinematic switch for demonstration only
**Keywords**: precise, editorial, quiet, confident, technical
**Page type**: showcase (a method page that is also a product page)
**Tier by section**: Hero L2 · Live tokens L1 · Tiers L1/L2/L3 · Scroll reveal L2

**Principles**
- Every motion has a job: confirm, orient, connect or delight. The hero is the only delight moment.
- Movement is small (4 to 16 px). Fades carry most of the change.
- Reduced motion removes movement and keeps the state changes.

## 2. Motion Tokens

```css
:root {
  --motion-duration-instant: 90ms;
  --motion-duration-fast: 150ms;
  --motion-duration-base: 240ms;
  --motion-duration-slow: 400ms;
  --motion-duration-slower: 600ms;

  --motion-ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --motion-ease-enter: cubic-bezier(0, 0, 0.2, 1);
  --motion-ease-exit: cubic-bezier(0.4, 0, 1, 1);
  --motion-ease-emphasis: cubic-bezier(0.2, 0.8, 0.2, 1);
  --motion-ease-linear: linear;

  --motion-distance-sm: 4px;
  --motion-distance-md: 8px;
  --motion-distance-lg: 16px;
  --motion-stagger: 60ms;
}
```

**Token rules**
- Exits are 60 to 75 percent of the matching enter duration.
- The Playful and Cinematic values are shown by the page switch. The page itself uses Calm.

## 3. Choreography Inventory

| Element | Trigger | Property | Duration | Easing | Delay | Reduced-motion fallback |
|---------|---------|----------|----------|--------|-------|-------------------------|
| Hero title, lead, actions | Page load | opacity, transform | base | enter | 0 to 2 × stagger | opacity only, no movement |
| Primary and secondary buttons | Hover, press | background-color, border-color, transform | fast (press: instant) | standard | 0 | colour change only |
| Token box | Click | transform, background-color | base (move), fast (colour) | enter (move) | 0 | no movement, colour change only |
| Accordion panel | Click | grid-template-rows | base | standard | 0 | same, instant |
| Card lift | Hover, focus-within | transform, border-color | base | standard | 0 | border colour only |
| Reveal cards | Enter viewport | opacity, transform | slow | enter | 0 | visible at once |
| Progress bar | Scroll | transform (scaleX) | linear, tied to scroll | none | 0 | hidden |

Anything not in this table does not animate.

## 4. Component Motion

### Button
- **Default**: static, background set by token colour.
- **Hover**: border turns to accent, lifts by half a small distance.
- **Focus-visible**: 2 px outline, 2 px offset.
- **Active**: scale 0.98 in the instant duration.
- **Disabled**: no motion, reduced opacity.

### Card
- **Default**: static border.
- **Hover / focus-within**: lifts by the small distance, border picks up the accent.
- **Enter**: reveals once with the reveal rule.

### Accordion
- **Default**: height 0 (grid row 0fr).
- **Open**: grid row animates to 1fr. The chevron, if present, rotates 180 degrees.
- **Reduced motion**: the same change, instant.

### Token box
- **Default**: static.
- **Pressed**: moves right by four times the large distance, colour shifts to the hover accent.
- **Reduced motion**: colour change only.

## 5. Scroll Behavior

- **Reveal**: threshold 0.15, reveal once, root margin bottom 10 percent. Applies to cards in the reveal section.
- **Scroll-linked**: progress bar at the top of the page only. No pins on this page.
- **Mobile (600 px and below)**: reveal stays. The header hides its links except the last one. The token box stays in place.

## 6. Page & Route Transitions

- **Type**: none. The page is a single document.
- **Duration**: not applicable.
- **Shared elements**: none.

## 7. Performance Budget

- **Animated properties**: transform, opacity, plus grid-template-rows on one accordion. The progress bar uses transform.
- **Exceptions**: grid-template-rows on the accordion. It animates layout, but only inside one small card, and it avoids a pixel height. Recorded here on purpose.
- **Maximum simultaneously animating elements**: 12.
- **Infinite loops**: none.
- **Target**: 60 fps on a mid-range phone with a 4x CPU slowdown.

## 8. Accessibility

- **Reduced motion**: from the OS setting, with an in-page switch as an extra. Movement is removed, state changes and fades stay, the progress bar is hidden.
- **Flashing**: none.
- **Auto-playing content longer than 5 s**: none.
- **Keyboard and focus**: every hover effect has a focus-visible state. The skip link is the first focusable element.

## 9. Do's and Don'ts

**Do's**
- Keep the hero entrance under 700 ms in total.
- Show the final state at once when reduced motion is on.
- Name every token and use it everywhere.
- Keep the accordion's button label and `aria-expanded` in sync.

**Don'ts**
- Do not transition `transition: all`.
- Do not animate width, height, top, left, margin or padding, except the one recorded exception.
- Do not animate blur or large shadows.
- Do not hide content with CSS that depends on JavaScript. The `js` class gates the reveal.
- Do not add a second animation library to this page.
- Do not loop anything.

## 10. Dependencies

| Package | Version | Why | Tier |
|---------|---------|-----|------|
| None | — | The page is plain HTML, CSS and JavaScript so GitHub Pages can serve it without a build. | — |

**No dependency**: this page uses no animation library.
