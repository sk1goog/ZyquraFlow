# Fix JSON Prompt v0.1

**ID:** `fix_json.v0.1`

The following text was intended to be valid JSON but has errors. Extract and fix it to match this schema:

```json
{
  "title": "string",
  "participants": ["string"],
  "key_points": ["string"],
  "action_items": ["string"],
  "summary": "string"
}
```

Output ONLY the corrected JSON, no other text.

Invalid output:
---
{invalid_json}
---
