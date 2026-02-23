"""Ollama LLM provider with mock fallback when Ollama is unavailable."""
import json
import time
from dataclasses import dataclass

import httpx

from backend.providers.base import LLMProvider, LLMResponse


@dataclass
class OllamaConfig:
    base_url: str = "http://localhost:11434"


class OllamaProvider(LLMProvider):
    def __init__(self, config: OllamaConfig | None = None):
        self.config = config or OllamaConfig()

    async def complete(self, prompt: str, model: str, prompt_id: str, **kwargs) -> LLMResponse:
        start = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                r = await client.post(
                    f"{self.config.base_url}/api/generate",
                    json={"model": model, "prompt": prompt, "stream": False},
                )
                if r.status_code != 200:
                    return self._mock_response(prompt, model, prompt_id, start)
                data = r.json()
                text = data.get("response", "")
        except Exception:
            return self._mock_response(prompt, model, prompt_id, start)
        duration_ms = (time.perf_counter() - start) * 1000
        return LLMResponse(text=text, model=model, prompt_id=prompt_id, duration_ms=duration_ms)

    def _mock_response(self, prompt: str, model: str, prompt_id: str, start: float) -> LLMResponse:
        """Return mocked JSON when Ollama is unavailable."""
        duration_ms = (time.perf_counter() - start) * 1000
        if "fix_json" in prompt_id:
            mock = {
                "title": "Corrected Summary",
                "participants": [],
                "key_points": ["Corrected from invalid JSON"],
                "action_items": [],
                "summary": "This is a mock response because Ollama was unavailable.",
            }
        else:
            mock = {
                "title": "Mock Summary (Ollama unavailable)",
                "participants": ["Unknown"],
                "key_points": ["Ollama is not running. Start Ollama to get real summaries."],
                "action_items": ["Install and run Ollama: https://ollama.ai"],
                "summary": "This is a mock summary. Ollama was not available when summarizing.",
            }
        return LLMResponse(
            text=json.dumps(mock, indent=2),
            model=model,
            prompt_id=prompt_id,
            duration_ms=duration_ms,
        )
