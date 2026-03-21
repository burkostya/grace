# FILE:lesson_11/src/database_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление персистентностью данных точек параболы в базе данных SQLite.
# SCOPE:Создание таблиц, очистка данных, сохранение и получение списка точек.
# INPUT:Списки кортежей (x, y) для сохранения.
# OUTPUT:Списки кортежей (x, y) при чтении.
# KEYWORDS:[DOMAIN(8): Database; CONCEPT(7): Persistence; TECH(9): SQLite3]
# LINKS:[USES_API(8): sqlite3; WRITES_LOG(7): lesson_11/app_11.log]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется очистка таблицы перед сохранением в save_points?
# A: Согласно требованиям задачи, необходимо сохранять "новый список точек", что подразумевает замену старого состояния новым для обеспечения консистентности отображения одной кривой.
# Q: Почему путь к БД и логу жестко прописан?
# A: Это прямое требование ТЗ для данного урока (lesson_11).
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичная реализация модуля database_manager с поддержкой LDD 2.0 и семантической разметкой.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Инициализирует таблицу points в БД] => init_db
# FUNC 10[Заменяет все точки в БД на новые] => save_points
# FUNC 10[Возвращает список всех точек из БД] => get_points
# END_MODULE_MAP
#
# START_USE_CASES:
# - [init_db]: System -> CreateTableIfNotExist -> DatabaseReady
# - [save_points]: UI_Controller -> ReplacePoints -> DataPersisted
# - [get_points]: UI_Controller -> FetchPoints -> DataLoaded
# END_USE_CASES

import sqlite3
import logging
import os

# START_BLOCK_LOGGING_CONFIG: [Настройка LDD 2.0 логирования]
LOG_FILE = "lesson_11/app_11.log"
DB_PATH = "lesson_11/parabola_11.db"

# Обеспечиваем наличие директории для лога
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logger = logging.getLogger("database_manager")
# END_BLOCK_LOGGING_CONFIG

# START_FUNCTION_init_db
# START_CONTRACT:
# PURPOSE:Создает таблицу points (x REAL, y REAL), если она отсутствует в базе данных.
# INPUTS: Нет
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Создает файл БД и таблицу на диске.
# KEYWORDS:[PATTERN(7): Initialization; CONCEPT(8): SchemaDefinition]
# COMPLEXITY_SCORE: 3[Простая DDL операция]
# END_CONTRACT
def init_db():
    """
    Функция выполняет первичную настройку базы данных SQLite. Она открывает соединение 
    с файлом parabola_11.db и выполняет SQL-запрос CREATE TABLE IF NOT EXISTS. 
    Это гарантирует, что структура данных готова к работе перед выполнением операций 
    чтения или записи, не уничтожая существующие данные при повторном вызове.
    """
    logger.info(f"[Flow][IMP:5][init_db][START][Operation] Начало инициализации БД [INFO]")
    
    # START_BLOCK_EXECUTE_DDL: [Выполнение SQL для создания таблицы]
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS points (x REAL, y REAL)")
            conn.commit()
            logger.info(f"[IO][IMP:8][init_db][EXECUTE_DDL][SQL] Таблица 'points' проверена/создана в {DB_PATH} [SUCCESS]")
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][init_db][EXECUTE_DDL][Exception] Ошибка при создании таблицы: {e} [FATAL]")
        raise
    # END_BLOCK_EXECUTE_DDL
    
    logger.info(f"[Flow][IMP:5][init_db][END][Operation] Инициализация БД завершена [SUCCESS]")
# END_FUNCTION_init_db

# START_FUNCTION_save_points
# START_CONTRACT:
# PURPOSE:Очищает таблицу points и сохраняет новый список координат.
# INPUTS: 
# - list[tuple[float, float]] => points_list: Список точек для сохранения
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Удаляет старые записи и вставляет новые в таблицу points.
# KEYWORDS:[PATTERN(8): Transaction; CONCEPT(9): DataReplacement]
# COMPLEXITY_SCORE: 5[Требует транзакционности для атомарной замены данных]
# END_CONTRACT
def save_points(points_list):
    """
    Функция обеспечивает атомарную замену набора точек в базе данных. Сначала выполняется 
    команда DELETE для очистки таблицы, затем используется executemany для эффективной 
    вставки всего списка кортежей. Использование контекстного менеджера sqlite3.connect 
    гарантирует автоматический commit при успехе и rollback при возникновении исключения.
    """
    logger.info(f"[Flow][IMP:6][save_points][START][Operation] Сохранение {len(points_list)} точек [INFO]")
    
    # START_BLOCK_TRANSACTION: [Очистка и вставка данных]
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            # Очистка старых данных
            cursor.execute("DELETE FROM points")
            logger.debug(f"[IO][IMP:7][save_points][TRANSACTION][Delete] Старые точки удалены [SUCCESS]")
            
            # Вставка новых данных
            cursor.executemany("INSERT INTO points (x, y) VALUES (?, ?)", points_list)
            conn.commit()
            
            logger.info(f"[BeliefState][IMP:9][save_points][TRANSACTION][Commit] Данные успешно заменены. Кол-во: {len(points_list)} [VALUE]")
    except Exception as e:
        logger.error(f"[SystemError][IMP:10][save_points][TRANSACTION][Exception] Сбой транзакции сохранения: {e} [FATAL]")
        raise
    # END_BLOCK_TRANSACTION
    
    logger.info(f"[Flow][IMP:6][save_points][END][Operation] Процесс сохранения завершен [SUCCESS]")
# END_FUNCTION_save_points

# START_FUNCTION_get_points
# START_CONTRACT:
# PURPOSE:Извлекает все записи из таблицы points.
# INPUTS: Нет
# OUTPUTS: 
# - list[tuple[float, float]] - Список всех точек из БД
# SIDE_EFFECTS: Нет
# KEYWORDS:[PATTERN(6): DataAccessObject; CONCEPT(8): Query]
# COMPLEXITY_SCORE: 4[Простая выборка данных]
# END_CONTRACT
def get_points():
    """
    Функция считывает все накопленные координаты из таблицы points. Она возвращает 
    результат в виде списка кортежей, где каждый кортеж представляет собой пару (x, y). 
    Если таблица пуста, возвращается пустой список. Логирование фиксирует объем 
    прочитанных данных для отладки потока данных в UI.
    """
    logger.info(f"[Flow][IMP:5][get_points][START][Operation] Запрос точек из БД [INFO]")
    points = []
    
    # START_BLOCK_FETCH_DATA: [Выполнение SELECT запроса]
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT x, y FROM points")
            points = cursor.fetchall()
            
            logger.info(f"[IO][IMP:8][get_points][FETCH_DATA][Result] Получено {len(points)} точек из БД [SUCCESS]")
    except Exception as e:
        logger.error(f"[SystemError][IMP:10][get_points][FETCH_DATA][Exception] Ошибка при чтении данных: {e} [FATAL]")
        raise
    # END_BLOCK_FETCH_DATA
    
    return points
# END_FUNCTION_get_points
