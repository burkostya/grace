# FILE:lesson_20/handlers.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Обработчики событий UI Gradio для Lesson 20.
# SCOPE:Связь UI с бизнес-логикой, БД и конфигурацией.
# INPUT:Параметры из Gradio UI.
# OUTPUT:DataFrame для таблицы и Figure для графика.
# KEYWORDS:[DOMAIN(8): UI; CONCEPT(7): Handlers; TECH(9): Gradio, Plotly, Pandas]
# LINKS:[USES_API(8): pandas, plotly.graph_objects]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему обработчики вынесены в отдельный файл?
# A: Это позволяет проводить Headless-тестирование логики UI без запуска сервера Gradio.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание модуля обработчиков UI.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Обрабатывает генерацию точек] => handle_generate
# FUNC 10[Обрабатывает отрисовку графика] => handle_draw
# END_MODULE_MAP

import pandas as pd
import plotly.graph_objects as go
import logging
from lesson_20.config_manager import save_config
from lesson_20.db_manager import save_points, get_points
from lesson_20.logic import calculate_parabola

logger = logging.getLogger("lesson_20")

# START_FUNCTION_handle_generate
# START_CONTRACT:
# PURPOSE:Сохранение конфига, расчет точек и сохранение в БД.
# INPUTS:
# - float => a: Коэффициент a
# - float => c: Коэффициент c
# - float => x_min: Минимум x
# - float => x_max: Максимум x
# OUTPUTS:
# - pd.DataFrame - Таблица с точками
# KEYWORDS:[PATTERN(6): Controller]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def handle_generate(a: float, c: float, x_min: float, x_max: float) -> pd.DataFrame:
    """
    Обрабатывает нажатие кнопки 'Generate'. Сохраняет параметры в конфиг,
    рассчитывает точки параболы, сохраняет их в БД и возвращает DataFrame.
    """
    # START_BLOCK_SAVE_CONFIG: [Сохранение конфигурации]
    config = {"a": a, "c": c, "x_min": x_min, "x_max": x_max}
    save_config(config)
    logger.info(f"[UI][IMP:7][handle_generate][SAVE_CONFIG][Success] Конфиг обновлен. [INFO]")
    # END_BLOCK_SAVE_CONFIG
    
    # START_BLOCK_CALC_AND_DB: [Расчет и сохранение в БД]
    points = calculate_parabola(a, c, x_min, x_max)
    if points:
        save_points(points)
        logger.info(f"[UI][IMP:9][handle_generate][CALC_AND_DB][Success] Точки сохранены в БД. [VALUE]")
    else:
        logger.error(f"[UI][IMP:10][handle_generate][CALC_AND_DB][Error] Ошибка генерации точек. [FATAL]")
    # END_BLOCK_CALC_AND_DB
    
    # START_BLOCK_RETURN_DF: [Формирование DataFrame]
    df = pd.DataFrame(points, columns=["x", "y"])
    return df
    # END_BLOCK_RETURN_DF
# END_FUNCTION_handle_generate

# START_FUNCTION_handle_draw
# START_CONTRACT:
# PURPOSE:Загрузка точек из БД и отрисовка графика Plotly.
# INPUTS: Нет
# OUTPUTS:
# - go.Figure - Объект графика Plotly
# KEYWORDS:[PATTERN(6): Visualizer]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def handle_draw() -> go.Figure:
    """
    Обрабатывает нажатие кнопки 'Draw Graph'. Загружает точки из БД
    и строит график параболы с помощью Plotly.
    """
    # START_BLOCK_LOAD_DATA: [Загрузка данных из БД]
    points = get_points()
    if not points:
        logger.warning(f"[UI][IMP:7][handle_draw][LOAD_DATA][Warning] Нет данных в БД для отрисовки. [INFO]")
        fig = go.Figure()
        fig.update_layout(title="No data in DB")
        return fig
    # END_BLOCK_LOAD_DATA
    
    # START_BLOCK_CREATE_PLOT: [Создание графика]
    df = pd.DataFrame(points, columns=["x", "y"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["x"], y=df["y"], mode='lines+markers', name='Parabola'))
    fig.update_layout(
        title="Parabola y = ax^2 + c",
        xaxis_title="x",
        yaxis_title="y",
        template="plotly_white"
    )
    logger.info(f"[UI][IMP:9][handle_draw][CREATE_PLOT][Success] График построен по {len(points)} точкам. [VALUE]")
    return fig
    # END_BLOCK_CREATE_PLOT
# END_FUNCTION_handle_draw
