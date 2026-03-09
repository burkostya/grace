# FILE:lesson_9/src/database_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление базой данных SQLite для хранения точек параболы.
# SCOPE: Создание таблиц, сохранение и получение координат (x, y).
# INPUT:Координаты точек, путь к БД.
# OUTPUT: Списки точек, статус выполнения операций.
# KEYWORDS:[DOMAIN(8): Database; CONCEPT(7): Persistence; TECH(9): sqlite3]
# LINKS:[USES_API(8): sqlite3]
# LINKS_TO_SPECIFICATION:[DevelopmentPlan.md:15-17]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления БД SQLite.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC [7][Инициализирует БД и создает таблицы] => init_db
# FUNC [9][Сохраняет список точек в БД] => save_points
# FUNC [8][Получает все точки из БД] => get_points
# END_MODULE_MAP
#
# START_USE_CASES:
# - [save_points]: System -> Clear old points & Insert new -> DataStored
# - [get_points]: UI/CLI -> Select all points -> DataRetrieved
# END_USE_CASES

import sqlite3
import logging
import os

# Настройка логгера для LDD 2.0
logger = logging.getLogger("lesson_9")
DB_PATH = "lesson_9/parabola.db"

# START_FUNCTION_init_db
# START_CONTRACT:
# PURPOSE:Создание таблицы points, если она не существует.
# INPUTS: 
# - None
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Создание файла БД и таблицы на диске.
# KEYWORDS:[PATTERN(6): Initialization; CONCEPT(8): Schema]
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def init_db():
    """
    Функция инициализирует соединение с SQLite и создает таблицу points.
    Таблица содержит две колонки: x (REAL) и y (REAL). 
    Используется для обеспечения структуры данных перед началом работы.
    """
    # START_BLOCK_CREATE_TABLE: [Выполнение SQL запроса на создание]
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS points (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    x REAL NOT NULL,
                    y REAL NOT NULL
                )
            """)
            conn.commit()
        logger.info(f"[DB][IMP:7][init_db][CREATE_TABLE][Success] БД инициализирована по пути {DB_PATH} [SUCCESS]")
    except Exception as e:
        logger.critical(f"[DB][IMP:10][init_db][CREATE_TABLE][Error] Ошибка инициализации БД: {e} [FATAL]")
    # END_BLOCK_CREATE_TABLE
# END_FUNCTION_init_db

# START_FUNCTION_save_points
# START_CONTRACT:
# PURPOSE:Очистка старых данных и сохранение новых точек.
# INPUTS: 
# - list[tuple[float, float]] => points: Список кортежей (x, y).
# OUTPUTS: 
# - bool - Статус успеха.
# SIDE_EFFECTS: Изменение данных в БД.
# KEYWORDS:[PATTERN(7): Transaction; CONCEPT(8): DataOverwrite]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def save_points(points: list) -> bool:
    """
    Функция реализует атомарную операцию обновления данных: сначала 
    удаляются все существующие записи из таблицы points, затем 
    вставляется новый пакет данных. Использование транзакции (with conn) 
    гарантирует целостность данных.
    """
    # START_BLOCK_TRANSACTION: [Очистка и вставка данных]
    try:
        init_db() # Гарантируем наличие таблицы
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            # Удаление старых данных
            cursor.execute("DELETE FROM points")
            logger.debug(f"[DB][IMP:5][save_points][TRANSACTION][Delete] Старые точки удалены. [INFO]")
            
            # Массовая вставка
            cursor.executemany("INSERT INTO points (x, y) VALUES (?, ?)", points)
            conn.commit()
            
        logger.info(f"[DB][IMP:9][save_points][TRANSACTION][Success] Сохранено {len(points)} точек. [VALUE]")
        return True
    except Exception as e:
        logger.error(f"[DB][IMP:10][save_points][TRANSACTION][Error] Ошибка при сохранении точек: {e} [FATAL]")
        return False
    # END_BLOCK_TRANSACTION
# END_FUNCTION_save_points

# START_FUNCTION_get_points
# START_CONTRACT:
# PURPOSE:Получение всех сохраненных точек из БД.
# INPUTS: 
# - None
# OUTPUTS: 
# - list[tuple[float, float]] - Список точек (x, y).
# SIDE_EFFECTS: Чтение из БД.
# KEYWORDS:[PATTERN(6): DataAccess; CONCEPT(8): Query]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def get_points() -> list:
    """
    Функция извлекает все записи из таблицы points и возвращает их 
    в виде списка кортежей. Если данных нет или произошла ошибка, 
    возвращается пустой список.
    """
    # START_BLOCK_QUERY_DATA: [Выполнение SELECT запроса]
    points = []
    try:
        if not os.path.exists(DB_PATH):
            logger.debug(f"[DB][IMP:4][get_points][QUERY_DATA][Check] Файл БД не найден. [INFO]")
            return []

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT x, y FROM points ORDER BY x")
            points = cursor.fetchall()
            
        logger.info(f"[DB][IMP:8][get_points][QUERY_DATA][Success] Извлечено {len(points)} точек. [VALUE]")
        return points
    except Exception as e:
        logger.error(f"[DB][IMP:10][get_points][QUERY_DATA][Error] Ошибка при получении точек: {e} [FATAL]")
        return []
    # END_BLOCK_QUERY_DATA
# END_FUNCTION_get_points
