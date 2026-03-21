# FILE:lesson_17/src/config_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление конфигурационным файлом config.json для Lesson_17.
# SCOPE:Чтение и запись параметров тригонометрической функции (A, B, C, D, x_min, x_max).
# INPUT:Путь к файлу config.json.
# OUTPUT:Словарь с параметрами или статус сохранения.
# KEYWORDS:[DOMAIN(8): Configuration; TECH(9): JSON]
# LINKS:[USES_API(8): json, os]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления конфигурацией для тригонометрической функции.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Загружает конфигурацию из JSON файла] => load_config
# FUNC 10[Сохраняет конфигурацию в JSON файл] => save_config
# END_MODULE_MAP

import json
import os
import logging

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "A": 1.0,
    "B": 1.0,
    "C": 0.0,
    "D": 0.0,
    "x_min": -10.0,
    "x_max": 10.0
}

# START_FUNCTION_load_config
# START_CONTRACT:
# PURPOSE:Загрузка параметров из config.json или возврат значений по умолчанию.
# INPUTS:
# - str => config_path: Путь к файлу конфигурации.
# OUTPUTS:
# - dict - Словарь с параметрами.
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def load_config(config_path: str = "lesson_17/config.json") -> dict:
    """
    Считывает JSON файл конфигурации. Если файл отсутствует или поврежден,
    возвращает словарь с параметрами по умолчанию для тригонометрической функции.
    Это обеспечивает отказоустойчивость системы при первом запуске или ошибках ФС.
    """
    # START_BLOCK_READ_FILE: [Попытка чтения файла]
    if not os.path.exists(config_path):
        logger.warning(f"[Config][IMP:7][load_config][READ_FILE][NotFound] Файл {config_path} не найден. Используем default. [WARN]")
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            logger.info(f"[Config][IMP:8][load_config][READ_FILE][Success] Конфигурация загружена из {config_path}. [OK]")
            return config
    except Exception as e:
        logger.error(f"[Config][IMP:10][load_config][READ_FILE][Error] Ошибка при чтении {config_path}: {e}. [FAIL]")
        return DEFAULT_CONFIG.copy()
    # END_BLOCK_READ_FILE
# END_FUNCTION_load_config

# START_FUNCTION_save_config
# START_CONTRACT:
# PURPOSE:Сохранение параметров в config.json.
# INPUTS:
# - dict => config: Словарь с параметрами.
# - str => config_path: Путь к файлу конфигурации.
# OUTPUTS:
# - bool - Статус успеха операции.
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def save_config(config: dict, config_path: str = "lesson_17/config.json") -> bool:
    """
    Записывает переданный словарь в JSON файл. Перед записью проверяет
    наличие директории и создает её при необходимости.
    """
    # START_BLOCK_WRITE_FILE: [Запись данных на диск]
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        logger.info(f"[Config][IMP:9][save_config][WRITE_FILE][Success] Конфигурация сохранена в {config_path}. [OK]")
        return True
    except Exception as e:
        logger.critical(f"[Config][IMP:10][save_config][WRITE_FILE][Error] Не удалось сохранить конфиг: {e}. [FATAL]")
        return False
    # END_BLOCK_WRITE_FILE
# END_FUNCTION_save_config
