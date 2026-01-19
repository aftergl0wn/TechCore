from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import (
    Mapped, declared_attr,
    declarative_base, mapped_column
)


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


engine = create_engine("sqlite:///:memory:")
Base = declarative_base(cls=Base)


class Book(Base):
    __tablename__ = "book"

    title: Mapped[str] = mapped_column(String(20))
    year: Mapped[int] = mapped_column(Integer, nullable=True)


Base.metadata.create_all(engine)
