# FILE: lesson_22/config_manager.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Управление конфигурацией параметров параболы (a, c, x_min, x_max) через config.json.
# SCOPE: Чтение и запись параметров во внешнее JSON-хранилище.
# INPUT: Параметры параболы (a, c, x_min, x_max).
# OUTPUT: Загруженные или сохраненные значения параметров.
# KEYWORDS:[DOMAIN(8): Configuration; CONCEPT(7): StateManagement; TECH(9): JSON]
# LINKS:[USES_API(8): json, os]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется JSON для конфигурации?
# A: Простота, нативная поддержка в Python и читаемость как человеком, так и другими агентами.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля config_manager.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Загружает конфигурацию из файла config.json] => load_config
# FUNC 10[Сохраняет параметры в файл config.json] => save_config
# END_MODULE_MAP

import json
import os
import logging

logger = logging.getLogger(__name__)


# START_FUNCTION_load_config
# START_CONTRACT:
# PURPOSE: Загружает параметры из config.json или возвращает дефолтные значения.
# INPUTS:
# - str => config_path: Путь к файлу конфигурации.
# OUTPUTS:
# - dict - Словарь с параметрами (a, c, x_min, x_max).
# SIDE_EFFECTS: Чтение файла с диска.
# KEYWORDS:[PATTERN(6): DefaultProvider; CONCEPT(8): DataLoading]
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def load_config(config_path: str = "lesson_22/config.json") -> dict:
    """
    Функция считывает параметры параболы из JSON-файла. Если файл отсутствует или поврежден,
    возвращает безопасные значения по умолчанию (a=1, c=0, x_min=-10, x_max=10).
    """
    # START_BLOCK_DEFAULT_VALUES: [Значения по умолчанию]
    defaults = {"a": 1.0, "c": 0.0, "x_min": -10.0, "x_max": 10.0}
    # END_BLOCK_DEFAULT_VALUES

    # START_BLOCK_READ_JSON: [Попытка чтения файла]
    if not os.path.exists(config_path):
        logger.info(
            f"[Config][IMP:7][load_config][READ_JSON][NotFound] Файл {config_path} не найден. Используются дефолтные значения. [WARN]"
        )
        return defaults

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            logger.debug(
                f"[Config][IMP:5][load_config][READ_JSON][Success] Конфигурация загружена: {config} [INFO]"
            )
            return config
    except Exception as e:
        logger.critical(
            f"[SystemError][IMP:10][load_config][READ_JSON][ExceptionEnrichment] Ошибка при чтении {config_path}: {e} [FATAL]"
        )
        return defaults
    # END_BLOCK_READ_JSON


# END_FUNCTION_load_config


# START_FUNCTION_save_config
# START_CONTRACT:
# PURPOSE: Сохраняет параметры в JSON-файл.
# INPUTS:
# - float => a: Коэффициент a.
# - float => c: Коэффициент c.
# - float => x_min: Минимум x.
# - float => x_max: Максимум x.
# - str => config_path: Путь для сохранения.
# OUTPUTS:
# - bool - Успешность операции.
# SIDE_EFFECTS: Запись файла на диск.
# KEYWORDS:[PATTERN(6): StatePersistence; CONCEPT(8): DataSaving]
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def save_config(
    a: float,
    c: float,
    x_min: float,
    x_max: float,
    config_path: str = "lesson_22/config.json",
) -> bool:
    """
    Функция записывает переданные параметры в файл config.json. Это фиксирует
    'Belief State' системы о текущих настройках генерации данных.
    """
    # START_BLOCK_PREPARE_DATA: [Формирование словаря]
    data = {"a": a, "c": c, "x_min": x_min, "x_max": x_max}
    logger.info(
        f"[BeliefState][IMP:9][save_config][PREPARE_DATA][Saving] Сохранение новой конфигурации: {data} [VALUE]"
    )
    # END_BLOCK_PREPARE_DATA

    # START_BLOCK_WRITE_JSON: [Атомарная запись в файл]
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logger.info(
            f"[Config][IMP:8][save_config][WRITE_JSON][Success] Файл {config_path} успешно обновлен. [SUCCESS]"
        )
        return True
    except Exception as e:
        logger.critical(
            f"[SystemError][IMP:10][save_config][WRITE_JSON][ExceptionEnrichment] Ошибка при записи {config_path}: {e} [FATAL]"
        )
        return False
    # END_BLOCK_WRITE_JSON


# END_FUNCTION_save_config
