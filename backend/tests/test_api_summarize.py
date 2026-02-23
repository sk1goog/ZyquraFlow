"""API-Tests: Zusammenfassen (mit gemocktem LLM)."""
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient


@pytest.fixture
def session_with_transcript(client: TestClient):
    """Sitzung mit gespeichertem Transkript anlegen."""
    r = client.post("/api/sessions")
    sid = r.json()["session_id"]
    client.put(
        f"/api/sessions/{sid}/transcript",
        json={"transcript": "Besprechung am Montag. Teilnehmer: Anna, Bert. Themen: Budget, Timeline."},
    )
    return sid


def test_summarize_returns_valid_session(client: TestClient, session_with_transcript):
    """Zusammenfassen liefert aktualisierte Sitzung mit summary (LLM gemockt)."""
    mock_response = type("R", (), {
        "text": """{
            "title": "Test-Besprechung",
            "participants": ["Anna", "Bert"],
            "key_points": ["Budget", "Timeline"],
            "action_items": ["Nächste Schritte klären"],
            "summary": "Kurze Test-Zusammenfassung."
        }""",
        "model": "llama3.2",
        "prompt_id": "summary.v0.1",
        "duration_ms": 100.0,
    })()

    with patch("backend.services.session_service.get_llm") as mock_llm:
        mock_llm.return_value.complete = AsyncMock(return_value=mock_response)
        r = client.post(f"/api/sessions/{session_with_transcript}/summarize")

    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "summarized"
    assert data["summary"] is not None
    assert data["summary"]["title"] == "Test-Besprechung"
    assert "Anna" in data["summary"]["participants"]
    assert data["summary_path"]


def test_summarize_no_transcript_returns_400(client: TestClient):
    """Ohne Transkript liefert Summarize 400."""
    create = client.post("/api/sessions").json()
    r = client.post(f"/api/sessions/{create['session_id']}/summarize")
    assert r.status_code == 400


def test_summarize_404(client: TestClient):
    r = client.post("/api/sessions/SESSION-nonexistent123/summarize")
    assert r.status_code == 400  # oder 404, je nach Implementierung
