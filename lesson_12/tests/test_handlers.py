# FILE:lesson_12/tests/test_handlers.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Headless-тесты чистой бизнес-логики.
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.1 - Исправление семантической разметки: добавлены MODULE_MAP и контракты тестов.]
# PREV_CHANGE_SUMMARY: [v1.0.0 - Создание тестов логики.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# CLASS 10[Тесты логики параболы] => TestParabolaLogic
# END_MODULE_MAP

import pytest
import pandas as pd
import plotly.graph_objects as go
from lesson_12.handlers import generate_parabola_points, build_comparison_figure

# START_CLASS_TestParabolaLogic
class TestParabolaLogic:
    """
    Набор тестов для проверки математической корректности и структуры данных
    в модуле handlers.py.
    """

    # START_FUNCTION_test_generate_points_structure
    # START_CONTRACT:
    # PURPOSE: Проверка структуры DataFrame.
    # END_CONTRACT
    def test_generate_points_structure(self):
        """Проверка структуры возвращаемого DataFrame."""
        # START_BLOCK_TEST: [Проверка колонок и длины]
        df = generate_parabola_points(a=1, c=0, x_min=-2, x_max=2, step=1)
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["x", "y", "y_edited"]
        assert len(df) == 5 # -2, -1, 0, 1, 2
        # END_BLOCK_TEST

    # START_FUNCTION_test_math_correctness
    # START_CONTRACT:
    # PURPOSE: Проверка точности расчетов.
    # END_CONTRACT
    def test_math_correctness(self):
        """y = 2*x^2 + 5 при x=2 -> y=13."""
        # START_BLOCK_TEST: [Проверка значения]
        df = generate_parabola_points(a=2, c=5, x_min=2, x_max=2)
        assert df.iloc[0]["y"] == 13
        assert df.iloc[0]["y_edited"] == 13
        # END_BLOCK_TEST

    # START_FUNCTION_test_build_figure
    # START_CONTRACT:
    # PURPOSE: Проверка генерации объекта графика.
    # END_CONTRACT
    def test_build_figure(self):
        """Проверка создания объекта графика."""
        # START_BLOCK_TEST: [Проверка типа и данных]
        data = [{"x": 0, "y": 0, "y_edited": 10}]
        fig = build_comparison_figure(data)
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 2 # Original + Edited
        assert fig.data[1].y[0] == 10
        # END_BLOCK_TEST
# END_CLASS_TestParabolaLogic
