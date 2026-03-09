# FILE: lesson_v7/src/cli.py
# VERSION: 1.0.1
# START_MODULE_CONTRACT:
# PURPOSE: Реализация CLI интерфейса для автономного управления приложением.
# SCOPE: Команды generate (генерация точек) и export-csv (экспорт в CSV).
# INPUT: Аргументы командной строки через argparse.
# OUTPUT: Выполнение команд и вывод результатов в stdout/stderr.
# KEYWORDS:[DOMAIN(7): CLI; CONCEPT(6): CommandLineInterface; TECH(9): Argparse]
# LINKS:[USES_API(10): config_manager; USES_API(10): parabola_logic; USES_API(10): database_manager]
# END_MODULE_CONTRACT
#
# START_INVARIANTS:
# - Команда generate ВСЕГДА считывает параметры из config.json.
# - Команда export-csv ВСЕГДА сохраняет данные в указанный файл.
# - При успешном выполнении команды возвращается exit code 0.
# END_INVARIANTS
#
# START_RATIONALE:
# Q: Почему используется argparse вместо click или typer?
# A: argparse встроен в стандартную библиотеку Python, не требует дополнительных зависимостей и полностью соответствует требованиям Agentic UX.
# Q: Почему export-csv использует pandas вместо ручного формирования CSV?
# A: pandas обеспечивает корректную обработку данных, экранирование и форматирование, что критично для надежности экспорта.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.1 - Исправлены отступы в handle_generate и handle_export_csv.]
# PREV_CHANGE_SUMMARY: [v1.0.0 - Первичное создание CLI интерфейса.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Инициализирует и настраивает парсер аргументов командной строки] => setup_argparser
# FUNC 10[Обрабатывает команду generate: генерация точек и сохранение в БД] => handle_generate
# FUNC 10[Обрабатывает команду export-csv: экспорт данных из БД в CSV] => handle_export_csv
# FUNC 10[Точка входа CLI: парсинг аргументов и делегирование командам] => main
# END_MODULE_MAP
#
# START_USE_CASES:
# -[setup_argparser]: Application (CLIStartup) -> SetupParser -> ParserReady
# -[handle_generate]: User (CLI) -> GeneratePoints -> PointsGenerated
# -[handle_export_csv]: User (CLI) -> ExportData -> DataExported
# -[main]: System (CLIEntry) -> ExecuteCommand -> CommandExecuted
# END_USE_CASES

import argparse
import logging
import sys
from pathlib import Path

# Импорт модулей приложения
from .config_manager import load_config
from .parabola_logic import generate_points
from .database_manager import init_database, save_points, load_points

