# FILE:lesson_12/tests/test_callbacks.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Headless UI тестирование callback-функций.
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.1 - Исправление семантической разметки: добавлены MODULE_MAP и контракты тестов.]
# PREV_CHANGE_SUMMARY: [v1.0.0 - Создание тестов callback-функций.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Тест callback генерации] => test_on_generate_headless
# FUNC 10[Тест callback отрисовки] => test_on_draw_headless
# FUNC 10[Тест callback сохранения] => test_on_save_headless
# END_MODULE_MAP

import pytest
import plotly.graph_objects as go
from lesson_12.app import on_generate, on_draw, on_save

# START_FUNCTION_test_on_generate_headless
# START_CONTRACT:
# PURPOSE: Проверка работы callback генерации без сервера.
# END_CONTRACT
def test_on_generate_headless():
    """Тест callback генерации без запуска сервера."""
    # START_BLOCK_TEST: [Вызов и проверка]
    table_data, status = on_generate(n_clicks=1, a=1, c=0, x_min=-5, x_max=5)
    
    assert isinstance(table_data, list)
    assert "x" in table_data[0]
    assert "y_edited" in table_data[0]
    assert "Generated" in status
    # END_BLOCK_TEST

# START_FUNCTION_test_on_draw_headless
# START_CONTRACT:
# PURPOSE: Проверка работы callback отрисовки без сервера.
# END_CONTRACT
def test_on_draw_headless():
    """Тест callback отрисовки."""
    # START_BLOCK_TEST: [Вызов и проверка]
    test_data = [{"x": 0, "y": 0, "y_edited": 5}]
    fig = on_draw(n_clicks=1, table_data=test_data)
    
    assert isinstance(fig, go.Figure)
    assert fig.data[1].y[0] == 5
    # END_BLOCK_TEST

# START_FUNCTION_test_on_save_headless
# START_CONTRACT:
# PURPOSE: Проверка работы callback сохранения без сервера.
# END_CONTRACT
def test_on_save_headless():
    """Тест callback сохранения."""
    # START_BLOCK_TEST: [Вызов и проверка]
    test_data = [{"x": 0, "y": 0, "y_edited": 99}]
    status = on_save(n_clicks=1, table_data=test_data)
    
    assert "Saved" in status
    # END_BLOCK_TEST
