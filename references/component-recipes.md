# Component Recipes

CSS recipes for common components. Each one uses the tokens from `templates/motion-tokens.css` and states its reduced-motion behaviour. Copy the pattern, then rename the classes to match the project.

## Button

```css
.btn {
  transition:
    background-color var(--motion-duration-fast) var(--motion-ease-standard),
    transform var(--motion-duration-fast) var(--motion-ease-standard);
}
.btn:hover { transform: translateY(-1px); }
.btn:active { transform: scale(0.98); transition-duration: var(--motion-duration-instant); }
```

Reduced motion: replace the hard-coded `-1px` lift with `calc(var(--motion-distance-sm) * -0.25)`, so it falls to zero when the distance tokens are set to 0. The press scale of 0.98 is a small state response, so it can stay. Record that choice in the spec.

## Link underline draw

```css
.link {
  background-image: linear-gradient(currentColor, currentColor);
  background-size: 0% 1px;
  background-position: 0 100%;
  background-repeat: no-repeat;
  transition: background-size var(--motion-duration-base) var(--motion-ease-standard);
}
.link:hover,
.link:focus-visible { background-size: 100% 1px; }
```

Reduced motion: no change needed. The underline appears at once if the duration is set to 0 in the reduced block.

## Card lift

```css
.card {
  transition: transform var(--motion-duration-base) var(--motion-ease-standard);
}
.card:hover,
.card:focus-within { transform: translateY(calc(var(--motion-distance-sm) * -1)); }
```

For a shadow change, fade a pseudo-element's opacity instead of transitioning `box-shadow`. Opacity is cheap; shadows repaint.

## Input focus ring

```css
.input {
  transition: box-shadow var(--motion-duration-fast) var(--motion-ease-standard),
              border-color var(--motion-duration-fast) var(--motion-ease-standard);
}
.input:focus-visible {
  border-color: var(--color-focus);
  box-shadow: 0 0 0 3px rgb(var(--focus-rgb) / 0.35);
}
```

Never remove the focus ring under reduced motion. It is not movement.

## Icon rotate (disclosure chevron)

```css
.chevron { transition: transform var(--motion-duration-fast) var(--motion-ease-standard); }
[aria-expanded="true"] > .chevron { transform: rotate(180deg); }
```

## Accordion

Animates the height with `grid-template-rows`, so no pixel height is needed. Supported in current browsers.

```css
.collapse {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows var(--motion-duration-base) var(--motion-ease-standard);
}
.collapse[data-open="true"] { grid-template-rows: 1fr; }
.collapse > div { overflow: hidden; min-height: 0; }
```

```html
<button aria-expanded="false" aria-controls="faq-1">Question</button>
<div class="collapse" id="faq-1" data-open="false"><div><p>Answer.</p></div></div>
```

Keep `aria-expanded` in sync with `data-open` in JavaScript.

`grid-template-rows` is a layout property, so the audit flags it. Record it as an exception: put `/* motion-exception: <reason> */` on the line above the `transition` declaration, and list the same exception in ANIMATION.md section 7. `analyze_motion.py` then reports it as a recorded exception, not as an error.

## Modal (native `<dialog>`)

```css
dialog {
  opacity: 0;
  transform: translateY(var(--motion-distance-md)) scale(0.98);
  transition:
    opacity var(--motion-duration-base) var(--motion-ease-enter),
    transform var(--motion-duration-base) var(--motion-ease-enter),
    display var(--motion-duration-base) allow-discrete;
}
dialog[open] { opacity: 1; transform: none; }
@starting-style {
  dialog[open] { opacity: 0; transform: translateY(var(--motion-distance-md)) scale(0.98); }
}
dialog::backdrop {
  background: rgb(0 0 0 / 0.5);
  opacity: 0;
  transition: opacity var(--motion-duration-base) var(--motion-ease-standard);
}
dialog[open]::backdrop { opacity: 1; }
```

`@starting-style` and `allow-discrete` need recent browsers. Without them the dialog still opens, just without the entrance. Check the support table before you rely on it.

Reduced motion: remove `transform` from both states. Keep the opacity change.

## Drawer (slides in from the side)

```css
.drawer {
  transform: translateX(100%);
  transition: transform var(--motion-duration-slow) var(--motion-ease-enter);
}
.drawer[data-open="true"] { transform: none; }

@media (prefers-reduced-motion: reduce) {
  .drawer { transform: none; transition: opacity var(--motion-duration-fast) linear; opacity: 0; }
  .drawer[data-open="true"] { opacity: 1; }
}
```

Close with the exit easing, and set `inert` on the content behind the drawer while it is open.

## Toast

```html
<div class="toasts" role="status" aria-live="polite"></div>
```

```css
.toast {
  transform: translateY(var(--motion-distance-lg));
  opacity: 0;
  transition:
    opacity var(--motion-duration-base) var(--motion-ease-enter),
    transform var(--motion-duration-base) var(--motion-ease-enter);
}
.toast.is-visible { opacity: 1; transform: none; }
```

- Keep the toast visible for at least 5 seconds, and longer for long messages.
- Pause the timer while the toast is hovered or focused.
- Give a control to dismiss it. Do not use motion alone to tell the user something happened.

## Tabs with a sliding indicator

Move the indicator with `transform` and set its width with `scaleX`. Do not transition `left` or `width`, because both trigger layout.

```css
.tab-indicator {
  position: absolute; left: 0; bottom: 0; height: 2px; width: 100%;
  transform-origin: left center;
  transition: transform var(--motion-duration-base) var(--motion-ease-standard);
}
```

```js
function moveIndicator(tab, indicator) {
  indicator.style.transform = `translateX(${tab.offsetLeft}px) scaleX(${tab.offsetWidth / indicator.parentElement.offsetWidth})`;
}
```

Reduced motion: the indicator still moves to the new tab, but instantly.

## Skeleton shimmer (loop)

```css
.skeleton { position: relative; overflow: hidden; background: var(--surface-2); }
.skeleton::after {
  content: "";
  position: absolute; inset: 0;
  transform: translateX(-100%);
  background: linear-gradient(90deg, transparent, rgb(255 255 255 / 0.08), transparent);
  animation: shimmer 1.6s var(--motion-ease-linear) infinite;
}
@keyframes shimmer { to { transform: translateX(100%); } }

@media (prefers-reduced-motion: reduce) {
  .skeleton::after { animation: none; }
}
```

The shimmer moves a pseudo-element with `transform`, which is cheaper than animating a background position.

## Spinner (loop)

A spinner is a loading indicator. It is essential information, so do not remove it under reduced motion. Slow it down and keep it visible.

```css
.spinner { animation: spin 0.9s var(--motion-ease-linear) infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (prefers-reduced-motion: reduce) {
  .spinner { animation-duration: 2.4s; }
}
```

Also give it an accessible name, such as `role="status"` with visible text like "Loading".
