"""Local-only score storage. No network, no telemetry.

Scores are written to ~/.drift/scores/<date>.json on the user's own machine.
Nothing ever leaves this filesystem. The history command reads from that
directory only.

Rationale: the book argues that the moment the Drift Check becomes a metric
reported upward, it stops measuring the Drift and starts producing it. The
tool enforces this in code.
"""

from __future__ import annotations
import json
import os
import re
import datetime
from pathlib import Path
from typing import List, Dict, Any

# Score files are named <date>.json, with same-day repeats suffixed
# <date>-2.json, <date>-3.json, and so on.
_FILENAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-(\d+))?$")


def _storage_dir() -> Path:
    """The directory where score files live. Created on first write."""
    base = os.environ.get("DRIFT_HOME")
    if base:
        return Path(base).expanduser()
    return Path.home() / ".drift" / "scores"


def save_check(scores: Dict[int, int], *, label: str | None = None) -> Path:
    """Persist a completed check to disk. Returns the file path.

    scores: mapping of question number (1..5) to score (1..5)
    label:  optional short note the user wrote when scoring
    """
    storage = _storage_dir()
    storage.mkdir(parents=True, exist_ok=True)

    today = datetime.date.today().isoformat()
    # If a file for today already exists, append a suffix.
    path = storage / f"{today}.json"
    n = 2
    while path.exists():
        path = storage / f"{today}-{n}.json"
        n += 1

    payload = {
        "date": today,
        "scores": {str(k): v for k, v in scores.items()},
        "total": sum(scores.values()),
        "label": label,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def _history_sort_key(path: Path) -> tuple:
    """Order score files by date, then by same-day sequence.

    A bare <date>.json is the first save of that day and sorts before
    <date>-2.json, <date>-3.json, and so on. Plain string sorting would
    put <date>-2.json first, because '-' precedes '.', so the sequence
    number is parsed out and compared as an integer.
    """
    match = _FILENAME_RE.match(path.stem)
    if match:
        return (match.group(1), int(match.group(2) or 1))
    # Names that do not fit the pattern sort last, by stem.
    return ("9999", 0, path.stem)


def load_history() -> List[Dict[str, Any]]:
    """Return all saved checks, ordered by date ascending.

    Empty list if the storage directory does not exist.
    """
    storage = _storage_dir()
    if not storage.exists():
        return []

    out = []
    for path in sorted(storage.glob("*.json"), key=_history_sort_key):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            data["__path"] = str(path)
            out.append(data)
        except (json.JSONDecodeError, OSError):
            # Silently skip a corrupted or unreadable file. The user can
            # inspect it directly; we do not loud-fail.
            continue
    return out


def storage_path() -> Path:
    """Public helper for the interface module to report where files live."""
    return _storage_dir()
