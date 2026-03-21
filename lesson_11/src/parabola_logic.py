# FILE:lesson_11/src/parabola_logic.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Математические расчеты для построения параболы y = ax^2 + c.
# SCOPE:Вычисление координат точек параболы в заданном диапазоне.
# INPUT:Коэффициенты a, c, границы x_min, x_max и шаг step.
# OUTPUT:Список кортежей (x, y).
# KEYWORDS:[DOMAIN(Math): Parabola; CONCEPT(Calculation): PointGeneration; TECH(Python): Math]
# LINKS:[USES_API(Logging): logging]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется цикл while для генерации точек?
# A: Цикл while с ручным инкрементом позволяет точно контролировать шаг и границы, избегая проблем с range для float.
# Q: Зачем фиксировать Belief State в логах?
# A: Это позволяет верифицировать ожидаемое поведение алгоритма (количество итераций) до его фактического завершения.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичная реализация функции calculate_points с LDD 2.0 логированием.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC [10][Вычисляет точки параболы y = ax^2 + c] => calculate_points
# END_MODULE_MAP
#
# START_USE_CASES:
# - calculate_points: User -> InputParams -> ListOfPoints
# END_USE_CASES

import logging
import os

# START_BLOCK_LOGGING_SETUP: [Настройка логирования в файл lesson_11/app_11.log]
log_file = os.path.join("lesson_11", "app_11.log")
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logger = logging.getLogger("parabola_logic")
# END_BLOCK_LOGGING_SETUP

# START_FUNCTION_calculate_points
# START_CONTRACT:
# PURPOSE:Вычисляет координаты (x, y) для параболы y = ax^2 + c.
# INPUTS: 
# - Коэффициент при x^2 => a: float
# - Свободный коэффициент => c: float
# - Минимальное значение x => x_min: float
# - Максимальное значение x => x_max: float
# - Шаг изменения x => step: float
# OUTPUTS: 
# - list - Список кортежей (x, y)
# SIDE_EFFECTS: Запись логов в файл lesson_11/app_11.log.
# KEYWORDS:[PATTERN(Math): QuadraticFunction; CONCEPT(Logic): Iteration]
# COMPLEXITY_SCORE: 5[Линейная сложность относительно количества точек.]
# END_CONTRACT
def calculate_points(a: float, c: float, x_min: float, x_max: float, step: float = 0.1) -> list:
    """
    Функция производит расчет координат точек параболической функции y = ax^2 + c.
    Итерация проходит от x_min до x_max включительно с заданным шагом.
    В процессе работы выполняется LDD 2.0 логирование для отслеживания состояния
    и верификации математической логики.
    """
    
    # START_BLOCK_INITIALIZE: [Инициализация переменных и расчет ожиданий]
    points = []
    current_x = float(x_min)
    
    # AI Belief State: Ожидаемое количество точек
    expected_points_count = int((x_max - x_min) / step) + 1
    logger.info(f"[BeliefState][IMP:9][calculate_points][INITIALIZE][LogicCheck] Ожидаемое количество точек: {expected_points_count} [VALUE]")
    
    logger.debug(f"[Flow][IMP:4][calculate_points][INITIALIZE][Params] Входные параметры: a={a}, c={c}, range=[{x_min}, {x_max}], step={step} [INFO]")
    # END_BLOCK_INITIALIZE
    
    # START_BLOCK_CALCULATION_LOOP: [Цикл вычисления координат]
    # Используем небольшую дельту для компенсации погрешности float при сравнении с x_max
    epsilon = step / 1000
    
    while current_x <= x_max + epsilon:
        # Вычисление y = ax^2 + c
        current_y = a * (current_x ** 2) + c
        points.append((round(current_x, 4), round(current_y, 4)))
        
        # Логирование каждой 10-й точки на низком приоритете
        if len(points) % 10 == 0:
            logger.debug(f"[Trace][IMP:2][calculate_points][CALCULATION_LOOP][Iteration] Рассчитано точек: {len(points)}, текущий x: {current_x} [SUCCESS]")
            
        current_x += step
    # END_BLOCK_CALCULATION_LOOP
    
    # START_BLOCK_FINALIZE: [Проверка результата и возврат]
    actual_count = len(points)
    
    if actual_count == 0:
        logger.warning(f"[Boundary][IMP:8][calculate_points][FINALIZE][DataCheck] Список точек пуст. Проверьте диапазон и шаг. [WARN]")
    else:
        logger.info(f"[BusinessLogic][IMP:10][calculate_points][FINALIZE][GoalReached] Расчет завершен. Итого точек: {actual_count} [SUCCESS]")
        
    return points
    # END_BLOCK_FINALIZE
# END_FUNCTION_calculate_points
