# FILE: lesson_15/tests/test_app.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Тестирование бэкенда, CLI и UI Lesson_15.
# SCOPE: Backend, CLI Smoke, UI Headless.
# KEYWORDS: [DOMAIN(8): Testing; TECH(7): Pytest; CONCEPT(9): AntiLoop]
# END_MODULE_CONTRACT

import pytest
import os
import json
import sqlite3
import subprocess
import pandas as pd
import plotly.graph_objects as go
import sys

# Добавляем корень проекта в PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from lesson_15.src.config_manager import ConfigManager
from lesson_15.src.database_manager import DatabaseManager
from lesson_15.src.parabola_logic import generate_points
from lesson_15.src.ui_controller import on_generate, on_draw

# START_BLOCK_ANTI_LOOP: [Протокол защиты от зацикливания]
TEST_COUNTER_FILE = ".test_counter_15.json"

def update_test_counter(success: bool):
    """Обновляет счетчик попыток и выводит чек-лист при неудачах."""
    if not os.path.exists(TEST_COUNTER_FILE):
        counter = {"attempts": 0}
    else:
        with open(TEST_COUNTER_FILE, 'r') as f:
            counter = json.load(f)
    
    if success:
        counter["attempts"] = 0
    else:
        counter["attempts"] += 1
    
    # Вывод статуса попыток ВСЕГДА при запуске (если попыток > 0)
    if counter["attempts"] > 0:
        print(f"\n[ANTI-LOOP] Текущее количество неудачных попыток: {counter['attempts']}")
        
        if counter["attempts"] >= 1:
            print("\n--- CHECKLIST ТИПОВЫХ ОШИБОК ---")
            print("- [ ] Проверка путей и cwd в subprocess (cli.py path).")
            print("- [ ] Проверка PYTHONPATH и импортов (sys.path).")
            print("- [ ] Соответствие версий библиотек через verify_env.py.")
            print("- [ ] Наличие необходимых файлов данных/конфигов (config.json).")
            print("- [ ] EXPERIENCE: Проверьте, не блокирует ли антивирус/защитник создание .db файлов.")

        if counter["attempts"] == 3:
            print("\n[ADVICE] Используйте MCP 'tavily' или 'Context7' для поиска решения проблемы.")
            
        if counter["attempts"] == 4:
            print("\n[WARNING] ВНИМАНИЕ: Риск зацикливания! Сделайте паузу и проведите рефлексию.")
            print("Не используете ли вы одну и ту же ошибочную стратегию? Рассмотрите альтернативы.")

        if counter["attempts"] >= 5:
            print("\n[CRITICAL] КРИТИЧЕСКАЯ ОШИБКА: Обнаружено зацикливание агента. ОСТАНОВИТЕСЬ.")
            print("Сформируйте запрос на помощь оператору. Запрос должен содержать:")
            print("1) Описание проблемы, 2) Предпринятые шаги, 3) Выдержки из логов, 4) План консультации.")
    
    with open(TEST_COUNTER_FILE, 'w') as f:
        json.dump(counter, f)
# END_BLOCK_ANTI_LOOP

# START_BLOCK_FIXTURES: [Фикстуры для тестов]
@pytest.fixture
def temp_dir(tmpdir):
    """Создает временную директорию для тестов."""
    return tmpdir

@pytest.fixture
def config_mgr(temp_dir):
    path = os.path.join(temp_dir, "config.json")
    return ConfigManager(path)

@pytest.fixture
def db_mgr(temp_dir):
    path = os.path.join(temp_dir, "test.db")
    return DatabaseManager(path)
# END_BLOCK_FIXTURES

# START_FUNCTION_test_backend_logic
# START_CONTRACT:
# PURPOSE: Проверка расчета параболы и сохранения в БД.
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def test_backend_logic(config_mgr, db_mgr, caplog):
    """Тест логики расчета и записи в БД с выводом логов IMP:7-10."""
    # START_BLOCK_TEST_CALC: [Проверка расчета]
    df = generate_points(a=2.0, c=5.0, x_min=-5, x_max=5, num_points=10)
    assert len(df) == 10
    assert df.iloc[0]["y"] == 2.0 * ((-5)**2) + 5.0
    # END_BLOCK_TEST_CALC

    # START_BLOCK_TEST_DB: [Проверка БД]
    db_mgr.save_points(df)
    df_loaded = db_mgr.get_points()
    assert len(df_loaded) == 10
    # END_BLOCK_TEST_DB

    # Вывод логов IMP:7-10 в консоль
    print("\n--- LDD Telemetry (IMP:7-10) ---")
    for record in caplog.records:
        if "[IMP:7]" in record.message or "[IMP:8]" in record.message or "[IMP:9]" in record.message or "[IMP:10]" in record.message:
            print(record.message)
# END_FUNCTION_test_backend_logic

# START_FUNCTION_test_cli_smoke
# START_CONTRACT:
# PURPOSE: Проверка CLI через subprocess.
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def test_cli_smoke(temp_dir):
    """Smoke тест CLI: generate и export-csv."""
    # START_BLOCK_CLI_GENERATE: [Команда generate]
    cli_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/cli.py"))
    src_dir = os.path.dirname(cli_path)
    lesson_dir = os.path.dirname(src_dir)
    
    # Создаем дефолтный конфиг в папке урока (где его ждет cli.py)
    config_path = os.path.join(lesson_dir, "config.json")
    with open(config_path, 'w') as f:
        json.dump({"a": 1, "c": 0, "x_min": -10, "x_max": 10}, f)
    
    # Запуск generate
    result = subprocess.run(
        [sys.executable, cli_path, "generate"],
        capture_output=True,
        text=True,
        cwd=src_dir
    )
    print(f"\nCLI Generate STDOUT: {result.stdout}")
    print(f"CLI Generate STDERR: {result.stderr}")
    assert result.returncode == 0
    # END_BLOCK_CLI_GENERATE

    # START_BLOCK_CLI_EXPORT: [Команда export-csv]
    csv_out = os.path.join(temp_dir, "output.csv")
    result = subprocess.run(
        [sys.executable, cli_path, "export-csv", "--out", csv_out],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(cli_path)
    )
    assert result.returncode == 0
    assert os.path.exists(csv_out)
    # END_BLOCK_CLI_EXPORT
# END_FUNCTION_test_cli_smoke

# START_FUNCTION_test_ui_headless
# START_CONTRACT:
# PURPOSE: Проверка обработчиков Gradio без запуска сервера.
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def test_ui_headless(config_mgr, db_mgr):
    """Headless тест UI контроллеров."""
    # START_BLOCK_UI_GENERATE: [Тест on_generate]
    df = on_generate(a=1.0, c=2.0, x_min=-5, x_max=5, config_mgr=config_mgr, db_mgr=db_mgr)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    # END_BLOCK_UI_GENERATE

    # START_BLOCK_UI_DRAW: [Тест on_draw]
    fig = on_draw(db_mgr)
    assert isinstance(fig, go.Figure)
    # END_BLOCK_UI_DRAW
# END_FUNCTION_test_ui_headless

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """Вызывается перед началом тестов."""
    update_test_counter(False) # Увеличиваем счетчик при старте

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """Вызывается после завершения тестов."""
    if exitstatus == 0:
        update_test_counter(True) # Сбрасываем при успехе

if __name__ == "__main__":
    # При прямом запуске через python
    update_test_counter(False)
    ret = pytest.main([__file__, "-s"])
    if ret == 0:
        update_test_counter(True)
# END_FUNCTION_test_app.py
