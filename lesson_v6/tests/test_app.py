# FILE: lesson_v6/tests/test_app.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Комплексные тесты для Lesson 6 с генерацией семантического контекста.
# SCOPE: Backend & LDD Test, CLI Smoke Test, UI Headless Test.
# INPUT: Фикстуры pytest, аргументы командной строки для CLI.
# OUTPUT: Результаты тестов с логами уровня [IMP:7-10].
# KEYWORDS:[DOMAIN(8): Testing; CONCEPT(7): Pytest; TECH(9): Subprocess]
# LINKS:[TESTS(8): config_manager, database_manager, parabola_logic, ui_controller, cli]
# END_MODULE_CONTRACT
#
# START_INVARIANTS:
# - Все тесты используют изолированные временные файлы.
# - Тесты CLI проверяют exit code 0.
# - Тесты UI проверяют возвращаемые типы без запуска сервера.
# END_INVARIANTS
#
# START_RATIONALE:
# Q: Почему используется caplog для логов?
# A: caplog позволяет перехватывать и проверять логи в тестах, что обеспечивает семантический контекст для отладки.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание комплексных тестов с LDD 2.0 логированием.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# TEST 10[Тестирование загрузки конфигурации] => test_load_config
# TEST 10[Тестирование сохранения конфигурации] => test_save_config
# TEST 10[Тестирование инициализации БД] => test_initialize_database
# TEST 10[Тестирование сохранения и загрузки точек] => test_save_and_load_points
# TEST 10[Тестирование расчета точек параболы] => test_calculate_parabola_points
# TEST 10[CLI Smoke Test: команда generate] => test_cli_generate
# TEST 10[CLI Smoke Test: команда export-csv] => test_cli_export_csv
# TEST 10[UI Headless Test: генерация данных] => test_ui_generate_data_handler
# TEST 10[UI Headless Test: построение графика] => test_ui_draw_graph_handler
# END_MODULE_MAP
#
# START_USE_CASES:
# -[test_load_config]: System (Test) -> VerifyConfigLoad -> ConfigLoadedSuccessfully
# -[test_cli_generate]: System (Test) -> VerifyCLI -> CLICommandExecuted
# -[test_ui_generate_data_handler]: System (Test) -> VerifyUIHandler -> UIHandlerWorks
# END_USE_CASES

import pytest
import subprocess
import sys
import os
import tempfile
import shutil
import re
import pandas as pd

# Импорт модулей проекта
from lesson_v6 import CONFIG_PATH, DB_PATH, LOG_PATH
from lesson_v6.src.config_manager import load_config, save_config
from lesson_v6.src.database_manager import initialize_database, save_points, load_points
from lesson_v6.src.parabola_logic import calculate_parabola_points
from lesson_v6.src.ui_controller import generate_data_handler, draw_graph_handler

