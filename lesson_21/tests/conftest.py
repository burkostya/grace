# FILE:lesson_21/tests/conftest.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Конфигурация pytest и Anti-Loop Protocol для Урока 21.
# SCOPE: Управление счетчиком попыток, хуки сессии.
# END_MODULE_CONTRACT

import pytest
import json
import os

COUNTER_FILE = ".test_counter_21.json"

def update_test_counter(success: bool):
    """
    Обновляет счетчик попыток в файле. Сбрасывает в 0 при успехе.
    """
    count = 0
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            try:
                data = json.load(f)
                count = data.get("count", 0)
            except:
                pass
    
    if success:
        count = 0
    else:
        count += 1
        
    with open(COUNTER_FILE, "w") as f:
        json.dump({"count": count}, f)
    return count

def pytest_sessionstart(session):
    """
    Вывод статуса попыток при старте.
    """
    count = 0
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            try:
                count = json.load(f).get("count", 0)
            except:
                pass
    
    if count > 0:
        print(f"\n\n[ANTI-LOOP] ПОПЫТКА №{count}")
        print("CHECKLIST:")
        print("- Проверьте пути к БД (используйте tmp_path)")
        print("- Проверьте SQL синтаксис (CREATE TABLE, INSERT)")
        print("- Проверьте наличие всех 3 таблиц")
        print("- Проверьте LDD логирование [IMP:7-10]")
        
        if count >= 3:
            print("СОВЕТ: Используйте MCP Context7 для уточнения синтаксиса sqlite3.")
        if count >= 4:
            print("ВНИМАНИЕ: Риск зацикливания! Проверьте логику инициализации.")

def pytest_sessionfinish(session, exitstatus):
    """
    Обновление счетчика по итогам сессии.
    """
    update_test_counter(exitstatus == 0)
