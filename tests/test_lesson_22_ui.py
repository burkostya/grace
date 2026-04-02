# FILE: tests/test_lesson_22_ui.py
# VERSION: 1.1.0
# START_MODULE_CONTRACT:
# PURPOSE: Headless-тестирование UI контроллеров Gradio для Lesson 22.
# SCOPE: Проверка типов возвращаемых значений и логики контроллеров без запуска UI.
# INPUT: Фикстура tmp_path.
# OUTPUT: Успешность тестов.
# KEYWORDS:[DOMAIN(8): UITesting; CONCEPT(7): Headless; TECH(9): Gradio]
# LINKS:[USES_API(8): pandas, plotly]
# END_MODULE_CONTRACT

import pytest
import pandas as pd
from lesson_22.ui import handle_generate, handle_draw
from lesson_22.db_manager import init_db


# START_FUNCTION_test_ui_handlers
# START_CONTRACT:
# PURPOSE: Проверка возвращаемых типов контроллеров UI через DI.
# INPUTS: tmp_path.
# KEYWORDS:[PATTERN(7): HeadlessTest; CONCEPT(8): UI_Logic]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def test_ui_handlers(tmp_path):
    """
    Тест имитирует вызовы контроллеров Gradio с передачей временных путей (DI)
    и проверяет, что они возвращают правильные объекты.
    """
    # START_BLOCK_SETUP_ENV: [Подготовка путей во временной папке]
    d = tmp_path / "lesson_22"
    d.mkdir()
    db_file = str(d / "points_22.db")
    config_file = str(d / "config.json")

    # Инициализируем БД
    init_db(db_path=db_file)
    # END_BLOCK_SETUP_ENV

    # START_BLOCK_TEST_GENERATE: [Тест контроллера генерации с DI]
    df = handle_generate(
        a=1.0, c=0.0, x_min=-5, x_max=5, db_path=db_file, config_path=config_file
    )
    assert isinstance(df, pd.DataFrame), (
        "handle_generate должен возвращать pandas.DataFrame"
    )
    assert not df.empty, "DataFrame не должен быть пустым"
    assert list(df.columns) == ["x", "y"], f"Неверные колонки: {df.columns}"
    # END_BLOCK_TEST_GENERATE

    # START_BLOCK_TEST_DRAW: [Тест контроллера отрисовки с DI]
    fig = handle_draw(db_path=db_file)
    assert hasattr(fig, "to_dict"), (
        "handle_draw должен возвращать объект графика Plotly"
    )
    assert "data" in fig.to_dict(), "График должен содержать данные"
    # END_BLOCK_TEST_DRAW


# END_FUNCTION_test_ui_handlers
