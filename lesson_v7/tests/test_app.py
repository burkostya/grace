# FILE: lesson_v7/tests/test_app.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Комплексные тесты для приложения lesson_v7.
# SCOPE: Проверка бизнес-логики, CLI интерфейса и UI контроллеров с LDD логированием.
# INPUT: Отсутствует (запуск через pytest).
# OUTPUT: Результаты тестов с выводом LDD логов [IMP:7-10].
# KEYWORDS:[DOMAIN(9): Testing; CONCEPT(8): LDDTelemetry; TECH(9): Pytest]
# LINKS:[TESTS(10): config_manager; TESTS(10): parabola_logic; TESTS(10): database_manager; TESTS(10): cli; TESTS(10): ui_controller]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему тесты используют caplog для вывода логов?
# A: Это обеспечивает телеметрию LDD - при падении теста мы видим реальный контекст выполнения через логи [IMP:7-10].
# Q: Почему тесты CLI используют subprocess?
# A: Это smoke test - проверка работоспособности CLI как внешней программы, а не только как модуля Python.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание комплексных тестов.]
# END_CHANGE_SUMMARY

import logging
import os
import subprocess
import sys
import tempfile
from pathlib import Path
import pytest

# Импорт модулей приложения
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lesson_v7.src.config_manager import load_config, save_config
from lesson_v7.src.parabola_logic import generate_points
from lesson_v7.src.database_manager import init_database, save_points, load_points
from lesson_v7.src.cli import main as cli_main
from lesson_v7.src.ui_controller import (
    generate_data_handler,
    draw_graph_handler,
    load_table_handler
)

# Настройка логирования для тестов
logging.basicConfig(level=logging.DEBUG)

# ============================================================================
# ТЕСТЫ БЭКЕНДА С LDD ТЕЛЕМЕТРИЕЙ
# ============================================================================

# START_TEST_TEST_CONFIG_MANAGER
def test_config_manager_load_and_save(caplog):
    """Тест загрузки и сохранения конфигурации с LDD логированием."""
    caplog.set_level(logging.INFO)
    
    # START_BLOCK_TEMP_CONFIG: [Создание временного файла конфигурации]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_config_path = Path(f.name)
        temp_config_path.write_text('{"a": 2.0, "c": 5.0, "x_min": -5.0, "x_max": 5.0}')
    
    try:
        # START_BLOCK_LOAD_CONFIG: [Загрузка конфигурации]
        config = load_config(temp_config_path)
        assert config['a'] == 2.0
        assert config['c'] == 5.0
        assert config['x_min'] == -5.0
        assert config['x_max'] == 5.0
        # END_BLOCK_LOAD_CONFIG
        
        # START_BLOCK_SAVE_CONFIG: [Сохранение конфигурации]
        new_config = {"a": 3.0, "c": 1.0, "x_min": -10.0, "x_max": 10.0}
        save_config(new_config, temp_config_path)
        loaded_config = load_config(temp_config_path)
        assert loaded_config['a'] == 3.0
        assert loaded_config['c'] == 1.0
        # END_BLOCK_SAVE_CONFIG
        
        # START_BLOCK_CHECK_LOGS: [Проверка LDD логов]
        imp_logs = [record for record in caplog.records if '[IMP:' in record.message]
        assert len(imp_logs) > 0, "Ожидаются логи с уровнем важности [IMP:7-10]"
        
        # Вывод логов для контекста
        for record in imp_logs:
            print(f"\n[LOG] {record.message}")
        # END_BLOCK_CHECK_LOGS
        
    finally:
        # START_BLOCK_CLEANUP: [Очистка временных файлов]
        if temp_config_path.exists():
            temp_config_path.unlink()
        # END_BLOCK_CLEANUP
# END_TEST_TEST_CONFIG_MANAGER

# START_TEST_TEST_PARABOLA_LOGIC
def test_parabola_logic_generate_points(caplog):
    """Тест генерации точек параболы с LDD логированием."""
    caplog.set_level(logging.INFO)
    
    # START_BLOCK_GENERATE_POINTS: [Генерация точек]
    points = generate_points(a=1.0, c=0.0, x_min=-10.0, x_max=10.0, num_points=100)
    
    assert len(points) == 100
    assert points[0][0] == -10.0
    assert points[-1][0] == 10.0
    
    # Проверка первой точки: y = 1*(-10)^2 + 0 = 100
    assert abs(points[0][1] - 100.0) < 0.01
    # END_BLOCK_GENERATE_POINTS
    
    # START_BLOCK_CHECK_LOGS: [Проверка LDD логов]
    imp_logs = [record for record in caplog.records if '[IMP:' in record.message]
    assert len(imp_logs) > 0, "Ожидаются логи с уровнем важности [IMP:7-10]"
    
    # Вывод логов для контекста
    for record in imp_logs:
        print(f"\n[LOG] {record.message}")
    # END_BLOCK_CHECK_LOGS
# END_TEST_TEST_PARABOLA_LOGIC

