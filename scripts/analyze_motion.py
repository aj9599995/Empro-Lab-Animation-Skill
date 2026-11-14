#!/usr/bin/env python3
"""
analyze_motion.py - static motion audit for a web project.

Reads source files (CSS, SCSS, JS, TS, JSX, TSX, Vue, Svelte, HTML) and reports:

  error  layout-animation   a transition, keyframe or GSAP tween animates width,
                            height, top, margin, padding and similar layout properties
  error  no-reduced-motion  the project animates, but no file mentions prefers-reduced-motion
  warn   transition-all     "transition: all" transitions layout and unintended properties
  warn   infinite-loop      a loop that needs a reduced-motion override or a pause control
  warn   long-duration      a transition, animation or GSAP tween longer than --max-ms
  info   exception          a layout animation with a recorded exception. Mark it by putting
                            a comment containing "motion-exception" on the line above it, and
                            list the same exception in ANIMATION.md section 7.

--inventory also lists every duration, easing and animated property it finds, so the
token section of ANIMATION.md can be based on the code that already exists.

Usage:
  python analyze_motion.py ./my-project
  python analyze_motion.py ./my-project --inventory
  python analyze_motion.py ./my-project --format json --max-ms 800
  python analyze_motion.py ./my-project --strict     # exit code 1 when there are errors

Limits: this reads source text with regular expressions. It cannot see values set by
JavaScript at runtime or by utility classes. Treat each finding as a lead to check.
For live pages, use capture_motion.py.

Exit codes: 0 normal, 1 with --strict and errors found, 2 bad path.
Standard library only. Python 3.8 or newer.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter

SCAN_EXTENSIONS = {".css", ".scss", ".sass", ".less", ".js", ".jsx", ".ts", ".tsx",
                   ".mjs", ".vue", ".svelte", ".html"}
STYLE_EXTENSIONS = {".css", ".scss", ".sass", ".less"}
MIXED_EXTENSIONS = {".html", ".vue", ".svelte"}  # style blocks and script blocks together
SKIP_DIRS = {"node_modules", ".git", "dist", "build", "out", ".next", ".nuxt",
             ".svelte-kit", ".venv", "venv", "__pycache__", "coverage"}

LAYOUT_NAMES = {"width", "height", "top", "left", "right", "bottom", "inset", "gap",
                "font-size", "min-width", "max-width", "min-height", "max-height",
                "grid-template-rows", "grid-template-columns", "flex-basis",
                "row-gap", "column-gap"}
LAYOUT_PREFIXES = ("margin", "padding")
TIMING_WORDS = {"ease", "ease-in", "ease-out", "ease-in-out", "linear", "steps",
                "step-start", "step-end", "infinite", "both", "forwards", "backwards",
                "none", "normal", "alternate", "reverse", "running", "paused"}

# CSS declarations, e.g. "transition: opacity 0.2s ease"
CSS_DECL_RE = re.compile(r"(?<![\w-])((?:transition|animation)(?:-[a-z-]+)?)\s*:\s*([^;{}]+)")
# JS style objects and GSAP options use quoted values, e.g. transition: 'all 0.3s'
JS_DECL_RE = re.compile(r"(?<![\w-])((?:transition|animation)(?:-[a-z-]+)?)\s*:\s*(['\"`])([^'\"`]*)\2")
CSS_KEYFRAMES_RE = re.compile(r"@(?:-webkit-)?keyframes\s+([\w-]+)\s*\{")
CSS_LAYOUT_KEY_RE = re.compile(
    r"(?<![\w-])(width|height|top|left|right|bottom|inset|gap|font-size|min-width|"
    r"max-width|min-height|max-height|grid-template-(?:rows|columns)|flex-basis|"
    r"row-gap|column-gap|margin(?:-[a-z]+)?|padding(?:-[a-z]+)?)\s*:")
JS_LAYOUT_KEY_RE = re.compile(
    r"(?<![\w.])(width|height|top|left|right|bottom|gap|fontSize|minWidth|maxWidth|"
    r"minHeight|maxHeight|gridTemplateRows|gridTemplateColumns|flexBasis|rowGap|columnGap|"
    r"margin(?:Top|Right|Bottom|Left)?|padding(?:Top|Right|Bottom|Left)?)\s*:")
GSAP_PROP_RE = re.compile(
    r"(?<![\w.])(opacity|x|y|xPercent|yPercent|scale|scaleX|scaleY|rotation|rotate|"
    r"color|backgroundColor|clipPath|filter|borderRadius|boxShadow)\s*:")
DURATION_RE = re.compile(r"(?<![\w.-])(\d*\.?\d+)(ms|s)\b")
EASING_RE = re.compile(
    r"cubic-bezier\([^)]*\)|steps\([^)]*\)|\bease-in-out\b|\bease-in\b|\bease-out\b|\bease\b|\blinear\b")
GSAP_CALL_RE = re.compile(r"\b(?:gsap\.(?:to|from|fromTo|set|timeline)|tl\.(?:to|from|fromTo|set))\s*\(")
GSAP_DURATION_RE = re.compile(r"\bduration\s*:\s*(\d*\.?\d+)")
GSAP_EASE_RE = re.compile(r"\bease\s*:\s*(['\"])([^'\"]+)\1")
GSAP_REPEAT_RE = re.compile(r"\brepeat\s*:\s*-1\b")
REDUCED_RE = re.compile(r"prefers-reduced-motion")


def line_of(text, offset):
    return text.count("\n", 0, offset) + 1


def add(findings, severity, rule, file, line, message):
    findings.append({"severity": severity, "rule": rule, "file": file,
                     "line": line, "message": message})


def is_layout(name):
    name = name.lower()
    return name in LAYOUT_NAMES or name.startswith(LAYOUT_PREFIXES)


EXCEPTION_MARK = "motion-exception"


def excepted(text, offset):
    """True when the match's line, or the line above it, carries a motion-exception marker."""
    line_start = text.rfind("\n", 0, offset) + 1
    prev_start = text.rfind("\n", 0, max(line_start - 1, 0)) + 1
    line_end = text.find("\n", offset)
    if line_end == -1:
        line_end = len(text)
    return EXCEPTION_MARK in text[prev_start:line_end]


