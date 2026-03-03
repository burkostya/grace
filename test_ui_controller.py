# FILE: test_ui_controller.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Тестирование логики контроллера без запуска Gradio.
# SCOPE: Модульное тестирование контроллера.
# KEYWORDS: [TECH(9): Pytest; DOMAIN(8): Testing; TECH(7): Pandas]
# END_MODULE_CONTRACT

import pytest
import os
import pandas as pd
from ui_controller import UIController

# START_FUNCTION_test_handle_generate
# START_CONTRACT:
# PURPOSE: Проверка, что контроллер возвращает корректный DataFrame.
# KEYWORDS: [CONCEPT(7): Integration_Test]
# END_CONTRACT
def test_handle_generate():
    db_name = "test_ui.db"
    if os.path.exists(db_name):
        os.remove(db_name)
        
    ctrl = UIController(db_name)
    df = ctrl.handle_generate(a=2.0, c=5.0)
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'x' in df.columns
    assert 'y' in df.columns
    
    # Проверка расчета для x=0: y = 2*0^2 + 5 = 5
    y_at_zero = df[df['x'] == 0.0]['y'].values[0]
    assert y_at_zero == 5.0
    
    os.remove(db_name)
# END_FUNCTION_test_handle_generate

# START_FUNCTION_test_handle_draw_logic
# START_CONTRACT:
# PURPOSE: Проверка логики подготовки графика (наличие данных).
# KEYWORDS: [CONCEPT(7): Plot_Logic]
# END_CONTRACT
def test_handle_draw_logic():
    db_name = "test_draw.db"
    ctrl = UIController(db_name)
    
    # Сначала пусто
    fig_empty = ctrl.handle_draw()
    assert fig_empty is None
    
    # Генерируем и проверяем
    ctrl.handle_generate(1, 1)
    fig = ctrl.handle_draw()
    assert fig is not None
    # Проверка типа (Plotly Figure)
    assert hasattr(fig, 'to_json') 

    os.remove(db_name)
# END_FUNCTION_test_handle_draw_logic