# START_FIXTURE_temp_dir
# START_CONTRACT:
# PURPOSE: Создание временной директории для изолированного тестирования.
# INPUTS: Отсутствуют.
# OUTPUTS: 
# - str - Путь к временной директории
# SIDE_EFFECTS: Создает временную директорию.
# KEYWORDS:[PATTERN(6): Fixture; CONCEPT(8): Isolation]
# END_CONTRACT
@pytest.fixture
def temp_dir():
    """Создает временную директорию для тестов."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)
# END_FIXTURE_temp_dir

# START_FIXTURE_temp_config_path
# START_CONTRACT:
# PURPOSE: Создание временного файла конфигурации.
# INPUTS: 
# - [Временная директория] => temp_dir: str
# OUTPUTS: 
# - str - Путь к временному файлу конфигурации
# SIDE_EFFECTS: Создает временный файл конфигурации.
# KEYWORDS:[PATTERN(6): Fixture; CONCEPT(8): TestSetup]
# END_CONTRACT
@pytest.fixture
def temp_config_path(temp_dir):
    """Создает временный файл конфигурации."""
    config_path = os.path.join(temp_dir, "config.json")
    default_config = {"a": 1.0, "c": 0.0, "x_min": -10.0, "x_max": 10.0}
    save_config(default_config, config_path)
    return config_path
# END_FIXTURE_temp_config_path

# START_FIXTURE_temp_db_path
# START_CONTRACT:
# PURPOSE: Создание временного файла базы данных.
# INPUTS: 
# - [Временная директория] => temp_dir: str
# OUTPUTS: 
# - str - Путь к временному файлу базы данных
# SIDE_EFFECTS: Создает временный файл базы данных.
# KEYWORDS:[PATTERN(6): Fixture; CONCEPT(8): TestSetup]
# END_CONTRACT
@pytest.fixture
def temp_db_path(temp_dir):
    """Создает временную базу данных."""
    db_path = os.path.join(temp_dir, "test.db")
    initialize_database(db_path)
    return db_path
# END_FIXTURE_temp_db_path

# ==================== Backend & LDD Tests ====================

# START_TEST_test_load_config
# START_CONTRACT:
# PURPOSE: Тестирование загрузки конфигурации с проверкой логов.
# INPUTS:
# - [Временный путь к конфигу] => temp_config_path: str
# - [Фикстура caplog] => caplog
# OUTPUTS:
# - None
# SIDE_EFFECTS: Отсутствуют.
# KEYWORDS:[PATTERN(6): UnitTest; CONCEPT(8): LogVerification]
# END_CONTRACT
def test_load_config(temp_config_path, caplog):
    """Тестирует загрузку конфигурации с проверкой логов уровня [IMP:7-10]."""
    
    # START_BLOCK_EXECUTE_TEST: [Выполнение теста]
    with caplog.at_level(logging.INFO):
        config = load_config(temp_config_path)
        
        # Проверка данных
        assert config["a"] == 1.0
        assert config["c"] == 0.0
        assert config["x_min"] == -10.0
        assert config["x_max"] == 10.0
        
        # Проверка логов уровня [IMP:7-10]
        high_imp_logs = [record for record in caplog.records
                         if "[IMP:7]" in record.message or "[IMP:8]" in record.message
                         or "[IMP:9]" in record.message or "[IMP:10]" in record.message]
        assert len(high_imp_logs) > 0, "Ожидаются логи уровня [IMP:7-10]"
        
        # Проверка формата лога
        log_message = high_imp_logs[0].message
        assert "[load_config]" in log_message
        assert "[READ_CONFIG_FILE]" in log_message
    # END_BLOCK_EXECUTE_TEST
# END_TEST_test_load_config

# START_TEST_test_save_config
# START_CONTRACT:
# PURPOSE: Тестирование сохранения конфигурации с проверкой логов.
# INPUTS: 
# - [Временная директория] => temp_dir: str
# - [Фикстура caplog] => caplog
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Создает временный файл конфигурации.
# KEYWORDS:[PATTERN(6): UnitTest; CONCEPT(8): LogVerification]
# END_CONTRACT
def test_save_config(temp_dir, caplog):
    """Тестирует сохранение конфигурации с проверкой логов уровня [IMP:7-10]."""
    
    # START_BLOCK_EXECUTE_TEST: [Выполнение теста]
    config_path = os.path.join(temp_dir, "test_config.json")
    test_config = {"a": 2.0, "c": 1.0, "x_min": -5.0, "x_max": 5.0}
    
    with caplog.at_level(logging.INFO):
        save_config(test_config, config_path)
        
        # Проверка сохраненных данных
        loaded_config = load_config(config_path)
        assert loaded_config == test_config
        
        # Проверка логов уровня [IMP:7-10]
        high_imp_logs = [record for record in caplog.records 
                         if "[IMP:7]" in record.message or "[IMP:8]" in record.message 
                         or "[IMP:9]" in record.message or "[IMP:10]" in record.message]
        assert len(high_imp_logs) > 0, "Ожидаются логи уровня [IMP:7-10]"
        
        # Проверка формата лога
        log_message = high_imp_logs[0].message
        assert "[save_config]" in log_message
        assert "[WRITE_CONFIG_FILE]" in log_message
    # END_BLOCK_EXECUTE_TEST
# END_TEST_test_save_config

# START_TEST_test_initialize_database
# START_CONTRACT:
# PURPOSE: Тестирование инициализации базы данных с проверкой логов.
# INPUTS: 
# - [Временная директория] => temp_dir: str
# - [Фикстура caplog] => caplog
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Создает временную базу данных.
# KEYWORDS:[PATTERN(6): UnitTest; CONCEPT(8): LogVerification]
# END_CONTRACT
def test_initialize_database(temp_dir, caplog):
    """Тестирует инициализацию базы данных с проверкой логов уровня [IMP:7-10]."""
    
    # START_BLOCK_EXECUTE_TEST: [Выполнение теста]
    db_path = os.path.join(temp_dir, "test.db")
    
    with caplog.at_level(logging.INFO):
        initialize_database(db_path)
        
        # Проверка существования файла БД
        assert os.path.exists(db_path)
        
        # Проверка логов уровня [IMP:7-10]
        high_imp_logs = [record for record in caplog.records 
                         if "[IMP:7]" in record.message or "[IMP:8]" in record.message 
                         or "[IMP:9]" in record.message or "[IMP:10]" in record.message]
        assert len(high_imp_logs) > 0, "Ожидаются логи уровня [IMP:7-10]"
        
        # Проверка формата лога
        log_message = high_imp_logs[0].message
        assert "[initialize_database]" in log_message
        assert "[CONNECT_AND_CREATE]" in log_message
    # END_BLOCK_EXECUTE_TEST
# END_TEST_test_initialize_database

# START_TEST_test_save_and_load_points
# START_CONTRACT:
# PURPOSE: Тестирование сохранения и загрузки точек с проверкой логов.
# INPUTS: 
# - [Временный путь к БД] => temp_db_path: str
# - [Фикстура caplog] => caplog
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Сохраняет точки в временную БД.
# KEYWORDS:[PATTERN(6): IntegrationTest; CONCEPT(8): LogVerification]
# END_CONTRACT
def test_save_and_load_points(temp_db_path, caplog):
    """Тестирует сохранение и загрузку точек с проверкой логов уровня [IMP:7-10]."""
    
    # START_BLOCK_EXECUTE_TEST: [Выполнение теста]
    test_points = [
        {"x": -1.0, "y": 1.0},
        {"x": 0.0, "y": 0.0},
        {"x": 1.0, "y": 1.0}
    ]
    
    with caplog.at_level(logging.INFO):
        save_points(test_points, temp_db_path)
        loaded_points = load_points(temp_db_path)
        
        # Проверка данных
        assert len(loaded_points) == 3
        assert loaded_points[0]["x"] == -1.0
        assert loaded_points[0]["y"] == 1.0
        
        # Проверка логов уровня [IMP:7-10]
        high_imp_logs = [record for record in caplog.records 
                         if "[IMP:7]" in record.message or "[IMP:8]" in record.message 
                         or "[IMP:9]" in record.message or "[IMP:10]" in record.message]
        assert len(high_imp_logs) > 0, "Ожидаются логи уровня [IMP:7-10]"
        
        # Проверка формата лога
        log_messages = [record.message for record in high_imp_logs]
        assert any("[save_points]" in msg for msg in log_messages)
        assert any("[load_points]" in msg for msg in log_messages)
    # END_BLOCK_EXECUTE_TEST
# END_TEST_test_save_and_load_points

# START_TEST_test_calculate_parabola_points
# START_CONTRACT:
# PURPOSE: Тестирование расчета точек параболы с проверкой логов.
# INPUTS: 
# - [Фикстура caplog] => caplog
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Отсутствуют.
# KEYWORDS:[PATTERN(6): UnitTest; CONCEPT(8): LogVerification]
# END_CONTRACT
def test_calculate_parabola_points(caplog):
    """Тестирует расчет точек параболы с проверкой логов уровня [IMP:7-10]."""
    
    # START_BLOCK_EXECUTE_TEST: [Выполнение теста]
    with caplog.at_level(logging.INFO):
        points = calculate_parabola_points(a=1.0, c=0.0, x_min=-2.0, x_max=2.0, step=1.0)
        
        # Проверка данных
        assert len(points) == 5  # -2, -1, 0, 1, 2
        assert points[0]["x"] == -2.0
        assert points[0]["y"] == 4.0  # y = 1*(-2)^2 + 0 = 4
        
        # Проверка логов уровня [IMP:7-10]
        high_imp_logs = [record for record in caplog.records 
                         if "[IMP:7]" in record.message or "[IMP:8]" in record.message 
                         or "[IMP:9]" in record.message or "[IMP:10]" in record.message]
        assert len(high_imp_logs) > 0, "Ожидаются логи уровня [IMP:7-10]"
        
        # Проверка формата лога
        log_message = high_imp_logs[0].message
        assert "[calculate_parabola_points]" in log_message
        assert "[CALCULATE_POINTS]" in log_message
    # END_BLOCK_EXECUTE_TEST
# END_TEST_test_calculate_parabola_points

# ==================== CLI Smoke Tests ====================

# START_TEST_test_cli_generate
# START_CONTRACT:
# PURPOSE: CLI Smoke Test для команды generate.
# INPUTS: Отсутствуют.
# OUTPUTS:
# - None
# SIDE_EFFECTS: Выполняет CLI команду через subprocess.
# KEYWORDS:[PATTERN(6): SmokeTest; CONCEPT(8): Subprocess]
# END_CONTRACT
def test_cli_generate():
    """Тестирует CLI команду generate через subprocess."""
    
    # START_BLOCK_EXECUTE_TEST: [Выполнение теста]
    result = subprocess.run(
        [sys.executable, "-m", "lesson_v6.src.cli", "generate"],
        capture_output=True,
        text=True,
        cwd="c:/Users/ivano/PythonProjects/NEW_LESSONS"
    )
    
    # Проверка exit code
    assert result.returncode == 0, f"CLI команда завершилась с ошибкой: {result.stderr}"
    
    # Проверка вывода
    assert "[OK] Сгенерировано" in result.stdout or "Generated" in result.stdout
    # END_BLOCK_EXECUTE_TEST
# END_TEST_test_cli_generate

# START_TEST_test_cli_export_csv
# START_CONTRACT:
# PURPOSE: CLI Smoke Test для команды export-csv.
# INPUTS: Отсутствует.
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Выполняет CLI команду через subprocess, создает CSV файл.
# KEYWORDS:[PATTERN(6): SmokeTest; CONCEPT(8): Subprocess]
# END_CONTRACT
def test_cli_export_csv(temp_dir):
    """Тестирует CLI команду export-csv через subprocess."""
    
    # START_BLOCK_EXECUTE_TEST: [Выполнение теста]
    csv_path = os.path.join(temp_dir, "test_export.csv")
    
    # Сначала генерируем данные
    subprocess.run(
        [sys.executable, "-m", "lesson_v6.src.cli", "generate"],
        capture_output=True,
        text=True,
        cwd="c:/Users/ivano/PythonProjects/NEW_LESSONS"
    )
    
    # Затем экспортируем
    result = subprocess.run(
        [sys.executable, "-m", "lesson_v6.src.cli", "export-csv", "--out", csv_path],
        capture_output=True,
        text=True,
        cwd="c:/Users/ivano/PythonProjects/NEW_LESSONS"
    )
    
    # Проверка exit code
    assert result.returncode == 0, f"CLI команда завершилась с ошибкой: {result.stderr}"
    
    # Проверка создания файла
    assert os.path.exists(csv_path), "CSV файл не был создан"
    
    # Проверка содержимого CSV
    df = pd.read_csv(csv_path)
    assert "x" in df.columns
    assert "y" in df.columns
    assert len(df) > 0
    # END_BLOCK_EXECUTE_TEST
# END_TEST_test_cli_export_csv

# ==================== UI Headless Tests ====================

# START_TEST_test_ui_generate_data_handler
# START_CONTRACT:
# PURPOSE: UI Headless Test для обработчика генерации данных.
# INPUTS:
# - [Фикстура caplog] => caplog
# OUTPUTS:
# - None
# SIDE_EFFECTS: Обновляет config.json и БД.
# KEYWORDS:[PATTERN(6): HeadlessTest; CONCEPT(8): MockUI]
# END_CONTRACT
def test_ui_generate_data_handler(caplog):
    """Тестирует UI обработчик генерации данных без запуска сервера."""
    
    # START_BLOCK_EXECUTE_TEST: [Выполнение теста]
    with caplog.at_level(logging.INFO):
        df, message = generate_data_handler(a=1.0, c=0.0, x_min=-2.0, x_max=2.0)
        
        # Проверка возвращаемых типов
        assert isinstance(df, pd.DataFrame)
        assert isinstance(message, str)
        assert "[OK] Сгенерировано" in message
        
        # Проверка данных DataFrame
        assert "x" in df.columns
        assert "y" in df.columns
        assert len(df) > 0
        
        # Проверка логов уровня [IMP:7-10]
        high_imp_logs = [record for record in caplog.records
                         if "[IMP:7]" in record.message or "[IMP:8]" in record.message
                         or "[IMP:9]" in record.message or "[IMP:10]" in record.message]
        assert len(high_imp_logs) > 0, "Ожидаются логи уровня [IMP:7-10]"
        
        # Проверка формата лога
        log_messages = [record.message for record in high_imp_logs]
        assert any("[generate_data_handler]" in msg for msg in log_messages)
    # END_BLOCK_EXECUTE_TEST
# END_TEST_test_ui_generate_data_handler

# START_TEST_test_ui_draw_graph_handler
# START_CONTRACT:
# PURPOSE: UI Headless Test для обработчика построения графика.
# INPUTS: 
# - [Фикстура caplog] => caplog
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Отсутствуют (только чтение из БД).
# KEYWORDS:[PATTERN(6): HeadlessTest; CONCEPT(8): MockUI]
# END_CONTRACT
def test_ui_draw_graph_handler(caplog):
    """Тестирует UI обработчик построения графика без запуска сервера."""
    
    # START_BLOCK_EXECUTE_TEST: [Выполнение теста]
    # Сначала генерируем данные
    generate_data_handler(a=1.0, c=0.0, x_min=-2.0, x_max=2.0)
    
    with caplog.at_level(logging.INFO):
        fig = draw_graph_handler()
        
        # Проверка возвращаемого типа
        assert fig is not None
        assert hasattr(fig, 'data')
        assert hasattr(fig, 'layout')
        
        # Проверка логов уровня [IMP:7-10]
        high_imp_logs = [record for record in caplog.records 
                         if "[IMP:7]" in record.message or "[IMP:8]" in record.message 
                         or "[IMP:9]" in record.message or "[IMP:10]" in record.message]
        assert len(high_imp_logs) > 0, "Ожидаются логи уровня [IMP:7-10]"
        
        # Проверка формата лога
        log_messages = [record.message for record in high_imp_logs]
        assert any("[draw_graph_handler]" in msg for msg in log_messages)
    # END_BLOCK_EXECUTE_TEST
# END_TEST_test_ui_draw_graph_handler

# Импорт logging для caplog
import logging
