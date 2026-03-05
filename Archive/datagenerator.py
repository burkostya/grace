# FILE: datagenerator.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Модуль для генерации точек параболы и их сохранения в базу данных SQLite.
# SCOPE: Математические расчеты, работа с базой данных (SQLite).
# INPUT: Коэффициенты параболы (a, c), диапазон x.
# OUTPUT: Записи в таблице 'points' базы данных 'parabola.db'.
# KEYWORDS: [DOMAIN(9): Mathematics; TECH(8): SQLite; CONCEPT(7): Parabola; TECH(6): Python]
# LINKS: [USES_API(7): sqlite3]
# END_MODULE_CONTRACT
# START_MODULE_MAP:
# CLASS 9 [Управляет генерацией данных и взаимодействием с SQLite] => DataGenerator
# METHOD 8 [Инициализирует БД и создает таблицу] => __init__
# METHOD 9 [Генерирует точки y = ax^2 + c и сохраняет их] => generate_points
# METHOD 7 [Возвращает все точки из БД] => get_all_points
# END_MODULE_MAP
# START_USE_CASES:
# - [DataGenerator.generate_points]: User (UI) -> CalculateAndSavePoints -> DatabaseUpdated
# - [DataGenerator.get_all_points]: System (UI) -> FetchPoints -> DataReadyForDisplay
# END_USE_CASES

import sqlite3
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# START_CLASS_DataGenerator
# START_CONTRACT:
# PURPOSE: Класс для работы с данными параболы в SQLite.
# ATTRIBUTES:
# - [Путь к файлу базы данных] => db_path: str
# METHODS:
# - [Инициализация и создание таблиц] => __init__(db_path)
# - [Расчет и сохранение точек] => generate_points(a, c, x_range)
# - [Чтение данных] => get_all_points()
# KEYWORDS: [PATTERN(8): DAO; DOMAIN(9): DataStorage; TECH(7): SQLite]
# END_CONTRACT

class DataGenerator:
    """Класс для генерации и хранения точек параболы."""

    # START_METHOD___init__
    # START_CONTRACT:
    # PURPOSE: Инициализация подключения к БД и создание таблицы.
    # INPUTS:
    # - [Путь к БД] => db_path: str
    # KEYWORDS: [CONCEPT(5): Initialization]
    # END_CONTRACT
    def __init__(self, db_path: str = "parabola.db"):
        self.db_path = db_path
        # START_BLOCK_INIT_DB: [Создание таблицы, если она не существует.]
        logger.debug(f"[SelfCheck][DataGenerator][INIT_DB][Params] Инициализация БД: {self.db_path} [ATTEMPT]")
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS points (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        x REAL,
                        y REAL
                    )
                """)
                conn.commit()
            logger.info(f"[TraceCheck][DataGenerator][INIT_DB][StepComplete] Таблица 'points' готова [SUCCESS]")
        except Exception as e:
            logger.error(f"[CriticalError][DataGenerator][INIT_DB][ExceptionCaught] Ошибка инициализации: {e} [FAIL]")
            raise
        # END_BLOCK_INIT_DB
    # END_METHOD___init__

    # START_METHOD_generate_points
    # START_CONTRACT:
    # PURPOSE: Генерирует точки параболы y = ax^2 + c и сохраняет их в БД.
    # INPUTS:
    # - [Коэффициент a] => a: float
    # - [Смещение c] => c: float
    # - [Диапазон x (start, end, step)] => x_range: tuple
    # KEYWORDS: [CONCEPT(8): Calculation; TECH(7): SQL_Insert]
    # END_CONTRACT
    def generate_points(self, a: float, c: float, x_range: tuple = (-10, 10, 0.5)):
        """Рассчитывает точки и обновляет БД."""
        # START_BLOCK_CLEAR_OLD_DATA: [Удаление старых записей перед генерацией.]
        logger.debug(f"[VarCheck][DataGenerator][CLEAR_OLD_DATA][ConditionCheck] Очистка таблицы перед новой генерацией [ATTEMPT]")
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM points")
        # END_BLOCK_CLEAR_OLD_DATA

        # START_BLOCK_CALCULATE_AND_SAVE: [Цикл расчета и вставки данных.]
        start, end, step = x_range
        points = []
        current_x = start
        while current_x <= end:
            y = a * (current_x ** 2) + c
            points.append((current_x, y))
            current_x += step
        
        logger.debug(f"[VarCheck][DataGenerator][CALCULATE_AND_SAVE][Params] Сгенерировано точек: {len(points)} [VALUE]")
        
        with sqlite3.connect(self.db_path) as conn:
            conn.executemany("INSERT INTO points (x, y) VALUES (?, ?)", points)
            conn.commit()
        
        logger.info(f"[TraceCheck][DataGenerator][CALCULATE_AND_SAVE][StepComplete] Данные успешно сохранены в БД [SUCCESS]")
        # END_BLOCK_CALCULATE_AND_SAVE
    # END_METHOD_generate_points

    # START_METHOD_get_all_points
    # START_CONTRACT:
    # PURPOSE: Получение всех точек из базы данных.
    # OUTPUTS:
    # - [Список кортежей (x, y)] => list[tuple[float, float]]
    # KEYWORDS: [TECH(6): SQL_Select]
    # END_CONTRACT
    def get_all_points(self):
        """Возвращает список всех точек из БД."""
        # START_BLOCK_FETCH_DATA: [Запрос всех данных из таблицы.]
        logger.debug(f"[SelfCheck][DataGenerator][FETCH_DATA][CallExternal] Запрос данных из БД [ATTEMPT]")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT x, y FROM points ORDER BY x")
            data = cursor.fetchall()
        logger.debug(f"[VarCheck][DataGenerator][FETCH_DATA][ReturnData] Получено строк: {len(data)} [VALUE]")
        return data
        # END_BLOCK_FETCH_DATA
    # END_METHOD_get_all_points

# END_CLASS_DataGenerator
