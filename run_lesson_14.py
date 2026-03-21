# FILE:run_lesson_14.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Точка входа для запуска Gradio приложения Lesson 14.
# SCOPE:Инициализация и запуск UI сервера.
# INPUT:Отсутствует (запуск через CLI).
# OUTPUT:Запущенный Gradio сервер.
# KEYWORDS:DOMAIN(Entry Point); CONCEPT(Application); TECH(Gradio)
# LINKS:USES_API(Gradio)
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется отложенный импорт (lazy import)?
# A: Грейдио и другие тяжелые библиотеки могут вызывать ошибки при импорте в начале скрипта, если окружение еще не готово.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание точки входа.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC[10][Точка входа приложения] => main
# END_MODULE_MAP
#
# START_USE_CASES:
# - [main]:User -> Run Script -> Gradio Server Started
# END_USE_CASES

import logging
import sys
import os

# Настройка логирования
logger = logging.getLogger("lesson_14")
logger.setLevel(logging.INFO)
if not logger.handlers:
    fh = logging.FileHandler("lesson_14/app_14.log", encoding="utf-8")
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)

# START_BLOCK_IMPORTS: [Отложенный импорт для ускорения запуска]
def setup_ui():
    import gradio as gr
    from lesson_14.src.ui_controller import UIController

    logger.info("[App][IMP:7][main][Setup][Init] Инициализация Gradio приложения... [INFO]")

    # Создаем контроллер
    ui_controller = UIController()

    # START_BLOCK_CREATE_UI: [Создание компонентов Gradio]
    with gr.Blocks(title="Trigonometric Functions Lesson 14") as demo:
        gr.Markdown("# Trigonometric Functions Calculator")
        gr.Markdown("Генерация и визуализация тригонометрических функций (sin, cos, tan)")

        with gr.Row():
            # Левая колонка: управление
            with gr.Column():
                func_type = gr.Dropdown(
                    choices=["sin", "cos", "tan"],
                    value="sin",
                    label="Function Type"
                )

                x_start = gr.Slider(
                    minimum=-6.28,
                    maximum=6.28,
                    value=0.0,
                    step=0.1,
                    label="X Start"
                )

                x_end = gr.Slider(
                    minimum=-6.28,
                    maximum=6.28,
                    value=6.28,
                    step=0.1,
                    label="X End"
                )

                num_points = gr.Slider(
                    minimum=10,
                    maximum=500,
                    value=100,
                    step=10,
                    label="Number of Points"
                )

                generate_btn = gr.Button("Generate Data", variant="primary")
                draw_btn = gr.Button("Draw Graph", variant="secondary")

                data_table = gr.Dataframe(label="Generated Points")

            # Правая колонка: график
            with gr.Column():
                graph = gr.Plot(label="Trigonometric Function Graph")
        # END_BLOCK_CREATE_UI

        # START_BLOCK_EVENT_HANDLERS: [Связывание событий]
        generate_btn.click(
            fn=ui_controller.handle_generate_data,
            inputs=[func_type, x_start, x_end, num_points],
            outputs=data_table
        )

        draw_btn.click(
            fn=ui_controller.handle_draw_graph,
            inputs=None,
            outputs=graph
        )
        # END_BLOCK_EVENT_HANDLERS

    logger.info("[App][IMP:9][main][Setup][Success] Gradio приложение успешно инициализировано [SUCCESS]")
    return demo
# END_BLOCK_IMPORTS

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE:Точка входа приложения с обработкой прерываний.
# INPUTS:Нет
# OUTPUTS:None
# SIDE_EFFECTS:Запуск Gradio сервера.
# KEYWORDS:PATTERN(Application Entry); CONCEPT(EntryPoint)
# COMPLEXITY_SCORE:3
# END_CONTRACT
def main():
    """
    Основная функция приложения. Настраивает логирование и запускает Gradio сервер.
    Обрабатывает KeyboardInterrupt для корректного завершения.
    """
    # START_BLOCK_SETUP: [Настройка окружения]
    try:
        # Импортируем UI только внутри main для отложенной инициализации
        demo = setup_ui()

        logger.info("[App][IMP:9][main][Launch][Start] Запуск Gradio сервера на http://127.0.0.1:7860 [START]")

        # Запускаем сервер
        demo.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            inbrowser=True
        )

    except KeyboardInterrupt:
        logger.info("[App][IMP:7][main][Shutdown][Signal] Получен сигнал прерывания (Ctrl+C) [INFO]")
        print("\nЗавершение работы Gradio сервера...")
        sys.exit(0)

    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][main][Fatal] Критическая ошибка запуска: {e} [FATAL]")
        sys.exit(1)
    # END_BLOCK_SETUP

if __name__ == "__main__":
    main()
# END_FUNCTION_main
