#!/usr/bin/env python3
"""
capture_motion.py - record the motion of a live web page with Playwright (Chromium).

Writes to the output folder:
  capture.json   declared transitions and animations (from computed style),
                 animations seen while the page is scrolled (Web Animations API),
                 and the animations that still run when the user prefers reduced motion
  top.png        screenshot of the first viewport

Setup, once:
  pip install playwright
  python -m playwright install chromium

Usage:
  python capture_motion.py --url https://example.com
  python capture_motion.py --url https://example.com --output ./motion-capture --scroll-steps 12
  python capture_motion.py --url https://example.com --viewport 390x844     # phone layout

Only inspect pages you are allowed to inspect. The script does not log in,
submit forms or click anything.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

try:
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Playwright is not installed. Run:\n"
          "  pip install playwright\n"
          "  python -m playwright install chromium", file=sys.stderr)
    sys.exit(2)


# Shared JavaScript helper: a short, readable selector for an element.
HELPERS_JS = """
const selectorOf = (el) => {
  if (!el || !el.tagName) return '';
  let s = el.tagName.toLowerCase();
  if (el.id) s += '#' + el.id;
  if (typeof el.className === 'string' && el.className.trim()) {
    s += '.' + el.className.trim().split(/\\s+/).slice(0, 2).join('.');
  }
  return s;
};
"""

# Every CSS transition and animation declared on an element in the body.
DECLARED_JS = HELPERS_JS + """
() => {
  const transitions = new Map();
  const animations = new Map();
  const add = (map, key, sample, extra) => {
    if (!map.has(key)) map.set(key, { ...extra, count: 0, sample });
    map.get(key).count += 1;
  };
  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el);
    const durations = cs.transitionDuration.split(',').map((s) => parseFloat(s));
    if (durations.some((d) => d > 0)) {
      const extra = {
        property: cs.transitionProperty,
        duration: cs.transitionDuration,
        easing: cs.transitionTimingFunction,
        delay: cs.transitionDelay
      };
      add(transitions, JSON.stringify(extra), selectorOf(el), extra);
    }
    if (cs.animationName !== 'none') {
      const extra = {
        name: cs.animationName,
        duration: cs.animationDuration,
        easing: cs.animationTimingFunction,
        iterations: cs.animationIterationCount,
        delay: cs.animationDelay,
        timeline: cs.animationTimeline || ''
      };
      add(animations, JSON.stringify(extra), selectorOf(el), extra);
    }
  }
  return {
    transitions: [...transitions.values()],
    animations: [...animations.values()]
  };
}
"""

# Every animation currently running on the document.
RUNNING_JS = HELPERS_JS + """
() => document.getAnimations().map((a) => {
  const effect = a.effect;
  const timing = effect && effect.getComputedTiming ? effect.getComputedTiming() : {};
  const props = new Set();
  if (effect && effect.getKeyframes) {
    for (const frame of effect.getKeyframes()) {
      Object.keys(frame).forEach((k) => {
        if (!['offset', 'easing', 'composite', 'computedOffset'].includes(k)) props.add(k);
      });
    }
  }
  return {
    kind: a.constructor.name,
    name: a.animationName || a.transitionProperty || '',
    target: effect && effect.target ? selectorOf(effect.target) : '',
    properties: [...props],
    duration: typeof timing.duration === 'number' ? Math.round(timing.duration) : String(timing.duration),
    delay: timing.delay || 0,
    easing: timing.easing || '',
    iterations: timing.iterations,
    timeline: a.timeline ? a.timeline.constructor.name : 'none',
    playState: a.playState
  };
})
"""

IDENTITY_KEYS = ("kind", "name", "target", "properties", "duration", "easing", "iterations", "timeline")


def parse_viewport(text):
    try:
        width, height = text.lower().split("x")
        return int(width), int(height)
    except ValueError:
        raise argparse.ArgumentTypeError("use WIDTHxHEIGHT, for example 1440x900")


def record_running(page, store, label):
    """Add every running animation to store, once per distinct animation."""
    for item in page.evaluate(RUNNING_JS):
        key = json.dumps({k: item[k] for k in IDENTITY_KEYS}, sort_keys=True)
        if key not in store:
            item["first_seen"] = label
            store[key] = item


def capture(url, out_dir, viewport, scroll_steps, step_wait, load_wait, timeout):
    width, height = viewport
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            # Pass 1: normal motion. Load, read declarations, then walk down the page.
            context = browser.new_context(viewport={"width": width, "height": height})
            page = context.new_page()
            page.goto(url, wait_until="load", timeout=timeout)
            page.wait_for_timeout(load_wait)

            declared = page.evaluate(DECLARED_JS)
            running = {}
            record_running(page, running, "top")
            page.screenshot(path=os.path.join(out_dir, "top.png"))

            total = page.evaluate("document.documentElement.scrollHeight")
            max_scroll = max(total - height, 0)
            for step in range(1, scroll_steps + 1):
                y = int(max_scroll * step / scroll_steps)
                page.evaluate("y => window.scrollTo(0, y)", y)
                page.wait_for_timeout(step_wait)
                record_running(page, running, f"scroll {step}/{scroll_steps}")
            context.close()

            # Pass 2: the same page with the user's reduced-motion preference.
            rm_context = browser.new_context(
                viewport={"width": width, "height": height},
                reduced_motion="reduce",
            )
            rm_page = rm_context.new_page()
            rm_page.goto(url, wait_until="load", timeout=timeout)
            rm_page.wait_for_timeout(load_wait)
            still_running = rm_page.evaluate(RUNNING_JS)
            rm_context.close()
        finally:
            browser.close()

    return {
        "url": url,
        "captured_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "viewport": {"width": width, "height": height},
        "scroll_steps": scroll_steps,
        "declared": declared,
        "running_during_scroll": list(running.values()),
        "reduced_motion": {
            "running_after_load": len(still_running),
            "still_running": still_running,
        },
        "notes": [
            "Only animations active at the sampled moments appear in running_during_scroll.",
            "Scroll-linked animations appear only while their scroll range is in view.",
            "JavaScript-driven values appear only while they run. Read the source for the rest.",
            "A non-zero reduced_motion.running_after_load is not automatically a failure: "
            "fades and colour changes may still run, and essential indicators such as spinners "
            "should stay. Check each one against ANIMATION.md.",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Record declared and running motion on a live web page.")
    parser.add_argument("--url", required=True, help="page to inspect (http or https)")
    parser.add_argument("--output", default="./motion-capture",
                        help="folder for capture.json and top.png (default: ./motion-capture)")
    parser.add_argument("--viewport", type=parse_viewport, default=(1440, 900),
                        help="WIDTHxHEIGHT (default 1440x900). Use 390x844 for a phone layout.")
    parser.add_argument("--scroll-steps", type=int, default=8,
                        help="how many scroll positions to sample (default 8)")
    parser.add_argument("--step-wait", type=int, default=700,
                        help="milliseconds to wait at each scroll position (default 700)")
    parser.add_argument("--load-wait", type=int, default=1500,
                        help="milliseconds to wait after load (default 1500)")
    parser.add_argument("--timeout", type=int, default=60000,
                        help="navigation timeout in milliseconds (default 60000)")
    args = parser.parse_args(argv)

    if not args.url.startswith(("http://", "https://")):
        parser.error("--url must start with http:// or https://")
    if args.scroll_steps < 1:
        parser.error("--scroll-steps must be at least 1")

    os.makedirs(args.output, exist_ok=True)
    try:
        result = capture(args.url, args.output, args.viewport, args.scroll_steps,
                         args.step_wait, args.load_wait, args.timeout)
    except PlaywrightError as exc:
        print(f"Capture failed: {exc}", file=sys.stderr)
        return 1

    path = os.path.join(args.output, "capture.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, ensure_ascii=False)

    print(f"Wrote {path}")
    print(f"  declared transitions: {len(result['declared']['transitions'])}")
    print(f"  declared animations:  {len(result['declared']['animations'])}")
    print(f"  running during scroll: {len(result['running_during_scroll'])}")
    print(f"  still running with reduced motion: {result['reduced_motion']['running_after_load']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
