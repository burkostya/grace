# FILE: lesson_v2/src/data_generator.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Модуль для расчета точек параболы и сохранения их в SQLite.
# SCOPE: Бэкенд, математические расчеты, работа с БД.
# INPUT: Параметры функции (a, c, x_min, x_max, step).
# OUTPUT: Данные в SQLite и DataFrame.
# KEYWORDS: [DOMAIN(9): Backend; TECH(8): SQLite; CONCEPT(7): Parabola]
# LINKS: [USES_API(7): sqlite3; USES_API(6): pandas]
# END_MODULE_CONTRACT
# START_MODULE_MAP:
# CLASS 9 [Управляет расчетами и БД] => DataGeneratorPro
# METHOD 8 [Генерирует точки и пишет в БД] => generate_points
# METHOD 7 [Читает все точки из БД] => get_all_points
# END_MODULE_MAP

import sqlite3
import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

# START_CLASS_DataGeneratorPro
# START_CONTRACT:
# PURPOSE: Класс для управления данными параболы в SQLite.
# ATTRIBUTES:
# - [Путь к файлу БД] => db_path: str
# METHODS:
# - [Генерация и сохранение точек] => generate_points()
# - [Получение данных] => get_all_points()
# KEYWORDS: [PATTERN(8): DAO; TECH(7): SQLite]
# END_CONTRACT

class DataGeneratorPro:
    """Класс для работы с данными параболы."""

    # START_METHOD___init__
    def __init__(self, db_path="lesson_v2/parabola_pro.db"):
        # START_BLOCK_INIT_DB: [Инициализация пути и создание папок.]
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        logger.debug(f"[VarCheck][DataGeneratorPro][__init__][Params] DB Path: {self.db_path} [VALUE]")
        self._create_table()
        # END_BLOCK_INIT_DB

    def _create_table(self):
        # START_BLOCK_CREATE_TABLE: [Создание таблицы в БД.]
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS points (x REAL, y REAL)")
        logger.info(f"[TraceCheck][DataGeneratorPro][_create_table][StepComplete] Таблица готова [SUCCESS]")
        # END_BLOCK_CREATE_TABLE
    # END_METHOD___init__

    # START_METHOD_generate_points
    # START_CONTRACT:
    # PURPOSE: Рассчитывает y = ax^2 + c и сохраняет в БД.
    # INPUTS:
    # - [Коэффициент a] => a: float
    # - [Смещение c] => c: float
    # - [Начало X] => x_min: float
    # - [Конец X] => x_max: float
    # - [Шаг] => step: float
    # END_CONTRACT
    def generate_points(self, a: float, c: float, x_min: float, x_max: float, step: float = 0.1):
        # START_BLOCK_CLEAR_OLD: [Очистка старых данных.]
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM points")
        logger.debug(f"[SelfCheck][DataGeneratorPro][generate_points][ConditionCheck] БД очищена [SUCCESS]")
        # END_BLOCK_CLEAR_OLD

        # START_BLOCK_CALC_AND_SAVE: [Расчет и вставка.]
        points = []
        current_x = x_min
        while current_x <= x_max:
            y = a * (current_x ** 2) + c
            points.append((current_x, y))
            current_x += step
        
        with sqlite3.connect(self.db_path) as conn:
            conn.executemany("INSERT INTO points (x, y) VALUES (?, ?)", points)
        
        logger.info(f"[TraceCheck][DataGeneratorPro][generate_points][StepComplete] Сгенерировано {len(points)} точек [SUCCESS]")
        # END_BLOCK_CALC_AND_SAVE
    # END_METHOD_generate_points

    # START_METHOD_get_all_points
    def get_all_points(self):
        # START_BLOCK_FETCH: [Чтение данных из БД.]
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query("SELECT * FROM points", conn)
        logger.debug(f"[VarCheck][DataGeneratorPro][get_all_points][ReturnData] Загружено строк: {len(df)} [VALUE]")
        return df
        # END_BLOCK_FETCH
    # END_METHOD_get_all_points

# END_CLASS_DataGeneratorPro
