"""Configuration with defaults."""
import os
from pathlib import Path

# Data root - configurable via env
DATA_ROOT = Path(os.getenv("ZYQURAFLOW_DATA", str(Path(__file__).resolve().parent.parent / "data")))
DB_PATH = Path(__file__).resolve().parent / "zyquraflow.db"
PROMPTS_ROOT = Path(__file__).resolve().parent.parent / "prompts"

# Default LLM
DEFAULT_PROVIDER = "ollama"
DEFAULT_MODEL = "llama3.2"
DEFAULT_DEBUG = False
