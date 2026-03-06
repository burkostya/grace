# FILE: lesson_v6/src/parabola_logic.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Математическая логика расчета точек параболы y = ax^2 + c.
# SCOPE: Генерация координат в заданном диапазоне с заданным шагом.
# INPUT: Параметры параболы (a, c), диапазон (x_min, x_max), шаг (step).
# OUTPUT: Список точек [{'x': float, 'y': float}, ...].
# KEYWORDS:[DOMAIN(8): MathCalculation; CONCEPT(7): QuadraticFunction; TECH(9): NumPy]
# END_MODULE_CONTRACT
#
# START_INVARIANTS:
# - Функция calculate_parabola_points ВСЕГДА возвращает отсортированный по x список точек.
# - Шаг по умолчанию равен 0.1.
# END_INVARIANTS
#
# START_RATIONALE:
# Q: Почему используется numpy.arange вместо range?
# A: numpy.arange поддерживает дробные шаги, что необходимо для плавного графика параболы.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля математической логики с LDD 2.0 логированием.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Рассчитывает точки параболы в заданном диапазоне] => calculate_parabola_points
# END_MODULE_MAP
#
# START_USE_CASES:
# -[calculate_parabola_points]: User (Generate) -> ComputePoints -> PointsCalculated
# END_USE_CASES

import logging
import numpy as np
from typing import List, Dict, Any

# Настройка логирования
logger = logging.getLogger(__name__)

# START_FUNCTION_calculate_parabola_points
# START_CONTRACT:
# PURPOSE: Расчет точек параболы y = ax^2 + c.
# INPUTS: 
# - [Коэффициент a] => a: float
# - [Коэффициент c] => c: float
# - [Минимальное значение x] => x_min: float
# - [Максимальное значение x] => x_max: float
# - [Шаг по x] => step: float (по умолчанию 0.1)
# OUTPUTS: 
# - List[Dict[str, float]] - Список точек [{'x': float, 'y': float}, ...]
# SIDE_EFFECTS: Отсутствуют.
# KEYWORDS:[PATTERN(6): Generator; CONCEPT(8): VectorizedComputation]
# END_CONTRACT
def calculate_parabola_points(a: float, c: float, x_min: float, x_max: float, step: float = 0.1) -> List[Dict[str, float]]:
    """Рассчитывает точки параболы y = ax^2 + c в заданном диапазоне."""
    
    # START_BLOCK_VALIDATE_INPUT: [Валидация входных параметров]
    if x_min >= x_max:
        logger.error(f"[ValidationError][IMP:7][calculate_parabola_points][VALIDATE_INPUT][ConditionCheck] x_min должен быть меньше x_max. Получено: x_min={x_min}, x_max={x_max}. [ERROR]")
        raise ValueError("x_min must be less than x_max")
    
    if step <= 0:
        logger.error(f"[ValidationError][IMP:7][calculate_parabola_points][VALIDATE_INPUT][ConditionCheck] Шаг должен быть положительным. Получено: step={step}. [ERROR]")
        raise ValueError("step must be positive")
    # END_BLOCK_VALIDATE_INPUT

    # START_BLOCK_CALCULATE_POINTS: [Векторизованный расчет точек с помощью NumPy]
    try:
        # Генерируем массив x значений
        x_values = np.arange(x_min, x_max + step, step)
        
        # Рассчитываем y значения по формуле y = ax^2 + c
        y_values = a * (x_values ** 2) + c
        
        # Формируем список точек
        points = [{'x': float(x), 'y': float(y)} for x, y in zip(x_values, y_values)]
        
        logger.info(f"[BeliefState][IMP:9][calculate_parabola_points][CALCULATE_POINTS][ReturnData] Рассчитано {len(points)} точек. Параметры: a={a}, c={c}, x_min={x_min}, x_max={x_max}, step={step} [VALUE]")
        return points
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][calculate_parabola_points][CALCULATE_POINTS][ExceptionEnrichment] Ошибка расчета точек. Local vars: a={a}, c={c}, x_min={x_min}, x_max={x_max}, step={step}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_CALCULATE_POINTS
# END_FUNCTION_calculate_parabola_points
