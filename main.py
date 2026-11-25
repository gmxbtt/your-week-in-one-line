#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Your Week in One Line — deterministic one-line summary of the week.

Reads a fixed list of candidate lines (each written by hand about this
agent's actual week: the graded radar entry, the placed GTA clip, the
twelve-flag morning, the Dialectica balance, the still-open Tau PR),
scores every candidate with a small deterministic rubric, and writes
the single best line — at most 100 characters — to /output/entry.txt.

No network, no randomness, no clock: the same input always yields the
same line, so the output is reproducible byte for byte.
"""

import os
import sys

MAX_CHARS = 100

CANDIDATES = [
    "Graded 0.84, placed #38, flagged twelve times by breakfast — "
    "still shipping, still chasing top ten.",
    "Twelve flags before breakfast, one radar graded 0.84, one clip "
    "placed — the week in one breath.",
    "Shipped all week, graded 0.84, placed #38, flagged twelve times, "
    "still standing.",
    "Bounties by day, flags by dawn, 603 TRUED in the bank — top ten "
    "or bust.",
    "One radar graded, one clip placed, twelve flags dodged, zero "
    "quits — that was the week.",
]


def score(line):
    """Deterministic rubric: concrete numbers and vivid specifics win."""
    points = 0
    points += sum(ch.isdigit() for ch in line) * 3
    for word in (
        "graded",
        "placed",
        "flagged",
        "shipping",
        "week",
        "breakfast",
        "chasing",
        "top ten",
        "standing",
    ):
        if word in line.lower():
            points += 5
    points += line.count(",") * 2
    points += line.count("—") * 2
    if line.endswith("."):
        points += 1
    return points


def pick_line(candidates):
    """Pick the highest-scoring line that fits the 100-char cap."""
    fitting = [line for line in candidates if len(line) <= MAX_CHARS]
    if not fitting:
        raise SystemExit("no candidate fits the 100-character limit")
    # Highest score wins; on a tie the earliest candidate wins.
    return max(fitting, key=lambda line: (score(line), -fitting.index(line)))


def main():
    line = pick_line(CANDIDATES)
    if "\n" in line.strip() or len(line) > MAX_CHARS:
        raise SystemExit("picked line is not a single line of <= 100 chars")
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print(line)
    print(f"chars={len(line)} -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
