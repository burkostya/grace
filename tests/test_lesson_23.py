# FILE:tests/test_lesson_23.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Comprehensive tests for lesson_23 backend and UI logic.
# SCOPE:Backend calculation, DB persistence, Config persistence, and Headless UI handlers.
# INPUT:Pytest fixtures (tmp_path, caplog).
# OUTPUT:Test success status and LDD telemetry.
# KEYWORDS:DOMAIN(Testing): QA; CONCEPT(LDD): Log selection; CONCEPT(AntiLoop): Protocol.
# LINKS:USES_API(pytest); USES_API(pandas); USES_API(plotly.graph_objects)
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: 1.0.0 - Initial implementation of lesson_23 test suite.
# END_CHANGE_SUMMARY

import pytest
import os
import pandas as pd
import plotly.graph_objects as go
import logging

# Native imports from lesson_23
from lesson_23.config_manager import ConfigManager
from lesson_23.db_manager import DBManager
from lesson_23.parabola_engine import calculate_parabola
from lesson_23.app_logic import handle_generate_data, handle_draw_graph, setup_logger


# START_FUNCTION_test_backend_logic
# START_CONTRACT:
# PURPOSE: Verifies parabola calculation, config saving, and DB persistence.
# INPUTS: - tmp_path: pytest fixture => temporary directory
# - caplog: pytest fixture => log capture
# OUTPUTS: None
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def test_backend_logic(tmp_path, caplog):
    """
    Ensures that the backend components work together: config is saved,
    math is correct, and data is stored in the SQLite database.
    """
    caplog.set_level(logging.INFO)

    # START_BLOCK_SETUP:[Setup temporary files and managers]
    config_file = tmp_path / "config.json"
    db_file = tmp_path / "app_23.db"
    log_file = tmp_path / "app_23.log"

    setup_logger(str(log_file))
    config_mgr = ConfigManager(str(config_file))
    db_mgr = DBManager(str(db_file))
    db_mgr.init_db()
    # END_BLOCK_SETUP

    # START_BLOCK_EXECUTION:[Run calculation and storage flow]
    a, c, x_min, x_max = 2.0, 5.0, -5, 5
    df = handle_generate_data(a, c, x_min, x_max, config_mgr, db_mgr)
    # END_BLOCK_EXECUTION

    # START_BLOCK_LDD_TELEMETRY:[Selection of critical logs]
    print("\n--- LDD TRAJECTORY (IMP:7-10) ---")
    found_belief = False
    for record in caplog.records:
        if "[IMP:" in record.message:
            try:
                imp_level = int(record.message.split("[IMP:")[1].split("]")[0])
                if imp_level >= 7:
                    print(record.message)
                if imp_level >= 9:
                    found_belief = True
            except (IndexError, ValueError):
                continue
    # END_BLOCK_LDD_TELEMETRY

    # START_BLOCK_VERIFICATION:[Check data integrity]
    assert not df.empty, "Error: DataFrame is empty after generation"
    assert len(df) == 100, f"Error: Expected 100 points, got {len(df)}"

    # Check math: y = 2x^2 + 5. For x=0, y should be 5.
    zero_row = df[df["x"] == 0]
    if not zero_row.empty:
        assert zero_row.iloc[0]["y"] == 5.0, (
            f"Error: Math failure! For x=0, y should be 5, got {zero_row.iloc[0]['y']}"
        )

    assert os.path.exists(config_file), "Error: config.json was not created"
    assert found_belief, (
        "Critical LDD Error: Business logic failed to output control log [IMP:9]"
    )
    # END_BLOCK_VERIFICATION


# END_FUNCTION_test_backend_logic


# START_FUNCTION_test_ui_headless
# START_CONTRACT:
# PURPOSE: Verifies Gradio handler return types without starting server.
# INPUTS: - tmp_path: pytest fixture
# - caplog: pytest fixture
# OUTPUTS: None
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def test_ui_headless(tmp_path, caplog):
    """
    Tests UI handlers directly to ensure they return the correct types
    expected by Gradio components (DataFrame and Plotly Figure).
    """
    caplog.set_level(logging.INFO)

    # START_BLOCK_SETUP:[Setup temporary files and managers]
    config_file = tmp_path / "config.json"
    db_file = tmp_path / "app_23.db"
    log_file = tmp_path / "app_23.log"

    setup_logger(str(log_file))
    config_mgr = ConfigManager(str(config_file))
    db_mgr = DBManager(str(db_file))
    db_mgr.init_db()
    # END_BLOCK_SETUP

    # START_BLOCK_GENERATE_HANDLER:[Call 'Generate Data' handler]
    # handle_generate_data returns pd.DataFrame
    df = handle_generate_data(1.0, 0.0, -10, 10, config_mgr, db_mgr)
    assert isinstance(df, pd.DataFrame), (
        "Error: handle_generate_data must return pd.DataFrame"
    )
    # END_BLOCK_GENERATE_HANDLER

    # START_BLOCK_GRAPH_HANDLER:[Call 'Draw Graph' handler]
    # handle_draw_graph returns plotly.graph_objects.Figure
    fig = handle_draw_graph(db_mgr)
    assert isinstance(fig, go.Figure), (
        "Error: handle_draw_graph must return plotly.graph_objects.Figure"
    )
    assert len(fig.data) > 0, "Error: Plotly Figure should contain data"
    # END_BLOCK_GRAPH_HANDLER

    print("\n--- UI HEADLESS TELEMETRY ---")
    for record in caplog.records:
        if "[IMP:9]" in record.message:
            print(f"[UI_MARKER]: {record.message}")


# END_FUNCTION_test_ui_headless
