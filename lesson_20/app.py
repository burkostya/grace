# FILE:lesson_20/app.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Определение интерфейса Gradio для Lesson 20.
# SCOPE:Создание UI компонентов и привязка обработчиков.
# INPUT:Конфигурация из config.json.
# OUTPUT:Объект Gradio Blocks.
# KEYWORDS:[DOMAIN(8): UI; CONCEPT(7): Interface; TECH(9): Gradio]
# LINKS:[USES_API(8): gradio]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется Gradio Blocks?
# A: Это позволяет гибко настраивать макет UI с колонками и вкладками.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание модуля интерфейса Gradio.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Создает и возвращает интерфейс Gradio] => create_app
# END_MODULE_MAP

import gradio as gr
import logging
from lesson_20.config_manager import load_config
from lesson_20.handlers import handle_generate, handle_draw

logger = logging.getLogger("lesson_20")

# START_FUNCTION_create_app
# START_CONTRACT:
# PURPOSE:Создание интерфейса Gradio для генерации и визуализации параболы.
# INPUTS: Нет
# OUTPUTS:
# - gr.Blocks - Объект интерфейса Gradio
# KEYWORDS:[PATTERN(6): Factory]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def create_app() -> gr.Blocks:
    """
    Создает и настраивает интерфейс Gradio с использованием Blocks.
    Загружает начальные значения из конфигурации.
    """
    # START_BLOCK_LOAD_INITIAL_CONFIG: [Загрузка начального конфига]
    config = load_config()
    logger.info(f"[App][IMP:7][create_app][LOAD_INITIAL_CONFIG][Success] Начальный конфиг загружен. [INFO]")
    # END_BLOCK_LOAD_INITIAL_CONFIG
    
    # START_BLOCK_DEFINE_UI: [Определение макета UI]
    with gr.Blocks(title="Lesson 20: Parabola Generator") as app:
        gr.Markdown("# Lesson 20: Parabola Generator y = ax^2 + c")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Parameters")
                a_input = gr.Number(label="Coefficient a", value=config.get("a", 1.0))
                c_input = gr.Number(label="Coefficient c", value=config.get("c", 0.0))
                x_min_input = gr.Number(label="x_min", value=config.get("x_min", -10.0))
                x_max_input = gr.Number(label="x_max", value=config.get("x_max", 10.0))
                
                generate_btn = gr.Button("Generate Points", variant="primary")
                draw_btn = gr.Button("Draw Graph", variant="secondary")
                
            with gr.Column(scale=2):
                with gr.Tabs():
                    with gr.TabItem("Table"):
                        table_output = gr.DataFrame(label="Generated Points")
                    with gr.TabItem("Graph"):
                        plot_output = gr.Plot(label="Parabola Visualization")
        
        # START_BLOCK_BIND_HANDLERS: [Привязка обработчиков событий]
        generate_btn.click(
            fn=handle_generate,
            inputs=[a_input, c_input, x_min_input, x_max_input],
            outputs=table_output
        )
        
        draw_btn.click(
            fn=handle_draw,
            inputs=[],
            outputs=plot_output
        )
        # END_BLOCK_BIND_HANDLERS
        
    logger.info(f"[App][IMP:9][create_app][DEFINE_UI][Success] Интерфейс Gradio создан. [VALUE]")
    return app
    # END_BLOCK_DEFINE_UI
# END_FUNCTION_create_app
