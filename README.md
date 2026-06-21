# drift

[![DOI](https://zenodo.org/badge/1237866128.svg)](https://doi.org/10.5281/zenodo.20786450)

A five-question terminal reading of the gap between what your organisation
says it does and what it does in practice. Companion utility to *Leading
Agile When No One Agrees* by Kyle Hauslaib.

The score is for the person scoring. The tool never sends data anywhere.

```
  DRIFT CHECK
  Five questions. Score 1 to 5. The score is for you.
  Reflect on the past three months,
  not your best week or your worst sprint.

  1 = rarely true   3 = sometimes true   5 = consistently true

  01  Information
      The information reaching strategic decision-makers matches
      what teams privately discuss about the same work.
      Score (1-5): 3
  ...
```

## Install

Requires Python 3.10 or later. No third-party dependencies.

```
pip install drift-check
```

Or run from a clone without installing:

```
git clone https://github.com/hauslaib/drift-cli
cd drift-cli
python3 -m drift
```

## Use

Run the five-question check interactively:

```
drift
```

Save the result as a local JSON file under `~/.drift/scores/`:

```
drift --save
drift --save --label "alpha team Q2"
```

Show your saved scores over time:

```
drift --history
```

Get a JSON object on stdout (for scripting):

```
echo "3 4 2 5 3" | drift --json
```

## What this tool does, and does not do

It walks the five-question Drift Check from the front matter of the book,
collects scores, computes the total, and prints the interpretation. If you
ask it to save, it writes a dated JSON file under your home directory.

It does not send data anywhere. It does not phone home. It does not call any
network API. There is no analytics, no telemetry, no opt-in or opt-out
because there is nothing to opt out of. The score is yours and stays on the
machine you ran the tool from.

This is a design choice, not an oversight. The book argues that the moment
the Drift Check becomes a metric reported upward, it stops measuring the
Drift and starts producing it. The tool enforces this in code.

## How to use the check in a team

The practical pattern from the book:

1. Each person on the team scores independently.
2. The team compares scores in retrospective.
3. The team decides which low-scoring dimension to attend to in the next
   sprint.

Do not roll the scores up beyond the team. The check is a prompt for a more
honest conversation, not a number for someone above you to track.

## Reading your score

```
21 to 25   Low Drift
14 to 20   Moderate Drift
13 or below  Significant Drift
```

The book covers each band in detail. The companion site at
https://kylehauslaib.com/companion/ has a printable version of the check
plus six related practical-tool worksheets.

## Development

```
git clone https://github.com/hauslaib/drift-cli
cd drift-cli
python3 -m drift                  # run interactively
python3 -m pytest tests/          # run the tests
```

The package has no runtime dependencies. The test suite uses `pytest`.

## File layout

```
drift-cli/
├── drift/
│   ├── __init__.py
│   ├── __main__.py        CLI entry point
│   ├── check.py           Domain model (Question, Reading, Check)
│   ├── interface.py       Terminal interaction
│   └── storage.py         Local-only score storage
├── tests/
│   ├── test_check.py
│   └── test_storage.py
├── README.md
├── LICENSE
├── LICENSE-CODE.md
├── LICENSE-CONTENT.md
├── CONTRIBUTING.md
└── pyproject.toml
```

## Licences

Code under MIT (`LICENSE-CODE.md`). The question text, reading bands, and
prose are under Creative Commons Attribution-ShareAlike 4.0 International
(`LICENSE-CONTENT.md`), matching the companion repository at
https://github.com/hauslaib/leading-agile-companion.

## Related

- The book: *Leading Agile When No One Agrees: A Field Guide to Engineering
  Leadership in Imperfect Organisations*
- Companion site: https://kylehauslaib.com/companion/
- Companion repository: https://github.com/hauslaib/leading-agile-companion

---

Kyle Hauslaib, 2026.

## Citation

If you use Drift CLI, please cite the archived release:

> Hauslaib, K. (2026). *Drift CLI* (Version 1.0.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.20786450

The DOI above is the concept DOI and always resolves to the latest version. A machine-readable citation is in [`CITATION.cff`](CITATION.cff).
