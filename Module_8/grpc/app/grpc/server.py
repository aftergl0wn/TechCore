import asyncio

import grpc

from app.grpc.generated import author_pb2, author_pb2_grpc

class AuthorServicer(author_pb2_grpc.AuthorServiceServicer):

    async def GetAuthor(self, request, context):

        return author_pb2.AuthorResponse(
            id=request.id,
            name="Tom"
        )

async def serve():
    server = grpc.aio.server()
    author_pb2_grpc.add_AuthorServiceServicer_to_server(
        AuthorServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()
