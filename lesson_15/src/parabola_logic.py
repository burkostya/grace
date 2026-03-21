# FILE: lesson_15/src/parabola_logic.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Бизнес-логика расчета точек параболы y = ax^2 + c.
# SCOPE: Calculation, Data Generation.
# INPUT: Коэффициенты a, c и диапазон x_min, x_max.
# OUTPUT: pd.DataFrame с колонками x, y.
# KEYWORDS: [DOMAIN(8): Math; TECH(7): Pandas; CONCEPT(9): Calculation]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание модуля расчета параболы.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Функция генерации точек параболы] => generate_points
# END_MODULE_MAP

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

# START_FUNCTION_generate_points
# START_CONTRACT:
# PURPOSE: Расчет точек параболы y = ax^2 + c.
# INPUTS: 
# - float => a: Коэффициент a.
# - float => c: Коэффициент c.
# - float => x_min: Минимум x.
# - float => x_max: Максимум x.
# - int => num_points: Количество точек (по умолчанию 100).
# OUTPUTS: 
# - pd.DataFrame - Таблица с колонками x, y.
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def generate_points(a: float, c: float, x_min: float, x_max: float, num_points: int = 100) -> pd.DataFrame:
    """
    Функция выполняет расчет значений y для заданного диапазона x на основе формулы параболы.
    Использует numpy для векторизованных вычислений и возвращает результат в формате pandas DataFrame.
    """
    
    # START_BLOCK_CALC_LOGIC: [Расчет точек]
    try:
        logger.debug(f"[Calc][IMP:5][generate_points][Params] a={a}, c={c}, x_range=[{x_min}, {x_max}] [INFO]")
        
        # Генерация равномерно распределенных значений x
        x_values = np.linspace(x_min, x_max, num_points)
        
        # Расчет y = ax^2 + c
        y_values = a * (x_values ** 2) + c
        
        # Формирование DataFrame
        df = pd.DataFrame({
            "x": x_values,
            "y": y_values
        })
        
        logger.info(f"[BeliefState][IMP:9][generate_points][Result] Рассчитано {len(df)} точек. [VALUE]")
        return df
    except Exception as e:
        logger.error(f"[Calc][IMP:10][generate_points][Error] Ошибка расчета: {e} [FATAL]")
        return pd.DataFrame(columns=["x", "y"])
    # END_BLOCK_CALC_LOGIC
# END_FUNCTION_generate_points
