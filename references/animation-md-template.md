# ANIMATION.md Template

Phase B output. Fill every section with real values before saving. The saved file must not contain placeholder text.

---

```markdown
# ANIMATION.md

> {{One sentence describing the motion, e.g. "Motion that confirms every action and never makes the user wait."}}

## 1. Motion Personality & Principles

**Personality**: {{calm / snappy / playful / cinematic}}
**Keywords**: {{4 to 6 words}}
**Page type**: {{content-heavy / showcase / app UI}}
**Tier by section**: {{e.g. Hero L3, Features L2, Footer L1}}

**Principles** (two to four, each tied to a job: confirm, orient, connect or delight):
- {{principle}}

## 2. Motion Tokens

```css
:root {
  --motion-duration-instant: {{90ms}};
  --motion-duration-fast: {{150ms}};
  --motion-duration-base: {{240ms}};
  --motion-duration-slow: {{400ms}};
  --motion-duration-slower: {{600ms}};

  --motion-ease-standard: {{cubic-bezier(0.2, 0, 0, 1)}};
  --motion-ease-enter: {{cubic-bezier(0, 0, 0.2, 1)}};
  --motion-ease-exit: {{cubic-bezier(0.4, 0, 1, 1)}};
  --motion-ease-emphasis: {{cubic-bezier(0.2, 0.8, 0.2, 1)}};
  --motion-ease-linear: linear;

  --motion-distance-sm: {{4px}};
  --motion-distance-md: {{8px}};
  --motion-distance-lg: {{16px}};
  --motion-stagger: {{60ms}};
}
```

**Token rules:**
- {{rule, e.g. "Exit durations are 60 to 75 percent of the matching enter duration."}}

## 3. Choreography Inventory

| Element | Trigger | Property | Duration | Easing | Delay | Reduced-motion fallback |
|---------|---------|----------|----------|--------|-------|-------------------------|
| {{Primary button}} | {{hover}} | {{background-color, transform}} | {{fast}} | {{standard}} | {{0}} | {{colour change only}} |
| {{Hero title}} | {{page load}} | {{opacity, transform}} | {{slower}} | {{enter}} | {{0}} | {{opacity only, fast}} |

Add one row for every animated element. An element that is not in this table does not animate.

## 4. Component Motion

### {{Component name}}
- **Default**: {{static, or what is shown}}
- **Hover / focus-visible / active**: {{what changes, which token}}
- **Enter / exit**: {{what plays, how long, how it leaves}}
- **Disabled**: {{no motion}}

Repeat for each component.

## 5. Scroll Behavior

- **Reveal**: {{threshold, once or every time, which elements}}
- **Scroll-linked or pinned**: {{section, start and end, pin count (maximum 2)}} or "None"
- **Mobile (600 px and below)**: {{what is disabled or simplified}}

## 6. Page & Route Transitions

- **Type**: {{none / fade / View Transitions API with fallback to none}}
- **Duration**: {{token name}}
- **Shared elements**: {{list, or "none"}}

## 7. Performance Budget

- **Animated properties**: {{transform, opacity}}
- **Exceptions** (property, element, reason): {{or "none"}}
- **Maximum simultaneously animating elements**: {{e.g. 12}}
- **Infinite loops**: {{list with pause control, or "none"}}
- **Target**: {{60 fps on a mid-range phone with a 4x CPU slowdown}}

## 8. Accessibility

- **Reduced motion**: {{movement removed, state changes kept, fades unchanged}}
- **Flashing**: {{none above three flashes per second}}
- **Auto-playing content longer than 5 s**: {{pause control, or "none"}}
- **Keyboard and focus**: {{a focus-visible state on every hover effect}}

## 9. Do's and Don'ts

**Do's** (at least four):
- {{do}}

**Don'ts** (at least five):
- {{don't}}

## 10. Dependencies

| Package | Version | Why | Tier |
|---------|---------|-----|------|
| {{gsap}} | {{3.x}} | {{ScrollTrigger for the pinned section}} | {{L3}} |

**No dependency**: {{say so if none are needed}}
```
