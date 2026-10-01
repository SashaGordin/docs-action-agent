import pytest
from fastapi.testclient import TestClient

from docs_action_agent.api import app, get_provider
from docs_action_agent.provider import FakeTextProvider, ProviderResult, ProviderTimeout

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_questions_endpoint() -> None:
    response = client.post("/questions", json={"question": "what is FastAPI?"})
    assert response.status_code == 200
    assert response.json() == {
        "response": "Its a biopic about Ted",
        "status": "answered",
    }


def test_timeout_questions_endpoint() -> None:
    timeout_provider = FakeTextProvider(outcome=ProviderTimeout("provider timed out"))

    app.dependency_overrides[get_provider] = lambda: timeout_provider

    try:
        response = client.post("/questions", json={"question": "what is FastAPI?"})
        assert response.status_code == 504
        assert response.json() == {"detail": "Provider timed out"}
    finally:
        app.dependency_overrides.clear()


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"question": ""},
        {"question": " "},
        {"question": 43},
    ],
)
def test_invalid_question_returns_422(payload: object) -> None:
    response = client.post("/questions", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"]


class UnexpectedFailureProvider:
    async def generate(self, question: str) -> ProviderResult:
        raise RuntimeError("sensitive internal detail")


def test_unexpected_failure_provider() -> None:
    unexpected_provider = UnexpectedFailureProvider()

    app.dependency_overrides[get_provider] = lambda: unexpected_provider

    error_client = TestClient(app, raise_server_exceptions=False)

    try:
        response = error_client.post(
            "/questions", json={"question": "what is FastAPI?"}
        )
        assert response.status_code == 500
        assert response.text == "Internal Server Error"
        assert "sensitive internal detail" not in response.text
    finally:
        app.dependency_overrides.clear()
