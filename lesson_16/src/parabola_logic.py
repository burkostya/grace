# FILE:lesson_16/src/parabola_logic.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Математическая логика расчета точек параболы y = ax^2 + c.
# SCOPE:Генерация набора точек (x, y) для заданного диапазона.
# INPUT:Параметры a, c, x_min, x_max.
# OUTPUT:DataFrame с колонками x и y.
# KEYWORDS:[DOMAIN(8): Math; TECH(9): Pandas, Numpy]
# LINKS:[USES_API(8): pandas, numpy]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля расчета параболы.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Генерирует DataFrame с точками параболы] => calculate_parabola
# END_MODULE_MAP

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

# START_FUNCTION_calculate_parabola
# START_CONTRACT:
# PURPOSE:Расчет точек параболы y = ax^2 + c.
# INPUTS:
# - float => a: Коэффициент при x^2.
# - float => c: Свободный член.
# - float => x_min: Начало диапазона x.
# - float => x_max: Конец диапазона x.
# - int => points_count: Количество точек для генерации.
# OUTPUTS:
# - pd.DataFrame - DataFrame с колонками x и y.
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def calculate_parabola(a: float, c: float, x_min: float, x_max: float, points_count: int = 100) -> pd.DataFrame:
    """
    Генерирует равномерно распределенные значения x в диапазоне [x_min, x_max]
    и вычисляет соответствующие значения y по формуле y = ax^2 + c.
    Результат возвращается в виде pandas DataFrame для удобства последующей
    обработки и визуализации.
    """
    # START_BLOCK_GENERATE_POINTS: [Расчет значений x и y]
    try:
        x_values = np.linspace(x_min, x_max, points_count)
        y_values = a * (x_values ** 2) + c
        
        df = pd.DataFrame({
            'x': x_values,
            'y': y_values
        })
        
        logger.info(f"[Logic][IMP:9][calculate_parabola][GENERATE_POINTS][Success] Сгенерировано {points_count} точек для a={a}, c={c}. [OK]")
        return df
    except Exception as e:
        logger.critical(f"[Logic][IMP:10][calculate_parabola][GENERATE_POINTS][Error] Ошибка при расчете параболы: {e}. [FATAL]")
        return pd.DataFrame(columns=['x', 'y'])
    # END_BLOCK_GENERATE_POINTS
# END_FUNCTION_calculate_parabola
