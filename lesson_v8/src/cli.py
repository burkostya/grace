# FILE: lesson_v8/src/cli.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: CLI интерфейс для автономного управления приложением генерации параболы.
# SCOPE: Обеспечение командной строки для генерации точек и экспорта данных в CSV.
# INPUT: Аргументы командной строки (через argparse).
# OUTPUT: Сообщения в stdout/stderr, файлы CSV (при экспорте), коды возврата.
# KEYWORDS:[DOMAIN(8): CommandLineInterface; CONCEPT(7): AgenticUX; TECH(9): Argparse]
# LINKS:[USES_API(8): config_manager, parabola_logic, database_manager]
# END_MODULE_CONTRACT
#
# START_INVARIANTS:
# - Команда generate ВСЕГДА читает параметры из config.json.
# - Команда export-csv ВСЕГДА экспортирует текущие данные из БД.
# - При успешном выполнении команды возвращается exit code 0.
# END_INVARIANTS
#
# START_RATIONALE:
# Q: Почему используется argparse вместо других библиотек CLI?
# A: argparse — стандартная библиотека Python, обеспечивает надежный парсинг аргументов и автоматическую генерацию справки.
# Q: Почему команды не требуют ввода параметров через терминал?
# A: Это соответствует концепции Agentic UX: параметры хранятся в config.json, что упрощает автоматизацию.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание CLI интерфейса.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Обрабатывает команду generate] => cmd_generate
# FUNC 10[Обрабатывает команду export-csv] => cmd_export_csv
# FUNC 10[Главная точка входа CLI] => main
# END_MODULE_MAP
#
# START_USE_CASES:
# -[cmd_generate]: User (CLI) -> ExecuteGenerateCommand -> PointsGeneratedInDB
# -[cmd_export_csv]: User (CLI) -> ExecuteExportCSVCommand -> CSVFileCreated
# -[main]: System (Startup) -> ParseCLIArguments -> CommandExecuted
# END_USE_CASES

import argparse
import logging
import os
import sys

# Настройка логирования в файл
LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "app_v8.log")
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Импорт модулей приложения
from .config_manager import load_config, save_config
from .parabola_logic import generate_parabola_points
from .database_manager import init_database, save_points, load_points


