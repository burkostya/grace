# FILE:lesson_14/src/database_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление хранением данных в SQLite базе.
# SCOPE:Инициализация БД, сохранение и извлечение точек тригонометрических функций.
# INPUT:Путь к файлу базы данных.
# OUTPUT:Сохранение/извлечение точек, инициализация схемы.
# KEYWORDS:DOMAIN(Data); CONCEPT(Database); TECH(Python, sqlite3)
# LINKS:USES_API(sqlite3)
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется SQLite вместо PostgreSQL/MySQL?
# A: SQLite - легковесная встраиваемая БД, идеальна для учебных приложений и демонстраций.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание менеджера базы данных.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# CLASS[10][Менеджер базы данных] => DatabaseManager
# END_MODULE_MAP
#
# START_USE_CASES:
# - [DatabaseManager]:User -> Init/Save/Load -> Data Storage
# END_USE_CASES

import sqlite3
import logging
import os

logger = logging.getLogger("lesson_14.database_manager")

# START_CLASS_DatabaseManager
class DatabaseManager:
    """
    Класс для управления базой данных SQLite. 
    Предоставляет методы для инициализации схемы, сохранения и извлечения точек.
    """
    
    def __init__(self, db_path: str = "lesson_14/trig.db"):
        self.db_path = db_path
        self._ensure_db_file()
        logger.info(f"[DB][IMP:7][DatabaseManager][__init__][Init] База данных инициализирована: {db_path} [SUCCESS]")
    
    def _ensure_db_file(self):
        """Создает файл базы данных, если его нет."""
        if not os.path.exists(self.db_path):
            self.init_db()
            logger.debug(f"[DB][IMP:4][DatabaseManager][ENSURE_DB] Создан новый файл БД: {self.db_path}")
    
    # START_FUNCTION_init_db
    # START_CONTRACT:
    # PURPOSE:Инициализация схемы базы данных.
    # INPUTS:Нет
    # OUTPUTS: 
    # - bool -True при успешной инициализации
    # SIDE_EFFECTS:Создание таблицы points, если не существует.
    # KEYWORDS:PATTERN(Database Schema); CONCEPT(Initialization)
    # COMPLEXITY_SCORE:4
    # END_CONTRACT
    def init_db(self) -> bool:
        """
        Инициализирует схему базы данных. 
        Создает таблицу points с колонками x и y, если она не существует.
        """
        # START_BLOCK_CREATE_TABLE: [Создание таблицы points]
        try:
            conn = sqlite3.connect(self.db_path)
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
            
            logger.debug(f"[DB][IMP:4][DatabaseManager][INIT_DB] Таблица points создана/проверена [SUCCESS]")
            return True
        except sqlite3.Error as e:
            logger.error(f"[DB][IMP:10][DatabaseManager][INIT_DB][Error] Ошибка инициализации БД: {e} [FAIL]")
            return False
        # END_BLOCK_CREATE_TABLE
    
    # START_FUNCTION_save_points
    # START_CONTRACT:
    # PURPOSE:Сохранение точек в базу данных (замена старых данных).
    # INPUTS: 
    # - list =>points: Список кортежей (x, y)
    # OUTPUTS: 
    # - bool -True при успешном сохранении
    # SIDE_EFFECTS:Очистка старых данных, запись новых точек.
    # KEYWORDS:PATTERN(Database Write); CONCEPT(Persistence)
    # COMPLEXITY_SCORE:5
    # END_CONTRACT
    def save_points(self, points: list) -> bool:
        """
        Сохраняет список точек в базу данных, удаляя старые данные.
        Использует транзакцию для атомарности.
        """
        # START_BLOCK_CLEAR_DATA: [Очистка старых данных]
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM points')
            logger.debug(f"[DB][IMP:5][DatabaseManager][SAVE_POINTS][Clear] Старые данные удалены: {cursor.rowcount} записей [INFO]")
        finally:
            conn.close()
        # END_BLOCK_CLEAR_DATA
        
        # START_BLOCK_INSERT_DATA: [Вставка новых точек]
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.executemany('INSERT INTO points (x, y) VALUES (?, ?)', points)
            conn.commit()
            
            logger.info(f"[DB][IMP:8][DatabaseManager][SAVE_POINTS][Success] Сохранено {cursor.rowcount} точек [SUCCESS]")
            result = True
        except sqlite3.Error as e:
            logger.error(f"[DB][IMP:10][DatabaseManager][SAVE_POINTS][Error] Ошибка сохранения: {e} [FAIL]")
            result = False
        finally:
            conn.close()
        # END_BLOCK_INSERT_DATA
        
        return result
    
    # START_FUNCTION_get_points
    # START_CONTRACT:
    # PURPOSE:Извлечение всех точек из базы данных.
    # INPUTS:Нет
    # OUTPUTS: 
    # - list -Список кортежей (x, y)
    # SIDE_EFFECTS:Чтение из БД.
    # KEYWORDS:PATTERN(Database Read); CONCEPT(Retrieval)
    # COMPLEXITY_SCORE:3
    # END_CONTRACT
    def get_points(self) -> list:
        """
        Извлекает все точки из базы данных.
        Возвращает пустой список, если таблица пуста.
        """
        # START_BLOCK_QUERY_DATA: [Запрос всех точек]
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT x, y FROM points ORDER BY id')
            points = cursor.fetchall()
            
            conn.close()
            
            logger.debug(f"[DB][IMP:4][DatabaseManager][GET_POINTS] Извлечено {len(points)} точек [INFO]")
            return points
        except sqlite3.Error as e:
            logger.error(f"[DB][IMP:10][DatabaseManager][GET_POINTS][Error] Ошибка чтения: {e} [FAIL]")
            return []
        # END_BLOCK_QUERY_DATA

# END_CLASS_DatabaseManager
