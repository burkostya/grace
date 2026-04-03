# FILE:lesson_23/app_logic.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Orchestrator for the parabola generation application.
# SCOPE:Connecting UI events to backend calculation and persistence.
# INPUT:UI parameters (a, c, x_min, x_max).
# OUTPUT:DataFrames for tables and Plotly Figures for graphs.
# KEYWORDS:DOMAIN(AppLogic): Coordination; CONCEPT(Flow): UI-to-Backend.
# LINKS:USES_API(plotly.graph_objects); USES_API(pandas)
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: 1.0.0 - Initial implementation of application orchestration logic.
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC[7][Sets up logging] => setup_logger
# FUNC[8][Handles 'Generate Data' button] => handle_generate_data
# FUNC[8][Handles 'Draw Graph' button] => handle_draw_graph
# END_MODULE_MAP

import logging
import os
import pandas as pd
import plotly.graph_objects as go
from .config_manager import ConfigManager
from .db_manager import DBManager
from .parabola_engine import calculate_parabola


# START_FUNCTION_setup_logger
def setup_logger(log_file: str):
    """
    Configures the application logger to write to a specific file with
    a standardized format for LDD 2.0.
    """
    logger = logging.getLogger("app_23")
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers
    if not logger.handlers:
        fh = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger


# END_FUNCTION_setup_logger


# START_FUNCTION_handle_generate_data
# START_CONTRACT:
# PURPOSE: Updates config, calculates points, saves to DB, returns DF.
# INPUTS:
# - a: float => quadratic coefficient
# - c: float => constant term
# - x_min: float => range start
# - x_max: float => range end
# - config_mgr: ConfigManager => manager instance
# - db_mgr: DBManager => manager instance
# OUTPUTS:
# - pd.DataFrame - result table
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def handle_generate_data(
    a: float,
    c: float,
    x_min: float,
    x_max: float,
    config_mgr: ConfigManager,
    db_mgr: DBManager,
) -> pd.DataFrame:
    """
    Orchestrates the entire data generation flow: saves parameters,
    calculates the parabola, stores points in SQLite, and returns them.
    """
    logger = logging.getLogger("app_23")
    logger.info(
        f"[INFO][IMP:9][app_logic][handle_generate_data][START] Generating data for a={a}, c={c}, x_min={x_min}, x_max={x_max}.[SUCCESS]"
    )

    # START_BLOCK_SAVE_CONFIG:[Persist current parameters]
    data = {"a": a, "c": c, "x_min": x_min, "x_max": x_max}
    config_mgr.save_config(data)
    # END_BLOCK_SAVE_CONFIG

    # START_BLOCK_CALCULATE:[Generate math points]
    points = calculate_parabola(a, c, x_min, x_max)
    # END_BLOCK_CALCULATE

    # START_BLOCK_SAVE_DB:[Persist points to SQL]
    db_mgr.save_points(points)
    # END_BLOCK_SAVE_DB

    # START_BLOCK_RETURN_DF:[Return table for Gradio]
    df = db_mgr.get_points()
    logger.info(
        f"[INFO][IMP:7][app_logic][handle_generate_data][END] Returning DataFrame with {len(df)} rows.[SUCCESS]"
    )
    return df
    # END_BLOCK_RETURN_DF


# END_FUNCTION_handle_generate_data


# START_FUNCTION_handle_draw_graph
# START_CONTRACT:
# PURPOSE: Fetches data from DB and builds Plotly figure.
# INPUTS:
# - db_mgr: DBManager => manager instance
# OUTPUTS:
# - go.Figure - Plotly interactive chart.
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def handle_draw_graph(db_mgr: DBManager) -> go.Figure:
    """
    Retrieves data from the persistent storage and constructs an
    interactive Plotly figure for visualization.
    """
    logger = logging.getLogger("app_23")
    logger.info(
        f"[INFO][IMP:7][app_logic][handle_draw_graph][START] Drawing graph from DB data.[SUCCESS]"
    )

    # START_BLOCK_FETCH:[Get data from SQLite]
    df = db_mgr.get_points()
    # END_BLOCK_FETCH

    # START_BLOCK_PLOT:[Build Plotly trace]
    fig = go.Figure()
    if not df.empty:
        fig.add_trace(
            go.Scatter(x=df["x"], y=df["y"], mode="lines+markers", name="Parabola")
        )
        fig.update_layout(
            title="Parabola Visualization", xaxis_title="x", yaxis_title="y"
        )
        logger.info(
            f"[INFO][IMP:8][app_logic][handle_draw_graph][LOGIC] Plot built with {len(df)} points.[SUCCESS]"
        )
    else:
        fig.update_layout(title="No Data Available")
        logger.warning(
            f"[WARN][IMP:9][app_logic][handle_draw_graph][VALIDATION] Attempted to draw graph with empty DB.[SUCCESS]"
        )
    # END_BLOCK_PLOT

    # AI Belief State: Plotly figure correctly represents the data stored in DB.
    logger.info(
        f"[BELIEF][IMP:9][app_logic][handle_draw_graph][VALIDATION] Plotly Figure is generated correctly from SQLite state.[SUCCESS]"
    )
    return fig


# END_FUNCTION_handle_draw_graph
