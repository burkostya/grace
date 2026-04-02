# FILE: tests/conftest.py
# VERSION: 1.2.0
# START_MODULE_CONTRACT:
# PURPOSE: Глобальная конфигурация pytest и реализация Anti-Loop Protocol.
# SCOPE: Хуки сессии, управление счетчиком попыток, чек-листы.
# KEYWORDS:[PATTERN(9): AntiLoop; CONCEPT(8): Infrastructure]
# END_MODULE_CONTRACT

import pytest
import json
import os

COUNTER_FILE = ".test_counter.json"


# START_FUNCTION_pytest_sessionstart
def pytest_sessionstart(session):
    """Инициализация сессии и вывод счетчика попыток."""
    count = 0
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, "r") as f:
                data = json.load(f)
                count = data.get("attempts", 0)
        except (json.JSONDecodeError, ValueError):
            count = 0

    if count > 0:
        print(f"\n[ANTI-LOOP][IMP:10] ОБНАРУЖЕН ПОВТОРНЫЙ ЗАПУСК. ПОПЫТКА: {count + 1}")
        print("--- CHECKLIST ---")
        print("1. Проверьте использование tmp_path для всех файлов (БД, конфиги).")
        print("2. Проверьте импорты модулей (Native Import vs Subprocess).")
        print("3. Соответствие версий библиотек через test_lib.py.")
        if count >= 3:
            print(
                "[IMP:10] ВНИМАНИЕ: Используйте Context 7 или Tavily для поиска решения!"
            )
        if count >= 4:
            print(
                "[IMP:10] ВНИМАНИЕ: Риск зацикливания! Сделайте паузу и проведите рефлексию (Суперпозиция)."
            )
        if count >= 5:
            print(
                "[FATAL][IMP:10] КРИТИЧЕСКАЯ ОШИБКА: Обнаружено зацикливание! ОСТАНОВИТЕСЬ."
            )


# END_FUNCTION_pytest_sessionstart


# START_FUNCTION_pytest_sessionfinish
def pytest_sessionfinish(session, exitstatus):
    """Обновление или сброс счетчика попыток."""
    # Сброс счетчика только при 100% успехе
    if exitstatus == 0:
        if os.path.exists(COUNTER_FILE):
            os.remove(COUNTER_FILE)
            print("\n[Anti-Loop][IMP:10] Тесты пройдены! Счетчик сброшен. [SUCCESS]")
    else:
        attempts = 0
        if os.path.exists(COUNTER_FILE):
            try:
                with open(COUNTER_FILE, "r") as f:
                    data = json.load(f)
                    attempts = data.get("attempts", 0)
            except (json.JSONDecodeError, ValueError):
                attempts = 0

        with open(COUNTER_FILE, "w") as f:
            json.dump({"attempts": attempts + 1}, f)
        print(
            f"\n[Anti-Loop][IMP:10] Тесты провалены. Попытка {attempts + 1} зафиксирована. [FAIL]"
        )


# END_FUNCTION_pytest_sessionfinish
