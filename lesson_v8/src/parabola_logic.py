# FILE: lesson_v8/src/parabola_logic.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Математический расчет точек параболы по формуле y = ax^2 + c.
# SCOPE: Генерация точек параболы на основе коэффициентов a и c и диапазона x.
# INPUT: Коэффициенты a и c, диапазон x_min и x_max, количество точек.
# OUTPUT: DataFrame pandas с колонками x и y.
# KEYWORDS:[DOMAIN(9): MathematicalComputation; CONCEPT(8): QuadraticFunction; TECH(9): NumPy]
# LINKS:[USES_API(9): numpy, pandas]
# END_MODULE_CONTRACT
#
# START_INVARIANTS:
# - Функция generate_parabola_points ВСЕГДА возвращает pandas DataFrame.
# - DataFrame ВСЕГДА содержит ровно num_points строк (если num_points > 0).
# - Значения y рассчитываются строго по формуле y = a*x^2 + c.
# END_INVARIANTS
#
# START_RATIONALE:
# Q: Почему используется numpy для генерации точек?
# A: NumPy обеспечивает векторизованные операции, которые значительно быстрее и эффективнее циклов Python.
# Q: Почему num_points имеет дефолтное значение 100?
# A: 100 точек обеспечивают достаточное разрешение для визуализации параболы при разумной производительности.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля математических вычислений параболы.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Генерирует точки параболы y = ax^2 + c] => generate_parabola_points
# END_MODULE_MAP
#
# START_USE_CASES:
# -[generate_parabola_points]: Application (DataGeneration) -> CalculateParabolaPoints -> PointsDataFrameGenerated
# END_USE_CASES

import logging
import numpy as np
import pandas as pd
from typing import Optional

logger = logging.getLogger(__name__)


# START_FUNCTION_generate_parabola_points
# START_CONTRACT:
# PURPOSE: Генерирует DataFrame с точками параболы y = ax^2 + c в заданном диапазоне x.
# INPUTS: 
# - a => a: float (коэффициент при x^2)
# - c => c: float (свободный член)
# - x_min => x_min: float (минимальное значение x)
# - x_max => x_max: float (максимальное значение x)
# - num_points => num_points: int (количество точек, опционально, дефолт 100)
# OUTPUTS: 
# - pd.DataFrame - DataFrame с колонками 'x' и 'y', содержащий точки параболы
# SIDE_EFFECTS: Отсутствуют (чистая функция без побочных эффектов).
# KEYWORDS:[PATTERN(9): Vectorization; CONCEPT(8): QuadraticEquation]
# COMPLEXITY_SCORE: 3[Низкая сложность: векторизованные операции NumPy.]
# END_CONTRACT
def generate_parabola_points(
    a: float, 
    c: float, 
    x_min: float, 
    x_max: float, 
    num_points: int = 100
) -> pd.DataFrame:
    """
    Функция выполняет генерацию точек параболы по формуле y = ax^2 + c.
    Использует векторизованные операции NumPy для эффективного вычисления значений.
    Генерирует равномерно распределенные точки в заданном диапазоне x_min..x_max.
    Результат возвращается в виде pandas DataFrame для удобства последующей обработки и визуализации.
    """
    
    # START_BLOCK_VALIDATE_INPUTS: [Проверка входных параметров]
    if num_points <= 0:
        logger.error(f"[InvalidInput][IMP:9][generate_parabola_points][VALIDATE_INPUTS][ValueError] num_points должен быть положительным. Получен: {num_points} [ERROR]")
        raise ValueError(f"num_points должен быть положительным, получено: {num_points}")
    
    if x_min >= x_max:
        logger.error(f"[InvalidInput][IMP:9][generate_parabola_points][VALIDATE_INPUTS][ValueError] x_min должен быть меньше x_max. Получены: x_min={x_min}, x_max={x_max} [ERROR]")
        raise ValueError(f"x_min должен быть меньше x_max, получены: x_min={x_min}, x_max={x_max}")
    
    logger.debug(f"[ParamsValidated][IMP:4][generate_parabola_points][VALIDATE_INPUTS][ParamCheck] Параметры валидны: a={a}, c={c}, x_min={x_min}, x_max={x_max}, num_points={num_points} [INFO]")
    # END_BLOCK_VALIDATE_INPUTS
    
    # START_BLOCK_GENERATE_POINTS: [Генерация точек параболы]
    try:
        # Генерация равномерно распределенных значений x
        x_values = np.linspace(x_min, x_max, num_points)
        
        # Вычисление значений y по формуле y = ax^2 + c
        y_values = a * (x_values ** 2) + c
        
        # Создание DataFrame
        df = pd.DataFrame({
            'x': x_values,
            'y': y_values
        })
        
        logger.info(f"[PointsGenerated][IMP:9][generate_parabola_points][GENERATE_POINTS][Calculation] Сгенерировано {len(df)} точек параболы. AI Belief: Парабола с вершиной в (0, {c}), {'выпуклая вверх' if a > 0 else 'выпуклая вниз' if a < 0 else 'прямая линия'}. [VALUE]")
        
        return df
        
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][generate_parabola_points][GENERATE_POINTS][ExceptionEnrichment] Ошибка при генерации точек. Local vars: a={a}, c={c}, x_min={x_min}, x_max={x_max}, num_points={num_points}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_GENERATE_POINTS
# END_FUNCTION_generate_parabola_points
