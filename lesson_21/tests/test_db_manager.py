# FILE:lesson_21/tests/test_db_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Тестирование db_manager.py: инициализация БД и получение соединений.
# SCOPE: Проверка создания таблиц, наполнения справочника, LDD-телеметрия.
# END_MODULE_CONTRACT

import pytest
import sqlite3
import os
import logging
from lesson_21.db_manager import init_db, get_connection

# START_FUNCTION_test_db_initialization
# START_CONTRACT:
# PURPOSE:Проверка создания таблиц и наполнения справочника товаров.
# INPUTS: tmp_path (pytest fixture), caplog (pytest fixture)
# KEYWORDS:[PATTERN(7): LDD; CONCEPT(8): Telemetry]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def test_db_initialization(tmp_path, caplog):
    """
    Тест проверяет, что init_db корректно создает файл БД, 
    все 3 таблицы и наполняет справочник items 20-ю позициями.
    Также верифицируется наличие LDD-логов уровня IMP:9.
    """
    # ВАЖНО: Устанавливаем уровень перехвата логов
    caplog.set_level("INFO")
    
    # START_BLOCK_EXECUTION: [Вызов инициализации БД]
    db_file = tmp_path / "test_erp.db"
    db_path = str(db_file)
    
    init_db(db_path)
    # END_BLOCK_EXECUTION

    # START_BLOCK_LDD_TELEMETRY: [Вывод среза траектории для агента]
    found_log_schema = False
    found_log_data = False
    print("\n--- LDD ТРАЕКТОРИЯ (IMP:7-10) ---")
    for record in caplog.records:
        if "[IMP:" in record.message:
            try:
                imp_level = int(record.message.split("[IMP:")[1].split("]")[0])
                if imp_level >= 7:
                    print(record.message)
                if imp_level >= 9:
                    if "CREATE_TABLES" in record.message:
                        found_log_schema = True
                    if "POPULATE_ITEMS" in record.message:
                        found_log_data = True
            except (IndexError, ValueError):
                continue
    # END_BLOCK_LDD_TELEMETRY

    # START_BLOCK_VERIFICATION: [Бизнес-проверки]
    # 1. Проверка существования файла
    assert os.path.exists(db_path), "Ошибка: Файл БД не создан"
    
    # 2. Проверка таблиц
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    assert "invoices" in tables, "Ошибка: Таблица invoices не создана"
    assert "items" in tables, "Ошибка: Таблица items не создана"
    assert "invoice_lines" in tables, "Ошибка: Таблица invoice_lines не создана"
    
    # 3. Проверка количества товаров
    cursor.execute("SELECT COUNT(*) FROM items")
    count = cursor.fetchone()[0]
    assert count == 20, f"Ошибка: Ожидалось 20 товаров, найдено {count}"
    
    # 4. Проверка LDD-логов
    assert found_log_schema, "Критическая ошибка LDD: Не найден лог инициализации схемы [IMP:9]"
    assert found_log_data, "Критическая ошибка LDD: Не найден лог наполнения данными [IMP:9]"
    
    conn.close()
    # END_BLOCK_VERIFICATION
# END_FUNCTION_test_db_initialization

# START_FUNCTION_test_get_connection
# START_CONTRACT:
# PURPOSE:Проверка корректности возвращаемого соединения.
# INPUTS: tmp_path (pytest fixture)
# KEYWORDS:[PATTERN(6): Factory; CONCEPT(7): RowFactory]
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def test_get_connection(tmp_path):
    """
    Тест проверяет, что get_connection возвращает объект sqlite3.Connection
    с настроенным row_factory = sqlite3.Row.
    """
    db_file = tmp_path / "test_conn.db"
    db_path = str(db_file)
    
    # START_BLOCK_EXECUTION: [Получение соединения]
    conn = get_connection(db_path)
    # END_BLOCK_EXECUTION
    
    # START_BLOCK_VERIFICATION: [Проверка свойств соединения]
    assert isinstance(conn, sqlite3.Connection), "Ошибка: Возвращен не объект sqlite3.Connection"
    assert conn.row_factory == sqlite3.Row, "Ошибка: row_factory не настроен на sqlite3.Row"
    
    # Проверка доступа по имени
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test (id INTEGER, val TEXT)")
    cursor.execute("INSERT INTO test VALUES (1, 'test_val')")
    row = cursor.execute("SELECT * FROM test").fetchone()
    
    assert row["val"] == "test_val", "Ошибка: Доступ по имени поля не работает (RowFactory)"
    
    conn.close()
    # END_BLOCK_VERIFICATION
# END_FUNCTION_test_get_connection
