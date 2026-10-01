import pytest

from docs_action_agent.settings import load_settings


def test_load_settings_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("MODEL_API_KEY", "fake-test-key")
    monkeypatch.setenv("MODEL_NAME", "fake-test-model")

    settings = load_settings()

    assert settings.model_name == "fake-test-model"
    assert settings.model_api_key.get_secret_value() == "fake-test-key"


def test_missing_api_key_is_rejected(monkeypatch) -> None:
    monkeypatch.delenv("MODEL_API_KEY", raising=False)
    monkeypatch.setenv("MODEL_NAME", "fake-test-model")

    with pytest.raises(KeyError):
        load_settings()
