# FILE: lesson_v6/src/database_manager.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Управление базой данных SQLite для хранения точек параболы.
# SCOPE: Создание таблицы, сохранение и получение данных, очистка.
# INPUT: Путь к файлу БД (по умолчанию из __init__.py), данные точек.
# OUTPUT: Список точек из БД, статус операции.
# KEYWORDS:[DOMAIN(8): DataPersistence; CONCEPT(7): SQLite; TECH(9): SQL]
# LINKS:[WRITES_DATA_TO(8): parabola.db]
# END_MODULE_CONTRACT
#
# START_INVARIANTS:
# - Функция initialize_database ВСЕГДА создает таблицу points с правильной схемой.
# - Функция save_points ВСЕГДА перезаписывает таблицу points (DROP + CREATE).
# - Функция load_points ВСЕГДА возвращает список словарей с ключами 'x' и 'y'.
# END_INVARIANTS
#
# START_RATIONALE:
# Q: Почему используется DROP TABLE вместо DELETE FROM?
# A: Для учебного примера это упрощает схему и гарантирует чистоту данных при каждой генерации.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления БД с LDD 2.0 логированием.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Инициализирует БД и создает таблицу points] => initialize_database
# FUNC 10[Сохраняет точки в БД с перезаписью таблицы] => save_points
# FUNC 10[Загружает все точки из БД] => load_points
# END_MODULE_MAP
#
# START_USE_CASES:
# -[initialize_database]: System (Startup) -> SetupDatabase -> DatabaseReady
# -[save_points]: Logic (Calculation) -> PersistPoints -> DataStored
# -[load_points]: UI (Visualization) -> RetrieveData -> DataRetrieved
# END_USE_CASES

import sqlite3
import logging
from typing import List, Dict, Any

# Настройка логирования
logger = logging.getLogger(__name__)

# START_FUNCTION_initialize_database
# START_CONTRACT:
# PURPOSE: Инициализация базы данных и создание таблицы points.
# INPUTS: 
# - [Путь к файлу БД] => db_path: str
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Создает файл БД и таблицу points.
# KEYWORDS:[PATTERN(6): Repository; CONCEPT(8): SchemaMigration]
# END_CONTRACT
def initialize_database(db_path: str) -> None:
    """Инициализирует базу данных и создает таблицу points."""
    
    # START_BLOCK_CONNECT_AND_CREATE: [Подключение к БД и создание таблицы]
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                x REAL NOT NULL,
                y REAL NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info(f"[BeliefState][IMP:9][initialize_database][CONNECT_AND_CREATE][ReturnData] База данных инициализирована: {db_path} [VALUE]")
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][initialize_database][CONNECT_AND_CREATE][ExceptionEnrichment] Ошибка инициализации БД. Local vars: db_path={db_path}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_CONNECT_AND_CREATE
# END_FUNCTION_initialize_database

# START_FUNCTION_save_points
# START_CONTRACT:
# PURPOSE: Сохранение точек параболы в базу данных.
# INPUTS: 
# - [Список точек] => points: List[Dict[str, float]]
# - [Путь к файлу БД] => db_path: str
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Перезаписывает таблицу points новыми данными.
# KEYWORDS:[PATTERN(6): BulkInsert; CONCEPT(8): Transaction]
# END_CONTRACT
def save_points(points: List[Dict[str, float]], db_path: str) -> None:
    """Сохраняет точки параболы в базу данных (перезапись таблицы)."""
    
    # START_BLOCK_VALIDATE_INPUT: [Валидация входных данных]
    if not points:
        logger.warning(f"[ValidationError][IMP:5][save_points][VALIDATE_INPUT][ConditionCheck] Список точек пуст. Операция отменена. [WARN]")
        return
    # END_BLOCK_VALIDATE_INPUT

    # START_BLOCK_TRUNCATE_AND_INSERT: [Очистка таблицы и вставка новых данных]
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Удаляем старые данные
        cursor.execute('DROP TABLE IF EXISTS points')
        
        # Создаем новую таблицу
        cursor.execute('''
            CREATE TABLE points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                x REAL NOT NULL,
                y REAL NOT NULL
            )
        ''')
        
        # Вставляем новые данные
        cursor.executemany('INSERT INTO points (x, y) VALUES (?, ?)', 
                          [(p['x'], p['y']) for p in points])
        
        conn.commit()
        conn.close()
        
        logger.info(f"[BeliefState][IMP:9][save_points][TRUNCATE_AND_INSERT][ReturnData] Сохранено {len(points)} точек в БД. [VALUE]")
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][save_points][TRUNCATE_AND_INSERT][ExceptionEnrichment] Ошибка сохранения точек. Local vars: db_path={db_path}, points_count={len(points)}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_TRUNCATE_AND_INSERT
# END_FUNCTION_save_points

# START_FUNCTION_load_points
# START_CONTRACT:
# PURPOSE: Загрузка всех точек из базы данных.
# INPUTS: 
# - [Путь к файлу БД] => db_path: str
# OUTPUTS: 
# - List[Dict[str, float]] - Список точек [{'x': float, 'y': float}, ...]
# SIDE_EFFECTS: Отсутствуют.
# KEYWORDS:[PATTERN(6): Query; CONCEPT(8): ResultMapping]
# END_CONTRACT
def load_points(db_path: str) -> List[Dict[str, float]]:
    """Загружает все точки параболы из базы данных."""
    
    # START_BLOCK_QUERY_DATABASE: [Запрос данных из БД]
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT x, y FROM points ORDER BY x')
        rows = cursor.fetchall()
        
        conn.close()
        
        points = [{'x': row[0], 'y': row[1]} for row in rows]
        
        logger.info(f"[BeliefState][IMP:9][load_points][QUERY_DATABASE][ReturnData] Загружено {len(points)} точек из БД. [VALUE]")
        return points
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][load_points][QUERY_DATABASE][ExceptionEnrichment] Ошибка загрузки точек. Local vars: db_path={db_path}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_QUERY_DATABASE
# END_FUNCTION_load_points
