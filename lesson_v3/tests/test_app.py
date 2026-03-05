# FILE:lesson_v3/tests/test_app.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Тестирование бизнес-логики, CLI и UI контроллеров Lesson_v3.
# SCOPE:Backend, CLI Smoke, UI Headless тесты.
# INPUT:Моковые данные, вызовы функций.
# OUTPUT:Результаты тестов pytest.
# KEYWORDS:[DOMAIN(8):Testing; CONCEPT(7):Pytest; TECH(9):Python_pytest]
# LINKS:[USES_API(9):parabola_logic, config_manager, database_manager, cli, ui_controller]
# END_MODULE_CONTRACT

# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание тестов для Lesson_v3.]
# END_CHANGE_SUMMARY

import os
import sys
import pytest
import pandas as pd
import plotly.graph_objects as go
import subprocess
import logging

# Добавляем корень проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from lesson_v3.src.parabola_logic import generate_parabola_points
from lesson_v3.src.config_manager import load_config, save_config
from lesson_v3.src.database_manager import init_db, save_points, load_points
from lesson_v3.src.ui_controller import on_generate_click, on_draw_click

# Фикстуры для путей
@pytest.fixture
def test_paths(tmp_path):
    config_path = tmp_path / "config.json"
    db_path = tmp_path / "parabola.db"
    return str(config_path), str(db_path)

# START_FUNCTION_test_backend_logic
# START_CONTRACT:
# PURPOSE:Проверка расчета параболы и работы с БД.
# INPUTS: caplog (фикстура pytest)
# OUTPUTS: Нет
# SIDE_EFFECTS: Нет.
# END_CONTRACT
def test_backend_logic(test_paths, caplog):
    """Проверка логики расчета и сохранения в БД."""
    # START_BLOCK_TEST_CALC: [Тест расчета]
    caplog.set_level(logging.INFO)
    config_path, db_path = test_paths
    
    # 1. Тест расчета
    points = generate_parabola_points(a=2.0, c=5.0, x_min=-2, x_max=2, num_points=5)
    assert len(points) == 5
    # y = 2*x^2 + 5. Для x=0, y=5.
    assert points[2][0] == 0.0
    assert points[2][1] == 5.0
    # END_BLOCK_TEST_CALC

    # START_BLOCK_TEST_DB: [Тест БД]
    init_db(db_path)
    save_points(db_path, points)
    df = load_points(db_path)
    assert len(df) == 5
    assert df.iloc[2]['y'] == 5.0
    # END_BLOCK_TEST_DB

    # START_BLOCK_CHECK_LOGS: [Проверка логов LDD]
    # Ищем логи с IMP:9
    important_logs = [rec.message for rec in caplog.records if "[IMP:9]" in rec.message]
    assert len(important_logs) > 0
    print("\n[LDD Telemetry] Important logs found:")
    for log in important_logs:
        print(f"  - {log}")
    # END_BLOCK_CHECK_LOGS
# END_FUNCTION_test_backend_logic

# START_FUNCTION_test_cli_smoke
# START_CONTRACT:
# PURPOSE:Дымовой тест CLI через subprocess.
# INPUTS: Нет
# OUTPUTS: Нет
# SIDE_EFFECTS: Создает временные файлы.
# END_CONTRACT
def test_cli_smoke(tmp_path):
    """Проверка CLI команд generate и export-csv."""
    # START_BLOCK_CLI_GENERATE: [Тест команды generate]
    cli_path = os.path.join("lesson_v3", "src", "cli.py")
    
    # Запуск генерации
    result_gen = subprocess.run(
        [sys.executable, cli_path, "generate"],
        capture_output=True, text=True
    )
    assert result_gen.returncode == 0
    # END_BLOCK_CLI_GENERATE

    # START_BLOCK_CLI_EXPORT: [Тест команды export-csv]
    out_csv = tmp_path / "export.csv"
    result_exp = subprocess.run(
        [sys.executable, cli_path, "export-csv", "--out", str(out_csv)],
        capture_output=True, text=True
    )
    assert result_exp.returncode == 0
    assert os.path.exists(out_csv)
    # END_BLOCK_CLI_EXPORT
# END_FUNCTION_test_cli_smoke

# START_FUNCTION_test_ui_headless
# START_CONTRACT:
# PURPOSE:Тестирование обработчиков UI без запуска сервера.
# INPUTS: Нет
# OUTPUTS: Нет
# SIDE_EFFECTS: Нет.
# END_CONTRACT
def test_ui_headless(test_paths):
    """Проверка контроллеров UI."""
    # START_BLOCK_TEST_UI_HANDLERS: [Тест обработчиков]
    # Подменяем пути в модуле ui_controller для теста
    import lesson_v3.src.ui_controller as ui
    config_path, db_path = test_paths
    ui.CONFIG_PATH = config_path
    ui.DB_PATH = db_path
    
    # 1. Тест генерации
    status = ui.on_generate_click(a=1.0, c=0.0, x_min=-5, x_max=5)
    assert "Successfully generated" in status
    
    # 2. Тест отрисовки
    df, fig = ui.on_draw_click()
    assert isinstance(df, pd.DataFrame)
    assert isinstance(fig, go.Figure)
    assert not df.empty
    # END_BLOCK_TEST_UI_HANDLERS
# END_FUNCTION_test_ui_headless
