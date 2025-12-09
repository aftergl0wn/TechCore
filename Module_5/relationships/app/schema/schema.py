from typing import Optional

from pydantic import BaseModel


class BookSchemaBase(BaseModel):
    author_id: Optional[int]
    title: str
    year: Optional[int]


class BookSchemaResponse(BookSchemaBase):
    id: int

    class Config:
        orm_mode = True


class BookSchemaRequest(BookSchemaBase):
    pass


class AuthorSchemaBase(BaseModel):
    name: str


class AuthorSchemaResponse(AuthorSchemaBase):
    id: int

    class Config:
        orm_mode = True


class AuthorSchemaRequest(AuthorSchemaBase):
    pass
