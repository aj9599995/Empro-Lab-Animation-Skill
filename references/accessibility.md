# Accessibility

Motion can make a page hard to use for some people: those with vestibular disorders, those with photosensitive epilepsy, and those who are distracted or have attention disorders. Plan for them from the start.

## prefers-reduced-motion

The user's operating system setting, read by the browser.

- Windows: Settings → Accessibility → Visual effects → Animation effects (off).
- macOS: System Settings → Accessibility → Display → Reduce motion.
- iOS: Settings → Accessibility → Motion → Reduce Motion.

**What reduced motion means in this skill:**
- Remove movement: translate, scale, rotate, parallax, pinned scroll movement.
- Keep state changes: fades, colour changes, focus rings, the final layout.
- Stop or slow loops. Keep essential indicators such as spinners, but slow them down.
- Turn off smooth scrolling (`scroll-behavior: auto`).
- Show hidden content at once, or fade it. Never leave content invisible.

**How to implement it:**
- CSS: `@media (prefers-reduced-motion: reduce) { ... }`, or set the distance tokens to 0 as `templates/motion-tokens.css` does.
- JavaScript: `window.matchMedia('(prefers-reduced-motion: reduce)')`. Listen for changes with `addEventListener('change', ...)`.
- GSAP: `gsap.matchMedia()` with the `prefers-reduced-motion: no-preference` query.

**Opt-out is not the default.** Do not add an in-page toggle that hides the OS setting. An in-page toggle is fine as an extra, but the OS setting must work on its own.

## WCAG criteria that apply to motion

| Criterion | Level | What it requires |
|-----------|-------|------------------|
| 2.2.2 Pause, Stop, Hide | A | Any content that moves, blinks or scrolls automatically for more than 5 seconds must have a way to pause, stop or hide it. |
| 2.3.1 Three Flashes or Below Threshold | A | Nothing flashes more than three times in any one-second period. |
| 2.3.3 Animation from Interactions | AAA | Motion triggered by interaction can be turned off, unless it is essential. Reduced motion covers this in practice. |
| 2.4.7 Focus Visible | AA | Keyboard focus is always visible. Motion must never hide it. |
| 2.4.11 Focus Not Obscured | AA | A sticky header or an animated overlay must not cover the focused element. |
| 1.4.13 Content on Hover or Focus | AA | Tooltips and hover content that appear with motion can be dismissed, hovered and kept visible. |
| 4.1.3 Status Messages | AA | Toasts and status updates use `role="status"` or `aria-live`, so screen readers announce them without the motion. |

Use the level the project targets. Most projects target AA.

## Flashing

- Never flash more than three times per second. Check strobe-style effects, fast colour cycles and rapid opacity toggles.
- Large areas of a flashing colour are the most dangerous. Keep flashes small, or do not use them.
- The static audit does not measure flashing. Check it by eye and in the spec.

## Vestibular triggers

These cause dizziness or nausea for some people. Use them rarely, and always behind reduced motion:
- Parallax with large movement, and parallax on a full-screen background.
- Zoom or scale that fills the screen, especially on scroll.
- Spinning or rotating elements that are large or near the centre of the screen.
- Panning backgrounds and horizontal scrolling that moves without the user's input.

## Focus and keyboard

- Every hover effect has a `:focus-visible` equivalent.
- Animations must not move the focused element away from the user's point of focus.
- A dialog, drawer or menu that animates in must move focus into it, and return focus when it closes.
- Keep the tab order the same as the reading order, even when items animate into place.

## Screen readers

- Decorative motion is hidden from assistive technology. Add `aria-hidden="true"` to decorative canvases and SVGs.
- Do not put information only in motion. A progress bar also needs text such as "62%".
- Announce results with `aria-live="polite"`, not by animating them in and expecting the user to notice.

## Auto-playing content

- Carousels pause on hover and focus, and have pause, previous and next controls.
- Loops longer than five seconds have a pause control, or they stop under reduced motion.
- Auto-advancing slides must not advance more often than once every five seconds unless the user can pause them.

## Testing

- Turn on reduced motion in the OS and in DevTools. Walk through every page. Check that movement is gone and content is visible.
- Use the keyboard only. Check that every hover effect has a focus state.
- Zoom to 200 percent. Check that animations do not cover text.
- Use a screen reader on one key flow. Check that status messages are announced once.
