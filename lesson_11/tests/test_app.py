# FILE:lesson_11/tests/test_app.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Комплексное тестирование приложения Lesson 11 (Backend, CLI, UI).
# SCOPE:Модульные тесты логики, интеграционные тесты БД и конфига, дымовые тесты CLI, headless тесты UI.
# INPUT:Тестовые данные для параболы, временные файлы БД и конфига.
# OUTPUT:Отчеты pytest, логи LDD в консоль.
# KEYWORDS:[DOMAIN(8): Testing; CONCEPT(7): LDD_Verification; TECH(9): pytest, subprocess]
# LINKS:[USES_API(8): pytest, pandas, plotly; READS_DATA_FROM(7): src.parabola_logic, src.cli, src.ui_controller]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется фикстура для очистки файлов?
# A: Чтобы тесты были изолированными и не зависели от состояния предыдущих запусков или реальных данных приложения.
# Q: Зачем проверять caplog на наличие [IMP:7-10]?
# A: Это требование LDD 2.0 для верификации того, что критические бизнес-события и "Belief State" фиксируются в логах.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание комплексных тестов с семантической разметкой.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Фикстура для подготовки окружения тестов] => setup_test_env
# FUNC 10[Тест бэкенд логики и LDD логов] => test_backend_and_ldd
# FUNC 10[Дымовой тест CLI интерфейса] => test_cli_smoke
# FUNC 10[Headless тест обработчиков UI] => test_ui_headless
# END_MODULE_MAP

import pytest
import os
import subprocess
import pandas as pd
import plotly.graph_objects as go
import logging
import sys

# Добавляем корень проекта в sys.path для корректных импортов
sys.path.append(os.getcwd())

from lesson_11.src.parabola_logic import calculate_points
from lesson_11.src.config_manager import load_config, save_config
from lesson_11.src.database_manager import init_db, save_points, get_points
from lesson_11.src.ui_controller import handle_generate, handle_draw

# START_BLOCK_FIXTURES: [Настройка тестового окружения]
@pytest.fixture(autouse=True)
def setup_test_env():
    """
    Фикстура для подготовки чистого окружения перед каждым тестом.
    Удаляет временные файлы БД и конфига, чтобы избежать интерференции.
    """
    test_db = "lesson_11/parabola_11.db"
    test_config = "lesson_11/config.json"
    test_log = "lesson_11/app_11.log"
    
    # Очистка перед тестом
    # BUG_FIX_CONTEXT: Удаление лог-файла в Windows часто вызывает PermissionError,
    # если он открыт другим процессом или текущим логгером.
    # Ограничиваемся очисткой БД и конфига.
    for f in [test_db, test_config]:
        if os.path.exists(f):
            try:
                os.remove(f)
            except PermissionError:
                pass
            
    yield
    
    # Очистка после теста (опционально)
    # for f in [test_db, test_config]:
    #     if os.path.exists(f):
    #         os.remove(f)
# END_BLOCK_FIXTURES

# START_FUNCTION_test_backend_and_ldd
# START_CONTRACT:
# PURPOSE:Проверка бэкенд компонентов и наличия LDD логов высокой важности.
# INPUTS: 
# - pytest fixture => caplog: Захват логов
# OUTPUTS: None
# SIDE_EFFECTS: Создает записи в логах, файлы БД и конфига.
# KEYWORDS:[PATTERN(8): LDD_Test; CONCEPT(9): SemanticVerification]
# COMPLEXITY_SCORE: 6[Интеграционный тест нескольких модулей с анализом логов.]
# END_CONTRACT
def test_backend_and_ldd(caplog):
    """
    Тест проверяет связку parabola_logic, config_manager и database_manager.
    Особое внимание уделяется проверке наличия логов с уровнем важности IMP:7-10,
    что подтверждает работу системы в режиме Log Driven Development.
    """
    caplog.set_level(logging.DEBUG)
    
    # START_BLOCK_LOGIC_TEST: [Проверка математической логики]
    points = calculate_points(a=2.0, c=5.0, x_min=-2.0, x_max=2.0, step=1.0)
    # Ожидаемые точки: (-2, 13), (-1, 7), (0, 5), (1, 7), (2, 13)
    assert len(points) == 5
    assert points[2] == (0.0, 5.0)
    print(f"\n[TEST][IMP:10][test_backend_and_ldd][LOGIC] Математика проверена. Точек: {len(points)}")
    # END_BLOCK_LOGIC_TEST
    
    # START_BLOCK_CONFIG_TEST: [Проверка менеджера конфигурации]
    test_conf = {"a": 2.0, "c": 5.0, "x_min": -2.0, "x_max": 2.0}
    save_config(test_conf)
    loaded_conf = load_config()
    assert loaded_conf["a"] == 2.0
    assert loaded_conf["x_max"] == 2.0
    # END_BLOCK_CONFIG_TEST
    
    # START_BLOCK_DB_TEST: [Проверка менеджера БД]
    init_db()
    save_points(points)
    db_points = get_points()
    assert len(db_points) == 5
    assert db_points[0][0] == -2.0
    # END_BLOCK_DB_TEST
    
    # START_BLOCK_LDD_VERIFICATION: [Семантическая верификация трассы логов]
    # Ищем логи высокой важности [IMP:7-10]
    important_logs = [record.message for record in caplog.records if any(f"IMP:{i}" in record.message for i in range(7, 11))]
    
    print("\n--- LDD HIGH IMPORTANCE LOGS SELECTION ---")
    for log in important_logs:
        print(f"[LDD_VERIFY] {log}")
    
    # Проверка наличия критических маркеров
    assert any("BeliefState" in log for log in important_logs), "Отсутствует лог BeliefState (IMP:9-10)"
    assert any("GoalReached" in log or "Success" in log for log in important_logs), "Отсутствует лог завершения цели"
    # END_BLOCK_LDD_VERIFICATION
