# FILE:lesson_v3/src/cli.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:CLI интерфейс для автономного управления Lesson_v3.
# SCOPE:Генерация данных и экспорт в CSV.
# INPUT:Аргументы командной строки (generate, export-csv).
# OUTPUT:Результаты в БД или CSV файл.
# KEYWORDS:[DOMAIN(8):CLI; CONCEPT(7):Agentic_UX; TECH(9):Python_argparse]
# LINKS:[USES_API(9):config_manager, database_manager, parabola_logic]
# END_MODULE_CONTRACT

# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание CLI интерфейса.]
# END_CHANGE_SUMMARY

# START_MODULE_MAP:
# FUNC 10[Точка входа CLI] => main
# FUNC 10[Команда генерации данных] => handle_generate
# FUNC 10[Команда экспорта в CSV] => handle_export
# END_MODULE_MAP

import argparse
import os
import sys
import logging
import pandas as pd

# Добавляем корень проекта в sys.path для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from lesson_v3.src.config_manager import load_config
from lesson_v3.src.database_manager import init_db, save_points, load_points
from lesson_v3.src.parabola_logic import generate_parabola_points

# Настройка логирования
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app_v3.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "parabola.db")

# START_FUNCTION_handle_generate
# START_CONTRACT:
# PURPOSE:Генерация данных на основе параметров из config.json.
# INPUTS: Нет
# OUTPUTS: 
# - bool -Успешность операции
# SIDE_EFFECTS: Обновляет БД.
# END_CONTRACT
def handle_generate() -> bool:
    """Выполняет генерацию точек в БД."""
    # START_BLOCK_GENERATE_FLOW: [Поток генерации]
    try:
        config = load_config(CONFIG_PATH)
        points = generate_parabola_points(
            a=config["a"], 
            c=config["c"], 
            x_min=config["x_min"], 
            x_max=config["x_max"]
        )
        
        init_db(DB_PATH)
        success = save_points(DB_PATH, points)
        
        if success:
            logger.info(f"[BeliefState][IMP:9][handle_generate][GENERATE_FLOW][Success] Данные успешно сгенерированы. [VALUE]")
        return success
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][handle_generate][GENERATE_FLOW][Exception] Ошибка генерации: {e} [FATAL]")
        return False
    # END_BLOCK_GENERATE_FLOW
# END_FUNCTION_handle_generate

# START_FUNCTION_handle_export
# START_CONTRACT:
# PURPOSE:Экспорт данных из БД в CSV.
# INPUTS: 
# - str =>out_file: Путь к выходному файлу
# OUTPUTS: 
# - bool -Успешность операции
# SIDE_EFFECTS: Создает CSV файл.
# END_CONTRACT
def handle_export(out_file: str) -> bool:
    """Экспортирует данные из БД в CSV."""
    # START_BLOCK_EXPORT_FLOW: [Поток экспорта]
    try:
        df = load_points(DB_PATH)
        if df.empty:
            logger.warning(f"[CLI][IMP:7][handle_export][EXPORT_FLOW][EmptyDB] БД пуста. Экспорт невозможен. [WARN]")
            return False
            
        df.to_csv(out_file, index=False)
        logger.info(f"[BeliefState][IMP:9][handle_export][EXPORT_FLOW][Success] Данные экспортированы в {out_file}. [VALUE]")
        return True
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][handle_export][EXPORT_FLOW][Exception] Ошибка экспорта: {e} [FATAL]")
        return False
    # END_BLOCK_EXPORT_FLOW
# END_FUNCTION_handle_export

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE:Парсинг аргументов и запуск команд.
# INPUTS: Нет
# OUTPUTS: Нет
# SIDE_EFFECTS: Выполняет команды CLI.
# END_CONTRACT
def main():
    """Точка входа CLI."""
    # START_BLOCK_PARSE_ARGS: [Парсинг аргументов]
    parser = argparse.ArgumentParser(description="Lesson_v3 CLI: Parabola Generator")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Команда generate
    subparsers.add_parser("generate", help="Generate points based on config.json")
    
    # Команда export-csv
    export_parser = subparsers.add_parser("export-csv", help="Export points to CSV")
    export_parser.add_argument("--out", required=True, help="Output CSV filename")
    
    args = parser.parse_args()
    # END_BLOCK_PARSE_ARGS

    # START_BLOCK_EXECUTE_COMMAND: [Выполнение команды]
    if args.command == "generate":
        if handle_generate():
            sys.exit(0)
        else:
            sys.exit(1)
    elif args.command == "export-csv":
        if handle_export(args.out):
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)
    # END_BLOCK_EXECUTE_COMMAND

if __name__ == "__main__":
    main()
# END_FUNCTION_main
