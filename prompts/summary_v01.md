# Summary Prompt v0.1

**ID:** `summary.v0.1`

Summarize the following transcript into structured JSON. Output ONLY valid JSON matching this schema:

```json
{
  "title": "string",
  "participants": ["string"],
  "key_points": ["string"],
  "action_items": ["string"],
  "summary": "string"
}
```

Rules:
- `title`: A brief descriptive title (1-10 words)
- `participants`: List of participant names mentioned
- `key_points`: Bullet points of main topics discussed
- `action_items`: Tasks or follow-ups identified
- `summary`: 2-4 sentence executive summary

Transcript:
---
{transcript}
---