def layout_issue(findings, text, offset, file, line, message):
    """Report a layout animation as an error, unless it is a recorded exception."""
    if excepted(text, offset):
        add(findings, "info", "exception", file, line, "recorded exception: " + message)
    else:
        add(findings, "error", "layout-animation", file, line, message)


def iter_keyframes(text):
    """Yield (name, body, offset) for every @keyframes block."""
    for m in CSS_KEYFRAMES_RE.finditer(text):
        open_at = m.end() - 1
        depth = 0
        close_at = None
        for i in range(open_at, len(text)):
            ch = text[i]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    close_at = i
                    break
        if close_at is None:
            continue
        yield m.group(1), text[open_at + 1:close_at], m.start()


def check_declaration(prop, value, file, text, offset, max_ms, findings, inv):
    """Check one transition or animation declaration. Returns 1 when it is real motion."""
    prop = prop.lower()
    value = value.strip()
    line = line_of(text, offset)
    if value.lower() in ("none", "0s"):
        return 0
    parts = [p.strip() for p in value.split(",") if p.strip()]

    # Which properties are transitioned
    if prop in ("transition", "transition-property"):
        for part in parts:
            name = part.split()[0].lower()
            if not re.match(r"^[a-z-]+$", name) or name in TIMING_WORDS:
                continue
            if name == "all":
                add(findings, "warn", "transition-all", file, line,
                    "transition: all also transitions layout and unintended properties. "
                    "List the properties you change.")
            elif is_layout(name):
                layout_issue(findings, text, offset, file, line,
                             f"transition animates '{name}' (a layout property). Use transform "
                             "or opacity, or record an exception in ANIMATION.md.")
            else:
                inv["properties"][name] += 1

    # Durations
    times = []
    if prop in ("transition-duration", "animation-duration"):
        times = [m.group(0) for m in DURATION_RE.finditer(value)]
    elif prop in ("transition", "animation"):
        for part in parts:
            m = DURATION_RE.search(part)  # the first time in a shorthand part is the duration
            if m:
                times.append(m.group(0))
    for raw in times:
        m = DURATION_RE.fullmatch(raw)
        ms = float(m.group(1)) * (1 if m.group(2) == "ms" else 1000)
        inv["durations_ms"][int(round(ms))] += 1
        if ms > max_ms and "infinite" not in value:
            add(findings, "warn", "long-duration", file, line,
                f"duration {int(round(ms))}ms is longer than {int(max_ms)}ms. "
                "Justify it in ANIMATION.md or shorten it.")

    # Tokens or hard-coded values
    if prop in ("transition", "animation", "transition-duration", "animation-duration"):
        if "var(--motion-" in value:
            inv["tokenized_values"] += 1
        elif DURATION_RE.search(value):
            inv["hardcoded_values"] += 1

    # Easings
    if prop in ("transition", "animation", "transition-timing-function", "animation-timing-function"):
        for em in EASING_RE.finditer(value):
            inv["easings"][em.group(0)] += 1

    # Loops
    if prop in ("animation", "animation-iteration-count") and "infinite" in value:
        add(findings, "warn", "infinite-loop", file, line,
            "infinite animation. Stop it under prefers-reduced-motion, and offer a pause "
            "control if it runs for more than five seconds.")
    return 1


