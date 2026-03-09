# FILE:lesson_9/tests/test_app.py
# VERSION:1.0.2
# START_MODULE_CONTRACT:
# PURPOSE: Комплексное тестирование приложения lesson_9 (Backend, CLI, UI).
# SCOPE: Модульные, интеграционные и дымовые тесты.
# INPUT: Исходный код в lesson_9/src/.
# OUTPUT: Результаты выполнения pytest.
# KEYWORDS:[DOMAIN(8): Testing; CONCEPT(9): Pytest; TECH(7): Subprocess]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.2 - Исправление аргументов CLI в тестах (generate не принимает параметры, export-csv использует --out).]
# PREV_CHANGE_SUMMARY: [v1.0.1 - Исправление имен функций и путей импорта.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Backend & LDD Test: Проверка расчета и БД] => test_backend_logic
# FUNC 10[CLI Smoke Test: Проверка cli.py через subprocess] => test_cli_smoke
# FUNC 10[UI Headless Test: Проверка Gradio контроллеров] => test_ui_headless
# END_MODULE_MAP

import pytest
import subprocess
import os
import sys
import pandas as pd
import plotly.graph_objects as go
import logging
import json

# Добавляем корень проекта в sys.path для корректной работы импортов вида lesson_9.src...
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from lesson_9.src.parabola_logic import calculate_parabola_points
from lesson_9.src.database_manager import save_points, get_points, init_db
from lesson_9.src.config_manager import load_config, save_config
from lesson_9.src.ui_controller import handle_generate, handle_draw_graph

# Настройка логирования для тестов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# START_FUNCTION_test_backend_logic
# START_CONTRACT:
# PURPOSE: Проверка математической логики и сохранения в БД.
# INPUTS: 
# - caplog => caplog: pytest fixture
# OUTPUTS: 
# - None
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def test_backend_logic(caplog):
    """
    Тест проверяет корректность расчета параболы и успешность записи данных в SQLite.
    Используется caplog для верификации LDD логов уровня IMP:7-10.
    """
    caplog.set_level(logging.INFO)
    
    # START_BLOCK_CALCULATION: [Проверка математики]
    logger.info("[Test][IMP:9][test_backend_logic][CALCULATION][Start] Начинаем проверку расчета [INFO]")
    points = calculate_parabola_points(1, 0, -10, 10, 0.1)
    assert len(points) > 0
    # Проверка вершины (0, 0) для y = 1*x^2 + 0
    x_vals = [p[0] for p in points]
    y_vals = [p[1] for p in points]
    if 0.0 in x_vals:
        idx = x_vals.index(0.0)
        assert y_vals[idx] == 0.0
    logger.info("[Test][IMP:9][test_backend_logic][CALCULATION][Success] Расчет верен [SUCCESS]")
    # END_BLOCK_CALCULATION

    # START_BLOCK_DATABASE: [Проверка БД]
    init_db()
    save_points(points)
    
    history = get_points()
    assert len(history) == len(points)
    logger.info("[Test][IMP:8][test_backend_logic][DATABASE][Success] Данные в БД сохранены и считаны [SUCCESS]")
    # END_BLOCK_DATABASE

    # START_BLOCK_LOG_VERIFICATION: [Принудительный вывод логов в консоль]
    important_logs = [record.message for record in caplog.records if "[IMP:" in record.message]
    print("\n--- [LDD TELEMETRY: IMP:7-10] ---")
    for log in important_logs:
        print(log)
    print("--- [END TELEMETRY] ---\n")
    
    assert len(important_logs) > 0
    # END_BLOCK_LOG_VERIFICATION
# END_FUNCTION_test_backend_logic

# START_FUNCTION_test_cli_smoke
# START_CONTRACT:
# PURPOSE: Дымовой тест CLI интерфейса.
# INPUTS: None
# OUTPUTS: None
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def test_cli_smoke():
    """
    Запуск cli.py через subprocess для проверки команд generate и export-csv.
    """
    cli_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/cli.py'))
    
    # START_BLOCK_GENERATE: [Команда generate]
    # В lesson_9/src/cli.py команда generate не принимает аргументов, а берет их из конфига.
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    
    # Сначала подготовим конфиг
    save_config({"a": 1.0, "c": 0.0, "x_min": -5, "x_max": 5})
    
    result = subprocess.run(
        [sys.executable, cli_path, "generate"],
        capture_output=True,
        text=True,
        env=env
    )
    assert result.returncode == 0
    assert "successfully" in result.stdout.lower() or "успешно" in result.stdout.lower()
    # END_BLOCK_GENERATE

    # START_BLOCK_EXPORT: [Команда export-csv]
    # В cli.py аргумент называется --out
    export_file = "test_export.csv"
    result = subprocess.run(
        [sys.executable, cli_path, "export-csv", "--out", export_file],
        capture_output=True,
        text=True,
        env=env
    )
    assert result.returncode == 0
    if os.path.exists(export_file):
        os.remove(export_file)
    # END_BLOCK_EXPORT
# END_FUNCTION_test_cli_smoke

# START_FUNCTION_test_ui_headless
# START_CONTRACT:
# PURPOSE: Тестирование логики UI контроллера без запуска сервера.
# INPUTS: None
# OUTPUTS: None
# COMPLEXITY_SCORE: 7
# END_CONTRACT
def test_ui_headless():
    """
    Проверка функций-обработчиков в ui_controller.py.
    """
    # START_BLOCK_HANDLE_CALC: [Тест расчета]
    # handle_generate(a, c, x_min, x_max) -> pd.DataFrame
    df = handle_generate(2.0, 1.0, -5, 5)
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    # END_BLOCK_HANDLE_CALC

    # START_BLOCK_HANDLE_DRAW: [Тест отрисовки]
    fig = handle_draw_graph()
    assert isinstance(fig, go.Figure)
    # END_BLOCK_HANDLE_DRAW

    # START_BLOCK_CONFIG: [Тест конфига]
    test_cfg = {"a": 5.0, "c": 10.0, "x_min": -1, "x_max": 1}
    save_config(test_cfg)
    loaded = load_config()
    assert loaded["a"] == 5.0
    # END_BLOCK_CONFIG
# END_FUNCTION_test_ui_headless
