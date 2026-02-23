# ZyquraFlow – Projektstruktur & Technology Stack

Übersicht der Verzeichnisstruktur und der verwendeten Technologien (relevant für Stack-Beurteilung).

---

## Verzeichnisbaum (relevant für den Stack)

```
ZyquraFlow/
├── docs/
│   ├── FOUNDATION.md          # Projektregeln, Konstitution
│   └── PROJECT-STRUCTURE.md   # Diese Datei
├── prompts/                   # LLM-Prompts (nur IDs, keine Logik)
│   ├── summary_v01.md         # ID: summary.v0.1
│   └── fix_json_v01.md       # ID: fix_json.v0.1
├── backend/                   # Python FastAPI-Backend
│   ├── __init__.py
│   ├── config.py              # DATA_ROOT, DB_PATH, Defaults
│   ├── db.py                  # SQLite, init_db, db_cursor
│   ├── llm.py                 # Provider-Registry, get_config/set_config
│   ├── main.py                # FastAPI-App, alle REST-Endpunkte
│   ├── prompts.py             # Prompt-Loader (lädt aus /prompts)
│   ├── schema.py              # JSON-Schema-Validierung Summary
│   ├── storage.py             # Dateisystem: cases/sessions
│   ├── requirements.txt       # Python-Abhängigkeiten
│   ├── providers/
│   │   ├── base.py            # LLMProvider-Interface
│   │   ├── ollama.py          # Ollama + Mock-Fallback
│   │   └── __init__.py
│   └── services/
│       ├── session_service.py # Sessions: CRUD, Upload, Summarize
│       ├── case_service.py    # Cases: CRUD, Link/Unlink
│       └── __init__.py
├── src/                       # Frontend (React + TypeScript)
│   ├── index.css              # Globale Styles, Tokens-Import
│   ├── main.tsx               # React-Einstieg
│   ├── App.tsx                # Layout, Navigation, Screen-Routing
│   ├── ui-kit/                # Design-System
│   │   ├── tokens.css         # CSS-Variablen (Farben, Typo, Spacing)
│   │   ├── Button.tsx/.css
│   │   ├── Input.tsx, TextArea, Card, Sidebar, Topbar, PageLayout
│   │   └── index.ts           # Re-Exports
│   ├── core/
│   │   ├── config.ts          # Backend-URL (VITE_BACKEND_URL)
│   │   └── api/
│   │       ├── client.ts      # Fetch-API-Client (alle Endpunkte)
│   │       └── types.ts       # DTOs (SessionDto, CaseDto, …)
│   └── modules/
│       ├── sessions/          # SessionsScreen (Upload, Transcript, Summarize)
│       ├── cases/             # CasesScreen (Create, Link/Unlink)
│       ├── reports/           # ReportsScreen (Platzhalter)
│       └── system/             # SystemScreen (Provider, Debug, Health)
├── src-tauri/                 # Tauri (Rust) – Desktop-Hülle
│   ├── Cargo.toml             # Rust-Abhängigkeiten (tauri, …)
│   ├── tauri.conf.json        # App-Name, Bundle-ID, Build-Config
│   ├── build.rs
│   ├── src/
│   │   ├── main.rs
│   │   └── lib.rs
│   ├── capabilities/          # Tauri-Berechtigungen
│   └── icons/                 # App-Icons (PNG, icns, ico)
├── public/
├── scripts/
│   └── run-backend.sh         # Backend starten (venv + uvicorn)
├── index.html                 # Vite-Einstieg
├── package.json               # npm: React, Vite, Tauri CLI, Scripts
├── vite.config.ts             # Vite + React, Path-Aliase (@ui-kit, …)
├── tsconfig.json / tsconfig.app.json / tsconfig.node.json
├── eslint.config.js
└── README.md
```

**Nicht im Baum (Runtime/Generated):**  
`node_modules/`, `backend/.venv/`, `src-tauri/target/`, `dist/`, `data/` (wird zur Laufzeit befüllt).

---

## Technology Stack – Kurzüberblick

| Schicht        | Technologie        | Zweck |
|----------------|--------------------|--------|
| **Desktop-App**| Tauri 2 + Rust     | Native Hülle, Fenster, kein Electron |
| **Frontend**   | React 18+ + TypeScript | UI-Logik, Komponenten |
| **Build (Frontend)** | Vite 7        | Dev-Server, Bundling, HMR |
| **Styling**    | CSS (Design Tokens in `tokens.css`) | Kein Tailwind/Bootstrap, eigene Komponenten |
| **Backend**    | Python 3.9+        | Laufzeit Backend |
| **API**        | FastAPI + Uvicorn  | REST-API, CORS |
| **Datenbank**  | SQLite             | Metadaten (Sessions, Cases), Datei im Backend |
| **Speicher**   | Dateisystem        | `data/cases/…` (Audio, summary.json) |
| **LLM**        | Ollama (optional)  | Summarization; bei Ausfall: Mock-Antworten |

---

## Datenfluss (für Erklärung)

- **UI** ruft nur das **Backend** über den **API-Client** (`src/core/api/client.ts`) auf.
- **Backend** nutzt **Services** (session_service, case_service), **DB** (SQLite), **Storage** (Dateien), **LLM** (Ollama/Mock).
- **Prompts** liegen nur unter `prompts/` und werden per ID geladen (`summary.v0.1`, `fix_json.v0.1`).
- **Tauri** lädt das gebaute Frontend (Vite-Build) und zeigt es in einem nativen Fenster.

---

## Wichtige Konfigurationsdateien

- **Backend-URL (Frontend):** `src/core/config.ts` bzw. Env `VITE_BACKEND_URL` (Default: `http://localhost:8000`).
- **Datenpfad (Backend):** `backend/config.py`, Env `ZYQURAFLOW_DATA` (Default: Repo-Root `data/`).
- **Tauri:** `src-tauri/tauri.conf.json` (identifier, build, icons).

Diese MD-Datei kann man nutzen, um den Stack und die Struktur Schritt für Schritt zu erklären oder erklären zu lassen.
