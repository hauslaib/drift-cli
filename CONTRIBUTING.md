# Contributing

This is a small utility. Most of it is fixed by the book's content.
Contributions are welcome in three specific shapes.

## Translations

If you translate the question text, the SA clause applies: your translation
must also be released under CC BY-SA 4.0. Open a pull request adding the
translations as a separate module (for example, `drift/text_de.py` for
German) and a `--language` flag in `drift/__main__.py`. Discuss in an issue
first so the structure can be agreed.

## Bug fixes and ergonomics

Welcome. Open an issue describing the bug or the small ergonomic
improvement, then a pull request. Keep changes focused. The tool has no
dependencies and is intended to stay that way.

## What is unlikely to be merged

- Changes to the question text itself. The questions come from the book's
  front matter and are co-versioned with the manuscript.
- Telemetry, analytics, or any feature that sends data anywhere. The tool's
  privacy stance is a design constraint, not a default. The book argues
  that the moment the Drift Check becomes a metric reported upward, it
  stops measuring the Drift and starts producing it.
- Dependencies that are not part of the Python standard library, unless
  there is a compelling reason. The current zero-dependency footprint is
  intentional.
- Visual flourishes: emoji, progress bars, animations, ASCII art. The brand
  is Continental Restraint. The tool stays calm.

## Voice conventions

The book and this tool share a small set of style choices:

- British English in prose (except in CSS or CLI keywords).
- Straight ASCII apostrophes.
- No em-dashes. Comma, semicolon, or full stop instead.
- No en-dashes. Hyphen for ranges ("1-5", not "1--5").
- A short avoid-list documented in the book's production notes.

Pull requests that introduce these patterns will be asked to revise.

## Running the tests

```
git clone https://github.com/hauslaib/drift-cli
cd drift-cli
pip install -e ".[dev]"
pytest
```

The tests use a temporary `DRIFT_HOME` so they do not write to your real
home directory.

## Reporting issues

GitHub issues at https://github.com/hauslaib/drift-cli/issues.

Kyle Hauslaib, 2026.
