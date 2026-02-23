"""Filesystem storage for sessions and cases."""
import shutil
import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional

from backend.config import DATA_ROOT


def ensure_data_root():
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    (DATA_ROOT / "cases").mkdir(exist_ok=True)


def generate_case_id(db_conn=None) -> str:
    """Generate next case ID. Pass DB conn to avoid reinit, or None to use default."""
    yyyy = datetime.now().strftime("%Y")
    from backend.db import get_conn, init_db
    init_db()
    conn = db_conn or get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM cases WHERE case_id LIKE ?",
        (f"CASE-{yyyy}-%",),
    )
    n = cur.fetchone()[0] + 1
    if not db_conn:
        conn.close()
    return f"CASE-{yyyy}-{n:04d}"


def generate_session_dir(case_id: Optional[str]) -> tuple:
    """Create session directory. Returns (full_path, session_id)."""
    ensure_data_root()
    session_id = f"SESSION-{uuid.uuid4().hex}"
    if case_id:
        case_dir = DATA_ROOT / "cases" / case_id
        case_dir.mkdir(parents=True, exist_ok=True)
        session_dir = case_dir / session_id
    else:
        session_dir = DATA_ROOT / "cases" / "_unlinked" / session_id
        session_dir.parent.mkdir(parents=True, exist_ok=True)
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir, session_id


def get_session_dir(case_id: str, session_id: str) -> Path:
    """Get path for an existing session."""
    return DATA_ROOT / "cases" / case_id / session_id


def get_unlinked_session_dir(session_id: str) -> Path:
    return DATA_ROOT / "cases" / "_unlinked" / session_id


def move_session_to_case(session_id: str, from_case: Optional[str], to_case: str) -> Path:
    """Move session directory from one case (or _unlinked) to another."""
    ensure_data_root()
    if from_case:
        src = DATA_ROOT / "cases" / from_case / session_id
    else:
        src = DATA_ROOT / "cases" / "_unlinked" / session_id
    dst_dir = DATA_ROOT / "cases" / to_case
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / session_id
    if src.exists():
        shutil.move(str(src), str(dst))
    else:
        dst.mkdir(parents=True, exist_ok=True)
    return dst

