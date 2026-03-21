# FILE:lesson_10/tests/test_app.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Набор тестов для верификации бизнес-логики, CLI и UI приложения Lesson 10.
# SCOPE:Backend (расчеты, БД), CLI (smoke tests), UI (headless tests).
# INPUT:Тестовые данные, вызовы функций.
# OUTPUT:Результаты тестов pytest, логи в stdout.
# KEYWORDS:[DOMAIN(Testing): Pytest; CONCEPT(Verification): LDD; TECH(Python): subprocess, caplog]
# LINKS:[USES_API(9): pytest, pandas, plotly]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему тесты используют caplog для вывода логов?
# A: Согласно бизнес-требованиям, тесты должны генерировать семантический контекст (IMP:7-10) для верификации траектории работы алгоритма.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание набора тестов.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Тест бэкенда: расчет, конфиг, БД] => test_backend_logic
# FUNC 10[Тест CLI: smoke test через subprocess] => test_cli_smoke
# FUNC 10[Тест UI: headless проверка обработчиков Gradio] => test_ui_headless
# END_MODULE_MAP
#
# START_USE_CASES:
# - [test_backend_logic]: Developer -> Run Pytest -> BackendVerified
# - [test_cli_smoke]: Developer -> Run Pytest -> CLIVerified
# - [test_ui_headless]: Developer -> Run Pytest -> UIVerified
# END_USE_CASES

import pytest
import os
import subprocess
import pandas as pd
import plotly.graph_objects as go
import logging
from lesson_10.src.config_manager import load_config, save_config
from lesson_10.src.database_manager import save_points, get_points_df
from lesson_10.src.parabola_logic import calculate_parabola_points
from lesson_10.src.ui_controller import handle_generate_data, handle_draw_graph

# Настройка логгера для тестов
logger = logging.getLogger(__name__)

# START_FUNCTION_test_backend_logic
# START_CONTRACT:
# PURPOSE:Проверка логики расчета, сохранения конфига и записи в БД.
# INPUTS: caplog (pytest fixture)
# OUTPUTS: None
# SIDE_EFFECTS: Создает временные файлы конфига и БД.
# KEYWORDS:[PATTERN(Test): Backend]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def test_backend_logic(caplog):
    """
    Тестирует связку: расчет параболы -> сохранение в БД -> чтение из БД.
    Проверяет корректность вычислений и целостность данных.
    Использует caplog для вывода важных логов в консоль.
    """
    # START_BLOCK_BACKEND_TEST: [Тестирование бэкенда]
    caplog.set_level(logging.DEBUG)
    
    # 1. Тест расчета
    points = calculate_parabola_points(a=2.0, c=5.0, x_min=-5, x_max=5, num_points=10)
    assert len(points) == 10
    # Проверка y = 2*x^2 + 5 для x=0
    # x_values = np.linspace(-5, 5, 10), x=0 может не попасть точно, проверим знак
    assert all(p[1] >= 5.0 for p in points)
    
    # 2. Тест БД
    db_test_path = "lesson_10/test_data.db"
    if os.path.exists(db_test_path): os.remove(db_test_path)
    
    save_points(points, db_path=db_test_path)
    df = get_points_df(db_path=db_test_path)
    assert len(df) == 10
    assert list(df.columns) == ['x', 'y']
    
    # Вывод логов IMP:7-10 в консоль
    print("\n--- LDD Telemetry (Backend) ---")
    for record in caplog.records:
        if "[IMP:" in record.message:
            imp_level = int(record.message.split("[IMP:")[1].split("]")[0])
            if imp_level >= 7:
                print(f"LOG: {record.message}")
    
    if os.path.exists(db_test_path): os.remove(db_test_path)
    # END_BLOCK_BACKEND_TEST
# END_FUNCTION_test_backend_logic

# START_FUNCTION_test_cli_smoke
# START_CONTRACT:
# PURPOSE:Изолированный тест для cli.py через subprocess.run.
# INPUTS: None
# OUTPUTS: None
# SIDE_EFFECTS: Вызывает внешние процессы.
# KEYWORDS:[PATTERN(Test): CLI]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def test_cli_smoke():
    """
    Выполняет запуск CLI команд 'generate' и 'export-csv' через subprocess.
    Проверяет коды возврата (exit code 0) и создание выходных файлов.
    """
    # START_BLOCK_CLI_TEST: [Тестирование CLI]
    cli_path = "lesson_10/src/cli.py"
    csv_out = "lesson_10/test_export.csv"
    if os.path.exists(csv_out): os.remove(csv_out)
    
    # 1. Тест generate
    res_gen = subprocess.run(["python", cli_path, "generate"], capture_output=True, text=True)
    assert res_gen.returncode == 0
    print(f"\nCLI Generate Output: {res_gen.stdout}")
    
    # 2. Тест export-csv
    res_exp = subprocess.run(["python", cli_path, "export-csv", "--out", csv_out], capture_output=True, text=True)
    assert res_exp.returncode == 0
    assert os.path.exists(csv_out)
    
    if os.path.exists(csv_out): os.remove(csv_out)
    # END_BLOCK_CLI_TEST
# END_FUNCTION_test_cli_smoke

# START_FUNCTION_test_ui_headless
# START_CONTRACT:
# PURPOSE:Проверка обработчиков Gradio (имитация кликов) без запуска сервера.
# INPUTS: None
# OUTPUTS: None
# SIDE_EFFECTS: Нет.
# KEYWORDS:[PATTERN(Test): UI]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def test_ui_headless():
    """
    Имитирует вызовы функций-обработчиков UI (handle_generate_data, handle_draw_graph).
    Проверяет типы возвращаемых данных (DataFrame, Plotly Figure).
    """
    # START_BLOCK_UI_TEST: [Тестирование UI]
    # 1. Тест генерации данных
    df = handle_generate_data(a=1.0, c=0.0, x_min=-10, x_max=10)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    
    # 2. Тест отрисовки графика
    fig = handle_draw_graph()
    assert isinstance(fig, go.Figure)
    assert len(fig.data) > 0
    # END_BLOCK_UI_TEST
# END_FUNCTION_test_ui_headless
