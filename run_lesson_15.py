# FILE: run_lesson_15.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Точка запуска Gradio сервера для Lesson_15.
# SCOPE: UI, Entry Point.
# INPUT: Нет (использует config.json).
# OUTPUT: Gradio Web Server.
# KEYWORDS: [DOMAIN(8): UI; TECH(7): Gradio; CONCEPT(9): EntryPoint]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание точки запуска Gradio.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Основная функция запуска UI] => main
# END_MODULE_MAP

import gradio as gr
import os
import sys
import logging

# Настройка логирования
LOG_FILE = os.path.join(os.path.dirname(__file__), "lesson_15/app_15.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s][%(asctime)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE: Инициализация и запуск Gradio интерфейса.
# INPUTS: Нет
# OUTPUTS: Нет
# COMPLEXITY_SCORE: 7
# END_CONTRACT
def main():
    """
    Основная функция запуска приложения. Использует отложенный импорт (Lazy Import)
    для тяжелых библиотек и внутренних модулей.
    """
    
    # START_BLOCK_LAZY_IMPORTS: [Отложенный импорт]
    from lesson_15.src.config_manager import ConfigManager
    from lesson_15.src.database_manager import DatabaseManager
    from lesson_15.src.ui_controller import on_generate, on_draw
    # END_BLOCK_LAZY_IMPORTS

    # START_BLOCK_SETUP: [Инициализация менеджеров]
    base_dir = os.path.join(os.path.dirname(__file__), "lesson_15")
    config_path = os.path.join(base_dir, "config.json")
    db_path = os.path.join(base_dir, "parabola.db")
    
    config_mgr = ConfigManager(config_path)
    db_mgr = DatabaseManager(db_path)
    
    # Загрузка начального конфига
    config = config_mgr.load()
    logger.info(f"[UI][IMP:7][main][Setup] Начальный конфиг загружен: {config} [INFO]")
    # END_BLOCK_SETUP

    # START_BLOCK_UI_LAYOUT: [Описание интерфейса Gradio]
    with gr.Blocks(title="Lesson 15: Parabola Generator") as ui:
        gr.Markdown("# Lesson 15: Parabola Generator (y = ax^2 + c)")
        
        with gr.Row():
            # Левая колонка: Управление и таблица
            with gr.Column(scale=1):
                gr.Markdown("### Controls")
                a_input = gr.Slider(minimum=-10, maximum=10, value=config["a"], label="Coefficient a")
                c_input = gr.Slider(minimum=-10, maximum=10, value=config["c"], label="Coefficient c")
                x_min_input = gr.Slider(minimum=-50, maximum=0, value=config["x_min"], label="X Min")
                x_max_input = gr.Slider(minimum=0, maximum=50, value=config["x_max"], label="X Max")
                
                with gr.Row():
                    btn_generate = gr.Button("Generate Data", variant="primary")
                    btn_draw = gr.Button("Draw Graph")
                
                gr.Markdown("### Data Table")
                table_output = gr.Dataframe(label="Points Table", interactive=False)
            
            # Правая колонка: График
            with gr.Column(scale=1):
                gr.Markdown("### Visualization")
                plot_output = gr.Plot(label="Parabola Graph")

        # START_BLOCK_UI_EVENTS: [Привязка событий]
        btn_generate.click(
            fn=lambda a, c, x_min, x_max: on_generate(a, c, x_min, x_max, config_mgr, db_mgr),
            inputs=[a_input, c_input, x_min_input, x_max_input],
            outputs=[table_output]
        )
        
        btn_draw.click(
            fn=lambda: on_draw(db_mgr),
            inputs=[],
            outputs=[plot_output]
        )
        # END_BLOCK_UI_EVENTS

    # START_BLOCK_LAUNCH: [Запуск сервера]
    logger.info(f"[BeliefState][IMP:9][main][Launch] Запуск Gradio сервера... [VALUE]")
    try:
        ui.launch(inbrowser=True)
    except KeyboardInterrupt:
        logger.info(f"[UI][IMP:7][main][Shutdown] Сервер остановлен пользователем. [INFO]")
    # END_BLOCK_LAUNCH
# END_FUNCTION_main

if __name__ == "__main__":
    main()
# END_FUNCTION_main
