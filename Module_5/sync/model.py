import os
from dotenv import load_dotenv

from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import (
    Mapped, Session, declared_attr,
    declarative_base, mapped_column, sessionmaker
)

load_dotenv(".env")


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


Base = declarative_base(cls=Base)
engine = create_engine(os.environ["DATABASE_URL"])
SessionLocal = sessionmaker(engine, class_=Session)


class Book(Base):
    __tablename__ = "book"

    title: Mapped[str] = mapped_column(String(20))
    year: Mapped[int]


class Author(Base):
    __tablename__ = "author"

    name: Mapped[str] = mapped_column(String(20))
