# FILE: test_datagenerator.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Тестирование модуля datagenerator.py с использованием pytest.
# SCOPE: Модульное тестирование бэкенда.
# KEYWORDS: [TECH(9): Pytest; DOMAIN(8): Testing; TECH(7): SQLite]
# END_MODULE_CONTRACT

import pytest
import os
from datagenerator import DataGenerator

# START_FUNCTION_test_db_initialization
# START_CONTRACT:
# PURPOSE: Проверка создания файла БД и таблицы.
# KEYWORDS: [CONCEPT(7): DB_Init]
# END_CONTRACT
def test_db_initialization():
    db_name = "test_parabola.db"
    if os.path.exists(db_name):
        os.remove(db_name)
    
    dg = DataGenerator(db_name)
    assert os.path.exists(db_name)
    
    # Проверка, что таблица пуста
    points = dg.get_all_points()
    assert len(points) == 0
    
    os.remove(db_name)
# END_FUNCTION_test_db_initialization

# START_FUNCTION_test_point_generation
# START_CONTRACT:
# PURPOSE: Проверка корректности расчета и сохранения точек.
# KEYWORDS: [CONCEPT(8): Math_Logic]
# END_CONTRACT
def test_point_generation():
    db_name = "test_gen.db"
    dg = DataGenerator(db_name)
    
    # y = 1*x^2 + 0, x in [-2, 2] step 1 => (-2,4), (-1,1), (0,0), (1,1), (2,4)
    dg.generate_points(a=1.0, c=0.0, x_range=(-2, 2, 1))
    
    points = dg.get_all_points()
    assert len(points) == 5
    
    # Проверка конкретной точки (0,0)
    x_vals = [p[0] for p in points]
    y_vals = [p[1] for p in points]
    
    assert 0.0 in x_vals
    idx = x_vals.index(0.0)
    assert y_vals[idx] == 0.0
    
    # Проверка точки (-2, 4)
    assert -2.0 in x_vals
    idx_neg = x_vals.index(-2.0)
    assert y_vals[idx_neg] == 4.0

    os.remove(db_name)
# END_FUNCTION_test_point_generation
