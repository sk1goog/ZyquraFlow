"""LLM provider registry and config."""
from typing import Optional

from backend.config import DEFAULT_PROVIDER, DEFAULT_MODEL, DEFAULT_DEBUG
from backend.db import init_db, get_conn


_provider_instance = None


def get_config():
    init_db()
    conn = get_conn()
    conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
    cur = conn.cursor()
    cur.execute("SELECT key, value FROM config")
    rows = {r["key"]: r["value"] for r in cur.fetchall()}
    conn.close()
    return {
        "provider": rows.get("provider", DEFAULT_PROVIDER),
        "model": rows.get("model", DEFAULT_MODEL),
        "debug": rows.get("debug", str(DEFAULT_DEBUG)).lower() == "true",
    }


def set_config(provider: Optional[str] = None, model: Optional[str] = None, debug: Optional[bool] = None):
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    if provider is not None:
        cur.execute("INSERT OR REPLACE INTO config (key, value) VALUES ('provider', ?)", (provider,))
    if model is not None:
        cur.execute("INSERT OR REPLACE INTO config (key, value) VALUES ('model', ?)", (model,))
    if debug is not None:
        cur.execute("INSERT OR REPLACE INTO config (key, value) VALUES ('debug', ?)", (str(debug).lower(),))
    conn.commit()
    conn.close()


def get_llm():
    global _provider_instance
    if _provider_instance is None:
        from backend.providers import OllamaProvider
        _provider_instance = OllamaProvider()
    return _provider_instance