# Настройка логирования
LOG_FILE = Path(__file__).parent.parent / "app_v7.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# START_FUNCTION_setup_argparser
# START_CONTRACT:
# PURPOSE: Настройка парсера аргументов командной строки.
# INPUTS: 
# - Нет
# OUTPUTS: 
# - argparse.ArgumentParser - Настроенный парсер аргументов
# SIDE_EFFECTS: Отсутствуют.
# KEYWORDS:[PATTERN(6): Builder; CONCEPT(7): ArgumentParsing]
# END_CONTRACT
def setup_argparser() -> argparse.ArgumentParser:
    """Настраивает и возвращает парсер аргументов командной строки."""
    
    # START_BLOCK_CREATE_PARSER: [Создание парсера и подкоманд]
    parser = argparse.ArgumentParser(
        description="CLI интерфейс для генерации точек параболы (Lesson v7)"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')
    
    # Команда generate
    generate_parser = subparsers.add_parser(
        'generate',
        help='Генерирует точки параболы и сохраняет их в БД'
    )
    
    # Команда export-csv
    export_parser = subparsers.add_parser(
        'export-csv',
        help='Экспортирует данные из БД в CSV файл'
    )
    export_parser.add_argument(
        '--out',
        type=str,
        required=True,
        help='Путь к выходному CSV файлу'
    )
    
    logger.debug(f"[CLI][IMP:4][setup_argparser][CREATE_PARSER][ParserSetup] Парсер аргументов настроен [INFO]")
    return parser
    # END_BLOCK_CREATE_PARSER
# END_FUNCTION_setup_argparser

# START_FUNCTION_handle_generate
# START_CONTRACT:
# PURPOSE: Обработка команды generate: генерация точек и сохранение в БД.
# INPUTS: 
# - Нет
# OUTPUTS: 
# - int - Код выхода (0 при успехе, 1 при ошибке)
# SIDE_EFFECTS: Читает config.json, генерирует точки, сохраняет в БД.
# KEYWORDS:[PATTERN(7): CommandHandler; CONCEPT(8): DataGeneration]
# END_CONTRACT
def handle_generate() -> int:
    """Обрабатывает команду generate."""
    
    # START_BLOCK_LOAD_CONFIG: [Загрузка конфигурации]
    logger.info(f"[CLI][IMP:7][handle_generate][LOAD_CONFIG][CommandStart] Выполнение команды 'generate' [INFO]")
    
    try:
        config = load_config()
        a = config['a']
        c = config['c']
        x_min = config['x_min']
        x_max = config['x_max']
        
        logger.info(f"[BeliefState][IMP:9][handle_generate][LOAD_CONFIG][ConfigLoaded] Параметры загружены: a={a}, c={c}, x_range=({x_min}, {x_max}) [VALUE]")
    except Exception as e:
        logger.error(f"[CLI][IMP:10][handle_generate][LOAD_CONFIG][ExceptionEnrichment] Ошибка загрузки конфигурации. Err: {e} [FATAL]")
        return 1
    # END_BLOCK_LOAD_CONFIG
    
    # START_BLOCK_GENERATE_POINTS: [Генерация точек]
    try:
        points = generate_points(a, c, x_min, x_max)
        logger.info(f"[BeliefState][IMP:9][handle_generate][GENERATE_POINTS][PointsGenerated] Сгенерировано {len(points)} точек [VALUE]")
    except Exception as e:
        logger.error(f"[CLI][IMP:10][handle_generate][GENERATE_POINTS][ExceptionEnrichment] Ошибка генерации точек. Err: {e} [FATAL]")
        return 1
    # END_BLOCK_GENERATE_POINTS
    
    # START_BLOCK_SAVE_TO_DB: [Сохранение в БД]
    try:
        # BUG_FIX_CONTEXT: Исправлен отступ. Ранее блок был вложен в except предыдущего блока, из-за чего сохранение не срабатывало при успехе.
        init_database()
        save_points(points)
        logger.info(f"[BeliefState][IMP:9][handle_generate][SAVE_TO_DB][DataSaved] Точки успешно сохранены в БД [SUCCESS]")
        print(f"[OK] Сгенерировано и сохранено {len(points)} точек в БД.")
        return 0
    except Exception as e:
        logger.error(f"[CLI][IMP:10][handle_generate][SAVE_TO_DB][ExceptionEnrichment] Ошибка сохранения в БД. Err: {e} [FATAL]")
        return 1
    # END_BLOCK_SAVE_TO_DB
# END_FUNCTION_handle_generate

# START_FUNCTION_handle_export_csv
# START_CONTRACT:
# PURPOSE: Обработка команды export-csv: экспорт данных из БД в CSV.
# INPUTS: 
# - Путь к выходному CSV файлу => output_path: str
# OUTPUTS: 
# - int - Код выхода (0 при успехе, 1 при ошибке)
# SIDE_EFFECTS: Читает данные из БД, сохраняет в CSV файл.
# KEYWORDS:[PATTERN(7): CommandHandler; CONCEPT(8): DataExport]
# END_CONTRACT
def handle_export_csv(output_path: str) -> int:
    """Обрабатывает команду export-csv."""
    
    # START_BLOCK_LOAD_FROM_DB: [Загрузка данных из БД]
    logger.info(f"[CLI][IMP:7][handle_export_csv][LOAD_FROM_DB][CommandStart] Выполнение команды 'export-csv' в {output_path} [INFO]")
    
    try:
        points = load_points()
        logger.info(f"[BeliefState][IMP:9][handle_export_csv][LOAD_FROM_DB][DataLoaded] Загружено {len(points)} точек из БД [VALUE]")
    except Exception as e:
        logger.error(f"[CLI][IMP:10][handle_export_csv][LOAD_FROM_DB][ExceptionEnrichment] Ошибка загрузки из БД. Err: {e} [FATAL]")
        return 1
    # END_BLOCK_LOAD_FROM_DB
    
    # START_BLOCK_SAVE_TO_CSV: [Сохранение в CSV]
    try:
        # BUG_FIX_CONTEXT: Исправлен отступ. Ранее блок был вложен в except предыдущего блока, из-за чего экспорт не срабатывал при успехе.
        import pandas as pd
        
        df = pd.DataFrame(points, columns=['x', 'y'])
        df.to_csv(output_path, index=False, encoding='utf-8')
        
        logger.info(f"[BeliefState][IMP:9][handle_export_csv][SAVE_TO_CSV][DataExported] Данные успешно экспортированы в {output_path} [SUCCESS]")
        print(f"[OK] Экспортировано {len(points)} точек в {output_path}.")
        return 0
        
    except ImportError:
        logger.error(f"[CLI][IMP:10][handle_export_csv][SAVE_TO_CSV][LibraryError] pandas не установлен. Невозможно экспортировать в CSV. [FATAL]")
        print("Ошибка: pandas не установлен. Установите pandas для экспорта в CSV.")
        return 1
    except Exception as e:
        logger.critical(f"[CLI][IMP:10][handle_export_csv][SAVE_TO_CSV][ExceptionEnrichment] Ошибка экспорта. Local vars: output_path={output_path}, points_count={len(points)}. Err: {e} [FATAL]")
        return 1
    # END_BLOCK_SAVE_TO_CSV
# END_FUNCTION_handle_export_csv

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE: Точка входа CLI: парсинг аргументов и делегирование командам.
# INPUTS: 
# - Аргументы командной строки => args: list (опционально, по умолчанию sys.argv[1:])
# OUTPUTS: 
# - int - Код выхода (0 при успехе, 1 при ошибке)
# SIDE_EFFECTS: Выполняет соответствующую команду и выводит результаты.
# KEYWORDS:[PATTERN(8): EntryPoint; CONCEPT(9): CommandDelegation]
# END_CONTRACT
def main(args: list = None) -> int:
    """Точка входа CLI интерфейса."""
    
    # START_BLOCK_PARSE_ARGS: [Парсинг аргументов]
    if args is None:
        args = sys.argv[1:]
    
    parser = setup_argparser()
    parsed_args = parser.parse_args(args)
    
    logger.debug(f"[CLI][IMP:4][main][PARSE_ARGS][ArgsParsed] Аргументы: {parsed_args} [INFO]")
    # END_BLOCK_PARSE_ARGS
    
    # START_BLOCK_DISPATCH_COMMAND: [Диспетчеризация команд]
    if parsed_args.command == 'generate':
        return handle_generate()
    elif parsed_args.command == 'export-csv':
        return handle_export_csv(parsed_args.out)
    else:
        parser.print_help()
        return 0
    # END_BLOCK_DISPATCH_COMMAND
# END_FUNCTION_main

if __name__ == '__main__':
    sys.exit(main())
