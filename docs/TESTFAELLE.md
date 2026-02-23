# Testfälle – ZyquraFlow

Alle Tests sind **automatisiert** ausführbar. Nach größeren Änderungen beide Test-Suiten laufen lassen.

---

## 1. Backend-Tests (pytest)

**Ausführung (im Projektroot):**
```bash
npm run test:backend
```
(Dabei wird `PYTHONPATH=.` gesetzt; Python sollte die Backend-Abhängigkeiten haben, z. B. nach `source backend/.venv/bin/activate` und `pip install -r backend/requirements.txt`.)

**Voraussetzung:** `pip install -r backend/requirements.txt` (enthält pytest, pytest-asyncio).

### Abgedeckte Funktionalität

| Bereich | Testdatei | Testfälle |
|--------|-----------|-----------|
| **System** | `test_api_system.py` | Health liefert status/provider/ollama_available; Config lesen/patchen; Provider-Liste |
| **Sitzungen** | `test_api_sessions.py` | Sitzung anlegen; Liste (leer → eine); Einzelsitzung abrufen; 404 bei unbekannter ID; Transkript aktualisieren; Audio-Upload (Stub); Unlink |
| **Sitzungen (Summarize)** | `test_api_summarize.py` | Zusammenfassen mit gemocktem LLM → Session mit summary; 400 ohne Transkript; 400 bei unbekannter Session |
| **Fälle** | `test_api_cases.py` | Fall anlegen; Liste (leer → einer); Fall abrufen; 404; Sitzung verknüpfen; 404 bei unbekanntem Fall; Unlink und erneutes Verknüpfen mit anderem Fall |
| **Schema** | `test_schema.py` | Summary-JSON: gültig; fehlendes Feld; kein Dict; participants nur Liste von Strings |

**Isolation:** Jeder Test nutzt ein eigenes temporäres Verzeichnis und eine eigene SQLite-Datei (`conftest.py`), keine echten Daten.

---

## 2. Frontend-Tests (Vitest + React Testing Library)

**Ausführung:**
```bash
npm run test
```
Watch-Modus (bei Änderungen neu laufen):
```bash
npm run test:watch
```

### Abgedeckte Funktionalität

| Komponente | Testdatei | Testfälle |
|------------|-----------|-----------|
| **App** | `App.test.tsx` | Navigation zeigt Sitzungen, Fälle, Berichte, System; Topbar-Titel „Sitzungen“; Marke „ZyquraFlow“ im Seitenbereich |
| **SessionsScreen** | `SessionsScreen.test.tsx` | „Sitzung anlegen“-Button sichtbar; listSessions wird aufgerufen; Nach Klick auf „Sitzung anlegen“ erscheint neue Sitzung in der Liste (API gemockt) |

Die API-Aufrufe werden in den Frontend-Tests gemockt (`vi.mock('@core/api/client')`), es wird kein Backend benötigt.

---

## 3. Alle Tests auf einmal

- **Backend:** `npm run test:backend`
- **Frontend:** `npm run test`

Beide nacheinander ausführen (z. B. in CI oder vor jedem Commit):
```bash
npm run test:backend && npm run test
```

---

## 4. Erweiterung

- **Backend:** Neue API-Endpunkte oder Services in `backend/tests/` abdecken (gleiche Fixtures: `client`, isolierte DB/Data).
- **Frontend:** Neue Screens/Komponenten in `*.test.tsx` mit `@testing-library/react` testen; API weiter mit `vi.mock('@core/api/client')` mocken.

Diese Datei bei neuen Testfällen anpassen.
