# FILE:lesson_v3/src/parabola_logic.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Математический расчет точек параболы y = ax^2 + c.
# SCOPE:Генерация списка точек (x, y) на заданном диапазоне.
# INPUT:Коэффициенты a, c, диапазон x_min, x_max, количество точек.
# OUTPUT:Список кортежей (x, y).
# KEYWORDS:[DOMAIN(8):Math; CONCEPT(7):Parabola; TECH(9):Python_math]
# END_MODULE_CONTRACT

# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля расчета параболы.]
# END_CHANGE_SUMMARY

# START_MODULE_MAP:
# FUNC 10[Генерирует список точек параболы] => generate_parabola_points
# END_MODULE_MAP

import logging
import numpy as np

logger = logging.getLogger(__name__)

# START_FUNCTION_generate_parabola_points
# START_CONTRACT:
# PURPOSE:Расчет точек параболы.
# INPUTS: 
# - float =>a: Коэффициент a
# - float =>c: Коэффициент c
# - float =>x_min: Начало диапазона
# - float =>x_max: Конец диапазона
# - int =>num_points: Количество точек (по умолчанию 100)
# OUTPUTS: 
# - list -Список кортежей (x, y)
# SIDE_EFFECTS: Нет.
# END_CONTRACT
def generate_parabola_points(a: float, c: float, x_min: float, x_max: float, num_points: int = 100) -> list:
    """Генерирует точки параболы y = ax^2 + c."""
    # START_BLOCK_CALCULATE_POINTS: [Математический расчет]
    try:
        x_values = np.linspace(x_min, x_max, num_points)
        y_values = a * (x_values ** 2) + c
        
        points = [(float(x), float(y)) for x, y in zip(x_values, y_values)]
        
        logger.info(f"[BeliefState][IMP:9][generate_parabola_points][CALCULATE_POINTS][Success] Сгенерировано {len(points)} точек для a={a}, c={c}. [VALUE]")
        return points
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][generate_parabola_points][CALCULATE_POINTS][Exception] Ошибка расчета: {e} [FATAL]")
        return []
    # END_BLOCK_CALCULATE_POINTS
# END_FUNCTION_generate_parabola_points
