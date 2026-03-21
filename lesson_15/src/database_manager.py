# FILE: lesson_15/src/database_manager.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Управление SQLite БД для хранения точек параболы.
# SCOPE: Persistence, Data Storage.
# INPUT: Путь к файлу БД.
# OUTPUT: Таблица точек (x, y).
# KEYWORDS: [DOMAIN(8): Database; TECH(7): SQLite; CONCEPT(9): Persistence]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание модуля управления БД.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# CLASS 10[Класс для работы с SQLite] => DatabaseManager
# END_MODULE_MAP

import sqlite3
import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

# START_FUNCTION_DatabaseManager
class DatabaseManager:
    """
    Класс DatabaseManager обеспечивает хранение и извлечение рассчитанных точек параболы
    в локальной базе данных SQLite.
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()

    # START_FUNCTION_init_db
    # START_CONTRACT:
    # PURPOSE: Инициализация схемы БД.
    # INPUTS: Нет
    # OUTPUTS: Нет
    # COMPLEXITY_SCORE: 3
    # END_CONTRACT
    def init_db(self):
        """Создает таблицу points, если она не существует."""
        # START_BLOCK_INIT_LOGIC: [Создание таблицы]
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("CREATE TABLE IF NOT EXISTS points (x REAL, y REAL)")
            logger.info(f"[DB][IMP:7][DatabaseManager][init_db][Schema] БД инициализирована. [SUCCESS]")
        except Exception as e:
            logger.error(f"[DB][IMP:10][DatabaseManager][init_db][Error] Ошибка инициализации БД: {e} [FATAL]")
        # END_BLOCK_INIT_LOGIC

    # START_FUNCTION_save_points
    # START_CONTRACT:
    # PURPOSE: Сохранение DataFrame с точками в БД.
    # INPUTS: 
    # - pd.DataFrame => df: Данные для сохранения.
    # OUTPUTS: 
    # - bool - Успешность операции.
    # COMPLEXITY_SCORE: 4
    # END_CONTRACT
    def save_points(self, df: pd.DataFrame) -> bool:
        """Очищает таблицу и сохраняет новые точки."""
        # START_BLOCK_SAVE_LOGIC: [Запись данных]
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM points")
                df.to_sql("points", conn, if_exists="append", index=False)
            logger.info(f"[BeliefState][IMP:9][DatabaseManager][save_points][IO] Сохранено {len(df)} точек. [VALUE]")
            return True
        except Exception as e:
            logger.error(f"[DB][IMP:10][DatabaseManager][save_points][Error] Ошибка сохранения точек: {e} [FATAL]")
            return False
        # END_BLOCK_SAVE_LOGIC

    # START_FUNCTION_get_points
    # START_CONTRACT:
    # PURPOSE: Извлечение всех точек из БД.
    # INPUTS: Нет
    # OUTPUTS: 
    # - pd.DataFrame - Данные из БД.
    # COMPLEXITY_SCORE: 3
    # END_CONTRACT
    def get_points(self) -> pd.DataFrame:
        """Возвращает все точки из БД в виде DataFrame."""
        # START_BLOCK_GET_LOGIC: [Чтение данных]
        try:
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql("SELECT * FROM points", conn)
            logger.debug(f"[DB][IMP:5][DatabaseManager][get_points][IO] Извлечено {len(df)} точек. [SUCCESS]")
            return df
        except Exception as e:
            logger.error(f"[DB][IMP:10][DatabaseManager][get_points][Error] Ошибка чтения БД: {e} [FATAL]")
            return pd.DataFrame(columns=["x", "y"])
        # END_BLOCK_GET_LOGIC
# END_FUNCTION_DatabaseManager
