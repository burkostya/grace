# FILE:lesson_v4/src/config_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление конфигурацией приложения через JSON файл.
# SCOPE:Чтение и валидация настроек из config.json.
# INPUT:Путь к JSON файлу.
# OUTPUT:Объект конфигурации (dict).
# KEYWORDS:[DOMAIN(8): Configuration; CONCEPT(7): SettingsManagement; TECH(9): JSON]
# LINKS:[READS_DATA_FROM(9): lesson_v4/config.json]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления конфигурацией.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Загружает конфигурацию из файла] => load_config
# END_MODULE_MAP
#
# START_USE_CASES:
# - [load_config]: System -> ReadConfigFile -> ConfigLoaded
# END_USE_CASES

import json
import os
import logging

logger = logging.getLogger(__name__)

# START_FUNCTION_load_config
# START_CONTRACT:
# PURPOSE:Загружает и возвращает настройки из JSON файла.
# INPUTS: 
# - str => config_path: Путь к файлу конфигурации
# OUTPUTS: 
# - dict -Словарь с настройками
# SIDE_EFFECTS: Чтение файловой системы.
# KEYWORDS:[PATTERN(6): Singleton; CONCEPT(8): I/O]
# END_CONTRACT
def load_config(config_path: str = "lesson_v4/config.json") -> dict:
    """Загружает конфигурацию из JSON файла."""
    
    # START_BLOCK_READ_FILE: [Чтение данных из файла]
    logger.debug(f"[Config][IMP:5][load_config][READ_FILE][Start] Загрузка конфигурации из {config_path} [INFO]")
    
    if not os.path.exists(config_path):
        logger.error(f"[Config][IMP:10][load_config][READ_FILE][Error] Файл {config_path} не найден! [FATAL]")
        raise FileNotFoundError(f"Config file not found: {config_path}")

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info(f"[BeliefState][IMP:9][load_config][READ_FILE][Success] Конфигурация успешно загружена. [VALUE]")
        return config
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][load_config][READ_FILE][Exception] Ошибка парсинга JSON: {e} [FATAL]")
        raise
    # END_BLOCK_READ_FILE
# END_FUNCTION_load_config
