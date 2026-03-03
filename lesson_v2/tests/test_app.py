# FILE: lesson_v2/tests/test_app.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Автотесты для проверки Backend и Controller в Parabola Pro.
# KEYWORDS: [TECH(9): Pytest; CONCEPT(8): AutoTest]
# END_MODULE_CONTRACT

import pytest
import os
import sys
import pandas as pd
import plotly.graph_objects as go

# Добавляем корень проекта в sys.path для импорта из lesson_v2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from lesson_v2.src.data_generator import DataGeneratorPro
from lesson_v2.src.ui_controller import UIControllerPro

@pytest.fixture
def db_path(tmp_path):
    """Создает временную БД для тестов."""
    return str(tmp_path / "test_parabola.db")

# START_FUNCTION_test_backend_calculation
def test_backend_calculation(db_path):
    # START_BLOCK_TEST_GEN: [Проверка расчетов бэкенда.]
    gen = DataGeneratorPro(db_path=db_path)
    gen.generate_points(a=1, c=0, x_min=0, x_max=2, step=1) # x=0,1,2
    
    df = gen.get_all_points()
    assert len(df) == 3
    assert df.iloc[0]['y'] == 0 # 1*0^2 + 0
    assert df.iloc[1]['y'] == 1 # 1*1^2 + 0
    assert df.iloc[2]['y'] == 4 # 1*2^2 + 0
    # END_BLOCK_TEST_GEN

# START_FUNCTION_test_controller_logic
def test_controller_logic(db_path, monkeypatch):
    # START_BLOCK_TEST_CTRL: [Проверка логики контроллера без запуска UI.]
    # Подменяем путь к БД в классе через monkeypatch или передаем в конструктор
    # Для простоты создадим контроллер и вручную укажем путь к БД его генератору
    ctrl = UIControllerPro()
    ctrl.generator = DataGeneratorPro(db_path=db_path)
    
    # Тест генерации
    df = ctrl.handle_generate(a=2, c=5, x_min=-1, x_max=1)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    
    # Тест отрисовки
    fig = ctrl.handle_draw()
    assert isinstance(fig, go.Figure)
    assert len(fig.data) > 0
    # END_BLOCK_TEST_CTRL
