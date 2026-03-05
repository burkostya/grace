# FILE:lesson_v3/src/config_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление конфигурационным файлом JSON для Lesson_v3.
# SCOPE:Чтение, запись и инициализация параметров параболы.
# INPUT:Путь к файлу config.json, параметры (a, c, x_min, x_max).
# OUTPUT:Словарь с параметрами конфигурации.
# KEYWORDS:[DOMAIN(8):Configuration; CONCEPT(7):JSON_Storage; TECH(9):Python_json]
# LINKS:[READS_DATA_FROM(9):lesson_v3/config.json]
# END_MODULE_CONTRACT

# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления конфигурацией.]
# END_CHANGE_SUMMARY

# START_MODULE_MAP:
# FUNC 10[Загружает конфигурацию из файла или создает дефолтную] => load_config
# FUNC 10[Сохраняет параметры в файл конфигурации] => save_config
# END_MODULE_MAP

import json
import os
import logging

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "a": 1.0,
    "c": 0.0,
    "x_min": -10.0,
    "x_max": 10.0
}

# START_FUNCTION_load_config
# START_CONTRACT:
# PURPOSE:Загрузка параметров из JSON файла.
# INPUTS: 
# - str =>config_path: Путь к файлу
# OUTPUTS: 
# - dict -Словарь с параметрами
# SIDE_EFFECTS: Создает файл, если он отсутствует.
# END_CONTRACT
def load_config(config_path: str) -> dict:
    """Загружает конфигурацию или создает дефолтную."""
    # START_BLOCK_CHECK_EXISTENCE: [Проверка наличия файла]
    if not os.path.exists(config_path):
        logger.info(f"[Config][IMP:8][load_config][CHECK_EXISTENCE][FileMissing] Файл {config_path} не найден. Создаю дефолтный. [ACTION]")
        save_config(config_path, DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    # END_BLOCK_CHECK_EXISTENCE

    # START_BLOCK_READ_JSON: [Чтение данных]
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.debug(f"[Config][IMP:5][load_config][READ_JSON][Success] Конфигурация загружена: {config} [INFO]")
        return config
    except Exception as e:
        logger.error(f"[Config][IMP:10][load_config][READ_JSON][Error] Ошибка чтения {config_path}: {e}. Возвращаю дефолт. [FATAL]")
        return DEFAULT_CONFIG
    # END_BLOCK_READ_JSON
# END_FUNCTION_load_config

# START_FUNCTION_save_config
# START_CONTRACT:
# PURPOSE:Сохранение параметров в JSON файл.
# INPUTS: 
# - str =>config_path: Путь к файлу
# - dict =>config_data: Данные для сохранения
# OUTPUTS: 
# - bool -Успешность операции
# SIDE_EFFECTS: Перезаписывает файл конфигурации.
# END_CONTRACT
def save_config(config_path: str, config_data: dict) -> bool:
    """Сохраняет конфигурацию в файл."""
    # START_BLOCK_WRITE_JSON: [Запись данных]
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4)
        logger.info(f"[BeliefState][IMP:9][save_config][WRITE_JSON][Success] Конфигурация сохранена в {config_path}. [VALUE]")
        return True
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][save_config][WRITE_JSON][Exception] Не удалось сохранить конфиг: {e} [FATAL]")
        return False
    # END_BLOCK_WRITE_JSON
# END_FUNCTION_save_config
