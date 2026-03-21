# FILE:lesson_11/src/cli.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Автономное управление бэкендом через интерфейс командной строки (CLI).
# SCOPE:Обработка команд генерации данных и экспорта в CSV.
# INPUT:Аргументы командной строки (sys.argv).
# OUTPUT:Результаты выполнения команд в консоль, файлы (CSV) и БД.
# KEYWORDS:[DOMAIN(8): CLI; CONCEPT(7): BackendControl; TECH(9): argparse, csv]
# LINKS:[USES_API(8): argparse, csv, logging; READS_DATA_FROM(7): config_manager, database_manager, parabola_logic]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется argparse?
# A: Это стандартная библиотека Python для создания надежных CLI интерфейсов с автоматической генерацией help.
# Q: Зачем нужно логирование в файл app_11.log?
# A: Для обеспечения трассируемости действий автономного агента и отладки по LDD 2.0.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичная реализация CLI модуля с командами generate и export-csv.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Выполняет генерацию точек на основе конфига] => cmd_generate
# FUNC 10[Экспортирует данные из БД в CSV файл] => cmd_export_csv
# FUNC 10[Точка входа в CLI приложение] => main
# END_MODULE_MAP
#
# START_USE_CASES:
# - [cmd_generate]: Admin -> Run "generate" -> DataCalculatedAndStored
# - [cmd_export_csv]: Admin -> Run "export-csv --out file.csv" -> DataExportedToCSV
# END_USE_CASES

import argparse
import csv
import logging
import os
import sys

# Импорт внутренних модулей
from lesson_11.src.config_manager import load_config
from lesson_11.src.database_manager import save_points, get_points, init_db
from lesson_11.src.parabola_logic import calculate_points

# START_BLOCK_LOGGING_SETUP: [Настройка LDD 2.0 логирования]
LOG_FILE = "lesson_11/app_11.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logger = logging.getLogger("cli_backend")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    # Файловый обработчик
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Консольный обработчик для CLI фидбека
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

logger.info(f"[System][IMP:9][cli][LOGGING_SETUP][Init] CLI модуль запущен. Лог: {LOG_FILE} [SUCCESS]")
# END_BLOCK_LOGGING_SETUP

# START_FUNCTION_cmd_generate
# START_CONTRACT:
# PURPOSE:Считывает параметры из конфига, вычисляет точки и сохраняет в БД.
# INPUTS: 
# - argparse.Namespace => args: Аргументы команды
# OUTPUTS: 
# - bool - Успешность операции
# SIDE_EFFECTS: Запись в БД parabola_11.db.
# KEYWORDS:[PATTERN(8): Command; CONCEPT(9): DataGeneration]
# COMPLEXITY_SCORE: 5[Линейный процесс: конфиг -> расчет -> БД.]
# END_CONTRACT
def cmd_generate(args):
    """
    Команда генерации данных. Считывает текущие настройки из config.json,
    выполняет расчет точек параболы через parabola_logic и сохраняет результат
    в базу данных. Используется для автономного обновления данных без UI.
    """
    logger.info(f"[Flow][IMP:5][cmd_generate][START][Operation] Запуск генерации данных из конфига [INFO]")
    
    # START_BLOCK_LOAD_CONFIG: [Загрузка параметров]
    config = load_config()
    a = config.get("a", 1.0)
    c = config.get("c", 0.0)
    x_min = config.get("x_min", -10.0)
    x_max = config.get("x_max", 10.0)
    logger.debug(f"[IO][IMP:7][cmd_generate][LOAD_CONFIG][Params] Загружено: a={a}, c={c}, x_range=[{x_min}, {x_max}] [SUCCESS]")
    # END_BLOCK_LOAD_CONFIG
    
    # START_BLOCK_CALC_AND_SAVE: [Расчет и сохранение]
    try:
        points = calculate_points(a, c, x_min, x_max)
        logger.info(f"[BusinessLogic][IMP:9][cmd_generate][CALC_AND_SAVE][Calc] Рассчитано {len(points)} точек [VALUE]")
        
        save_points(points)
        logger.info(f"[IO][IMP:8][cmd_generate][CALC_AND_SAVE][DB] Точки успешно сохранены в БД [SUCCESS]")
        return True
    except Exception as e:
        logger.error(f"[SystemError][IMP:10][cmd_generate][CALC_AND_SAVE][Error] Сбой генерации: {e} [FATAL]")
        return False
    # END_BLOCK_CALC_AND_SAVE
