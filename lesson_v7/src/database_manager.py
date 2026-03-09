# FILE: lesson_v7/src/database_manager.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Управление базой данных SQLite для хранения точек параболы.
# SCOPE: Создание таблиц, сохранение и чтение точек, очистка данных.
# INPUT: Путь к файлу базы данных (по умолчанию lesson_v7/points.db).
# OUTPUT: Данные точек из БД (список кортежей или DataFrame).
# KEYWORDS:[DOMAIN(8): DataAccess; CONCEPT(7): Persistence; TECH(9): SQLite]
# LINKS:[READS_DATA_FROM(8): parabola_logic; WRITES_DATA_TO(10): points.db]
# END_MODULE_CONTRACT
#
# START_INVARIANTS:
# - Функция init_database ВСЕГДА создает таблицу points, если она не существует.
# - Функция save_points ПЕРЕЗАПИСЫВАЕТ все данные в таблице (сначала очищает, затем вставляет).
# - Функция load_points ВСЕГДА возвращает список кортежей [(x, y), ...], даже если таблица пуста (пустой список).
# END_INVARIANTS
#
# START_RATIONALE:
# Q: Почему используется SQLite вместо других БД?
# A: SQLite встроена в Python, не требует отдельного сервера и идеально подходит для локальных учебных приложений.
# Q: Почему save_points очищает таблицу перед вставкой?
# A: Это обеспечивает согласованность данных - в БД хранится только последний сгенерированный набор точек.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления базой данных.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Инициализирует базу данных и создает таблицу points] => init_database
# FUNC 10[Сохраняет точки в базу данных (перезаписывает старые данные)] => save_points
# FUNC 10[Загружает точки из базы данных] => load_points
# END_MODULE_MAP
#
# START_USE_CASES:
# -[init_database]: Application (Startup) -> SetupDatabase -> DatabaseReady
# -[save_points]: Application (GenerateCommand) -> PersistPoints -> DataSaved
# -[load_points]: Application (DrawCommand) -> RetrievePoints -> DataLoaded
# END_USE_CASES

import logging
import sqlite3
from pathlib import Path
from typing import List, Tuple

logger = logging.getLogger(__name__)

# Константы для путей и SQL
DEFAULT_DB_PATH = Path(__file__).parent.parent / "points.db"
TABLE_NAME = "points"
CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    x REAL NOT NULL,
    y REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""
DELETE_ALL_SQL = f"DELETE FROM {TABLE_NAME}"
INSERT_POINT_SQL = f"INSERT INTO {TABLE_NAME} (x, y) VALUES (?, ?)"
SELECT_POINTS_SQL = f"SELECT x, y FROM {TABLE_NAME} ORDER BY x"

