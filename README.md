<div align="center">

# Empro Labs Animation Skill

**A Claude Code skill for web motion: spec first, code second.**

[![License: MIT](https://img.shields.io/badge/License-MIT-FB923C.svg?style=flat-square)](./LICENSE)
![HTML](https://img.shields.io/badge/HTML-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)

</div>

## Install in one line

You need [Claude Code](https://claude.com/claude-code) and [Git](https://git-scm.com). Paste one line into your terminal.

**Windows (PowerShell)**

```powershell
$d = "$env:USERPROFILE\.claude\skills\empro-labs-animation-skill"; if (Test-Path "$d\.git") { git -C $d pull --ff-only } else { git clone https://github.com/aj9599995/Empro-Lab-Animation-Skill $d }
```

**Mac, Linux or Git Bash**

```bash
d="$HOME/.claude/skills/empro-labs-animation-skill"; if [ -d "$d/.git" ]; then git -C "$d" pull --ff-only; else git clone https://github.com/aj9599995/Empro-Lab-Animation-Skill "$d"; fi && echo "Installed. Type /empro-labs-animation-skill in Claude Code."
```

Then open Claude Code and type `/` in the chat box. **empro-labs-animation-skill** appears in the list. Choose it and type your request, for example `/empro-labs-animation-skill add a hover effect to the pricing cards`.

- If the command does not appear, run `/reload-skills`, or restart Claude Code.
- Works in Claude Code: the terminal CLI, the desktop app and the IDE extensions. Other chat apps do not read this folder.
- **Update:** paste the same line again. It pulls the latest version.
- **Remove:** delete the folder `~/.claude/skills/empro-labs-animation-skill` (on Windows, `%USERPROFILE%\.claude\skills\empro-labs-animation-skill`).
- **One project only:** clone the repo into that project's `.claude/skills/empro-labs-animation-skill` folder instead.

## What it does

Give the skill a reference URL, a screenshot or video, a few keywords, or your existing code. It first writes an `ANIMATION.md` motion spec: the personality, the timing tokens, what animates and why, the reduced-motion fallback for each animation, and a performance budget. After you approve the spec, it writes the animation code to match it.

The result is motion that is consistent across a site, works for people who turn off motion, and stays smooth on a phone.

## How it works

**Phase A · Understand.** Reads the input. Runs `capture_motion.py` on a reference URL or `analyze_motion.py` on existing code. Picks a personality and an interaction tier: L1 micro, L2 choreographed or L3 scroll story.

**Phase B · Write `ANIMATION.md`.** Ten sections: personality, tokens, choreography table, component motion, scroll behaviour, page transitions, performance budget, accessibility, do's and don'ts, dependencies.

**Phase C · Implement.** Tokens everywhere. Only `transform` and `opacity` are animated unless an exception is recorded. Reduced motion comes from the first version. JavaScript animations are cleaned up on unmount.

**Phase D · Audit.** Runs the static audit with `--strict`, checks reduced motion and a phone width in the browser, and works through the quality checklist.

## Repository layout

```
Empro-Lab-Animation-Skill/
├── SKILL.md                  # the skill itself (instructions for Claude)
├── README.md                 # this file
├── LICENSE                   # MIT
├── .gitignore
├── references/               # read on demand, one topic per file
│   ├── animation-md-template.md   # format of the ANIMATION.md the skill saves
│   ├── motion-principles.md       # when to animate, timing, easing
│   ├── interaction-tiers.md       # L1 micro, L2 choreographed, L3 scroll story
│   ├── motion-personalities.md    # calm, snappy, playful, cinematic
│   ├── tooling.md                 # CSS, WAAPI, GSAP, Motion, View Transitions, Lottie
│   ├── component-recipes.md       # buttons, cards, modals, drawers, toasts, loaders
│   ├── gsap-recipes.md            # timelines, ScrollTrigger, matchMedia, React cleanup
│   ├── scroll-patterns.md         # reveal, progress, sticky stack, parallax
│   ├── performance.md             # frame budget and mobile rules
│   ├── accessibility.md           # reduced motion and WCAG motion criteria
│   └── quality-checklist.md       # 100-point audit
├── scripts/                  # helpers Claude runs with Bash
│   ├── analyze_motion.py          # static audit of project code
│   └── capture_motion.py          # live capture of a reference page (Playwright)
├── templates/                # starter code for a project
│   ├── motion-tokens.css          # tokens, base keyframes, reduced-motion block
│   └── reveal.js                  # dependency-free scroll reveal
└── docs/                     # landing page for GitHub Pages (self-contained)
    ├── index.html
    ├── styles.css
    ├── app.js
    └── ANIMATION.md               # the page's own motion spec (written by the skill)
```


## Scripts

Audit the code in a project (standard library only):

```bash
python scripts/analyze_motion.py ./my-project --inventory --strict
```

Capture a live reference page (one-time setup first):

```bash
pip install playwright
python -m playwright install chromium
python scripts/capture_motion.py --url https://example.com --output ./motion-capture
```

Both scripts accept `--help`.

## Run the landing page locally

```bash
cd Empro-Lab-Animation-Skill/docs
python -m http.server 8000
```

Then open http://localhost:8000. Opening `index.html` directly with `file://` will not work, because the page uses an ES module.

## License

[MIT](./LICENSE)
