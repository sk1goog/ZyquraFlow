"""FastAPI application."""
import tempfile
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel

from backend.db import init_db
from backend.services import session_service, case_service
from backend.llm import get_config, set_config

app = FastAPI(title="ZyquraFlow API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TranscriptBody(BaseModel):
    transcript: str


class CaseCreateBody(BaseModel):
    alias: str


class ConfigPatchBody(BaseModel):
    provider: Optional[str] = None
    model: Optional[str] = None
    debug: Optional[bool] = None


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    """Provider health check."""
    cfg = get_config()
    ollama_available = False
    try:
        import httpx
        r = httpx.get("http://localhost:11434/api/tags", timeout=2.0)
        ollama_available = r.status_code == 200
    except Exception:
        pass
    return {
        "status": "ok",
        "provider": cfg["provider"],
        "ollama_available": ollama_available,
    }


@app.get("/api/system/config")
def get_system_config():
    return get_config()


@app.patch("/api/system/config")
def patch_system_config(body: ConfigPatchBody):
    set_config(provider=body.provider, model=body.model, debug=body.debug)
    return get_config()


@app.get("/api/system/providers")
def list_providers():
    return [
        {"id": "ollama", "name": "Ollama", "models": ["llama3.2", "llama3.1", "mistral", "codellama"]},
    ]


@app.post("/api/sessions")
def create_session():
    return session_service.create_session(case_id=None)


@app.get("/api/sessions")
def list_sessions(case_id: Optional[str] = None):
    return session_service.list_sessions(case_id=case_id)


@app.get("/api/sessions/{session_id}")
def get_session(session_id: str):
    s = session_service.get_session(session_id)
    if not s:
        raise HTTPException(404, "Session not found")
    return s


@app.post("/api/sessions/{session_id}/audio")
async def upload_audio(session_id: str, file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(400, "No file")
    ext = Path(file.filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = Path(tmp.name)
    try:
        s = session_service.update_audio(session_id, tmp_path, len(content))
        return s
    finally:
        tmp_path.unlink(missing_ok=True)


@app.put("/api/sessions/{session_id}/transcript")
def update_transcript(session_id: str, body: TranscriptBody):
    return session_service.update_transcript(session_id, body.transcript)


@app.post("/api/sessions/{session_id}/summarize")
async def summarize(session_id: str):
    try:
        s = await session_service.summarize_session(session_id)
        return s
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.post("/api/sessions/{session_id}/unlink")
def unlink(session_id: str):
    try:
        session_service.unlink_session(session_id)
        return {}
    except ValueError as e:
        raise HTTPException(404, str(e))


@app.get("/api/cases")
def list_cases():
    return case_service.list_cases()


@app.post("/api/cases")
def create_case(body: CaseCreateBody):
    return case_service.create_case(body.alias)


@app.get("/api/cases/{case_id}")
def get_case(case_id: str):
    c = case_service.get_case(case_id)
    if not c:
        raise HTTPException(404, "Case not found")
    return c


@app.post("/api/cases/{case_id}/sessions/{session_id}")
def link_session(case_id: str, session_id: str):
    try:
        session_service.link_session(session_id, case_id)
        return {}
    except ValueError as e:
        raise HTTPException(404, str(e))
