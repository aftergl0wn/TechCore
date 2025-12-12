from pydantic import BaseModel

from app.schema.schema_book_author import BookSchemaResponse
from app.schema.schema_review import ReviewResponseSchema


class BookReviewSchema(BaseModel):
    book: BookSchemaResponse
    reviews: list[ReviewResponseSchema]
