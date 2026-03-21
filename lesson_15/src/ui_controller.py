# FILE: lesson_15/src/ui_controller.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Контроллеры для Gradio UI (обработка кликов и обновление данных).
# SCOPE: UI Logic, Event Handling.
# INPUT: Параметры из UI компонентов.
# OUTPUT: Обновленные компоненты (DataFrame, Plotly Figure).
# KEYWORDS: [DOMAIN(8): UI; TECH(7): Gradio, Plotly; CONCEPT(9): Controller]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание контроллеров UI.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Обработчик генерации данных] => on_generate
# FUNC 10[Обработчик отрисовки графика] => on_draw
# END_MODULE_MAP

import plotly.graph_objects as go
import pandas as pd
import logging
import os

from lesson_15.src.config_manager import ConfigManager
from lesson_15.src.database_manager import DatabaseManager
from lesson_15.src.parabola_logic import generate_points

logger = logging.getLogger(__name__)

# START_FUNCTION_on_generate
# START_CONTRACT:
# PURPOSE: Сохранение конфига, генерация точек и обновление таблицы.
# INPUTS: 
# - float => a, c, x_min, x_max: Параметры из UI.
# - ConfigManager => config_mgr: Менеджер конфига.
# - DatabaseManager => db_mgr: Менеджер БД.
# OUTPUTS: 
# - pd.DataFrame - Данные для таблицы.
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def on_generate(a, c, x_min, x_max, config_mgr, db_mgr):
    """
    Обработчик кнопки 'Generate Data'. Сохраняет параметры в config.json,
    рассчитывает точки и сохраняет их в БД. Возвращает DataFrame для отображения.
    """
    # START_BLOCK_GENERATE_LOGIC: [Генерация и сохранение]
    try:
        # 1. Сохранение конфига
        new_config = {"a": a, "c": c, "x_min": x_min, "x_max": x_max}
        config_mgr.save(new_config)
        logger.info(f"[UI][IMP:7][on_generate][Config] Параметры сохранены: {new_config} [INFO]")
        
        # 2. Генерация точек
        df = generate_points(a, c, x_min, x_max)
        
        # 3. Сохранение в БД
        db_mgr.save_points(df)
        
        logger.info(f"[BeliefState][IMP:9][on_generate][Result] Данные сгенерированы и сохранены. [VALUE]")
        return df
    except Exception as e:
        logger.error(f"[UI][IMP:10][on_generate][Error] Ошибка генерации: {e} [FATAL]")
        return pd.DataFrame(columns=["x", "y"])
    # END_BLOCK_GENERATE_LOGIC

# START_FUNCTION_on_draw
# START_CONTRACT:
# PURPOSE: Чтение данных из БД и построение графика Plotly.
# INPUTS: 
# - DatabaseManager => db_mgr: Менеджер БД.
# OUTPUTS: 
# - go.Figure - Объект графика Plotly.
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def on_draw(db_mgr):
    """
    Обработчик кнопки 'Draw Graph'. Считывает данные из БД и строит интерактивный график.
    """
    # START_BLOCK_DRAW_LOGIC: [Построение графика]
    try:
        df = db_mgr.get_points()
        
        if df.empty:
            logger.warning(f"[UI][IMP:8][on_draw][Warning] Нет данных для графика. [WARN]")
            fig = go.Figure()
            fig.update_layout(title="Нет данных для отображения")
            return fig
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["x"], y=df["y"], mode='lines+markers', name='Parabola'))
        fig.update_layout(
            title=f"Parabola y = ax^2 + c",
            xaxis_title="X",
            yaxis_title="Y",
            template="plotly_white"
        )
        
        logger.info(f"[BeliefState][IMP:9][on_draw][Result] График успешно построен. [VALUE]")
        return fig
    except Exception as e:
        logger.error(f"[UI][IMP:10][on_draw][Error] Ошибка отрисовки: {e} [FATAL]")
        return go.Figure()
    # END_BLOCK_DRAW_LOGIC
# END_FUNCTION_on_draw
