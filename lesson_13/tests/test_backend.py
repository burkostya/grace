# FILE:lesson_13/tests/test_backend.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Тестирование бэкенд-логики (Config, DB, Math) с проверкой LDD логов.
# SCOPE:Unit-тесты для ConfigManager, DatabaseManager и calculate_parabola.
# INPUT:Модули src.
# OUTPUT:Отчет pytest и вывод логов IMP:7-10.
# KEYWORDS:DOMAIN(Testing); CONCEPT(Unit Test); TECH(pytest, caplog)
# LINKS:LINKS_TO_SPECIFICATION(GOAL_TESTING_LDD)
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание комплексных тестов бэкенда.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC[10][Тест ConfigManager] => test_config_manager
# FUNC[10][Тест DatabaseManager] => test_database_manager
# FUNC[10][Тест Parabola Logic] => test_parabola_logic
# END_MODULE_MAP

import pytest
import os
import logging
from lesson_13.src.config_manager import ConfigManager
from lesson_13.src.database_manager import DatabaseManager
from lesson_13.src.parabola_logic import calculate_parabola_points

# START_FUNCTION_setup_logging_for_tests
# START_CONTRACT:
# PURPOSE:Настройка вывода логов в консоль для pytest.
# END_CONTRACT
@pytest.fixture(autouse=True)
def setup_caplog(caplog):
    """Фикстура для настройки уровня логирования в тестах."""
    caplog.set_level(logging.DEBUG)
# END_FUNCTION_setup_logging_for_tests

# START_FUNCTION_test_config_manager
# START_CONTRACT:
# PURPOSE:Проверка загрузки и сохранения конфигурации.
# COMPLEXITY_SCORE:5
# END_CONTRACT
def test_config_manager(tmp_path, caplog):
    """
    Тестирует ConfigManager: создание дефолтного конфига, 
    сохранение изменений и повторную загрузку.
    """
    # START_BLOCK_TEST_CONFIG: [Логика теста конфига]
    config_file = tmp_path / "test_config.json"
    cm = ConfigManager(str(config_file))
    
    # 1. Load default
    config = cm.load_config()
    assert config["a"] == 1.0
    
    # 2. Save new
    cm.save_config({"a": 5.0, "c": 10.0})
    
    # 3. Reload
    cm2 = ConfigManager(str(config_file))
    config2 = cm2.load_config()
    assert config2["a"] == 5.0
    assert config2["c"] == 10.0
    
    # Проверка LDD логов (IMP:7-10)
    important_logs = [rec.message for rec in caplog.records if "[IMP:" in rec.message and any(f"IMP:{i}" in rec.message for i in range(7, 11))]
    print("\n--- IMPORTANT CONFIG LOGS ---")
    for log in important_logs:
        print(log)
    assert len(important_logs) > 0
    # END_BLOCK_TEST_CONFIG
# END_FUNCTION_test_config_manager

# START_FUNCTION_test_database_manager
# START_CONTRACT:
# PURPOSE:Проверка работы с SQLite.
# COMPLEXITY_SCORE:6
# END_CONTRACT
def test_database_manager(tmp_path, caplog):
    """
    Тестирует DatabaseManager: инициализацию, сохранение точек
    и их корректное извлечение.
    """
    # START_BLOCK_TEST_DB: [Логика теста БД]
    db_file = tmp_path / "test_parabola.db"
    db = DatabaseManager(str(db_file))
    
    # 1. Init
    assert db.init_db() is True
    
    # 2. Save
    points = [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0)]
    assert db.save_points(points) is True
    
    # 3. Get
    saved_points = db.get_points()
    assert len(saved_points) == 3
    assert saved_points[1] == (1.0, 1.0)
    
    # Проверка LDD логов (IMP:7-10)
    important_logs = [rec.message for rec in caplog.records if "[IMP:" in rec.message and any(f"IMP:{i}" in rec.message for i in range(7, 11))]
    print("\n--- IMPORTANT DB LOGS ---")
    for log in important_logs:
        print(log)
    assert len(important_logs) > 0
    # END_BLOCK_TEST_DB
# END_FUNCTION_test_database_manager

# START_FUNCTION_test_parabola_logic
# START_CONTRACT:
# PURPOSE:Проверка математических расчетов.
# COMPLEXITY_SCORE:4
# END_CONTRACT
def test_parabola_logic(caplog):
    """
    Тестирует calculate_parabola_points: точность формулы и обработку ошибок.
    """
    # START_BLOCK_TEST_MATH: [Логика теста математики]
    # 1. Normal case: y = 1*x^2 + 0*x + 0
    points = calculate_parabola_points(1.0, 0.0, 0.0, -2, 2, 9)
    # x: -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2 (9 points)
    assert len(points) == 9
    assert points[0] == (-2.0, 4.0)
    assert points[4] == (0.0, 0.0)
    
    # 2. Error case: x_min > x_max
    empty_points = calculate_parabola_points(1.0, 0.0, 0.0, 10, 5, 10)
    assert len(empty_points) == 0
    
    # Проверка LDD логов (IMP:7-10)
    important_logs = [rec.message for rec in caplog.records if "[IMP:" in rec.message and any(f"IMP:{i}" in rec.message for i in range(7, 11))]
    print("\n--- IMPORTANT MATH LOGS ---")
    for log in important_logs:
        print(log)
    assert len(important_logs) > 0
    # END_BLOCK_TEST_MATH
# END_FUNCTION_test_parabola_logic
