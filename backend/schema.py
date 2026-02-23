"""JSON schema for summary validation."""
from typing import Any, Optional, Tuple

SUMMARY_SCHEMA = {
    "type": "object",
    "required": ["title", "participants", "key_points", "action_items", "summary"],
    "properties": {
        "title": {"type": "string"},
        "participants": {"type": "array", "items": {"type": "string"}},
        "key_points": {"type": "array", "items": {"type": "string"}},
        "action_items": {"type": "array", "items": {"type": "string"}},
        "summary": {"type": "string"},
    },
}


def validate_summary(data: Any) -> Tuple[bool, Optional[str]]:
    """Validate summary against schema. Returns (valid, error_msg)."""
    if not isinstance(data, dict):
        return False, "Expected object"
    for key in ["title", "participants", "key_points", "action_items", "summary"]:
        if key not in data:
            return False, f"Missing required field: {key}"
    if not isinstance(data["title"], str):
        return False, "title must be string"
    if not isinstance(data["participants"], list) or not all(isinstance(x, str) for x in data["participants"]):
        return False, "participants must be list of strings"
    if not isinstance(data["key_points"], list) or not all(isinstance(x, str) for x in data["key_points"]):
        return False, "key_points must be list of strings"
    if not isinstance(data["action_items"], list) or not all(isinstance(x, str) for x in data["action_items"]):
        return False, "action_items must be list of strings"
    if not isinstance(data["summary"], str):
        return False, "summary must be string"
    return True, None