# START_FUNCTION_cmd_generate
# START_CONTRACT:
# PURPOSE: Выполняет генерацию точек параболы на основе параметров из config.json и сохраняет их в БД.
# INPUTS: 
# - args => args: argparse.Namespace (аргументы командной строки, не используются)
# OUTPUTS: 
# - int - Код возврата (0 при успехе, 1 при ошибке)
# SIDE_EFFECTS: Читает config.json, генерирует точки, сохраняет в БД SQLite.
# KEYWORDS:[PATTERN(8): CommandPattern; CONCEPT(7): DataGeneration]
# COMPLEXITY_SCORE: 5[Средняя сложность: чтение конфига, генерация, сохранение в БД.]
# END_CONTRACT
def cmd_generate(args: argparse.Namespace) -> int:
    """
    Функция выполняет генерацию точек параболы на основе параметров, загруженных из config.json.
    Считывает коэффициенты a, c и диапазон x_min, x_max из конфигурационного файла,
    генерирует точки параболы по формуле y = ax^2 + c и сохраняет их в базу данных SQLite.
    Функция обеспечивает полный цикл генерации данных без необходимости ввода параметров через терминал.
    """
    
    # START_BLOCK_LOAD_CONFIG: [Загрузка конфигурации]
    try:
        config = load_config()
        a = config['a']
        c = config['c']
        x_min = config['x_min']
        x_max = config['x_max']
        
        logger.info(f"[ConfigLoaded][IMP:8][cmd_generate][LOAD_CONFIG][DataLoad] Параметры загружены: a={a}, c={c}, x_min={x_min}, x_max={x_max} [SUCCESS]")
        print(f"Параметры загружены из config.json: a={a}, c={c}, x_min={x_min}, x_max={x_max}")
        
    except Exception as e:
        logger.critical(f"[ConfigError][IMP:10][cmd_generate][LOAD_CONFIG][ExceptionEnrichment] Ошибка загрузки конфигурации. Err: {e} [FATAL]")
        print(f"Ошибка загрузки конфигурации: {e}", file=sys.stderr)
        return 1
    # END_BLOCK_LOAD_CONFIG
    
    # START_BLOCK_GENERATE_POINTS: [Генерация точек параболы]
    try:
        df = generate_parabola_points(a, c, x_min, x_max)
        logger.info(f"[PointsGenerated][IMP:9][cmd_generate][GENERATE_POINTS][Calculation] Сгенерировано {len(df)} точек [SUCCESS]")
        print(f"Сгенерировано {len(df)} точек параболы")
        
    except Exception as e:
        logger.critical(f"[GenerationError][IMP:10][cmd_generate][GENERATE_POINTS][ExceptionEnrichment] Ошибка генерации точек. Err: {e} [FATAL]")
        print(f"Ошибка генерации точек: {e}", file=sys.stderr)
        return 1
    # END_BLOCK_GENERATE_POINTS
    
    # START_BLOCK_SAVE_TO_DATABASE: [Сохранение в БД]
    try:
        init_database()
        save_points(df)
        logger.info(f"[PointsSaved][IMP:9][cmd_generate][SAVE_TO_DATABASE][DBOperation] Точки успешно сохранены в БД [SUCCESS]")
        print("Точки успешно сохранены в базу данных")
        
    except Exception as e:
        logger.critical(f"[DatabaseError][IMP:10][cmd_generate][SAVE_TO_DATABASE][ExceptionEnrichment] Ошибка сохранения в БД. Err: {e} [FATAL]")
        print(f"Ошибка сохранения в базу данных: {e}", file=sys.stderr)
        return 1
    # END_BLOCK_SAVE_TO_DATABASE
    
    return 0
# END_FUNCTION_cmd_generate


# START_FUNCTION_cmd_export_csv
# START_CONTRACT:
# PURPOSE: Экспортирует текущие данные из БД SQLite в указанный CSV файл.
# INPUTS: 
# - args => args: argparse.Namespace (аргументы командной строки, содержит поле out)
# OUTPUTS: 
# - int - Код возврата (0 при успехе, 1 при ошибке)
# SIDE_EFFECTS: Создает CSV файл с данными из БД.
# KEYWORDS:[PATTERN(8): CommandPattern; CONCEPT(7): DataExport]
# COMPLEXITY_SCORE: 4[Низкая сложность: чтение из БД, сохранение в CSV.]
# END_CONTRACT
def cmd_export_csv(args: argparse.Namespace) -> int:
    """
    Функция выполняет экспорт данных точек параболы из базы данных SQLite в CSV файл.
    Считывает текущие данные из таблицы points и сохраняет их в указанный пользователем файл.
    Если база данных пуста, создается пустой CSV файл с заголовками колонок.
    Функция обеспечивает возможность экспорта данных для дальнейшего анализа или использования.
    """
    
    # START_BLOCK_VALIDATE_OUTPUT_PATH: [Проверка пути к выходному файлу]
    output_file = args.out
    if not output_file:
        logger.error(f"[InvalidInput][IMP:9][cmd_export_csv][VALIDATE_OUTPUT_PATH][ValueError] Не указан выходной файл (--out) [ERROR]")
        print("Ошибка: не указан выходной файл (--out)", file=sys.stderr)
        return 1
    # END_BLOCK_VALIDATE_OUTPUT_PATH
    
    # START_BLOCK_LOAD_FROM_DATABASE: [Загрузка данных из БД]
    try:
        df = load_points()
        logger.info(f"[PointsLoaded][IMP:8][cmd_export_csv][LOAD_FROM_DATABASE][DBOperation] Загружено {len(df)} точек из БД [SUCCESS]")
        
    except Exception as e:
        logger.critical(f"[DatabaseError][IMP:10][cmd_export_csv][LOAD_FROM_DATABASE][ExceptionEnrichment] Ошибка загрузки из БД. Err: {e} [FATAL]")
        print(f"Ошибка загрузки из базы данных: {e}", file=sys.stderr)
        return 1
    # END_BLOCK_LOAD_FROM_DATABASE
    
    # START_BLOCK_SAVE_TO_CSV: [Сохранение в CSV файл]
    try:
        df.to_csv(output_file, index=False, encoding='utf-8')
        logger.info(f"[CSVExported][IMP:9][cmd_export_csv][SAVE_TO_CSV][FileOperation] Данные экспортированы в {output_file} ({len(df)} строк) [SUCCESS]")
        print(f"Данные экспортированы в {output_file} ({len(df)} строк)")
        
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][cmd_export_csv][SAVE_TO_CSV][ExceptionEnrichment] Ошибка сохранения CSV. Local vars: output_file={output_file}. Err: {e} [FATAL]")
        print(f"Ошибка сохранения CSV файла: {e}", file=sys.stderr)
        return 1
    # END_BLOCK_SAVE_TO_CSV
    
    return 0
