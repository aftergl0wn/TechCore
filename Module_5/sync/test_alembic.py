
import os

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def container():
    with PostgresContainer("postgres:13") as postgres:
        yield postgres.get_connection_url()


@pytest.fixture(scope="session")
def migrate(container):
    os.environ["SYNC_URL"] = container
    config = Config("alembic.ini")
    config.set_main_option(
        "sqlalchemy.url", container
    )
    command.upgrade(config, "head")


@pytest.fixture(scope="session")
def session(migrate, container):
    engine = create_engine(container)
    SessionLocal = sessionmaker(engine, class_=Session)
    with SessionLocal() as session:
        yield session
    engine.dispose()


def test_tables_exist_after_migrations(session):
    result = session.execute(
        text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
    )
    tables = [row[0] for row in result]
    assert "book" in tables
    assert "author" in tables
