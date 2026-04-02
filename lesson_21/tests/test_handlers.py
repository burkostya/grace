# FILE:lesson_21/tests/test_handlers.py
# VERSION:1.1.0
# START_MODULE_CONTRACT:
# PURPOSE:Тестирование бизнес-логики ERP-прототипа (handlers.py).
# SCOPE: Поиск товаров, добавление строк, обновление количества, расчет сумм.
# INPUT:Фикстуры pytest (tmp_path, caplog).
# OUTPUT: Результаты тестов (PASSED/FAILED), LDD-траектория.
# KEYWORDS:[DOMAIN(8): Testing; CONCEPT(7): LDD; TECH(9): Pytest]
# LINKS:[USES_API(8): lesson_21.handlers]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется monkeypatch для DB_PATH?
# A: Чтобы тесты не мутировали реальную БД проекта и работали в изолированной временной папке tmp_path.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.1.0 - Добавлена фикстура setup_db для инициализации временной БД перед каждым тестом.]
# PREV_CHANGE_SUMMARY: [v1.0.0 - Создание тестов для search_items, add_line_to_invoice, update_line_qty.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Фикстура для инициализации временной БД] => setup_db
# FUNC 10[Тест поиска товаров по частичному совпадению] => test_search_items
# FUNC 10[Тест добавления товара и пересчета суммы накладной] => test_add_line_to_invoice
# FUNC 10[Тест обновления количества и пересчета итогов] => test_update_line_qty
# END_MODULE_MAP

import pytest
import logging
import lesson_21.db_manager as db_manager
from lesson_21.db_manager import init_db
from lesson_21.handlers import (
    search_items, add_line_to_invoice, update_line_qty, 
    get_invoices, get_invoice_lines, create_demo_invoice
)

@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    """
    Фикстура автоматически инициализирует временную БД перед каждым тестом.
    Использует monkeypatch для подмены пути к БД в модуле db_manager.
    """
    db_file = tmp_path / "test_erp_handlers.db"
    db_path = str(db_file)
    monkeypatch.setattr(db_manager, "DB_PATH", db_path)
    init_db(db_path)

# START_FUNCTION_test_search_items
# START_CONTRACT:
# PURPOSE:Проверка корректности поиска товаров по LIKE.
# INPUTS: caplog (pytest fixture)
# OUTPUTS: None
# KEYWORDS:[PATTERN(7): LDD; CONCEPT(8): Telemetry]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def test_search_items(caplog):
    """
    Тест проверяет, что поиск находит товары по частичному совпадению имени.
    Также проверяется наличие LDD-логов уровня IMP:9.
    """
    caplog.set_level("INFO")
    
    # START_BLOCK_EXECUTION: [Вызов поиска]
    results = search_items("Laptop")
    # END_BLOCK_EXECUTION

    # START_BLOCK_LDD_TELEMETRY: [Вывод траектории]
    print("\n--- LDD ТРАЕКТОРИЯ (IMP:7-10) ---")
    found_log = False
    for record in caplog.records:
        if "[IMP:" in record.message:
            try:
                imp_level = int(record.message.split("[IMP:")[1].split("]")[0])
                if imp_level >= 7:
                    print(record.message)
                if imp_level >= 9 and "search_items" in record.message:
                    found_log = True
            except (IndexError, ValueError):
                continue
    # END_BLOCK_LDD_TELEMETRY

    # START_BLOCK_VERIFICATION: [Проверки]
    assert len(results) > 0, "Ошибка: Поиск 'Laptop' не вернул результатов"
    assert any("Laptop Pro 15" in item['name'] for item in results), "Ошибка: Ожидаемый товар не найден"
    assert found_log, "Критическая ошибка LDD: Нет записи [IMP:9] для search_items"
    # END_BLOCK_VERIFICATION
# END_FUNCTION_test_search_items

