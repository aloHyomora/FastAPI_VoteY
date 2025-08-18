from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "VoteY API"
    API_PREFIX: str = "/api"
    API_KEY: str = "change-me"

    OUTBOUND_BASE_URL: str = "http://localhost:8000/api"
    OUTBOUND_API_KEY: str | None = None
    REQUEST_TIMEOUT: float = 5.0

    # HMAC 서명
    HMAC_SECRET: str | None = None          # 예: very-secret-shared-key
    CLOCK_SKEW_SECONDS: int = 300           # 허용 시간 오차(초)

    DATA_DIR: str = Field(default="app/data/json")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
# Optionally resolve to Path elsewhere