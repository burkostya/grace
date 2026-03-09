# FILE: lesson_v8/src/config_manager.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Управление чтением и записью конфигурации приложения в формате JSON.
# SCOPE: Работа с файлом конфигурации config.json, загрузка и сохранение параметров параболы.
# INPUT: Путь к файлу конфигурации (опционально), словарь с параметрами для сохранения.
# OUTPUT: Словарь с параметрами конфигурации (a, c, x_min, x_max).
# KEYWORDS:[DOMAIN(8): ConfigurationManagement; CONCEPT(7): StatePersistence; TECH(9): JSON]
# LINKS:[READS_DATA_FROM(8): config.json; WRITES_DATA_TO(8): config.json]
# END_MODULE_CONTRACT
#
# START_INVARIANTS:
# - Функция load_config ВСЕГДА возвращает словарь с ключами 'a', 'c', 'x_min', 'x_max'.
# - Если файл конфигурации отсутствует, создается файл с дефолтными значениями.
# END_INVARIANTS
#
# START_RATIONALE:
# Q: Почему используется json вместо других форматов?
# A: JSON — стандартный формат для конфигураций, легко читается человеком и поддерживается нативно в Python.
# Q: Почему дефолтные значения создаются при отсутствии файла?
# A: Это обеспечивает работоспособность приложения "из коробки" без предварительной настройки.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления конфигурацией.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Загружает конфигурацию из файла или создает дефолтную] => load_config
# FUNC 10[Сохраняет конфигурацию в файл] => save_config
# END_MODULE_MAP
#
# START_USE_CASES:
# -[load_config]: Application (Startup) -> LoadConfiguration -> ConfigLoaded
# -[save_config]: UI (UserAction) -> SaveConfiguration -> ConfigPersisted
# END_USE_CASES

import json
import logging
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Путь к файлу конфигурации относительно директории урока
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config.json")

# Дефолтные значения конфигурации
DEFAULT_CONFIG = {
    "a": 1.0,
    "c": 0.0,
    "x_min": -10.0,
    "x_max": 10.0
}


# START_FUNCTION_load_config
# START_CONTRACT:
# PURPOSE: Загружает конфигурацию из JSON файла. Если файл отсутствует, создает его с дефолтными значениями.
# INPUTS: 
# - config_path => config_path: str (путь к файлу конфигурации, опционально)
# OUTPUTS: 
# - dict - Словарь с параметрами конфигурации (ключи: 'a', 'c', 'x_min', 'x_max')
# SIDE_EFFECTS: Создает файл конфигурации с дефолтными значениями, если он отсутствует.
# KEYWORDS:[PATTERN(8): Singleton; CONCEPT(7): LazyInitialization]
# COMPLEXITY_SCORE: 4[Низкая сложность: проверка файла, чтение JSON, обработка исключений.]
# END_CONTRACT
def load_config(config_path: str = CONFIG_FILE) -> Dict[str, Any]:
    """
    Функция выполняет загрузку конфигурации приложения из JSON файла.
    При отсутствии файла конфигурации автоматически создает его с дефолтными значениями параметров.
    Это обеспечивает отказоустойчивость приложения и возможность работы без предварительной настройки.
    Функция использует безопасный подход к работе с файловой системой и обрабатывает возможные ошибки.
    """
    
    # START_BLOCK_CHECK_FILE_EXISTENCE: [Проверка существования файла конфигурации]
    if not os.path.exists(config_path):
        logger.warning(f"[ConfigMissing][IMP:7][load_config][CHECK_FILE_EXISTENCE][FileCheck] Файл конфигурации не найден: {config_path}. Будет создан дефолтный конфиг. [WARN]")
        save_config(DEFAULT_CONFIG, config_path)
        logger.info(f"[ConfigCreated][IMP:8][load_config][CHECK_FILE_EXISTENCE][FileOperation] Создан дефолтный файл конфигурации: {config_path} [SUCCESS]")
        return DEFAULT_CONFIG.copy()
    # END_BLOCK_CHECK_FILE_EXISTENCE
    
    # START_BLOCK_READ_CONFIG_FILE: [Чтение и парсинг JSON файла]
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        logger.info(f"[ConfigLoaded][IMP:8][load_config][READ_CONFIG_FILE][FileOperation] Конфигурация успешно загружена из: {config_path} [SUCCESS]")
        
        # START_BLOCK_VALIDATE_CONFIG_KEYS: [Проверка наличия всех необходимых ключей]
        required_keys = ['a', 'c', 'x_min', 'x_max']
        for key in required_keys:
            if key not in config:
                logger.error(f"[InvalidConfig][IMP:9][load_config][VALIDATE_CONFIG_KEYS][ValidationError] Отсутствует обязательный ключ: {key} [ERROR]")
                config[key] = DEFAULT_CONFIG[key]
        # END_BLOCK_VALIDATE_CONFIG_KEYS
        
        return config
        
    except json.JSONDecodeError as e:
        logger.critical(f"[JSONDecodeError][IMP:10][load_config][READ_CONFIG_FILE][ExceptionEnrichment] Ошибка парсинга JSON. Local vars: config_path={config_path}. Err: {e} [FATAL]")
        raise
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][load_config][READ_CONFIG_FILE][ExceptionEnrichment] Неожиданная ошибка при чтении конфига. Local vars: config_path={config_path}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_READ_CONFIG_FILE
# END_FUNCTION_load_config


