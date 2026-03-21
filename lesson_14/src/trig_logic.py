# FILE:lesson_14/src/trig_logic.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Реализация математической логики расчета тригонометрических функций.
# SCOPE:Вычисление значений y по формулам sin(x), cos(x), tan(x).
# INPUT:Тип функции, диапазон x, количество точек.
# OUTPUT:Список точек (x, y).
# KEYWORDS:DOMAIN(Mathematics); CONCEPT(Trigonometry); TECH(Python, math)
# LINKS:LINKS_TO_SPECIFICATION(GOAL_TRIG_LOGIC)
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используются радианы, а не градусы?
# A: В Python math.sin/cos/tan принимают радианы, что является стандартом в математике и физике.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля тригонометрической логики.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC[10][Функция расчета точек тригонометрических функций] => calculate_trig_points
# END_MODULE_MAP
#
# START_USE_CASES:
# - [calculate_trig_points]:User -> Input Params -> List of Points
# END_USE_CASES

import logging
import math

logger = logging.getLogger(__name__)

# START_BLOCK_FUNCTION_MAP: [Карта функций для выбора]
FUNCTION_MAP = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan
}
# END_BLOCK_FUNCTION_MAP

# START_FUNCTION_calculate_trig_points
# START_CONTRACT:
# PURPOSE:Расчет точек тригонометрических функций sin(x), cos(x), tan(x).
# INPUTS: 
# - str =>func_type: Тип функции (sin/cos/tan)
# - float =>x_start: Начало диапазона
# - float =>x_end: Конец диапазона
# - int =>num_points: Количество точек
# OUTPUTS: 
# - list -Список кортежей (x, y)
# SIDE_EFFECTS: Нет
# KEYWORDS:PATTERN(Algorithm); CONCEPT(Math)
# COMPLEXITY_SCORE:4
# END_CONTRACT
def calculate_trig_points(func_type: str, x_start: float, x_end: float, num_points: int) -> list:
    """
    Вычисляет координаты (x, y) для заданной тригонометрической функции.
    Поддерживает функции sin, cos, tan.
    """
    # START_BLOCK_VALIDATE_INPUT: [Проверка входных данных]
    if func_type not in FUNCTION_MAP:
        logger.error(f"[Math][IMP:10][calculate_trig_points][VALIDATION][Error] Неизвестный тип функции: {func_type} [FATAL]")
        return []
    
    if x_start >= x_end:
        logger.error(f"[Math][IMP:10][calculate_trig_points][VALIDATION][Error] x_start ({x_start}) >= x_end ({x_end}) [FATAL]")
        return []
    
    if num_points < 2:
        logger.error(f"[Math][IMP:10][calculate_trig_points][VALIDATION][Error] num_points ({num_points}) < 2 [FATAL]")
        return []
    
    logger.debug(f"[Math][IMP:4][calculate_trig_points][VALIDATION][Params] func_type={func_type}, range=[{x_start}, {x_end}], points={num_points} [INFO]")
    # END_BLOCK_VALIDATE_INPUT

    # START_BLOCK_CALCULATION: [Цикл вычисления точек]
    func = FUNCTION_MAP[func_type]
    points = []
    step = (x_end - x_start) / (num_points - 1)
    
    for i in range(num_points):
        x = x_start + i * step
        y = func(x)
        points.append((round(x, 4), round(y, 4)))
    
    logger.info(f"[BeliefState][IMP:9][calculate_trig_points][RESULT][Value] Вычислено {len(points)} точек для {func_type}(x) [SUCCESS]")
    return points
    # END_BLOCK_CALCULATION

# END_FUNCTION_calculate_trig_points
