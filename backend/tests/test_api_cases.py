"""API-Tests: Fälle anlegen, auflisten, abrufen, Sitzung verknüpfen/lösen."""
from fastapi.testclient import TestClient


def test_create_case(client: TestClient):
    r = client.post("/api/cases", json={"alias": "Test-Fall 1"})
    assert r.status_code == 200
    data = r.json()
    assert "case_id" in data
    assert data["case_id"].startswith("CASE-")
    assert data["alias"] == "Test-Fall 1"
    assert "sessions" in data


def test_list_cases_empty_then_one(client: TestClient):
    r = client.get("/api/cases")
    assert r.status_code == 200
    assert r.json() == []

    client.post("/api/cases", json={"alias": "Fall A"})
    r2 = client.get("/api/cases")
    assert r2.status_code == 200
    assert len(r2.json()) == 1
    assert r2.json()[0]["alias"] == "Fall A"


def test_get_case(client: TestClient):
    create = client.post("/api/cases", json={"alias": "Mein Fall"}).json()
    cid = create["case_id"]
    r = client.get(f"/api/cases/{cid}")
    assert r.status_code == 200
    assert r.json()["case_id"] == cid
    assert r.json()["sessions"] == []


def test_get_case_404(client: TestClient):
    r = client.get("/api/cases/CASE-2020-9999")
    assert r.status_code == 404


def test_link_session_to_case(client: TestClient):
    case = client.post("/api/cases", json={"alias": "Fall B"}).json()
    session = client.post("/api/sessions").json()
    cid, sid = case["case_id"], session["session_id"]

    r = client.post(f"/api/cases/{cid}/sessions/{sid}")
    assert r.status_code == 200

    r2 = client.get(f"/api/cases/{cid}")
    assert r2.status_code == 200
    assert len(r2.json()["sessions"]) == 1
    assert r2.json()["sessions"][0]["session_id"] == sid

    r3 = client.get(f"/api/sessions/{sid}")
    assert r3.json()["case_id"] == cid


def test_link_session_404_case(client: TestClient):
    session = client.post("/api/sessions").json()
    r = client.post(f"/api/cases/CASE-2020-9999/sessions/{session['session_id']}")
    assert r.status_code == 404


def test_unlink_then_link_another_case(client: TestClient):
    case1 = client.post("/api/cases", json={"alias": "Fall 1"}).json()
    case2 = client.post("/api/cases", json={"alias": "Fall 2"}).json()
    session = client.post("/api/sessions").json()
    sid = session["session_id"]

    client.post(f"/api/cases/{case1['case_id']}/sessions/{sid}")
    client.post(f"/api/sessions/{sid}/unlink")
    client.post(f"/api/cases/{case2['case_id']}/sessions/{sid}")

    r = client.get(f"/api/sessions/{sid}")
    assert r.json()["case_id"] == case2["case_id"]