# END_FUNCTION_cmd_generate

# START_FUNCTION_cmd_export_csv
# START_CONTRACT:
# PURPOSE:Экспортирует все точки из БД в указанный CSV файл.
# INPUTS: 
# - argparse.Namespace => args: Аргументы команды (содержит out)
# OUTPUTS: 
# - bool - Успешность операции
# SIDE_EFFECTS: Создание/перезапись CSV файла.
# KEYWORDS:[PATTERN(8): Command; CONCEPT(9): DataExport]
# COMPLEXITY_SCORE: 5[Чтение из БД и запись в файл.]
# END_CONTRACT
def cmd_export_csv(args):
    """
    Команда экспорта данных. Извлекает все записи из таблицы точек в БД
    и записывает их в CSV файл по пути, указанному в аргументе --out.
    Если данных в БД нет, выводит предупреждение.
    """
    filename = args.out
    logger.info(f"[Flow][IMP:5][cmd_export_csv][START][Target] Экспорт в файл: {filename} [INFO]")
    
    # START_BLOCK_FETCH_DB: [Получение данных]
    points = get_points()
    if not points:
        logger.warning(f"[Boundary][IMP:8][cmd_export_csv][FETCH_DB][NoData] В БД нет данных для экспорта [WARN]")
        return False
    logger.debug(f"[IO][IMP:7][cmd_export_csv][FETCH_DB][Success] Получено {len(points)} точек [SUCCESS]")
    # END_BLOCK_FETCH_DB
    
    # START_BLOCK_WRITE_CSV: [Запись в файл]
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['x', 'y']) # Header
            writer.writerows(points)
        
        logger.info(f"[BeliefState][IMP:10][cmd_export_csv][WRITE_CSV][Success] Файл {filename} успешно создан [SUCCESS]")
        return True
    except Exception as e:
        logger.error(f"[SystemError][IMP:10][cmd_export_csv][WRITE_CSV][Error] Ошибка записи CSV: {e} [FATAL]")
        return False
    # END_BLOCK_WRITE_CSV
# END_FUNCTION_cmd_export_csv

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE:Парсинг аргументов и маршрутизация команд.
# INPUTS: Нет
# OUTPUTS: Нет
# SIDE_EFFECTS: Инициализация БД.
# KEYWORDS:[PATTERN(9): Router; CONCEPT(8): EntryPoint]
# COMPLEXITY_SCORE: 6[Настройка парсера и обработка подкоманд.]
# END_CONTRACT
def main():
    """
    Главная функция CLI. Настраивает парсер argparse с подкомандами generate и export-csv.
    Инициализирует базу данных перед выполнением команд для обеспечения целостности.
    """
    # START_BLOCK_INIT_DB: [Инициализация БД]
    init_db()
    # END_BLOCK_INIT_DB

    # START_BLOCK_SETUP_PARSER: [Настройка argparse]
    parser = argparse.ArgumentParser(description="Lesson 11 Backend CLI Control")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Команда generate
    subparsers.add_parser("generate", help="Generate points based on config.json")
    
    # Команда export-csv
    export_parser = subparsers.add_parser("export-csv", help="Export points from DB to CSV")
    export_parser.add_argument("--out", required=True, help="Output CSV filename")
    
    args = parser.parse_args()
    logger.debug(f"[Trace][IMP:4][main][SETUP_PARSER][Args] Получена команда: {args.command} [INFO]")
    # END_BLOCK_SETUP_PARSER
    
    # START_BLOCK_EXECUTION: [Выполнение команды]
    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "export-csv":
        cmd_export_csv(args)
    else:
        parser.print_help()
        logger.info(f"[Flow][IMP:5][main][EXECUTION][NoCommand] Команда не указана, выведен help [INFO]")
    # END_BLOCK_EXECUTION

if __name__ == "__main__":
    main()
# END_FUNCTION_main
