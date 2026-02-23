"""Pytest fixtures: temporäres Datenverzeichnis + Test-DB, API-Client."""
import pytest
from pathlib import Path

from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def test_env(tmp_path, monkeypatch):
    """Pro Test: eigenes Temp-Verzeichnis und Test-DB, keine echten Daten."""
    db_path = tmp_path / "test.db"
    monkeypatch.setattr("backend.config.DATA_ROOT", tmp_path)
    monkeypatch.setattr("backend.config.DB_PATH", db_path)
    monkeypatch.setattr("backend.db.DB_PATH", db_path)
    from backend.db import init_db
    init_db()
    yield


@pytest.fixture
def client():
    """FastAPI TestClient gegen die echte App (mit gepatchter Config)."""
    from backend.main import app
    return TestClient(app)
