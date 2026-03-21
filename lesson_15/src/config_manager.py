# FILE: lesson_15/src/config_manager.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Управление конфигурацией приложения (чтение/запись JSON).
# SCOPE: State Management, Persistence.
# INPUT: Путь к файлу config.json.
# OUTPUT: Словарь с параметрами (a, c, x_min, x_max).
# KEYWORDS: [DOMAIN(8): Configuration; TECH(7): JSON; CONCEPT(9): Persistence]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание модуля управления конфигурацией.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# CLASS 10[Класс для работы с конфигурацией] => ConfigManager
# END_MODULE_MAP

import json
import os
import logging

logger = logging.getLogger(__name__)

# START_FUNCTION_ConfigManager
class ConfigManager:
    """
    Класс ConfigManager обеспечивает централизованное управление состоянием приложения,
    сохраняя и загружая параметры генерации параболы из JSON файла.
    """
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.default_config = {
            "a": 1.0,
            "c": 0.0,
            "x_min": -10.0,
            "x_max": 10.0
        }

    # START_FUNCTION_load
    # START_CONTRACT:
    # PURPOSE: Загрузка конфигурации из файла.
    # INPUTS: Нет
    # OUTPUTS: 
    # - dict - Параметры конфигурации.
    # COMPLEXITY_SCORE: 3
    # END_CONTRACT
    def load(self) -> dict:
        """Загружает конфиг или возвращает дефолтный, если файл отсутствует."""
        # START_BLOCK_LOAD_LOGIC: [Чтение файла]
        if not os.path.exists(self.config_path):
            logger.info(f"[Config][IMP:7][ConfigManager][load][FileCheck] Файл не найден, используем дефолт. [INFO]")
            return self.default_config
        
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                logger.debug(f"[Config][IMP:5][ConfigManager][load][IO] Конфиг загружен: {config} [SUCCESS]")
                return config
        except Exception as e:
            logger.error(f"[Config][IMP:10][ConfigManager][load][Error] Ошибка чтения конфига: {e} [FATAL]")
            return self.default_config
        # END_BLOCK_LOAD_LOGIC

    # START_FUNCTION_save
    # START_CONTRACT:
    # PURPOSE: Сохранение конфигурации в файл.
    # INPUTS: 
    # - dict => config: Параметры для сохранения.
    # OUTPUTS: 
    # - bool - Успешность операции.
    # COMPLEXITY_SCORE: 3
    # END_CONTRACT
    def save(self, config: dict) -> bool:
        """Сохраняет переданный словарь в JSON файл."""
        # START_BLOCK_SAVE_LOGIC: [Запись в файл]
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)
            logger.info(f"[BeliefState][IMP:9][ConfigManager][save][IO] Конфиг успешно сохранен. [VALUE]")
            return True
        except Exception as e:
            logger.error(f"[Config][IMP:10][ConfigManager][save][Error] Ошибка записи конфига: {e} [FATAL]")
            return False
        # END_BLOCK_SAVE_LOGIC
# END_FUNCTION_ConfigManager
