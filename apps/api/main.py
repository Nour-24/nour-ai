from fastapi import FastAPI

from apps.api.routers.v1 import router as v1_router
from nour.config.app_config import AppConfig


def create_app(config: AppConfig | None = None) -> FastAPI:

    if config is None:
        config = AppConfig()
    app = FastAPI(
        title=config.app_name,
        description="AI-powered Incident Investigation Platform",
        version=config.app_version,
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )
    app.include_router(v1_router, prefix="/api/v1")

    return app
