# FILE:lesson_12/handlers.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Чистая бизнес-логика для работы с параболой и визуализацией.
# SCOPE: Генерация точек, подготовка данных для графиков Plotly.
# INPUT: Коэффициенты параболы, данные из таблицы.
# OUTPUT: Pandas DataFrame, Plotly Figure.
# KEYWORDS:[DOMAIN(8): Mathematics; CONCEPT(9): PureLogic; TECH(7): Plotly]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему здесь нет импортов Dash?
# A: Для обеспечения Headless-тестируемости. Логика должна работать независимо от UI-фреймворка.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.1 - Исправление семантической разметки: добавлены MODULE_MAP и USE_CASES.]
# PREV_CHANGE_SUMMARY: [v1.0.0 - Создание модуля с функциями генерации точек и построения графиков.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Генерирует точки параболы y = ax^2 + c] => generate_parabola_points
# FUNC 9[Строит сравнительный график Original vs Edited] => build_comparison_figure
# END_MODULE_MAP
#
# START_USE_CASES:
# - [generate_parabola_points]: User -> InputParams -> ParabolaDataFrame
# - [build_comparison_figure]: User -> TableData -> PlotlyFigure
# END_USE_CASES

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import logging

logger = logging.getLogger("lesson_12.app")

# START_FUNCTION_generate_parabola_points
# START_CONTRACT:
# PURPOSE: Расчет точек параболы и инициализация колонки редактирования.
# INPUTS: 
# - a: float - Коэффициент кривизны
# - c: float - Смещение по y
# - x_min: float - Начало диапазона
# - x_max: float - Конец диапазона
# - step: float - Шаг дискретизации
# OUTPUTS: 
# - pd.DataFrame - Таблица с колонками [x, y, y_edited]
# KEYWORDS:[CONCEPT(8): DataGeneration]
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def generate_parabola_points(a: float, c: float, x_min: float, x_max: float, step: float = 1.0) -> pd.DataFrame:
    """
    Функция генерирует массив значений x в заданном диапазоне и вычисляет соответствующие значения y 
    по формуле y = ax^2 + c. Также создается колонка y_edited, которая изначально является копией y.
    Это позволяет пользователю в дальнейшем редактировать значения в UI.
    """
    # START_BLOCK_CALCULATION: [Математический расчет]
    logger.debug(f"[Logic][IMP:5][generate_parabola_points][CALCULATION][Start] Params: a={a}, c={c}, range=[{x_min}, {x_max}] [INFO]")
    
    x_values = np.arange(x_min, x_max + step, step)
    y_values = a * (x_values ** 2) + c
    
    df = pd.DataFrame({
        "x": x_values,
        "y": y_values,
        "y_edited": y_values
    })
    # END_BLOCK_CALCULATION

    logger.info(f"[BeliefState][IMP:9][generate_parabola_points][CALCULATION][Success] Сгенерировано {len(df)} точек. [VALUE]")
    return df
# END_FUNCTION_generate_parabola_points

# START_FUNCTION_build_comparison_figure
# START_CONTRACT:
# PURPOSE: Создание интерактивного графика для сравнения исходных и измененных данных.
# INPUTS: 
# - table_data: list[dict] - Данные из DataTable
# OUTPUTS: 
# - go.Figure - Объект графика Plotly
# KEYWORDS:[CONCEPT(9): Visualization]
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def build_comparison_figure(table_data: list[dict]) -> go.Figure:
    """
    Функция принимает список словарей (формат Dash DataTable) и строит две линии на графике.
    Первая линия отображает исходные значения 'y', вторая — отредактированные 'y_edited'.
    Это позволяет наглядно увидеть разницу после ручного вмешательства пользователя.
    """
    # START_BLOCK_PREPARE_DATA: [Конвертация данных]
    if not table_data:
        logger.warning("[Logic][IMP:7][build_comparison_figure][PREPARE_DATA][Empty] Данные таблицы пусты. [WARN]")
        return go.Figure()
        
    df = pd.DataFrame(table_data)
    # END_BLOCK_PREPARE_DATA

    # START_BLOCK_CREATE_PLOT: [Построение графика]
    fig = go.Figure()
    
    # Исходная кривая
    fig.add_trace(go.Scatter(
        x=df["x"], y=df["y"],
        mode="lines+markers",
        name="Original (y)",
        line=dict(color="blue", dash="dash")
    ))
    
    # Отредактированная кривая
    fig.add_trace(go.Scatter(
        x=df["x"], y=df["y_edited"],
        mode="lines+markers",
        name="Edited (y_edited)",
        line=dict(color="red", width=3)
    ))
    
    fig.update_layout(
        title="Parabola Comparison: Original vs Edited",
        xaxis_title="X",
        yaxis_title="Y",
        template="plotly_white",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    # END_BLOCK_CREATE_PLOT

    logger.info(f"[BeliefState][IMP:9][build_comparison_figure][CREATE_PLOT][Success] График построен для {len(df)} точек. [VALUE]")
    return fig
# END_FUNCTION_build_comparison_figure
