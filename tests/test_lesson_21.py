# FILE:tests/test_lesson_21.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Тестирование ETL-пайплайна и семантическая верификация траектории.
# SCOPE: Проверка загрузки CSV в SQLite, валидация очистки данных.
# KEYWORDS:[PATTERN(7): LDD; CONCEPT(8): ETL_Test]
# END_MODULE_CONTRACT

import pytest
import sqlite3
import pandas as pd
import os
import logging
from lesson_21_swarm_test.etl_module import load_csv_to_db


# START_FUNCTION_test_etl_success
# START_CONTRACT:
# PURPOSE: Проверка успешного сценария: чтение, очистка, запись в БД.
# INPUTS: tmp_path (pytest fixture), caplog (fixture)
# KEYWORDS:[PATTERN(9): LDD_Verification]
# END_CONTRACT
def test_etl_success(tmp_path, caplog):
    """
    Тест проверяет полный цикл ETL. Он создает временный CSV, запускает загрузку
    и верифицирует данные в БД + наличие логов IMP:9.
    """
    caplog.set_level(logging.INFO)

    # START_BLOCK_SETUP:[Подготовка тестовых данных]
    csv_file = tmp_path / "test_data.csv"
    db_file = tmp_path / "test_warehouse.db"

    # Создаем данные с одной пустой строкой (score=NaN)
    data = "id,name,score\n1,Alice,100\n2,Bob,\n3,Charlie,90\n"
    csv_file.write_text(data)
    # END_BLOCK_SETUP

    # START_BLOCK_EXECUTION:[Вызов тестируемой функции]
    result = load_csv_to_db(str(csv_file), str(db_file))
    # END_BLOCK_EXECUTION

    # START_BLOCK_LDD_TELEMETRY:[Вывод семантической траектории]
    print("\n--- LDD ТРАЕКТОРИЯ (IMP:7-10) ---")
    found_belief = False
    for record in caplog.records:
        if "[IMP:" in record.message:
            try:
                imp_level = int(record.message.split("[IMP:")[1].split("]")[0])
                if imp_level >= 7:
                    print(record.message)
                if imp_level >= 9 and "load_csv_to_db" in record.message:
                    found_belief = True
            except (IndexError, ValueError):
                continue
    # END_BLOCK_LDD_TELEMETRY

    # START_BLOCK_VERIFICATION:[Бизнес-проверки]
    assert result is True, "Загрузка должна вернуть True"
    assert os.path.exists(db_file), "Файл базы данных должен быть создан"

    # Проверка контента в БД
    conn = sqlite3.connect(db_file)
    df_db = pd.read_sql("SELECT * FROM scores", conn)
    conn.close()

    assert len(df_db) == 2, f"Ожидалось 2 строки в БД (без NaN), найдено: {len(df_db)}"
    assert 2 not in df_db["id"].values, (
        "Bob (id=2) с пустым score не должен попасть в БД"
    )

    # Семантическая верификация: Был ли достигнут Belief State [IMP:9]
    assert found_belief, "Критическая ошибка LDD: Не найден лог достижения цели [IMP:9]"
    # END_BLOCK_VERIFICATION


# END_FUNCTION_test_etl_success
