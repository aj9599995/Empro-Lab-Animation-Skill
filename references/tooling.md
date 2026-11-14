# Tooling

Use the smallest tool that does the job. Each step up adds weight, a dependency and something to maintain.

| Need | Use | Why |
|------|-----|-----|
| Hover, focus, press, toggle | CSS `transition` | No JavaScript, no weight. Adjust it with a media query for reduced motion. |
| One-shot entrance, looping shimmer or spinner | CSS `@keyframes` | Runs on the compositor when it animates only `transform` or `opacity`. |
| JavaScript-triggered motion you must control (pause, reverse, await) | Web Animations API (`element.animate`) | Built into the browser. `.finished` is a promise. |
| Exit before removal | WAAPI with `await anim.finished` | Keeps the DOM in step with the animation. |
| Multi-step sequence, timeline, stagger across many elements | GSAP timeline | Timeline control and reliable stagger. |
| Scroll-linked, pinned or scrubbed sections | GSAP with ScrollTrigger | Mature. Handles resize and refresh. |
| Simple scroll-linked progress or reveal, no library | CSS scroll-driven animations (`animation-timeline: view()` or `scroll()`) | No JavaScript. Check support and always add a fallback. |
| Layout animation in React (elements that change size or position) | `motion` package (formerly Framer Motion) | Handles layout transitions and exit animations in React components. |
| Page or route transitions | View Transitions API (`document.startViewTransition`) | Native transitions between states. Check support; fall back to no transition. |
| Designer-made icon or illustration animation | Lottie (JSON) or Rive (state machines) | The designer owns the motion. Check file size and the cost on phones. |

## Rules

- **Check the project first.** Read `package.json` and use what is already installed before adding anything.
- **GSAP is for L3 and real timelines.** Do not add it for hover effects that CSS handles.
- **One library per job.** Do not ship two animation libraries that both do scroll reveals.
- **Check browser support** on MDN before you rely on View Transitions or scroll-driven animations. Always write the fallback.
- **Lottie and Rive:** lazy-load them. As a rule of thumb, keep a single file under 200 KB, and keep the file out of the first render.
- **Record the choice.** Name every new dependency, its version and its reason in the Dependencies section of ANIMATION.md.
