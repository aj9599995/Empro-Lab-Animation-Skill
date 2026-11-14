# Motion Principles

Motion has four jobs. Every animation must do at least one of them. If it does none, remove it.

| Job | Question it answers | Example |
|-----|--------------------|---------|
| **Confirm** | Did my action work? | Button press, checkbox tick, "saved" check mark |
| **Orient** | Where did this come from, and where is it going? | A modal grows from the button that opened it; a list item slides in from its side |
| **Connect** | How are these things related? | A thumbnail grows into the detail view |
| **Delight** | Is this moment worth noticing? | Hero entrance, empty-state illustration. At most once per page. |

## Timing

| Type | Duration | Notes |
|------|----------|-------|
| Micro (hover, press, toggle) | 100 to 250 ms | Should feel instant. Never longer than 250 ms. |
| Transition (enter, exit, swap) | 200 to 400 ms | Exit is 60 to 75 percent of enter. |
| Large surface (page, drawer, hero) | 400 to 700 ms | Use sparingly. |
| Cinematic (scroll story) | 700 ms to 1.2 s | Only in L3 sections. |

- Anything longer than 1 s needs a reason written in ANIMATION.md.
- Shorter is the default. When unsure, pick the faster value.

## Easing

| Situation | Token | Why |
|-----------|-------|-----|
| Element arrives on screen | `--motion-ease-enter` (decelerate) | Starts fast and lands softly |
| Element leaves the screen | `--motion-ease-exit` (accelerate) | Leaves quickly |
| Element moves and stays on screen | `--motion-ease-standard` | Balanced |
| Progress bar, spinner, marquee, ticker | `--motion-ease-linear` | Constant speed reads as time passing |
| Playful overshoot | `--motion-ease-emphasis` | Only in the playful personality |

- Do not use `linear` for UI movement. It looks mechanical.
- Do not rely on the CSS default `ease`. Name the curve with a token.

## Distance and scale

- UI elements move 4 to 16 px. Page-level elements may move up to 32 px.
- Scale entrances from 0.95 to 0.98, never from 0. Scaling from zero looks like a glitch.
- Fade and move together. An opacity-only change is fine for small updates.

## Stagger

- Delay between items: 30 to 90 ms, depending on the personality.
- Total stagger (delay times item count) stays under 600 ms. After about eight items, reveal the rest together.
- Stagger in reading order (top to bottom, then left to right), not in DOM order if they differ.

## State, not events

- Animate when state changes, not on every render. A re-render that changes nothing must not replay the animation.
- Play entrances once. Do not replay them when the user scrolls back up, unless the spec says so.

## When not to animate

- Keyboard navigation feedback. It must be instant.
- Text input and typing.
- Numbers and tables that update often. Show the new value; do not count up to it, unless the spec asks for it.
- An action the user repeats many times. The tenth click must not wait for an animation.
- Anything the user did not trigger and does not need to see.

## Perceived speed

- A wait longer than 300 ms gets a skeleton or a progress indicator. Do not leave a blank page with a spinner in the middle.
- Show the new state at once, then animate the change. Do not hold the new state back until an animation has finished.
