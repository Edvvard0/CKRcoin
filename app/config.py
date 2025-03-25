import os
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: list[int]
    BASE_SITE: str

    DB_URL: str

    API_HOST: str
    API_PORT: int

    LOG_LEVEL: str

    MODE: Literal["TEST", "DEV", "PROD"]
    TEST_DB_URL: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )

    def get_webhook_url(self) -> str:
        return f"{self.BASE_SITE}/webhook"


settings = Settings()
database_url = settings.DB_URL
