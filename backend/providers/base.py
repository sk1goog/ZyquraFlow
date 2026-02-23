"""LLM provider interface."""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str
    model: str
    prompt_id: str
    duration_ms: float


class LLMProvider(ABC):
    @abstractmethod
    async def complete(self, prompt: str, model: str, prompt_id: str, **kwargs) -> LLMResponse:
        pass
