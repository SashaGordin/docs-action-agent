from typing import Protocol

from pydantic import BaseModel


class ProviderError(Exception):
    ...


class ProviderTimeout(ProviderError):
    ...


class ProviderUsage(BaseModel):
    input_tokens: int
    output_tokens: int


class ProviderResult(BaseModel):
    answer: str
    usage: ProviderUsage


class TextProvider(Protocol):
    async def generate(self, question: str) -> ProviderResult: ...


class FakeTextProvider:
    def __init__(self, outcome: ProviderResult | ProviderError):
        self.outcome = outcome

    async def generate(self, question: str) -> ProviderResult:
        if isinstance(self.outcome, ProviderError):
            raise self.outcome
        return self.outcome

