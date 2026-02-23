# ZyquraFlow

Local-first desktop prototype for session management, case linking, and transcript summarization.

## Tech Stack

- **Frontend:** Tauri + React + TypeScript + Vite
- **Backend:** Python FastAPI + Uvicorn
- **DB:** SQLite (in `backend/`)
- **Storage:** `data/` directory at repo root
- **LLM:** Ollama (mock fallback if unavailable)

## Prerequisites

- **Node.js** 18+ and npm
- **Rust** (for Tauri) — [install](https://rustup.rs/)
- **Python** 3.11+ and pip/venv

## Step 1: Run the backend

From the **repo root**:

```bash
python -m venv backend/.venv
source backend/.venv/bin/activate   # Windows: backend\.venv\Scripts\activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the script: `./scripts/run-backend.sh`

Backend runs at `http://localhost:8000`.

## Step 2: Run the Tauri app

In a separate terminal, from repo root:

```bash
npm install
npm run tauri dev
```

This starts the Vite dev server and opens the Tauri window. The app talks to the backend at `http://localhost:8000` (configurable via `VITE_BACKEND_URL`).

## Project structure

```
ZyquraFlow/
├── docs/
│   └── FOUNDATION.md      # Project rules
├── prompts/
│   ├── summary_v01.md     # summary.v0.1
│   └── fix_json_v01.md    # fix_json.v0.1
├── src/                   # Frontend
│   ├── ui-kit/            # Design tokens + components
│   ├── core/              # Config, API client
│   ├── modules/
│   │   ├── sessions/      # Sessions screen
│   │   ├── cases/         # Cases screen
│   │   ├── reports/       # Placeholder
│   │   └── system/        # Provider, debug, health
│   └── App.tsx
├── src-tauri/             # Tauri (Rust)
├── backend/               # FastAPI
│   ├── main.py
│   ├── db.py
│   ├── storage.py
│   ├── prompts.py
│   ├── schema.py
│   ├── llm.py
│   ├── providers/         # Ollama + mock
│   └── services/
└── data/                  # Created at runtime
    └── cases/
        ├── CASE-YYYY-####/
        │   └── SESSION-<uuid>/
        │       ├── audio.<ext>
        │       └── summary.json
        └── _unlinked/     # Sessions not in a case
```

## Tests

- **Backend (pytest):** `npm run test:backend` — 26 API- und Schema-Tests (isolierte Temp-DB/Data).
- **Frontend (Vitest):** `npm run test` — 5 Komponenten-Tests (API gemockt).
- Beide nacheinander: `npm run test:backend && npm run test`

Details und Erweiterung: [docs/TESTFAELLE.md](docs/TESTFAELLE.md).

## Usage

1. **Sessions:** Create session → upload audio → paste transcript → Summarize
2. **Cases:** Create case (alias) → link sessions
3. **System:** Select Ollama model, toggle debug, check provider health

If Ollama is not running, summarization returns a mock response but keeps the pipeline the same.

## Ollama / Mac Mini M4

Die App nutzt **Ollama** lokal. Standardmodell ist **llama3.2:3b** (geeignet für Mac Mini M4 mit 8 GB RAM).

- **Empfohlen bei 8 GB:** `llama3.2:3b` oder `phi3:mini` (unter System → Anbieter & Modell wählbar).
- **Bei 16 GB RAM:** z. B. `llama3.2` (7B) oder `mistral` für bessere Qualität.
- Modelle installieren: `ollama pull llama3.2:3b` bzw. `ollama pull phi3:mini`.
