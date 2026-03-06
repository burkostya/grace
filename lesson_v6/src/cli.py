# FILE: lesson_v6/src/cli.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: CLI интерфейс (Agentic UX) для управления бэкендом Lesson 6.
# SCOPE: Команды generate (генерация точек) и export-csv (экспорт данных).
# INPUT: Аргументы командной строки.
# OUTPUT: Выполнение команд или сообщения об ошибках.
# KEYWORDS:[DOMAIN(8): CommandLineInterface; CONCEPT(7): AgenticUX; TECH(9): Argparse]
# LINKS:[USES_API(8): config_manager, database_manager, parabola_logic]
# END_MODULE_CONTRACT
#
# START_INVARIANTS:
# - Команда generate ВСЕГДА читает параметры из config.json.
# - Команда export-csv ВСЕГДА экспортирует текущие данные из БД.
# END_INVARIANTS
#
# START_RATIONALE:
# Q: Почему используется argparse вместо click или typer?
# A: argparse — стандартная библиотека Python, не требует дополнительных зависимостей.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание CLI модуля с LDD 2.0 логированием.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Обработка команды generate] => handle_generate
# FUNC 10[Обработка команды export-csv] => handle_export_csv
# FUNC 10[Главная точка входа CLI] => main
# END_MODULE_MAP
#
# START_USE_CASES:
# -[handle_generate]: User (CLI) -> GeneratePoints -> PointsGenerated
# -[handle_export_csv]: User (CLI) -> ExportData -> DataExported
# END_USE_CASES

import argparse
import csv
import logging
import sys
import os

# Импорт модулей проекта
from lesson_v6 import CONFIG_PATH, DB_PATH, LOG_PATH
from lesson_v6.src.config_manager import load_config
from lesson_v6.src.database_manager import initialize_database, save_points, load_points
from lesson_v6.src.parabola_logic import calculate_parabola_points

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# START_FUNCTION_handle_generate
# START_CONTRACT:
# PURPOSE: Обработка команды generate - генерация точек параболы.
# INPUTS: 
# - [Аргументы командной строки] => args: argparse.Namespace
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Обновляет config.json, перезаписывает таблицу points в БД.
# KEYWORDS:[PATTERN(6): CommandHandler; CONCEPT(8): Workflow]
# END_CONTRACT
def handle_generate(args: argparse.Namespace) -> None:
    """Обрабатывает команду generate."""
    
    # START_BLOCK_LOAD_CONFIG: [Загрузка конфигурации]
    try:
        config = load_config(CONFIG_PATH)
        logger.info(f"[ConfigLoad][IMP:7][handle_generate][LOAD_CONFIG][ReturnData] Загружена конфигурация: {config} [VALUE]")
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][handle_generate][LOAD_CONFIG][ExceptionEnrichment] Ошибка загрузки конфигурации. Err: {e} [FATAL]")
        sys.exit(1)
    # END_BLOCK_LOAD_CONFIG

    # START_BLOCK_INITIALIZE_DATABASE: [Инициализация БД]
    try:
        initialize_database(DB_PATH)
        logger.info(f"[DatabaseInit][IMP:7][handle_generate][INITIALIZE_DATABASE][ReturnData] База данных инициализирована [VALUE]")
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][handle_generate][INITIALIZE_DATABASE][ExceptionEnrichment] Ошибка инициализации БД. Err: {e} [FATAL]")
        sys.exit(1)
    # END_BLOCK_INITIALIZE_DATABASE

    # START_BLOCK_CALCULATE_POINTS: [Расчет точек параболы]
    try:
        points = calculate_parabola_points(
            a=config['a'],
            c=config['c'],
            x_min=config['x_min'],
            x_max=config['x_max']
        )
        logger.info(f"[Calculation][IMP:8][handle_generate][CALCULATE_POINTS][ReturnData] Рассчитано {len(points)} точек [VALUE]")
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][handle_generate][CALCULATE_POINTS][ExceptionEnrichment] Ошибка расчета точек. Err: {e} [FATAL]")
        sys.exit(1)
    # END_BLOCK_CALCULATE_POINTS

    # START_BLOCK_SAVE_POINTS: [Сохранение точек в БД]
    try:
        save_points(points, DB_PATH)
        logger.info(f"[DatabaseSave][IMP:8][handle_generate][SAVE_POINTS][ReturnData] Точки успешно сохранены в БД [VALUE]")
        print(f"[OK] Сгенерировано {len(points)} точек параболы")
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][handle_generate][SAVE_POINTS][ExceptionEnrichment] Ошибка сохранения точек. Err: {e} [FATAL]")
        sys.exit(1)
    # END_BLOCK_SAVE_POINTS
