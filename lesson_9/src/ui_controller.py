# FILE:lesson_9/src/ui_controller.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление пользовательским интерфейсом (UI) на базе Gradio.
# SCOPE: Создание веб-интерфейса для настройки параметров, генерации данных и визуализации.
# INPUT:Ввод пользователя через виджеты Gradio, данные из SQLite.
# OUTPUT: Интерактивный график Plotly, таблица данных, обновленный config.json.
# KEYWORDS:[DOMAIN(8): UI; CONCEPT(7): Visualization; TECH(9): gradio, plotly, pandas]
# LINKS:[USES_API(8): gradio, plotly, pandas; USES_MODULE(9): config_manager, database_manager, parabola_logic]
# LINKS_TO_SPECIFICATION:[DevelopmentPlan.md:32-39]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание UI контроллера с Gradio и Plotly.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC [9][Обработчик генерации данных] => handle_generate
# FUNC [9][Обработчик отрисовки графика] => handle_draw_graph
# FUNC [10][Создание интерфейса Gradio] => create_ui
# END_MODULE_MAP
#
# START_USE_CASES:
# - [handle_generate]: User -> Click 'Generate' -> DataStoredAndTableUpdated
# - [handle_draw_graph]: User -> Click 'Draw' -> PlotlyChartRendered
# END_USE_CASES

import gradio as gr
import pandas as pd
import plotly.graph_objects as go
import logging
from lesson_9.src.config_manager import load_config, save_config
from lesson_9.src.database_manager import save_points, get_points
from lesson_9.src.parabola_logic import calculate_parabola_points

# Настройка логгера для LDD 2.0
logger = logging.getLogger("lesson_9")

# START_FUNCTION_handle_generate
# START_CONTRACT:
# PURPOSE:Сохранение параметров, расчет точек и обновление таблицы.
# INPUTS: 
# - float => a, c, x_min, x_max: Параметры параболы.
# OUTPUTS: 
# - pd.DataFrame - Данные для отображения в таблице.
# SIDE_EFFECTS: Обновление config.json и SQLite БД.
# KEYWORDS:[PATTERN(8): Callback; CONCEPT(9): DataUpdate]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def handle_generate(a, c, x_min, x_max):
    """
    Обработчик кнопки 'Generate Data'. Сохраняет текущие значения 
    ползунков в конфиг, вычисляет точки и записывает их в БД. 
    Возвращает DataFrame для обновления компонента gr.Dataframe.
    """
    # START_BLOCK_SAVE_CONFIG: [Обновление конфига]
    new_config = {"a": a, "c": c, "x_min": x_min, "x_max": x_max}
    save_config(new_config)
    logger.info(f"[UI][IMP:7][handle_generate][SAVE_CONFIG][Success] Конфиг обновлен: {new_config} [INFO]")
    # END_BLOCK_SAVE_CONFIG

    # START_BLOCK_PROCESS: [Расчет и сохранение]
    points = calculate_parabola_points(a, c, x_min, x_max)
    save_points(points)
    logger.info(f"[UI][IMP:9][handle_generate][PROCESS][Success] Сгенерировано и сохранено {len(points)} точек. [VALUE]")
    # END_BLOCK_PROCESS

    # START_BLOCK_PREPARE_DF: [Подготовка данных для таблицы]
    df = pd.DataFrame(points, columns=['x', 'y'])
    return df
    # END_BLOCK_PREPARE_DF
# END_FUNCTION_handle_generate

# START_FUNCTION_handle_draw_graph
# START_CONTRACT:
# PURPOSE:Построение графика Plotly на основе данных из БД.
# INPUTS: 
# - None
# OUTPUTS: 
# - go.Figure - Объект графика Plotly.
# SIDE_EFFECTS: Чтение из БД.
# KEYWORDS:[PATTERN(8): Visualization; CONCEPT(9): PlotlyChart]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def handle_draw_graph():
    """
    Обработчик кнопки 'Draw Graph'. Читает данные из базы данных 
    и строит интерактивный график параболы с помощью Plotly.
    """
    # START_BLOCK_FETCH: [Получение данных]
    points = get_points()
    if not points:
        logger.warning(f"[UI][IMP:8][handle_draw_graph][FETCH][Empty] Нет данных для построения графика. [WARNING]")
        return go.Figure()
    # END_BLOCK_FETCH

    # START_BLOCK_PLOT: [Создание фигуры Plotly]
    df = pd.DataFrame(points, columns=['x', 'y'])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['x'], y=df['y'], mode='lines+markers', name='Parabola'))
    fig.update_layout(
        title="Parabola Visualization (y = ax^2 + c)",
        xaxis_title="X",
        yaxis_title="Y",
        template="plotly_white"
    )
    logger.info(f"[UI][IMP:9][handle_draw_graph][PLOT][Success] График построен для {len(df)} точек. [VALUE]")
    return fig
    # END_BLOCK_PLOT
# END_FUNCTION_handle_draw_graph

# START_FUNCTION_create_ui
# START_CONTRACT:
# PURPOSE:Сборка интерфейса Gradio.
# INPUTS: 
# - None
# OUTPUTS: 
# - gr.Blocks - Объект интерфейса Gradio.
# SIDE_EFFECTS: Нет.
# KEYWORDS:[PATTERN(7): Factory; CONCEPT(8): Layout]
# COMPLEXITY_SCORE: 7
# END_CONTRACT
def create_ui():
    """
    Функция конструирует интерфейс Gradio, используя Blocks. 
    Реализует двухколоночную верстку: управление слева, визуализация справа.
    """
    # Загружаем начальные значения
    config = load_config()

    with gr.Blocks(title="Lesson 9: Parabola Explorer") as demo:
        gr.Markdown("# 📈 Parabola Explorer (Lesson 9)")
        
        with gr.Row():
            # Левая колонка: Управление
            with gr.Column():
                gr.Markdown("### 🛠 Parameters")
                a_slider = gr.Slider(minimum=-10, maximum=10, value=config['a'], step=0.1, label="Coefficient 'a'")
                c_slider = gr.Slider(minimum=-50, maximum=50, value=config['c'], step=0.5, label="Constant 'c'")
                xmin_slider = gr.Slider(minimum=-100, maximum=0, value=config['x_min'], step=1, label="X Min")
                xmax_slider = gr.Slider(minimum=0, maximum=100, value=config['x_max'], step=1, label="X Max")
                
                with gr.Row():
                    gen_btn = gr.Button("🚀 Generate Data", variant="primary")
                    draw_btn = gr.Button("📊 Draw Graph")
                
                gr.Markdown("### 📋 Data Table")
                table = gr.Dataframe(headers=["x", "y"], interactive=False)

            # Правая колонка: График
            with gr.Column():
                gr.Markdown("### 📉 Visualization")
                plot = gr.Plot(label="Parabola Plot")

        # Привязка событий
        gen_btn.click(
            fn=handle_generate,
            inputs=[a_slider, c_slider, xmin_slider, xmax_slider],
            outputs=table
        )
        
        draw_btn.click(
            fn=handle_draw_graph,
            inputs=[],
            outputs=plot
        )

    logger.info(f"[UI][IMP:10][create_ui][INIT][Success] Интерфейс Gradio успешно сконфигурирован. [SUCCESS]")
    return demo
# END_FUNCTION_create_ui
