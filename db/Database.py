import sqlite3
from pathlib import Path

class Database:

    def __init__(self, db_name) -> None:
        self.__path = Path(__file__).parent / "data" / db_name
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        self.__path.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(self.__path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        conn = self.get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS portfolio
                     (
                     id INTEGER PRIMARY KEY AUTOINCREMENT
                     )
            """)
        conn.commit()
        conn.close()

    