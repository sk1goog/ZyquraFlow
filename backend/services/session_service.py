"""Session use case / service."""
import json
from pathlib import Path

from backend.db import db_cursor, init_db
from backend.storage import generate_session_dir, get_session_dir, get_unlinked_session_dir
from backend.schema import validate_summary
from backend.prompts import load_prompt
from backend.llm import get_llm, get_config
from backend.config import DATA_ROOT


def _session_row_to_dto(row, summary_path=None):
    s = dict(row)
    summary_json = None
    path = summary_path or (s.get("summary_path") and Path(s["summary_path"]))
    if path and Path(path).exists():
        try:
            summary_json = json.loads(Path(path).read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "session_id": s["session_id"],
        "case_id": s["case_id"],
        "created_at": s["created_at"],
        "audio_path": s["audio_path"] or "",
        "summary_path": s["summary_path"],
        "file_size": s["file_size"] or 0,
        "duration": s["duration"],
        "status": s["status"] or "draft",
        "transcript": s.get("transcript"),
        "summary": summary_json,
    }


def create_session(case_id=None) -> dict:
    init_db()
    session_dir, session_id = generate_session_dir(case_id)
    case_for_db = case_id if case_id and case_id != "_unlinked" else None

    with db_cursor() as cur:
        cur.execute(
            """
            INSERT INTO sessions (session_id, case_id, created_at, audio_path, status)
            VALUES (?, ?, datetime('now'), '', 'draft')
            """,
            (session_id, case_for_db),
        )
    return get_session(session_id)


def list_sessions(case_id=None) -> list:
    init_db()
    with db_cursor() as cur:
        if case_id:
            cur.execute(
                "SELECT * FROM sessions WHERE case_id = ? ORDER BY created_at DESC",
                (case_id,),
            )
        else:
            cur.execute("SELECT * FROM sessions ORDER BY created_at DESC")
        rows = cur.fetchall()
    from backend.db import row_to_dict
    return [_session_row_to_dto(row_to_dict(r)) for r in rows]


def get_session(session_id: str):
    init_db()
    with db_cursor() as cur:
        cur.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        row = cur.fetchone()
    if not row:
        return None
    from backend.db import row_to_dict
    return _session_row_to_dto(row_to_dict(row))


def _resolve_session_path(session_id: str):
    """Find session dir; return (path, case_id)."""
    init_db()
    with db_cursor() as cur:
        cur.execute("SELECT case_id FROM sessions WHERE session_id = ?", (session_id,))
        row = cur.fetchone()
    if not row:
        raise ValueError(f"Session not found: {session_id}")
    case_id = row["case_id"]
    if case_id:
        return get_session_dir(case_id, session_id), case_id
    return get_unlinked_session_dir(session_id), None


def update_audio(session_id: str, file_path: Path, file_size: int) -> dict:
    init_db()
    session_path, _ = _resolve_session_path(session_id)
    dest = session_path / f"audio{file_path.suffix}"
    if file_path != dest:
        import shutil
        shutil.copy2(file_path, dest)
    rel = str(dest.relative_to(DATA_ROOT))

    with db_cursor() as cur:
        cur.execute(
            "UPDATE sessions SET audio_path = ?, file_size = ?, status = 'uploaded' WHERE session_id = ?",
            (rel, file_size, session_id),
        )
    return get_session(session_id)


def update_transcript(session_id: str, transcript: str) -> dict:
    init_db()
    with db_cursor() as cur:
        cur.execute(
            "UPDATE sessions SET transcript = ? WHERE session_id = ?",
            (transcript, session_id),
        )
    return get_session(session_id)


async def summarize_session(session_id: str) -> dict:
    import time
    import logging
    init_db()
    s = get_session(session_id)
    if not s:
        raise ValueError(f"Session not found: {session_id}")
    transcript = s.get("transcript") or ""
    if not transcript.strip():
        raise ValueError("No transcript to summarize")

    cfg = get_config()
    llm = get_llm()
    prompt = load_prompt("summary.v0.1", transcript=transcript)
    t0 = time.perf_counter()
    resp = await llm.complete(prompt, cfg["model"], "summary.v0.1")
    if cfg.get("debug"):
        logging.getLogger("zyquraflow").info(
            "LLM call: prompt_id=summary.v0.1 model=%s params={} duration_ms=%.0f%s",
            cfg["model"],
            resp.duration_ms,
            " output_len=%d" % len(resp.text) if cfg.get("debug") else "",
        )

    # Parse and validate
    try:
        data = json.loads(resp.text)
    except json.JSONDecodeError:
        data = None

    valid, err = validate_summary(data) if data else (False, "Invalid JSON")
    if not valid:
        # Repair retry
        fix_prompt = load_prompt("fix_json.v0.1", invalid_json=resp.text)
        resp2 = await llm.complete(fix_prompt, cfg["model"], "fix_json.v0.1")
        try:
            data = json.loads(resp2.text)
        except json.JSONDecodeError:
            raise ValueError(f"Summary validation failed: {err}. Repair failed.")
        valid, err = validate_summary(data)
        if not valid:
            raise ValueError(f"Summary validation failed after repair: {err}")

    session_path, _ = _resolve_session_path(session_id)
    summary_path = session_path / "summary.json"
    summary_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    rel_summary = str(summary_path.relative_to(DATA_ROOT))

    with db_cursor() as cur:
        cur.execute(
            "UPDATE sessions SET summary_path = ?, status = 'summarized' WHERE session_id = ?",
            (rel_summary, session_id),
        )
    return get_session(session_id)


def link_session(session_id: str, case_id: str) -> None:
    from backend.storage import move_session_to_case
    init_db()
    with db_cursor() as cur:
        cur.execute("SELECT case_id FROM sessions WHERE session_id = ?", (session_id,))
        row = cur.fetchone()
    if not row:
        raise ValueError(f"Session not found: {session_id}")
    from_case = row["case_id"]
    move_session_to_case(session_id, from_case, case_id)
    with db_cursor() as cur:
        cur.execute("UPDATE sessions SET case_id = ? WHERE session_id = ?", (case_id, session_id))


def unlink_session(session_id: str) -> None:
    from backend.storage import move_session_to_case
    init_db()
    with db_cursor() as cur:
        cur.execute("SELECT case_id FROM sessions WHERE session_id = ?", (session_id,))
        row = cur.fetchone()
    if not row:
        raise ValueError(f"Session not found: {session_id}")
    from_case = row["case_id"]
    if from_case:
        move_session_to_case(session_id, from_case, "_unlinked")
    with db_cursor() as cur:
        cur.execute("UPDATE sessions SET case_id = NULL WHERE session_id = ?", (session_id,))
