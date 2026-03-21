# FILE:lesson_12/config_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Управление конфигурационным файлом config.json.
# SCOPE: Чтение и запись параметров параболы.
# INPUT: Параметры (a, c, x_min, x_max).
# OUTPUT: Словарь параметров.
# KEYWORDS:[DOMAIN(7): Persistence; CONCEPT(8): Configuration]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.1 - Исправление семантической разметки: добавлены MODULE_MAP и USE_CASES.]
# PREV_CHANGE_SUMMARY: [v1.0.0 - Создание модуля управления конфигурацией.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 8[Сохраняет параметры в JSON] => save_config
# FUNC 8[Загружает параметры из JSON] => load_config
# END_MODULE_MAP
#
# START_USE_CASES:
# - [save_config]: App -> Params -> config.json
# - [load_config]: App -> config.json -> Params
# END_USE_CASES

import json
import os
import logging

logger = logging.getLogger("lesson_12.app")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

# START_FUNCTION_save_config
# START_CONTRACT:
# PURPOSE: Сохранение параметров генерации в файл.
# INPUTS: 
# - a: float
# - c: float
# - x_min: float
# - x_max: float
# OUTPUTS: None
# COMPLEXITY_SCORE: 2
# END_CONTRACT
def save_config(a: float, c: float, x_min: float, x_max: float):
    """Сохраняет параметры в JSON файл."""
    # START_BLOCK_WRITE: [Запись в файл]
    data = {"a": a, "c": c, "x_min": x_min, "x_max": x_max}
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"[IO][IMP:8][save_config][WRITE][Success] Конфиг сохранен: {data} [VALUE]")
    # END_BLOCK_WRITE
# END_FUNCTION_save_config

# START_FUNCTION_load_config
# START_CONTRACT:
# PURPOSE: Загрузка параметров генерации из файла.
# INPUTS: None
# OUTPUTS: 
# - dict - Словарь параметров
# COMPLEXITY_SCORE: 2
# END_CONTRACT
def load_config() -> dict:
    """Загружает параметры из JSON файла. Возвращает дефолтные, если файл отсутствует."""
    # START_BLOCK_READ: [Чтение из файла]
    if not os.path.exists(CONFIG_PATH):
        logger.debug("[IO][IMP:4][load_config][READ][Default] Файл не найден, возврат дефолтов. [INFO]")
        return {"a": 1.0, "c": 0.0, "x_min": -10.0, "x_max": 10.0}
    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)
    logger.debug(f"[IO][IMP:4][load_config][READ][Success] Конфиг загружен: {data} [INFO]")
    return data
    # END_BLOCK_READ
# END_FUNCTION_load_config