# END_FUNCTION_cmd_export_csv


# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE: Главная точка входа CLI интерфейса. Парсит аргументы и делегирует выполнение команд.
# INPUTS: 
# - argv => argv: list (список аргументов командной строки, опционально)
# OUTPUTS: 
# - int - Код возврата (0 при успехе, 1 при ошибке)
# SIDE_EFFECTS: Парсит аргументы командной строки, выполняет соответствующие команды.
# KEYWORDS:[PATTERN(9): MainEntryPoint; CONCEPT(8): CommandDispatcher]
# COMPLEXITY_SCORE: 3[Низкая сложность: парсинг аргументов и делегирование.]
# END_CONTRACT
def main(argv: list = None) -> int:
    """
    Функция является главной точкой входа для CLI интерфейса приложения.
    Парсит аргументы командной строки и делегирует выполнение соответствующим командам.
    Поддерживает две основные команды: generate (генерация точек) и export-csv (экспорт в CSV).
    При отсутствии аргументов выводит справку по использованию.
    """
    
    # START_BLOCK_SETUP_PARSER: [Настройка парсера аргументов]
    parser = argparse.ArgumentParser(
        description='CLI интерфейс для генерации точек параболы',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')
    
    # Команда generate
    parser_generate = subparsers.add_parser(
        'generate',
        help='Генерация точек параболы на основе параметров из config.json'
    )
    
    # Команда export-csv
    parser_export = subparsers.add_parser(
        'export-csv',
        help='Экспорт данных из БД в CSV файл'
    )
    parser_export.add_argument(
        '--out',
        required=True,
        help='Путь к выходному CSV файлу'
    )
    # END_BLOCK_SETUP_PARSER
    
    # START_BLOCK_PARSE_AND_EXECUTE: [Парсинг и выполнение команды]
    args = parser.parse_args(argv)
    
    if args.command is None:
        parser.print_help()
        return 0
    
    logger.info(f"[CommandStarted][IMP:8][main][PARSE_AND_EXECUTE][CommandExecution] Выполняется команда: {args.command} [INFO]")
    
    if args.command == 'generate':
        return cmd_generate(args)
    elif args.command == 'export-csv':
        return cmd_export_csv(args)
    else:
        logger.error(f"[UnknownCommand][IMP:9][main][PARSE_AND_EXECUTE][CommandError] Неизвестная команда: {args.command} [ERROR]")
        print(f"Неизвестная команда: {args.command}", file=sys.stderr)
        return 1
    # END_BLOCK_PARSE_AND_EXECUTE
# END_FUNCTION_main


if __name__ == '__main__':
    sys.exit(main())