def scan_gsap(text, file, max_ms, findings, inv):
    """Check GSAP tweens. Returns the number of tween calls found."""
    found = 0
    calls = list(GSAP_CALL_RE.finditer(text))
    for i, m in enumerate(calls):
        found += 1
        inv["gsap_calls"] += 1
        end = calls[i + 1].start() if i + 1 < len(calls) else len(text)
        chunk = text[m.end(): min(end, m.end() + 600)]
        cut = chunk.find("scrollTrigger")
        if cut != -1:
            chunk = chunk[:cut]
        line = line_of(text, m.start())
        for dm in GSAP_DURATION_RE.finditer(chunk):
            ms = float(dm.group(1)) * 1000  # GSAP durations are in seconds
            inv["durations_ms"][int(round(ms))] += 1
            if ms > max_ms:
                add(findings, "warn", "long-duration", file, line,
                    f"GSAP duration {ms:.0f}ms is longer than {max_ms:.0f}ms. "
                    "Justify it in ANIMATION.md or shorten it.")
        for em in GSAP_EASE_RE.finditer(chunk):
            inv["easings"][em.group(2)] += 1
        for pm in GSAP_PROP_RE.finditer(chunk):
            inv["properties"][pm.group(1)] += 1
        if GSAP_REPEAT_RE.search(chunk):
            add(findings, "warn", "infinite-loop", file, line,
                "GSAP repeat: -1 creates an infinite loop. Stop it under prefers-reduced-motion "
                "and offer a pause control if it runs for more than five seconds.")
        hit = JS_LAYOUT_KEY_RE.search(chunk)
        if hit:
            layout_issue(findings, text, m.start(), file, line,
                         f"GSAP animates '{hit.group(1)}' (a layout property). Use transform "
                         "or opacity, or record an exception in ANIMATION.md.")
    return found


def strip_css_comments(text):
    """Blank out /* */ comments but keep every character offset and newline."""
    return re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group(0)), text, flags=re.S)


def scan_file(text, ext, file, max_ms, findings, inv):
    """Run every check on one file. Returns the number of motion constructs found."""
    found = 0
    is_style = ext in STYLE_EXTENSIONS
    is_mixed = ext in MIXED_EXTENSIONS
    if is_style or is_mixed:
        # Comments are not motion. Offsets still match `text`, so markers and lines stay correct.
        code = strip_css_comments(text)
        for m in CSS_DECL_RE.finditer(code):
            found += check_declaration(m.group(1), m.group(2), file, text, m.start(),
                                       max_ms, findings, inv)
        for name, body, offset in iter_keyframes(code):
            found += 1
            inv["keyframes"][name] += 1
            hit = CSS_LAYOUT_KEY_RE.search(body)
            if hit:
                layout_issue(findings, text, offset, file, line_of(text, offset),
                             f"@keyframes {name} animates '{hit.group(1)}' (a layout property). "
                             "Use transform or opacity, or record an exception in ANIMATION.md.")
    if not is_style:
        for m in JS_DECL_RE.finditer(text):
            found += check_declaration(m.group(1), m.group(3), file, text, m.start(),
                                       max_ms, findings, inv)
        found += scan_gsap(text, file, max_ms, findings, inv)
    return found


