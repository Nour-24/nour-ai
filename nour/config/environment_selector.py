import os
from typing import Literal

from dotenv import dotenv_values
from pydantic import TypeAdapter

Environment = Literal[
    "development",
    "testing",
    "staging",
    "production",
]


def get_environment() -> Environment:
    values = dotenv_values(".env")

    environment = os.getenv("ENVIRONMENT") or values.get("ENVIRONMENT") or "development"

    return TypeAdapter(Environment).validate_python(environment)


def get_env_file(environment: Environment) -> str | None:
    if environment == "production":
        return None

    return f".env.{environment}"
