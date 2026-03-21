# FILE:lesson_14/src/cli.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Реализация CLI интерфейса (Agentic UX) для управления расчетом и экспортом данных.
# SCOPE:Команды generate и export-csv.
# INPUT:Аргументы командной строки.
# OUTPUT:Коды завершения, логи в app_14.log, CSV файлы.
# KEYWORDS:DOMAIN(CLI); CONCEPT(Agentic UX); TECH(Python, argparse, logging)
# LINKS:USES_API(argparse); USES_API(logging)
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется argparse?
# A: Стандартная библиотека Python для создания надежных CLI интерфейсов с автоматической генерацией help.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание CLI интерфейса.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC[10][Точка входа CLI] => main
# END_MODULE_MAP
#
# START_USE_CASES:
# - [main]:User -> CLI Command -> Business Action (Generate/Export)
# END_USE_CASES

import argparse
import sys
import os
import logging
import csv

# START_BLOCK_IMPORTS: [Отложенный импорт для ускорения help и предотвращения сбоев]
def get_managers():
    from lesson_14.src.config_manager import ConfigManager
    from lesson_14.src.database_manager import DatabaseManager
    from lesson_14.src.trig_logic import calculate_trig_points
    return ConfigManager, DatabaseManager, calculate_trig_points
# END_BLOCK_IMPORTS

# Настройка логирования
logger = logging.getLogger("lesson_14.cli")
log_file = "lesson_14/app_14.log"
os.makedirs(os.path.dirname(log_file), exist_ok=True)
file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE:Парсинг аргументов и выполнение команд.
# INPUTS: 
# - list =>args: Список аргументов (sys.argv[1:])
# OUTPUTS: 
# - int -Код завершения (0 - успех, 1 - ошибка)
# SIDE_EFFECTS: Изменение БД, создание файлов, запись логов.
# KEYWORDS:PATTERN(Command); CONCEPT(CLI)
# COMPLEXITY_SCORE:6
# END_CONTRACT
def main(args=None):
    """
    Основная функция CLI. Настраивает парсер, определяет подкоманды generate и export-csv,
    и вызывает соответствующую логику. Реализует паттерн Agentic UX через подробное логирование.
    """
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Lesson 14 CLI Tool - Trigonometric Functions")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Команда generate
    gen_parser = subparsers.add_parser("generate", help="Calculate trigonometric points and save to DB")
    
    # Команда export-csv
    export_parser = subparsers.add_parser("export-csv", help="Export points from DB to CSV")
    export_parser.add_argument("--out", required=True, help="Output CSV filename")

    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        return 0

    # START_BLOCK_EXECUTION: [Выполнение выбранной команды]
    try:
        ConfigManager, DatabaseManager, calculate_trig_points = get_managers()
        config_mgr = ConfigManager()
        db_mgr = DatabaseManager()
        
        if parsed_args.command == "generate":
            # START_BLOCK_GENERATE: [Логика генерации]
            logger.info(f"[CLI][IMP:7][main][GENERATE][Flow] Начало выполнения команды generate. [INFO]")
            
            config = config_mgr.load_config()
            func_type = config.get("function_type", "sin")
            x_start = config.get("x_start", 0.0)
            x_end = config.get("x_end", 6.28)
            num_points = config.get("num_points", 100)
            
            points = calculate_trig_points(func_type, x_start, x_end, num_points)
            
            db_mgr.init_db()
            success = db_mgr.save_points(points)
            
            if success:
                logger.info(f"[BeliefState][IMP:9][main][GENERATE][Status] Успешно сгенерировано и сохранено {len(points)} точек для {func_type}(x). [SUCCESS]")
                print(f"Successfully generated {len(points)} points for {func_type}(x).")
                return 0
            else:
                logger.error(f"[CLI][IMP:10][main][GENERATE][Error] Сбой при сохранении точек в БД. [FATAL]")
                return 1
            # END_BLOCK_GENERATE

        elif parsed_args.command == "export-csv":
            # START_BLOCK_EXPORT: [Логика экспорта]
            logger.info(f"[CLI][IMP:7][main][EXPORT][Flow] Начало экспорта в {parsed_args.out}. [INFO]")
            
            points = db_mgr.get_points()
            if not points:
                logger.warning(f"[CLI][IMP:8][main][EXPORT][Warn] Нет данных в БД для экспорта. [WARN]")
                print("No data found in database.")
                return 1
            
            try:
                os.makedirs(os.path.dirname(os.path.abspath(parsed_args.out)), exist_ok=True)
                with open(parsed_args.out, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["x", "y"])
                    writer.writerows(points)
                
                logger.info(f"[BeliefState][IMP:9][main][EXPORT][Status] Данные успешно экспортированы в {parsed_args.out}. [SUCCESS]")
                print(f"Exported {len(points)} points to {parsed_args.out}.")
                return 0
            except Exception as e:
                logger.critical(f"[SystemError][IMP:10][main][EXPORT][Exception] Ошибка записи CSV: {e} [FATAL]")
                return 1
            # END_BLOCK_EXPORT

    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][main][EXECUTION][Exception] Непредвиденная ошибка CLI: {e} [FATAL]")
        return 1
    # END_BLOCK_EXECUTION

if __name__ == "__main__":
    sys.exit(main())
# END_FUNCTION_main
