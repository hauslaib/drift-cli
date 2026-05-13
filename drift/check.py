"""The Drift Check domain model.

Five questions, each scored 1-5. The questions and the reading-your-score
guidance are taken from the front matter of the book. Pure Python, no
dependencies.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Question:
    """A single Drift Check question."""
    number: int
    name: str
    statement: str
    chapter_pointer: str

    def __str__(self) -> str:
        return self.statement


# The five questions, in the order the book lists them.
QUESTIONS: List[Question] = [
    Question(
        number=1,
        name="Information",
        statement=(
            "The information reaching strategic decision-makers matches what "
            "teams privately discuss about the same work."
        ),
        chapter_pointer="Chapter 1 and Chapter 11",
    ),
    Question(
        number=2,
        name="Decisions",
        statement=(
            "The decisions that shape your team's work originate in scheduled "
            "meetings; corridor conversations confirm or refine them."
        ),
        chapter_pointer="Chapter 9 and Chapter 16",
    ),
    Question(
        number=3,
        name="Commitments",
        statement=(
            "Planning produces commitments that reflect honest team estimates, "
            "with leaders accepting the result."
        ),
        chapter_pointer="Chapter 3 and Chapter 4",
    ),
    Question(
        number=4,
        name="Improvement",
        statement=(
            "Retrospective action items from three sprints ago can be located "
            "and shown to have changed something."
        ),
        chapter_pointer="Chapter 6",
    ),
    Question(
        number=5,
        name="Knowledge",
        statement=(
            "Two or more people on the team can perform the work that depends "
            "on its most experienced specialist."
        ),
        chapter_pointer="Chapter 7 and Chapter 21",
    ),
]


@dataclass
class Reading:
    """The interpretation of a Drift Check total."""
    band: str
    label: str
    summary: str

    @classmethod
    def from_total(cls, total: int) -> "Reading":
        if total >= 21:
            return cls(
                band="low",
                label="Low Drift",
                summary=(
                    "The organisation operates close to what it says about "
                    "itself. The book's later chapters will still be useful; "
                    "the diagnostic ones in Part I will largely confirm what "
                    "you already see."
                ),
            )
        if total >= 14:
            return cls(
                band="moderate",
                label="Moderate Drift",
                summary=(
                    "The two systems diverge in some areas. The chapter that "
                    "maps to your lowest-scoring dimension is worth a closer "
                    "look."
                ),
            )
        return cls(
            band="significant",
            label="Significant Drift",
            summary=(
                "The Lived System is doing most of the work, while the Stated "
                "System carries on unchanged. Part I and Part II walk through "
                "the patterns. Part III addresses the leadership practice of "
                "working inside them."
            ),
        )


@dataclass
class Check:
    """A completed Drift Check: questions, scores, total, reading."""
    scores: dict  # question.number -> int 1..5

    def __post_init__(self):
        for n, s in self.scores.items():
            if not (1 <= s <= 5):
                raise ValueError(
                    f"Question {n} score {s} is out of range. Each score is 1 to 5."
                )

    @property
    def total(self) -> int:
        return sum(self.scores.values())

    @property
    def reading(self) -> Reading:
        return Reading.from_total(self.total)

    @property
    def lowest(self) -> Question:
        """The question with the lowest score. Ties resolve to lowest number."""
        if not self.scores:
            raise ValueError("No scores recorded.")
        lowest_num = min(self.scores.keys(), key=lambda n: (self.scores[n], n))
        return next(q for q in QUESTIONS if q.number == lowest_num)
