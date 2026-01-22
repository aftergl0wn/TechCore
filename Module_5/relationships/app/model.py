import os
from dotenv import load_dotenv
from typing import AsyncGenerator, Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped,
    declared_attr, mapped_column, relationship
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
session_maker = async_sessionmaker(engine, class_=AsyncSession)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as async_session:
        yield async_session


class Book(Base):
    title: Mapped[str] = mapped_column(String(250))
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    author_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("author.id"),
        nullable=True
    )
    author: Mapped["Author"] = relationship(back_populates="books")


class Author(Base):
    name: Mapped[str] = mapped_column(String(250))
    books: Mapped[list["Book"]] = relationship(back_populates="author")
