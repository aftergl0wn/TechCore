from typing import Optional

from pydantic import BaseModel


class BookSchemaBase(BaseModel):
    title: str
    year: Optional[int]


class BookSchemaResponse(BookSchemaBase):
    id: int

    class Config:
        orm_mode = True


class BookSchemaRequest(BookSchemaBase):
    pass


class BookSchemaUpdate(BookSchemaBase):
    title: Optional[str]
