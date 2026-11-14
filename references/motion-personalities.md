# Motion Personalities

Pick one personality for the whole page or product. Mixing them makes a product feel inconsistent. Each row maps to a token in `templates/motion-tokens.css`.

| Token | Calm (default) | Snappy | Playful | Cinematic |
|-------|----------------|--------|---------|-----------|
| `--motion-duration-instant` | 90ms | 60ms | 120ms | 120ms |
| `--motion-duration-fast` | 150ms | 100ms | 200ms | 220ms |
| `--motion-duration-base` | 240ms | 180ms | 320ms | 450ms |
| `--motion-duration-slow` | 400ms | 280ms | 480ms | 800ms |
| `--motion-duration-slower` | 600ms | 400ms | 700ms | 1200ms |
| `--motion-ease-enter` | cubic-bezier(0, 0, 0.2, 1) | cubic-bezier(0, 0, 0.2, 1) | cubic-bezier(0, 0, 0.2, 1) | cubic-bezier(0.16, 1, 0.3, 1) |
| `--motion-ease-exit` | cubic-bezier(0.4, 0, 1, 1) | cubic-bezier(0.4, 0, 1, 1) | cubic-bezier(0.4, 0, 1, 1) | cubic-bezier(0.7, 0, 0.84, 0) |
| `--motion-ease-standard` | cubic-bezier(0.2, 0, 0, 1) | cubic-bezier(0.2, 0, 0, 1) | cubic-bezier(0.3, 0, 0, 1) | cubic-bezier(0.65, 0, 0.35, 1) |
| `--motion-ease-emphasis` | cubic-bezier(0.2, 0.8, 0.2, 1) | cubic-bezier(0.2, 0.8, 0.2, 1) | cubic-bezier(0.34, 1.56, 0.64, 1) | cubic-bezier(0.16, 1, 0.3, 1) |
| `--motion-distance-sm` | 4px | 2px | 6px | 8px |
| `--motion-distance-md` | 8px | 8px | 16px | 16px |
| `--motion-distance-lg` | 16px | 16px | 40px | 80px |
| `--motion-stagger` | 60ms | 30ms | 70ms | 100ms |

## Calm (default)

- **Feel:** quiet, confident, unhurried but never slow.
- **Use for:** content sites, blogs, documentation, editorial pages, service sites, landing pages with heavy text.
- **Avoid:** overshoot, large movement, long stagger chains.

## Snappy

- **Feel:** precise, responsive, almost mechanical in its speed.
- **Use for:** dashboards, product UIs, tools people use all day, admin panels.
- **Avoid:** anything that delays the user. Keep stagger short or remove it on long lists.

## Playful

- **Feel:** friendly, bouncy, a little cheeky.
- **Use for:** consumer apps, kids' products, creative tools, onboarding and empty states.
- **Avoid:** overshoot on text, on forms, or on anything that moves often. Overshoot only on scale and translate, never on opacity.

## Cinematic

- **Feel:** slow, deliberate, dramatic. Each movement is an event.
- **Use for:** hero sections, product launches, brand stories, L3 scroll sections.
- **Avoid:** application UI. Cinematic timings feel broken when a user has to wait for a menu.

## Under reduced motion (all personalities)

- Distance tokens go to 0. Stagger goes to 0.
- Fades and colour changes keep their durations, so state still changes visibly.
- Loops stop or slow down. Parallax and pinned movement turn off.

## Choosing between two

- Content-heavy and calm → calm.
- Product UI that people repeat often → snappy.
- Friendly audience, low stakes → playful.
- One hero moment on an otherwise calm page → calm for the page, cinematic for that section only, and say so in the spec.
