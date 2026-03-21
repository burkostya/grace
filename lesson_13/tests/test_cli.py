# FILE:lesson_13/tests/test_cli.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Дымовые тесты CLI интерфейса Lesson 13.
# SCOPE:Проверка команд generate и export-csv через subprocess.
# INPUT:Команды CLI.
# OUTPUT:Результаты тестов (exit codes, наличие файлов).
# KEYWORDS:DOMAIN(Testing); CONCEPT(Smoke Test); TECH(Python, pytest, subprocess)
# LINKS:USES_API(subprocess); USES_API(pytest)
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание дымовых тестов CLI.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC[10][Тест команды generate] => test_cli_generate
# FUNC[10][Тест команды export-csv] => test_cli_export
# END_MODULE_MAP

import subprocess
import os
import pytest

# START_FUNCTION_test_cli_generate
# START_CONTRACT:
# PURPOSE:Проверка успешного выполнения команды generate.
# INPUTS: Нет
# OUTPUTS: None
# SIDE_EFFECTS: Создает/обновляет БД и конфиг.
# KEYWORDS:CONCEPT(Integration)
# COMPLEXITY_SCORE:3
# END_CONTRACT
def test_cli_generate():
    """
    Запускает команду generate через subprocess и проверяет код возврата 0.
    Также проверяет, что файл БД был создан.
    """
    # START_BLOCK_RUN_GENERATE: [Запуск процесса]
    cmd = ["python", "-m", "lesson_13.src.cli", "generate"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(f"\nSTDOUT: {result.stdout}")
    print(f"STDERR: {result.stderr}")
    
    assert result.returncode == 0
    assert "Successfully generated" in result.stdout
    assert os.path.exists("lesson_13/parabola.db")
    # END_BLOCK_RUN_GENERATE
# END_FUNCTION_test_cli_generate

# START_FUNCTION_test_cli_export
# START_CONTRACT:
# PURPOSE:Проверка успешного выполнения команды export-csv.
# INPUTS: Нет
# OUTPUTS: None
# SIDE_EFFECTS: Создает CSV файл.
# KEYWORDS:CONCEPT(Integration)
# COMPLEXITY_SCORE:3
# END_CONTRACT
def test_cli_export():
    """
    Запускает команду export-csv после генерации данных.
    Проверяет код возврата 0 и наличие выходного файла.
    """
    # START_BLOCK_PREPARE_DATA: [Гарантируем наличие данных]
    subprocess.run(["python", "-m", "lesson_13.src.cli", "generate"])
    # END_BLOCK_PREPARE_DATA

    # START_BLOCK_RUN_EXPORT: [Запуск экспорта]
    out_file = "lesson_13/tests/output_test.csv"
    if os.path.exists(out_file):
        os.remove(out_file)
        
    cmd = ["python", "-m", "lesson_13.src.cli", "export-csv", "--out", out_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(f"\nSTDOUT: {result.stdout}")
    print(f"STDERR: {result.stderr}")
    
    assert result.returncode == 0
    assert "Exported" in result.stdout
    assert os.path.exists(out_file)
    # END_BLOCK_RUN_EXPORT
# END_FUNCTION_test_cli_export
