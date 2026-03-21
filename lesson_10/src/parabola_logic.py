# FILE:lesson_10/src/parabola_logic.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Математический расчет точек параболы y = ax^2 + c.
# SCOPE:Вычисление списка координат (x, y) в заданном диапазоне.
# INPUT:Коэффициенты a, c, диапазон x_min, x_max.
# OUTPUT:Список кортежей (x, y).
# KEYWORDS:[DOMAIN(Math): Parabola; CONCEPT(Calculation): Geometry; TECH(Python): numpy]
# LINKS:[USES_API(9): numpy]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется numpy для генерации диапазона x?
# A: Это обеспечивает высокую точность и производительность при генерации большого количества точек.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля математической логики.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Вычисляет список точек параболы] => calculate_parabola_points
# END_MODULE_MAP
#
# START_USE_CASES:
# - [calculate_parabola_points]: Logic -> ComputePoints -> PointsListReturned
# END_USE_CASES

import numpy as np
import logging

logger = logging.getLogger(__name__)

# START_FUNCTION_calculate_parabola_points
# START_CONTRACT:
# PURPOSE:Генерирует список точек (x, y) для функции y = ax^2 + c.
# INPUTS: 
# - Коэффициент a => a: float
# - Коэффициент c => c: float
# - Минимум x => x_min: float
# - Максимум x => x_max: float
# - Количество точек => num_points: int
# OUTPUTS: 
# - list[tuple[float, float]] - Список вычисленных координат
# SIDE_EFFECTS: Нет.
# KEYWORDS:[PATTERN(Algorithm): Math]
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def calculate_parabola_points(a: float, c: float, x_min: float, x_max: float, num_points: int = 100) -> list:
    """
    Выполняет расчет координат параболы. Использует numpy.linspace для 
    равномерного распределения точек по оси X и векторизованные операции 
    для вычисления Y. Результат преобразуется в список кортежей для 
    совместимости с SQLite executemany.
    """
    # START_BLOCK_COMPUTE_POINTS: [Математический расчет]
    try:
        logger.debug(f"[Logic][IMP:4][calculate_parabola_points][COMPUTE_POINTS][Params] a={a}, c={c}, x_min={x_min}, x_max={x_max} [INFO]")
        
        # Генерация массива X
        x_values = np.linspace(x_min, x_max, num_points)
        
        # Вычисление массива Y: y = ax^2 + c
        y_values = a * (x_values ** 2) + c
        
        # Формирование списка кортежей
        points = list(zip(x_values.tolist(), y_values.tolist()))
        
        logger.info(f"[BeliefState][IMP:9][calculate_parabola_points][COMPUTE_POINTS][Success] Рассчитано {len(points)} точек. [SUCCESS]")
        return points
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][calculate_parabola_points][COMPUTE_POINTS][Exception] Ошибка расчета: {e} [FATAL]")
        return []
    # END_BLOCK_COMPUTE_POINTS
# END_FUNCTION_calculate_parabola_points
