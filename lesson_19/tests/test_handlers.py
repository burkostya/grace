# FILE: lesson_19/tests/test_handlers.py
# VERSION: 1.0.1
# START_MODULE_CONTRACT:
# PURPOSE: Тестирование чистой бизнес-логики ERP-прототипа.
# SCOPE: Проверка генерации, получения и обновления данных.
# INPUT: Временная БД.
# OUTPUT: Результаты тестов (PASSED/FAILED).
# KEYWORDS: [DOMAIN(8): Testing; CONCEPT(7): UnitTests; TECH(9): Pytest]
# END_MODULE_CONTRACT

import pytest
import os
import sys

# Добавляем корень проекта в sys.path для корректных импортов
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from lesson_19.db_manager import init_db, fetch_query
from lesson_19.handlers import generate_mock_data, get_invoices, get_invoice_lines, update_invoice_lines

# START_FUNCTION_test_db_initialization
def test_db_initialization(temp_db):
    """
    Проверка создания таблиц.
    """
    init_db(temp_db)
    tables = fetch_query(temp_db, "SELECT name FROM sqlite_master WHERE type='table'")
    table_names = [t[0] for t in tables]
    assert "invoices" in table_names
    assert "invoice_lines" in table_names
# END_FUNCTION_test_db_initialization

# START_FUNCTION_test_generate_mock_data
# START_CONTRACT:
# PURPOSE: Проверка генерации 5 накладных и верификация траектории через LDD логи.
# INPUTS: temp_db (fixture), caplog (fixture)
# KEYWORDS: [PATTERN(7): LDD; CONCEPT(8): Telemetry]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def test_generate_mock_data(temp_db, caplog):
    """
    Тест проверяет не только количество созданных записей, но и
    верифицирует траекторию работы алгоритма через анализ логов IMP:7-10.
    """
    # START_BLOCK_EXECUTION: [Вызов генерации данных]
    init_db(temp_db)
    generate_mock_data(temp_db)
    
    invoices = get_invoices(temp_db)
    assert len(invoices) == 5
    # END_BLOCK_EXECUTION
    
    # START_BLOCK_LDD_VERIFICATION: [Проверка траектории через логи]
    print("\n--- LDD TELEMETRY (IMP:7-10) ---")
    found_cleanup = False
    found_generate = False
    
    for record in caplog.records:
        # Фильтруем и выводим важные логи для "принудительного чтения"
        if any(f"[IMP:{i}]" in record.message for i in range(7, 11)):
            print(record.message)
            
            if "[IMP:7]" in record.message and "CLEANUP" in record.message:
                found_cleanup = True
            if "[IMP:9]" in record.message and "generate_mock_data" in record.message:
                found_generate = True
                
    # Защита от Иллюзий: верификация ключевых этапов траектории
    assert found_cleanup, "LDD Error: Не найдена запись об очистке БД [IMP:7]"
    assert found_generate, "LDD Error: Не найдена финальная запись генерации [IMP:9]"
    # END_BLOCK_LDD_VERIFICATION
# END_FUNCTION_test_generate_mock_data

# START_FUNCTION_test_update_invoice_lines
def test_update_invoice_lines(temp_db):
    """
    Проверка обновления строк и пересчета суммы.
    """
    init_db(temp_db)
    generate_mock_data(temp_db)
    
    # Берем первую накладную
    inv = get_invoices(temp_db)[0]
    inv_id = inv["id"]
    lines = get_invoice_lines(temp_db, inv_id)
    
    # Меняем количество в первой строке
    lines[0]["quantity"] = 10
    update_invoice_lines(temp_db, inv_id, lines)
    
    # Проверяем пересчет
    updated_inv = fetch_query(temp_db, "SELECT total_amount FROM invoices WHERE id = ?", (inv_id,))[0][0]
    updated_lines = get_invoice_lines(temp_db, inv_id)
    
    expected_total = sum(l["amount"] for l in updated_lines)
    assert updated_inv == expected_total
    assert updated_lines[0]["quantity"] == 10
# END_FUNCTION_test_update_invoice_lines
