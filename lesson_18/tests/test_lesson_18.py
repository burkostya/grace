# FILE: lesson_18/tests/test_lesson_18.py
# VERSION: 1.1.0
# START_MODULE_CONTRACT:
# PURPOSE: Тестирование бизнес-логики и UI Headless для Lesson 18 (Parabola Generator).
# SCOPE: Расчеты, SQLite, JSON Config, Gradio Handlers.
# INPUT: Временные файлы через tmp_path.
# OUTPUT: Результаты тестов pytest и LDD логи.
# KEYWORDS: [DOMAIN(8): Testing; CONCEPT(7): LDD; TECH(9): Pytest, Gradio, Plotly]
# LINKS: [USES_API(8): lesson_18.src.config_manager, lesson_18.src.data_processor, lesson_18.src.ui_controller]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.1.0 - Добавлены явные # CHECKLIST комментарии для Anti-Loop Protocol.]
# PREV_CHANGE_SUMMARY: [v1.0.0 - Первичное создание тестов.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Тест ConfigManager: чтение/запись] => test_config_manager
# FUNC 10[Тест DataProcessor: расчеты и БД] => test_data_processor
# FUNC 10[Тест UIController: headless обработчики] => test_ui_controller_headless
# END_MODULE_MAP

import pytest
import os
import pandas as pd
import plotly.graph_objects as go
import logging
from lesson_18.src.config_manager import ConfigManager
from lesson_18.src.data_processor import DataProcessor
from lesson_18.src.ui_controller import UIController

# START_FUNCTION_test_config_manager
# START_CONTRACT:
# PURPOSE: Проверка сохранения и загрузки конфигурации.
# INPUTS: tmp_path (pytest fixture), caplog
# OUTPUTS: None
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def test_config_manager(tmp_path, caplog):
    """
    Тест проверяет, что ConfigManager корректно создает файл,
    сохраняет параметры и загружает их обратно.
    """
    caplog.set_level(logging.DEBUG)
    # START_BLOCK_SETUP: [Инициализация путей]
    # CHECKLIST: [PATHS] Используется ли tmp_path для изоляции конфига?
    config_file = tmp_path / "test_config.json"
    cm = ConfigManager(config_path=str(config_file))
    # END_BLOCK_SETUP

    # START_BLOCK_SAVE_LOAD: [Сохранение и загрузка]
    # CHECKLIST: [DATA] Соответствуют ли типы данных (float, int) ожидаемым в JSON?
    test_params = {"a": 2.5, "c": -10.0, "x_min": -5, "x_max": 5}
    save_status = cm.save_config(test_params)
    assert save_status is True
    
    loaded_params = cm.load_config()
    assert loaded_params == test_params
    # END_BLOCK_SAVE_LOAD

    # START_BLOCK_LDD_VERIFY: [Проверка логов IMP:7-10]
    # CHECKLIST: [LDD] Выводятся ли логи [IMP:9] для save_config?
    print("\n--- LDD TELEMETRY (ConfigManager) ---")
    found_imp9 = False
    for record in caplog.records:
        if any(f"[IMP:{i}]" in record.message for i in range(7, 11)):
            print(record.message)
            if "[IMP:9]" in record.message and "save_config" in record.message:
                found_imp9 = True
    assert found_imp9, "LDD Error: Missing [IMP:9] for save_config"
    # END_BLOCK_LDD_VERIFY
# END_FUNCTION_test_config_manager

