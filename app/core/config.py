from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "VoteY API"
    API_PREFIX: str = "/api"
    API_KEY: str = "change-me"  # .env로 덮어쓰기
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()