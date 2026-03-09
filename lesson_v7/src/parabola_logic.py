# FILE: lesson_v7/src/parabola_logic.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Реализация математической логики генерации точек параболы.
# SCOPE: Расчет координат y = ax^2 + c для заданного диапазона x.
# INPUT: Параметры параболы (a, c, x_min, x_max).
# OUTPUT: Список точек [(x, y), ...] или DataFrame.
# KEYWORDS:[DOMAIN(9): MathLogic; CONCEPT(8): Vectorization; TECH(9): NumPy]
# LINKS:[READS_DATA_FROM(8): config_manager; WRITES_DATA_TO(8): database_manager]
# END_MODULE_CONTRACT
#
# START_INVARIANTS:
# - Функция generate_points ВСЕГДА возвращает список кортежей (x, y), даже если x_min >= x_max (возвращает пустой список).
# - Расчет выполняется с использованием векторизованных операций NumPy для производительности.
# END_INVARIANTS
#
# START_RATIONALE:
# Q: Почему используется NumPy вместо чистого Python?
# A: NumPy обеспечивает векторизацию, что значительно ускоряет вычисления для больших диапазонов и является стандартом в ML/Data Science.
# Q: Почему возвращается список кортежей, а не словарь?
# A: Список кортежей легче сериализовать в SQL и использовать для построения графиков.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля математической логики параболы.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Генерирует точки параболы y = ax^2 + c для заданного диапазона] => generate_points
# END_MODULE_MAP
#
# START_USE_CASES:
# -[generate_points]: Application (GenerateCommand) -> CalculateParabola -> PointsGenerated
# END_USE_CASES

import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)

# START_FUNCTION_generate_points
# START_CONTRACT:
# PURPOSE: Генерация точек параболы по формуле y = ax^2 + c.
# INPUTS: 
# - Коэффициент при x^2 => a: float
# - Свободный член => c: float
# - Минимальное значение x => x_min: float
# - Максимальное значение x => x_max: float
# - Количество точек (опционально) => num_points: int (по умолчанию 100)
# OUTPUTS: 
# - List[Tuple[float, float]] - Список точек [(x, y), ...]
# SIDE_EFFECTS: Отсутствуют.
# KEYWORDS:[PATTERN(7): Vectorization; CONCEPT(9): MathematicalFunction]
# END_CONTRACT
def generate_points(a: float, c: float, x_min: float, x_max: float, num_points: int = 100) -> List[Tuple[float, float]]:
    """Генерирует точки параболы y = ax^2 + c для заданного диапазона x."""
    
    # START_BLOCK_VALIDATE_INPUTS: [Валидация входных параметров]
    logger.debug(f"[MathCalc][IMP:4][generate_points][VALIDATE_INPUTS][Params] Начало генерации. a={a}, c={c}, x_range=({x_min}, {x_max}), num_points={num_points} [INFO]")
    
    if num_points <= 0:
        logger.error(f"[MathCalc][IMP:10][generate_points][VALIDATE_INPUTS][ValidationError] Количество точек должно быть положительным. Local vars: num_points={num_points} [FATAL]")
        raise ValueError("Количество точек должно быть положительным числом.")
    
    if x_min >= x_max:
        logger.warning(f"[MathCalc][IMP:8][generate_points][VALIDATE_INPUTS][RangeCheck] x_min >= x_max. Возврат пустого списка. Local vars: x_min={x_min}, x_max={x_max} [WARN]")
        return []
    # END_BLOCK_VALIDATE_INPUTS
    
    # START_BLOCK_CALCULATE_POINTS: [Векторизованный расчет точек]
    try:
        import numpy as np
        
        # Генерация равномерно распределенных значений x
        x_values = np.linspace(x_min, x_max, num_points)
        
        # Расчет значений y по формуле y = ax^2 + c
        y_values = a * (x_values ** 2) + c
        
        # Формирование списка кортежей
        points = list(zip(x_values, y_values))
        
        logger.info(f"[BeliefState][IMP:9][generate_points][CALCULATE_POINTS][CalculationComplete] Сгенерировано {len(points)} точек. Парабола: y={a}*x^2+{c}. Вершина в (0, {c}). [VALUE]")
        return points
        
    except ImportError:
        # Fallback на чистый Python, если NumPy недоступен
        logger.warning(f"[MathCalc][IMP:7][generate_points][CALCULATE_POINTS][LibraryFallback] NumPy недоступен. Использование чистого Python. [WARN]")
        
        step = (x_max - x_min) / (num_points - 1)
        points = []
        
        for i in range(num_points):
            x = x_min + i * step
            y = a * (x ** 2) + c
            points.append((x, y))
        
        logger.info(f"[BeliefState][IMP:9][generate_points][CALCULATE_POINTS][CalculationComplete] Сгенерировано {len(points)} точек (чистый Python). [VALUE]")
        return points
        
    except Exception as e:
        logger.critical(f"[MathCalc][IMP:10][generate_points][CALCULATE_POINTS][ExceptionEnrichment] Ошибка при расчете. Local vars: a={a}, c={c}, x_min={x_min}, x_max={x_max}, num_points={num_points}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_CALCULATE_POINTS
# END_FUNCTION_generate_points
