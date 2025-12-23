import os
from dotenv import load_dotenv

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import (
    Mapped, declared_attr,
    declarative_base, mapped_column, relationship
)
from typing import AsyncGenerator

load_dotenv()


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


Base = declarative_base(cls=Base)
engine = create_async_engine(
    os.environ.get("ASYNC_URL", "postgresql+asyncpg://user:mysecretpassword@db:5432/fastapi").strip(),
    echo=True
)
session_maker = async_sessionmaker(engine, class_=AsyncSession)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as async_session:
        yield async_session


class Book(Base):
    __tablename__ = "book"

    title: Mapped[str] = mapped_column(String(20))
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("author.id"),
        nullable=True
    )
    author: Mapped["Author"] = relationship(back_populates="books")


class Author(Base):
    __tablename__ = "author"

    name: Mapped[str] = mapped_column(String(20))
    books: Mapped[list["Book"]] = relationship(back_populates="author")
