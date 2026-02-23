"""API-Tests: Health, System-Config, Provider-Liste."""
import pytest
from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "provider" in data
    assert "ollama_available" in data


def test_get_system_config(client: TestClient):
    r = client.get("/api/system/config")
    assert r.status_code == 200
    data = r.json()
    assert "provider" in data
    assert "model" in data
    assert "debug" in data
    assert "whisper_model" in data


def test_patch_system_config(client: TestClient):
    r = client.patch("/api/system/config", json={"debug": True})
    assert r.status_code == 200
    data = r.json()
    assert data["debug"] is True

    r2 = client.patch("/api/system/config", json={"debug": False})
    assert r2.status_code == 200
    assert r2.json()["debug"] is False


def test_list_providers(client: TestClient):
    r = client.get("/api/system/providers")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(p["id"] == "ollama" for p in data)


def test_patch_whisper_model(client: TestClient):
    r = client.patch("/api/system/config", json={"whisper_model": "small"})
    assert r.status_code == 200
    assert r.json()["whisper_model"] == "small"


def test_list_whisper_models(client: TestClient):
    r = client.get("/api/system/whisper-models")
    assert r.status_code == 200
    data = r.json()
    assert "models" in data
    assert "base" in data["models"]
    assert "small" in data["models"]
