# FILE: lesson_18/tests/conftest.py
# VERSION: 1.1.0
# START_MODULE_CONTRACT:
# PURPOSE: Конфигурация pytest и усиленный Anti-Loop Protocol для Lesson 18.
# SCOPE: Хуки сессии pytest, управление счетчиком попыток, вывод чек-листов.
# KEYWORDS: [DOMAIN(8): Testing; CONCEPT(7): AntiLoop; TECH(9): Pytest]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.1.0 - Усиление Anti-Loop Protocol: добавлены детальные чек-листы и предупреждения о зацикливании.]
# PREV_CHANGE_SUMMARY: [v1.0.0 - Первичное создание conftest.py.]
# END_CHANGE_SUMMARY

import pytest
import json
import os
import sys

COUNTER_FILE = ".test_counter_18.json"

# START_FUNCTION_update_test_counter
# START_CONTRACT:
# PURPOSE: Управление счетчиком неудачных попыток и вывод инструкций.
# INPUTS:
# - bool => success: Статус завершения тестов
# OUTPUTS: None
# SIDE_EFFECTS: Создает/удаляет .test_counter_18.json, выводит текст в stdout.
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def update_test_counter(success: bool):
    """
    Функция реализует Anti-Loop Protocol. При успехе (success=True) счетчик сбрасывается.
    При неудаче счетчик инкрементируется, и в консоль выводится прогрессивный набор
    инструкций и чек-листов для предотвращения повторения одних и тех же ошибок.
    """
    # START_BLOCK_RESET: [Сброс при успехе]
    if success:
        if os.path.exists(COUNTER_FILE):
            os.remove(COUNTER_FILE)
        return
    # END_BLOCK_RESET

    # START_BLOCK_INCREMENT: [Инкремент счетчика]
    count = 0
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as f:
            try:
                data = json.load(f)
                count = data.get("count", 0)
            except Exception:
                count = 0
    
    count += 1
    with open(COUNTER_FILE, 'w') as f:
        json.dump({"count": count}, f)
    # END_BLOCK_INCREMENT

    # START_BLOCK_REPORTING: [Вывод отчета Anti-Loop]
    print(f"\n\033[91m[ANTI-LOOP PROTOCOL] Попытка №{count}\033[0m")
    
    if count >= 1:
        print("\n--- 📋 CHECKLIST (General) ---")
        print("- [ ] PATHS: Используется ли tmp_path для всех файлов (DB, JSON)?")
        print("- [ ] IMPORTS: Корректны ли импорты (from lesson_18.src...)?")
        print("- [ ] LDD: Выводятся ли логи [IMP:7-10] в консоль (флаг -s)?")
        print("- [ ] ENVIRONMENT: Проверены ли версии библиотек через test_lib.py?")
    
    if count >= 3:
        print("\n--- 🔍 EXTERNAL HELP ---")
        print("[ADVICE] Вы застряли. Используйте MCP 'tavily' для поиска ошибок или 'Context 7' для документации.")
        print("Возможно, проблема в специфике Windows (пути, кодировки) или версиях Gradio/Plotly.")
    
    if count >= 4:
        print("\n--- 🧠 REFLECTION REQUIRED ---")
        print("[WARNING] ВНИМАНИЕ: Риск зацикливания! Вы применяете одну и ту же стратегию?")
        print("Попробуйте 'Суперпозицию': сформулируйте 3 альтернативных причины ошибки.")
    
    if count >= 5:
        print("\n--- 🛑 ESCALATION ---")
        print("[CRITICAL] ОБНАРУЖЕНО ЗАЦИКЛИВАНИЕ АГЕНТА. ОСТАНОВИТЕСЬ.")
        print("Сформируйте запрос оператору: 1) Описание, 2) Шаги, 3) Логи, 4) План консультации.")
        sys.exit(1) # Принудительная остановка при критическом зацикливании
    # END_BLOCK_REPORTING
# END_FUNCTION_update_test_counter

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    """Хук завершения сессии для обновления счетчика."""
    update_test_counter(exitstatus == 0)
