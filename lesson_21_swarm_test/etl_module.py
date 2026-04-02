# FILE:lesson_21_swarm_test/etl_module.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Простой ETL-процесс для загрузки данных из CSV в SQLite с валидацией.
# SCOPE: Извлечение (CSV), Трансформация (Drop NaN), Загрузка (SQLite).
# INPUT: Путь к CSV файлу (data.csv), путь к БД (warehouse.db).
# OUTPUT: Таблица 'scores' в базе данных SQLite.
# KEYWORDS:[DOMAIN(9): ETL; CONCEPT(8): DataProcessing; TECH(9): Pandas, SQLite]
# LINKS:[READS_DATA_FROM(8): data.csv; USES_API(9): pandas, sqlite3]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется Pandas для удаления пустых значений?
# A: Pandas эффективен в векторизованных операциях фильтрации, что снижает риск логических ошибок по сравнению с итерацией по строкам.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля ETL-загрузки для Swarm-теста.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Основная функция ETL: читает CSV, очищает и сохраняет в БД] => load_csv_to_db
# END_MODULE_MAP
#
# START_USE_CASES:
# -[load_csv_to_db]: System (CLI/Test) -> ProcessCSVtoSQLite -> DataLoadedToWarehouse
# END_USE_CASES

import pandas as pd
import sqlite3
import logging
import os

logger = logging.getLogger(__name__)


# START_FUNCTION_load_csv_to_db
# START_CONTRACT:
# PURPOSE: Выполняет полный цикл ETL для одного CSV файла.
# INPUTS:
# - csv_path => str: Путь к исходному CSV файлу.
# - db_path => str: Путь к результирующей базе данных SQLite.
# OUTPUTS:
# - bool - True если загрузка прошла успешно, иначе False.
# SIDE_EFFECTS: Создает/обновляет таблицу 'scores' в БД.
# KEYWORDS:[PATTERN(8): Pipeline; CONCEPT(9): DataCleaning]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def load_csv_to_db(csv_path: str, db_path: str) -> bool:
    """
    Функция реализует цепочку обработки данных: чтение, очистка от неполных записей (NaN)
    и сохранение в реляционную таблицу SQLite. Используется Pandas для повышения
    надежности и векторизации операций трансформации. Логирование [IMP:7-10]
    обеспечивает семантическую трассировку для AI-агентов.
    """

    # START_BLOCK_EXTRACT:[Чтение исходных данных]
    logger.info(
        f"[ETL][IMP:7][load_csv_to_db][EXTRACT][IO] Начало чтения {csv_path} [START]"
    )
    try:
        df = pd.read_csv(csv_path)
        logger.debug(
            f"[VarCheck][IMP:4][load_csv_to_db][EXTRACT][State] Загружено строк: {len(df)} [INFO]"
        )
    except Exception as e:
        logger.critical(
            f"[SystemError][IMP:10][load_csv_to_db][EXTRACT][ExceptionEnrichment] Ошибка при чтении CSV: {e} [FATAL]"
        )
        return False
    # END_BLOCK_EXTRACT

    # START_BLOCK_TRANSFORM:[Очистка и валидация данных]
    # BUG_FIX_CONTEXT: Ранее pd.dropna() не пересоздавал DataFrame без явного присваивания или inplace=True.
    initial_count = len(df)
    df = df.dropna()
    final_count = len(df)

    logger.info(
        f"[ETL][IMP:8][load_csv_to_db][TRANSFORM][ConditionCheck] Удалено {initial_count - final_count} неполных строк. Осталось: {final_count} [SUCCESS]"
    )
    # END_BLOCK_TRANSFORM

    # START_BLOCK_LOAD:[Сохранение в SQLite]
    try:
        conn = sqlite3.connect(db_path)
        # BUG_FIX_CONTEXT: Используем if_exists='replace' для тестовой среды, чтобы избежать дублей ID при перезапусках.
        df.to_sql("scores", conn, if_exists="replace", index=False)
        conn.close()

        logger.info(
            f"[BeliefState][IMP:9][load_csv_to_db][LOAD][AAGGoal] Данные успешно загружены в таблицу scores в {db_path} [VALUE]"
        )
        return True
    except Exception as e:
        logger.critical(
            f"[SystemError][IMP:10][load_csv_to_db][LOAD][ExceptionEnrichment] Сбой при записи в БД: {e} [FATAL]"
        )
        return False
    # END_BLOCK_LOAD


# END_FUNCTION_load_csv_to_db
