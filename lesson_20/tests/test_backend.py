# FILE:lesson_20/tests/test_backend.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Тестирование бэкенд-логики Lesson 20 (Logic, Config, DB).
# SCOPE:Проверка расчета параболы, сохранения конфига и работы с БД.
# KEYWORDS:[DOMAIN(8): Testing; CONCEPT(7): Backend; TECH(9): Pytest, LDD]
# END_MODULE_CONTRACT

import os
import pytest
import pandas as pd
from lesson_20.logic import calculate_parabola
from lesson_20.config_manager import load_config, save_config
from lesson_20.db_manager import init_db, save_points, get_points

# START_FUNCTION_test_logic_calculation
# START_CONTRACT:
# PURPOSE:Проверка корректности расчета точек параболы.
# INPUTS: caplog
# OUTPUTS: None
# KEYWORDS:[PATTERN(7): LDD; CONCEPT(8): Telemetry]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def test_logic_calculation(caplog):
    """
    Тест проверяет, что функция calculate_parabola генерирует 100 точек
    и корректно рассчитывает y для x=0.
    """
    # START_BLOCK_EXECUTION: [Вызов логики]
    a, c = 2.0, 5.0
    points = calculate_parabola(a, c, -10, 10)
    # END_BLOCK_EXECUTION

    # START_BLOCK_LDD_TELEMETRY: [Вывод траектории]
    print("\n--- LDD ТРАЕКТОРИЯ (IMP:7-10) ---")
    for record in caplog.records:
        if "[IMP:" in record.message:
            try:
                imp_level = int(record.message.split("[IMP:")[1].split("]")[0])
                if imp_level >= 7:
                    print(record.message)
            except: continue
    # END_BLOCK_LDD_TELEMETRY

    # START_BLOCK_VERIFICATION: [Проверки]
    assert len(points) == 100, "Должно быть сгенерировано 100 точек"
    # Находим точку x=0 (или ближайшую)
    df = pd.DataFrame(points, columns=["x", "y"])
    y_at_zero = df.iloc[49:51]["y"].mean() # Приблизительно для 100 точек от -10 до 10
    assert abs(y_at_zero - c) < 1.0, f"Для x=0 y должен быть близок к c={c}"
    # END_BLOCK_VERIFICATION
# END_FUNCTION_test_logic_calculation

# START_FUNCTION_test_config_manager
# START_CONTRACT:
# PURPOSE:Проверка сохранения и загрузки конфигурации.
# INPUTS: tmp_path, caplog
# END_CONTRACT
def test_config_manager(tmp_path, caplog):
    """
    Тест проверяет сохранение и загрузку конфига во временной папке.
    """
    config_file = tmp_path / "test_config.json"
    test_data = {"a": 5.0, "c": 10.0, "x_min": -5.0, "x_max": 5.0}
    
    # START_BLOCK_EXECUTION: [Сохранение и загрузка]
    save_config(test_data, str(config_file))
    loaded_data = load_config(str(config_file))
    # END_BLOCK_EXECUTION

    # START_BLOCK_VERIFICATION: [Проверки]
    assert loaded_data == test_data, "Загруженные данные должны совпадать с сохраненными"
    # END_BLOCK_VERIFICATION
# END_FUNCTION_test_config_manager

# START_FUNCTION_test_db_manager
# START_CONTRACT:
# PURPOSE:Проверка инициализации и работы с БД.
# INPUTS: tmp_path, caplog
# END_CONTRACT
def test_db_manager(tmp_path, caplog):
    """
    Тест проверяет инициализацию БД, сохранение и получение точек.
    """
    db_file = tmp_path / "test_points.db"
    test_points = [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0)]
    
    # START_BLOCK_EXECUTION: [Работа с БД]
    init_db(str(db_file))
    save_points(test_points, str(db_file))
    loaded_points = get_points(str(db_file))
    # END_BLOCK_EXECUTION

    # START_BLOCK_VERIFICATION: [Проверки]
    assert len(loaded_points) == 3, "Должно быть загружено 3 точки"
    assert loaded_points[1] == (1.0, 1.0), "Данные точки должны совпадать"
    # END_BLOCK_VERIFICATION
# END_FUNCTION_test_db_manager
