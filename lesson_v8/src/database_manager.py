# FILE: lesson_v8/src/database_manager.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Управление SQLite базой данных для хранения точек параболы.
# SCOPE: Создание таблиц, сохранение, чтение и очистка данных точек параболы.
# INPUT: DataFrame с точками для сохранения (опционально).
# OUTPUT: DataFrame с точками из БД (при чтении), None (при записи/очистке).
# KEYWORDS:[DOMAIN(8): DataPersistence; CONCEPT(7): SQLite; TECH(9): Database]
# LINKS:[WRITES_DATA_TO(8): parabola_points.db; READS_DATA_FROM(8): parabola_points.db]
# END_MODULE_CONTRACT
#
# START_INVARIANTS:
# - Функция init_database ВСЕГДА создает таблицу points, если она не существует.
# - Функция save_points ПЕРЕЗАПИСЫВАЕТ все данные в таблице points (не добавляет).
# - Функция load_points ВСЕГДА возвращает pandas DataFrame (пустой, если данных нет).
# END_INVARIANTS
#
# START_RATIONALE:
# Q: Почему используется SQLite вместо других СУБД?
# A: SQLite — встроенная база данных, не требующая отдельного сервера, идеально подходит для локальных приложений.
# Q: Почему save_points перезаписывает данные вместо добавления?
# A: Это соответствует бизнес-логике приложения: каждая генерация создает новый набор точек параболы.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления базой данных.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Инициализирует базу данных и создает таблицу] => init_database
# FUNC 10[Очищает таблицу точек] => clear_points
# FUNC 10[Сохраняет DataFrame в базу данных] => save_points
# FUNC 10[Загружает точки из базы данных в DataFrame] => load_points
# END_MODULE_MAP
#
# START_USE_CASES:
# -[init_database]: Application (Startup) -> InitializeDatabase -> DatabaseReady
# -[save_points]: Application (DataGeneration) -> SavePointsToDB -> PointsPersisted
# -[load_points]: Application (DataDisplay) -> LoadPointsFromDB -> DataFrameLoaded
# -[clear_points]: Application (DataCleanup) -> ClearDatabase -> DatabaseCleared
# END_USE_CASES

import logging
import os
import sqlite3
import pandas as pd
from typing import Optional

logger = logging.getLogger(__name__)

# Путь к файлу базы данных относительно директории урока
DB_FILE = os.path.join(os.path.dirname(__file__), "..", "parabola_points.db")

# Имя таблицы для хранения точек
TABLE_NAME = "points"


# START_FUNCTION_init_database
# START_CONTRACT:
# PURPOSE: Инициализирует базу данных SQLite и создает таблицу points, если она не существует.
# INPUTS: 
# - db_path => db_path: str (путь к файлу базы данных, опционально)
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Создает файл базы данных и таблицу points с колонками x и y.
# KEYWORDS:[PATTERN(7): LazyInitialization; CONCEPT(6): TableCreation]
# COMPLEXITY_SCORE: 3[Низкая сложность: выполнение SQL запроса CREATE TABLE.]
# END_CONTRACT
def init_database(db_path: str = DB_FILE) -> None:
    """
    Функция выполняет инициализацию базы данных SQLite для хранения точек параболы.
    Создает файл базы данных, если он не существует, и таблицу points с колонками x и y.
    Таблица создается только один раз, что обеспечивается конструкцией IF NOT EXISTS.
    Это позволяет безопасно вызывать функцию многократно без риска потери данных.
    """
    
    # START_BLOCK_CONNECT_AND_CREATE_TABLE: [Подключение к БД и создание таблицы]
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                x REAL NOT NULL,
                y REAL NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        
        logger.info(f"[DatabaseInitialized][IMP:8][init_database][CONNECT_AND_CREATE_TABLE][DBOperation] База данных инициализирована: {db_path}, таблица: {TABLE_NAME} [SUCCESS]")
        
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][init_database][CONNECT_AND_CREATE_TABLE][ExceptionEnrichment] Ошибка инициализации БД. Local vars: db_path={db_path}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_CONNECT_AND_CREATE_TABLE
# END_FUNCTION_init_database


# START_FUNCTION_clear_points
# START_CONTRACT:
# PURPOSE: Очищает таблицу points от всех записей.
# INPUTS: 
# - db_path => db_path: str (путь к файлу базы данных, опционально)
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Удаляет все записи из таблицы points.
# KEYWORDS:[PATTERN(6): DataCleanup; CONCEPT(5): TableTruncate]
# COMPLEXITY_SCORE: 2[Низкая сложность: выполнение SQL запроса DELETE.]
# END_CONTRACT
def clear_points(db_path: str = DB_FILE) -> None:
    """
    Функция выполняет очистку таблицы points от всех записей.
    Это необходимо перед сохранением нового набора точек параболы.
    Операция является атомарной и удаляет все строки из таблицы.
    """
    
    # START_BLOCK_DELETE_ALL_RECORDS: [Удаление всех записей из таблицы]
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"DELETE FROM {TABLE_NAME}")
        
        conn.commit()
        deleted_rows = cursor.rowcount
        conn.close()
        
        logger.info(f"[PointsCleared][IMP:8][clear_points][DELETE_ALL_RECORDS][DBOperation] Удалено {deleted_rows} записей из таблицы {TABLE_NAME} [SUCCESS]")
        
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][clear_points][DELETE_ALL_RECORDS][ExceptionEnrichment] Ошибка очистки БД. Local vars: db_path={db_path}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_DELETE_ALL_RECORDS
# END_FUNCTION_clear_points


