# FILE:lesson_v5/src/database_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление базой данных SQLite для хранения точек параболы.
# SCOPE:Создание таблиц, сохранение и получение данных.
# INPUT:Путь к файлу БД.
# OUTPUT:Интерфейс для работы с данными.
# KEYWORDS:[DOMAIN(8): Database; CONCEPT(7): Persistence; TECH(9): SQLite]
# LINKS:[WRITES_DATA_TO(9): lesson_v5/parabola.db]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления БД.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# CLASS 10[Управляет соединением и операциями с БД] => DatabaseManager
# END_MODULE_MAP
#
# START_USE_CASES:
# - [DatabaseManager]: System -> ManageDataPersistence -> DataStored
# END_USE_CASES

import sqlite3
import logging
import os

logger = logging.getLogger(__name__)

# START_CLASS_DatabaseManager
class DatabaseManager:
    """Класс для управления базой данных SQLite."""
    
    def __init__(self, db_path: str):
        # START_BLOCK_INIT_DB: [Инициализация соединения и создание таблиц]
        self.db_path = db_path
        logger.debug(f"[DB][IMP:5][DatabaseManager][INIT_DB][Start] Инициализация БД: {db_path} [INFO]")
        
        # Создаем директорию, если она не существует
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        self._create_tables()
        # END_BLOCK_INIT_DB

    def _create_tables(self):
        # START_BLOCK_CREATE_TABLES: [Создание структуры таблиц]
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS parabola_points (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        a REAL,
                        c REAL,
                        x REAL,
                        y REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
            logger.info(f"[BeliefState][IMP:9][DatabaseManager][CREATE_TABLES][Success] Таблицы созданы/проверены. [VALUE]")
        except Exception as e:
            logger.critical(f"[SystemError][IMP:10][DatabaseManager][CREATE_TABLES][Exception] Ошибка создания таблиц: {e} [FATAL]")
            raise
        # END_BLOCK_CREATE_TABLES

    # START_FUNCTION_save_points
    # START_CONTRACT:
    # PURPOSE:Сохраняет список точек в БД.
    # INPUTS: 
    # - list => points: Список кортежей (a, c, x, y)
    # OUTPUTS: 
    # - None
    # SIDE_EFFECTS: Запись в БД.
    # KEYWORDS:[PATTERN(6): BatchInsert; CONCEPT(8): Persistence]
    # END_CONTRACT
    def save_points(self, points: list):
        """Сохраняет точки в базу данных."""
        # START_BLOCK_SAVE_POINTS: [Пакетная вставка данных]
        logger.debug(f"[DB][IMP:7][DatabaseManager][SAVE_POINTS][Start] Сохранение {len(points)} точек [INFO]")
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.executemany(
                    "INSERT INTO parabola_points (a, c, x, y) VALUES (?, ?, ?, ?)",
                    points
                )
                conn.commit()
            logger.info(f"[BeliefState][IMP:9][DatabaseManager][SAVE_POINTS][Success] Точки успешно сохранены. [VALUE]")
        except Exception as e:
            logger.error(f"[SystemError][IMP:10][DatabaseManager][SAVE_POINTS][Exception] Ошибка сохранения: {e} [FATAL]")
            raise
        # END_BLOCK_SAVE_POINTS
    # END_FUNCTION_save_points

    # START_FUNCTION_get_all_points
    # START_CONTRACT:
    # PURPOSE:Возвращает все сохраненные точки.
    # INPUTS: Нет
    # OUTPUTS: 
    # - list -Список всех точек из БД
    # SIDE_EFFECTS: Чтение из БД.
    # KEYWORDS:[PATTERN(6): Query; CONCEPT(8): Retrieval]
    # END_CONTRACT
    def get_all_points(self) -> list:
        """Возвращает все точки из базы данных."""
        # START_BLOCK_GET_POINTS: [Выборка данных]
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT a, c, x, y, timestamp FROM parabola_points ORDER BY timestamp DESC")
                rows = cursor.fetchall()
            logger.info(f"[BeliefState][IMP:9][DatabaseManager][GET_POINTS][Success] Получено {len(rows)} записей. [VALUE]")
            return rows
        except Exception as e:
            logger.error(f"[SystemError][IMP:10][DatabaseManager][GET_POINTS][Exception] Ошибка чтения: {e} [FATAL]")
            raise
        # END_BLOCK_GET_POINTS
    # END_FUNCTION_get_all_points
# END_CLASS_DatabaseManager
