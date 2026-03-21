# FILE:run_lesson_13.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Точка входа в приложение Lesson 13 с интерфейсом Gradio.
# SCOPE: Инициализация UI, настройка компонентов и запуск сервера.
# INPUT: Пользовательский ввод через веб-интерфейс.
# OUTPUT: Веб-интерфейс Gradio.
# KEYWORDS:[DOMAIN(App): EntryPoint; TECH(UI): Gradio; CONCEPT(UX): Interactive]
# LINKS:[USES_API(Controller): UIController]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание точки входа с использованием Gradio и отложенным импортом.]
# END_CHANGE_SUMMARY

import logging
import sys
import os

# Настройка логирования для вывода в консоль и файл
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s]%(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("lesson_13/app_13.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("lesson_13")

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE: Инициализация и запуск Gradio интерфейса.
# INPUTS: Нет
# OUTPUTS: Нет
# SIDE_EFFECTS: Запускает локальный веб-сервер.
# KEYWORDS:[PATTERN(Startup): Main; CONCEPT(UI): Layout]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def main():
    """
    Основная функция запуска приложения. Использует отложенный импорт для тяжелых библиотек
    и настраивает макет интерфейса Gradio с двумя колонками.
    """
    logger.info(f"[App][IMP:9][main][Start] Запуск приложения Lesson 13 [START]")

    # START_BLOCK_LAZY_IMPORTS: [Отложенный импорт]
    try:
        import gradio as gr
        from lesson_13.src.ui_controller import UIController
        logger.debug(f"[App][IMP:4][main][LAZY_IMPORTS] Библиотеки успешно импортированы [SUCCESS]")
    except ImportError as e:
        logger.critical(f"[App][IMP:10][main][LAZY_IMPORTS] Ошибка импорта: {e} [FATAL]")
        return
    # END_BLOCK_LAZY_IMPORTS

    # START_BLOCK_INIT_CONTROLLER: [Инициализация контроллера]
    controller = UIController()
    # END_BLOCK_INIT_CONTROLLER

    # START_BLOCK_UI_LAYOUT: [Определение макета UI]
    with gr.Blocks(title="Lesson 13: Parabola Generator") as demo:
        gr.Markdown("# Parabola Data Generator and Visualizer")
        
        with gr.Row():
            # Левая колонка: Ввод и Таблица
            with gr.Column():
                gr.Markdown("### Parameters")
                with gr.Row():
                    a_input = gr.Number(label="Coefficient A", value=1.0)
                    b_input = gr.Number(label="Coefficient B", value=0.0)
                    c_input = gr.Number(label="Coefficient C", value=0.0)
                
                with gr.Row():
                    x_start = gr.Number(label="X Start", value=-10.0)
                    x_end = gr.Number(label="X End", value=10.0)
                    num_points = gr.Slider(label="Number of Points", minimum=2, maximum=1000, value=100, step=1)
                
                generate_btn = gr.Button("Generate Data", variant="primary")
                data_table = gr.DataFrame(label="Generated Points")
            
            # Правая колонка: График
            with gr.Column():
                gr.Markdown("### Visualization")
                draw_btn = gr.Button("Draw Graph")
                plot_output = gr.Plot(label="Parabola Plot")

        # START_BLOCK_EVENT_HANDLERS: [Привязка обработчиков]
        generate_btn.click(
            fn=controller.handle_generate_data,
            inputs=[a_input, b_input, c_input, x_start, x_end, num_points],
            outputs=data_table
        )
        
        draw_btn.click(
            fn=controller.handle_draw_graph,
            inputs=[],
            outputs=plot_output
        )
        # END_BLOCK_EVENT_HANDLERS

    # END_BLOCK_UI_LAYOUT

    # START_BLOCK_LAUNCH: [Запуск]
    try:
        logger.info(f"[App][IMP:9][main][LAUNCH] Запуск Gradio сервера... [RUNNING]")
        demo.launch(inbrowser=True)
    except KeyboardInterrupt:
        logger.info(f"[App][IMP:9][main][LAUNCH] Сервер остановлен пользователем [STOPPED]")
    except Exception as e:
        logger.error(f"[App][IMP:10][main][LAUNCH] Ошибка при запуске сервера: {e} [FAIL]")
    # END_BLOCK_LAUNCH

# END_FUNCTION_main

if __name__ == "__main__":
    main()
