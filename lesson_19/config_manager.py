# FILE: lesson_19/config_manager.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Управление конфигурацией и справочниками ERP-прототипа.
# SCOPE: Чтение/запись config.json, хранение справочника товаров.
# INPUT: Путь к файлу конфигурации.
# OUTPUT: Параметры системы и справочники.
# KEYWORDS: [DOMAIN(8): Config; CONCEPT(7): JSON; TECH(9): Settings]
# LINKS: [USES_API(8): json]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание менеджера конфигурации со справочником товаров.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Получение справочника товаров] => get_products
# FUNC 8[Загрузка конфигурации] => load_config
# END_MODULE_MAP

import json
import os
import logging

logger = logging.getLogger(__name__)

# START_FUNCTION_get_products
# START_CONTRACT:
# PURPOSE: Возвращает справочник товаров для генерации и выбора.
# INPUTS: None
# OUTPUTS: 
# - dict - Словарь {название: цена}
# KEYWORDS: [PATTERN(6): Dictionary; CONCEPT(8): MasterData]
# COMPLEXITY_SCORE: 2
# END_CONTRACT
def get_products() -> dict:
    """
    Возвращает захардкоженный справочник товаров.
    """
    # START_BLOCK_PRODUCTS: [Справочник товаров]
    products = {
        "Ноутбук": 50000.0,
        "Монитор": 15000.0,
        "Клавиатура": 2500.0,
        "Мышь": 1200.0,
        "Принтер": 8000.0,
        "Сканер": 6000.0,
        "Колонки": 3500.0,
        "Веб-камера": 4500.0
    }
    logger.debug(f"[Config][IMP:4][get_products][FETCH] Справочник товаров получен [SUCCESS]")
    return products
    # END_BLOCK_PRODUCTS
# END_FUNCTION_get_products

# START_FUNCTION_load_config
# START_CONTRACT:
# PURPOSE: Загрузка настроек из config.json или создание дефолтных.
# INPUTS:
# - str => config_path: Путь к файлу
# OUTPUTS:
# - dict - Настройки
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def load_config(config_path: str) -> dict:
    """
    Загружает конфигурацию. Если файла нет, создает его с дефолтными значениями.
    """
    # START_BLOCK_LOAD: [Загрузка или создание]
    default_config = {
        "db_path": "lesson_19/erp_base.db",
        "log_path": "lesson_19/app_19.log",
        "mock_invoice_count": 5
    }
    
    if not os.path.exists(config_path):
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        logger.info(f"[Config][IMP:7][load_config][CREATE] Создан дефолтный конфиг: {config_path} [SUCCESS]")
        return default_config
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.debug(f"[Config][IMP:5][load_config][LOAD] Конфиг загружен [SUCCESS]")
        return config
    except Exception as e:
        logger.error(f"[Config][IMP:10][load_config][ERROR] Ошибка чтения конфига: {e} [FATAL]")
        return default_config
    # END_BLOCK_LOAD
# END_FUNCTION_load_config
