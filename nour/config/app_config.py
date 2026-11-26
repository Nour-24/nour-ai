from typing import Any, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

from nour.config.environment_selector import (
    Environment,
    get_env_file,
    get_environment,
)


class AppConfig(BaseSettings):
    environment: Environment

    app_name: str = "NOUR AI"
    app_version: str = "0.1.0"
    app_description: str = "AI-powered Incident Investigation Platform"

    debug: bool = False

    log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )

    def __init__(
        self,
        environment: Environment | None = None,
        **kwargs: Any,
    ) -> None:
        selected_environment = get_environment() if environment is None else environment

        super().__init__(
            environment=selected_environment,
            _env_file=get_env_file(selected_environment),
            **kwargs,
        )
