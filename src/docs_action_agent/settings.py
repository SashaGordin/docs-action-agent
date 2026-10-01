import os

from pydantic import BaseModel, SecretStr


class Settings(BaseModel):
    model_api_key: SecretStr
    model_name: str


def load_settings() -> Settings:
    return Settings(
        model_api_key=os.environ["MODEL_API_KEY"],
        model_name=os.environ["MODEL_NAME"],
    )
