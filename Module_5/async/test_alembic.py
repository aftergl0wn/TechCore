
import os

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def container():
    with PostgresContainer("postgres:13") as postgres:
        url = postgres.get_connection_url().replace(
            "postgresql+psycopg2://", "postgresql+asyncpg://"
        )
        yield url


@pytest.fixture(scope="session")
def migrate(container):
    os.environ["ASYNC_URL"] = container
    config = Config("alembic.ini")
    config.set_main_option(
        "sqlalchemy.url", container
    )
    command.upgrade(config, "head")


@pytest_asyncio.fixture
async def async_session(migrate, container):
    engine = create_async_engine(container)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession)
    async with AsyncSessionLocal() as async_session:
        yield async_session


@pytest.mark.asyncio
async def test_tables_exist_after_migrations(async_session):
    result = await async_session.execute(
        text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
    )
    tables = [row[0] for row in result]
    assert "book" in tables
    assert "author" in tables
