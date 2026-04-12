# FILE:lesson_25/ui_controller.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Orchestrates Gradio event handlers and business logic calls.
# SCOPE:UI controllers (Headless Testable), State management coordination.
# INPUT:UI component values.
# OUTPUT:DataFrames and Plotly Figures.
# KEYWORDS:[DOMAIN(8):UI; CONCEPT(7):Controller; TECH(9):Gradio]
# LINKS:[USES_API(8):gradio; USES_API(8):plotly]
# END_MODULE_CONTRACT

# START_RATIONALE:
# Q: Why isolate controllers from the main UI script?
# A: Enables Headless testing of logic without launching the Gradio server.
# END_RATIONALE

# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Initial implementation of UI controllers.]
# END_CHANGE_SUMMARY

# START_MODULE_MAP:
# FUNC 10[Handles data generation button click] => handle_generate
# FUNC 10[Handles graph drawing button click] => handle_draw
# END_MODULE_MAP

import pandas as pd
import plotly.express as px
import logging
from .config_manager import ConfigManager
from .db_manager import DBManager
from .generator import generate_parabola_points

logger = logging.getLogger(__name__)

# Initialize managers with default paths (can be overridden in tests)
_config_mgr = ConfigManager()
_db_mgr = DBManager()


# START_FUNCTION_handle_generate
# START_CONTRACT:
# PURPOSE:Persists config, generates points, saves to DB, and returns table.
# INPUTS:
# - float => a: x^2 coefficient.
# - float => c: constant coefficient.
# - float => x_min: range start.
# - float => x_max: range end.
# OUTPUTS:
# - DataFrame - generated points for UI table.
# SIDE_EFFECTS: Updates config.json, updates parabola_25.db.
# KEYWORDS:[PATTERN(8):Controller; CONCEPT(7):Persistence]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def handle_generate(a, c, x_min, x_max):
    """
    Handler for the 'Generate Data' button.
    Coordinates saving state, generating data, and persistence.
    """
    # START_BLOCK_UPDATE_STATE: [Saving config]
    new_config = {"a": a, "c": c, "x_min": x_min, "x_max": x_max}
    _config_mgr.save_config(new_config)
    # END_BLOCK_UPDATE_STATE

    # START_BLOCK_GENERATION: [Calculating and saving points]
    df = generate_parabola_points(a, c, x_min, x_max)
    _db_mgr.save_points(df)
    # END_BLOCK_GENERATION

    logger.info(
        f"[AgenticUX][IMP:9][handle_generate][Flow] Data generated and persisted. Returning {len(df)} rows to UI. [VALUE]"
    )
    return df


# END_FUNCTION_handle_generate


# START_FUNCTION_handle_draw
# START_CONTRACT:
# PURPOSE:Fetches points from DB and returns a Plotly Figure.
# INPUTS: None
# OUTPUTS:
# - Plotly Figure - interactive chart.
# SIDE_EFFECTS: None
# KEYWORDS:[PATTERN(8):Controller; CONCEPT(7):Visualization]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def handle_draw():
    """
    Handler for the 'Draw Graph' button.
    Reads existing points from DB and creates a visualization.
    """
    # START_BLOCK_READ_DATA: [Fetching from DB]
    df = _db_mgr.get_points()
    # END_BLOCK_READ_DATA

    # START_BLOCK_VISUALIZATION: [Creating Plotly figure]
    if df.empty:
        logger.warning(
            f"[LogicCheck][IMP:8][handle_draw][Condition] Database is empty. Returning empty plot."
        )
        fig = px.scatter(title="No data to display. Please generate data first.")
    else:
        fig = px.line(df, x="x", y="y", title=f"Parabola Graph")
        fig.add_scatter(x=df["x"], y=df["y"], mode="markers", name="Points")
    # END_BLOCK_VISUALIZATION

    logger.info(
        f"[AgenticUX][IMP:9][handle_draw][Flow] Graph generated from {len(df)} points. [VALUE]"
    )
    return fig


# END_FUNCTION_handle_draw
