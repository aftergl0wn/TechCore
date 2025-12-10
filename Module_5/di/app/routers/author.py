from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud import AuthorRepository
from app.model import get_db_session
from app.schema.schema import AuthorSchemaRequest, AuthorSchemaResponse

router_author = APIRouter()


@router_author.post(
    "/author",
    response_model=AuthorSchemaResponse
)
async def create_author(
    author: AuthorSchemaRequest,
    session: AsyncSession = Depends(get_db_session),
):
    return await AuthorRepository.create(author, session)


@router_author.get(
    "/author/{author_id}",
    response_model=AuthorSchemaResponse
)
async def author(
    author_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    author = await AuthorRepository.get_by_id(author_id, session)
    if author is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Author not found"
        )
    return author
