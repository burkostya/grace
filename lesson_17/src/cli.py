# FILE:lesson_17/src/cli.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Точка входа CLI для Lesson_17 (Agentic UX).
# SCOPE:Автономное управление генерацией и экспортом данных для тригонометрической функции.
# INPUT:Аргументы командной строки.
# OUTPUT:Статус выполнения или CSV файл.
# KEYWORDS:[DOMAIN(8): CLI; TECH(9): Argparse, Agentic UX]
# LINKS:[USES_API(8): argparse, pandas]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля CLI для тригонометрической функции.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Парсит аргументы и запускает команды] => main
# END_MODULE_MAP

import argparse
import logging
import sys
import os
import pandas as pd

# Добавляем корень проекта в PYTHONPATH для корректных импортов
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from lesson_17.src.config_manager import load_config
from lesson_17.src.trig_logic import calculate_trig
from lesson_17.src.database_manager import save_points, get_points

# Настройка логирования для CLI
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("lesson_17/app_17.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE:Парсинг аргументов и выполнение команд CLI.
# INPUTS: Нет (использует sys.argv)
# OUTPUTS: Нет
# COMPLEXITY_SCORE: 7
# END_CONTRACT
def main():
    """
    Основная функция CLI. Поддерживает команды:
    - generate: Считывает параметры из config.json, рассчитывает тригонометрическую функцию и сохраняет в БД.
    - export-csv: Считывает данные из БД и сохраняет в указанный CSV файл.
    """
    # START_BLOCK_PARSE_ARGS: [Настройка парсера]
    parser = argparse.ArgumentParser(description="Lesson_17 CLI (Agentic UX)")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Команда generate
    subparsers.add_parser("generate", help="Generate data based on config.json")
    
    # Команда export-csv
    export_parser = subparsers.add_parser("export-csv", help="Export data from DB to CSV")
    export_parser.add_argument("--out", required=True, help="Output CSV file path")
    
    args = parser.parse_args()
    # END_BLOCK_PARSE_ARGS
    
    # START_BLOCK_EXECUTE_COMMAND: [Выполнение выбранной команды]
    if args.command == "generate":
        logger.info(f"[CLI][IMP:7][main][EXECUTE_COMMAND][Start] Команда generate запущена. [OK]")
        config = load_config()
        df = calculate_trig(
            A=config['A'],
            B=config['B'],
            C=config['C'],
            D=config['D'],
            x_min=config['x_min'],
            x_max=config['x_max']
        )
        save_points(df)
        logger.info(f"[CLI][IMP:9][main][EXECUTE_COMMAND][Success] Данные успешно сгенерированы и сохранены. [OK]")
        
    elif args.command == "export-csv":
        logger.info(f"[CLI][IMP:7][main][EXECUTE_COMMAND][Start] Команда export-csv запущена. [OK]")
        df = get_points()
        if df.empty:
            logger.warning(f"[CLI][IMP:8][main][EXECUTE_COMMAND][Empty] БД пуста. Экспорт невозможен. [WARN]")
            return
        
        os.makedirs(os.path.dirname(args.out), exist_ok=True) if os.path.dirname(args.out) else None
        df.to_csv(args.out, index=False)
        logger.info(f"[CLI][IMP:9][main][EXECUTE_COMMAND][Success] Данные экспортированы в {args.out}. [OK]")
        
    else:
        parser.print_help()
    # END_BLOCK_EXECUTE_COMMAND

if __name__ == "__main__":
    main()
# END_FUNCTION_main
