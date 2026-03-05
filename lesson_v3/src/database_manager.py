# FILE:lesson_v3/src/database_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление базой данных SQLite для хранения точек параболы.
# SCOPE:Создание таблиц, очистка, запись и чтение данных.
# INPUT:Путь к файлу БД, список кортежей (x, y).
# OUTPUT:DataFrame или список точек.
# KEYWORDS:[DOMAIN(8):Database; CONCEPT(7):SQLite_Storage; TECH(9):Python_sqlite3]
# LINKS:[READS_DATA_FROM(9):lesson_v3/parabola.db]
# END_MODULE_CONTRACT

# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления БД.]
# END_CHANGE_SUMMARY

# START_MODULE_MAP:
# FUNC 10[Инициализирует БД и создает таблицу] => init_db
# FUNC 10[Сохраняет список точек в БД] => save_points
# FUNC 10[Загружает все точки из БД] => load_points
# END_MODULE_MAP

import sqlite3
import logging
import os
import pandas as pd

logger = logging.getLogger(__name__)

# START_FUNCTION_init_db
# START_CONTRACT:
# PURPOSE:Создание таблицы points, если она не существует.
# INPUTS: 
# - str =>db_path: Путь к файлу БД
# OUTPUTS: 
# - bool -Успешность инициализации
# SIDE_EFFECTS: Создает файл БД и таблицу.
# END_CONTRACT
def init_db(db_path: str) -> bool:
    """Инициализирует базу данных."""
    # START_BLOCK_CREATE_TABLE: [Создание таблицы]
    try:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS points (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    x REAL NOT NULL,
                    y REAL NOT NULL
                )
            """)
            conn.commit()
        logger.info(f"[DB][IMP:8][init_db][CREATE_TABLE][Success] БД {db_path} инициализирована. [ACTION]")
        return True
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][init_db][CREATE_TABLE][Exception] Ошибка инициализации БД: {e} [FATAL]")
        return False
    # END_BLOCK_CREATE_TABLE
# END_FUNCTION_init_db

# START_FUNCTION_save_points
# START_CONTRACT:
# PURPOSE:Очистка старых данных и сохранение новых точек.
# INPUTS: 
# - str =>db_path: Путь к файлу БД
# - list =>points: Список кортежей (x, y)
# OUTPUTS: 
# - bool -Успешность сохранения
# SIDE_EFFECTS: Удаляет все записи из таблицы points.
# END_CONTRACT
def save_points(db_path: str, points: list) -> bool:
    """Сохраняет точки в БД."""
    # START_BLOCK_INSERT_DATA: [Очистка и вставка]
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM points")
            cursor.executemany("INSERT INTO points (x, y) VALUES (?, ?)", points)
            conn.commit()
        logger.info(f"[BeliefState][IMP:9][save_points][INSERT_DATA][Success] Сохранено {len(points)} точек в БД. [VALUE]")
        return True
    except Exception as e:
        logger.error(f"[DB][IMP:10][save_points][INSERT_DATA][Error] Ошибка сохранения точек: {e} [FATAL]")
        return False
    # END_BLOCK_INSERT_DATA
# END_FUNCTION_save_points

# START_FUNCTION_load_points
# START_CONTRACT:
# PURPOSE:Загрузка всех точек из БД в формате DataFrame.
# INPUTS: 
# - str =>db_path: Путь к файлу БД
# OUTPUTS: 
# - pd.DataFrame -Таблица с точками
# SIDE_EFFECTS: Нет.
# END_CONTRACT
def load_points(db_path: str) -> pd.DataFrame:
    """Загружает точки из БД."""
    # START_BLOCK_SELECT_DATA: [Чтение данных]
    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query("SELECT x, y FROM points ORDER BY x", conn)
        logger.debug(f"[DB][IMP:5][load_points][SELECT_DATA][Success] Загружено {len(df)} точек. [INFO]")
        return df
    except Exception as e:
        logger.error(f"[DB][IMP:10][load_points][SELECT_DATA][Error] Ошибка загрузки точек: {e} [FATAL]")
        return pd.DataFrame(columns=["x", "y"])
    # END_BLOCK_SELECT_DATA
# END_FUNCTION_load_points
