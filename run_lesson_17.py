# FILE:run_lesson_17.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Точка входа для запуска Gradio UI Lesson_17.
# SCOPE:Инициализация UI и запуск сервера для тригонометрической функции.
# INPUT:Нет.
# OUTPUT:Запущенный Gradio сервер.
# KEYWORDS:[DOMAIN(8): UI; TECH(9): Gradio, Plotly]
# LINKS:[USES_API(8): gradio, plotly]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание точки входа UI для тригонометрической функции.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Инициализирует и запускает Gradio UI] => main
# END_MODULE_MAP

import logging
import sys
import os

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("lesson_17/app_17.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE:Инициализация и запуск Gradio UI для тригонометрической функции.
# INPUTS: Нет
# OUTPUTS: Нет
# COMPLEXITY_SCORE: 8
# END_CONTRACT
def main():
    """
    Создает интерфейс Gradio с двумя колонками:
    - Левая: Ввод параметров (A, B, C, D, x_min, x_max), кнопки "Generate Data" и "Draw Graph", таблица данных.
    - Правая: График Plotly.
    Использует отложенный импорт для ускорения запуска и предотвращения ошибок окружения.
    """
    # START_BLOCK_LAZY_IMPORTS: [Отложенный импорт тяжелых библиотек]
    import gradio as gr
    from lesson_17.src.config_manager import load_config
    from lesson_17.src.ui_controller import on_generate_click, on_draw_click
    from lesson_17.src.database_manager import get_points
    # END_BLOCK_LAZY_IMPORTS
    
    # START_BLOCK_LOAD_INITIAL_CONFIG: [Загрузка начальных параметров]
    config = load_config()
    initial_df = get_points()
    # END_BLOCK_LOAD_INITIAL_CONFIG
    
    # START_BLOCK_BUILD_UI: [Построение интерфейса Gradio]
    with gr.Blocks(title="Lesson_17: Trigonometric Function") as ui:
        gr.Markdown("# Lesson_17: Trigonometric Function Generator (y = A * sin(B * x + C) + D)")
        
        with gr.Row():
            # Левая колонка: Управление и Таблица
            with gr.Column():
                gr.Markdown("### Parameters")
                A_input = gr.Number(label="Amplitude (A)", value=config.get('A', 1.0))
                B_input = gr.Number(label="Frequency (B)", value=config.get('B', 1.0))
                C_input = gr.Number(label="Phase Shift (C)", value=config.get('C', 0.0))
                D_input = gr.Number(label="Vertical Shift (D)", value=config.get('D', 0.0))
                x_min_input = gr.Number(label="x_min", value=config.get('x_min', -10.0))
                x_max_input = gr.Number(label="x_max", value=config.get('x_max', 10.0))
                
                with gr.Row():
                    btn_generate = gr.Button("Generate Data", variant="primary")
                    btn_draw = gr.Button("Draw Graph")
                
                table_output = gr.Dataframe(value=initial_df, label="Generated Points")
            
            # Правая колонка: График
            with gr.Column():
                gr.Markdown("### Visualization")
                plot_output = gr.Plot(label="Trigonometric Function Plot")
        
        # Привязка событий
        btn_generate.click(
            fn=on_generate_click,
            inputs=[A_input, B_input, C_input, D_input, x_min_input, x_max_input],
            outputs=table_output
        )
        
        btn_draw.click(
            fn=on_draw_click,
            inputs=[],
            outputs=plot_output
        )
    # END_BLOCK_BUILD_UI
    
    # START_BLOCK_LAUNCH_UI: [Запуск сервера]
    try:
        logger.info(f"[UI][IMP:9][main][LAUNCH_UI][Start] Запуск Gradio сервера. [OK]")
        ui.launch(inbrowser=True)
    except KeyboardInterrupt:
        logger.info(f"[UI][IMP:9][main][LAUNCH_UI][Stop] Сервер остановлен пользователем. [OK]")
    except Exception as e:
        logger.critical(f"[UI][IMP:10][main][LAUNCH_UI][Error] Ошибка при запуске UI: {e}. [FATAL]")
    # END_BLOCK_LAUNCH_UI

if __name__ == "__main__":
    main()
# END_FUNCTION_main
