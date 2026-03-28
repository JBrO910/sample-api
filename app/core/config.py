from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration settings.

    Values are loaded from environment variables or .env file.
    """

    DATABASE_URL: str
    RATE_LIMIT_SECONDS: int = 10
    DISABLE_RATE_LIMIT: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()