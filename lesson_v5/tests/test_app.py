# FILE:lesson_v5/tests/test_app.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Тестирование приложения lesson_v5 (Backend, CLI, UI Headless).
# SCOPE:Проверка бизнес-логики, CLI команд и UI контроллеров.
# INPUT:Моковые данные и вызовы функций.
# OUTPUT:Результаты тестов pytest.
# KEYWORDS:[DOMAIN(8): Testing; CONCEPT(7): LDD_Telemetry; TECH(9): pytest]
# LINKS:[USES_API(8): pytest, subprocess; READS_DATA_FROM(9): lesson_v5/config.json]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание тестов с LDD телеметрией.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Тест бизнес-логики] => test_parabola_logic
# FUNC 10[Тест CLI генерации] => test_cli_generate
# FUNC 10[Тест UI контроллера] => test_ui_controller
# END_MODULE_MAP
#
# START_USE_CASES:
# - [test_parabola_logic]: Developer -> RunTests -> LogicVerified
# END_USE_CASES

import pytest
import os
import subprocess
import pandas as pd
import logging
from lesson_v5.src.parabola_logic import generate_parabola_points
from lesson_v5.src.ui_controller import ui_generate_handler
from lesson_v5.src.database_manager import DatabaseManager
from lesson_v5.src.config_manager import load_config

# Настройка логирования для тестов
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# START_FUNCTION_test_parabola_logic
# START_CONTRACT:
# PURPOSE:Проверяет корректность расчета точек параболы.
# INPUTS: caplog (pytest fixture)
# OUTPUTS: None
# SIDE_EFFECTS: Нет.
# KEYWORDS:[PATTERN(6): UnitTesting; CONCEPT(8): MathVerification]
# END_CONTRACT
def test_parabola_logic(caplog):
    """Тест бизнес-логики расчета параболы."""
    # START_BLOCK_TEST_LOGIC: [Проверка расчета]
    with caplog.at_level(logging.DEBUG):
        a, c = 1.0, 0.0
        range_x = [-2, 2]
        step = 1.0
        
        points = generate_parabola_points(a, c, range_x, step)
        
        # Проверка количества точек: (-2, -1, 0, 1, 2) => 5 точек
        assert len(points) == 5
        assert points[0] == (-2.0, 4.0)
        assert points[2] == (0.0, 0.0)
        assert points[4] == (2.0, 4.0)
        
        # LDD Telemetry: Вывод логов IMP:7-10 в stdout при успехе/ошибке
        important_logs = [rec.message for rec in caplog.records if "[IMP:9]" in rec.message or "[IMP:10]" in rec.message]
        print("\n--- LDD Telemetry (IMP:7-10) ---")
        for log in important_logs:
            print(log)
    # END_BLOCK_TEST_LOGIC
# END_FUNCTION_test_parabola_logic

# START_FUNCTION_test_cli_generate
# START_CONTRACT:
# PURPOSE:Дымовой тест CLI через subprocess.
# INPUTS: None
# OUTPUTS: None
# SIDE_EFFECTS: Создание БД и CSV файла.
# KEYWORDS:[PATTERN(6): SmokeTesting; CONCEPT(8): CLI_Verification]
# END_CONTRACT
def test_cli_generate():
    """Дымовой тест CLI команд."""
    # START_BLOCK_TEST_CLI: [Вызов CLI через subprocess]
    # 1. Тест генерации
    cmd_gen = [
        "python", "-m", "lesson_v5.src.cli", "generate",
        "--a", "2.0", "--c", "1.0", "--range", "-1", "1", "--step", "0.5"
    ]
    result_gen = subprocess.run(cmd_gen, capture_output=True, text=True)
    assert result_gen.returncode == 0
    assert "Успешно сгенерировано" in result_gen.stdout
    
    # 2. Тест экспорта
    export_file = "test_export.csv"
    cmd_exp = ["python", "-m", "lesson_v5.src.cli", "export-csv", "--output", export_file]
    result_exp = subprocess.run(cmd_exp, capture_output=True, text=True)
    assert result_exp.returncode == 0
    assert os.path.exists(export_file)
    
    # Очистка
    if os.path.exists(export_file):
        os.remove(export_file)
    # END_BLOCK_TEST_CLI
# END_FUNCTION_test_cli_generate

# START_FUNCTION_test_ui_controller
# START_CONTRACT:
# PURPOSE:Headless тест UI контроллера (без запуска сервера).
# INPUTS: None
# OUTPUTS: None
# SIDE_EFFECTS: Запись в БД.
# KEYWORDS:[PATTERN(6): HeadlessTesting; CONCEPT(8): UI_LogicVerification]
# END_CONTRACT
def test_ui_controller():
    """Тест логики UI контроллера."""
    # START_BLOCK_TEST_UI: [Вызов обработчика напрямую]
    a, c = 1.0, 5.0
    min_x, max_x = 0, 10
    step = 2.0
    
    fig, df = ui_generate_handler(a, c, min_x, max_x, step)
    
    # Проверка типов возвращаемых значений (Headless)
    import plotly.graph_objects as go
    assert isinstance(fig, go.Figure)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == 6 # (0, 2, 4, 6, 8, 10)
    # END_BLOCK_TEST_UI
# END_FUNCTION_test_ui_controller
