# FILE:lesson_24/ui_controller.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Handle interaction between Gradio UI and backend logic.
# SCOPE: UI logic (generate_data, draw_graph).
# INPUT: UI component values (a, c, x_min, x_max).
# OUTPUT: Gradio component updates (Dataframe, Plot).
# KEYWORDS:DOMAIN(Parabola): UI; CONCEPT(Gradio): Controller
# LINKS:USES_API(Gradio); USES_API(Plotly); READS_DATA_FROM(lesson_24/db_manager.py)
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: 1.0.0 - Initial implementation of UI controller.
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC [9][Handles data generation and DB saving] => handle_generate_data
# FUNC [9][Handles graph drawing from DB] => handle_draw_graph
# END_MODULE_MAP

import pandas as pd
import plotly.graph_objects as go
import logging
from lesson_24 import config_manager, db_manager, logic

# START_BLOCK_LOGGING_SETUP: [Setup local logger]
logger = logging.getLogger("lesson_24.ui_controller")
# END_BLOCK_LOGGING_SETUP


# START_FUNCTION_handle_generate_data
# START_CONTRACT:
# PURPOSE:Save config, calculate parabola points, save to DB, and return data for UI table.
# INPUTS:
# - a: float => Coefficient a
# - c: float => Coefficient c
# - x_min: float => Range start
# - x_max: float => Range end
# OUTPUTS:
# - pd.DataFrame - Calculated points for UI display
# SIDE_EFFECTS: Updates config.json, updates parabola.db.
# KEYWORDS:PATTERN(UI): DataGen
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def handle_generate_data(a, c, x_min, x_max):
    """
    Orchestrates the data generation flow:
    1. Saves the parameters to config.json.
    2. Calculates parabola points using logic.py.
    3. Saves points to SQLite database.
    4. Returns a DataFrame for the UI component.
    """
    # START_BLOCK_GEN:[Perform data generation orchestration]
    try:
        logger.info(
            f"[IMP:9][handle_generate_data][GEN][UI] Request with a={a}, c={c}, x=[{x_min}, {x_max}].[BELIEF:DATA_GEN_START]"
        )

        # Save config
        config = {"a": a, "c": c, "x_min": x_min, "x_max": x_max}
        config_manager.save_config(config)

        # Calculate
        points = logic.calculate_parabola(a, c, x_min, x_max)

        # Save to DB
        db_manager.save_points(points)

        # Get from DB for UI
        df = db_manager.get_points()

        logger.info(
            f"[IMP:8][handle_generate_data][GEN][UI] Data generation and storage successful.[SUCCESS]"
        )
        return df
    except Exception as e:
        logger.error(
            f"[IMP:10][handle_generate_data][GEN][ERROR] UI handler failed: {str(e)}[CRITICAL]"
        )
        return pd.DataFrame(columns=["x", "y"])
    # END_BLOCK_GEN


# END_FUNCTION_handle_generate_data


# START_FUNCTION_handle_draw_graph
# START_CONTRACT:
# PURPOSE:Retrieve points from DB and return a Plotly Figure for UI display.
# INPUTS: None
# OUTPUTS:
# - plotly.graph_objects.Figure - Parabola plot
# SIDE_EFFECTS: Reads from parabola.db.
# KEYWORDS:PATTERN(UI): Visualization
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def handle_draw_graph():
    """
    Orchestrates the graph visualization flow:
    1. Retrieves points from SQLite database.
    2. Constructs a Plotly figure with a parabola trace.
    3. Returns the figure object to the UI component.
    """
    # START_BLOCK_PLOT:[Perform graph rendering orchestration]
    try:
        logger.info(
            f"[IMP:9][handle_draw_graph][PLOT][UI] Requesting points from DB for plotting.[BELIEF:DRAW_GRAPH_START]"
        )

        # Get from DB
        df = db_manager.get_points()

        if df.empty:
            logger.warning(
                f"[IMP:7][handle_draw_graph][PLOT][UI] No data found in database to plot.[WARNING]"
            )

        # Create Plotly figure
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df["x"],
                y=df["y"],
                mode="lines",
                name="Parabola",
                line=dict(color="blue", width=2),
            )
        )

        # Styling
        fig.update_layout(
            title="Parabola Visualization",
            xaxis_title="x",
            yaxis_title="y",
            template="plotly_white",
        )

        logger.info(
            f"[IMP:8][handle_draw_graph][PLOT][UI] Plotly figure generated.[SUCCESS]"
        )
        return fig
    except Exception as e:
        logger.error(
            f"[IMP:10][handle_draw_graph][PLOT][ERROR] Graph handler failed: {str(e)}[CRITICAL]"
        )
        # Return empty figure
        return go.Figure()
    # END_BLOCK_PLOT


# END_FUNCTION_handle_draw_graph
