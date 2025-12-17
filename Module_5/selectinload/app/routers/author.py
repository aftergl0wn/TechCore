from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from app.crud.crud import AuthorRepository
from app.schema.schema import AuthorSchemaRequest, AuthorSchemaResponse

router_author = APIRouter()


@router_author.post(
    "/author",
    response_model=AuthorSchemaResponse
)
async def create_author(
    author: AuthorSchemaRequest,
):
    return await AuthorRepository.create(author)


@router_author.get(
    "/author/{author_id}",
    response_model=AuthorSchemaResponse
)
async def author(
    author_id: int,
):
    author = await AuthorRepository.get_by_id(author_id)
    if author is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Author not found"
        )
    return author
