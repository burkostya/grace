# FILE:lesson_24/tests/test_lesson_24.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Unit and headless UI tests for Lesson 24 parabola application.
# SCOPE: Backend logic, LDD telemetry, and Headless UI verification.
# INPUT: Pytest fixtures (tmp_path, caplog).
# OUTPUT: Test results and filtered LDD logs [IMP:7-10].
# KEYWORDS:DOMAIN(Parabola): Testing; CONCEPT(Pytest): LDD_Telemetry
# LINKS:USES_API(Pytest); USES_API(Pandas); USES_API(Plotly)
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: 1.0.0 - Initial implementation of backend and headless tests.
# END_CHANGE_SUMMARY

import pytest
import os
import pandas as pd
import plotly.graph_objects as go
import logging
from lesson_24 import config_manager, db_manager, logic, ui_controller

# Configure logging for tests
# START_BLOCK_LOGGING_SETUP: [Setup local logger for test suite]
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lesson_24.tests")
# END_BLOCK_LOGGING_SETUP


# START_FUNCTION_test_backend_ldd
# START_CONTRACT:
# PURPOSE:Verify calculation logic, DB persistence and LDD log trajectory.
# INPUTS:
# - tmp_path: pytest fixture for isolated file storage
# - caplog: pytest fixture for capturing logs
# OUTPUTS: None
# SIDE_EFFECTS: Creates temporary files for config and db.
# KEYWORDS:PATTERN(Test): Backend_LDD
# COMPLEXITY_SCORE: 7
# END_CONTRACT
def test_backend_ldd(tmp_path, caplog):
    """
    Test scenario:
    1. Define test parameters.
    2. Calculate parabola points.
    3. Save to temporary database.
    4. Retrieve from database and verify content.
    5. Output LDD logs [IMP:7-10] for trajectory verification.
    """
    caplog.set_level(logging.INFO)

    # Define temp paths
    db_file = tmp_path / "test_parabola.db"
    db_path = str(db_file)

    # START_BLOCK_CALC:[Perform calculation and storage]
    a, c = 2.0, 5.0
    x_min, x_max = -5, 5

    # Business Logic call
    points = logic.calculate_parabola(a, c, x_min, x_max, num_points=20)

    # Persistence call
    db_manager.save_points(points, db_path=db_path)

    # Retrieval call
    df = db_manager.get_points(db_path=db_path)
    # END_BLOCK_CALC

    # START_BLOCK_LDD_TELEMETRY: [Output filtered logs for AI agent analysis]
    found_imp_9 = False
    print("\n--- LDD TRAJECTORY (IMP:7-10) ---")
    for record in caplog.records:
        if "[IMP:" in record.message:
            try:
                imp_str = record.message.split("[IMP:")[1].split("]")[0]
                imp_level = int(imp_str)
                if imp_level >= 7:
                    print(record.message)
                if imp_level >= 9:
                    found_imp_9 = True
            except (ValueError, IndexError):
                continue
    print("--- END LDD TRAJECTORY ---")
    # END_BLOCK_LDD_TELEMETRY

    # START_BLOCK_VERIFICATION:[Check business invariants]
    assert len(df) == 20, f"Expected 20 points, got {len(df)}"
    assert "x" in df.columns and "y" in df.columns, "DataFrame missing required columns"

    # Verify math for one point (x=0 should be c)
    y_at_0 = (
        df[df["x"].abs() < 0.1]["y"].values[0]
        if not df[df["x"].abs() < 0.1].empty
        else None
    )
    if y_at_0 is not None:
        assert abs(y_at_0 - c) < 0.5, f"Expected y close to {c} at x=0, got {y_at_0}"

    # Anti-Illusion: Verify LDD compliance
    assert found_imp_9, "CRITICAL: LDD log level [IMP:9] missing in execution trace"
    # END_BLOCK_VERIFICATION


# END_FUNCTION_test_backend_ldd


# START_FUNCTION_test_ui_headless
# START_CONTRACT:
# PURPOSE:Verify Gradio controller handlers return correct types (Headless UI Test).
# INPUTS:
# - tmp_path: pytest fixture for isolated storage
# OUTPUTS: None
# SIDE_EFFECTS: Updates local files in lesson_24/ temporarily.
# KEYWORDS:PATTERN(Test): Headless_UI
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def test_ui_headless(tmp_path):
    """
    Simulates UI interaction by calling handler functions directly.
    Checks return types and state changes without launching the Gradio server.
    """
    # START_BLOCK_UI_MOCK_STATE:[Isolate UI side-effects]
    # We use actual file paths but in a controlled manner if possible,
    # or rely on the fact that these are isolated for the test.
    # Note: ui_controller imports modules that use default paths.
    # In a real SWE project, we would inject paths via config.
    # END_BLOCK_UI_MOCK_STATE

    # START_BLOCK_HANDLER_1:[Test handle_generate_data]
    df_result = ui_controller.handle_generate_data(a=1, c=0, x_min=-10, x_max=10)
    assert isinstance(df_result, pd.DataFrame), "Handler must return a DataFrame"
    assert not df_result.empty, "DataFrame should not be empty after data generation"
    # END_BLOCK_HANDLER_1

    # START_BLOCK_HANDLER_2:[Test handle_draw_graph]
    fig_result = ui_controller.handle_draw_graph()
    assert isinstance(fig_result, go.Figure), "Handler must return a Plotly Figure"
    # END_BLOCK_HANDLER_2


# END_FUNCTION_test_ui_headless