# START_FUNCTION_save_config
# START_CONTRACT:
# PURPOSE: Сохраняет конфигурацию в JSON файл.
# INPUTS: 
# - config => config: Dict[str, Any] (словарь с параметрами конфигурации)
# - config_path => config_path: str (путь к файлу конфигурации, опционально)
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Записывает конфигурацию в файл, перезаписывая предыдущее содержимое.
# KEYWORDS:[PATTERN(6): Persistence; CONCEPT(7): StateSerialization]
# COMPLEXITY_SCORE: 3[Низкая сложность: сериализация в JSON и запись файла.]
# END_CONTRACT
def save_config(config: Dict[str, Any], config_path: str = CONFIG_FILE) -> None:
    """
    Функция выполняет сохранение конфигурации приложения в JSON файл.
    Конфигурация сериализуется в JSON формат и записывается в указанный файл.
    При успешной записи старое содержимое файла полностью заменяется новым.
    Функция обеспечивает сохранение состояния приложения между запусками.
    """
    
    # START_BLOCK_VALIDATE_INPUT: [Проверка входных данных]
    if not isinstance(config, dict):
        logger.error(f"[InvalidInput][IMP:9][save_config][VALIDATE_INPUT][TypeError] config должен быть словарем. Получен тип: {type(config)} [ERROR]")
        raise TypeError("config должен быть словарем")
    
    required_keys = ['a', 'c', 'x_min', 'x_max']
    for key in required_keys:
        if key not in config:
            logger.error(f"[InvalidInput][IMP:9][save_config][VALIDATE_INPUT][ValueError] Отсутствует обязательный ключ: {key} [ERROR]")
            raise ValueError(f"Отсутствует обязательный ключ: {key}")
    # END_BLOCK_VALIDATE_INPUT
    
    # START_BLOCK_WRITE_CONFIG_FILE: [Сериализация и запись в файл]
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        logger.info(f"[ConfigSaved][IMP:8][save_config][WRITE_CONFIG_FILE][FileOperation] Конфигурация успешно сохранена в: {config_path} [SUCCESS]")
        
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][save_config][WRITE_CONFIG_FILE][ExceptionEnrichment] Ошибка при сохранении конфига. Local vars: config_path={config_path}, config={config}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_WRITE_CONFIG_FILE
# END_FUNCTION_save_config
