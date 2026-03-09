# FILE: lesson_v8/tests/test_app.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Тестовый модуль для проверки функциональности приложения lesson_v8.
# SCOPE: Покрытие бизнес-логики, CLI интерфейса и UI контроллеров.
# INPUT: Отсутствует (тесты запускаются через pytest).
# OUTPUT: Результаты тестирования (stdout/stderr pytest).
# KEYWORDS:[DOMAIN(9): Testing; CONCEPT(8): Pytest; TECH(9): LDD]
# LINKS:[TESTS(9): config_manager, parabola_logic, database_manager, cli, ui_controller]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание тестового модуля.]
# END_CHANGE_SUMMARY

"""
Тестовый модуль для приложения lesson_v8.

Включает:
- Backend & LDD Tests: проверка бизнес-логики с выводом логов IMP:7-10
- CLI Smoke Tests: проверка команд через subprocess.run
- UI Headless Tests: проверка обработчиков Gradio без запуска сервера
"""

import logging
import os
import subprocess
import sys
import tempfile
import pytest
import pandas as pd
import plotly.graph_objects as go

# Добавление пути к src для импорта модулей
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config_manager import load_config, save_config, DEFAULT_CONFIG
from parabola_logic import generate_parabola_points
from database_manager import init_database, save_points, load_points, clear_points, DB_FILE


# ============================================================================
# BACKEND & LDD TESTS
# ============================================================================

class TestConfigManager:
    """Тесты для модуля управления конфигурацией."""
    
    def test_load_config_default(self, caplog):
        """Тест загрузки дефолтной конфигурации при отсутствии файла."""
        caplog.set_level(logging.DEBUG)
        
        # Временный файл конфигурации
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_config_path = f.name
        
        try:
            # Удаляем файл, чтобы проверить создание дефолтной конфигурации
            if os.path.exists(temp_config_path):
                os.remove(temp_config_path)
            
            config = load_config(temp_config_path)
            
            # Проверка структуры конфигурации
            assert isinstance(config, dict)
            assert 'a' in config
            assert 'c' in config
            assert 'x_min' in config
            assert 'x_max' in config
            
            # Проверка дефолтных значений
            assert config['a'] == DEFAULT_CONFIG['a']
            assert config['c'] == DEFAULT_CONFIG['c']
            assert config['x_min'] == DEFAULT_CONFIG['x_min']
            assert config['x_max'] == DEFAULT_CONFIG['x_max']
            
            # Проверка, что файл был создан
            assert os.path.exists(temp_config_path)
            
        finally:
            # Очистка
            if os.path.exists(temp_config_path):
                os.remove(temp_config_path)
        
        # Вывод логов IMP:7-10
        logs = caplog.text
        print("\n=== LOGS IMP:7-10 ===")
        for record in caplog.records:
            if '[IMP:7]' in record.message or '[IMP:8]' in record.message or \
               '[IMP:9]' in record.message or '[IMP:10]' in record.message:
                print(record.message)
        print("====================\n")
    
    def test_save_and_load_config(self, caplog):
        """Тест сохранения и загрузки конфигурации."""
        caplog.set_level(logging.DEBUG)
        
        # Временный файл конфигурации
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_config_path = f.name
        
        try:
            # Сохранение конфигурации
            test_config = {
                'a': 2.5,
                'c': -3.0,
                'x_min': -20.0,
                'x_max': 20.0
            }
            save_config(test_config, temp_config_path)
            
            # Загрузка конфигурации
            loaded_config = load_config(temp_config_path)
            
            # Проверка значений
            assert loaded_config['a'] == test_config['a']
            assert loaded_config['c'] == test_config['c']
            assert loaded_config['x_min'] == test_config['x_min']
            assert loaded_config['x_max'] == test_config['x_max']
            
        finally:
            # Очистка
            if os.path.exists(temp_config_path):
                os.remove(temp_config_path)
        
        # Вывод логов IMP:7-10
        logs = caplog.text
        print("\n=== LOGS IMP:7-10 ===")
        for record in caplog.records:
            if '[IMP:7]' in record.message or '[IMP:8]' in record.message or \
               '[IMP:9]' in record.message or '[IMP:10]' in record.message:
                print(record.message)
        print("====================\n")


