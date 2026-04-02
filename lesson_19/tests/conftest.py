# FILE: lesson_19/tests/conftest.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Конфигурация pytest и Anti-Loop Protocol.
# SCOPE: Управление счетчиком попыток, фикстуры для тестов.
# INPUT: События pytest.
# OUTPUT: Телеметрия и защита от зацикливания.
# KEYWORDS: [DOMAIN(8): Testing; CONCEPT(7): AntiLoop; TECH(9): Pytest]
# END_MODULE_CONTRACT

import pytest
import json
import os
import logging

COUNTER_FILE = ".test_counter_19.json"

# START_FUNCTION_pytest_sessionstart
def pytest_sessionstart(session):
    """
    Инициализация сессии: чтение счетчика попыток.
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
    
    if count >= 2:
        print("\n--- CHECKLIST ---")
        print("- Проверьте пути к БД (используйте tmp_path)")
        print("- Проверьте импорты (относительные vs абсолютные)")
        print("- Проверьте наличие dash-ag-grid в окружении")
    
    if count >= 4:
        print("\n[WARNING] Риск зацикливания! Проверьте стратегию решения.")
# END_FUNCTION_pytest_sessionstart

# START_FUNCTION_pytest_sessionfinish
def pytest_sessionfinish(session, exitstatus):
    """
    Завершение сессии: сброс счетчика при успехе.
    """
    if exitstatus == 0:
        if os.path.exists(COUNTER_FILE):
            os.remove(COUNTER_FILE)
        print("\n[ANTI-LOOP] Тесты пройдены! Счетчик сброшен.")
# END_FUNCTION_pytest_sessionfinish

@pytest.fixture
def temp_db(tmp_path):
    """
    Фикстура для временной БД.
    """
    db_file = tmp_path / "test_erp.db"
    return str(db_file)
