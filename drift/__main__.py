"""CLI entry point. Run with `python -m drift` or `drift` after install."""

from __future__ import annotations
import argparse
import json
import sys

from drift import __version__
from drift.check import Check, QUESTIONS, Reading
from drift.interface import run_interactive, print_history


def _make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="drift",
        description=(
            "A five-question terminal reading of the gap between what your "
            "organisation says it does and what it does in practice. "
            "Companion utility to Leading Agile When No One Agrees."
        ),
        epilog="The score is for the person scoring. The tool never sends data anywhere.",
    )
    p.add_argument(
        "--version", action="version", version=f"drift {__version__}"
    )
    p.add_argument(
        "--save", action="store_true",
        help="Save the result as a local JSON file under ~/.drift/scores/.",
    )
    p.add_argument(
        "--label", type=str, default=None,
        help="Optional short note attached to the saved file (e.g., the team name).",
    )
    p.add_argument(
        "--history", action="store_true",
        help="Show previously saved scores instead of running a new check.",
    )
    p.add_argument(
        "--json", action="store_true",
        help="Print the result as JSON instead of formatted prose. Useful in scripts.",
    )
    return p


def _print_json(check: Check) -> None:
    out = {
        "scores": check.scores,
        "total": check.total,
        "reading": {
            "band": check.reading.band,
            "label": check.reading.label,
            "summary": check.reading.summary,
        },
        "lowest": {
            "number": check.lowest.number,
            "name": check.lowest.name,
            "chapter_pointer": check.lowest.chapter_pointer,
        },
    }
    print(json.dumps(out, indent=2))


def main(argv: list[str] | None = None) -> int:
    args = _make_parser().parse_args(argv)

    if args.history:
        return print_history()

    if args.json:
        # Non-interactive JSON mode reads scores from stdin as
        # "1 2 3 4 5" (space-separated) or as JSON {"1": 3, "2": 4, ...}.
        # Falls back to interactive if stdin is a tty.
        if sys.stdin.isatty():
            check = run_interactive(save=args.save, label=args.label)
        else:
            raw = sys.stdin.read().strip()
            scores = _parse_scores(raw)
            check = Check(scores=scores)
            if args.save:
                from drift.storage import save_check
                save_check(scores, label=args.label)
        _print_json(check)
        return 0

    run_interactive(save=args.save, label=args.label)
    return 0


def _parse_scores(raw: str) -> dict[int, int]:
    """Parse stdin scores. Accepts JSON or whitespace-separated integers."""
    raw = raw.strip()
    if not raw:
        raise SystemExit("No scores provided on stdin.")
    if raw.startswith("{"):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            raise SystemExit(f"Could not parse JSON: {e}")
        return {int(k): int(v) for k, v in data.items()}
    nums = raw.split()
    if len(nums) != 5:
        raise SystemExit(f"Expected 5 scores, got {len(nums)}.")
    return {i + 1: int(n) for i, n in enumerate(nums)}


if __name__ == "__main__":
    sys.exit(main())
