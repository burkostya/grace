# FILE:lesson_20/logic.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Бизнес-логика расчета точек параболы y = ax^2 + c.
# SCOPE:Генерация списка точек (x, y) на заданном интервале.
# INPUT:Параметры a, c, x_min, x_max.
# OUTPUT:Список кортежей (x, y).
# KEYWORDS:[DOMAIN(8): Mathematics; CONCEPT(7): Parabola; TECH(9): Python]
# LINKS:[USES_API(8): math]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется 100 точек?
# A: Этого достаточно для плавного отображения графика в Plotly.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание модуля бизнес-логики.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Рассчитывает точки параболы] => calculate_parabola
# END_MODULE_MAP

import logging

logger = logging.getLogger("lesson_20")

# START_FUNCTION_calculate_parabola
# START_CONTRACT:
# PURPOSE:Генерация 100 точек параболы y = ax^2 + c.
# INPUTS:
# - float => a: Коэффициент a
# - float => c: Коэффициент c
# - float => x_min: Минимум x
# - float => x_max: Максимум x
# OUTPUTS:
# - list - Список кортежей (x, y)
# KEYWORDS:[PATTERN(6): Generator]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def calculate_parabola(a: float, c: float, x_min: float, x_max: float) -> list:
    """
    Рассчитывает 100 точек параболы y = ax^2 + c на интервале [x_min, x_max].
    """
    # START_BLOCK_GENERATE_POINTS: [Генерация точек]
    points = []
    num_points = 100
    
    if x_min >= x_max:
        logger.error(f"[Logic][IMP:10][calculate_parabola][GENERATE_POINTS][Error] x_min >= x_max: {x_min} >= {x_max}. [FATAL]")
        return []
        
    step = (x_max - x_min) / (num_points - 1)
    
    for i in range(num_points):
        x = x_min + i * step
        y = a * (x ** 2) + c
        points.append((x, y))
        
    logger.info(f"[Logic][IMP:9][calculate_parabola][GENERATE_POINTS][Success] Сгенерировано {len(points)} точек. [VALUE]")
    return points
    # END_BLOCK_GENERATE_POINTS
# END_FUNCTION_calculate_parabola
