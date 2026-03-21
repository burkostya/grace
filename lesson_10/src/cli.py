# FILE:lesson_10/src/cli.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Интерфейс командной строки (CLI) для автономного управления бэкендом.
# SCOPE:Генерация данных и экспорт в CSV через терминал.
# INPUT:Аргументы командной строки (generate, export-csv).
# OUTPUT:Вывод в stdout, файлы на диске (data.db, export.csv).
# KEYWORDS:[DOMAIN(CLI): Interface; CONCEPT(AgenticUX): Autonomous; TECH(Python): argparse]
# LINKS:[USES_API(8): argparse, pandas]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему команда generate не принимает параметры a, c и т.д.?
# A: Согласно бизнес-требованиям, CLI должен автоматически считывать параметры из config.json для обеспечения автономности агентов.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание CLI интерфейса.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Точка входа CLI, парсинг аргументов] => main
# FUNC 10[Выполняет генерацию на основе конфига] => run_generate
# FUNC 10[Экспортирует данные из БД в CSV] => run_export_csv
# END_MODULE_MAP
#
# START_USE_CASES:
# - [run_generate]: Agent -> cli.py generate -> DBUpdated
# - [run_export_csv]: Agent -> cli.py export-csv --out file.csv -> CSVFileCreated
# END_USE_CASES

import argparse
import sys
import logging
import os
from lesson_10.src.config_manager import load_config
from lesson_10.src.database_manager import save_points, get_points_df
from lesson_10.src.parabola_logic import calculate_parabola_points

# Настройка логирования для CLI
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s][IMP:9][CLI] %(message)s',
    handlers=[
        logging.FileHandler("lesson_10/app_10.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# START_FUNCTION_run_generate
# START_CONTRACT:
# PURPOSE:Выполняет генерацию точек, считывая параметры из config.json.
# INPUTS: Нет
# OUTPUTS: 
# - bool - Успешность операции
# SIDE_EFFECTS: Обновляет data.db.
# KEYWORDS:[PATTERN(Action): Generator]
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def run_generate() -> bool:
    """
    Считывает текущие параметры из файла конфигурации и запускает 
    процесс генерации точек параболы с последующим сохранением в БД.
    Это позволяет агентам управлять бэкендом без ручного ввода параметров.
    """
    # START_BLOCK_CLI_GENERATE: [Генерация через CLI]
    try:
        config = load_config()
        points = calculate_parabola_points(
            config['a'], config['c'], 
            config['x_min'], config['x_max']
        )
        success = save_points(points)
        if success:
            logger.info(f"[BeliefState][IMP:9][run_generate][CLI_GENERATE][Success] Генерация завершена успешно. [SUCCESS]")
        return success
    except Exception as e:
        logger.error(f"[SystemError][IMP:10][run_generate][CLI_GENERATE][Exception] Ошибка генерации: {e} [FATAL]")
        return False
    # END_BLOCK_CLI_GENERATE
# END_FUNCTION_run_generate

# START_FUNCTION_run_export_csv
# START_CONTRACT:
# PURPOSE:Экспортирует данные из БД в указанный CSV файл.
# INPUTS: 
# - Путь к выходному файлу => out_path: str
# OUTPUTS: 
# - bool - Успешность операции
# SIDE_EFFECTS: Создает CSV файл на диске.
# KEYWORDS:[PATTERN(Export): CSV]
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def run_export_csv(out_path: str) -> bool:
    """
    Извлекает все точки из базы данных и сохраняет их в формате CSV.
    Если данных в БД нет, выводит предупреждение и не создает файл.
    """
    # START_BLOCK_CLI_EXPORT: [Экспорт в CSV]
    try:
        df = get_points_df()
        if df.empty:
            logger.warning(f"[State][IMP:6][run_export_csv][CLI_EXPORT][Empty] Нет данных для экспорта. [WARN]")
            return False
            
        df.to_csv(out_path, index=False)
        logger.info(f"[BeliefState][IMP:9][run_export_csv][CLI_EXPORT][Success] Данные экспортированы в {out_path} [SUCCESS]")
        return True
    except Exception as e:
        logger.error(f"[SystemError][IMP:10][run_export_csv][CLI_EXPORT][Exception] Ошибка экспорта: {e} [FATAL]")
        return False
    # END_BLOCK_CLI_EXPORT
# END_FUNCTION_run_export_csv

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE:Точка входа CLI, парсинг аргументов и вызов команд.
# INPUTS: Нет
# OUTPUTS: 
# - int - Код возврата (0 - успех, 1 - ошибка)
# SIDE_EFFECTS: Выполняет команды CLI.
# KEYWORDS:[PATTERN(Entry): Main]
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def main():
    """
    Инициализирует парсер аргументов командной строки и направляет 
    выполнение в соответствующие функции-обработчики команд.
    """
    # START_BLOCK_CLI_PARSING: [Парсинг аргументов]
    parser = argparse.ArgumentParser(description="Lesson 10 Parabola CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Команда generate
    subparsers.add_parser("generate", help="Generate points based on config.json")
    
    # Команда export-csv
    export_parser = subparsers.add_parser("export-csv", help="Export points to CSV")
    export_parser.add_argument("--out", required=True, help="Output CSV filename")
    
    args = parser.parse_args()
    
    if args.command == "generate":
        success = run_generate()
        sys.exit(0 if success else 1)
    elif args.command == "export-csv":
        success = run_export_csv(args.out)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)
    # END_BLOCK_CLI_PARSING
# END_FUNCTION_main

if __name__ == "__main__":
    main()
# END_FUNCTION_main
