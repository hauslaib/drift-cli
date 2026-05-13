"""Tests for the Drift Check domain model."""

import pytest
from drift.check import Check, Question, Reading, QUESTIONS


class TestQuestions:
    def test_five_questions_present(self):
        assert len(QUESTIONS) == 5

    def test_questions_numbered_sequentially(self):
        assert [q.number for q in QUESTIONS] == [1, 2, 3, 4, 5]

    def test_each_question_has_a_name_and_statement(self):
        for q in QUESTIONS:
            assert q.name
            assert q.statement
            assert len(q.statement) > 30


class TestReading:
    def test_low_drift_at_21(self):
        r = Reading.from_total(21)
        assert r.band == "low"
        assert r.label == "Low Drift"

    def test_low_drift_at_25(self):
        r = Reading.from_total(25)
        assert r.band == "low"

    def test_moderate_drift_at_14(self):
        r = Reading.from_total(14)
        assert r.band == "moderate"

    def test_moderate_drift_at_20(self):
        r = Reading.from_total(20)
        assert r.band == "moderate"

    def test_significant_drift_at_13(self):
        r = Reading.from_total(13)
        assert r.band == "significant"

    def test_significant_drift_at_5(self):
        r = Reading.from_total(5)
        assert r.band == "significant"


class TestCheck:
    def test_total_is_sum_of_scores(self):
        c = Check(scores={1: 3, 2: 4, 3: 2, 4: 5, 5: 3})
        assert c.total == 17

    def test_reading_at_17_is_moderate(self):
        c = Check(scores={1: 3, 2: 4, 3: 2, 4: 5, 5: 3})
        assert c.reading.band == "moderate"

    def test_lowest_resolves_ties_by_question_number(self):
        c = Check(scores={1: 5, 2: 2, 3: 2, 4: 5, 5: 5})
        # both Q2 and Q3 scored 2; lowest number wins
        assert c.lowest.number == 2

    def test_score_below_one_raises(self):
        with pytest.raises(ValueError):
            Check(scores={1: 0, 2: 3, 3: 3, 4: 3, 5: 3})

    def test_score_above_five_raises(self):
        with pytest.raises(ValueError):
            Check(scores={1: 6, 2: 3, 3: 3, 4: 3, 5: 3})

    def test_perfect_score_is_low_drift(self):
        c = Check(scores={1: 5, 2: 5, 3: 5, 4: 5, 5: 5})
        assert c.total == 25
        assert c.reading.band == "low"

    def test_minimum_score_is_significant_drift(self):
        c = Check(scores={1: 1, 2: 1, 3: 1, 4: 1, 5: 1})
        assert c.total == 5
        assert c.reading.band == "significant"
