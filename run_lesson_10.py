# FILE:run_lesson_10.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Точка запуска Gradio UI для приложения Lesson 10.
# SCOPE:Инициализация интерфейса, настройка компонентов и запуск сервера.
# INPUT:Параметры из config.json (при старте).
# OUTPUT:Запущенный веб-сервер Gradio.
# KEYWORDS:[DOMAIN(UI): EntryPoint; CONCEPT(AgenticUX): Interactive; TECH(Python): gradio]
# LINKS:[USES_API(9): gradio]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется Lazy Import для Gradio?
# A: Согласно паттернам надежного запуска, это предотвращает сбои при инициализации, если окружение еще не полностью готово.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание скрипта запуска UI.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Инициализирует и запускает Gradio UI] => main
# END_MODULE_MAP
#
# START_USE_CASES:
# - [main]: User -> run_lesson_10.py -> GradioServerStarted
# END_USE_CASES

import logging
import sys
import os

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s][IMP:9][UI_SERVER] %(message)s',
    handlers=[
        logging.FileHandler("lesson_10/app_10.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE:Создает и запускает интерфейс Gradio.
# INPUTS: Нет
# OUTPUTS: None
# SIDE_EFFECTS: Запускает веб-сервер.
# KEYWORDS:[PATTERN(Entry): Server]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def main():
    """
    Инициализирует Gradio интерфейс с двумя колонками: управление и 
    визуализация. Настраивает обработчики событий для кнопок генерации 
    и отрисовки. Использует отложенный импорт для тяжелых библиотек.
    """
    # START_BLOCK_LAZY_IMPORTS: [Отложенный импорт]
    import gradio as gr
    from lesson_10.src.config_manager import load_config
    from lesson_10.src.ui_controller import handle_generate_data, handle_draw_graph
    # END_BLOCK_LAZY_IMPORTS

    # START_BLOCK_UI_DEFINITION: [Определение интерфейса]
    config = load_config()
    
    with gr.Blocks(title="Lesson 10: Parabola Generator") as ui:
        gr.Markdown("# Parabola Generator (y = ax^2 + c)")
        
        with gr.Row():
            # Левая колонка: Управление
            with gr.Column():
                gr.Markdown("### Parameters")
                a_input = gr.Slider(minimum=-10, maximum=10, value=config['a'], label="Coefficient a")
                c_input = gr.Slider(minimum=-100, maximum=100, value=config['c'], label="Coefficient c")
                x_min_input = gr.Slider(minimum=-100, maximum=0, value=config['x_min'], label="X Min")
                x_max_input = gr.Slider(minimum=0, maximum=100, value=config['x_max'], label="X Max")
                
                with gr.Row():
                    btn_generate = gr.Button("Generate Data", variant="primary")
                    btn_draw = gr.Button("Draw Graph")
                
                table_output = gr.Dataframe(label="Points Table", interactive=False)
            
            # Правая колонка: График
            with gr.Column():
                plot_output = gr.Plot(label="Parabola Graph")
        
        # Настройка событий
        btn_generate.click(
            fn=handle_generate_data,
            inputs=[a_input, c_input, x_min_input, x_max_input],
            outputs=table_output
        )
        
        btn_draw.click(
            fn=handle_draw_graph,
            inputs=[],
            outputs=plot_output
        )
        
        logger.info(f"[BeliefState][IMP:9][main][UI_DEFINITION][Success] Интерфейс Gradio сконфигурирован. [SUCCESS]")
    # END_BLOCK_UI_DEFINITION

    # START_BLOCK_LAUNCH_SERVER: [Запуск сервера]
    try:
        logger.info(f"[State][IMP:8][main][LAUNCH_SERVER][IO] Запуск Gradio сервера... [INFO]")
        ui.launch(inbrowser=True, share=False)
    except KeyboardInterrupt:
        logger.info(f"[State][IMP:7][main][LAUNCH_SERVER][Interrupt] Сервер остановлен пользователем. [INFO]")
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][main][LAUNCH_SERVER][Exception] Ошибка запуска сервера: {e} [FATAL]")
    # END_BLOCK_LAUNCH_SERVER
# END_FUNCTION_main

if __name__ == "__main__":
    main()
# END_FUNCTION_main
