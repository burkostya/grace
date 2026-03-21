# FILE:lesson_10/src/database_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление базой данных SQLite для хранения точек параболы.
# SCOPE:Создание таблиц, очистка данных, запись и чтение точек.
# INPUT:Путь к файлу БД.
# OUTPUT:Данные в формате списка кортежей или pandas DataFrame.
# KEYWORDS:[DOMAIN(Persistence): Database; CONCEPT(Storage): SQLite; TECH(Python): sqlite3, pandas]
# LINKS:[USES_API(9): sqlite3, pandas]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется pandas для чтения данных?
# A: Это упрощает интеграцию с Gradio (Dataframe) и Plotly, а также ускоряет обработку больших наборов точек.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля управления БД.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Инициализирует БД и создает таблицу points] => init_db
# FUNC 10[Очищает таблицу и записывает новые точки] => save_points
# FUNC 10[Считывает все точки из БД в DataFrame] => get_points_df
# END_MODULE_MAP
#
# START_USE_CASES:
# - [init_db]: System -> CreateTable -> DBReady
# - [save_points]: Logic -> WritePoints -> DataPersisted
# - [get_points_df]: UI/CLI -> ReadPoints -> DataFrameReturned
# END_USE_CASES

import sqlite3
import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

# START_FUNCTION_init_db
# START_CONTRACT:
# PURPOSE:Создает таблицу points, если она не существует.
# INPUTS: 
# - Путь к БД => db_path: str
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Создает файл БД и таблицу.
# KEYWORDS:[PATTERN(Schema): Initializer]
# COMPLEXITY_SCORE: 2
# END_CONTRACT
def init_db(db_path: str = "lesson_10/data.db"):
    """
    Инициализирует соединение с SQLite и создает структуру таблицы 'points' 
    с колонками x и y (тип REAL). Это фундамент для хранения результатов расчетов.
    """
    # START_BLOCK_CREATE_TABLE: [Создание схемы]
    try:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        with sqlite3.connect(db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS points (x REAL, y REAL)")
        logger.info(f"[State][IMP:7][init_db][CREATE_TABLE][IO] БД {db_path} инициализирована. [SUCCESS]")
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][init_db][CREATE_TABLE][Exception] Ошибка инициализации БД: {e} [FATAL]")
    # END_BLOCK_CREATE_TABLE
# END_FUNCTION_init_db

# START_FUNCTION_save_points
# START_CONTRACT:
# PURPOSE:Очищает таблицу и записывает новый набор точек.
# INPUTS: 
# - Список точек => points: list[tuple[float, float]]
# - Путь к БД => db_path: str
# OUTPUTS: 
# - bool - Успешность операции
# SIDE_EFFECTS: Удаляет старые данные из таблицы.
# KEYWORDS:[PATTERN(Transaction): Writer]
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def save_points(points: list, db_path: str = "lesson_10/data.db") -> bool:
    """
    Выполняет атомарную операцию обновления данных: сначала удаляет все записи 
    из таблицы 'points', затем вставляет новые значения через executemany.
    Это гарантирует, что в БД всегда актуальный срез данных последнего расчета.
    """
    # START_BLOCK_UPDATE_DATA: [Транзакционная запись]
    try:
        init_db(db_path)
        with sqlite3.connect(db_path) as conn:
            conn.execute("DELETE FROM points")
            conn.executemany("INSERT INTO points (x, y) VALUES (?, ?)", points)
        logger.info(f"[BeliefState][IMP:9][save_points][UPDATE_DATA][IO] Сохранено {len(points)} точек в БД. [SUCCESS]")
        return True
    except Exception as e:
        logger.error(f"[SystemError][IMP:10][save_points][UPDATE_DATA][Exception] Ошибка сохранения точек: {e} [FATAL]")
        return False
    # END_BLOCK_UPDATE_DATA
# END_FUNCTION_save_points

# START_FUNCTION_get_points_df
# START_CONTRACT:
# PURPOSE:Считывает данные из БД в pandas DataFrame.
# INPUTS: 
# - Путь к БД => db_path: str
# OUTPUTS: 
# - pd.DataFrame - Таблица с колонками x, y
# SIDE_EFFECTS: Нет.
# KEYWORDS:[PATTERN(Query): Reader]
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def get_points_df(db_path: str = "lesson_10/data.db") -> pd.DataFrame:
    """
    Использует pandas для выполнения SQL-запроса и преобразования результата 
    в DataFrame. Если БД пуста или отсутствует, возвращает пустой DataFrame 
    с заданными именами колонок.
    """
    # START_BLOCK_READ_DF: [Чтение в DataFrame]
    try:
        if not os.path.exists(db_path):
            logger.warning(f"[State][IMP:6][get_points_df][READ_DF][IO] БД {db_path} не существует. [WARN]")
            return pd.DataFrame(columns=['x', 'y'])
            
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query("SELECT x, y FROM points", conn)
            logger.debug(f"[Data][IMP:4][get_points_df][READ_DF][Success] Считано {len(df)} строк. [VALUE]")
            return df
    except Exception as e:
        logger.error(f"[SystemError][IMP:10][get_points_df][READ_DF][Exception] Ошибка чтения БД: {e} [FATAL]")
        return pd.DataFrame(columns=['x', 'y'])
    # END_BLOCK_READ_DF
# END_FUNCTION_get_points_df