# START_FUNCTION_test_data_processor
# START_CONTRACT:
# PURPOSE: Проверка математических расчетов и работы с SQLite.
# INPUTS: tmp_path, caplog
# OUTPUTS: None
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def test_data_processor(tmp_path, caplog):
    """
    Тест проверяет генерацию точек параболы и их сохранение/загрузку из БД.
    """
    caplog.set_level(logging.DEBUG)
    # START_BLOCK_SETUP: [Инициализация БД]
    # CHECKLIST: [PATHS] Используется ли tmp_path для изоляции БД?
    db_file = tmp_path / "test_parabola.db"
    dp = DataProcessor(db_path=str(db_file))
    # END_BLOCK_SETUP

    # START_BLOCK_GENERATE: [Генерация точек]
    # CHECKLIST: [MATH] Верна ли формула y = ax^2 + c?
    # CHECKLIST: [PANDAS] Содержит ли DataFrame 100 точек по умолчанию?
    a, c, x_min, x_max = 1.0, 5.0, -10, 10
    df = dp.generate_points(a, c, x_min, x_max)
    assert len(df) == 100
    assert df.iloc[0]['x'] == x_min
    assert df.iloc[-1]['x'] == x_max
    # Проверка формулы y = ax^2 + c
    expected_y = a * (x_min ** 2) + c
    assert abs(df.iloc[0]['y'] - expected_y) < 1e-9
    # END_BLOCK_GENERATE

    # START_BLOCK_DB_OPS: [Сохранение и загрузка из БД]
    # CHECKLIST: [SQLITE] Создается ли таблица автоматически при сохранении?
    save_status = dp.save_to_db(df)
    assert save_status is True
    
    loaded_df = dp.load_from_db()
    assert len(loaded_df) == 100
    pd.testing.assert_frame_equal(df, loaded_df)
    # END_BLOCK_DB_OPS

    # START_BLOCK_LDD_VERIFY: [Проверка логов IMP:7-10]
    # CHECKLIST: [LDD] Есть ли логи [IMP:9] для generate_points и save_to_db?
    print("\n--- LDD TELEMETRY (DataProcessor) ---")
    found_imp9_math = False
    found_imp9_db = False
    for record in caplog.records:
        if any(f"[IMP:{i}]" in record.message for i in range(7, 11)):
            print(record.message)
            if "[IMP:9]" in record.message:
                if "generate_points" in record.message: found_imp9_math = True
                if "save_to_db" in record.message: found_imp9_db = True
    
    assert found_imp9_math, "LDD Error: Missing [IMP:9] for generate_points"
    assert found_imp9_db, "LDD Error: Missing [IMP:9] for save_to_db"
    # END_BLOCK_LDD_VERIFY
# END_FUNCTION_test_data_processor

# START_FUNCTION_test_ui_controller_headless
# START_CONTRACT:
# PURPOSE: Проверка обработчиков событий UI без запуска сервера.
# INPUTS: tmp_path, caplog
# OUTPUTS: None
# COMPLEXITY_SCORE: 7
# END_CONTRACT
def test_ui_controller_headless(tmp_path, caplog):
    """
    Тест проверяет handle_generate и handle_draw в UIController.
    Использует моки путей для изоляции.
    """
    caplog.set_level(logging.DEBUG)
    # START_BLOCK_SETUP: [Инициализация контроллера с тестовыми путями]
    # CHECKLIST: [PATHS] Переопределены ли пути в ConfigManager и DataProcessor?
    config_file = tmp_path / "ui_config.json"
    db_file = tmp_path / "ui_parabola.db"
    
    # Патчим пути в контроллере через его компоненты
    ui = UIController()
    ui.config_manager.config_path = str(config_file)
    ui.data_processor.db_path = str(db_file)
    ui.data_processor._init_db() # Переинициализируем для нового пути
    # END_BLOCK_SETUP

    # START_BLOCK_HANDLE_GENERATE: [Тест генерации через UI]
    # CHECKLIST: [UI] Возвращает ли handle_generate DataFrame?
    df = ui.handle_generate(2.0, 10.0, -5, 5)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 100
    # END_BLOCK_HANDLE_GENERATE

    # START_BLOCK_HANDLE_DRAW: [Тест отрисовки через UI]
    # CHECKLIST: [PLOTLY] Возвращает ли handle_draw объект go.Figure?
    fig = ui.handle_draw()
    assert isinstance(fig, go.Figure)
    assert len(fig.data) > 0
    assert fig.data[0].name == 'Parabola'
    # END_BLOCK_HANDLE_DRAW

    # START_BLOCK_LDD_VERIFY: [Проверка логов IMP:7-10]
    # CHECKLIST: [LDD] Есть ли логи [IMP:9] от UIController?
    print("\n--- LDD TELEMETRY (UIController) ---")
    found_imp9_ui = False
    for record in caplog.records:
        if any(f"[IMP:{i}]" in record.message for i in range(7, 11)):
            print(record.message)
            if "[IMP:9]" in record.message and "UIController" in record.message:
                found_imp9_ui = True
    
    assert found_imp9_ui, "LDD Error: Missing [IMP:9] for UIController handlers"
    # END_BLOCK_LDD_VERIFY
# END_FUNCTION_test_ui_controller_headless
