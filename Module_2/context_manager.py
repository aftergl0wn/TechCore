import sqlite3


class DatabaseConnection:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.conn = sqlite3.connect(self.name)
        return self.conn

    def __exit__(self, exp_type, exp_value, exc_traceback):
        try:
            self.conn.close()
        finally:
            if exp_type is not None:
                print(f"Возникла ошибка {exp_type}: {exp_value}")


if __name__ == "__main__":
    with DatabaseConnection("db.sqlite") as conn:
        cur = conn.cursor()
        query_1 = '''
        CREATE TABLE IF NOT EXISTS directors(
            id INTEGER PRIMARY KEY,
            full_name TEXT,
            birth_year INTEGER
        );
        '''
        cur.execute(query_1)
