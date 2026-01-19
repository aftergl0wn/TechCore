import asyncio


class Session:
    def __init__(self):
        self.data = {}
        self.id = 0
        self.lock = asyncio.Lock()


session = Session()


def get_db_session():
    yield session
