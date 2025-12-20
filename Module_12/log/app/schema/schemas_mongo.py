from typing import Optional

from pydantic import BaseModel, Field


class ReviewBaseSchema(BaseModel):
    product_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str]


class ReviewResponseSchema(ReviewBaseSchema):
    id: str = Field(..., alias="_id")

    class Config:
        allow_population_by_field_name = True


class ReviewRequestSchema(ReviewBaseSchema):
    pass


class ReviewUpdateSchema(ReviewBaseSchema):
    product_id: Optional[str]
    rating: Optional[int] = Field(None, ge=1, le=5)
