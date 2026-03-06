# FILE:lesson_v5/src/ui_controller.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Контроллер пользовательского интерфейса (UI) на базе Gradio.
# SCOPE:Обработка событий UI, вызов бизнес-логики и визуализация.
# INPUT:Параметры из UI (a, c, range, step).
# OUTPUT:График Plotly и таблица данных.
# KEYWORDS:[DOMAIN(8): UI; CONCEPT(7): Visualization; TECH(9): Gradio]
# LINKS:[USES_API(8): gradio, plotly; WRITES_DATA_TO(9): lesson_v5/parabola.db]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание UI контроллера.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Обработчик генерации для UI] => ui_generate_handler
# FUNC 10[Создает интерфейс Gradio] => create_ui
# END_MODULE_MAP
#
# START_USE_CASES:
# - [ui_generate_handler]: User -> ClickGenerate -> PlotAndTableUpdated
# END_USE_CASES

import gradio as gr
import plotly.graph_objects as go
import pandas as pd
import logging
from lesson_v5.src.config_manager import load_config
from lesson_v5.src.database_manager import DatabaseManager
from lesson_v5.src.parabola_logic import generate_parabola_points

logger = logging.getLogger(__name__)

# START_FUNCTION_ui_generate_handler
# START_CONTRACT:
# PURPOSE:Обрабатывает запрос на генерацию из UI и возвращает визуализацию.
# INPUTS: 
# - float => a: Коэффициент a
# - float => c: Коэффициент c
# - float => min_x: Минимум x
# - float => max_x: Максимум x
# - float => step: Шаг x
# OUTPUTS: 
# - tuple - (Plotly Figure, Pandas DataFrame)
# SIDE_EFFECTS: Запись в БД.
# KEYWORDS:[PATTERN(6): Controller; CONCEPT(8): Visualization]
# END_CONTRACT
def ui_generate_handler(a: float, c: float, min_x: float, max_x: float, step: float):
    """Обработчик генерации для UI."""
    
    # START_BLOCK_UI_GENERATE: [Логика генерации и визуализации]
    logger.info(f"[BeliefState][IMP:9][UI][GENERATE][Start] UI запрос: a={a}, c={c}, range=[{min_x}, {max_x}], step={step} [VALUE]")
    
    try:
        config = load_config()
        db = DatabaseManager(config["db_path"])
        
        # Генерация точек
        points = generate_parabola_points(a, c, [min_x, max_x], step)
        
        # Сохранение в БД
        db_points = [(a, c, x, y) for x, y in points]
        db.save_points(db_points)
        
        # Подготовка данных для визуализации
        df = pd.DataFrame(points, columns=["x", "y"])
        
        # Создание графика Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["x"], y=df["y"], mode='lines+markers', name=f'y={a}x^2+{c}'))
        fig.update_layout(title="График параболы", xaxis_title="X", yaxis_title="Y")
        
        logger.info(f"[BeliefState][IMP:9][UI][GENERATE][Success] Визуализация готова. [VALUE]")
        return fig, df
        
    except Exception as e:
        logger.error(f"[SystemError][IMP:10][UI][GENERATE][Exception] Ошибка UI генерации: {e} [FATAL]")
        return None, pd.DataFrame()
    # END_BLOCK_UI_GENERATE
# END_FUNCTION_ui_generate_handler

# START_FUNCTION_create_ui
# START_CONTRACT:
# PURPOSE:Создает и настраивает интерфейс Gradio.
# INPUTS: Нет
# OUTPUTS: 
# - gradio.Blocks -Объект интерфейса
# SIDE_EFFECTS: Нет.
# KEYWORDS:[PATTERN(6): Factory; CONCEPT(8): UI_Layout]
# END_CONTRACT
def create_ui():
    """Создает интерфейс Gradio."""
    
    # START_BLOCK_UI_LAYOUT: [Определение структуры интерфейса]
    config = load_config()
    
    with gr.Blocks(title="Генератор параболы v5") as demo:
        gr.Markdown("# Генератор параболы y = ax² + c")
        
        with gr.Row():
            # Левая колонка: Управление
            with gr.Column():
                gr.Markdown("### Параметры")
                a_input = gr.Number(label="Коэффициент a", value=config["default_a"])
                c_input = gr.Number(label="Коэффициент c", value=config["default_c"])
                min_x_input = gr.Number(label="Min X", value=config["range_x"][0])
                max_x_input = gr.Number(label="Max X", value=config["range_x"][1])
                step_input = gr.Number(label="Шаг", value=config["step"])
                
                generate_btn = gr.Button("Сгенерировать", variant="primary")
            
            # Правая колонка: Вывод
            with gr.Column():
                gr.Markdown("### Результаты")
                plot_output = gr.Plot(label="График")
                table_output = gr.Dataframe(label="Точки")
        
        # Привязка событий
        generate_btn.click(
            fn=ui_generate_handler,
            inputs=[a_input, c_input, min_x_input, max_x_input, step_input],
            outputs=[plot_output, table_output]
        )
        
    return demo
    # END_BLOCK_UI_LAYOUT
# END_FUNCTION_create_ui

if __name__ == "__main__":
    demo = create_ui()
    demo.launch()
# END_FUNCTION_create_ui
