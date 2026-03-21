# FILE:lesson_17/src/trig_logic.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Реализация математической логики расчета тригонометрической функции y = A * sin(B * x + C) + D.
# SCOPE:Вычисление значений y по формуле тригонометрической функции с параметрами.
# INPUT:Параметры функции (A, B, C, D) и диапазон x (x_min, x_max).
# OUTPUT:DataFrame с колонками x и y.
# KEYWORDS:[DOMAIN(9): Mathematics; CONCEPT(8): Trigonometry; TECH(9): Python, math]
# LINKS:[USES_API(9): math.sin]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется формула y = A * sin(B * x + C) + D вместо простой sin(x)?
# A: Эта формула позволяет демонстрировать амплитуду (A), частоту (B), фазовый сдвиг (C) и вертикальный сдвиг (D) тригонометрической функции, что делает урок более образовательным.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля тригонометрической логики с параметрической формулой.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Функция расчета точек тригонометрической функции] => calculate_trig
# END_MODULE_MAP
#
# START_USE_CASES:
# - [calculate_trig]:User -> Input Params -> DataFrame with x, y
# END_USE_CASES

import logging
import math
import pandas as pd

logger = logging.getLogger(__name__)

# START_FUNCTION_calculate_trig
# START_CONTRACT:
# PURPOSE:Расчет точек тригонометрической функции y = A * sin(B * x + C) + D.
# INPUTS:
# - float => A: Амплитуда (множитель перед sin)
# - float => B: Частота (множитель перед x)
# - float => C: Фазовый сдвиг (добавляется к аргументу sin)
# - float => D: Вертикальный сдвиг (добавляется к результату)
# - float => x_min: Начало диапазона x
# - float => x_max: Конец диапазона x
# OUTPUTS:
# - pd.DataFrame - DataFrame с колонками x и y
# SIDE_EFFECTS: Нет
# KEYWORDS:[PATTERN(6): Algorithm; CONCEPT(9): Trigonometry]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def calculate_trig(A: float, B: float, C: float, D: float, x_min: float, x_max: float) -> pd.DataFrame:
    """
    Вычисляет значения y для тригонометрической функции y = A * sin(B * x + C) + D
    на заданном диапазоне x. Создает DataFrame с колонками x и y.
    
    Функция генерирует точки от x_min до x_max с равномерным шагом,
    применяя к каждому значению x формулу тригонометрической функции.
    """
    # START_BLOCK_VALIDATE_INPUT: [Проверка входных данных]
    if x_min >= x_max:
        logger.error(f"[Math][IMP:10][calculate_trig][VALIDATION][Error] x_min ({x_min}) >= x_max ({x_max}) [FATAL]")
        return pd.DataFrame(columns=['x', 'y'])
    
    logger.debug(f"[Math][IMP:4][calculate_trig][VALIDATION][Params] A={A}, B={B}, C={C}, D={D}, range=[{x_min}, {x_max}] [INFO]")
    # END_BLOCK_VALIDATE_INPUT

    # START_BLOCK_GENERATE_POINTS: [Генерация точек]
    num_points = 100  # Количество точек для генерации
    step = (x_max - x_min) / (num_points - 1)
    
    x_values = []
    y_values = []
    
    for i in range(num_points):
        x = x_min + i * step
        y = A * math.sin(B * x + C) + D
        x_values.append(round(x, 4))
        y_values.append(round(y, 4))
    
    logger.info(f"[BeliefState][IMP:9][calculate_trig][CALCULATION][Value] Вычислено {num_points} точек по формуле y = {A} * sin({B} * x + {C}) + {D} [SUCCESS]")
    # END_BLOCK_GENERATE_POINTS

    # START_BLOCK_CREATE_DATAFRAME: [Создание DataFrame]
    df = pd.DataFrame({'x': x_values, 'y': y_values})
    logger.info(f"[Data][IMP:8][calculate_trig][DATAFRAME][Success] Создан DataFrame с {len(df)} строками [OK]")
    return df
    # END_BLOCK_CREATE_DATAFRAME
# END_FUNCTION_calculate_trig
