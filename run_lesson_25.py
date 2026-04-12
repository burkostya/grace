# FILE:run_lesson_25.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Entry point for Lesson 25 Parabola Generator.
# SCOPE:UI Assembly and Gradio server launch.
# INPUT:None (CLI execution).
# OUTPUT:Gradio Web Interface.
# KEYWORDS:[DOMAIN(8):Entrypoint; CONCEPT(7):Launcher; TECH(9):Gradio]
# LINKS:[USES_API(8):gradio; USES_API(8):lesson_25.ui_controller]
# END_MODULE_CONTRACT

# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Initial implementation of the launcher.]
# END_CHANGE_SUMMARY

import logging
import os

# START_BLOCK_LOGGING_CONFIG: [Configuring LDD logging]
LOG_FILE = "lesson_25/app_25.log"
os.makedirs("lesson_25", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
# END_BLOCK_LOGGING_CONFIG


def main():
    """
    Main entry point for the Gradio application.
    Uses lazy imports for heavy libraries to improve startup perception.
    """
    # START_BLOCK_LAZY_IMPORTS: [Importing heavy dependencies]
    import gradio as gr
    from lesson_25.ui_controller import handle_generate, handle_draw, _config_mgr
    # END_BLOCK_LAZY_IMPORTS

    # START_BLOCK_LOAD_INITIAL_STATE: [Loading config for UI defaults]
    config = _config_mgr.load_config()
    # END_BLOCK_LOAD_INITIAL_STATE

    # START_BLOCK_UI_ASSEMBLY: [Building Gradio layout]
    with gr.Blocks(title="Lesson 25: Parabola Generator") as demo:
        gr.Markdown("# Lesson 25: Parabola Generator ($y = ax^2 + c$)")

        with gr.Row():
            # Left Column: Controls and Table
            with gr.Column(scale=1):
                gr.Markdown("### Controls")
                with gr.Group():
                    a_input = gr.Slider(
                        minimum=-10,
                        maximum=10,
                        value=config.get("a", 1.0),
                        label="Coefficient 'a'",
                    )
                    c_input = gr.Slider(
                        minimum=-50,
                        maximum=50,
                        value=config.get("c", 0.0),
                        label="Constant 'c'",
                    )
                    x_min_input = gr.Number(
                        value=config.get("x_min", -10.0), label="x_min"
                    )
                    x_max_input = gr.Number(
                        value=config.get("x_max", 10.0), label="x_max"
                    )

                with gr.Row():
                    btn_generate = gr.Button("Generate Data", variant="primary")
                    btn_draw = gr.Button("Draw Graph")

                gr.Markdown("### Data Table")
                out_table = gr.DataFrame(headers=["x", "y"], label="Points from SQLite")

            # Right Column: Visualization
            with gr.Column(scale=1):
                gr.Markdown("### Visualization")
                out_plot = gr.Plot(label="Parabola Plotly Chart")

        # START_BLOCK_EVENT_BINDING: [Connecting buttons to handlers]
        btn_generate.click(
            fn=handle_generate,
            inputs=[a_input, c_input, x_min_input, x_max_input],
            outputs=out_table,
        )

        btn_draw.click(fn=handle_draw, inputs=[], outputs=out_plot)
        # END_BLOCK_EVENT_BINDING

    # START_BLOCK_LAUNCH: [Starting server]
    logger.info(f"[Launcher][IMP:10][main][Flow] Launching Gradio server... [SUCCESS]")
    demo.launch(inbrowser=True)
    # END_BLOCK_LAUNCH


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("[Launcher][IMP:10][main][Flow] Application stopped by user.")
