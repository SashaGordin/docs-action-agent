import pytest
from pydantic import ValidationError

from docs_action_agent.models import QuestionRequest, QuestionResponse


def test_valid_question_accepted() -> None:
    question_text = "Does this work?"
    question_request = QuestionRequest(question=question_text)
    assert question_request.question == question_text


def test_missing_question_rejected() -> None:
    with pytest.raises(ValidationError):
        QuestionRequest()


def test_integer_question_rejected() -> None:
    with pytest.raises(ValidationError):
        QuestionRequest(question=43)


def test_result_serializes() -> None:
    result_text = "yes it does"
    result_status = "answered"
    expected_result = {"response": "yes it does", "status": "answered"}

    response = QuestionResponse(response=result_text, status=result_status)
    model_response = response.model_dump()

    assert model_response == expected_result


def test_unsupported_result_status() -> None:
    with pytest.raises(ValidationError):
        QuestionResponse(response="Yeah this won't work", status="Failed")


def test_blank_question_rejected() -> None:
    with pytest.raises(ValidationError):
        QuestionRequest(question="")


def test_whitespace_only_question_rejected() -> None:
    with pytest.raises(ValidationError):
        QuestionRequest(question=" ")
