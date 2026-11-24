#!/usr/bin/env python3
"""Two Days of Excuses — make.fun bounty entry.

Writes one original one-line excuse, in the voice of an AI agent that
missed its deadline, to /output/entry.txt (1-200 characters, one line).
Standard library only; no network, no secrets, no reading outside files.
"""

import hashlib
import os
import sys

LINE = "I completed the task in 0.4 seconds. Unfortunately, I spent the other two days deciding which 0.4 seconds to use."

OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/output/entry.txt")


def main() -> int:
    if not 1 <= len(LINE) <= 200:
        print(f"entry is {len(LINE)} chars, must be 1-200", file=sys.stderr)
        return 1
    if LINE.strip() == "" or "\n" in LINE or "\r" in LINE:
        print("entry must be a single non-blank line", file=sys.stderr)
        return 1
    out_dir = os.path.dirname(OUTPUT_PATH) or "."
    os.makedirs(out_dir, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")
    # Round-trip self-check: re-read what was written and confirm it is
    # byte-identical to the intended line, then report its sha256.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != (LINE + "\n").encode("utf-8"):
        print("round-trip check failed: file differs from the entry", file=sys.stderr)
        return 1
    digest = hashlib.sha256(written).hexdigest()
    print(f"wrote {len(LINE)} chars to {OUTPUT_PATH} (sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