# START_FUNCTION_init_database
# START_CONTRACT:
# PURPOSE: Инициализация базы данных и создание таблицы points.
# INPUTS: 
# - Путь к файлу базы данных => db_path: Path (опционально, по умолчанию DEFAULT_DB_PATH)
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Создает файл базы данных и таблицу points, если они не существуют.
# KEYWORDS:[PATTERN(6): Initialization; CONCEPT(8): SchemaCreation]
# END_CONTRACT
def init_database(db_path: Path = DEFAULT_DB_PATH) -> None:
    """Инициализирует базу данных и создает таблицу points."""
    
    # START_BLOCK_CONNECT_DB: [Подключение к базе данных]
    logger.info(f"[DBInit][IMP:7][init_database][CONNECT_DB][DBConnect] Инициализация базы данных: {db_path} [INFO]")
    
    try:
        # Создаем родительскую директорию, если она не существует
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(CREATE_TABLE_SQL)
            conn.commit()
            
            logger.info(f"[DBInit][IMP:7][init_database][CONNECT_DB][TableCreated] Таблица {TABLE_NAME} успешно создана или уже существует. [SUCCESS]")
            
    except sqlite3.Error as e:
        logger.critical(f"[DBInit][IMP:10][init_database][CONNECT_DB][ExceptionEnrichment] Ошибка SQLite. Local vars: db_path={db_path}. Err: {e} [FATAL]")
        raise
    except Exception as e:
        logger.critical(f"[DBInit][IMP:10][init_database][CONNECT_DB][ExceptionEnrichment] Неожиданная ошибка. Local vars: db_path={db_path}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_CONNECT_DB
# END_FUNCTION_init_database

# START_FUNCTION_save_points
# START_CONTRACT:
# PURPOSE: Сохранение точек в базу данных (перезапись старых данных).
# INPUTS: 
# - Список точек => points: List[Tuple[float, float]]
# - Путь к файлу базы данных => db_path: Path (опционально)
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Очищает таблицу points и вставляет новые данные.
# KEYWORDS:[PATTERN(7): Transaction; CONCEPT(9): DataPersistence]
# END_CONTRACT
def save_points(points: List[Tuple[float, float]], db_path: Path = DEFAULT_DB_PATH) -> None:
    """Сохраняет точки в базу данных, перезаписывая старые данные."""
    
    # START_BLOCK_VALIDATE_INPUT: [Валидация входных данных]
    logger.debug(f"[DBSave][IMP:4][save_points][VALIDATE_INPUT][Params] Сохранение {len(points)} точек в БД [INFO]")
    
    if not isinstance(points, list):
        logger.error(f"[DBSave][IMP:10][save_points][VALIDATE_INPUT][ValidationError] Точки должны быть списком. Local vars: points={points} [FATAL]")
        raise TypeError("Точки должны быть списком кортежей (x, y).")
    
    for point in points:
        if not isinstance(point, tuple) or len(point) != 2:
            logger.error(f"[DBSave][IMP:10][save_points][VALIDATE_INPUT][ValidationError] Неверный формат точки. Local vars: point={point} [FATAL]")
            raise ValueError("Каждая точка должна быть кортежем (x, y).")
    # END_BLOCK_VALIDATE_INPUT
    
    # START_BLOCK_TRANSACTION: [Транзакция: очистка и вставка данных]
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Очистка старых данных
            cursor.execute(DELETE_ALL_SQL)
            logger.debug(f"[DBSave][IMP:5][save_points][TRANSACTION][DataClear] Старые данные очищены [INFO]")
            
            # Вставка новых данных
            if points:
                cursor.executemany(INSERT_POINT_SQL, points)
                conn.commit()
                logger.info(f"[BeliefState][IMP:9][save_points][TRANSACTION][DataSaved] Успешно сохранено {len(points)} точек в {TABLE_NAME}. [VALUE]")
            else:
                conn.commit()
                logger.warning(f"[DBSave][IMP:8][save_points][TRANSACTION][EmptyData] Список точек пуст. База очищена. [WARN]")
            
    except sqlite3.Error as e:
        logger.critical(f"[DBSave][IMP:10][save_points][TRANSACTION][ExceptionEnrichment] Ошибка SQLite. Local vars: db_path={db_path}, points_count={len(points)}. Err: {e} [FATAL]")
        raise
    except Exception as e:
        logger.critical(f"[DBSave][IMP:10][save_points][TRANSACTION][ExceptionEnrichment] Неожиданная ошибка. Local vars: db_path={db_path}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_TRANSACTION
# END_FUNCTION_save_points

# START_FUNCTION_load_points
# START_CONTRACT:
# PURPOSE: Загрузка точек из базы данных.
# INPUTS: 
# - Путь к файлу базы данных => db_path: Path (опционально)
# OUTPUTS: 
# - List[Tuple[float, float]] - Список точек [(x, y), ...]
# SIDE_EFFECTS: Отсутствуют.
# KEYWORDS:[PATTERN(6): Query; CONCEPT(8): DataRetrieval]
# END_CONTRACT
def load_points(db_path: Path = DEFAULT_DB_PATH) -> List[Tuple[float, float]]:
    """Загружает точки из базы данных."""
    
    # START_BLOCK_QUERY_DB: [Запрос данных из БД]
    logger.debug(f"[DBLoad][IMP:4][load_points][QUERY_DB][DBConnect] Загрузка точек из {db_path} [INFO]")
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(SELECT_POINTS_SQL)
            points = cursor.fetchall()
            
            logger.info(f"[BeliefState][IMP:9][load_points][QUERY_DB][DataLoaded] Загружено {len(points)} точек из {TABLE_NAME}. [VALUE]")
            return points
            
    except sqlite3.Error as e:
        logger.critical(f"[DBLoad][IMP:10][load_points][QUERY_DB][ExceptionEnrichment] Ошибка SQLite. Local vars: db_path={db_path}. Err: {e} [FATAL]")
        raise
    except Exception as e:
        logger.critical(f"[DBLoad][IMP:10][load_points][QUERY_DB][ExceptionEnrichment] Неожиданная ошибка. Local vars: db_path={db_path}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_QUERY_DB
# END_FUNCTION_load_points
