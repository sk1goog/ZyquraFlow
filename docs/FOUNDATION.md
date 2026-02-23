# FOUNDATION (Evergreen Rules) — v0.1

This file is the project's constitution. All changes MUST comply.

## Hard Rules

1. **UI never touches DB/files/LLM directly.** UI calls backend Services/UseCases only via typed API client.
2. **Repo structure is hybrid:**
   - `ui-kit/` — design tokens + reusable UI components
   - `core/` — config, provider registry, logging, interfaces
   - `infra/` — sqlite, storage, llm adapters
   - `modules/<feature>/` — sessions, cases, reports, system
   - `prompts/` — prompt files referenced by ID
   - `backend/` — FastAPI app, db, providers, storage
3. **UI-Kit-first:** recurring UI patterns must be moved into ui-kit. No parallel styling systems.
4. **Prompts live ONLY in /prompts** and are referenced by IDs. No prompt text in UI/services.
5. **LLM outputs structured JSON.** Backend validates against schema; invalid → repair/retry; never store invalid.
6. **Storage is dual:** SQLite = metadata index, filesystem = content archive under `data/`.
7. **Local-first is default;** cloud is optional, never required.
8. **Debug mode exists:** logs prompt-id, model, params, timing (and optional output). Normal mode minimal logs.
9. **Domain logic must be testable** without UI; core logic gets unit tests.
10. **Prototypes are built inside final structure** (no throwaway folders). Minimal slice is allowed, but structure stays.

## v0.1 Modules

- **Sessions:** audio upload + metadata + manual transcript + summarize → summary.json
- **Cases:** create case (CASE-YYYY-#### + alias) + link sessions + list sessions per case
- **Reports:** placeholder screen
- **System:** provider/model selection + debug toggle + provider status

## Data layout (v0.1)

```
data/cases/CASE-YYYY-####/SESSION-<uuid>/
  audio.<ext>
  summary.json
```

SQLite stores: session_id, case_id (nullable), created_at, audio_path, summary_path, file_size, duration (optional), status.

## Tech Stack

- **Frontend:** Tauri + React + TypeScript + Vite
- **Styling:** ui-kit with CSS variables (design tokens) + reusable components
- **Backend:** Python FastAPI + Uvicorn
- **DB:** SQLite (file in backend folder)
- **LLM:** provider abstraction; OllamaProvider as default (mock fallback if unavailable)
