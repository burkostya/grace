# FILE:lesson_13/src/parabola_logic.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Реализация математической логики расчета параболы.
# SCOPE:Вычисление значений y по формуле y = ax^2 + c.
# INPUT:Коэффициенты a, c и диапазон x.
# OUTPUT:Список точек (x, y).
# KEYWORDS:DOMAIN(Mathematics); CONCEPT(Parabola); TECH(Python, math)
# LINKS:LINKS_TO_SPECIFICATION(GOAL_PARABOLA_LOGIC)
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется шаг 0.5?
# A: Для обеспечения достаточной плавности графика при умеренном количестве точек.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля математической логики.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC[10][Функция расчета точек параболы] => calculate_parabola
# END_MODULE_MAP
#
# START_USE_CASES:
# - [calculate_parabola]:User -> Input Params -> List of Points
# END_USE_CASES

import logging

logger = logging.getLogger(__name__)

# START_FUNCTION_calculate_parabola_points
# START_CONTRACT:
# PURPOSE:Расчет точек параболы y = ax^2 + bx + c.
# INPUTS: 
# - float =>a: Коэффициент A
# - float =>b: Коэффициент B
# - float =>c: Коэффициент C
# - float =>x_start: Начало диапазона
# - float =>x_end: Конец диапазона
# - int =>num_points: Количество точек
# OUTPUTS: 
# - list -Список кортежей (x, y)
# SIDE_EFFECTS: Нет
# KEYWORDS:PATTERN(Algorithm); CONCEPT(Math)
# COMPLEXITY_SCORE:4
# END_CONTRACT
def calculate_parabola_points(a: float, b: float, c: float, x_start: float, x_end: float, num_points: int) -> list:
    """
    Вычисляет координаты (x, y) для параболы y = ax^2 + bx + c.
    Использует равномерное распределение точек в заданном диапазоне.
    """
    # START_BLOCK_VALIDATION: [Проверка входных данных]
    if x_start >= x_end:
        logger.error(f"[Math][IMP:10][calculate_parabola_points][VALIDATION][Error] x_start ({x_start}) >= x_end ({x_end}) [FATAL]")
        return []
    if num_points < 2:
        logger.error(f"[Math][IMP:10][calculate_parabola_points][VALIDATION][Error] num_points ({num_points}) < 2 [FATAL]")
        return []
    
    logger.debug(f"[Math][IMP:4][calculate_parabola_points][VALIDATION][Params] a={a}, b={b}, c={c}, range=[{x_start}, {x_end}], points={num_points} [INFO]")
    # END_BLOCK_VALIDATION

    # START_BLOCK_CALCULATION: [Цикл вычисления точек]
    points = []
    step = (x_end - x_start) / (num_points - 1)
    
    for i in range(num_points):
        x = x_start + i * step
        # Формула: y = a * x^2 + b * x + c
        y = a * (x ** 2) + b * x + c
        points.append((round(x, 4), round(y, 4)))
    # END_BLOCK_CALCULATION

    # START_BLOCK_RESULT: [Логирование результата]
    logger.info(f"[BeliefState][IMP:9][calculate_parabola_points][RESULT][Value] Вычислено {len(points)} точек. [SUCCESS]")
    return points
    # END_BLOCK_RESULT
# END_FUNCTION_calculate_parabola_points
