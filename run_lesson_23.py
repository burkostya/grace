# FILE:run_lesson_23.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Entry point for the Lesson 23 Gradio application.
# SCOPE:UI Layout and server lifecycle management.
# INPUT:User interaction via web browser.
# OUTPUT:Web server hosting the Gradio UI.
# KEYWORDS:DOMAIN(UI): Web interface; CONCEPT(Launcher): Gradio server.
# LINKS:USES_API(gradio); USES_API(plotly.graph_objects)
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: 1.0.0 - Initial implementation of the Gradio launcher for Lesson 23.
# END_CHANGE_SUMMARY

import sys
import os
import logging


# START_FUNCTION_main
def main():
    """
    Initializes backend managers, sets up the Gradio interface with two columns,
    and launches the server.
    """
    # START_BLOCK_LAZY_IMPORTS:[Import heavy libraries inside main]
    import gradio as gr
    import plotly.graph_objects as go
    from lesson_23.config_manager import ConfigManager
    from lesson_23.db_manager import DBManager
    from lesson_23.app_logic import (
        handle_generate_data,
        handle_draw_graph,
        setup_logger,
    )
    # END_BLOCK_LAZY_IMPORTS

    # START_BLOCK_PATHS:[Define local paths for the lesson]
    lesson_dir = "lesson_23"
    config_path = os.path.join(lesson_dir, "config.json")
    db_path = os.path.join(lesson_dir, "app_23.db")
    log_path = os.path.join(lesson_dir, "app_23.log")
    # END_BLOCK_PATHS

    # START_BLOCK_SETUP:[Initialize managers and logger]
    logger = setup_logger(log_path)
    # Add console handler for stdout visibility
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(ch)

    logger.info(
        f"[INFO][IMP:9][launcher][main][START] Starting Lesson 23 Parabola App.[SUCCESS]"
    )

    config_mgr = ConfigManager(config_path)
    db_mgr = DBManager(db_path)
    db_mgr.init_db()

    initial_config = config_mgr.load_config()
    # END_BLOCK_SETUP

    # START_BLOCK_UI_DEFINITION:[Build Gradio interface]
    with gr.Blocks(title="Lesson 23: Parabola Generator") as demo:
        gr.Markdown("# Lesson 23: Parabola $y = ax^2 + c$")

        with gr.Row():
            # LEFT COLUMN
            with gr.Column(scale=1):
                gr.Markdown("### Controls & Data")
                a_input = gr.Slider(
                    minimum=-10,
                    maximum=10,
                    value=initial_config.get("a", 1.0),
                    label="Coefficient a",
                )
                c_input = gr.Slider(
                    minimum=-20,
                    maximum=20,
                    value=initial_config.get("c", 0.0),
                    label="Constant c",
                )
                x_min_input = gr.Number(
                    value=initial_config.get("x_min", -10), label="x_min"
                )
                x_max_input = gr.Number(
                    value=initial_config.get("x_max", 10), label="x_max"
                )

                with gr.Row():
                    btn_generate = gr.Button("Generate Data", variant="primary")
                    btn_draw = gr.Button("Draw Graph")

                table_output = gr.Dataframe(label="Parabola Points", interactive=False)

            # RIGHT COLUMN
            with gr.Column(scale=2):
                gr.Markdown("### Visualization")
                plot_output = gr.Plot(label="Interactive Parabola")

        # START_BLOCK_UI_LOGIC:[Connect buttons to handlers]
        btn_generate.click(
            fn=lambda a, c, x_min, x_max: handle_generate_data(
                a, c, x_min, x_max, config_mgr, db_mgr
            ),
            inputs=[a_input, c_input, x_min_input, x_max_input],
            outputs=[table_output],
        )

        btn_draw.click(
            fn=lambda: handle_draw_graph(db_mgr), inputs=[], outputs=[plot_output]
        )
        # END_BLOCK_UI_LOGIC

    # START_BLOCK_LAUNCH:[Start the server]
    try:
        logger.info(
            f"[INFO][IMP:10][launcher][main][SERVER] Launching Gradio server...[SUCCESS]"
        )
        demo.launch(inbrowser=True)
    except KeyboardInterrupt:
        logger.info(
            f"[INFO][IMP:10][launcher][main][SERVER] Server stopped by user.[SUCCESS]"
        )
    except Exception as e:
        logger.error(
            f"[ERROR][IMP:10][launcher][main][CRITICAL] Server crash: {e}[FAILURE]"
        )
    # END_BLOCK_LAUNCH


# END_FUNCTION_main

if __name__ == "__main__":
    main()
