from contextlib import asynccontextmanager

from fastapi import FastAPI

from apps.api.routers.v1 import router as v1_router
from nour.config.app_config import AppConfig
from nour.config.database_config import DatabaseConfig
from nour.infrastructure.database.connectdb import (
    create_database_async_engine,
    create_database_engine,
)
from nour.infrastructure.database.tables import create_all_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform any startup tasks here
    config = DatabaseConfig()

    engine_async = create_database_async_engine(config)
    engine_sync = create_database_engine(config)
    app.state.engine_async = engine_async
    app.state.engine_sync = engine_sync
    print("Application startup complete.")
    try:
        yield
    finally:
        await engine_async.dispose()
        engine_sync.dispose()
    # Perform any shutdown tasks here
    print("Shutting down the application...")


def create_app(config: AppConfig | None = None) -> FastAPI:

    if config is None:
        config = AppConfig()
    app = FastAPI(
        lifespan=lifespan,
        title=config.app_name,
        description="AI-powered Incident Investigation Platform",
        version=config.app_version,
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )
    app.include_router(v1_router, prefix="/api/v1")

    return app
