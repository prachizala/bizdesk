import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "BizDesk"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "bizdesk-secure-owner-token-secret-32-chars")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 720
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./bizdesk.db")
    DEFAULT_CURRENCY: str = "INR"
    DEFAULT_TAX_RATE: float = 18.0

    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings()
