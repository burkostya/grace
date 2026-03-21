# FILE:lesson_13/src/database_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление хранением данных в SQLite.
# SCOPE:Инициализация БД, сохранение точек и получение данных.
# INPUT:Путь к файлу БД.
# OUTPUT:Результаты SQL запросов.
# KEYWORDS:DOMAIN(Data Storage); CONCEPT(SQL); TECH(Python, sqlite3, logging)
# LINKS:USES_API(sqlite3)
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется SQLite?
# A: Легковесная БД, не требующая сервера, идеально подходит для локального хранения точек параболы.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля работы с БД.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# CLASS[10][Класс для работы с SQLite] => DatabaseManager
# END_MODULE_MAP
#
# START_USE_CASES:
# - [DatabaseManager]:System -> Save/Get Points -> Persistent Data Storage
# END_USE_CASES

import sqlite3
import os
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    DatabaseManager инкапсулирует все операции с базой данных SQLite.
    Он отвечает за создание таблиц, очистку старых данных и сохранение новых
    вычисленных точек параболы.
    """

    def __init__(self, db_path: str = "lesson_13/parabola.db"):
        # START_BLOCK_INIT: [Инициализация пути к БД]
        self.db_path = db_path
        logger.debug(f"[DB][IMP:4][DatabaseManager][INIT][Flow] Инициализация с путем: {db_path} [SUCCESS]")
        # END_BLOCK_INIT

    # START_FUNCTION_init_db
    # START_CONTRACT:
    # PURPOSE:Создание таблицы для хранения точек, если она не существует.
    # INPUTS: 
    # - Нет
    # OUTPUTS: 
    # - bool -Успешность инициализации
    # SIDE_EFFECTS: Создает файл БД и таблицу
    # KEYWORDS:CONCEPT(Schema)
    # COMPLEXITY_SCORE:4
    # END_CONTRACT
    def init_db(self) -> bool:
        """
        Выполняет SQL запрос для создания таблицы points.
        Таблица содержит колонки id, x и y.
        """
        # START_BLOCK_CREATE_TABLE: [Выполнение DDL запроса]
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS points (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        x REAL NOT NULL,
                        y REAL NOT NULL
                    )
                ''')
                conn.commit()
            logger.info(f"[DB][IMP:7][DatabaseManager][init_db][IO] Таблица points проверена/создана в {self.db_path} [SUCCESS]")
            return True
        except Exception as e:
            logger.critical(f"[SystemError][IMP:10][DatabaseManager][init_db][Exception] Ошибка инициализации БД: {e} [FATAL]")
            return False
        # END_BLOCK_CREATE_TABLE
    # END_FUNCTION_init_db

    # START_FUNCTION_save_points
    # START_CONTRACT:
    # PURPOSE:Сохранение списка точек в БД с предварительной очисткой.
    # INPUTS: 
    # - list =>points: Список кортежей (x, y)
    # OUTPUTS: 
    # - bool -Успешность сохранения
    # SIDE_EFFECTS: Очищает таблицу points и вставляет новые данные
    # KEYWORDS:PATTERN(Transaction); CONCEPT(ETL)
    # COMPLEXITY_SCORE:5
    # END_CONTRACT
    def save_points(self, points: list) -> bool:
        """
        Очищает таблицу points и вставляет новые значения.
        Использует транзакцию для обеспечения целостности данных.
        """
        # START_BLOCK_TRANSACTION: [Очистка и вставка данных]
        if not points:
            logger.warning(f"[DB][IMP:6][DatabaseManager][save_points][Flow] Попытка сохранить пустой список точек. [WARN]")
            return False

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM points")
                cursor.executemany("INSERT INTO points (x, y) VALUES (?, ?)", points)
                conn.commit()
            logger.info(f"[BeliefState][IMP:9][DatabaseManager][save_points][IO] Сохранено {len(points)} точек в БД. [SUCCESS]")
            return True
        except Exception as e:
            logger.error(f"[DB][IMP:10][DatabaseManager][save_points][Exception] Ошибка при сохранении точек: {e} [FATAL]")
            return False
        # END_BLOCK_TRANSACTION
    # END_FUNCTION_save_points

    # START_FUNCTION_get_points
    # START_CONTRACT:
    # PURPOSE:Получение всех точек из БД.
    # INPUTS: 
    # - Нет
    # OUTPUTS: 
    # - list -Список кортежей (x, y)
    # SIDE_EFFECTS: Нет
    # KEYWORDS:CONCEPT(Query)
    # COMPLEXITY_SCORE:3
    # END_CONTRACT
    def get_points(self) -> list:
        """
        Выполняет SELECT запрос для получения всех сохраненных точек.
        Возвращает список кортежей, отсортированных по x.
        """
        # START_BLOCK_QUERY: [Выполнение SELECT]
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT x, y FROM points ORDER BY x")
                results = cursor.fetchall()
            logger.info(f"[DB][IMP:8][DatabaseManager][get_points][IO] Извлечено {len(results)} точек из БД. [SUCCESS]")
            return results
        except Exception as e:
            logger.error(f"[DB][IMP:10][DatabaseManager][get_points][Exception] Ошибка при чтении точек: {e} [FATAL]")
            return []
        # END_BLOCK_QUERY
    # END_FUNCTION_get_points
