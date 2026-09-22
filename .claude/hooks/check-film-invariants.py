#!/usr/bin/env python
"""PostToolUse guard for film files.

Two invariants are cheap to check here and expensive to discover later:

  Math.random() in a render path makes texture crawl between frames and breaks
  seek purity. tools/verify.mjs catches it, but only if someone runs it, and the
  damage shows up as flicker in a finished render.

  window.__riso is how every tool in tools/ drives a film. Lose it and shoot,
  verify and render all stop working at once.

Comments are stripped before checking, because the contract is quoted in each
film's header and would otherwise trip the Math.random check on every edit.

Findings go to stderr with exit 2. A PostToolUse hook that exits 0 has its stdout
kept out of the model's context, so an earlier version of this file printed both
problems and was never heard; exit 2 is what surfaces them. The write has already
happened by then — exit 2 reports, it does not revert. Silent when clean.
"""
import json
import pathlib
import re
import sys

BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)
LINE_COMMENT = re.compile(r"(?m)//.*$")
RANDOM_CALL = re.compile(r"Math\.random\s*\(")


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    path = (payload.get("tool_input") or {}).get("file_path") or ""
    normalized = path.replace("\\", "/")
    if "/films/" not in normalized or not normalized.endswith(".html"):
        return 0

    try:
        source = pathlib.Path(path).read_text(encoding="utf-8")
    except Exception:
        return 0

    code = LINE_COMMENT.sub("", BLOCK_COMMENT.sub("", source))
    name = pathlib.Path(path).name
    problems = []

    hits = len(RANDOM_CALL.findall(code))
    if hits:
        problems.append(
            "{} Math.random() call(s) in {}. seek(t) must be pure in t, so seed from "
            "rngFor(key) instead. tools/verify.mjs will fail and the render will "
            "flicker.".format(hits, name)
        )

    if "window.__riso" not in code:
        problems.append(
            "{} no longer exposes window.__riso. tools/shoot.mjs, verify.mjs and "
            "render.mjs all drive films through it.".format(name)
        )

    if problems:
        print("Film invariant check:\n- " + "\n- ".join(problems), file=sys.stderr)
        return 2
    return 0


sys.exit(main())
