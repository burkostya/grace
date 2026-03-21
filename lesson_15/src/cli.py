# FILE: lesson_15/src/cli.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: CLI интерфейс для автономного управления бэкендом (Agentic UX).
# SCOPE: CLI, Automation.
# INPUT: Аргументы командной строки (generate, export-csv).
# OUTPUT: Результаты в БД или CSV файл.
# KEYWORDS: [DOMAIN(8): CLI; TECH(7): Argparse; CONCEPT(9): AgenticUX]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание CLI интерфейса.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Точка входа CLI] => main
# END_MODULE_MAP

import argparse
import os
import sys
import logging
import pandas as pd

# Добавляем корень проекта в PYTHONPATH для импортов
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from lesson_15.src.config_manager import ConfigManager
from lesson_15.src.database_manager import DatabaseManager
from lesson_15.src.parabola_logic import generate_points

# Настройка логирования
LOG_FILE = os.path.join(os.path.dirname(__file__), "../app_15.log")
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s][%(asctime)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE: Обработка команд CLI.
# INPUTS: Нет (использует sys.argv)
# OUTPUTS: Нет
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def main():
    """
    Основная функция CLI, которая парсит аргументы и вызывает соответствующие методы бэкенда.
    Поддерживает команды 'generate' (автоматически из конфига) и 'export-csv'.
    """
    
    # START_BLOCK_SETUP: [Инициализация менеджеров]
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config.json")
    db_path = os.path.join(base_dir, "parabola.db")
    
    config_mgr = ConfigManager(config_path)
    db_mgr = DatabaseManager(db_path)
    # END_BLOCK_SETUP

    # START_BLOCK_PARSE_ARGS: [Парсинг аргументов]
    parser = argparse.ArgumentParser(description="Lesson 15 CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Команда generate
    subparsers.add_parser("generate", help="Generate points based on config.json")
    
    # Команда export-csv
    export_parser = subparsers.add_parser("export-csv", help="Export points from DB to CSV")
    export_parser.add_argument("--out", required=True, help="Output CSV filename")
    
    args = parser.parse_args()
    # END_BLOCK_PARSE_ARGS

    # START_BLOCK_EXECUTE_COMMAND: [Выполнение команд]
    if args.command == "generate":
        # Загрузка конфига
        config = config_mgr.load()
        logger.info(f"[CLI][IMP:7][main][Command] Выполнение generate с параметрами: {config} [INFO]")
        
        # Генерация точек
        df = generate_points(
            a=config["a"],
            c=config["c"],
            x_min=config["x_min"],
            x_max=config["x_max"]
        )
        
        # Сохранение в БД
        if db_mgr.save_points(df):
            logger.info(f"[BeliefState][IMP:9][main][Result] Генерация завершена успешно. [VALUE]")
        else:
            logger.error(f"[CLI][IMP:10][main][Error] Ошибка сохранения в БД. [FATAL]")
            sys.exit(1)

    elif args.command == "export-csv":
        logger.info(f"[CLI][IMP:7][main][Command] Экспорт данных в {args.out} [INFO]")
        
        # Получение данных из БД
        df = db_mgr.get_points()
        
        if df.empty:
            logger.warning(f"[CLI][IMP:8][main][Warning] БД пуста, нечего экспортировать. [WARN]")
        else:
            try:
                df.to_csv(args.out, index=False)
                logger.info(f"[BeliefState][IMP:9][main][Result] Данные экспортированы в {args.out}. [VALUE]")
            except Exception as e:
                logger.error(f"[CLI][IMP:10][main][Error] Ошибка записи CSV: {e} [FATAL]")
                sys.exit(1)
    else:
        parser.print_help()
    # END_BLOCK_EXECUTE_COMMAND

if __name__ == "__main__":
    main()
# END_FUNCTION_main
