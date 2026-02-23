"""Unit-Tests: Schema-Validierung (Summary-JSON)."""
import pytest
from backend.schema import validate_summary


def test_validate_summary_valid():
    data = {
        "title": "Test",
        "participants": ["A", "B"],
        "key_points": ["Punkt 1"],
        "action_items": ["Aufgabe 1"],
        "summary": "Kurze Zusammenfassung.",
    }
    ok, err = validate_summary(data)
    assert ok is True
    assert err is None


def test_validate_summary_missing_field():
    data = {
        "title": "Test",
        "participants": [],
        "key_points": [],
        # "action_items" fehlt
        "summary": "Text",
    }
    ok, err = validate_summary(data)
    assert ok is False
    assert "action_items" in err or "Missing" in err


def test_validate_summary_not_dict():
    ok, err = validate_summary(None)
    assert ok is False
    assert err is not None

    ok2, err2 = validate_summary([])
    assert ok2 is False


def test_validate_summary_participants_must_be_list_of_strings():
    data = {
        "title": "T",
        "participants": [1, 2],  # Zahlen statt Strings
        "key_points": [],
        "action_items": [],
        "summary": "S",
    }
    ok, err = validate_summary(data)
    assert ok is False
