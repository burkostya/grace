# FILE: lesson_18/src/config_manager.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Управление конфигурационным файлом config.json для сохранения параметров параболы.
# SCOPE: Чтение и запись JSON конфигурации.
# INPUT: Параметры a, c, x_min, x_max.
# OUTPUT: Словарь с параметрами.
# KEYWORDS: [DOMAIN(8): Configuration; CONCEPT(7): Persistence; TECH(9): JSON]
# LINKS: [USES_API(8): json, os]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления конфигурацией.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# CLASS 10[Класс для работы с JSON конфигом] => ConfigManager
# END_MODULE_MAP
#
# START_USE_CASES:
# - [ConfigManager]: User -> Save/Load Params -> Persistent State
# END_USE_CASES

import json
import os
import logging

logger = logging.getLogger(__name__)

# START_FUNCTION_ConfigManager
# START_CONTRACT:
# PURPOSE: Класс для управления конфигурацией приложения.
# KEYWORDS: [PATTERN(7): Singleton-like]
# COMPLEXITY_SCORE: 3
# END_CONTRACT
class ConfigManager:
    """
    Класс ConfigManager обеспечивает сохранение и загрузку параметров параболы
    в файл config.json. Это позволяет сохранять состояние приложения между запусками.
    """

    def __init__(self, config_path: str = "lesson_18/config.json"):
        self.config_path = config_path
        self.default_config = {
            "a": 1.0,
            "c": 0.0,
            "x_min": -10,
            "x_max": 10
        }
        # START_BLOCK_INIT_CHECK: [Проверка наличия директории]
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        # END_BLOCK_INIT_CHECK

    # START_FUNCTION_load_config
    # START_CONTRACT:
    # PURPOSE: Загрузка конфигурации из файла.
    # INPUTS: Нет
    # OUTPUTS: 
    # - dict - Словарь с параметрами
    # COMPLEXITY_SCORE: 4
    # END_CONTRACT
    def load_config(self) -> dict:
        """
        Загружает параметры из config.json. Если файл отсутствует или поврежден,
        возвращает значения по умолчанию.
        """
        # START_BLOCK_READ_FILE: [Чтение файла конфигурации]
        if not os.path.exists(self.config_path):
            logger.info(f"[Config][IMP:7][ConfigManager][load_config][IO] Файл {self.config_path} не найден. Используем default. [INFO]")
            return self.default_config

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                logger.debug(f"[Config][IMP:5][ConfigManager][load_config][IO] Конфигурация загружена успешно. [SUCCESS]")
                return config
        except Exception as e:
            logger.error(f"[Config][IMP:10][ConfigManager][load_config][Exception] Ошибка при чтении конфига: {e}. [ERROR]")
            return self.default_config
        # END_BLOCK_READ_FILE

    # START_FUNCTION_save_config
    # START_CONTRACT:
    # PURPOSE: Сохранение конфигурации в файл.
    # INPUTS:
    # - dict => config: Словарь с параметрами
    # OUTPUTS: 
    # - bool - Статус успеха
    # COMPLEXITY_SCORE: 4
    # END_CONTRACT
    def save_config(self, config: dict) -> bool:
        """
        Сохраняет переданный словарь параметров в файл config.json.
        """
        # START_BLOCK_WRITE_FILE: [Запись файла конфигурации]
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
            logger.info(f"[BeliefState][IMP:9][ConfigManager][save_config][IO] Параметры {config} сохранены в {self.config_path}. [VALUE]")
            return True
        except Exception as e:
            logger.critical(f"[Config][IMP:10][ConfigManager][save_config][Exception] Не удалось сохранить конфиг: {e}. [FATAL]")
            return False
        # END_BLOCK_WRITE_FILE
# END_FUNCTION_ConfigManager
