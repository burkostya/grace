# FILE:lesson_20/config_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление конфигурационным файлом JSON для параметров параболы.
# SCOPE:Чтение и запись параметров a, c, x_min, x_max.
# INPUT:Путь к файлу config.json.
# OUTPUT:Словарь параметров или статус сохранения.
# KEYWORDS:[DOMAIN(8): Configuration; CONCEPT(7): StateManagement; TECH(9): JSON]
# LINKS:[USES_API(8): json]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется JSON для хранения параметров?
# A: Это простое и человекочитаемое решение для хранения небольшого набора настроек UI.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание модуля управления конфигурацией.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Загружает конфигурацию из файла] => load_config
# FUNC 10[Сохраняет конфигурацию в файл] => save_config
# END_MODULE_MAP

import json
import os
import logging

logger = logging.getLogger("lesson_20")

# START_FUNCTION_load_config
# START_CONTRACT:
# PURPOSE:Загрузка параметров из JSON файла.
# INPUTS:
# - str => config_path: Путь к файлу
# OUTPUTS:
# - dict - Словарь с параметрами
# KEYWORDS:[PATTERN(6): Loader]
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def load_config(config_path: str = "lesson_20/config.json") -> dict:
    """
    Загружает параметры параболы из указанного JSON файла. 
    Если файл отсутствует, возвращает значения по умолчанию.
    """
    default_config = {"a": 1.0, "c": 0.0, "x_min": -10.0, "x_max": 10.0}
    
    # START_BLOCK_READ_FILE: [Чтение файла конфигурации]
    if not os.path.exists(config_path):
        logger.info(f"[Config][IMP:7][load_config][READ_FILE][Status] Файл не найден, используем default. [INFO]")
        return default_config
        
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            logger.info(f"[Config][IMP:8][load_config][READ_FILE][Success] Конфиг загружен из {config_path}. [SUCCESS]")
            return config
    except Exception as e:
        logger.error(f"[Config][IMP:10][load_config][READ_FILE][Error] Ошибка чтения конфига: {e}. [FATAL]")
        return default_config
    # END_BLOCK_READ_FILE
# END_FUNCTION_load_config

# START_FUNCTION_save_config
# START_CONTRACT:
# PURPOSE:Сохранение параметров в JSON файл.
# INPUTS:
# - dict => config: Словарь параметров
# - str => config_path: Путь к файлу
# OUTPUTS:
# - bool - Статус успеха
# KEYWORDS:[PATTERN(6): Saver]
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def save_config(config: dict, config_path: str = "lesson_20/config.json") -> bool:
    """
    Сохраняет переданный словарь параметров в JSON файл.
    """
    # START_BLOCK_WRITE_FILE: [Запись в файл]
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        logger.info(f"[Config][IMP:9][save_config][WRITE_FILE][Success] Конфиг сохранен в {config_path}. [VALUE]")
        return True
    except Exception as e:
        logger.error(f"[Config][IMP:10][save_config][WRITE_FILE][Error] Ошибка сохранения конфига: {e}. [FATAL]")
        return False
    # END_BLOCK_WRITE_FILE
# END_FUNCTION_save_config
