# FILE:lesson_17/tests/test_app.py
# VERSION:1.1.0
# START_MODULE_CONTRACT:
# PURPOSE:Комплексное тестирование Lesson_17 (Backend, CLI, UI Headless) с соблюдением LDD и Anti-Loop.
# SCOPE:Проверка корректности расчетов тригонометрической функции, работы с БД, CLI команд и UI контроллеров.
# INPUT:Нет.
# OUTPUT:Результаты тестов Pytest.
# KEYWORDS:[DOMAIN(8): Testing; TECH(9): Pytest, Anti-Loop, LDD]
# LINKS:[USES_API(8): pytest, subprocess]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.1.0 - Исправление архитектурных нарушений: внедрение реального LDD через caplog, Anti-Loop Protocol и семантических контрактов.]
# PREV_CHANGE_SUMMARY:[v1.0.0 - Первичное создание тестов с Anti-Loop Protocol.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Реализация Anti-Loop Protocol] => update_test_counter
# FUNC 10[Проверка логики и реальных логов LDD] => test_backend_logic
# FUNC 10[Smoke-тест CLI через subprocess] => test_cli_smoke
# FUNC 10[Headless-тест UI контроллеров] => test_ui_headless
# END_MODULE_MAP

import pytest
import os
import json
import pandas as pd
import subprocess
import sys
import logging
import math

# Добавляем корень проекта в PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from lesson_17.src.config_manager import load_config, save_config
from lesson_17.src.database_manager import save_points, get_points
from lesson_17.src.trig_logic import calculate_trig
from lesson_17.src.ui_controller import on_generate_click, on_draw_click

# Настройка логирования для тестов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEST_CONFIG_PATH = "lesson_17/tests/test_config.json"
TEST_DB_PATH = "lesson_17/tests/test_app.db"
COUNTER_FILE = ".test_counter_17.json"

# START_FUNCTION_update_test_counter
# START_CONTRACT:
# PURPOSE:Реализация Anti-Loop Protocol. Сбрасывает счетчик при успехе, инкрементирует при неудаче.
# INPUTS:
# - bool => success: Статус прохождения тестов
# OUTPUTS:
# - None
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def update_test_counter(success: bool):
    """
    Управляет счетчиком попыток тестирования. При неудаче выводит чеклист
    типовых ошибок для предотвращения зацикливания агента.
    """
    # START_BLOCK_LOAD_DATA: [Загрузка состояния счетчика]
    if not os.path.exists(COUNTER_FILE):
        data = {"attempts": 0}
    else:
        try:
            with open(COUNTER_FILE, 'r') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = {"attempts": 0}
    # END_BLOCK_LOAD_DATA
    
    # START_BLOCK_UPDATE_STATE: [Обновление счетчика]
    if success:
        data["attempts"] = 0
    else:
        data["attempts"] += 1
        
    with open(COUNTER_FILE, 'w') as f:
        json.dump(data, f)
    # END_BLOCK_UPDATE_STATE
        
    # START_BLOCK_CHECKLIST_OUTPUT: [Вывод чеклиста при ошибках]
    if data["attempts"] > 0:
        print(f"\n[ANTI-LOOP] Попытка №{data['attempts']}")
        print("--- CHECKLIST ТИПОВЫХ ОШИБОК ---")
        print("- [ ] Проверьте PYTHONPATH (sys.path.append)")
        print("- [ ] Проверьте пути в subprocess.run (используйте cwd=...)")
        print("- [ ] Убедитесь, что тесты не используют 'фейковые' логи через print")
        print("- [ ] Проверьте наличие директорий для БД и конфигов")
        
        if data["attempts"] >= 3:
            print("[ADVICE] Используйте MCP 'tavily' или 'Context 7' для поиска решения.")
        if data["attempts"] >= 4:
            print("[WARNING] ВНИМАНИЕ: Риск зацикливания! Проведите рефлексию стратегии.")
        if data["attempts"] >= 5:
            print("[CRITICAL] ОБНАРУЖЕНО ЗАЦИКЛИВАНИЕ! Остановитесь и запросите помощь.")
    # END_BLOCK_CHECKLIST_OUTPUT
# END_FUNCTION_update_test_counter

@pytest.fixture(autouse=True)
def setup_teardown():
    """Очистка тестовых файлов перед и после тестов."""
    files_to_clean = [TEST_CONFIG_PATH, TEST_DB_PATH, "lesson_17/tests/output_test.csv"]
    for f in files_to_clean:
        if os.path.exists(f):
            os.remove(f)
    yield
    # Очистка после тестов

