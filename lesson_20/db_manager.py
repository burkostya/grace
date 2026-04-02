# FILE:lesson_20/db_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление SQLite базой данных для хранения точек параболы.
# SCOPE:Инициализация БД, сохранение и получение точек (x, y).
# INPUT:Путь к файлу points.db.
# OUTPUT:Статус операций или список точек.
# KEYWORDS:[DOMAIN(8): Database; CONCEPT(7): Persistence; TECH(9): SQLite]
# LINKS:[USES_API(8): sqlite3]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется SQLite?
# A: Это легковесная БД, не требующая сервера, идеально подходит для учебных уроков.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание модуля управления БД.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Инициализирует таблицу в БД] => init_db
# FUNC 10[Сохраняет список точек в БД] => save_points
# FUNC 10[Получает все точки из БД] => get_points
# END_MODULE_MAP

import sqlite3
import os
import logging

logger = logging.getLogger("lesson_20")

# START_FUNCTION_init_db
# START_CONTRACT:
# PURPOSE:Создание таблицы points в БД.
# INPUTS:
# - str => db_path: Путь к БД
# OUTPUTS:
# - bool - Статус успеха
# KEYWORDS:[PATTERN(6): Initializer]
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def init_db(db_path: str = "lesson_20/points.db") -> bool:
    """
    Инициализирует базу данных SQLite и создает таблицу points, если она не существует.
    """
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
        logger.info(f"[DB][IMP:8][init_db][CREATE_TABLE][Success] БД инициализирована: {db_path}. [SUCCESS]")
        return True
    except Exception as e:
        logger.error(f"[DB][IMP:10][init_db][CREATE_TABLE][Error] Ошибка инициализации БД: {e}. [FATAL]")
        return False
    # END_BLOCK_CREATE_TABLE
# END_FUNCTION_init_db

# START_FUNCTION_save_points
# START_CONTRACT:
# PURPOSE:Сохранение списка точек в БД.
# INPUTS:
# - list => points: Список кортежей (x, y)
# - str => db_path: Путь к БД
# OUTPUTS:
# - bool - Статус успеха
# KEYWORDS:[PATTERN(6): Saver]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def save_points(points: list, db_path: str = "lesson_20/points.db") -> bool:
    """
    Очищает таблицу points и сохраняет новый набор точек.
    """
    # START_BLOCK_INSERT_DATA: [Вставка данных]
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM points")
            cursor.executemany("INSERT INTO points (x, y) VALUES (?, ?)", points)
            conn.commit()
        logger.info(f"[DB][IMP:9][save_points][INSERT_DATA][Success] Сохранено {len(points)} точек. [VALUE]")
        return True
    except Exception as e:
        logger.error(f"[DB][IMP:10][save_points][INSERT_DATA][Error] Ошибка сохранения точек: {e}. [FATAL]")
        return False
    # END_BLOCK_INSERT_DATA
# END_FUNCTION_save_points

# START_FUNCTION_get_points
# START_CONTRACT:
# PURPOSE:Получение всех точек из БД.
# INPUTS:
# - str => db_path: Путь к БД
# OUTPUTS:
# - list - Список кортежей (x, y)
# KEYWORDS:[PATTERN(6): Loader]
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def get_points(db_path: str = "lesson_20/points.db") -> list:
    """
    Выбирает все точки из таблицы points и возвращает их в виде списка кортежей.
    """
    # START_BLOCK_SELECT_DATA: [Выборка данных]
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT x, y FROM points ORDER BY x")
            points = cursor.fetchall()
        logger.info(f"[DB][IMP:8][get_points][SELECT_DATA][Success] Загружено {len(points)} точек. [SUCCESS]")
        return points
    except Exception as e:
        logger.error(f"[DB][IMP:10][get_points][SELECT_DATA][Error] Ошибка получения точек: {e}. [FATAL]")
        return []
    # END_BLOCK_SELECT_DATA
# END_FUNCTION_get_points
