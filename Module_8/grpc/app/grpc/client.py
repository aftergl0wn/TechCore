import grpc

from app.grpc.generated import author_pb2, author_pb2_grpc


async def get_author(author_id: int):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = author_pb2_grpc.AuthorServiceStub(channel)
        request = author_pb2.AuthorRequest(id=author_id)
        response = await stub.GetAuthor(request)
        return response
