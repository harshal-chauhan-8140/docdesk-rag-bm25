from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Database configuration required by the application."""

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        hide_input_in_errors=True,
    )

    host: str = Field(min_length=1)
    port: int = Field(default=5432, ge=1, le=65535)
    user: str = Field(min_length=1)
    password: SecretStr = Field(min_length=1)
    name: str = Field(min_length=1)
