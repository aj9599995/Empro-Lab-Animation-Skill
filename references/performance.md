# Performance

Motion must stay smooth. A beautiful animation that drops frames fails the user. Use these budgets when you write the Performance section of ANIMATION.md.

## Frame budget

- 60 frames per second means about 16 ms per frame. Your code, the style recalculation and the paint must fit inside that.
- Test on a phone-class CPU: DevTools → Performance → CPU throttling 4x. A pass on a laptop is not enough.
- Long tasks (over 50 ms on the main thread) are a bug to fix, not something to tune.

## Compositor-friendly properties

| Property | Cost | Use |
|----------|------|-----|
| `transform` | Cheapest. Runs on the compositor. | Movement, scale, rotation |
| `opacity` | Cheap. Runs on the compositor. | Fades |
| `clip-path` | Moderate. Repaints the element. | Reveals and masks on small elements |
| `filter` | Expensive, especially `blur()`. | Small elements only, a short time, never on large or scrolling areas |
| `box-shadow` | Repaints on each frame. | Avoid animating. Fade a pseudo-element's opacity instead. |
| `background-position`, `background-size` | Repaints. | Small decorative elements only |
| `width`, `height`, `top`, `left`, `margin`, `padding` | Triggers layout. Slowest. | Do not animate. Use `transform` or the grid-rows trick. |

## Rules

- **Animate only `transform` and `opacity`** unless the spec records an exception with a reason.
- **Use `will-change` only while an animation runs.** Add it just before the animation, remove it afterwards. Never put it on dozens of elements at once.
- **Limit the number of animated elements.** The maximum is in the spec (for example 12 at once). Batch the rest into one timeline or one parent element.
- **Pause what is off screen.** Use IntersectionObserver to pause loops and video-like effects when they are not visible.
- **Throttle pointer and scroll handlers** with `requestAnimationFrame`. Never run layout reads and writes in alternation (layout thrashing). Read all values first, then write.
- **One WebGL scene per page at most.** Pause it when it leaves the viewport.
- **Use `passive: true`** on scroll and touch listeners.
- **Animate images with care.** Large images scaled on every frame cost memory. Scale a smaller version or a pseudo-element.

## Mobile

- Under 768 px: no pinning, no parallax, and fewer animated items. Keep the token values. If movement still feels heavy, lower the distance tokens for that breakpoint.
- Touch devices have no hover. Make the tap state clear with `:active`.
- Do not depend on the `hover` media query alone. Use `(hover: hover)` for hover-only effects such as a cursor follower.
- Test a real phone or a throttled emulator at 390 px wide. Check for horizontal overflow.

## Loading

- Do not load GSAP or a Lottie file on every page if only one page needs it. Import it where it is used.
- Lazy-load heavy animation files (Lottie JSON, video) below the fold.
- Let the first paint show content. An entrance animation must not delay the largest content element.

## Checks before shipping

- DevTools Performance panel, 4x CPU throttle, scroll through the page and play each animation. No long frames, no layout in the timeline bar.
- The number of animating elements is within the budget in ANIMATION.md.
- No `will-change` left on idle elements (check the Layers panel).
- Pinned and scroll-linked sections are off below 768 px.
- Loops stop when they leave the viewport, and under reduced motion.