# START_TEST_TEST_DATABASE_MANAGER
def test_database_manager_save_and_load(caplog):
    """Тест сохранения и загрузки точек в БД с LDD логированием."""
    caplog.set_level(logging.INFO)
    
    # START_BLOCK_TEMP_DB: [Создание временной базы данных]
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        temp_db_path = Path(f.name)
    
    try:
        # START_BLOCK_INIT_DB: [Инициализация БД]
        init_database(temp_db_path)
        # END_BLOCK_INIT_DB
        
        # START_BLOCK_SAVE_POINTS: [Сохранение точек]
        test_points = [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0)]
        save_points(test_points, temp_db_path)
        # END_BLOCK_SAVE_POINTS
        
        # START_BLOCK_LOAD_POINTS: [Загрузка точек]
        loaded_points = load_points(temp_db_path)
        assert len(loaded_points) == 3
        assert loaded_points[0] == (0.0, 0.0)
        assert loaded_points[1] == (1.0, 1.0)
        assert loaded_points[2] == (2.0, 4.0)
        # END_BLOCK_LOAD_POINTS
        
        # START_BLOCK_CHECK_LOGS: [Проверка LDD логов]
        imp_logs = [record for record in caplog.records if '[IMP:' in record.message]
        assert len(imp_logs) > 0, "Ожидаются логи с уровнем важности [IMP:7-10]"
        
        # Вывод логов для контекста
        for record in imp_logs:
            print(f"\n[LOG] {record.message}")
        # END_BLOCK_CHECK_LOGS
        
    finally:
        # START_BLOCK_CLEANUP: [Очистка временных файлов]
        if temp_db_path.exists():
            temp_db_path.unlink()
        # END_BLOCK_CLEANUP
# END_TEST_TEST_DATABASE_MANAGER

# ============================================================================
# SMOKE ТЕСТЫ CLI
# ============================================================================

# START_TEST_TEST_CLI_GENERATE
def test_cli_generate_smoke():
    """Smoke тест CLI команды generate через subprocess."""
    # START_BLOCK_RUN_CLI: [Запуск CLI через subprocess]
    result = subprocess.run(
        [sys.executable, "-m", "lesson_v7.src.cli", "generate"],
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).parent.parent.parent)
    )
    
    assert result.returncode == 0, f"CLI вернул код {result.returncode}. Stderr: {result.stderr}"
    assert "[OK]" in str(result.stdout)
    # END_BLOCK_RUN_CLI
# END_TEST_TEST_CLI_GENERATE

# START_TEST_TEST_CLI_EXPORT_CSV
def test_cli_export_csv_smoke():
    """Smoke тест CLI команды export-csv через subprocess."""
    # START_BLOCK_CREATE_TEMP_FILE: [Создание временного CSV файла]
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
        temp_csv_path = Path(f.name)
    
    try:
        # START_BLOCK_RUN_CLI: [Запуск CLI через subprocess]
        result = subprocess.run(
            [sys.executable, "-m", "lesson_v7.src.cli", "export-csv", "--out", str(temp_csv_path)],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent.parent)
        )
        
        assert result.returncode == 0, f"CLI вернул код {result.returncode}. Stderr: {result.stderr}"
        assert "[OK]" in str(result.stdout)
        assert temp_csv_path.exists(), "CSV файл не был создан"
        # END_BLOCK_RUN_CLI
        
    finally:
        # START_BLOCK_CLEANUP: [Очистка временных файлов]
        if temp_csv_path.exists():
            temp_csv_path.unlink()
        # END_BLOCK_CLEANUP
# END_TEST_TEST_CLI_EXPORT_CSV

# ============================================================================
# HEADLESS ТЕСТЫ UI КОНТРОЛЛЕРА
# ============================================================================

# START_TEST_TEST_UI_GENERATE_DATA_HANDLER
def test_ui_generate_data_handler(caplog):
    """Headless тест обработчика генерации данных UI с LDD логированием."""
    caplog.set_level(logging.INFO)
    
    # START_BLOCK_TEMP_FILES: [Создание временных файлов]
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        temp_config_path = Path(f.name)
        temp_config_path.write_text('{"a": 1.0, "c": 0.0, "x_min": -5.0, "x_max": 5.0}')
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        temp_db_path = Path(f.name)
    
    try:
        # START_BLOCK_MOCK_PATHS: [Мок путей для тестов]
        from lesson_v7.src import config_manager
        from lesson_v7.src import database_manager
        
        original_config_path = config_manager.DEFAULT_CONFIG_PATH
        original_db_path = database_manager.DEFAULT_DB_PATH
        
        config_manager.DEFAULT_CONFIG_PATH = temp_config_path
        database_manager.DEFAULT_DB_PATH = temp_db_path
        # END_BLOCK_MOCK_PATHS
        
        # START_BLOCK_CALL_HANDLER: [Вызов обработчика]
        result = generate_data_handler(a=2.0, c=1.0, x_min=-3.0, x_max=3.0)
        assert "[OK]" in result
        # END_BLOCK_CALL_HANDLER
        
        # START_BLOCK_CHECK_LOGS: [Проверка LDD логов]
        imp_logs = [record for record in caplog.records if '[IMP:' in record.message]
        assert len(imp_logs) > 0, "Ожидаются логи с уровнем важности [IMP:7-10]"
        
        # Вывод логов для контекста
        for record in imp_logs:
            print(f"\n[LOG] {record.message}")
        # END_BLOCK_CHECK_LOGS
        
        # START_BLOCK_RESTORE_PATHS: [Восстановление оригинальных путей]
        config_manager.DEFAULT_CONFIG_PATH = original_config_path
        database_manager.DEFAULT_DB_PATH = original_db_path
        # END_BLOCK_RESTORE_PATHS
        
    finally:
        # START_BLOCK_CLEANUP: [Очистка временных файлов]
        if temp_config_path.exists():
            temp_config_path.unlink()
        if temp_db_path.exists():
            temp_db_path.unlink()
        # END_BLOCK_CLEANUP
