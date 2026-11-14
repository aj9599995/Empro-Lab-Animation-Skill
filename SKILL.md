---
name: empro-labs-animation-skill
argument-hint: "[what should move, and where, or a reference URL]"
description: Designs and builds web UI motion (micro-interactions, component and page transitions, loaders, scroll reveals and scroll-linked effects) in CSS, the Web Animations API or GSAP. Spec first - writes an ANIMATION.md motion spec, gets the user's approval, then generates animation code that respects prefers-reduced-motion and a performance budget. Use when the user asks for animations, motion, transitions, hover or click effects, scroll animations, loaders, or says "make this feel smooth", "make it feel alive" or "add motion to this page". Not for video rendering, 3D engines or backend logic.
---

# Empro Labs Animation Skill

Web motion design skill. Two steps: **write the motion spec (ANIMATION.md) first, then write the code.**

ANIMATION.md is a file saved in the project. It can be edited by hand, reused in other projects, and read by other tools.

Paths in this file are relative to the skill folder (`~/.claude/skills/empro-labs-animation-skill/`). Use absolute paths when you run the scripts.

## Request

The user's request from the slash command:

$ARGUMENTS

If the request above is empty, ask one question: what should move, and where? Then start Phase A.

## Core flow

```
Phase A  Understand the input  ──→  Phase B  Write ANIMATION.md (user approves)  ──→  Phase C  Implement  ──→  Phase D  Audit
```

## Startup checks (in this order)

1. Does the project have `ANIMATION.md`? → Reuse it, edit it or rebuild it, as the user asks.
2. Does it have `DESIGN.md` (from the web-design skill)? → Inherit its colours, fonts and style direction. Keep the motion consistent with it.
3. Does it have motion tokens (`--motion-*` variables or a motion file)? → Reuse them. Do not invent new values.
4. Does it already have animation code? → Run `python scripts/analyze_motion.py <project> --inventory` first, so you know what exists before you propose changes.
5. None of the above → Phase A.

## Phase A: Understand

Inputs can be combined:

| Input | What to do |
|-------|-----------|
| Reference URL | Run `python scripts/capture_motion.py --url [URL] --output ./motion-capture`. Read `capture.json` for real durations, easings, animated properties and scroll-linked effects. Use `top.png` for mood. |
| Video or screenshot of the motion | Describe the trigger, the approximate duration and the easing feel. Confirm the numbers with the user. |
| Keywords ("snappy", "cinematic") | Match them to a personality in `references/motion-personalities.md`. |
| Brand name ("like Linear") | Capture the live site if it is reachable. If not, ask for a reference URL. Do not guess motion from memory of a brand. |
| Existing code | Run the inventory script and keep what works. |

### A1. Personality (ask at most two questions)

- **Feel:** calm, snappy, playful or cinematic?
- **Page type:** content-heavy (motion stays out of the way) or showcase (motion can lead)?

Show one or two candidates from `references/motion-personalities.md`, each with a one-line reason. The user confirms.

### A2. Interaction tier (required, do not skip)

See `references/interaction-tiers.md`.

| Tier | Experience | Tooling |
|------|-----------|---------|
| **L1 Micro** | Hover, focus, press, toggles, small state changes | CSS transitions only |
| **L2 Choreographed** | Enter and exit, staggered lists, modals, drawers, route changes, loaders | CSS keyframes, Web Animations API or a GSAP timeline |
| **L3 Scroll story** | Scroll-linked reveals, pinning, parallax, sections driven by a timeline | GSAP + ScrollTrigger, or CSS scroll-driven animations with a fallback |

L3 is capped at two pinned sections per page. Each page section states its tier in the spec.

### A3. Stack

Check `package.json` and the framework (plain HTML, React, Vue, Svelte, Next.js). Choose tooling with `references/tooling.md`. Default: CSS and the Web Animations API. Add GSAP only for L3 or complex timelines.

## Phase B: Write ANIMATION.md

Follow `references/animation-md-template.md`. Ten sections:

