import pytest
from sqlalchemy.orm import sessionmaker

from model import engine


@pytest.fixture
def db_session():
    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as session:
        yield session
