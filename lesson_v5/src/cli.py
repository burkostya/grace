# FILE:lesson_v5/src/cli.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Интерфейс командной строки (CLI) для управления генерацией параболы.
# SCOPE:Парсинг аргументов, вызов бизнес-логики и сохранение в БД.
# INPUT:Аргументы командной строки (a, c, range, step).
# OUTPUT:Системный код выхода (exit code) и вывод в консоль.
# KEYWORDS:[DOMAIN(8): CLI; CONCEPT(7): AgenticUX; TECH(9): argparse]
# LINKS:[USES_API(8): argparse; WRITES_DATA_TO(9): lesson_v5/parabola.db]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание CLI интерфейса.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Точка входа CLI] => main
# END_MODULE_MAP
#
# START_USE_CASES:
# - [main]: Agent -> ExecuteCommand -> DataGeneratedAndStored
# END_USE_CASES

import argparse
import sys
import logging
import pandas as pd
from lesson_v5.src.config_manager import load_config
from lesson_v5.src.database_manager import DatabaseManager
from lesson_v5.src.parabola_logic import generate_parabola_points

# Настройка логирования для CLI
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s][IMP:9][CLI] %(message)s'
)
logger = logging.getLogger(__name__)

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE:Парсит аргументы и выполняет команды CLI.
# INPUTS: 
# - list => args: Список аргументов командной строки
# OUTPUTS: 
# - int -Код выхода (0 - успех, 1 - ошибка)
# SIDE_EFFECTS: Запись в БД, вывод в stdout.
# KEYWORDS:[PATTERN(6): EntryPoint; CONCEPT(8): CommandPattern]
# END_CONTRACT
def main(args=None):
    """Основная функция CLI."""
    
    # START_BLOCK_PARSE_ARGS: [Настройка парсера аргументов]
    parser = argparse.ArgumentParser(description="CLI для генерации точек параболы y = ax^2 + c")
    subparsers = parser.add_subparsers(dest="command", help="Команды")

    # Команда generate
    gen_parser = subparsers.add_parser("generate", help="Генерация точек")
    gen_parser.add_argument("--a", type=float, help="Коэффициент a")
    gen_parser.add_argument("--c", type=float, help="Коэффициент c")
    gen_parser.add_argument("--range", type=float, nargs=2, help="Диапазон x (min max)")
    gen_parser.add_argument("--step", type=float, help="Шаг x")

    # Команда export-csv
    export_parser = subparsers.add_parser("export-csv", help="Экспорт данных в CSV")
    export_parser.add_argument("--output", type=str, default="parabola_export.csv", help="Путь к файлу")

    parsed_args = parser.parse_args(args)
    # END_BLOCK_PARSE_ARGS

    # START_BLOCK_EXECUTE_COMMAND: [Выполнение выбранной команды]
    try:
        config = load_config()
        db = DatabaseManager(config["db_path"])

        if parsed_args.command == "generate":
            # START_BLOCK_GENERATE: [Логика генерации]
            a = parsed_args.a if parsed_args.a is not None else config["default_a"]
            c = parsed_args.c if parsed_args.c is not None else config["default_c"]
            range_x = parsed_args.range if parsed_args.range is not None else config["range_x"]
            step = parsed_args.step if parsed_args.step is not None else config["step"]

            logger.info(f"[BeliefState][IMP:9][CLI][GENERATE][Start] Генерация: a={a}, c={c}, range={range_x}, step={step} [VALUE]")
            
            points = generate_parabola_points(a, c, range_x, step)
            
            # Подготовка данных для БД (a, c, x, y)
            db_points = [(a, c, x, y) for x, y in points]
            db.save_points(db_points)
            
            print(f"Успешно сгенерировано и сохранено {len(points)} точек.")
            return 0
            # END_BLOCK_GENERATE

        elif parsed_args.command == "export-csv":
            # START_BLOCK_EXPORT: [Логика экспорта]
            logger.info(f"[BeliefState][IMP:9][CLI][EXPORT][Start] Экспорт в {parsed_args.output} [VALUE]")
            data = db.get_all_points()
            if not data:
                print("Нет данных для экспорта.")
                return 0
            
            df = pd.DataFrame(data, columns=["a", "c", "x", "y", "timestamp"])
            df.to_csv(parsed_args.output, index=False)
            print(f"Данные экспортированы в {parsed_args.output}")
            return 0
            # END_BLOCK_EXPORT

        else:
            parser.print_help()
            return 0

    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][CLI][EXECUTE][Exception] Ошибка выполнения: {e} [FATAL]")
        return 1
    # END_BLOCK_EXECUTE_COMMAND

if __name__ == "__main__":
    sys.exit(main())
# END_FUNCTION_main
