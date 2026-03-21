# FILE:lesson_11/src/config_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление конфигурацией приложения через JSON файл.
# SCOPE:Чтение и запись параметров конфигурации в lesson_11/config.json.
# INPUT:Словарь конфигурации для сохранения или запрос на загрузку.
# OUTPUT:Словарь с параметрами конфигурации.
# KEYWORDS:[DOMAIN(8): Configuration; CONCEPT(7): Persistence; TECH(9): JSON]
# LINKS:[USES_API(8): json, logging]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется абсолютный путь относительно корня проекта для логов и конфига?
# A: Для обеспечения предсказуемого поведения при запуске из разных директорий и соответствия структуре NEW_LESSONS.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления конфигурацией с LDD 2.0 логированием.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Загружает параметры из JSON файла] => load_config
# FUNC 10[Сохраняет параметры в JSON файл] => save_config
# END_MODULE_MAP
#
# START_USE_CASES:
# - [load_config]: System -> ReadFile -> ConfigLoaded
# - [save_config]: User/System -> WriteFile -> ConfigSaved
# END_USE_CASES

import json
import logging
import os

# START_BLOCK_LOGGING_SETUP: [Настройка LDD 2.0 логирования]
LOG_FILE = "lesson_11/app_11.log"
CONFIG_FILE = "lesson_11/config.json"

# Создаем директорию для логов если нужно (хотя в данном случае она уже есть)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logger = logging.getLogger("config_manager")
# END_BLOCK_LOGGING_SETUP

# START_FUNCTION_load_config
# START_CONTRACT:
# PURPOSE:Загружает конфигурацию из файла lesson_11/config.json.
# INPUTS: 
# - Нет
# OUTPUTS: 
# - dict - Словарь с параметрами конфигурации.
# SIDE_EFFECTS: Чтение файла с диска.
# KEYWORDS:[PATTERN(6): DataAccessObject; CONCEPT(8): Serialization]
# COMPLEXITY_SCORE: 5[Обработка исключений при чтении файла.]
# END_CONTRACT
def load_config() -> dict:
    """
    Функция выполняет чтение файла конфигурации в формате JSON. 
    В случае отсутствия файла или ошибок парсинга, возвращает пустой словарь 
    и фиксирует событие в логе с высоким уровнем важности. 
    Используется LDD 2.0 для трассировки процесса загрузки.
    """
    # START_BLOCK_READ_FILE: [Чтение данных с диска]
    logger.info(f"[Flow][IMP:5][load_config][READ_FILE][Start] Попытка загрузки конфигурации из {CONFIG_FILE} [INFO]")
    
    if not os.path.exists(CONFIG_FILE):
        logger.warning(f"[IO][IMP:8][load_config][READ_FILE][ConditionCheck] Файл {CONFIG_FILE} не найден. [WARN]")
        return {}

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
            logger.info(f"[IO][IMP:7][load_config][READ_FILE][Success] Конфигурация успешно загружена. Ключей: {len(config_data)} [SUCCESS]")
            return config_data
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][load_config][READ_FILE][ExceptionEnrichment] Ошибка при чтении JSON: {e} [FATAL]")
        return {}
    # END_BLOCK_READ_FILE
# END_FUNCTION_load_config

# START_FUNCTION_save_config
# START_CONTRACT:
# PURPOSE:Сохраняет переданный словарь в файл lesson_11/config.json.
# INPUTS: 
# - dict => config_dict: Словарь с параметрами.
# OUTPUTS: 
# - bool - Статус успешности операции.
# SIDE_EFFECTS: Запись файла на диск.
# KEYWORDS:[PATTERN(6): DataAccessObject; CONCEPT(8): Persistence]
# COMPLEXITY_SCORE: 4[Линейная запись с обработкой ошибок.]
# END_CONTRACT
def save_config(config_dict: dict) -> bool:
    """
    Функция сериализует переданный словарь в формат JSON и записывает его в файл.
    Обеспечивает атомарность логирования процесса записи через LDD 2.0.
    В случае успеха возвращает True, при ошибке — False с записью критического лога.
    """
    # START_BLOCK_WRITE_FILE: [Запись данных на диск]
    logger.info(f"[Flow][IMP:5][save_config][WRITE_FILE][Start] Сохранение конфигурации в {CONFIG_FILE} [INFO]")
    
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=4, ensure_ascii=False)
            
        logger.info(f"[BeliefState][IMP:9][save_config][WRITE_FILE][Success] Конфигурация сохранена. [VALUE]")
        return True
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][save_config][WRITE_FILE][ExceptionEnrichment] Не удалось сохранить файл: {e} [FATAL]")
        return False
    # END_BLOCK_WRITE_FILE
# END_FUNCTION_save_config