# START_FUNCTION_test_backend_logic
# START_CONTRACT:
# PURPOSE:Проверка математической логики и верификация реальных логов LDD.
# INPUTS:
# - caplog: pytest fixture для захвата логов
# OUTPUTS:
# - None
# KEYWORDS:[PATTERN(7): LDD; CONCEPT(8): Telemetry]
# LINKS:[USES_API(9): lesson_17.src.trig_logic.calculate_trig]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def test_backend_logic(caplog):
    """
    Проверяет расчет тригонометрической функции и корректность записи в БД.
    Использует caplog для подтверждения того, что бизнес-логика выдает нужные логи [IMP:9].
    """
    # START_BLOCK_CALCULATION: [Расчет и проверка значений]
    caplog.set_level(logging.INFO)
    df = calculate_trig(A=2.0, B=1.0, C=0.0, D=0.0, x_min=-2, x_max=2)
    assert len(df) == 100
    expected_y = 2.0 * math.sin(1.0 * (-2.0) + 0.0) + 0.0
    assert abs(df.iloc[0]['y'] - expected_y) < 0.001
    # END_BLOCK_CALCULATION
    
    # START_BLOCK_LDD_VERIFY: [Верификация реальных логов]
    # Обязательная инъекция логов уровней [IMP:7-10] для верификации траектории.
    found_log = False
    print("\n--- LDD TELEMETRY (IMP:7-10) ---")
    for record in caplog.records:
        if any(f"[IMP:{i}]" in record.message for i in range(7, 11)):
            print(record.message)
            if "[IMP:9]" in record.message and "calculate_trig" in record.message:
                found_log = True
    
    assert found_log, "LDD Error: Бизнес-логика не выдала целевой лог [IMP:9] при расчете"
    # END_BLOCK_LDD_VERIFY
    
    # START_BLOCK_DB_STORAGE: [Проверка БД]
    success = save_points(df, db_path=TEST_DB_PATH)
    assert success is True
    df_read = get_points(db_path=TEST_DB_PATH)
    assert len(df_read) == 100
    assert abs(df_read.iloc[0]['y'] - expected_y) < 0.001
    # END_BLOCK_DB_STORAGE
# END_FUNCTION_test_backend_logic

# START_FUNCTION_test_cli_smoke
# START_CONTRACT:
# PURPOSE:Проверка CLI команд через subprocess с корректными путями.
# INPUTS:
# - None
# OUTPUTS:
# - None
# KEYWORDS:[DOMAIN(8): CLI; CONCEPT(9): SmokeTest]
# LINKS:[USES_API(9): lesson_17.src.cli]
# COMPLEXITY_SCORE: 7
# END_CONTRACT
def test_cli_smoke():
    """
    Smoke-тест CLI. Проверяет команды generate и export-csv.
    Использует cwd для корректного поиска файлов внутри lesson_17.
    """
    # START_BLOCK_PREPARE_CONFIG: [Подготовка тестового конфига]
    config = {"A": 1.0, "B": 1.0, "C": 0.0, "D": 0.0, "x_min": -5, "x_max": 5}
    # CLI ожидает config.json в корне lesson_17
    lesson_dir = os.path.abspath("lesson_17")
    config_path = os.path.join(lesson_dir, "config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f)
    # END_BLOCK_PREPARE_CONFIG
    
    # START_BLOCK_CLI_GENERATE: [Команда generate]
    cli_script = "src/cli.py"
    result = subprocess.run(
        [sys.executable, cli_script, "generate"],
        capture_output=True,
        text=True,
        cwd=lesson_dir
    )
    assert result.returncode == 0
    # END_BLOCK_CLI_GENERATE
    
    # START_BLOCK_CLI_EXPORT: [Команда export-csv]
    csv_path = os.path.abspath("lesson_17/tests/output_test.csv")
    result = subprocess.run(
        [sys.executable, cli_script, "export-csv", "--out", csv_path],
        capture_output=True,
        text=True,
        cwd=lesson_dir
    )
    assert result.returncode == 0
    assert os.path.exists(csv_path)
    # END_BLOCK_CLI_EXPORT
# END_FUNCTION_test_cli_smoke

# START_FUNCTION_test_ui_headless
# START_CONTRACT:
# PURPOSE:Проверка контроллеров UI без запуска сервера.
# INPUTS:
# - None
# OUTPUTS:
# - None
# KEYWORDS:[DOMAIN(8): UI; CONCEPT(9): Headless]
# LINKS:[USES_API(9): lesson_17.src.ui_controller]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def test_ui_headless():
    """
    Проверяет функции-обработчики Gradio (on_generate_click, on_draw_click).
    """
    # START_BLOCK_UI_GENERATE: [Тест контроллера генерации]
    df = on_generate_click(A=3.0, B=1.0, C=0.0, D=0.0, x_min=-1, x_max=1)
    assert not df.empty
    assert len(df) == 100
    # END_BLOCK_UI_GENERATE
    
    # START_BLOCK_UI_DRAW: [Тест контроллера отрисовки]
    fig = on_draw_click()
    assert fig is not None
    assert hasattr(fig, 'data')
    # END_BLOCK_UI_DRAW
# END_FUNCTION_test_ui_headless

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """Инициализация счетчика перед началом сессии."""
    update_test_counter(False)

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """Сброс или инкремент счетчика после завершения сессии."""
    update_test_counter(exitstatus == 0)
