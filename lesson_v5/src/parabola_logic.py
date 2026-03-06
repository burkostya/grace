# FILE:lesson_v5/src/parabola_logic.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Бизнес-логика расчета точек параболы y = ax^2 + c.
# SCOPE:Генерация набора точек (x, y) на основе параметров.
# INPUT:Параметры a, c, диапазон x, шаг.
# OUTPUT:Список кортежей (x, y).
# KEYWORDS:[DOMAIN(8): Math; CONCEPT(7): Parabola; TECH(9): Python]
# LINKS:[USES_API(8): math]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля бизнес-логики.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Генерирует точки параболы] => generate_parabola_points
# END_MODULE_MAP
#
# START_USE_CASES:
# - [generate_parabola_points]: User -> InputParameters -> ParabolaPointsGenerated
# END_USE_CASES

import logging

logger = logging.getLogger(__name__)

# START_FUNCTION_generate_parabola_points
# START_CONTRACT:
# PURPOSE:Рассчитывает значения y для заданного диапазона x.
# INPUTS: 
# - float => a: Коэффициент a
# - float => c: Коэффициент c
# - list => range_x: Список [min_x, max_x]
# - float => step: Шаг изменения x
# OUTPUTS: 
# - list -Список кортежей (x, y)
# SIDE_EFFECTS: Нет.
# KEYWORDS:[PATTERN(6): Generator; CONCEPT(8): Calculation]
# END_CONTRACT
def generate_parabola_points(a: float, c: float, range_x: list, step: float) -> list:
    """Генерирует точки параболы y = ax^2 + c."""
    
    # START_BLOCK_CALCULATE_POINTS: [Итерационный расчет точек]
    logger.debug(f"[Logic][IMP:5][generate_parabola_points][CALCULATE_POINTS][Start] Расчет для a={a}, c={c}, range={range_x}, step={step} [INFO]")
    
    points = []
    current_x = float(range_x[0])
    max_x = float(range_x[1])
    
    # AI Belief State: Мы ожидаем, что количество точек будет (max-min)/step + 1
    expected_count = int((max_x - current_x) / step) + 1
    logger.debug(f"[BeliefState][IMP:9][generate_parabola_points][CALCULATE_POINTS][Expectation] Ожидаемое количество точек: {expected_count} [VALUE]")

    try:
        while current_x <= max_x + (step / 10): # Небольшой допуск для точности float
            y = a * (current_x ** 2) + c
            points.append((current_x, y))
            current_x += step
            
        logger.info(f"[BeliefState][IMP:9][generate_parabola_points][CALCULATE_POINTS][Success] Сгенерировано {len(points)} точек. [VALUE]")
        return points
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][generate_parabola_points][CALCULATE_POINTS][Exception] Ошибка расчета: {e}. Local vars: current_x={current_x} [FATAL]")
        raise
    # END_BLOCK_CALCULATE_POINTS
# END_FUNCTION_generate_parabola_points
