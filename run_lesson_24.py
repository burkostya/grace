# FILE:run_lesson_24.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Main entry point for starting the Gradio UI of Lesson 24.
# SCOPE: Application launch.
# INPUT: Command line.
# OUTPUT: Gradio server (Gradio server instance).
# KEYWORDS:DOMAIN(Parabola): Launcher; CONCEPT(Gradio): UI_Launch
# LINKS:USES_API(Gradio); USES_API(logging); READS_DATA_FROM(lesson_24/ui_controller.py)
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: 1.0.0 - Initial implementation of launcher.
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC [10][Initializes and launches the Gradio server] => main
# END_MODULE_MAP

import logging
import sys
import os

# Configure logging
# START_BLOCK_LOGGING_CONFIG: [Setup unified logging to file and stdout]
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("lesson_24/app_24.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("lesson_24.launcher")
# END_BLOCK_LOGGING_CONFIG


# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE:Launch the Gradio UI for the parabola calculator.
# INPUTS: None
# OUTPUTS: None
# SIDE_EFFECTS: Starts local HTTP server.
# KEYWORDS:PATTERN(App): EntryPoint
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def main():
    """
    Constructs the Gradio UI layout and starts the server.
    Loads initial parameters from config.json.
    Includes error handling for server launch.
    """
    # START_BLOCK_UI_DESIGN:[Define Gradio interface layout]
    try:
        import gradio as gr
        from lesson_24 import config_manager, ui_controller

        # Load initial config
        config = config_manager.load_config()

        with gr.Blocks(title="Lesson 24 - Parabola Framework") as demo:
            gr.Markdown("# Lesson 24: Parabola y = ax^2 + c")

            with gr.Row():
                # Left Column: Controls & Table
                with gr.Column(scale=1):
                    gr.Markdown("### 1. Generation Controls")
                    a_slider = gr.Slider(
                        minimum=-10,
                        maximum=10,
                        value=config.get("a", 1.0),
                        label="a (Coefficient)",
                    )
                    c_slider = gr.Slider(
                        minimum=-50,
                        maximum=50,
                        value=config.get("c", 0.0),
                        label="c (Constant)",
                    )
                    x_min_slider = gr.Slider(
                        minimum=-100,
                        maximum=0,
                        value=config.get("x_min", -10.0),
                        label="x_min",
                    )
                    x_max_slider = gr.Slider(
                        minimum=0,
                        maximum=100,
                        value=config.get("x_max", 10.0),
                        label="x_max",
                    )

                    with gr.Row():
                        btn_gen = gr.Button("Generate Data", variant="primary")
                        btn_plot = gr.Button("Draw Graph", variant="secondary")

                    table_output = gr.Dataframe(label="Parabola Points (from SQLite)")

                # Right Column: Graph
                with gr.Column(scale=1):
                    gr.Markdown("### 2. Visualization")
                    plot_output = gr.Plot(label="Plotly Interactive Graph")

            # Event handlers
            btn_gen.click(
                fn=ui_controller.handle_generate_data,
                inputs=[a_slider, c_slider, x_min_slider, x_max_slider],
                outputs=[table_output],
            )

            btn_plot.click(
                fn=ui_controller.handle_draw_graph, inputs=[], outputs=[plot_output]
            )

        logger.info(
            "[IMP:9][main][LAUNCH][UI] Gradio UI initialized successfully.[BELIEF:SERVER_START]"
        )
        demo.launch(inbrowser=True)
    except Exception as e:
        logger.error(
            f"[IMP:10][main][LAUNCH][ERROR] Failed to start Gradio UI: {str(e)}[CRITICAL]"
        )
        sys.exit(1)
    # END_BLOCK_UI_DESIGN


# END_FUNCTION_main

if __name__ == "__main__":
    main()
