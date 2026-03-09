# FILE:lesson_9/src/config_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление конфигурационным файлом JSON для параметров параболы.
# SCOPE: Чтение и запись параметров a, c, x_min, x_max в config.json.
# INPUT:Путь к файлу конфигурации, значения параметров.
# OUTPUT: Словарь с параметрами или статус операции записи.
# KEYWORDS:[DOMAIN(8): Configuration; CONCEPT(7): JSON_Storage; TECH(9): json, os]
# LINKS:[USES_API(8): json, os]
# LINKS_TO_SPECIFICATION:[DevelopmentPlan.md:11-13]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления конфигурацией.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC [8][Загружает конфигурацию из файла] => load_config
# FUNC [8][Сохраняет конфигурацию в файл] => save_config
# END_MODULE_MAP
#
# START_USE_CASES:
# - [load_config]: System -> Read config.json -> ParametersLoaded
# - [save_config]: User/System -> Write config.json -> ParametersPersisted
# END_USE_CASES

import json
import os
import logging

# Настройка логгера для LDD 2.0
logger = logging.getLogger("lesson_9")
if not logger.handlers:
    handler = logging.FileHandler("lesson_9/app_9.log", encoding="utf-8")
    formatter = logging.Formatter('%(asctime)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

CONFIG_PATH = "lesson_9/config.json"

# START_FUNCTION_load_config
# START_CONTRACT:
# PURPOSE:Загрузка параметров из JSON файла. Если файл отсутствует, возвращает дефолтные значения.
# INPUTS: 
# - None
# OUTPUTS: 
# - dict - Словарь с параметрами (a, c, x_min, x_max)
# SIDE_EFFECTS: Чтение файла с диска.
# KEYWORDS:[PATTERN(6): DefaultValues; CONCEPT(8): FileIO]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def load_config() -> dict:
    """
    Функция выполняет чтение конфигурационного файла config.json. 
    В случае отсутствия файла или ошибок парсинга, возвращается набор 
    безопасных значений по умолчанию (a=1, c=0, x_min=-10, x_max=10).
    Это обеспечивает отказоустойчивость системы при первом запуске.
    """
    # START_BLOCK_DEFAULT_VALUES: [Инициализация дефолтных параметров]
    defaults = {
        "a": 1.0,
        "c": 0.0,
        "x_min": -10.0,
        "x_max": 10.0
    }
    logger.debug(f"[Config][IMP:4][load_config][DEFAULT_VALUES][Init] Дефолтные значения подготовлены: {defaults} [INFO]")
    # END_BLOCK_DEFAULT_VALUES

    # START_BLOCK_READ_FILE: [Попытка чтения файла]
    if not os.path.exists(CONFIG_PATH):
        logger.info(f"[Config][IMP:7][load_config][READ_FILE][Check] Файл {CONFIG_PATH} не найден. Используем дефолты. [WARNING]")
        return defaults

    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
            logger.info(f"[Config][IMP:8][load_config][READ_FILE][Success] Конфигурация успешно загружена из {CONFIG_PATH} [VALUE]")
            # Объединяем с дефолтами на случай отсутствия ключей
            final_config = {**defaults, **config}
            return final_config
    except Exception as e:
        logger.error(f"[Config][IMP:10][load_config][READ_FILE][Error] Ошибка при чтении {CONFIG_PATH}: {e}. Возврат дефолтов. [FATAL]")
        return defaults
    # END_BLOCK_READ_FILE
# END_FUNCTION_load_config

# START_FUNCTION_save_config
# START_CONTRACT:
# PURPOSE:Сохранение параметров в JSON файл.
# INPUTS: 
# - dict => config: Словарь с параметрами для сохранения.
# OUTPUTS: 
# - bool - Статус успеха операции.
# SIDE_EFFECTS: Запись файла на диск.
# KEYWORDS:[PATTERN(6): Persistence; CONCEPT(8): FileIO]
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def save_config(config: dict) -> bool:
    """
    Функция сериализует переданный словарь в формат JSON и записывает его 
    в файл config.json. Используется отступ (indent=4) для обеспечения 
    читаемости файла человеком. Перед записью проверяется наличие директории.
    """
    # START_BLOCK_PREPARE_DIR: [Проверка и создание директории]
    config_dir = os.path.dirname(CONFIG_PATH)
    if config_dir and not os.path.exists(config_dir):
        os.makedirs(config_dir)
        logger.debug(f"[Config][IMP:5][save_config][PREPARE_DIR][Create] Директория {config_dir} создана. [INFO]")
    # END_BLOCK_PREPARE_DIR

    # START_BLOCK_WRITE_FILE: [Запись данных в файл]
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        logger.info(f"[Config][IMP:9][save_config][WRITE_FILE][Success] Параметры {config} сохранены в {CONFIG_PATH} [VALUE]")
        return True
    except Exception as e:
        logger.critical(f"[Config][IMP:10][save_config][WRITE_FILE][Error] Не удалось сохранить конфиг: {e} [FATAL]")
        return False
    # END_BLOCK_WRITE_FILE
# END_FUNCTION_save_config