class TestParabolaLogic:
    """Тесты для модуля математических вычислений параболы."""
    
    def test_generate_parabola_points(self, caplog):
        """Тест генерации точек параболы."""
        caplog.set_level(logging.DEBUG)
        
        a = 2.0
        c = 1.0
        x_min = -5.0
        x_max = 5.0
        num_points = 11
        
        df = generate_parabola_points(a, c, x_min, x_max, num_points)
        
        # Проверка типа результата
        assert isinstance(df, pd.DataFrame)
        
        # Проверка колонок
        assert 'x' in df.columns
        assert 'y' in df.columns
        
        # Проверка количества точек
        assert len(df) == num_points
        
        # Проверка формулы y = ax^2 + c
        for _, row in df.iterrows():
            expected_y = a * (row['x'] ** 2) + c
            assert abs(row['y'] - expected_y) < 0.0001
        
        # Проверка диапазона x
        assert df['x'].min() == x_min
        assert df['x'].max() == x_max
        
        # Вывод логов IMP:7-10
        print("\n=== LOGS IMP:7-10 ===")
        for record in caplog.records:
            if '[IMP:7]' in record.message or '[IMP:8]' in record.message or \
               '[IMP:9]' in record.message or '[IMP:10]' in record.message:
                print(record.message)
        print("====================\n")
    
    def test_generate_parabola_points_invalid_inputs(self, caplog):
        """Тест обработки невалидных входных параметров."""
        caplog.set_level(logging.DEBUG)
        
        # Тест: num_points <= 0
        with pytest.raises(ValueError):
            generate_parabola_points(1.0, 0.0, -10.0, 10.0, 0)
        
        # Тест: x_min >= x_max
        with pytest.raises(ValueError):
            generate_parabola_points(1.0, 0.0, 10.0, -10.0)
        
        # Вывод логов IMP:7-10
        print("\n=== LOGS IMP:7-10 ===")
        for record in caplog.records:
            if '[IMP:7]' in record.message or '[IMP:8]' in record.message or \
               '[IMP:9]' in record.message or '[IMP:10]' in record.message:
                print(record.message)
        print("====================\n")


class TestDatabaseManager:
    """Тесты для модуля управления базой данных."""
    
    def test_database_operations(self, caplog):
        """Тест полного цикла операций с базой данных."""
        caplog.set_level(logging.DEBUG)
        
        # Временная база данных
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            temp_db_path = f.name
        
        try:
            # Инициализация базы данных
            init_database(temp_db_path)
            
            # Генерация точек
            df = generate_parabola_points(1.0, 0.0, -5.0, 5.0, 11)
            
            # Сохранение точек
            save_points(df, temp_db_path)
            
            # Загрузка точек
            loaded_df = load_points(temp_db_path)
            
            # Проверка количества точек
            assert len(loaded_df) == len(df)
            
            # Проверка значений
            pd.testing.assert_frame_equal(loaded_df.reset_index(drop=True), df.reset_index(drop=True))
            
            # Очистка базы данных
            clear_points(temp_db_path)
            
            # Проверка, что база данных очищена
            empty_df = load_points(temp_db_path)
            assert len(empty_df) == 0
            
        finally:
            # Очистка
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        
        # Вывод логов IMP:7-10
        print("\n=== LOGS IMP:7-10 ===")
        for record in caplog.records:
            if '[IMP:7]' in record.message or '[IMP:8]' in record.message or \
               '[IMP:9]' in record.message or '[IMP:10]' in record.message:
                print(record.message)
        print("====================\n")


# ============================================================================
# CLI SMOKE TESTS
# ============================================================================

class TestCLI:
    """Тесты для CLI интерфейса."""
    
    def test_cli_generate_command(self, caplog):
        """Тест команды generate через вызов функции main."""
        caplog.set_level(logging.DEBUG)
        
        # Импорт CLI модуля
        from lesson_v8.src.cli import main
        
        # Вызов команды generate
        return_code = main(['generate'])
        
        # Проверка exit code
        assert return_code == 0, f"Command failed with return code: {return_code}"
        
        # Вывод логов IMP:7-10
        print("\n=== LOGS IMP:7-10 ===")
        for record in caplog.records:
            if '[IMP:7]' in record.message or '[IMP:8]' in record.message or \
               '[IMP:9]' in record.message or '[IMP:10]' in record.message:
                print(record.message)
        print("====================\n")
    
    def test_cli_export_csv_command(self, caplog):
        """Тест команды export-csv через вызов функции main."""
        caplog.set_level(logging.DEBUG)
        
        # Временный CSV файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_csv_path = f.name
        
        try:
            # Импорт CLI модуля
            from lesson_v8.src.cli import main
            
            # Сначала генерируем данные
            main(['generate'])
            
            # Запуск команды export-csv
            return_code = main(['export-csv', '--out', temp_csv_path])
            
            # Проверка exit code
            assert return_code == 0, f"Command failed with return code: {return_code}"
            
            # Проверка, что файл создан
            assert os.path.exists(temp_csv_path)
            
            # Проверка содержимого CSV
            df = pd.read_csv(temp_csv_path)
            assert 'x' in df.columns
            assert 'y' in df.columns
            assert len(df) > 0
            
        finally:
            # Очистка
            if os.path.exists(temp_csv_path):
                os.remove(temp_csv_path)
        
        # Вывод логов IMP:7-10
        print("\n=== LOGS IMP:7-10 ===")
        for record in caplog.records:
            if '[IMP:7]' in record.message or '[IMP:8]' in record.message or \
               '[IMP:9]' in record.message or '[IMP:10]' in record.message:
                print(record.message)
        print("====================\n")


