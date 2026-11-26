from typing import Any, Self

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

from nour.config.environment_selector import (
    Environment,
    get_env_file,
    get_environment,
)


class DatabaseConfig(BaseSettings):
    environment: Environment = Field(validation_alias="ENVIRONMENT")

    host: str = "localhost"
    port: int = Field(default=5432, ge=1, le=65535)
    user: str
    password: SecretStr
    name: str
    pool_size: int = Field(default=10, ge=1)
    max_overflow: int = Field(default=20, ge=0)
    echo: bool = False

    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
        hide_input_in_errors=True,
    )

    def __init__(
        self,
        environment: Environment | None = None,
        **kwargs: Any,
    ) -> None:
        selected_environment = get_environment() if environment is None else environment

        super().__init__(
            ENVIRONMENT=selected_environment,
            _env_file=get_env_file(selected_environment),
            **kwargs,
        )

    @model_validator(mode="after")
    def validate_database_name(self) -> Self:
        is_testing = self.environment == "testing"
        is_test_db = self.name.startswith("testing_")

        if is_testing and not is_test_db:
            raise ValueError("Testing database name must start with 'testing_'.")

        if not is_testing and is_test_db:
            raise ValueError("Test databases can only be used in testing.")

        return self

    @property
    def base_url(self) -> URL:
        return URL.create(
            drivername="postgresql",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.name,
        )

    @property
    def async_url(self) -> URL:
        return self.base_url.set(
            drivername="postgresql+asyncpg",
        )

    @property
    def sync_url(self) -> URL:
        return self.base_url.set(
            drivername="postgresql+psycopg2",
        )