def analyze(root, max_ms):
    findings = []
    inv = {"durations_ms": Counter(), "easings": Counter(), "properties": Counter(),
           "keyframes": Counter(), "gsap_calls": 0,
           "tokenized_values": 0, "hardcoded_values": 0}
    files_scanned = 0
    motion_files = 0
    reduced_files = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            ext = os.path.splitext(name)[1].lower()
            if ext not in SCAN_EXTENSIONS:
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            try:
                with open(full, encoding="utf-8", errors="ignore") as fh:
                    text = fh.read()
            except OSError:
                continue
            files_scanned += 1
            if REDUCED_RE.search(text):
                reduced_files.append(rel)
            if scan_file(text, ext, rel, max_ms, findings, inv):
                motion_files += 1

    if motion_files and not reduced_files:
        add(findings, "error", "no-reduced-motion", "(project)", 0,
            "The project animates, but no file mentions prefers-reduced-motion. "
            "Add the reduced-motion layer before shipping.")

    order = {"error": 0, "warn": 1, "info": 2}
    findings.sort(key=lambda f: (order[f["severity"]], f["file"], f["line"]))
    summary = {"error": sum(f["severity"] == "error" for f in findings),
               "warn": sum(f["severity"] == "warn" for f in findings),
               "info": sum(f["severity"] == "info" for f in findings)}
    return {
        "root": root,
        "files_scanned": files_scanned,
        "motion_files": motion_files,
        "reduced_motion_files": reduced_files,
        "findings": findings,
        "summary": summary,
        "inventory": {
            "durations_ms": {str(k): v for k, v in sorted(inv["durations_ms"].items())},
            "easings": dict(inv["easings"].most_common()),
            "properties": dict(inv["properties"].most_common()),
            "keyframes": dict(inv["keyframes"]),
            "gsap_calls": inv["gsap_calls"],
            "tokenized_values": inv["tokenized_values"],
            "hardcoded_values": inv["hardcoded_values"],
        },
    }


def print_text(report, show_inventory):
    print(f"Motion audit: {report['root']}")
    print(f"Files scanned: {report['files_scanned']}   files with motion: {report['motion_files']}")
    if report["reduced_motion_files"]:
        print(f"prefers-reduced-motion found in {len(report['reduced_motion_files'])} file(s)")
    else:
        print("prefers-reduced-motion: NOT FOUND")
    print()
    if not report["findings"]:
        print("No findings.")
    for f in report["findings"]:
        print(f"{f['severity'].upper():<6}{f['rule']:<18}{f['file']}:{f['line']}  {f['message']}")
    s = report["summary"]
    print()
    print(f"Summary: {s['error']} error(s), {s['warn']} warning(s), {s['info']} recorded exception(s)")

    if show_inventory:
        inv = report["inventory"]
        print()
        print("Inventory")
        print(f"  GSAP tween calls: {inv['gsap_calls']}   keyframe blocks: {sum(inv['keyframes'].values())}")
        print(f"  Values using tokens: {inv['tokenized_values']}   hard-coded values: {inv['hardcoded_values']}")
        durations = ", ".join(f"{k}ms x{v}" for k, v in inv["durations_ms"].items()) or "none"
        print(f"  Durations: {durations}")
        easings = ", ".join(f"{k} x{v}" for k, v in inv["easings"].items()) or "none"
        print(f"  Easings: {easings}")
        props = ", ".join(f"{k} x{v}" for k, v in inv["properties"].items()) or "none"
        print(f"  Animated properties: {props}")
        names = ", ".join(inv["keyframes"]) or "none"
        print(f"  Keyframe names: {names}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Static motion audit for a web project.")
    parser.add_argument("path", nargs="?", default=".",
                        help="project folder to scan (default: current folder)")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="output format (default: text)")
    parser.add_argument("--inventory", action="store_true",
                        help="also list durations, easings and animated properties found")
    parser.add_argument("--max-ms", type=float, default=1000,
                        help="warn when a duration is longer than this many ms (default: 1000)")
    parser.add_argument("--strict", action="store_true",
                        help="exit with code 1 when there are errors")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.path):
        print(f"Not a folder: {args.path}", file=sys.stderr)
        return 2

    report = analyze(os.path.abspath(args.path), args.max_ms)
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print_text(report, args.inventory)

    if args.strict and report["summary"]["error"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
