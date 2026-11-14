# Quality Checklist (100 points)

Phase D audit. Score each item, then fix everything that fails before you report the work as done. The red lines in SKILL.md are mandatory; they are not included in the score. A failed red line means the work is not done, whatever the score.

| Area | Points |
|------|--------|
| 1. Spec | 15 |
| 2. Timing and easing | 15 |
| 3. Performance | 20 |
| 4. Accessibility | 25 |
| 5. Implementation | 15 |
| 6. Responsive and cross-browser | 10 |
| **Total** | **100** |

## 1. Spec (15)

- [ ] ANIMATION.md exists and has all ten sections filled in (3 points)
- [ ] Every animated element is in the choreography table (3 points)
- [ ] Each page section names its tier, L1, L2 or L3 (3 points)
- [ ] Tokens in the spec match the tokens in the code (3 points)
- [ ] Dependencies are listed with a reason for each (3 points)

## 2. Timing and easing (15)

- [ ] Every duration and easing uses a token. No magic numbers in components (4 points)
- [ ] Micro animations are 250 ms or less; entrances and route transitions are 500 ms or less (4 points)
- [ ] Exits are shorter than enters (2 points)
- [ ] Enters use the enter curve, exits use the exit curve, and linear is used only for progress, spinners and marquees (3 points)
- [ ] Stagger is 600 ms or less in total, and the stagger follows reading order (2 points)

## 3. Performance (20)

- [ ] Only `transform` and `opacity` are animated, or the exception is recorded in the spec (6 points)
- [ ] The animating-element count is within the budget (3 points)
- [ ] `will-change` is added only during animation and removed afterwards (2 points)
- [ ] DevTools Performance check at 4x CPU throttle shows no long frames during the main animations (5 points)
- [ ] Off-screen loops and pinned sections are paused or disabled (2 points)
- [ ] Mobile (under 768 px) has no pinning and no parallax (2 points)

## 4. Accessibility (25)

- [ ] Every animation has a reduced-motion fallback: movement removed, state kept (6 points)
- [ ] Reduced motion tested in the OS or DevTools on every page; content is visible (4 points)
- [ ] Loops longer than five seconds have a pause control (3 points)
- [ ] Nothing flashes more than three times per second (3 points)
- [ ] Every hover effect has a focus-visible state and a touch equivalent (3 points)
- [ ] Animated overlays do not hide the focused element; focus moves into and back out of dialogs (3 points)
- [ ] Status messages use `aria-live` or `role="status"` (3 points)

## 5. Implementation (15)

- [ ] Motion code lives in one place (tokens file plus small modules) (3 points)
- [ ] JavaScript animations are killed on unmount or route change (4 points)
- [ ] Hidden start states are set in JavaScript for GSAP, not in CSS that hides content without JavaScript (3 points)
- [ ] Transitions list their properties; no `transition: all` (3 points)
- [ ] Animations play once for entrances; they do not replay on every render (2 points)

## 6. Responsive and cross-browser (10)

- [ ] Checked at 390 px, 768 px and 1440 px. No horizontal overflow from animated elements (4 points)
- [ ] Touch devices get a clear tap state (2 points)
- [ ] Features with limited support (View Transitions, scroll-driven animations, `@starting-style`) have a fallback, checked on MDN (2 points)
- [ ] Checked in at least two browser engines, or the gap is noted in the spec (2 points)

## Scoring

- **90 to 100:** ready to ship. Note any open items in the report.
- **75 to 89:** fix the failed items before shipping.
- **Below 75:** go back to Phase B or C. Do not ship.
- Any failed red line overrides the score.

## Report format

```
Score: {{n}}/100 · Red lines: {{pass / fail list}}
Passed: {{short list}}
Failed and fixed: {{item → what was changed}}
Open: {{item → why it stays open, and who decides}}
```
