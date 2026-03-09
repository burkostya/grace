# FILE:lesson_9/src/parabola_logic.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Математическое ядро для расчета координат параболы.
# SCOPE: Вычисление y = ax^2 + c для заданного диапазона x.
# INPUT:Параметры a, c, x_min, x_max, step.
# OUTPUT: Список кортежей (x, y).
# KEYWORDS:[DOMAIN(9): Mathematics; CONCEPT(8): Parabola; TECH(7): Python]
# LINKS:[]
# LINKS_TO_SPECIFICATION:[business_requirements.md:23-33]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля математической логики.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC [10][Рассчитывает список точек параболы] => calculate_parabola_points
# END_MODULE_MAP
#
# START_USE_CASES:
# - [calculate_parabola_points]: System -> Math Calculation -> PointsGenerated
# END_USE_CASES

import logging

# Настройка логгера для LDD 2.0
logger = logging.getLogger("lesson_9")

# START_FUNCTION_calculate_parabola_points
# START_CONTRACT:
# PURPOSE:Генерация набора точек (x, y) на основе квадратичной функции.
# INPUTS: 
# - float => a: Коэффициент при x^2.
# - float => c: Свободный член.
# - float => x_min: Начало диапазона.
# - float => x_max: Конец диапазона.
# - float => step: Шаг изменения x (по умолчанию 0.1).
# OUTPUTS: 
# - list[tuple[float, float]] - Список рассчитанных точек.
# SIDE_EFFECTS: Нет.
# KEYWORDS:[PATTERN(8): Algorithm; CONCEPT(9): QuadraticFunction]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def calculate_parabola_points(a: float, c: float, x_min: float, x_max: float, step: float = 0.1) -> list:
    """
    Функция итерируется от x_min до x_max с заданным шагом, вычисляя 
    значение y по формуле y = a * x^2 + c. Результаты округляются 
    до 4 знаков после запятой для предотвращения ошибок точности 
    плавающей точки при отображении.
    """
    # START_BLOCK_VALIDATE_INPUTS: [Проверка входных параметров]
    if x_min >= x_max:
        logger.error(f"[Logic][IMP:10][calculate_parabola_points][VALIDATE][Error] x_min ({x_min}) >= x_max ({x_max}) [FATAL]")
        return []
    
    if step <= 0:
        logger.error(f"[Logic][IMP:10][calculate_parabola_points][VALIDATE][Error] Шаг должен быть положительным: {step} [FATAL]")
        return []
        
    logger.debug(f"[Logic][IMP:4][calculate_parabola_points][VALIDATE][Params] a={a}, c={c}, range=[{x_min}, {x_max}], step={step} [INFO]")
    # END_BLOCK_VALIDATE_INPUTS

    # START_BLOCK_CALCULATION_LOOP: [Цикл генерации точек]
    points = []
    current_x = x_min
    
    # Используем небольшую дельту для корректного включения x_max
    epsilon = step / 100.0
    
    while current_x <= x_max + epsilon:
        # Формула: y = ax^2 + c
        y = a * (current_x ** 2) + c
        
        # Округление для чистоты данных
        points.append((round(current_x, 4), round(y, 4)))
        
        current_x += step
    # END_BLOCK_CALCULATION_LOOP

    # START_BLOCK_RETURN_RESULTS: [Логирование итога и возврат]
    logger.info(f"[Logic][IMP:9][calculate_parabola_points][RETURN][Success] Сгенерировано {len(points)} точек. [VALUE]")
    return points
    # END_BLOCK_RETURN_RESULTS
# END_FUNCTION_calculate_parabola_points
