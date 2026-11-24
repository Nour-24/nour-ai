from fastapi import FastAPI

from .routers.v1 import router as v1_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Nour AI",
        description="AI-powered Incident Investigation Platform",
        version="0.1.0",
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )
    app.include_router(v1_router, prefix="/api/v1")

    return app