# END_FUNCTION_test_backend_and_ldd

# START_FUNCTION_test_cli_smoke
# START_CONTRACT:
# PURPOSE:Дымовое тестирование CLI интерфейса через subprocess.
# INPUTS: None
# OUTPUTS: None
# SIDE_EFFECTS: Выполняет команды в отдельном процессе, создает файлы.
# KEYWORDS:[PATTERN(7): SmokeTest; CONCEPT(8): CLI_Verification]
# COMPLEXITY_SCORE: 5[Запуск внешних процессов и проверка кодов возврата.]
# END_CONTRACT
def test_cli_smoke():
    """
    Тест проверяет работоспособность CLI модуля. Выполняются команды 'generate'
    и 'export-csv'. Критерий успеха - код возврата 0 и физическое наличие
    созданного CSV файла.
    """
    # START_BLOCK_CLI_GENERATE: [Тест команды generate]
    # Сначала создадим конфиг, чтобы было на чем генерировать
    save_config({"a": 1.0, "c": 0.0, "x_min": -5.0, "x_max": 5.0})
    
    # BUG_FIX_CONTEXT: Добавляем текущую директорию в PYTHONPATH для subprocess,
    # чтобы импорты вида 'from lesson_11.src...' работали корректно.
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd() + os.pathsep + env.get("PYTHONPATH", "")
    
    cmd_gen = [sys.executable, "lesson_11/src/cli.py", "generate"]
    result_gen = subprocess.run(cmd_gen, capture_output=True, text=True, env=env)
    
    print(f"\n[CLI_OUT][generate] {result_gen.stdout}")
    assert result_gen.returncode == 0, f"CLI generate failed: {result_gen.stderr}"
    # END_BLOCK_CLI_GENERATE
    
    # START_BLOCK_CLI_EXPORT: [Тест команды export-csv]
    csv_path = "lesson_11/test_export.csv"
    if os.path.exists(csv_path):
        os.remove(csv_path)
        
    cmd_exp = [sys.executable, "lesson_11/src/cli.py", "export-csv", "--out", csv_path]
    result_exp = subprocess.run(cmd_exp, capture_output=True, text=True, env=env)
    
    print(f"[CLI_OUT][export-csv] {result_exp.stdout}")
    assert result_exp.returncode == 0, f"CLI export-csv failed: {result_exp.stderr}"
    assert os.path.exists(csv_path), "CSV файл не был создан"
    
    # Проверка содержимого CSV
    df = pd.read_csv(csv_path)
    assert not df.empty
    assert "x" in df.columns and "y" in df.columns
    
    # Чистка
    if os.path.exists(csv_path):
        os.remove(csv_path)
    # END_BLOCK_CLI_EXPORT
# END_FUNCTION_test_cli_smoke

# START_FUNCTION_test_ui_headless
# START_CONTRACT:
# PURPOSE:Тестирование функций-обработчиков UI без запуска сервера Gradio.
# INPUTS: None
# OUTPUTS: None
# SIDE_EFFECTS: Взаимодействие с БД и конфигом.
# KEYWORDS:[PATTERN(7): HeadlessTest; CONCEPT(8): UI_Logic_Verification]
# COMPLEXITY_SCORE: 5[Имитация вызовов UI и проверка типов возвращаемых данных.]
# END_CONTRACT
def test_ui_headless():
    """
    Тест имитирует действия пользователя в интерфейсе Gradio, вызывая напрямую
    функции handle_generate и handle_draw. Проверяется корректность типов
    возвращаемых данных (DataFrame для таблицы и Figure для графика), что
    гарантирует совместимость с компонентами Gradio.
    """
    # START_BLOCK_UI_GENERATE: [Имитация нажатия кнопки Generate]
    init_db() # Нужна для handle_generate
    df_result = handle_generate(a=1.0, c=2.0, x_min=-10.0, x_max=10.0)
    
    assert isinstance(df_result, pd.DataFrame), "handle_generate должен возвращать pandas.DataFrame"
    assert len(df_result) > 0
    print(f"\n[UI_TEST][handle_generate] DataFrame получен. Строк: {len(df_result)}")
    # END_BLOCK_UI_GENERATE
    
    # START_BLOCK_UI_DRAW: [Имитация нажатия кнопки Draw]
    fig_result = handle_draw()
    
    assert isinstance(fig_result, go.Figure), "handle_draw должен возвращать plotly.graph_objects.Figure"
    # Проверка наличия данных на графике
    assert len(fig_result.data) > 0, "График не содержит данных (traces)"
    assert fig_result.layout.title.text == 'Parabola Visualization: y = ax^2 + c'
    print(f"[UI_TEST][handle_draw] Plotly Figure получена и проверена.")
    # END_BLOCK_UI_DRAW
# END_FUNCTION_test_ui_headless