# ============================================================================
# UI HEADLESS TESTS
# ============================================================================
class TestUIController:
    """Тесты для UI контроллера (headless)."""
    
    def test_handle_generate(self, caplog):
        """Тест обработчика кнопки Generate Data."""
        caplog.set_level(logging.DEBUG)
        
        # Импорт через пакет lesson_v8
        from lesson_v8.src.ui_controller import handle_generate
        
        # Временная база данных
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            temp_db_path = f.name
        
        # Временный файл конфигурации
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_config_path = f.name
        
        try:
            # Подмена путей
            import database_manager
            import config_manager
            original_db_path = database_manager.DB_FILE
            original_config_path = config_manager.CONFIG_FILE
            database_manager.DB_FILE = temp_db_path
            config_manager.CONFIG_FILE = temp_config_path
            
            # Вызов обработчика
            df, fig = handle_generate(a=2.0, c=1.0, x_min=-5.0, x_max=5.0)
            
            # Восстановление путей
            database_manager.DB_FILE = original_db_path
            config_manager.CONFIG_FILE = original_config_path
            
            # Проверка типа результата
            assert isinstance(df, pd.DataFrame)
            assert fig is None
            
            # Проверка колонок
            assert 'x' in df.columns
            assert 'y' in df.columns
            
            # Проверка количества точек
            assert len(df) == 100  # дефолтное значение
            
            # Проверка формулы y = ax^2 + c
            for _, row in df.iterrows():
                expected_y = 2.0 * (row['x'] ** 2) + 1.0
                assert abs(row['y'] - expected_y) < 0.0001
            
        finally:
            # Очистка
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
            if os.path.exists(temp_config_path):
                os.remove(temp_config_path)
        
        # Вывод логов IMP:7-10
        print("\n=== LOGS IMP:7-10 ===")
        for record in caplog.records:
            if '[IMP:7]' in record.message or '[IMP:8]' in record.message or \
               '[IMP:9]' in record.message or '[IMP:10]' in record.message:
                print(record.message)
        print("====================\n")
    
    def test_handle_draw_graph(self, caplog):
        """Тест обработчика кнопки Draw Graph."""
        caplog.set_level(logging.DEBUG)
        
        # Импорт через пакет lesson_v8
        from lesson_v8.src.ui_controller import handle_draw_graph
        
        # Временная база данных
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            temp_db_path = f.name
        
        try:
            # Подмена пути
            import database_manager
            original_db_path = database_manager.DB_FILE
            database_manager.DB_FILE = temp_db_path
            
            # Инициализация и сохранение данных
            init_database(temp_db_path)
            df = generate_parabola_points(1.0, 0.0, -5.0, 5.0, 11)
            save_points(df, temp_db_path)
            
            # Вызов обработчика
            df_result, fig = handle_draw_graph()
            
            # Восстановление пути
            database_manager.DB_FILE = original_db_path
            
            # Проверка типа результата
            assert df_result is None
            assert isinstance(fig, go.Figure)
            
        finally:
            # Очистка
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        
        # Вывод логов IMP:7-10
        print("\n=== LOGS IMP:7-10 ===")
        for record in caplog.records:
            if '[IMP:7]' in record.message or '[IMP:8]' in record.message or \
               '[IMP:9]' in record.message or '[IMP:10]' in record.message:
                print(record.message)
        print("====================\n")
    
    def test_create_interface(self, caplog):
        """Тест создания интерфейса."""
        caplog.set_level(logging.DEBUG)
        
        # Импорт через пакет lesson_v8
        from lesson_v8.src.ui_controller import create_interface
        
        import gradio as gr
        
        # Создание интерфейса
        interface = create_interface()
        
        # Проверка типа результата
        assert isinstance(interface, gr.Blocks)
        
        # Вывод логов IMP:7-10
        print("\n=== LOGS IMP:7-10 ===")
        for record in caplog.records:
            if '[IMP:7]' in record.message or '[IMP:8]' in record.message or \
               '[IMP:9]' in record.message or '[IMP:10]' in record.message:
                print(record.message)
        print("====================\n")
