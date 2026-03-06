# FILE: lesson_v6/src/config_manager.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Управление файлом конфигурации config.json для Lesson 6.
# SCOPE: Чтение и запись параметров параболы (a, c, x_min, x_max).
# INPUT: Путь к файлу конфигурации (по умолчанию из __init__.py).
# OUTPUT: Словарь с параметрами или обновление файла конфигурации.
# KEYWORDS:[DOMAIN(8): StateManagement; CONCEPT(7): JSONSerialization; TECH(9): FileIO]
# LINKS:[READS_DATA_FROM(8): config.json]
# END_MODULE_CONTRACT
#
# START_INVARIANTS:
# - Функция load_config ВСЕГДА возвращает словарь с ключами 'a', 'c', 'x_min', 'x_max'.
# - Функция save_config ВСЕГДА создает валидный JSON файл.
# END_INVARIANTS
#
# START_RATIONALE:
# Q: Почему используется json.load/json.dump вместо ручного парсинга?
# A: Стандартная библиотека json обеспечивает надежную сериализацию/десериализацию и обработку ошибок.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления конфигурацией с LDD 2.0 логированием.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Загружает параметры из config.json] => load_config
# FUNC 10[Сохраняет параметры в config.json] => save_config
# END_MODULE_MAP
#
# START_USE_CASES:
# -[load_config]: System (Startup) -> ReadConfiguration -> ParametersLoaded
# -[save_config]: User (UI/CLI) -> UpdateParameters -> ConfigurationSaved
# END_USE_CASES

import json
import logging
import os
from typing import Dict, Any

# Настройка логирования
logger = logging.getLogger(__name__)

# START_FUNCTION_load_config
# START_CONTRACT:
# PURPOSE: Чтение параметров из файла конфигурации.
# INPUTS: 
# - [Путь к файлу конфигурации] => config_path: str
# OUTPUTS: 
# - dict - Словарь с параметрами {'a': float, 'c': float, 'x_min': float, 'x_max': float}
# SIDE_EFFECTS: Отсутствуют.
# KEYWORDS:[PATTERN(6): Singleton; CONCEPT(8): LazyLoad]
# END_CONTRACT
def load_config(config_path: str) -> Dict[str, Any]:
    """Загружает параметры конфигурации из JSON файла."""
    
    # START_BLOCK_VERIFY_FILE_EXISTS: [Проверка существования файла конфигурации]
    if not os.path.exists(config_path):
        logger.warning(f"[FileCheck][IMP:5][load_config][VERIFY_FILE_EXISTS][ConditionCheck] Файл конфигурации не найден: {config_path}. Будут использованы значения по умолчанию. [WARN]")
        return {"a": 1.0, "c": 0.0, "x_min": -10.0, "x_max": 10.0}
    # END_BLOCK_VERIFY_FILE_EXISTS

    # START_BLOCK_READ_CONFIG_FILE: [Чтение и парсинг JSON файла]
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        logger.info(f"[BeliefState][IMP:9][load_config][READ_CONFIG_FILE][ReturnData] Конфигурация успешно загружена. Параметры: {config} [VALUE]")
        return config
    except json.JSONDecodeError as e:
        logger.critical(f"[SystemError][IMP:10][load_config][READ_CONFIG_FILE][ExceptionEnrichment] Ошибка парсинга JSON. Local vars: config_path={config_path}. Err: {e} [FATAL]")
        raise
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][load_config][READ_CONFIG_FILE][ExceptionEnrichment] Неизвестная ошибка при чтении конфигурации. Local vars: config_path={config_path}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_READ_CONFIG_FILE
# END_FUNCTION_load_config

# START_FUNCTION_save_config
# START_CONTRACT:
# PURPOSE: Сохранение параметров в файл конфигурации.
# INPUTS: 
# - [Словарь с параметрами] => config: Dict[str, Any]
# - [Путь к файлу конфигурации] => config_path: str
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Перезаписывает файл config.json.
# KEYWORDS:[PATTERN(6): Persistence; CONCEPT(8): AtomicWrite]
# END_CONTRACT
def save_config(config: Dict[str, Any], config_path: str) -> None:
    """Сохраняет параметры конфигурации в JSON файл."""
    
    # START_BLOCK_VALIDATE_INPUT: [Валидация входных данных]
    required_keys = ['a', 'c', 'x_min', 'x_max']
    for key in required_keys:
        if key not in config:
            logger.error(f"[ValidationError][IMP:7][save_config][VALIDATE_INPUT][ConditionCheck] Отсутствует обязательный ключ: {key}. [ERROR]")
            raise ValueError(f"Missing required key: {key}")
    # END_BLOCK_VALIDATE_INPUT

    # START_BLOCK_WRITE_CONFIG_FILE: [Запись JSON файла]
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            
        logger.info(f"[BeliefState][IMP:9][save_config][WRITE_CONFIG_FILE][ReturnData] Конфигурация успешно сохранена. Параметры: {config} [VALUE]")
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][save_config][WRITE_CONFIG_FILE][ExceptionEnrichment] Ошибка при записи конфигурации. Local vars: config_path={config_path}, config={config}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_WRITE_CONFIG_FILE
# END_FUNCTION_save_config