# START_FUNCTION_save_points
# START_CONTRACT:
# PURPOSE: Сохраняет DataFrame с точками параболы в базу данных SQLite.
# INPUTS: 
# - df => df: pd.DataFrame (DataFrame с колонками x и y)
# - db_path => db_path: str (путь к файлу базы данных, опционально)
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Перезаписывает все данные в таблице points новыми точками из DataFrame.
# KEYWORDS:[PATTERN(8): DataPersistence; CONCEPT(7): DataFrameToSQL]
# COMPLEXITY_SCORE: 4[Низкая сложность: очистка таблицы и вставка данных из DataFrame.]
# END_CONTRACT
def save_points(df: pd.DataFrame, db_path: str = DB_FILE) -> None:
    """
    Функция выполняет сохранение точек параболы из pandas DataFrame в базу данных SQLite.
    Перед сохранением таблица очищается от старых данных, что обеспечивает соответствие
    бизнес-логике приложения (каждая генерация создает новый набор точек).
    DataFrame должен содержать колонки 'x' и 'y' с числовыми значениями.
    """
    
    # START_BLOCK_VALIDATE_INPUT: [Проверка входного DataFrame]
    if not isinstance(df, pd.DataFrame):
        logger.error(f"[InvalidInput][IMP:9][save_points][VALIDATE_INPUT][TypeError] df должен быть pandas DataFrame. Получен тип: {type(df)} [ERROR]")
        raise TypeError("df должен быть pandas DataFrame")
    
    if 'x' not in df.columns or 'y' not in df.columns:
        logger.error(f"[InvalidInput][IMP:9][save_points][VALIDATE_INPUT][ValueError] DataFrame должен содержать колонки 'x' и 'y'. Колонки: {list(df.columns)} [ERROR]")
        raise ValueError("DataFrame должен содержать колонки 'x' и 'y'")
    
    if len(df) == 0:
        logger.warning(f"[EmptyDataFrame][IMP:7][save_points][VALIDATE_INPUT][DataCheck] DataFrame пустой, сохранение пропущено [WARN]")
        return
    # END_BLOCK_VALIDATE_INPUT
    
    # START_BLOCK_SAVE_TO_DATABASE: [Очистка и сохранение данных]
    try:
        # Сначала очищаем таблицу
        clear_points(db_path)
        
        # Сохраняем новые данные
        conn = sqlite3.connect(db_path)
        
        df.to_sql(TABLE_NAME, conn, if_exists='append', index=False)
        
        conn.close()
        
        logger.info(f"[PointsSaved][IMP:8][save_points][SAVE_TO_DATABASE][DBOperation] Сохранено {len(df)} точек в таблицу {TABLE_NAME} [SUCCESS]")
        
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][save_points][SAVE_TO_DATABASE][ExceptionEnrichment] Ошибка сохранения точек. Local vars: db_path={db_path}, df_shape={df.shape}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_SAVE_TO_DATABASE
# END_FUNCTION_save_points


# START_FUNCTION_load_points
# START_CONTRACT:
# PURPOSE: Загружает точки параболы из базы данных SQLite в pandas DataFrame.
# INPUTS: 
# - db_path => db_path: str (путь к файлу базы данных, опционально)
# OUTPUTS: 
# - pd.DataFrame - DataFrame с колонками x и y, содержащий точки из БД
# SIDE_EFFECTS: Отсутствуют (чистая функция чтения).
# KEYWORDS:[PATTERN(7): DataRetrieval; CONCEPT(6): SQLToDataFrame]
# COMPLEXITY_SCORE: 3[Низкая сложность: выполнение SQL запроса SELECT и создание DataFrame.]
# END_CONTRACT
def load_points(db_path: str = DB_FILE) -> pd.DataFrame:
    """
    Функция выполняет загрузку точек параболы из базы данных SQLite в pandas DataFrame.
    Считывает все записи из таблицы points и возвращает их в виде DataFrame с колонками x и y.
    Если таблица пуста или база данных не содержит данных, возвращается пустой DataFrame.
    """
    
    # START_BLOCK_LOAD_FROM_DATABASE: [Чтение данных из БД]
    try:
        conn = sqlite3.connect(db_path)
        
        df = pd.read_sql_query(f"SELECT x, y FROM {TABLE_NAME} ORDER BY id", conn)
        
        conn.close()
        
        logger.info(f"[PointsLoaded][IMP:8][load_points][LOAD_FROM_DATABASE][DBOperation] Загружено {len(df)} точек из таблицы {TABLE_NAME} [SUCCESS]")
        
        return df
        
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][load_points][LOAD_FROM_DATABASE][ExceptionEnrichment] Ошибка загрузки точек. Local vars: db_path={db_path}. Err: {e} [FATAL]")
        raise
    # END_BLOCK_LOAD_FROM_DATABASE
# END_FUNCTION_load_points
