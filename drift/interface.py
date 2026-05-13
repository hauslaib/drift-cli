"""Terminal interaction for the Drift Check.

Continental Restraint applied to a CLI. No emoji, no progress bars,
no animations. Two-space indent for body text. Question labels in
small caps. Reading section visually separated.
"""

from __future__ import annotations
import sys
from typing import Dict
from drift.check import Check, Question, QUESTIONS
from drift.storage import save_check, storage_path


# ANSI codes. Quiet palette: ink for body, muted copper for the band
# label, dim grey for metadata. No bright primaries.
class _A:
    RESET = "\x1b[0m"
    DIM   = "\x1b[2m"
    BOLD  = "\x1b[1m"
    INK   = "\x1b[38;5;235m"   # near-black fallback
    GOLD  = "\x1b[38;5;180m"   # muted copper
    UND   = "\x1b[4m"


def _supports_colour() -> bool:
    return sys.stdout.isatty() and "NO_COLOR" not in __import__("os").environ


def _c(text: str, code: str) -> str:
    if not _supports_colour():
        return text
    return f"{code}{text}{_A.RESET}"


def _header() -> str:
    return (
        "\n"
        "  " + _c("DRIFT CHECK", _A.BOLD) + "\n"
    )


def _intro() -> str:
    return (
        "  Five questions. Score 1 to 5. The score is for you.\n"
        "  Reflect on the past three months,\n"
        "  not your best week or your worst sprint.\n"
        "\n"
        "  1 = rarely true   3 = sometimes true   5 = consistently true\n"
    )


def _ask_score(q: Question) -> int:
    """Prompt for a single question. Re-asks on invalid input."""
    print()
    label = f"{q.number:02d}  {q.name}"
    print("  " + _c(label, _A.BOLD))
    # Statement wrapped at ~64 chars, indented.
    print(_wrap(q.statement, width=66, indent="      "))
    while True:
        try:
            raw = input("      " + _c("Score (1-5): ", _A.DIM))
        except (EOFError, KeyboardInterrupt):
            print()
            print("  Interrupted. No scores saved.")
            sys.exit(130)
        raw = raw.strip()
        try:
            score = int(raw)
            if 1 <= score <= 5:
                return score
        except ValueError:
            pass
        print("      " + _c("Score must be 1, 2, 3, 4, or 5.", _A.DIM))


def _wrap(text: str, width: int, indent: str) -> str:
    """Word-wrap text to width, prefixing each line with indent."""
    words = text.split()
    lines = []
    current = ""
    for w in words:
        candidate = (current + " " + w).strip()
        if len(candidate) <= width:
            current = candidate
        else:
            lines.append(indent + current)
            current = w
    if current:
        lines.append(indent + current)
    return "\n".join(lines)


def _print_reading(check: Check) -> None:
    print()
    print("  " + _c("─" * 66, _A.DIM))
    print()
    total_line = f"TOTAL  {check.total} / 25"
    print("  " + _c(total_line, _A.BOLD))
    reading = check.reading
    print("  " + _c(reading.label.upper(), _A.GOLD))
    print()
    print(_wrap(reading.summary, width=66, indent="  "))

    if reading.band == "moderate":
        # Point the reader at the chapter for their lowest-scoring dimension.
        low = check.lowest
        print()
        print(
            "  Your lowest-scoring dimension was "
            + _c(low.name, _A.BOLD)
            + " ("
            + str(check.scores[low.number])
            + "/5)."
        )
        print(f"  See {low.chapter_pointer}.")

    print()


def _footer(saved_path: str | None) -> None:
    print("  " + _c("─" * 66, _A.DIM))
    print()
    if saved_path:
        print("  Saved to " + _c(saved_path, _A.DIM))
        print("  This file is local to your machine. Nothing is sent anywhere.")
    else:
        print("  Not saved. (Use --save to write a local copy.)")
    print()
    print(
        "  " + _c(
            "Do not roll the scores up beyond the team.",
            _A.DIM,
        )
    )
    print()


def run_interactive(*, save: bool = False, label: str | None = None) -> Check:
    """Run a full interactive Drift Check session.

    Returns the completed Check. Writes a local JSON if save=True.
    """
    print(_header())
    print(_intro())

    scores: Dict[int, int] = {}
    for q in QUESTIONS:
        scores[q.number] = _ask_score(q)

    check = Check(scores=scores)
    _print_reading(check)

    saved_path = None
    if save:
        p = save_check(scores, label=label)
        saved_path = str(p)
    _footer(saved_path)

    return check


def print_history() -> int:
    """Print the user's saved scores in chronological order.

    Returns 0 if scores were found, 1 if none.
    """
    from drift.storage import load_history
    history = load_history()
    print()
    print("  " + _c("DRIFT CHECK · HISTORY", _A.BOLD))
    print()
    if not history:
        print("  No saved scores. Run `drift --save` to record one.")
        print()
        print("  Storage location (will be created on first save):")
        print("    " + _c(str(storage_path()), _A.DIM))
        print()
        return 1

    print("  Date         Total  Band")
    print("  " + _c("─" * 28, _A.DIM))
    for entry in history:
        total = entry["total"]
        from drift.check import Reading
        band = Reading.from_total(total).label
        print(f"  {entry['date']}   {total:>4}   {band}")
    print()
    print(
        f"  {len(history)} entry"
        + ("" if len(history) == 1 else "ies")
        + ". Stored at "
        + _c(str(storage_path()), _A.DIM)
    )
    print()
    return 0
