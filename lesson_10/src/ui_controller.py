# FILE:lesson_10/src/ui_controller.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Контроллер для Gradio UI, связывающий интерфейс с бизнес-логикой.
# SCOPE:Обработка нажатий кнопок, обновление графиков и таблиц.
# INPUT:События UI, параметры из полей ввода.
# OUTPUT:Обновленные компоненты Gradio (DataFrame, Plotly Figure).
# KEYWORDS:[DOMAIN(UI): Controller; CONCEPT(Interaction): Gradio; TECH(Python): plotly, pandas]
# LINKS:[USES_API(9): gradio, plotly, pandas]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему логика генерации и отрисовки разделена на две функции?
# A: Это соответствует бизнес-требованиям (две кнопки) и позволяет пользователю сначала сгенерировать данные, а затем визуализировать их.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание контроллера UI.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Обрабатывает генерацию данных и сохранение конфига] => handle_generate_data
# FUNC 10[Считывает данные из БД и строит график Plotly] => handle_draw_graph
# END_MODULE_MAP
#
# START_USE_CASES:
# - [handle_generate_data]: User -> Click Generate -> ConfigSaved & DBUpdated
# - [handle_draw_graph]: User -> Click Draw -> PlotlyFigureReturned
# END_USE_CASES

import pandas as pd
import plotly.graph_objects as go
import logging
from lesson_10.src.config_manager import save_config
from lesson_10.src.database_manager import save_points, get_points_df
from lesson_10.src.parabola_logic import calculate_parabola_points

logger = logging.getLogger(__name__)

# START_FUNCTION_handle_generate_data
# START_CONTRACT:
# PURPOSE:Сохраняет параметры в конфиг, рассчитывает точки и пишет в БД.
# INPUTS: 
# - a: float
# - c: float
# - x_min: float
# - x_max: float
# OUTPUTS: 
# - pd.DataFrame - Таблица сгенерированных точек
# SIDE_EFFECTS: Обновляет config.json и data.db.
# KEYWORDS:[PATTERN(Action): Generator]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def handle_generate_data(a: float, c: float, x_min: float, x_max: float) -> pd.DataFrame:
    """
    Выполняет полный цикл генерации данных: сохранение параметров в файл 
    конфигурации, математический расчет точек параболы и их запись в 
    базу данных SQLite. Возвращает DataFrame для отображения в UI.
    """
    # START_BLOCK_PROCESS_GENERATION: [Генерация и сохранение]
    try:
        # 1. Сохранение конфига
        config = {"a": a, "c": c, "x_min": x_min, "x_max": x_max}
        save_config(config)
        
        # 2. Расчет точек
        points = calculate_parabola_points(a, c, x_min, x_max)
        
        # 3. Сохранение в БД
        save_points(points)
        
        # 4. Получение DF для возврата
        df = get_points_df()
        
        logger.info(f"[BeliefState][IMP:9][handle_generate_data][PROCESS_GENERATION][Success] Данные сгенерированы и сохранены. [SUCCESS]")
        return df
    except Exception as e:
        logger.error(f"[SystemError][IMP:10][handle_generate_data][PROCESS_GENERATION][Exception] Ошибка генерации: {e} [FATAL]")
        return pd.DataFrame(columns=['x', 'y'])
    # END_BLOCK_PROCESS_GENERATION
# END_FUNCTION_handle_generate_data

# START_FUNCTION_handle_draw_graph
# START_CONTRACT:
# PURPOSE:Строит интерактивный график на основе данных из БД.
# INPUTS: Нет
# OUTPUTS: 
# - go.Figure - Объект графика Plotly
# SIDE_EFFECTS: Нет.
# KEYWORDS:[PATTERN(Visualization): Plotter]
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def handle_draw_graph() -> go.Figure:
    """
    Считывает текущие данные из базы данных и формирует интерактивный 
    график с помощью Plotly. Если данных нет, возвращает пустую фигуру 
    с соответствующим заголовком.
    """
    # START_BLOCK_CREATE_PLOT: [Отрисовка графика]
    try:
        df = get_points_df()
        
        fig = go.Figure()
        
        if not df.empty:
            fig.add_trace(go.Scatter(
                x=df['x'], 
                y=df['y'], 
                mode='lines+markers', 
                name='Parabola',
                line=dict(color='blue', width=2)
            ))
            fig.update_layout(
                title="Parabola Visualization (y = ax^2 + c)",
                xaxis_title="X",
                yaxis_title="Y",
                template="plotly_white"
            )
            logger.info(f"[BeliefState][IMP:9][handle_draw_graph][CREATE_PLOT][Success] График построен для {len(df)} точек. [SUCCESS]")
        else:
            fig.update_layout(title="No data in database. Click 'Generate Data' first.")
            logger.warning(f"[State][IMP:6][handle_draw_graph][CREATE_PLOT][Empty] Данные в БД отсутствуют. [WARN]")
            
        return fig
    except Exception as e:
        logger.error(f"[SystemError][IMP:10][handle_draw_graph][CREATE_PLOT][Exception] Ошибка отрисовки: {e} [FATAL]")
        return go.Figure()
    # END_BLOCK_CREATE_PLOT
# END_FUNCTION_handle_draw_graph
