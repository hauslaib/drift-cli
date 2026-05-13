"""Tests for the local-only storage layer.

These tests use a temporary DRIFT_HOME so they do not write to the user's
real ~/.drift directory.
"""

import json
import os
import tempfile
import pytest

from drift.storage import save_check, load_history, storage_path


@pytest.fixture
def temp_home(monkeypatch, tmp_path):
    monkeypatch.setenv("DRIFT_HOME", str(tmp_path / "scores"))
    return tmp_path


class TestSave:
    def test_writes_a_dated_json_file(self, temp_home):
        p = save_check({1: 3, 2: 3, 3: 3, 4: 3, 5: 3})
        assert p.exists()
        assert p.suffix == ".json"
        data = json.loads(p.read_text())
        assert data["total"] == 15
        assert data["scores"] == {"1": 3, "2": 3, "3": 3, "4": 3, "5": 3}

    def test_creates_storage_dir(self, temp_home):
        # The dir does not exist before save.
        path = storage_path()
        assert not path.exists()
        save_check({1: 1, 2: 1, 3: 1, 4: 1, 5: 1})
        assert path.exists()

    def test_label_persisted(self, temp_home):
        p = save_check({1: 4, 2: 4, 3: 4, 4: 4, 5: 4}, label="alpha team")
        data = json.loads(p.read_text())
        assert data["label"] == "alpha team"

    def test_second_save_on_same_day_does_not_overwrite(self, temp_home):
        p1 = save_check({1: 1, 2: 1, 3: 1, 4: 1, 5: 1})
        p2 = save_check({1: 5, 2: 5, 3: 5, 4: 5, 5: 5})
        assert p1 != p2
        assert p1.exists()
        assert p2.exists()


class TestLoad:
    def test_empty_when_no_storage_dir(self, temp_home):
        assert load_history() == []

    def test_loads_a_saved_check(self, temp_home):
        save_check({1: 3, 2: 3, 3: 3, 4: 3, 5: 3}, label="team A")
        history = load_history()
        assert len(history) == 1
        assert history[0]["total"] == 15
        assert history[0]["label"] == "team A"

    def test_orders_by_filename(self, temp_home):
        save_check({1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, label="first")
        save_check({1: 5, 2: 5, 3: 5, 4: 5, 5: 5}, label="second")
        history = load_history()
        assert len(history) == 2
        # First file written is today.json; second is today-2.json.
        # Sorted alphabetically, today.json comes first.
        assert history[0]["label"] == "first"
        assert history[1]["label"] == "second"

    def test_corrupted_file_is_skipped(self, temp_home, tmp_path):
        save_check({1: 3, 2: 3, 3: 3, 4: 3, 5: 3})
        # Plant a corrupted file in the same directory.
        bad = storage_path() / "garbage.json"
        bad.write_text("this is not json")
        history = load_history()
        # The valid file is still loaded; the bad one is silently skipped.
        assert len(history) == 1
