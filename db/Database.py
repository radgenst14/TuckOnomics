import sqlite3
from pathlib import Path
from datetime import date
from db.Models import Position

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
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     tckr TEXT NOT NULL,
                     shares REAL NOT NULL,
                     cost_basis REAL NOT NULL,
                     purchase_date TEXT NOT NULL
                     )
            """)
        conn.commit()
        conn.close()

    def remove_db(self):
        self.__path.unlink(missing_ok=True)

    def get_all_positions(self):
        # connect to database and select all positions from the portfolio
        conn = self.get_connection()
        rows = conn.execute(
            """
            SELECT * FROM portfolio
            """
        )
        
        # for each row create a position object and append to the returned positions lst
        positions = []
        for r in rows:
            p = Position(
                id=r["id"],
                tckr=r["tckr"],
                shares=r["shares"],
                cost_basis=r["cost_basis"],
                purchase_date=r["purchase_date"]
            )
            positions.append(p)
            
        conn.close()

        return positions
    
    def add_position(self, tckr: str, shares: float, cost_basis: float, purchase_date: date):
        conn = self.get_connection()
        cursor = conn.execute(
            "INSERT INTO portfolio (tckr, shares, cost_basis, purchase_date) VALUES (?, ?, ?, ?)",
            (tckr.upper(), shares, cost_basis, purchase_date.isoformat())
        )
        conn.commit()
        row_id = cursor.lastrowid
        conn.close()
        return row_id

    def remove_position(self, tckr: str, purchase_date: date):
        conn = self.get_connection()
        conn.execute(
            "DELETE FROM portfolio WHERE tckr = ? AND purchase_date = ?",
            (tckr.upper(), purchase_date.isoformat())
        )
        conn.commit()
        conn.close()