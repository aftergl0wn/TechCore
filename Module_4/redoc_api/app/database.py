class Session:
    def __init__(self):
        self.data = {}
        self.id = 0


session = Session()


def get_db_session():
    yield session
