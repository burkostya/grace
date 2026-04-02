# FILE: tests/test_lesson_22_backend.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Интеграционное тестирование бэкенда Lesson 22 (Config -> Calc -> DB).
# SCOPE: Проверка сохранения параметров, расчета точек и корректности данных в БД.
# INPUT: Фикстура tmp_path, caplog.
# OUTPUT: Успешность тестов и вывод логов IMP:7-10.
# KEYWORDS:[DOMAIN(8): BackendTesting; CONCEPT(7): LDD_Telemetry; TECH(9): Pytest]
# LINKS:[USES_API(8): pytest, sqlite3]
# END_MODULE_CONTRACT

import os
import sqlite3
import pytest
import logging
from lesson_22.config_manager import save_config, load_config
from lesson_22.calculator import calculate_parabola
from lesson_22.db_manager import init_db, save_points, get_points


# START_FUNCTION_test_backend_full_cycle
# START_CONTRACT:
# PURPOSE: Полная проверка цикла данных бэкенда.
# INPUTS: tmp_path, caplog.
# KEYWORDS:[PATTERN(7): IntegrationTest; CONCEPT(8): Telemetry]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def test_backend_full_cycle(tmp_path, caplog):
    """
    Тест проверяет:
    1. Сохранение и загрузку конфига.
    2. Расчет параболы.
    3. Инициализацию БД и сохранение точек.
    4. Верификацию логов IMP:7-10.
    """
    caplog.set_level(logging.INFO)

    # START_BLOCK_SETUP_PATHS: [Подготовка путей во временной папке]
    d = tmp_path / "lesson_22"
    d.mkdir()
    config_file = str(d / "config.json")
    db_file = str(d / "points_22.db")
    # END_BLOCK_SETUP_PATHS

    # START_BLOCK_CONFIG_TEST: [Тест конфигурации]
    a, c, x_min, x_max = 2.0, 5.0, -2.0, 2.0
    res_save = save_config(a, c, x_min, x_max, config_path=config_file)
    assert res_save, "Ошибка сохранения конфигурации"

    loaded = load_config(config_path=config_file)
    assert loaded["a"] == a, f"Неверное значение a: {loaded['a']}"
    # END_BLOCK_CONFIG_TEST

    # START_BLOCK_CALC_AND_DB: [Тест расчета и БД]
    points = calculate_parabola(a, c, x_min, x_max, step=1.0)
    # Ожидаемые точки для a=2, c=5: x=-2(y=13), x=-1(y=7), x=0(y=5), x=1(y=7), x=2(y=13)
    assert len(points) == 5, f"Ожидалось 5 точек, получено {len(points)}"

    init_db(db_path=db_file)
    res_db = save_points(points, db_path=db_file)
    assert res_db, "Ошибка сохранения в БД"

    db_points = get_points(db_path=db_file)
    assert len(db_points) == 5, "Данные в БД не соответствуют количеству точек"
    assert db_points[2] == (0.0, 5.0), f"Ошибка значения в центре: {db_points[2]}"
    # END_BLOCK_CALC_AND_DB

    # START_BLOCK_LDD_VERIFICATION: [Вывод и проверка логов]
    print("\n--- LDD ТРАЕКТОРИЯ (IMP:7-10) ---")
    found_belief = False
    for record in caplog.records:
        if "[IMP:" in record.message:
            try:
                imp_level = int(record.message.split("[IMP:")[1].split("]")[0])
                if imp_level >= 7:
                    print(record.message)
                if imp_level >= 9:
                    found_belief = True
            except (IndexError, ValueError):
                continue

    assert found_belief, (
        "Критическая ошибка LDD: В логах не найден Belief State (IMP:9)"
    )
    # END_BLOCK_LDD_VERIFICATION


# END_FUNCTION_test_backend_full_cycle
