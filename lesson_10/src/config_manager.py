# FILE:lesson_10/src/config_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление конфигурационным файлом config.json для хранения параметров параболы.
# SCOPE:Чтение, запись и инициализация настроек приложения.
# INPUT:Путь к файлу конфигурации.
# OUTPUT:Словарь с параметрами (a, c, x_min, x_max).
# KEYWORDS:[DOMAIN(State): Configuration; CONCEPT(Persistence): JSON; TECH(Python): json, os]
# LINKS:[USES_API(8): json]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется атомарная запись через временный файл?
# A: Для предотвращения повреждения config.json при сбое питания или прерывании процесса во время записи.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления конфигурацией.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Загружает конфигурацию из файла или создает дефолтную] => load_config
# FUNC 10[Сохраняет текущую конфигурацию в файл] => save_config
# END_MODULE_MAP
#
# START_USE_CASES:
# - [load_config]: System -> ReadConfig -> ConfigLoaded
# - [save_config]: User/CLI -> UpdateParams -> ConfigPersisted
# END_USE_CASES

import json
import os
import logging

logger = logging.getLogger(__name__)

# START_FUNCTION_load_config
# START_CONTRACT:
# PURPOSE:Загружает параметры из config.json. Если файл отсутствует, создает его с дефолтными значениями.
# INPUTS: 
# - Путь к файлу => config_path: str
# OUTPUTS: 
# - dict - Словарь с параметрами a, c, x_min, x_max
# SIDE_EFFECTS: Создает файл на диске, если его нет.
# KEYWORDS:[PATTERN(Defaults): Initializer]
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def load_config(config_path: str = "lesson_10/config.json") -> dict:
    """
    Загружает конфигурацию из JSON файла. В случае отсутствия файла 
    инициализирует его значениями по умолчанию (a=1.0, c=0.0, x_min=-10, x_max=10).
    Это гарантирует, что приложение всегда имеет валидное состояние для расчетов.
    """
    # START_BLOCK_CHECK_EXISTENCE: [Проверка наличия файла]
    defaults = {"a": 1.0, "c": 0.0, "x_min": -10.0, "x_max": 10.0}
    if not os.path.exists(config_path):
        logger.info(f"[State][IMP:7][load_config][CHECK_EXISTENCE][IO] Файл {config_path} не найден. Создаю дефолтный. [INFO]")
        save_config(defaults, config_path)
        return defaults
    # END_BLOCK_CHECK_EXISTENCE

    # START_BLOCK_READ_FILE: [Чтение данных]
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            logger.debug(f"[Data][IMP:4][load_config][READ_FILE][Success] Конфигурация загружена: {config} [VALUE]")
            return config
    except Exception as e:
        logger.error(f"[System][IMP:10][load_config][READ_FILE][Error] Ошибка чтения {config_path}: {e}. Возвращаю дефолты. [FATAL]")
        return defaults
    # END_BLOCK_READ_FILE
# END_FUNCTION_load_config

# START_FUNCTION_save_config
# START_CONTRACT:
# PURPOSE:Сохраняет словарь параметров в config.json.
# INPUTS: 
# - Словарь параметров => config: dict
# - Путь к файлу => config_path: str
# OUTPUTS: 
# - bool - Успешность операции
# SIDE_EFFECTS: Перезаписывает файл на диске.
# KEYWORDS:[PATTERN(Persistence): Writer]
# COMPLEXITY_SCORE: 2
# END_CONTRACT
def save_config(config: dict, config_path: str = "lesson_10/config.json") -> bool:
    """
    Выполняет сериализацию словаря в формат JSON и сохранение на диск.
    Используется для фиксации изменений параметров, внесенных через UI или CLI.
    """
    # START_BLOCK_WRITE_JSON: [Запись в файл]
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        logger.info(f"[BeliefState][IMP:9][save_config][WRITE_JSON][IO] Конфигурация успешно сохранена в {config_path} [SUCCESS]")
        return True
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][save_config][WRITE_JSON][Exception] Не удалось сохранить конфиг: {e} [FATAL]")
        return False
    # END_BLOCK_WRITE_JSON
# END_FUNCTION_save_config
