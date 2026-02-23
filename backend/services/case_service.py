"""Case use case / service."""
from backend.db import db_cursor, init_db
from backend.storage import generate_case_id, ensure_data_root


def list_cases() -> list[dict]:
    init_db()
    with db_cursor() as cur:
        cur.execute(
            """
            SELECT c.*, COUNT(s.session_id) as session_count
            FROM cases c
            LEFT JOIN sessions s ON s.case_id = c.case_id
            GROUP BY c.case_id
            ORDER BY c.created_at DESC
            """
        )
        rows = cur.fetchall()
    return [
        {
            "case_id": r["case_id"],
            "alias": r["alias"],
            "created_at": r["created_at"],
            "session_count": r["session_count"],
        }
        for r in rows
    ]


def create_case(alias: str) -> dict:
    init_db()
    ensure_data_root()
    case_id = generate_case_id()
    with db_cursor() as cur:
        cur.execute(
            "INSERT INTO cases (case_id, alias, created_at) VALUES (?, ?, datetime('now'))",
            (case_id, alias),
        )
    return get_case(case_id)


def get_case(case_id: str) -> dict:
    from backend.services.session_service import list_sessions
    init_db()
    with db_cursor() as cur:
        cur.execute("SELECT * FROM cases WHERE case_id = ?", (case_id,))
        row = cur.fetchone()
    if not row:
        return None
    sessions = list_sessions(case_id)
    return {
        "case_id": row["case_id"],
        "alias": row["alias"],
        "created_at": row["created_at"],
        "sessions": sessions,
    }
