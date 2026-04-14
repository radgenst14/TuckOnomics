import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import sqlite3
import pytest
from pathlib import Path
from db.Database import Database


class TestDatabaseInit:
    def test_accepts_string_db_name(self):
        db = Database("test.db")
        assert db is not None

    def test_returns_none_from_init(self):
        result = Database.__init__(Database.__new__(Database), "test.db")
        assert result is None

    def test_path_attribute_is_private(self):
        db = Database("test.db")
        assert hasattr(db, "_Database__path")

    def test_path_is_pathlib_path(self):
        db = Database("test.db")
        assert isinstance(db._Database__path, Path)

    def test_path_contains_db_name(self):
        db = Database("mydb.db")
        assert db._Database__path.name == "mydb.db"

    def test_multiple_instances_have_independent_paths(self):
        db1 = Database("first.db")
        db2 = Database("second.db")
        assert db1._Database__path != db2._Database__path

    def test_init_db_creates_portfolio_table(self):
        db = Database("test_init.db")
        conn = db.get_connection()
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='portfolio'"
        )
        assert cursor.fetchone() is not None
        conn.close()


class TestGetConnection:
    def test_returns_sqlite_connection(self):
        db = Database("test.db")
        conn = db.get_connection()
        assert isinstance(conn, sqlite3.Connection)
        conn.close()

    def test_connection_uses_row_factory(self):
        db = Database("test.db")
        conn = db.get_connection()
        assert conn.row_factory == sqlite3.Row
        conn.close()

    def test_data_directory_is_created(self):
        db = Database("test.db")
        assert db._Database__path.parent.exists()


class TestInitDb:
    def test_portfolio_table_exists(self):
        db = Database("test_portfolio.db")
        conn = db.get_connection()
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='portfolio'"
        )
        row = cursor.fetchone()
        assert row is not None
        conn.close()

    def test_portfolio_table_has_id_column(self):
        db = Database("test_portfolio.db")
        conn = db.get_connection()
        cursor = conn.execute("PRAGMA table_info(portfolio)")
        columns = [row["name"] for row in cursor.fetchall()]
        assert "id" in columns
        conn.close()

    def test_init_db_is_idempotent(self):
        db = Database("test_idempotent.db")
        # Calling init_db again should not raise
        db.init_db()
        db.init_db()
