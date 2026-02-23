"""API-Tests: Sitzungen anlegen, auflisten, abrufen, Transkript, Audio (Stub), Transcribe, Unlink."""
import io
from unittest.mock import patch
from fastapi.testclient import TestClient


def test_create_session(client: TestClient):
    r = client.post("/api/sessions")
    assert r.status_code == 200
    data = r.json()
    assert "session_id" in data
    assert data["session_id"].startswith("SESSION-")
    assert data["status"] == "draft"
    assert data["case_id"] is None


def test_list_sessions_empty_then_one(client: TestClient):
    r = client.get("/api/sessions")
    assert r.status_code == 200
    assert r.json() == []

    client.post("/api/sessions")
    r2 = client.get("/api/sessions")
    assert r2.status_code == 200
    assert len(r2.json()) == 1


def test_get_session(client: TestClient):
    create = client.post("/api/sessions").json()
    sid = create["session_id"]
    r = client.get(f"/api/sessions/{sid}")
    assert r.status_code == 200
    assert r.json()["session_id"] == sid


def test_get_session_404(client: TestClient):
    r = client.get("/api/sessions/SESSION-nonexistent123")
    assert r.status_code == 404


def test_update_transcript(client: TestClient):
    create = client.post("/api/sessions").json()
    sid = create["session_id"]
    r = client.put(
        f"/api/sessions/{sid}/transcript",
        json={"transcript": "Das ist ein Test-Transkript."},
    )
    assert r.status_code == 200
    assert r.json()["transcript"] == "Das ist ein Test-Transkript."


def test_upload_audio(client: TestClient):
    create = client.post("/api/sessions").json()
    sid = create["session_id"]
    # Minimaler Audio-Stub (WAV-Header oder beliebiger Inhalt)
    content = b"\x00\x00\x00\x00"
    r = client.post(
        f"/api/sessions/{sid}/audio",
        files={"file": ("test.ogg", io.BytesIO(content), "audio/ogg")},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "uploaded"
    assert data["file_size"] == 4


def test_transcribe_session(client: TestClient):
    create = client.post("/api/sessions").json()
    sid = create["session_id"]
    with patch("backend.main.session_service.transcribe_session") as transcribe:
        transcribe.return_value = {
            **create,
            "transcript": "Transkribierter Text.",
        }
        r = client.post(f"/api/sessions/{sid}/transcribe")
    assert r.status_code == 200
    assert r.json()["transcript"] == "Transkribierter Text."


def test_transcribe_no_audio_returns_400(client: TestClient):
    create = client.post("/api/sessions").json()
    sid = create["session_id"]
    with patch("backend.main.session_service.transcribe_session") as transcribe:
        transcribe.side_effect = ValueError("Keine Audiodatei in dieser Sitzung.")
        r = client.post(f"/api/sessions/{sid}/transcribe")
    assert r.status_code == 400


def test_unlink_session_success(client: TestClient):
    create = client.post("/api/sessions").json()
    sid = create["session_id"]
    r = client.post(f"/api/sessions/{sid}/unlink")
    assert r.status_code == 200
    # Session existiert weiter, case_id ist null
    r2 = client.get(f"/api/sessions/{sid}")
    assert r2.status_code == 200
    assert r2.json()["case_id"] is None


def test_unlink_session_404(client: TestClient):
    r = client.post("/api/sessions/SESSION-nonexistent123/unlink")
    assert r.status_code == 404
