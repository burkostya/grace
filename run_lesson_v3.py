# FILE:run_lesson_v3.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Точка запуска Gradio интерфейса для Lesson_v3.
# SCOPE:Инициализация UI, настройка колонок и запуск сервера.
# INPUT:Нет.
# OUTPUT:Запущенный сервер Gradio.
# KEYWORDS:[DOMAIN(8):UI; CONCEPT(7):Gradio_App; TECH(9):Python_gradio]
# LINKS:[USES_API(9):ui_controller, config_manager]
# END_MODULE_CONTRACT

# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание точки запуска UI.]
# END_CHANGE_SUMMARY

# START_MODULE_MAP:
# FUNC 10[Создает и запускает Gradio интерфейс] => main
# END_MODULE_MAP

import gradio as gr
import os
import sys
import logging

# Добавляем корень проекта в sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lesson_v3.src.ui_controller import on_generate_click, on_draw_click
from lesson_v3.src.config_manager import load_config

# Настройка логирования
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lesson_v3", "app_v3.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lesson_v3", "config.json")

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE:Инициализация и запуск Gradio.
# INPUTS: Нет
# OUTPUTS: Нет
# SIDE_EFFECTS: Запускает веб-сервер.
# END_CONTRACT
def main():
    """Запуск Gradio интерфейса."""
    # START_BLOCK_BUILD_UI: [Построение интерфейса]
    config = load_config(CONFIG_PATH)
    
    with gr.Blocks(title="Lesson_v3: Parabola Generator") as demo:
        gr.Markdown("# Lesson_v3: Parabola Generator $y = ax^2 + c$")
        
        with gr.Row():
            # Левая колонка: Ввод и Управление
            with gr.Column():
                gr.Markdown("### Parameters")
                a_input = gr.Number(label="Coefficient a", value=config["a"])
                c_input = gr.Number(label="Coefficient c", value=config["c"])
                x_min_input = gr.Number(label="x_min", value=config["x_min"])
                x_max_input = gr.Number(label="x_max", value=config["x_max"])
                
                with gr.Row():
                    btn_generate = gr.Button("Generate Data", variant="primary")
                    btn_draw = gr.Button("Draw Graph")
                
                status_output = gr.Textbox(label="Status", interactive=False)
            
            # Правая колонка: Вывод
            with gr.Column():
                gr.Markdown("### Results")
                table_output = gr.DataFrame(label="Points Table")
                plot_output = gr.Plot(label="Parabola Graph")
        
        # Привязка событий
        btn_generate.click(
            fn=on_generate_click,
            inputs=[a_input, c_input, x_min_input, x_max_input],
            outputs=status_output
        )
        
        btn_draw.click(
            fn=on_draw_click,
            inputs=[],
            outputs=[table_output, plot_output]
        )
    # END_BLOCK_BUILD_UI

    # START_BLOCK_LAUNCH_SERVER: [Запуск сервера]
    logger.info(f"[BeliefState][IMP:9][main][LAUNCH_SERVER][Success] Запуск Gradio сервера Lesson_v3. [VALUE]")
    demo.launch(server_name="127.0.0.1", server_port=7860)
    # END_BLOCK_LAUNCH_SERVER

if __name__ == "__main__":
    main()
# END_FUNCTION_main
