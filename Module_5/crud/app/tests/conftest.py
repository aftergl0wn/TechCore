import os
from pathlib import Path

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)
from sqlalchemy.pool import NullPool
from testcontainers.postgres import PostgresContainer


@pytest.fixture
def value():
    return {
        "title": "War and peace",
        "year": 1867
    }


@pytest.fixture(scope="session")
def container():
    with PostgresContainer("postgres:13") as postgres:
        url = postgres.get_connection_url().replace(
            "postgresql+psycopg2://", "postgresql+asyncpg://"
        )
        yield url


@pytest.fixture(scope="session", autouse=True)
def migrate(container):
    os.environ["ASYNC_URL"] = container
    app_dir = Path(__file__).parent.parent
    config = Config(str(app_dir / "alembic.ini"))
    config.set_main_option("script_location", str(app_dir / "alembic"))
    config.set_main_option(
        "sqlalchemy.url", container
    )
    command.upgrade(config, "head")


@pytest_asyncio.fixture(autouse=True)
async def cleanup_db():
    yield
    from app import model
    async with model.session_maker() as session:
        await session.execute(
            text("TRUNCATE TABLE book RESTART IDENTITY CASCADE")
        )
        await session.commit()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db_engine(container):
    from app import model
    model.engine = create_async_engine(container, poolclass=NullPool)
    model.session_maker = async_sessionmaker(model.engine, class_=AsyncSession)


@pytest_asyncio.fixture
async def async_client():
    from main import app
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as async_client:
        yield async_client
