# FILE:tests/test_lesson_25.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Verification of Lesson 25 Parabola Generator (Backend and UI Controllers).
# SCOPE:Business logic, Database, Config, and Headless UI testing.
# INPUT:Pytest fixtures (tmp_path, caplog).
# OUTPUT:Test results and LDD trace.
# KEYWORDS:[DOMAIN(8):Testing; CONCEPT(7):LDD; TECH(9):Pytest]
# LINKS:[USES_API(8):lesson_25]
# END_MODULE_CONTRACT

import os
import json
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import logging
import pytest
from lesson_25.config_manager import ConfigManager
from lesson_25.db_manager import DBManager
from lesson_25.generator import generate_parabola_points
import lesson_25.ui_controller as ui_ctrl

# Configure logging for tests
logging.basicConfig(level=logging.INFO)


# START_FUNCTION_test_config_manager
# START_CONTRACT:
# PURPOSE:Verify config load/save logic using tmp_path.
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def test_config_manager(tmp_path, caplog):
    """
    Test ensures that ConfigManager correctly saves and loads parameters from a temporary path.
    """
    caplog.set_level("INFO")
    config_file = tmp_path / "config.json"
    mgr = ConfigManager(config_path=str(config_file))

    # START_BLOCK_TEST_DEFAULTS: [Checking default values]
    config = mgr.load_config()
    assert config["a"] == 1.0
    assert config["c"] == 0.0
    # END_BLOCK_TEST_DEFAULTS

    # START_BLOCK_TEST_SAVE: [Saving and reloading]
    new_data = {"a": 2.5, "c": -10, "x_min": 0, "x_max": 5}
    mgr.save_config(new_data)
    loaded = mgr.load_config()
    assert loaded["a"] == 2.5
    assert loaded["c"] == -10
    # END_BLOCK_TEST_SAVE

    # Output LDD logs
    print("\n--- LDD LOGS (Config) ---")
    for record in caplog.records:
        if "[IMP:" in record.message:
            print(record.message)


# END_FUNCTION_test_config_manager


# START_FUNCTION_test_db_manager
# START_CONTRACT:
# PURPOSE:Verify SQLite operations (init, save, get).
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def test_db_manager(tmp_path, caplog):
    """
    Test ensures points are correctly persisted and retrieved from SQLite.
    """
    caplog.set_level("INFO")
    db_file = tmp_path / "test.db"
    mgr = DBManager(db_path=str(db_file))

    # START_BLOCK_TEST_PERSISTENCE: [Saving points]
    test_data = pd.DataFrame({"x": [1, 2, 3], "y": [1, 4, 9]})
    mgr.save_points(test_data)
    # END_BLOCK_TEST_PERSISTENCE

    # START_BLOCK_TEST_RETRIEVAL: [Reading points]
    df = mgr.get_points()
    assert len(df) == 3
    assert df.iloc[1]["y"] == 4
    # END_BLOCK_TEST_RETRIEVAL

    print("\n--- LDD LOGS (DB) ---")
    for record in caplog.records:
        if "[IMP:" in record.message:
            print(record.message)


# END_FUNCTION_test_db_manager


# START_FUNCTION_test_generator
# START_CONTRACT:
# PURPOSE:Verify parabola calculation logic.
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def test_generator(caplog):
    """
    Test verifies the math logic of y = ax^2 + c.
    """
    caplog.set_level("INFO")
    # a=2, c=1, x=2 => 2*(2^2)+1 = 2*4+1 = 9
    df = generate_parabola_points(a=2.0, c=1.0, x_min=0, x_max=2, num_points=3)

    assert len(df) == 3
    # Midpoint should be x=1, y=2*(1^2)+1 = 3
    assert df.iloc[1]["x"] == 1.0
    assert df.iloc[1]["y"] == 3.0

    print("\n--- LDD LOGS (Generator) ---")
    for record in caplog.records:
        if "[IMP:9]" in record.message:
            print(record.message)


# END_FUNCTION_test_generator


# START_FUNCTION_test_ui_headless
# START_CONTRACT:
# PURPOSE:Headless testing of Gradio handlers.
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def test_ui_headless(tmp_path, caplog):
    """
    Emulates UI interaction without starting the server.
    Injects temporary paths into controllers for isolation.
    """
    caplog.set_level("INFO")

    # Inject temporary paths for testing isolation
    test_config = tmp_path / "ui_config.json"
    test_db = tmp_path / "ui_test.db"

    ui_ctrl._config_mgr = ConfigManager(config_path=str(test_config))
    ui_ctrl._db_mgr = DBManager(db_path=str(test_db))

    # START_BLOCK_TEST_HANDLE_GENERATE: [Button 1 emulation]
    df = ui_ctrl.handle_generate(a=1, c=5, x_min=-2, x_max=2)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert os.path.exists(test_config)
    # END_BLOCK_TEST_HANDLE_GENERATE

    # START_BLOCK_TEST_HANDLE_DRAW: [Button 2 emulation]
    fig = ui_ctrl.handle_draw()
    assert isinstance(fig, go.Figure)
    # END_BLOCK_TEST_HANDLE_DRAW

    print("\n--- LDD LOGS (UI Headless) ---")
    for record in caplog.records:
        if "[IMP:9]" in record.message:
            print(record.message)


# END_FUNCTION_test_ui_headless
