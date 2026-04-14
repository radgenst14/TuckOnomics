import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from unittest.mock import patch
from core.Orchestrator import Orchestrator


class TestOrchestratorClassAttributes:
    def test_menu_string_contains_title(self):
        assert "TuckOnomics Menu" in Orchestrator.menu

    def test_menu_string_contains_add_position_option(self):
        assert "1)" in Orchestrator.menu
        assert "Add new position" in Orchestrator.menu

    def test_menu_string_contains_quit_option(self):
        assert "q)" in Orchestrator.menu
        assert "Quit" in Orchestrator.menu

    def test_valid_menu_inputs_contains_1(self):
        assert "1" in Orchestrator.valid_menu_inputs

    def test_valid_menu_inputs_contains_q(self):
        assert "q" in Orchestrator.valid_menu_inputs

    def test_valid_menu_inputs_does_not_contain_invalid(self):
        for bad in ["2", "Q", "", " ", "x"]:
            assert bad not in Orchestrator.valid_menu_inputs


class TestOrchestratorInit:
    def test_instantiation(self):
        orc = Orchestrator()
        assert orc is not None


class TestMenuInput:
    def test_returns_valid_input_1(self):
        orc = Orchestrator()
        with patch("builtins.input", return_value="1"):
            result = orc.menu_input()
        assert result == "1"

    def test_returns_valid_input_q(self):
        orc = Orchestrator()
        with patch("builtins.input", return_value="q"):
            result = orc.menu_input()
        assert result == "q"

    def test_loops_until_valid_input(self):
        orc = Orchestrator()
        # First two inputs invalid, third is valid
        side_effects = ["bad", "2", "q"]
        with patch("builtins.input", side_effect=side_effects):
            result = orc.menu_input()
        assert result == "q"

    def test_rejects_uppercase_q(self):
        orc = Orchestrator()
        side_effects = ["Q", "q"]
        with patch("builtins.input", side_effect=side_effects):
            result = orc.menu_input()
        assert result == "q"

    def test_rejects_whitespace(self):
        orc = Orchestrator()
        side_effects = [" ", "1"]
        with patch("builtins.input", side_effect=side_effects):
            result = orc.menu_input()
        assert result == "1"


class TestRun:
    def test_quit_immediately(self):
        orc = Orchestrator()
        # db prompt -> "testdb", then menu -> "q"
        with patch("builtins.input", side_effect=["testdb", "q"]), \
             patch("builtins.print"):
            orc.run()  # should return without error

    def test_select_1_then_quit(self):
        orc = Orchestrator()
        with patch("builtins.input", side_effect=["testdb", "1", "q"]), \
             patch("builtins.print"):
            orc.run()  # option 1 is a no-op; should exit cleanly on q

    def test_multiple_invalid_then_quit(self):
        orc = Orchestrator()
        # invalid menu entries are consumed by menu_input's loop
        with patch("builtins.input", side_effect=["testdb", "x", "y", "q"]), \
             patch("builtins.print"):
            orc.run()
