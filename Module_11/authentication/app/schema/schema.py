from typing import Optional

from pydantic import BaseModel


class AuthorSchemaBase(BaseModel):
    name: str


class AuthorSchemaResponse(AuthorSchemaBase):
    id: int

    class Config:
        orm_mode = True


class AuthorSchemaRequest(AuthorSchemaBase):
    pass


class BookSchemaBase(BaseModel):
    title: str
    year: Optional[int]


class BookSchemaResponse(BookSchemaBase):
    author_id: Optional[int]
    id: int

    class Config:
        orm_mode = True


class BookAllSchemaResponse(BookSchemaBase):
    id: int
    author: Optional[AuthorSchemaResponse]

    class Config:
        orm_mode = True


class BookSchemaRequest(BookSchemaBase):
    author_id: Optional[int]


class BookSchemaReport(BaseModel):
    author_name: str = None
    books_count: int
    earliest_year: int
    lastest_year: int


class AuthorBookSchemaResponse(BaseModel):
    author: AuthorSchemaResponse
    book: BookSchemaResponse
