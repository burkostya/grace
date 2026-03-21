# FILE:lesson_16/src/database_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление SQLite базой данных для Lesson_16.
# SCOPE:Сохранение и получение точек параболы (x, y).
# INPUT:DataFrame с точками или путь к БД.
# OUTPUT:DataFrame с точками или статус сохранения.
# KEYWORDS:[DOMAIN(8): Data Persistence; TECH(9): SQLite, Pandas]
# LINKS:[USES_API(8): sqlite3, pandas]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления БД.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Сохраняет DataFrame в таблицу points] => save_points
# FUNC 10[Считывает точки из таблицы points] => get_points
# END_MODULE_MAP

import sqlite3
import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

# START_FUNCTION_save_points
# START_CONTRACT:
# PURPOSE:Запись DataFrame в таблицу points.
# INPUTS:
# - pd.DataFrame => df: Данные для сохранения.
# - str => db_path: Путь к файлу БД.
# OUTPUTS:
# - bool - Статус успеха операции.
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def save_points(df: pd.DataFrame, db_path: str = "lesson_16/app_16.db") -> bool:
    """
    Сохраняет переданный DataFrame в таблицу 'points' базы данных SQLite.
    Если таблица уже существует, она перезаписывается (if_exists='replace').
    Перед сохранением проверяется наличие директории для БД.
    """
    # START_BLOCK_SAVE_TO_DB: [Запись в SQLite]
    try:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        with sqlite3.connect(db_path) as conn:
            df.to_sql('points', conn, if_exists='replace', index=False)
        logger.info(f"[DB][IMP:9][save_points][SAVE_TO_DB][Success] Сохранено {len(df)} точек в {db_path}. [OK]")
        return True
    except Exception as e:
        logger.critical(f"[DB][IMP:10][save_points][SAVE_TO_DB][Error] Ошибка при сохранении в БД: {e}. [FATAL]")
        return False
    # END_BLOCK_SAVE_TO_DB
# END_FUNCTION_save_points

# START_FUNCTION_get_points
# START_CONTRACT:
# PURPOSE:Чтение точек из таблицы points.
# INPUTS:
# - str => db_path: Путь к файлу БД.
# OUTPUTS:
# - pd.DataFrame - Данные из БД.
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def get_points(db_path: str = "lesson_16/app_16.db") -> pd.DataFrame:
    """
    Считывает все данные из таблицы 'points' и возвращает их в виде DataFrame.
    Если БД или таблица отсутствуют, возвращает пустой DataFrame.
    """
    # START_BLOCK_READ_FROM_DB: [Чтение из SQLite]
    if not os.path.exists(db_path):
        logger.warning(f"[DB][IMP:7][get_points][READ_FROM_DB][NotFound] БД {db_path} не найдена. [WARN]")
        return pd.DataFrame(columns=['x', 'y'])
    
    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql('SELECT * FROM points', conn)
            logger.info(f"[DB][IMP:8][get_points][READ_FROM_DB][Success] Считано {len(df)} точек из {db_path}. [OK]")
            return df
    except Exception as e:
        logger.error(f"[DB][IMP:10][get_points][READ_FROM_DB][Error] Ошибка при чтении из БД: {e}. [FAIL]")
        return pd.DataFrame(columns=['x', 'y'])
    # END_BLOCK_READ_FROM_DB
# END_FUNCTION_get_points