# START_FUNCTION_test_add_line_to_invoice
# START_CONTRACT:
# PURPOSE:Проверка добавления строки и пересчета total_sum в invoices.
# INPUTS: caplog (pytest fixture)
# OUTPUTS: None
# KEYWORDS:[PATTERN(7): LDD; CONCEPT(8): Telemetry]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def test_add_line_to_invoice(caplog):
    """
    Тест создает демо-инвойс, добавляет в него товар и проверяет,
    что общая сумма инвойса обновилась корректно (qty * price).
    """
    caplog.set_level("INFO")
    
    # START_BLOCK_PREPARE: [Подготовка данных]
    inv_id = create_demo_invoice("Test Client")
    # Берем первый попавшийся товар (Laptop Pro 15, price=1200.0)
    items = search_items("Laptop Pro 15")
    item_id = items[0]['id']
    price = items[0]['price']
    qty = 2
    expected_total = price * qty
    # END_BLOCK_PREPARE

    # START_BLOCK_EXECUTION: [Добавление строки]
    success = add_line_to_invoice(inv_id, item_id, qty)
    # END_BLOCK_EXECUTION

    # START_BLOCK_VERIFICATION: [Проверка итогов]
    assert success, "Ошибка: add_line_to_invoice вернул False"
    
    invoices = get_invoices()
    target_inv = next(inv for inv in invoices if inv['id'] == inv_id)
    
    assert target_inv['total_sum'] == expected_total, f"Ошибка: Сумма {target_inv['total_sum']} != {expected_total}"
    
    lines = get_invoice_lines(inv_id)
    assert len(lines) == 1, "Ошибка: Строка не добавлена в БД"
    assert lines[0]['line_sum'] == expected_total
    # END_BLOCK_VERIFICATION

    # START_BLOCK_LDD_TELEMETRY: [Вывод траектории]
    print("\n--- LDD ТРАЕКТОРИЯ (IMP:7-10) ---")
    found_log = False
    for record in caplog.records:
        if "[IMP:" in record.message:
            try:
                imp_level = int(record.message.split("[IMP:")[1].split("]")[0])
                if imp_level >= 7:
                    print(record.message)
                if imp_level >= 9 and "add_line_to_invoice" in record.message:
                    found_log = True
            except (IndexError, ValueError):
                continue
    assert found_log, "Критическая ошибка LDD: Нет записи [IMP:9] для add_line_to_invoice"
    # END_BLOCK_LDD_TELEMETRY
# END_FUNCTION_test_add_line_to_invoice

# START_FUNCTION_test_update_line_qty
# START_CONTRACT:
# PURPOSE:Проверка обновления количества и пересчета итогов.
# INPUTS: caplog (pytest fixture)
# OUTPUTS: None
# KEYWORDS:[PATTERN(7): LDD; CONCEPT(8): Telemetry]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def test_update_line_qty(caplog):
    """
    Тест добавляет строку, затем меняет в ней количество и проверяет,
    что итоговая сумма накладной пересчиталась.
    """
    caplog.set_level("INFO")
    
    # START_BLOCK_PREPARE: [Создание строки]
    inv_id = create_demo_invoice("Update Test")
    items = search_items("Monitor")
    item_id = items[0]['id']
    price = items[0]['price']
    
    add_line_to_invoice(inv_id, item_id, 1) # 1 шт
    lines = get_invoice_lines(inv_id)
    line_id = lines[0]['line_id']
    # END_BLOCK_PREPARE

    # START_BLOCK_EXECUTION: [Обновление количества]
    new_qty = 3
    expected_total = price * new_qty
    success = update_line_qty(line_id, new_qty)
    # END_BLOCK_EXECUTION

    # START_BLOCK_VERIFICATION: [Проверка]
    assert success
    invoices = get_invoices()
    target_inv = next(inv for inv in invoices if inv['id'] == inv_id)
    assert target_inv['total_sum'] == expected_total
    # END_BLOCK_VERIFICATION

    # START_BLOCK_LDD_TELEMETRY: [Вывод траектории]
    print("\n--- LDD ТРАЕКТОРИЯ (IMP:7-10) ---")
    found_log = False
    for record in caplog.records:
        if "[IMP:" in record.message:
            try:
                imp_level = int(record.message.split("[IMP:")[1].split("]")[0])
                if imp_level >= 7:
                    print(record.message)
                if imp_level >= 9 and "update_line_qty" in record.message:
                    found_log = True
            except (IndexError, ValueError):
                continue
    assert found_log, "Критическая ошибка LDD: Нет записи [IMP:9] для update_line_qty"
    # END_BLOCK_LDD_TELEMETRY
# END_FUNCTION_test_update_line_qty
