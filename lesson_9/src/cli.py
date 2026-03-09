# FILE:lesson_9/src/cli.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Интерфейс командной строки (CLI) для управления данными параболы.
# SCOPE: Команды генерации данных на основе конфига и экспорта данных в CSV.
# INPUT:Аргументы командной строки, config.json, SQLite БД.
# OUTPUT: Записи в БД, CSV файл, консольный вывод.
# KEYWORDS:[DOMAIN(8): CLI; CONCEPT(7): Automation; TECH(9): argparse, csv]
# LINKS:[USES_API(8): argparse, csv; USES_MODULE(9): config_manager, database_manager, parabola_logic]
# LINKS_TO_SPECIFICATION:[DevelopmentPlan.md:23-30]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание CLI с командами generate и export-csv.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC [9][Команда генерации данных] => cmd_generate
# FUNC [9][Команда экспорта в CSV] => cmd_export_csv
# FUNC [10][Точка входа CLI] => main
# END_MODULE_MAP
#
# START_USE_CASES:
# - [cmd_generate]: Agent -> Run 'generate' -> DataCalculatedAndStored
# - [cmd_export_csv]: Agent -> Run 'export-csv' -> DataExportedToCSV
# END_USE_CASES

import argparse
import csv
import sys
import logging
from lesson_9.src.config_manager import load_config
from lesson_9.src.database_manager import save_points, get_points
from lesson_9.src.parabola_logic import calculate_parabola_points

# Настройка логгера для LDD 2.0
logger = logging.getLogger("lesson_9")

# START_FUNCTION_cmd_generate
# START_CONTRACT:
# PURPOSE:Чтение конфигурации, расчет точек и сохранение в БД.
# INPUTS: 
# - None
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Обновление данных в SQLite БД.
# KEYWORDS:[PATTERN(8): Command; CONCEPT(9): DataFlow]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def cmd_generate():
    """
    Функция реализует бизнес-логику команды 'generate'. 
    Она загружает параметры из config.json через config_manager, 
    вызывает расчет точек в parabola_logic и сохраняет результат 
    в базу данных через database_manager.
    """
    # START_BLOCK_LOAD_CONFIG: [Загрузка параметров]
    config = load_config()
    logger.info(f"[CLI][IMP:7][cmd_generate][LOAD_CONFIG][Success] Параметры загружены: {config} [INFO]")
    # END_BLOCK_LOAD_CONFIG

    # START_BLOCK_CALCULATE: [Расчет точек]
    points = calculate_parabola_points(
        a=config.get("a", 1.0),
        c=config.get("c", 0.0),
        x_min=config.get("x_min", -10.0),
        x_max=config.get("x_max", 10.0)
    )
    # END_BLOCK_CALCULATE

    # START_BLOCK_SAVE_DB: [Сохранение в БД]
    if points:
        success = save_points(points)
        if success:
            print(f"Successfully generated and saved {len(points)} points to database.")
            logger.info(f"[CLI][IMP:9][cmd_generate][SAVE_DB][Success] Данные успешно обновлены в БД. [VALUE]")
        else:
            print("Error: Failed to save points to database.")
            logger.error(f"[CLI][IMP:10][cmd_generate][SAVE_DB][Error] Сбой при сохранении в БД. [FATAL]")
    else:
        print("Warning: No points were generated.")
        logger.warning(f"[CLI][IMP:8][cmd_generate][CALCULATE][Empty] Список точек пуст. [WARNING]")
    # END_BLOCK_SAVE_DB
# END_FUNCTION_cmd_generate

# START_FUNCTION_cmd_export_csv
# START_CONTRACT:
# PURPOSE:Экспорт данных из БД в CSV файл.
# INPUTS: 
# - str => output_file: Путь к выходному файлу.
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Создание CSV файла на диске.
# KEYWORDS:[PATTERN(8): Export; CONCEPT(9): FileIO]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def cmd_export_csv(output_file: str):
    """
    Функция извлекает все точки из базы данных и записывает их в CSV файл.
    Файл содержит заголовки 'x' и 'y'. Используется стандартная библиотека csv.
    """
    # START_BLOCK_FETCH_DATA: [Получение данных из БД]
    points = get_points()
    if not points:
        print("Error: No data found in database to export.")
        logger.error(f"[CLI][IMP:8][cmd_export_csv][FETCH_DATA][Empty] БД пуста, экспорт невозможен. [WARNING]")
        return
    # END_BLOCK_FETCH_DATA

    # START_BLOCK_WRITE_CSV: [Запись в файл]
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['x', 'y'])
            writer.writerows(points)
        print(f"Successfully exported {len(points)} points to {output_file}")
        logger.info(f"[CLI][IMP:9][cmd_export_csv][WRITE_CSV][Success] Экспорт завершен: {output_file} [VALUE]")
    except Exception as e:
        print(f"Error: Failed to write CSV file: {e}")
        logger.critical(f"[CLI][IMP:10][cmd_export_csv][WRITE_CSV][Error] Ошибка записи CSV: {e} [FATAL]")
    # END_BLOCK_WRITE_CSV
# END_FUNCTION_cmd_export_csv

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE:Парсинг аргументов и запуск соответствующих команд.
# INPUTS: 
# - list[str] => args: Список аргументов командной строки.
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Выполнение команд CLI.
# KEYWORDS:[PATTERN(7): EntryPoint; CONCEPT(8): Dispatcher]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def main():
    """
    Главная точка входа CLI. Настраивает argparse для обработки команд 
    'generate' и 'export-csv'. Обеспечивает дружелюбный интерфейс 
    для автоматизации задач.
    """
    parser = argparse.ArgumentParser(description="Lesson 9 Parabola CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Команда generate
    subparsers.add_parser("generate", help="Generate points based on config.json and save to DB")

    # Команда export-csv
    export_parser = subparsers.add_parser("export-csv", help="Export points from DB to CSV")
    export_parser.add_argument("--out", required=True, help="Output CSV file path")

    args = parser.parse_args()

    if args.command == "generate":
        cmd_generate()
    elif args.command == "export-csv":
        cmd_export_csv(args.out)
    else:
        parser.print_help()
# END_FUNCTION_main

if __name__ == "__main__":
    main()
