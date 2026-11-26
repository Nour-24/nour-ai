from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)

from nour.config.database_config import DatabaseConfig


def create_database_async_engine(config: DatabaseConfig) -> AsyncEngine:
    engine = create_async_engine(
        config.async_url,
        pool_size=config.pool_size,
        max_overflow=config.max_overflow,
        echo=config.echo,
    )
    return engine


def create_database_engine(config: DatabaseConfig) -> Engine:
    engine = create_engine(
        config.sync_url,
        pool_size=config.pool_size,
        max_overflow=config.max_overflow,
        echo=config.echo,
    )
    return engine


async def check_async_database_connection(engine: AsyncEngine) -> None:
    async with engine.connect() as connection:
        await connection.execute("SELECT 1")


def check_sync_database_connection(engine: Engine) -> None:
    with engine.connect() as connection:
        connection.execute("SELECT 1")