1. Motion Personality & Principles
2. Motion Tokens (durations, easings, distances)
3. Choreography Inventory (table: element, trigger, property, duration, easing, delay, reduced-motion fallback)
4. Component Motion (default, hover, focus-visible, active, disabled, enter, exit)
5. Scroll Behavior
6. Page & Route Transitions
7. Performance Budget
8. Accessibility
9. Do's and Don'ts (at least 8 items, at least 5 of them Don'ts)
10. Dependencies

Show a summary to the user and wait for approval. Then save `ANIMATION.md` in the project root.

## Phase C: Implement

1. **Tokens everywhere.** Every duration and easing is a variable, such as `var(--motion-duration-base)`. No magic numbers inside components.
2. **Animate only cheap properties.** `transform` and `opacity` first. `clip-path` and `filter` are allowed on small elements. Never animate `width`, `height`, `top`, `left`, `margin` or `padding` unless ANIMATION.md records an exception with a reason.
3. **Reduced motion is part of the first version, not a later patch.** Movement is removed and state changes stay. The distance tokens go to zero under reduced motion, and the `prefers-reduced-motion` block in `templates/motion-tokens.css` shows the pattern.
4. **Use the starter files** when the project has no motion layer yet: `templates/motion-tokens.css` and `templates/reveal.js`.
5. **Loops need a way out.** Any `infinite` animation stops or simplifies under reduced motion. Any loop that runs longer than five seconds gets a pause control.
6. **Clean up JavaScript.** Kill GSAP timelines and ScrollTriggers on unmount (use `gsap.context()` or `useGSAP`). Disconnect observers and remove listeners.
7. **Keep motion in one place.** Put tokens in one file and recipes in small modules. Do not scatter timing values across components.

## Phase D: Audit

1. Run the static audit: `python scripts/analyze_motion.py <project> --strict`. Fix every error. Review every warning and either fix it or justify it in ANIMATION.md.
2. Run the browser checks:
   - Turn on reduced motion (DevTools → Rendering → `prefers-reduced-motion: reduce`). Confirm no movement remains and content is still visible.
   - Throttle the CPU (4×) and record the Performance panel while the motion plays. Look for long frames.
   - Check a phone width (390 px). Look for horizontal overflow from animated elements.
3. Work through `references/quality-checklist.md`.
4. Report what passed, what failed and what you fixed.

## Red lines (every item must pass)

- Every animation in ANIMATION.md has a reduced-motion fallback.
- Only `transform`, `opacity` and recorded exceptions are animated.
- All durations and easings come from tokens.
- Every `infinite` loop respects reduced motion, and any loop longer than five seconds has a pause control.
- Nothing flashes more than three times per second.
- Interactive feedback appears within 100 ms. Micro animations are 250 ms or less. Entrance and route transitions are 500 ms or less.
- Hover-only feedback has a keyboard focus state and a touch equivalent.
- At widths of 600 px or less, no animated element causes horizontal scroll, and pinned sections are disabled or simplified.
- JavaScript animations are cleaned up on unmount.

## Reference index

Read only the files the current phase needs. Do not load them all.

| File | Contents | Read when |
|------|----------|-----------|
| `references/animation-md-template.md` | ANIMATION.md output template (10 sections) | Phase B |
| `references/motion-principles.md` | Why and when to animate, timing and easing rules | Phase A and B |
| `references/interaction-tiers.md` | L1, L2 and L3 tier definitions with code patterns | Phase A2 and B |
| `references/motion-personalities.md` | Four personality presets with token values | Phase A1 and B |
| `references/tooling.md` | CSS vs WAAPI vs GSAP vs Motion vs View Transitions vs Lottie | Phase A3 |
| `references/component-recipes.md` | Button, card, accordion, modal, drawer, toast, tabs, loaders | Phase C |
| `references/gsap-recipes.md` | GSAP timelines, ScrollTrigger, matchMedia, React cleanup | Phase C (GSAP only) |
| `references/scroll-patterns.md` | Reveal, progress bar, sticky stack, parallax, horizontal scroll | Phase B (scroll) and C |
| `references/performance.md` | Frame budget, compositor-friendly rules, mobile downgrade | Phase B and D |
| `references/accessibility.md` | Reduced motion, WCAG motion criteria, vestibular triggers | Phase B and D |
| `references/quality-checklist.md` | 100-point audit checklist | Phase D |

## Scripts

| Script | Use | Needs |
|--------|-----|-------|
| `scripts/analyze_motion.py` | Static audit of a project's CSS and JS. Finds layout animation, `transition: all`, infinite loops, long durations and missing reduced-motion handling. `--inventory` lists the existing timing values. | Python 3 (standard library only) |
| `scripts/capture_motion.py` | Records declared and running animations on a live URL, scrolls the page and checks what still runs with reduced motion. Writes `capture.json` and `top.png`. | Python 3, `pip install playwright`, `python -m playwright install chromium` |

Both scripts accept `--help`.

## Templates

| File | Use |
|------|-----|
| `templates/motion-tokens.css` | Token variables, base keyframes, reveal rules and the reduced-motion block. Copy into the project. |
| `templates/reveal.js` | Dependency-free scroll reveal with IntersectionObserver that respects reduced motion. |

## Language

Write ANIMATION.md and the summaries in the user's language. Keep CSS, JavaScript and token names in English.

## Fallback chain

- Capture script fails (no Playwright, or the site blocks the browser) → ask for a screenshot or a short screen recording and build from that description.
- The reference uses an animation library you cannot identify → say so and ask whether to match the feel or the exact motion.
- No input at all → ask one question about the feel, then use the calm personality.
