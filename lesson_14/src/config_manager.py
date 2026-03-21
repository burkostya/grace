# FILE:lesson_14/src/config_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление конфигурацией приложения через JSON файл.
# SCOPE:Чтение и сохранение параметров (функция, диапазон x, количество точек).
# INPUT:Путь к файлу конфигурации.
# OUTPUT:Словарь с параметрами или сохранение в файл.
# KEYWORDS:DOMAIN(Config); CONCEPT(State Management); TECH(Python, JSON)
# LINKS:USES_API(json)
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется JSON вместо YAML или INI?
# A: JSON - стандартный формат для конфигураций в Python, простой и широко поддерживается.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание менеджера конфигурации.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# CLASS[10][Менеджер конфигурации] => ConfigManager
# END_MODULE_MAP
#
# START_USE_CASES:
# - [ConfigManager]:User -> Load/Save Config -> Configuration State
# END_USE_CASES

import json
import logging
import os

logger = logging.getLogger("lesson_14.config_manager")

# START_BLOCK_DEFAULT_CONFIG: [Дефолтная конфигурация]
DEFAULT_CONFIG = {
    "function_type": "sin",
    "x_start": 0.0,
    "x_end": 6.28,  # 2π
    "num_points": 100
}
# END_BLOCK_DEFAULT_CONFIG

# START_CLASS_ConfigManager
class ConfigManager:
    """
    Класс для управления конфигурацией приложения. 
    Предоставляет методы для загрузки и сохранения параметров в JSON файл.
    """
    
    def __init__(self, config_path: str = "lesson_14/config.json"):
        self.config_path = config_path
        self._ensure_config_file()
        logger.info(f"[Config][IMP:7][ConfigManager][__init__][Init] Конфигурация инициализирована: {config_path} [SUCCESS]")
    
    def _ensure_config_file(self):
        """Создает файл конфигурации, если его нет."""
        if not os.path.exists(self.config_path):
            self.save_config(DEFAULT_CONFIG)
            logger.debug(f"[Config][IMP:4][ConfigManager][ENSURE_FILE] Создан новый файл конфигурации: {self.config_path}")
    
    # START_FUNCTION_load_config
    # START_CONTRACT:
    # PURPOSE:Загрузка конфигурации из файла.
    # INPUTS:Нет
    # OUTPUTS: 
    # - dict -Словарь с параметрами конфигурации
    # SIDE_EFFECTS:Чтение файла, если не существует - создание дефолтной конфигурации.
    # KEYWORDS:PATTERN(Data Access); CONCEPT(Configuration)
    # COMPLEXITY_SCORE:3
    # END_CONTRACT
    def load_config(self) -> dict:
        """
        Загружает конфигурацию из JSON файла. 
        Если файл не существует, создает его с дефолтными значениями.
        """
        # START_BLOCK_READ_FILE: [Чтение файла конфигурации]
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                logger.debug(f"[Config][IMP:4][ConfigManager][LOAD_CONFIG] Конфигурация загружена из файла [INFO]")
                return config
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.warning(f"[Config][IMP:6][ConfigManager][LOAD_CONFIG][Fallback] Ошибка чтения, используем дефолтную конфигурацию: {e} [WARN]")
            return DEFAULT_CONFIG.copy()
        # END_BLOCK_READ_FILE
    
    # START_FUNCTION_save_config
    # START_CONTRACT:
    # PURPOSE:Сохранение конфигурации в файл.
    # INPUTS: 
    # - dict =>config: Словарь с параметрами конфигурации
    # OUTPUTS: 
    # - bool -True при успешном сохранении
    # SIDE_EFFECTS:Запись в файл, создание директории если нужно.
    # KEYWORDS:PATTERN(Data Access); CONCEPT(Configuration)
    # COMPLEXITY_SCORE:3
    # END_CONTRACT
    def save_config(self, config: dict) -> bool:
        """
        Сохраняет конфигурацию в JSON файл. 
        Создает директорию, если она не существует.
        """
        # START_BLOCK_CREATE_DIR: [Создание директории]
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        # END_BLOCK_CREATE_DIR
        
        # START_BLOCK_WRITE_FILE: [Запись конфигурации в файл]
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
                logger.info(f"[Config][IMP:8][ConfigManager][SAVE_CONFIG] Конфигурация сохранена: {len(config)} параметров [SUCCESS]")
                return True
        except Exception as e:
            logger.error(f"[Config][IMP:10][ConfigManager][SAVE_CONFIG] Ошибка сохранения: {e} [FAIL]")
            return False
        # END_BLOCK_WRITE_FILE

# END_CLASS_ConfigManager
