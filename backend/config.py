"""Configuration with defaults."""
import os
from pathlib import Path

# Data root - configurable via env
DATA_ROOT = Path(os.getenv("ZYQURAFLOW_DATA", str(Path(__file__).resolve().parent.parent / "data")))
DB_PATH = Path(__file__).resolve().parent / "zyquraflow.db"
PROMPTS_ROOT = Path(__file__).resolve().parent.parent / "prompts"

# Default LLM (für Mac Mini M4 / 8 GB empfohlen: llama3.2:3b oder phi3:mini)
DEFAULT_PROVIDER = "ollama"
DEFAULT_MODEL = "llama3.2:3b"
DEFAULT_DEBUG = False

# Whisper (Speech-to-Text): "base" für Mac M4 8 GB, "small" bei mehr RAM
WHISPER_MODEL = os.getenv("ZYQURAFLOW_WHISPER_MODEL", "base")
