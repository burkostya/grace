# FILE: lesson_v7/src/config_manager.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Управление конфигурацией приложения через файл config.json.
# SCOPE: Чтение, запись и валидация параметров генерации параболы.
# INPUT: Путь к файлу конфигурации (по умолчанию lesson_v7/config.json).
# OUTPUT: Словарь с параметрами (a, c, x_min, x_max).
# KEYWORDS:[DOMAIN(8): StateManagement; CONCEPT(7): Persistence; TECH(9): JSON]
# LINKS:[READS_DATA_FROM(10): config.json; WRITES_DATA_TO(10): config.json]
# END_MODULE_CONTRACT
#
# START_INVARIANTS:
# - Функция load_config ВСЕГДА возвращает словарь, даже если файл не существует (создает дефолтный).
# - Функция save_config ВСЕГДА создает/перезаписывает файл конфигурации.
# END_INVARIANTS
#
# START_RATIONALE:
# Q: Почему используется pathlib.Path вместо строк?
# A: Path обеспечивает кроссплатформенную совместимость и удобные методы для работы с путями (parent, name, exists).
# Q: Почему load_config создает дефолтный конфиг при отсутствии файла?
# A: Это обеспечивает "Zero-Context Survival" - приложение может работать сразу после клонирования без ручной настройки.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления конфигурацией.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Загружает конфигурацию из JSON файла или создает дефолтную] => load_config
# FUNC 10[Сохраняет параметры конфигурации в JSON файл] => save_config
# END_MODULE_MAP
#
# START_USE_CASES:
# -[load_config]: Application (Startup) -> LoadParameters -> ConfigurationAvailable
# -[save_config]: User (UI/CLI) -> UpdateParameters -> ConfigurationPersisted
# END_USE_CASES

import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Константы для путей и дефолтных значений
DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "config.json"
DEFAULT_CONFIG = {
    "a": 1.0,
    "c": 0.0,
    "x_min": -10.0,
    "x_max": 10.0
}

# START_FUNCTION_load_config
# START_CONTRACT:
# PURPOSE: Загрузка параметров конфигурации из JSON файла.
# INPUTS: 
# - Путь к файлу конфигурации => config_path: Path (опционально, по умолчанию DEFAULT_CONFIG_PATH)
# OUTPUTS: 
# - dict - Словарь с параметрами конфигурации
# SIDE_EFFECTS: Создает файл конфигурации с дефолтными значениями, если он не существует.
# KEYWORDS:[PATTERN(6): Singleton; CONCEPT(8): LazyInitialization]
# END_CONTRACT
def load_config(config_path: Path = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    """Загружает конфигурацию из JSON файла или создает дефолтную."""
    
    # START_BLOCK_VERIFY_PATH: [Проверка существования файла конфигурации]
    logger.info(f"[ConfigLoad][IMP:7][load_config][VERIFY_PATH][FileCheck] Попытка загрузки конфигурации из {config_path} [INFO]")
    
    if not config_path.exists():
        # START_BLOCK_CREATE_DEFAULT: [Создание дефолтной конфигурации]
        logger.warning(f"[ConfigLoad][IMP:8][load_config][CREATE_DEFAULT][FileCreation] Файл конфигурации не найден. Создание дефолтного: {DEFAULT_CONFIG} [WARN]")
        save_config(DEFAULT_CONFIG, config_path)
        logger.info(f"[BeliefState][IMP:9][load_config][CREATE_DEFAULT][InitComplete] Инициализация дефолтной конфигурации завершена. Ожидаю параболу y=1*x^2+0. [VALUE]")
        # END_BLOCK_CREATE_DEFAULT
        
        return DEFAULT_CONFIG.copy()
    # END_BLOCK_VERIFY_PATH
    
    # START_BLOCK_READ_FILE: [Чтение и парсинг JSON]
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        # START_BLOCK_VALIDATE: [Валидация структуры конфигурации]
        required_keys = {"a", "c", "x_min", "x_max"}
        if not required_keys.issubset(config_data.keys()):
            missing_keys = required_keys - set(config_data.keys())
            logger.error(f"[ConfigLoad][IMP:10][load_config][VALIDATE][ValidationError] Отсутствуют обязательные ключи: {missing_keys}. Local vars: config_data={config_data} [FATAL]")
            raise ValueError(f"Некорректная структура конфигурации. Отсутствуют ключи: {missing_keys}")
        # END_BLOCK_VALIDATE
        
        logger.info(f"[BeliefState][IMP:9][load_config][READ_FILE][LoadSuccess] Конфигурация загружена успешно. Параметры: a={config_data['a']}, c={config_data['c']}, x_range=({config_data['x_min']}, {config_data['x_max']}) [VALUE]")
        return config_data
        
    except json.JSONDecodeError as e:
        logger.critical(f"[ConfigLoad][IMP:10][load_config][READ_FILE][ExceptionEnrichment] Ошибка парсинга JSON. Local vars: config_path={config_path}. Err: {e} [FATAL]")
        raise ValueError(f"Файл конфигурации содержит некорректный JSON: {e}") from e
    except Exception as e:
        logger.critical(f"[ConfigLoad][IMP:10][load_config][READ_FILE][ExceptionEnrichment] Неожиданная ошибка при чтении. Local vars: config_path={config_path}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_READ_FILE
# END_FUNCTION_load_config

# START_FUNCTION_save_config
# START_CONTRACT:
# PURPOSE: Сохранение параметров конфигурации в JSON файл.
# INPUTS: 
# - Словарь параметров => config_data: Dict[str, Any]
# - Путь к файлу конфигурации => config_path: Path (опционально)
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Создает или перезаписывает файл конфигурации.
# KEYWORDS:[PATTERN(6): Serialization; CONCEPT(8): Persistence]
# END_CONTRACT
def save_config(config_data: Dict[str, Any], config_path: Path = DEFAULT_CONFIG_PATH) -> None:
    """Сохраняет конфигурацию в JSON файл."""
    
    # START_BLOCK_VALIDATE_INPUT: [Валидация входных данных]
    logger.debug(f"[ConfigSave][IMP:4][save_config][VALIDATE_INPUT][Params] Сохранение конфигурации: {config_data} [INFO]")
    
    required_keys = {"a", "c", "x_min", "x_max"}
    if not required_keys.issubset(config_data.keys()):
        missing_keys = required_keys - set(config_data.keys())
        logger.error(f"[ConfigSave][IMP:10][save_config][VALIDATE_INPUT][ValidationError] Неверная структура данных. Отсутствуют ключи: {missing_keys}. Local vars: config_data={config_data} [FATAL]")
        raise ValueError(f"Некорректная структура конфигурации. Отсутствуют ключи: {missing_keys}")
    # END_BLOCK_VALIDATE_INPUT
    
    # START_BLOCK_WRITE_FILE: [Запись данных в файл]
    try:
        # Создаем родительскую директорию, если она не существует
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
        
        logger.info(f"[ConfigSave][IMP:7][save_config][WRITE_FILE][FileWrite] Конфигурация успешно сохранена в {config_path} [SUCCESS]")
        
    except Exception as e:
        logger.critical(f"[ConfigSave][IMP:10][save_config][WRITE_FILE][ExceptionEnrichment] Ошибка при записи файла. Local vars: config_path={config_path}, config_data={config_data}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_WRITE_FILE
# END_FUNCTION_save_config
