# FILE:lesson_16/tests/test_app.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Комплексное тестирование Lesson_16 (Backend, CLI, UI Headless).
# SCOPE:Проверка корректности расчетов, работы с БД, CLI команд и UI контроллеров.
# INPUT:Нет.
# OUTPUT:Результаты тестов Pytest.
# KEYWORDS:[DOMAIN(8): Testing; TECH(9): Pytest, Anti-Loop]
# LINKS:[USES_API(8): pytest, subprocess]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание тестов с Anti-Loop Protocol.]
# END_CHANGE_SUMMARY

import pytest
import os
import json
import pandas as pd
import subprocess
import sys
import logging

# Добавляем корень проекта в PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from lesson_16.src.config_manager import load_config, save_config
from lesson_16.src.database_manager import save_points, get_points
from lesson_16.src.parabola_logic import calculate_parabola
from lesson_16.src.ui_controller import on_generate_click, on_draw_click

# Настройка логирования для тестов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEST_CONFIG_PATH = "lesson_16/tests/test_config.json"
TEST_DB_PATH = "lesson_16/tests/test_app.db"
COUNTER_FILE = ".test_counter_16.json"

# START_FUNCTION_update_test_counter
def update_test_counter(success: bool):
    """
    Реализация Anti-Loop Protocol. Сбрасывает счетчик при успехе,
    инкрементирует при неудаче. Выводит чеклист при повторных ошибках.
    """
    if not os.path.exists(COUNTER_FILE):
        data = {"attempts": 0}
    else:
        with open(COUNTER_FILE, 'r') as f:
            data = json.load(f)
    
    if success:
        data["attempts"] = 0
    else:
        data["attempts"] += 1
        
    with open(COUNTER_FILE, 'w') as f:
        json.dump(data, f)
        
    if data["attempts"] > 0:
        print(f"\n[ANTI-LOOP] Попытка №{data['attempts']}")
        print("CHECKLIST:")
        print("- Проверьте PYTHONPATH (sys.path.append)")
        print("- Проверьте наличие директорий для БД и конфигов")
        print("- Проверьте корректность путей в subprocess.run")
        if data["attempts"] >= 3:
            print("СОВЕТ: Используйте MCP tavily или Context 7 для поиска решения.")
        if data["attempts"] >= 4:
            print("ВНИМАНИЕ: Риск зацикливания! Проведите рефлексию стратегии.")
# END_FUNCTION_update_test_counter

@pytest.fixture(autouse=True)
def setup_teardown():
    """Очистка тестовых файлов перед и после тестов."""
    for f in [TEST_CONFIG_PATH, TEST_DB_PATH, "lesson_16/tests/output_test.csv"]:
        if os.path.exists(f):
            os.remove(f)
    yield
    # Очистка после тестов (опционально)

# START_FUNCTION_test_backend_logic
def test_backend_logic():
    """Проверка математической логики и работы с БД."""
    print("\n[TEST][IMP:7][test_backend_logic] Start")
    
    # 1. Расчет
    df = calculate_parabola(a=2.0, c=5.0, x_min=-2, x_max=2, points_count=5)
    assert len(df) == 5
    assert df.iloc[0]['y'] == 2.0 * (-2)**2 + 5.0  # 13.0
    print("[TEST][IMP:9][test_backend_logic] Calculation OK")
    
    # 2. БД
    success = save_points(df, db_path=TEST_DB_PATH)
    assert success is True
    df_read = get_points(db_path=TEST_DB_PATH)
    assert len(df_read) == 5
    assert df_read.iloc[0]['y'] == 13.0
    print("[TEST][IMP:9][test_backend_logic] DB Storage OK")
# END_FUNCTION_test_backend_logic

# START_FUNCTION_test_cli_smoke
def test_cli_smoke():
    """Проверка CLI команд через subprocess."""
    print("\n[TEST][IMP:7][test_cli_smoke] Start")
    
    # Подготовка конфига
    config = {"a": 1.0, "c": 0.0, "x_min": -5, "x_max": 5}
    with open("lesson_16/config.json", 'w') as f:
        json.dump(config, f)
    
    # 1. Generate
    result = subprocess.run([sys.executable, "lesson_16/src/cli.py", "generate"], capture_output=True, text=True)
    assert result.returncode == 0
    print("[TEST][IMP:9][test_cli_smoke] CLI Generate OK")
    
    # 2. Export
    csv_path = "lesson_16/tests/output_test.csv"
    result = subprocess.run([sys.executable, "lesson_16/src/cli.py", "export-csv", "--out", csv_path], capture_output=True, text=True)
    assert result.returncode == 0
    assert os.path.exists(csv_path)
    df_csv = pd.read_csv(csv_path)
    assert not df_csv.empty
    print("[TEST][IMP:9][test_cli_smoke] CLI Export OK")
# END_FUNCTION_test_cli_smoke

# START_FUNCTION_test_ui_headless
def test_ui_headless():
    """Проверка контроллеров UI без запуска сервера."""
    print("\n[TEST][IMP:7][test_ui_headless] Start")
    
    # 1. on_generate_click
    df = on_generate_click(a=3.0, c=1.0, x_min=-1, x_max=1)
    assert not df.empty
    assert df.iloc[0]['y'] == 3.0 * (-1)**2 + 1.0 # 4.0
    print("[TEST][IMP:9][test_ui_headless] UI Generate Controller OK")
    
    # 2. on_draw_click
    fig = on_draw_click()
    assert fig is not None
    assert hasattr(fig, 'data')
    print("[TEST][IMP:9][test_ui_headless] UI Draw Controller OK")
# END_FUNCTION_test_ui_headless

def pytest_sessionfinish(session, exitstatus):
    """Хук для обновления счетчика Anti-Loop."""
    update_test_counter(exitstatus == 0)
