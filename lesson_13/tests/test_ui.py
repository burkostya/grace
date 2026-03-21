# FILE:lesson_13/tests/test_ui.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Тестирование UI контроллера для Lesson 13.
# SCOPE: Проверка обработчиков событий UI (headless).
# INPUT: Мокированные данные и вызовы методов контроллера.
# OUTPUT: Результаты тестов (PASSED/FAILED).
# KEYWORDS:[DOMAIN(Test): UI; CONCEPT(Verification): Headless; TECH(Framework): Pytest]
# LINKS:[USES_API(Controller): UIController]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание тестов для UIController с проверкой типов возвращаемых данных.]
# END_CHANGE_SUMMARY

import pytest
import pandas as pd
import plotly.graph_objects as go
import os
from lesson_13.src.ui_controller import UIController

# START_BLOCK_TEST_SETUP: [Настройка окружения для тестов]
@pytest.fixture
def ui_controller(tmp_path):
    db_path = tmp_path / "test_parabola.db"
    config_path = tmp_path / "test_config.json"
    return UIController(db_path=str(db_path), config_path=str(config_path))
# END_BLOCK_TEST_SETUP

# START_FUNCTION_test_handle_generate_data
# START_CONTRACT:
# PURPOSE: Проверка метода генерации данных.
# INPUTS: ui_controller fixture
# OUTPUTS: None
# SIDE_EFFECTS: Создает файлы в tmp_path
# KEYWORDS:[CONCEPT(Test): DataGeneration]
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def test_handle_generate_data(ui_controller):
    """
    Тест проверяет, что handle_generate_data возвращает pandas DataFrame
    и корректно рассчитывает количество строк.
    """
    # START_BLOCK_EXECUTE: [Выполнение действия]
    df = ui_controller.handle_generate_data(1, 0, 0, -5, 5, 50)
    # END_BLOCK_EXECUTE

    # START_BLOCK_VERIFY: [Проверка результата]
    assert isinstance(df, pd.DataFrame), "Результат должен быть DataFrame"
    assert len(df) == 50, f"Ожидалось 50 точек, получено {len(df)}"
    assert list(df.columns) == ['x', 'y'], "Неверные имена колонок"
    print(f"\n[TEST][IMP:9][test_handle_generate_data] DataFrame verified: {len(df)} rows [SUCCESS]")
    # END_BLOCK_VERIFY
# END_FUNCTION_test_handle_generate_data

# START_FUNCTION_test_handle_draw_graph
# START_CONTRACT:
# PURPOSE: Проверка метода отрисовки графика.
# INPUTS: ui_controller fixture
# OUTPUTS: None
# SIDE_EFFECTS: Читает из БД
# KEYWORDS:[CONCEPT(Test): Visualization]
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def test_handle_draw_graph(ui_controller):
    """
    Тест проверяет, что handle_draw_graph возвращает объект Plotly Figure,
    даже если данных в БД еще нет (возвращает пустую фигуру с аннотацией).
    """
    # START_BLOCK_EXECUTE_EMPTY: [Проверка на пустых данных]
    fig_empty = ui_controller.handle_draw_graph()
    assert isinstance(fig_empty, go.Figure), "Должен возвращать Figure даже без данных"
    # END_BLOCK_EXECUTE_EMPTY

    # START_BLOCK_EXECUTE_WITH_DATA: [Проверка с данными]
    ui_controller.handle_generate_data(1, 0, 0, -5, 5, 10)
    fig_data = ui_controller.handle_draw_graph()
    assert isinstance(fig_data, go.Figure), "Должен возвращать Figure с данными"
    assert len(fig_data.data) > 0, "График должен содержать данные"
    print(f"[TEST][IMP:9][test_handle_draw_graph] Plotly Figure verified [SUCCESS]")
    # END_BLOCK_EXECUTE_WITH_DATA
# END_FUNCTION_test_handle_draw_graph
