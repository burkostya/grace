# FILE:lesson_12/cli.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: CLI интерфейс для управления данными параболы.
# SCOPE: Генерация данных и экспорт в CSV.
# KEYWORDS:[DOMAIN(8): CLI; CONCEPT(9): AgenticUX]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.1 - Исправление семантической разметки: добавлены MODULE_MAP, USE_CASES и контракты функций.]
# PREV_CHANGE_SUMMARY: [v1.0.0 - Создание CLI интерфейса.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Точка входа CLI] => main
# END_MODULE_MAP
#
# START_USE_CASES:
# - [main]: Agent -> CLICommand -> DataOperation
# END_USE_CASES

import argparse
import pandas as pd
import sys
import os

# Добавляем родительскую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lesson_12.handlers import generate_parabola_points
from lesson_12.config_manager import load_config
from lesson_12.db_manager import save_points, load_points

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE: Парсинг аргументов и выполнение команд CLI.
# INPUTS: None (sys.argv)
# OUTPUTS: None
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def main():
    """
    Основная функция CLI. Поддерживает команды 'generate' для создания данных на основе конфига
    и 'export-csv' для выгрузки текущего состояния БД в файл.
    """
    # START_BLOCK_PARSING: [Парсинг аргументов]
    parser = argparse.ArgumentParser(description="Lesson 12 CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Команда generate
    subparsers.add_parser("generate", help="Generate points using config.json")

    # Команда export-csv
    export_parser = subparsers.add_parser("export-csv", help="Export DB to CSV")
    export_parser.add_argument("--out", required=True, help="Output filename")

    args = parser.parse_args()
    # END_BLOCK_PARSING

    # START_BLOCK_EXECUTION: [Выполнение команд]
    if args.command == "generate":
        conf = load_config()
        df = generate_parabola_points(conf['a'], conf['c'], conf['x_min'], conf['x_max'])
        save_points(df)
        print(f"Successfully generated {len(df)} points based on config.json")

    elif args.command == "export-csv":
        df = load_points()
        df.to_csv(args.out, index=False)
        print(f"Exported {len(df)} records to {args.out}")
    
    else:
        parser.print_help()
    # END_BLOCK_EXECUTION

if __name__ == "__main__":
    main()
# END_FUNCTION_main
