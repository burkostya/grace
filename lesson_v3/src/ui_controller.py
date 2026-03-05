# FILE:lesson_v3/src/ui_controller.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Контроллер для Gradio интерфейса Lesson_v3.
# SCOPE:Обработка нажатий кнопок, обновление графиков и таблиц.
# INPUT:Параметры из UI (a, c, x_min, x_max).
# OUTPUT:DataFrame для таблицы, Plotly Figure для графика.
# KEYWORDS:[DOMAIN(8):UI; CONCEPT(7):Gradio_Controller; TECH(9):Python_plotly]
# LINKS:[USES_API(9):config_manager, database_manager, parabola_logic]
# END_MODULE_CONTRACT

# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание контроллера UI.]
# END_CHANGE_SUMMARY

# START_MODULE_MAP:
# FUNC 10[Обработчик кнопки Generate Data] => on_generate_click
# FUNC 10[Обработчик кнопки Draw Graph] => on_draw_click
# END_MODULE_MAP

import os
import logging
import pandas as pd
import plotly.graph_objects as go
from lesson_v3.src.config_manager import save_config
from lesson_v3.src.database_manager import init_db, save_points, load_points
from lesson_v3.src.parabola_logic import generate_parabola_points

logger = logging.getLogger(__name__)

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "parabola.db")

# START_FUNCTION_on_generate_click
# START_CONTRACT:
# PURPOSE:Сохранение конфига и генерация точек в БД.
# INPUTS: 
# - float =>a: Коэффициент a
# - float =>c: Коэффициент c
# - float =>x_min: Начало диапазона
# - float =>x_max: Конец диапазона
# OUTPUTS: 
# - str -Статусное сообщение
# SIDE_EFFECTS: Обновляет config.json и parabola.db.
# END_CONTRACT
def on_generate_click(a: float, c: float, x_min: float, x_max: float) -> str:
    """Обработчик кнопки генерации данных."""
    # START_BLOCK_GENERATE_UI_FLOW: [Поток генерации из UI]
    try:
        # 1. Сохраняем конфиг
        config_data = {"a": a, "c": c, "x_min": x_min, "x_max": x_max}
        save_config(CONFIG_PATH, config_data)
        
        # 2. Генерируем точки
        points = generate_parabola_points(a, c, x_min, x_max)
        
        # 3. Сохраняем в БД
        init_db(DB_PATH)
        success = save_points(DB_PATH, points)
        
        if success:
            msg = f"Successfully generated {len(points)} points."
            logger.info(f"[BeliefState][IMP:9][on_generate_click][GENERATE_UI_FLOW][Success] {msg} [VALUE]")
            return msg
        else:
            return "Error saving points to database."
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][on_generate_click][GENERATE_UI_FLOW][Exception] Ошибка: {e} [FATAL]")
        return f"Error: {e}"
    # END_BLOCK_GENERATE_UI_FLOW
# END_FUNCTION_on_generate_click

# START_FUNCTION_on_draw_click
# START_CONTRACT:
# PURPOSE:Загрузка данных из БД и построение графика.
# INPUTS: Нет
# OUTPUTS: 
# - pd.DataFrame -Таблица точек
# - go.Figure -График Plotly
# SIDE_EFFECTS: Нет.
# END_CONTRACT
def on_draw_click():
    """Обработчик кнопки отрисовки графика."""
    # START_BLOCK_DRAW_UI_FLOW: [Поток отрисовки из UI]
    try:
        df = load_points(DB_PATH)
        
        if df.empty:
            logger.warning(f"[UI][IMP:7][on_draw_click][DRAW_UI_FLOW][EmptyDB] БД пуста. [WARN]")
            return df, go.Figure()
            
        # Создаем график
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['x'], y=df['y'], mode='lines+markers', name='Parabola'))
        fig.update_layout(title="Parabola y = ax^2 + c", xaxis_title="x", yaxis_title="y")
        
        logger.info(f"[BeliefState][IMP:9][on_draw_click][DRAW_UI_FLOW][Success] График построен. [VALUE]")
        return df, fig
    except Exception as e:
        logger.error(f"[UI][IMP:10][on_draw_click][DRAW_UI_FLOW][Error] Ошибка отрисовки: {e} [FATAL]")
        return pd.DataFrame(columns=["x", "y"]), go.Figure()
    # END_BLOCK_DRAW_UI_FLOW
# END_FUNCTION_on_draw_click
