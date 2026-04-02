# FILE: lesson_22/calculator.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Математический расчет точек параболы y = ax^2 + c.
# SCOPE: Вычисление последовательности (x, y) для визуализации.
# INPUT: Коэффициенты a, c и диапазон x_min, x_max.
# OUTPUT: Список кортежей [(x, y), ...].
# KEYWORDS:[DOMAIN(8): Math; CONCEPT(7): Calculation; TECH(9): Parabola]
# LINKS: []
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется фиксированный шаг?
# A: Это обеспечивает предсказуемую плотность точек для визуализации в Plotly и таблицах.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля calculator.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Рассчитывает набор точек параболы y = ax^2 + c] => calculate_parabola
# END_MODULE_MAP

import logging

logger = logging.getLogger(__name__)


# START_FUNCTION_calculate_parabola
# START_CONTRACT:
# PURPOSE: Генерирует список точек (x, y) параболы.
# INPUTS:
# - float => a: Коэффициент при x^2.
# - float => c: Свободный член.
# - float => x_min: Начало диапазона x.
# - float => x_max: Конец диапазона x.
# - float => step: Шаг по оси x (по умолчанию 0.5).
# OUTPUTS:
# - list - Список кортежей [(x, y), ...].
# SIDE_EFFECTS: Отсутствуют (чистая функция).
# KEYWORDS:[PATTERN(6): MathFunction; CONCEPT(8): DataGeneration]
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def calculate_parabola(
    a: float, c: float, x_min: float, x_max: float, step: float = 0.5
) -> list:
    """
    Функция итерируется по диапазону [x_min, x_max] с заданным шагом и вычисляет
    соответствующие значения y для каждого x. Результат возвращается как список
    точек, готовый для сохранения в БД или отображения.
    """
    # START_BLOCK_GENERATE_POINTS: [Итерационный расчет]
    points = []
    current_x = x_min

    logger.debug(
        f"[Calc][IMP:5][calculate_parabola][GENERATE_POINTS][Params] a={a}, c={c}, x_min={x_min}, x_max={x_max}, step={step} [INFO]"
    )

    # Защита от бесконечного цикла, если x_max < x_min или step <= 0
    if x_max < x_min or step <= 0:
        logger.error(
            f"[LogicError][IMP:9][calculate_parabola][GENERATE_POINTS][InvalidRange] Некорректные параметры: x_min={x_min} > x_max={x_max} или step={step} <= 0 [FATAL]"
        )
        return []

    while current_x <= x_max:
        y = a * (current_x**2) + c
        points.append((round(current_x, 2), round(y, 2)))
        current_x += step

    # Добавление последней точки x_max, если она не попала в цикл из-за шага
    if not points or points[-1][0] < x_max:
        y_max = a * (x_max**2) + c
        points.append((round(x_max, 2), round(y_max, 2)))

    logger.info(
        f"[BeliefState][IMP:9][calculate_parabola][GENERATE_POINTS][Success] Рассчитано {len(points)} точек параболы. [SUCCESS]"
    )
    return points
    # END_BLOCK_GENERATE_POINTS


# END_FUNCTION_calculate_parabola