# END_TEST_TEST_UI_GENERATE_DATA_HANDLER

# START_TEST_TEST_UI_DRAW_GRAPH_HANDLER
def test_ui_draw_graph_handler(caplog):
    """Headless тест обработчика построения графика UI с LDD логированием."""
    caplog.set_level(logging.INFO)
    
    # START_BLOCK_TEMP_DB: [Создание временной базы данных]
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        temp_db_path = Path(f.name)
    
    try:
        # START_BLOCK_MOCK_PATH: [Мок пути для тестов]
        from lesson_v7.src import database_manager
        original_db_path = database_manager.DEFAULT_DB_PATH
        database_manager.DEFAULT_DB_PATH = temp_db_path
        # END_BLOCK_MOCK_PATH
        
        # START_BLOCK_PREPARE_DATA: [Подготовка тестовых данных]
        init_database(temp_db_path)
        test_points = [(0.0, 0.0), (1.0, 1.0), (-1.0, 1.0)]
        save_points(test_points, temp_db_path)
        # END_BLOCK_PREPARE_DATA
        
        # START_BLOCK_CALL_HANDLER: [Вызов обработчика]
        fig = draw_graph_handler()
        assert fig is not None, "График не был создан"
        # END_BLOCK_CALL_HANDLER
        
        # START_BLOCK_CHECK_LOGS: [Проверка LDD логов]
        imp_logs = [record for record in caplog.records if '[IMP:' in record.message]
        assert len(imp_logs) > 0, "Ожидаются логи с уровнем важности [IMP:7-10]"
        
        # Вывод логов для контекста
        for record in imp_logs:
            print(f"\n[LOG] {record.message}")
        # END_BLOCK_CHECK_LOGS
        
        # START_BLOCK_RESTORE_PATH: [Восстановление оригинального пути]
        database_manager.DEFAULT_DB_PATH = original_db_path
        # END_BLOCK_RESTORE_PATH
        
    finally:
        # START_BLOCK_CLEANUP: [Очистка временных файлов]
        if temp_db_path.exists():
            temp_db_path.unlink()
        # END_BLOCK_CLEANUP
# END_TEST_TEST_UI_DRAW_GRAPH_HANDLER

# START_TEST_TEST_UI_LOAD_TABLE_HANDLER
def test_ui_load_table_handler(caplog):
    """Headless тест обработчика загрузки таблицы UI с LDD логированием."""
    caplog.set_level(logging.INFO)
    
    # START_BLOCK_PREPARE_DATA: [Подготовка тестовых данных]
    # Используем основную БД приложения для простоты теста
    test_points = [(0.0, 0.0), (1.0, 1.0), (2.0, 4.0)]
    init_database()
    save_points(test_points)
    # END_BLOCK_PREPARE_DATA
    
    try:
        # START_BLOCK_CALL_HANDLER: [Вызов обработчика]
        df = load_table_handler()
        assert df is not None, "DataFrame не был создан"
        assert len(df) >= 3, f"Ожидалось минимум 3 строки, получено {len(df)}"
        assert 'x' in df.columns and 'y' in df.columns, "Отсутствуют столбцы x или y"
        # END_BLOCK_CALL_HANDLER
        
        # START_BLOCK_CHECK_LOGS: [Проверка LDD логов]
        imp_logs = [record for record in caplog.records if '[IMP:' in record.message]
        assert len(imp_logs) > 0, "Ожидаются логи с уровнем важности [IMP:7-10]"
        
        # Вывод логов для контекста
        for record in imp_logs:
            print(f"\n[LOG] {record.message}")
        # END_BLOCK_CHECK_LOGS
        
    finally:
        # START_BLOCK_CLEANUP: [Очистка БД]
        # Очищаем БД после теста
        save_points([])
        # END_BLOCK_CLEANUP
# END_TEST_TEST_UI_LOAD_TABLE_HANDLER
