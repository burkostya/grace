# FILE: lesson_18/src/data_processor.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Расчет точек параболы y = ax^2 + c и работа с базой данных SQLite.
# SCOPE: Математические вычисления, ETL (Extract, Transform, Load) в SQLite.
# INPUT: Параметры a, c, x_min, x_max.
# OUTPUT: Pandas DataFrame с точками (x, y).
# KEYWORDS: [DOMAIN(8): Math; CONCEPT(7): Parabola; TECH(9): SQLite, Pandas]
# LINKS: [USES_API(8): sqlite3, pandas, numpy]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля обработки данных и работы с БД.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# CLASS 10[Класс для расчетов и хранения данных] => DataProcessor
# END_MODULE_MAP
#
# START_USE_CASES:
# - [DataProcessor]: User -> Generate Points -> SQLite Storage -> Visualization
# END_USE_CASES

import sqlite3
import pandas as pd
import numpy as np
import logging
import os

logger = logging.getLogger(__name__)

# START_FUNCTION_DataProcessor
# START_CONTRACT:
# PURPOSE: Класс для выполнения математических расчетов и взаимодействия с SQLite.
# KEYWORDS: [PATTERN(7): DataAccessObject]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
class DataProcessor:
    """
    DataProcessor отвечает за генерацию точек параболы по формуле y = ax^2 + c
    и их сохранение в базу данных SQLite для последующего использования.
    """

    def __init__(self, db_path: str = "lesson_18/parabola.db"):
        self.db_path = db_path
        # START_BLOCK_INIT_DB: [Инициализация базы данных]
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()
        # END_BLOCK_INIT_DB

    def _init_db(self):
        """Создает таблицу points, если она не существует."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("CREATE TABLE IF NOT EXISTS points (x REAL, y REAL)")
            logger.debug(f"[DB][IMP:7][DataProcessor][_init_db][IO] Таблица points инициализирована. [SUCCESS]")
        except Exception as e:
            logger.critical(f"[DB][IMP:10][DataProcessor][_init_db][Exception] Ошибка инициализации БД: {e}. [FATAL]")

    # START_FUNCTION_generate_points
    # START_CONTRACT:
    # PURPOSE: Генерация точек параболы.
    # INPUTS:
    # - float => a: Коэффициент a
    # - float => c: Коэффициент c
    # - float => x_min: Минимум x
    # - float => x_max: Максимум x
    # OUTPUTS: 
    # - pd.DataFrame - DataFrame с колонками x и y
    # COMPLEXITY_SCORE: 4
    # END_CONTRACT
    def generate_points(self, a: float, c: float, x_min: float, x_max: float) -> pd.DataFrame:
        """
        Вычисляет 100 точек параболы в заданном диапазоне.
        """
        # START_BLOCK_CALCULATION: [Математический расчет]
        x = np.linspace(x_min, x_max, 100)
        y = a * (x ** 2) + c
        df = pd.DataFrame({'x': x, 'y': y})
        logger.info(f"[Math][IMP:9][DataProcessor][generate_points][Logic] Сгенерировано {len(df)} точек для a={a}, c={c}. [VALUE]")
        return df
        # END_BLOCK_CALCULATION

    # START_FUNCTION_save_to_db
    # START_CONTRACT:
    # PURPOSE: Сохранение DataFrame в SQLite с предварительной очисткой.
    # INPUTS:
    # - pd.DataFrame => df: Данные для сохранения
    # OUTPUTS: 
    # - bool - Статус успеха
    # COMPLEXITY_SCORE: 6
    # END_CONTRACT
    def save_to_db(self, df: pd.DataFrame) -> bool:
        """
        Очищает таблицу points и записывает новые данные.
        """
        # START_BLOCK_DB_WRITE: [Запись в БД]
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Очистка старых данных
                conn.execute("DELETE FROM points")
                # Запись новых данных через pandas
                df.to_sql('points', conn, if_exists='append', index=False)
            logger.info(f"[BeliefState][IMP:9][DataProcessor][save_to_db][IO] Данные успешно сохранены в БД {self.db_path}. [SUCCESS]")
            return True
        except Exception as e:
            logger.error(f"[DB][IMP:10][DataProcessor][save_to_db][Exception] Ошибка при сохранении в БД: {e}. [ERROR]")
            return False
        # END_BLOCK_DB_WRITE

    # START_FUNCTION_load_from_db
    # START_CONTRACT:
    # PURPOSE: Загрузка данных из SQLite.
    # INPUTS: Нет
    # OUTPUTS: 
    # - pd.DataFrame - Загруженные данные
    # COMPLEXITY_SCORE: 4
    # END_CONTRACT
    def load_from_db(self) -> pd.DataFrame:
        """
        Считывает все точки из таблицы points.
        """
        # START_BLOCK_DB_READ: [Чтение из БД]
        try:
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql("SELECT * FROM points", conn)
            logger.debug(f"[DB][IMP:7][DataProcessor][load_from_db][IO] Загружено {len(df)} точек из БД. [SUCCESS]")
            return df
        except Exception as e:
            logger.error(f"[DB][IMP:10][DataProcessor][load_from_db][Exception] Ошибка при чтении из БД: {e}. [ERROR]")
            return pd.DataFrame(columns=['x', 'y'])
        # END_BLOCK_DB_READ
# END_FUNCTION_DataProcessor
