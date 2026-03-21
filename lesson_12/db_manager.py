# FILE:lesson_12/db_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Управление базой данных SQLite для хранения точек параболы.
# SCOPE: Создание таблиц, сохранение и загрузка данных.
# INPUT: Pandas DataFrame или список словарей.
# OUTPUT: Данные из БД.
# KEYWORDS:[DOMAIN(8): Database; TECH(7): SQLite]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.1 - Исправление семантической разметки: добавлены MODULE_MAP, USE_CASES и контракты функций.]
# PREV_CHANGE_SUMMARY: [v1.0.0 - Создание модуля управления БД.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 7[Инициализирует БД] => init_db
# FUNC 8[Сохраняет DataFrame в БД] => save_points
# FUNC 9[Обновляет БД из списка словарей] => update_points_from_dict
# FUNC 8[Загружает данные из БД] => load_points
# END_MODULE_MAP
#
# START_USE_CASES:
# - [init_db]: System -> SQLite -> TableCreated
# - [save_points]: Logic -> DataFrame -> SQLite
# - [update_points_from_dict]: UI -> ListDict -> SQLite
# - [load_points]: UI/CLI -> SQLite -> DataFrame
# END_USE_CASES

import sqlite3
import pandas as pd
import os
import logging

logger = logging.getLogger("lesson_12.app")
DB_PATH = os.path.join(os.path.dirname(__file__), "parabola.db")

# START_FUNCTION_init_db
# START_CONTRACT:
# PURPOSE: Инициализация схемы базы данных.
# INPUTS: None
# OUTPUTS: None
# COMPLEXITY_SCORE: 2
# END_CONTRACT
def init_db():
    """Инициализирует структуру таблицы в БД."""
    # START_BLOCK_SCHEMA: [Создание таблицы]
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                x REAL,
                y REAL,
                y_edited REAL
            )
        """)
    logger.info("[DB][IMP:7][init_db][SCHEMA][Success] БД инициализирована. [INFO]")
    # END_BLOCK_SCHEMA

# START_FUNCTION_save_points
# START_CONTRACT:
# PURPOSE: Полная перезапись данных в таблице.
# INPUTS: 
# - df: pd.DataFrame
# OUTPUTS: None
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def save_points(df: pd.DataFrame):
    """Полностью перезаписывает таблицу новыми точками."""
    # START_BLOCK_WRITE: [Запись в БД]
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM points")
        df.to_sql("points", conn, if_exists="append", index=False)
    logger.info(f"[DB][IMP:8][save_points][WRITE][Success] Сохранено {len(df)} точек. [VALUE]")
    # END_BLOCK_WRITE

# START_FUNCTION_update_points_from_dict
# START_CONTRACT:
# PURPOSE: Синхронизация данных из UI с базой данных.
# INPUTS: 
# - data: list[dict]
# OUTPUTS: None
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def update_points_from_dict(data: list[dict]):
    """Обновляет БД на основе данных из UI (с учетом правок)."""
    # START_BLOCK_SYNC: [Синхронизация]
    df = pd.DataFrame(data)
    save_points(df)
    logger.info("[DB][IMP:9][update_points_from_dict][SYNC][Success] БД синхронизирована с правками UI. [VALUE]")
    # END_BLOCK_SYNC

# START_FUNCTION_load_points
# START_CONTRACT:
# PURPOSE: Загрузка всех точек из базы данных.
# INPUTS: None
# OUTPUTS: 
# - pd.DataFrame
# COMPLEXITY_SCORE: 2
# END_CONTRACT
def load_points() -> pd.DataFrame:
    """Загружает все точки из БД."""
    # START_BLOCK_READ: [Чтение из БД]
    if not os.path.exists(DB_PATH):
        logger.debug("[DB][IMP:4][load_points][READ][Empty] Файл БД не найден. [INFO]")
        return pd.DataFrame(columns=["x", "y", "y_edited"])
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql("SELECT x, y, y_edited FROM points", conn)
    logger.debug(f"[DB][IMP:4][load_points][READ][Success] Загружено {len(df)} строк. [INFO]")
    return df
    # END_BLOCK_READ
# END_FUNCTION_load_points
