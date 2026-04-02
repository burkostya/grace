# FILE: lesson_22/db_manager.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Работа с базой данных SQLite для хранения точек параболы (points_22.db).
# SCOPE: Инициализация таблиц, пакетная вставка данных и извлечение данных.
# INPUT: Список кортежей точек (x, y) или путь к БД.
# OUTPUT: Список точек из БД или успешность операции.
# KEYWORDS:[DOMAIN(8): Database; CONCEPT(7): Persistence; TECH(9): SQLite]
# LINKS:[USES_API(8): sqlite3, os]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется SQLite?
# A: Автономность, отсутствие внешних зависимостей и поддержка SQL для аналитики.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля db_manager.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Инициализирует таблицу points в БД] => init_db
# FUNC 10[Пакетно сохраняет точки в БД] => save_points
# FUNC 10[Извлекает все точки из БД] => get_points
# END_MODULE_MAP

import sqlite3
import os
import logging

logger = logging.getLogger(__name__)


# START_FUNCTION_init_db
# START_CONTRACT:
# PURPOSE: Создает таблицу points, если она не существует.
# INPUTS:
# - str => db_path: Путь к файлу БД.
# OUTPUTS:
# - bool - Успешность операции.
# SIDE_EFFECTS: Создание файла и изменение схемы БД.
# KEYWORDS:[PATTERN(6): SchemaInitializer; CONCEPT(8): Setup]
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def init_db(db_path: str = "lesson_22/points_22.db") -> bool:
    """
    Функция проверяет наличие таблицы 'points' в БД и создает её при отсутствии.
    Колонки: id (PK), x (REAL), y (REAL).
    """
    # START_BLOCK_SETUP_SCHEMA: [Выполнение SQL-скрипта схемы]
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
            logger.info(
                f"[DB][IMP:8][init_db][SETUP_SCHEMA][Success] БД {db_path} инициализирована. [SUCCESS]"
            )
            return True
    except Exception as e:
        logger.critical(
            f"[SystemError][IMP:10][init_db][SETUP_SCHEMA][ExceptionEnrichment] Ошибка инициализации БД: {e} [FATAL]"
        )
        return False
    # END_BLOCK_SETUP_SCHEMA


# END_FUNCTION_init_db


# START_FUNCTION_save_points
# START_CONTRACT:
# PURPOSE: Очищает старые данные и сохраняет новые точки в БД.
# INPUTS:
# - list => points_list: Список кортежей [(x1, y1), (x2, y2), ...].
# - str => db_path: Путь к БД.
# OUTPUTS:
# - bool - Успешность операции.
# SIDE_EFFECTS: Изменение данных в БД.
# KEYWORDS:[PATTERN(6): BatchInsert; CONCEPT(8): DataPersistence]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def save_points(points_list: list, db_path: str = "lesson_22/points_22.db") -> bool:
    """
    Функция удаляет все текущие записи из таблицы 'points' и выполняет пакетную
    вставку новых данных. Использует транзакции для надежности.
    """
    # START_BLOCK_CLEAR_AND_INSERT: [Пакетная обработка данных]
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # Очистка старых данных
            cursor.execute("DELETE FROM points")
            # Пакетная вставка
            cursor.executemany("INSERT INTO points (x, y) VALUES (?, ?)", points_list)
            conn.commit()

            logger.info(
                f"[BeliefState][IMP:9][save_points][CLEAR_AND_INSERT][Success] Сохранено {len(points_list)} точек в БД. [SUCCESS]"
            )
            return True
    except Exception as e:
        logger.critical(
            f"[SystemError][IMP:10][save_points][CLEAR_AND_INSERT][ExceptionEnrichment] Ошибка сохранения точек: {e} [FATAL]"
        )
        return False
    # END_BLOCK_CLEAR_AND_INSERT


# END_FUNCTION_save_points


# START_FUNCTION_get_points
# START_CONTRACT:
# PURPOSE: Извлекает список всех точек из БД.
# INPUTS:
# - str => db_path: Путь к БД.
# OUTPUTS:
# - list - Список кортежей [(x, y), ...].
# SIDE_EFFECTS: Чтение данных из БД.
# KEYWORDS:[PATTERN(6): DataFetcher; CONCEPT(8): DataRetrieval]
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def get_points(db_path: str = "lesson_22/points_22.db") -> list:
    """
    Функция возвращает все накопленные данные из таблицы 'points' в виде списка кортежей.
    Используется для последующего отображения в таблице или построения графика.
    """
    # START_BLOCK_FETCH_DATA: [Чтение из SQLite]
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT x, y FROM points ORDER BY x ASC")
            data = cursor.fetchall()
            logger.debug(
                f"[DB][IMP:7][get_points][FETCH_DATA][Success] Получено {len(data)} точек. [INFO]"
            )
            return data
    except Exception as e:
        logger.critical(
            f"[SystemError][IMP:10][get_points][FETCH_DATA][ExceptionEnrichment] Ошибка извлечения данных: {e} [FATAL]"
        )
        return []
    # END_BLOCK_FETCH_DATA


# END_FUNCTION_get_points