# END_FUNCTION_handle_generate

# START_FUNCTION_handle_export_csv
# START_CONTRACT:
# PURPOSE: Обработка команды export-csv - экспорт данных в CSV.
# INPUTS: 
# - [Аргументы командной строки] => args: argparse.Namespace
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Создает CSV файл с данными из БД.
# KEYWORDS:[PATTERN(6): CommandHandler; CONCEPT(8): DataExport]
# END_CONTRACT
def handle_export_csv(args: argparse.Namespace) -> None:
    """Обрабатывает команду export-csv."""
    
    # START_BLOCK_LOAD_POINTS: [Загрузка точек из БД]
    try:
        points = load_points(DB_PATH)
        logger.info(f"[DatabaseLoad][IMP:7][handle_export_csv][LOAD_POINTS][ReturnData] Загружено {len(points)} точек из БД [VALUE]")
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][handle_export_csv][LOAD_POINTS][ExceptionEnrichment] Ошибка загрузки точек. Err: {e} [FATAL]")
        sys.exit(1)
    # END_BLOCK_LOAD_POINTS

    # START_BLOCK_WRITE_CSV: [Запись CSV файла]
    try:
        with open(args.out, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['x', 'y'])
            writer.writeheader()
            writer.writerows(points)
        
        logger.info(f"[CSVExport][IMP:9][handle_export_csv][WRITE_CSV][ReturnData] Данные экспортированы в {args.out} [VALUE]")
        print(f"[OK] Экспортировано {len(points)} точек в файл {args.out}")
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][handle_export_csv][WRITE_CSV][ExceptionEnrichment] Ошибка экспорта в CSV. Local vars: out={args.out}. Err: {e} [FATAL]")
        sys.exit(1)
    # END_BLOCK_WRITE_CSV
# END_FUNCTION_handle_export_csv

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE: Главная точка входа CLI - парсинг аргументов и диспетчеризация.
# INPUTS: 
# - [Аргументы командной строки] => argv: list (по умолчанию sys.argv[1:])
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Выполняет соответствующую команду или выводит справку.
# KEYWORDS:[PATTERN(6): EntryPoint; CONCEPT(8): CommandPattern]
# END_CONTRACT
def main(argv: list = None) -> None:
    """Главная точка входа CLI."""
    
    # START_BLOCK_SETUP_PARSER: [Настройка парсера аргументов]
    parser = argparse.ArgumentParser(
        description='CLI интерфейс для Lesson 6 - Генерация парабол',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')
    
    # Команда generate
    parser_generate = subparsers.add_parser('generate', help='Генерация точек параболы')
    parser_generate.set_defaults(func=handle_generate)
    
    # Команда export-csv
    parser_export = subparsers.add_parser('export-csv', help='Экспорт данных в CSV')
    parser_export.add_argument('--out', required=True, help='Путь к выходному CSV файлу')
    parser_export.set_defaults(func=handle_export_csv)
    
    args = parser.parse_args(argv)
    # END_BLOCK_SETUP_PARSER

    # START_BLOCK_DISPATCH_COMMAND: [Диспетчеризация команд]
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    try:
        args.func(args)
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][main][DISPATCH_COMMAND][ExceptionEnrichment] Неизвестная ошибка. Err: {e} [FATAL]")
        sys.exit(1)
    # END_BLOCK_DISPATCH_COMMAND
# END_FUNCTION_main

if __name__ == '__main__':
    main()
