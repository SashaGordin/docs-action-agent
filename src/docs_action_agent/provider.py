from typing import Protocol

from pydantic import BaseModel

from docs_action_agent.agent_loop import AgentAction, ToolExecutionResult


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

class ScriptedAgentProvider:
    def __init__(self, outcomes: list[AgentAction]):
        self.outcomes = outcomes

    async def generate(
        self, question: str, tool_results: tuple[ToolExecutionResult, ...]
    ) -> AgentAction:
        return self.outcomes.pop(0)
