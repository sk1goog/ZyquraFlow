"""Load prompts by ID from prompts/ directory."""
from pathlib import Path

from backend.config import PROMPTS_ROOT

PROMPT_IDS = {
    "summary.v0.1": "summary_v01.md",
    "fix_json.v0.1": "fix_json_v01.md",
}


def load_prompt(prompt_id: str, **kwargs: str) -> str:
    """Load prompt by ID and format with kwargs."""
    filename = PROMPT_IDS.get(prompt_id)
    if not filename:
        raise ValueError(f"Unknown prompt ID: {prompt_id}")
    path = PROMPTS_ROOT / filename
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    text = path.read_text(encoding="utf-8")
    # Simple placeholder replacement {key}
    for k, v in kwargs.items():
        text = text.replace("{" + k + "}", str(v))
    return text
