from docs_action_agent.models import QuestionResponse
from docs_action_agent.provider import TextProvider


async def generate_question(question: str, provider: TextProvider) -> QuestionResponse:
    result = await provider.generate(question)
    return QuestionResponse(response=result.answer, status="answered")
