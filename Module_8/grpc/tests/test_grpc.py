import pytest

from app.grpc.generated import author_pb2
from app.grpc.server import AuthorServicer


@pytest.mark.asyncio
async def test_grpc_async_call():
    servicer = AuthorServicer()
    request = author_pb2.AuthorRequest(id=1)
    response = await servicer.GetAuthor(request, None)
    assert response.id == 1
    assert response.name == "Tom"
    