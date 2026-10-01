from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status

from docs_action_agent.models import QuestionRequest, QuestionResponse
from docs_action_agent.provider import (
    FakeTextProvider,
    ProviderResult,
    ProviderTimeout,
    ProviderUsage,
    TextProvider,
)
from docs_action_agent.usecase import generate_question

app = FastAPI()


def get_provider() -> TextProvider:
    usage = ProviderUsage(input_tokens=43, output_tokens=34)
    result = ProviderResult(answer="Its a biopic about Ted", usage=usage)
    return FakeTextProvider(outcome=result)


@app.post("/questions", response_model=QuestionResponse)
async def ask_question(
    request: QuestionRequest,
    provider: Annotated[TextProvider, Depends(get_provider)],
) -> QuestionResponse:
    try:
        return await generate_question(question=request.question, provider=provider)
    except ProviderTimeout as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Provider timed out",
        ) from exc


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
