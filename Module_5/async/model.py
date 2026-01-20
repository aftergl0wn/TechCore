import os
from dotenv import load_dotenv
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped,
    declared_attr, mapped_column
)

load_dotenv(".env")


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class Base(PreBase, DeclarativeBase):
    pass


engine = create_async_engine(os.environ["ASYNC_URL"])
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession)


class Book(Base):
    title: Mapped[str] = mapped_column(String(250))
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


class Author(Base):
    name: Mapped[str] = mapped_column(String(250))
