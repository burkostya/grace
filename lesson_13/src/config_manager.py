# FILE:lesson_13/src/config_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление конфигурацией и состоянием приложения через JSON файл.
# SCOPE:Загрузка, сохранение и предоставление доступа к параметрам конфигурации.
# INPUT:Путь к файлу config.json.
# OUTPUT:Объект конфигурации (словарь).
# KEYWORDS:DOMAIN(State Management); CONCEPT(JSON Config); TECH(Python, json, logging)
# LINKS:USES_API(json); USES_API(logging)
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется класс ConfigManager?
# A: Для инкапсуляции логики работы с файловой системой и обеспечения единой точки доступа к настройкам.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления конфигурацией.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# CLASS[10][Класс для управления конфигурацией] => ConfigManager
# END_MODULE_MAP
#
# START_USE_CASES:
# - [ConfigManager]:System -> Load/Save Config -> Application State Synchronized
# END_USE_CASES

import json
import os
import logging

# Настройка логирования для модуля
logger = logging.getLogger(__name__)
log_file = "lesson_13/app_13.log"
if not os.path.exists(os.path.dirname(log_file)):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

class ConfigManager:
    """
    Класс ConfigManager отвечает за чтение и запись конфигурационного файла приложения.
    Он обеспечивает значения по умолчанию, если файл отсутствует, и гарантирует,
    что изменения состояния сохраняются между сессиями работы приложения.
    """

    def __init__(self, config_path: str = "lesson_13/config.json"):
        # START_BLOCK_INIT: [Инициализация путей и значений по умолчанию]
        self.config_path = config_path
        self.default_config = {
            "a": 1.0,
            "c": 0.0,
            "x_min": -10,
            "x_max": 10,
            "db_path": "lesson_13/parabola.db"
        }
        self.config = self.default_config.copy()
        logger.debug(f"[Config][IMP:4][ConfigManager][INIT][Flow] Инициализация ConfigManager с путем: {config_path} [SUCCESS]")
        # END_BLOCK_INIT

    # START_FUNCTION_load_config
    # START_CONTRACT:
    # PURPOSE:Загрузка конфигурации из файла.
    # INPUTS: 
    # - Нет
    # OUTPUTS: 
    # - dict -Словарь с параметрами конфигурации
    # SIDE_EFFECTS: Обновляет self.config
    # KEYWORDS:PATTERN(Singleton-like); CONCEPT(File I/O)
    # COMPLEXITY_SCORE:3
    # END_CONTRACT
    def load_config(self) -> dict:
        """
        Загружает данные из JSON файла. Если файл не найден, использует значения по умолчанию.
        В случае ошибки парсинга JSON также возвращает дефолтные значения.
        """
        # START_BLOCK_LOAD_FILE: [Чтение файла и десериализация]
        if not os.path.exists(self.config_path):
            logger.info(f"[Config][IMP:7][ConfigManager][load_config][IO] Файл не найден. Используются значения по умолчанию. [INFO]")
            self.config = self.default_config.copy()
            return self.config

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            logger.info(f"[Config][IMP:8][ConfigManager][load_config][IO] Конфигурация успешно загружена из {self.config_path} [SUCCESS]")
        except Exception as e:
            logger.error(f"[Config][IMP:10][ConfigManager][load_config][Exception] Ошибка при загрузке конфига: {e}. Local vars: path={self.config_path} [FATAL]")
            self.config = self.default_config.copy()
        # END_BLOCK_LOAD_FILE

        return self.config
    # END_FUNCTION_load_config

    # START_FUNCTION_save_config
    # START_CONTRACT:
    # PURPOSE:Сохранение текущей конфигурации в файл.
    # INPUTS: 
    # - dict =>new_config: Новые параметры (опционально)
    # OUTPUTS: 
    # - bool -Успешность операции
    # SIDE_EFFECTS: Перезаписывает файл на диске
    # KEYWORDS:CONCEPT(Persistence)
    # COMPLEXITY_SCORE:3
    # END_CONTRACT
    def save_config(self, new_config: dict = None) -> bool:
        """
        Сохраняет переданный или текущий словарь конфигурации в JSON файл.
        Обеспечивает создание директории, если она отсутствует.
        """
        # START_BLOCK_SAVE_FILE: [Сериализация и запись на диск]
        if new_config:
            self.config.update(new_config)
            logger.debug(f"[Config][IMP:5][ConfigManager][save_config][Flow] Обновление локального стейта перед сохранением. [INFO]")

        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            logger.info(f"[BeliefState][IMP:9][ConfigManager][save_config][IO] Конфигурация сохранена в {self.config_path} [SUCCESS]")
            return True
        except Exception as e:
            logger.critical(f"[SystemError][IMP:10][ConfigManager][save_config][Exception] Не удалось сохранить конфиг: {e} [FATAL]")
            return False
        # END_BLOCK_SAVE_FILE
    # END_FUNCTION_save_config
