# FILE:lesson_16/src/ui_controller.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Обработчики событий для Gradio UI Lesson_16.
# SCOPE:Координация действий между UI и бэкендом.
# INPUT:Параметры из UI компонентов.
# OUTPUT:Данные для обновления UI компонентов (таблица, график).
# KEYWORDS:[DOMAIN(8): UI; TECH(9): Gradio, Plotly]
# LINKS:[USES_API(8): plotly.express, pandas]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля контроллера UI.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Обработчик кнопки Generate Data] => on_generate_click
# FUNC 10[Обработчик кнопки Draw Graph] => on_draw_click
# END_MODULE_MAP

import pandas as pd
import plotly.express as px
import logging
from lesson_16.src.config_manager import save_config
from lesson_16.src.parabola_logic import calculate_parabola
from lesson_16.src.database_manager import save_points, get_points

logger = logging.getLogger(__name__)

# START_FUNCTION_on_generate_click
# START_CONTRACT:
# PURPOSE:Координация сохранения конфига, расчета и записи в БД.
# INPUTS:
# - float => a: Коэффициент a.
# - float => c: Коэффициент c.
# - float => x_min: Минимум x.
# - float => x_max: Максимум x.
# OUTPUTS:
# - pd.DataFrame - Обновленные данные для таблицы.
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def on_generate_click(a: float, c: float, x_min: float, x_max: float) -> pd.DataFrame:
    """
    Выполняет полный цикл обновления данных: сохраняет новые параметры в config.json,
    рассчитывает новые точки параболы и записывает их в SQLite. Возвращает
    результирующий DataFrame для отображения в UI.
    """
    # START_BLOCK_SAVE_CONFIG: [Сохранение параметров]
    config = {"a": a, "c": c, "x_min": x_min, "x_max": x_max}
    save_config(config)
    logger.info(f"[UI][IMP:7][on_generate_click][SAVE_CONFIG][Success] Параметры сохранены. [OK]")
    # END_BLOCK_SAVE_CONFIG
    
    # START_BLOCK_CALC_AND_SAVE: [Расчет и запись в БД]
    df = calculate_parabola(a, c, x_min, x_max)
    save_points(df)
    logger.info(f"[UI][IMP:9][on_generate_click][CALC_AND_SAVE][Success] Данные обновлены в БД. [OK]")
    # END_BLOCK_CALC_AND_SAVE
    
    return df
# END_FUNCTION_on_generate_click

# START_FUNCTION_on_draw_click
# START_CONTRACT:
# PURPOSE:Считывание данных из БД и построение графика.
# INPUTS: Нет
# OUTPUTS:
# - plotly.graph_objects.Figure - Объект графика Plotly.
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def on_draw_click():
    """
    Извлекает текущие точки из базы данных и строит линейный график
    с помощью Plotly Express. Если данных нет, возвращает пустой график.
    """
    # START_BLOCK_FETCH_DATA: [Получение данных из БД]
    df = get_points()
    logger.info(f"[UI][IMP:8][on_draw_click][FETCH_DATA][Success] Считано {len(df)} точек для графика. [OK]")
    # END_BLOCK_FETCH_DATA
    
    # START_BLOCK_CREATE_PLOT: [Построение графика]
    if df.empty:
        fig = px.line(title="No data available")
    else:
        fig = px.line(df, x='x', y='y', title=f"Parabola Plot")
    
    logger.info(f"[UI][IMP:9][on_draw_click][CREATE_PLOT][Success] График построен. [OK]")
    return fig
    # END_BLOCK_CREATE_PLOT
# END_FUNCTION_on_draw_click
