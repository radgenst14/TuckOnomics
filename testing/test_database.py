import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from db.Database import Database


class TestDatabaseInit:
    def test_accepts_string_path(self):
        db = Database("test.db")
        assert db is not None

    def test_accepts_absolute_path(self):
        db = Database("/some/path/to/file.db")
        assert db is not None

    def test_accepts_empty_string(self):
        db = Database("")
        assert db is not None

    def test_db_attribute_is_private(self):
        db = Database("test.db")
        # Private name mangling: __db -> _Database__db
        assert hasattr(db, "_Database__db")

    def test_db_stores_provided_value(self):
        path = "my_database.db"
        db = Database(path)
        assert db._Database__db == path

    def test_multiple_instances_are_independent(self):
        db1 = Database("first.db")
        db2 = Database("second.db")
        assert db1._Database__db != db2._Database__db

    def test_returns_none_from_init(self):
        # __init__ is annotated -> None
        result = Database.__init__(Database.__new__(Database), "test.db")
        assert result is None
