from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud import author_create, author_get_by_id
from app.model import get_db_session
from app.schema.schema import AuthorSchemaRequest, AuthorSchemaResponse

router_author = APIRouter()


@router_author.post(
    "/author",
    response_model=AuthorSchemaResponse
)
async def create_author(
    author: AuthorSchemaRequest,
    db: AsyncSession = Depends(get_db_session),
):
    return await author_create(author, db)


@router_author.get(
    "/author/{author_id}",
    response_model=AuthorSchemaResponse
)
async def author(
    author_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    author = await author_get_by_id(author_id, db)
    if author is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Author not found"
        )
    return author
