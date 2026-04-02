# FILE:lesson_20/tests/conftest.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Конфигурация pytest и Anti-Loop Protocol для Lesson 20.
# SCOPE:Управление счетчиком попыток и настройка логирования.
# KEYWORDS:[DOMAIN(8): Testing; CONCEPT(7): AntiLoop; TECH(9): Pytest]
# END_MODULE_CONTRACT

import pytest
import json
import os
import logging

COUNTER_FILE = ".test_counter_20.json"

# START_FUNCTION_pytest_sessionstart
def pytest_sessionstart(session):
    """
    Инициализация сессии: загрузка счетчика попыток.
    """
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as f:
            data = json.load(f)
            count = data.get("count", 0) + 1
    else:
        count = 1
    
    with open(COUNTER_FILE, 'w') as f:
        json.dump({"count": count}, f)
    
    print(f"\n[ANTI-LOOP] Попытка запуска тестов №{count}")
    
    if count >= 1:
        print("\n--- CHECKLIST ---")
        print("- Проверка путей и использование tmp_path.")
        print("- Проверка импортов (Native Import).")
        print("- Соответствие версий библиотек через test_lib.py.")
        print("- Наличие необходимых файлов данных/конфигов.")
    
    if count == 3:
        print("\n[ADVICE] Используйте MCP tavily или Context 7 для поиска решения.")
    elif count == 4:
        print("\n[WARNING] Риск зацикливания! Проведите рефлексию стратегии.")
    elif count >= 5:
        print("\n[CRITICAL] Обнаружено зацикливание! ОСТАНОВИТЕСЬ и сформируйте запрос на помощь.")

# START_FUNCTION_pytest_sessionfinish
def pytest_sessionfinish(session, exitstatus):
    """
    Завершение сессии: сброс счетчика при успехе.
    """
    if exitstatus == 0:
        if os.path.exists(COUNTER_FILE):
            os.remove(COUNTER_FILE)
        print("\n[ANTI-LOOP] Тесты пройдены! Счетчик сброшен.")

@pytest.fixture(autouse=True)
def setup_logging(caplog):
    """
    Автоматическая настройка уровня логирования для каждого теста.
    """
    caplog.set_level(logging.DEBUG, logger="lesson_20")
