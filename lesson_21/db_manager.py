# FILE:lesson_21/db_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление SQLite БД для ERP-прототипа: создание таблиц и инициализация демо-данных.
# SCOPE: Инициализация схемы БД, наполнение справочника товаров, предоставление соединений.
# INPUT:Путь к файлу БД (по умолчанию erp_base.db).
# OUTPUT: Соединение sqlite3.Connection, созданные таблицы в БД.
# KEYWORDS:[DOMAIN(8): ERP; CONCEPT(7): DatabaseManagement; TECH(9): SQLite3]
# LINKS:[USES_API(8): sqlite3]
# LINKS_TO_SPECIFICATION:lesson_21/business_requirements.md#ARTIFACT_DB_SCHEMA
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется sqlite3 напрямую без ORM?
# A: Требование учебного урока для демонстрации SQL-запросов и минимизации зависимостей.
# Q: Почему демо-данные зашиты в код?
# A: Для обеспечения автономности и воспроизводимости урока без внешних CSV/JSON файлов.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля db_manager с таблицами invoices, items, invoice_lines.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Создает таблицы и заполняет справочник товаров демо-позициями] => init_db
# FUNC 8[Возвращает объект соединения с SQLite БД] => get_connection
# END_MODULE_MAP
#
# START_USE_CASES:
# - [init_db]: System (Startup) -> CreateSchemaAndPopulate -> DatabaseReady
# - [get_connection]: Handlers -> RequestConnection -> SqliteConnectionProvided
# END_USE_CASES

import sqlite3
import logging
import os

# Настройка логгера для модуля
logger = logging.getLogger(__name__)

DB_PATH = "lesson_21/erp_base.db"

# START_FUNCTION_get_connection
# START_CONTRACT:
# PURPOSE:Возвращает объект соединения с SQLite БД.
# INPUTS:
# - Путь к БД (опционально) => db_path: str
# OUTPUTS:
# - sqlite3.Connection -Объект соединения
# SIDE_EFFECTS: Создает файл БД, если он отсутствует.
# KEYWORDS:[PATTERN(6): Factory; CONCEPT(8): ConnectionManagement]
# LINKS:[USES_API(8): sqlite3.connect]
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """
    Функция устанавливает соединение с базой данных SQLite по указанному пути.
    Она настраивает row_factory на sqlite3.Row для удобного доступа к полям по именам,
    что критично для интеграции с Ag-Grid и Pandas в последующих модулях.
    """
    # START_BLOCK_CONNECT: [Установка соединения]
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        logger.debug(f"[DB][IMP:7][get_connection][CONNECT][IO] Соединение с {db_path} установлено [SUCCESS]")
        return conn
    except Exception as e:
        logger.error(f"[DB][IMP:10][get_connection][CONNECT][Exception] Ошибка подключения к {db_path}: {e} [FATAL]")
        raise
    # END_BLOCK_CONNECT
# END_FUNCTION_get_connection

# START_FUNCTION_init_db
# START_CONTRACT:
# PURPOSE:Создает структуру таблиц и наполняет справочник товаров.
# INPUTS:
# - Путь к БД (опционально) => db_path: str
# OUTPUTS:
# - None
# SIDE_EFFECTS: Модифицирует схему БД, вставляет ~20 записей в таблицу items.
# KEYWORDS:[PATTERN(7): Initializer; CONCEPT(9): SchemaDefinition]
# LINKS:[READS_DATA_FROM(7): Hardcoded Demo Data]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def init_db(db_path: str = DB_PATH):
    """
    Функция выполняет полную инициализацию базы данных. Она создает три таблицы:
    invoices (заголовки), items (справочник товаров) и invoice_lines (строки накладных).
    После создания таблиц функция очищает справочник товаров и заполняет его 
    20-ю демонстрационными позициями для обеспечения работоспособности прототипа.
    """
    # START_BLOCK_CREATE_TABLES: [Создание структуры таблиц]
    logger.info(f"[BeliefState][IMP:9][init_db][CREATE_TABLES][Schema] Начинаю инициализацию схемы БД в {db_path} [START]")
    
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    queries = [
        """
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            client_name TEXT NOT NULL,
            total_sum REAL DEFAULT 0
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS invoice_lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            qty INTEGER NOT NULL,
            price REAL NOT NULL,
            line_sum REAL NOT NULL,
            FOREIGN KEY (invoice_id) REFERENCES invoices (id),
            FOREIGN KEY (item_id) REFERENCES items (id)
        )
        """
    ]
    
    for query in queries:
        cursor.execute(query)
    conn.commit()
    
    logger.debug(f"[DB][IMP:8][init_db][CREATE_TABLES][SQL] Таблицы созданы или уже существуют [SUCCESS]")
    # END_BLOCK_CREATE_TABLES

    # START_BLOCK_POPULATE_ITEMS: [Наполнение справочника товаров]
    # Демо-данные: 20 позиций электроники и офисных товаров
    demo_items = [
        ("SKU-001", "Laptop Pro 15", 1200.0),
        ("SKU-002", "Monitor 27 inch", 350.0),
        ("SKU-003", "Wireless Mouse", 25.0),
        ("SKU-004", "Mechanical Keyboard", 85.0),
        ("SKU-005", "USB-C Hub", 45.0),
        ("SKU-006", "External SSD 1TB", 110.0),
        ("SKU-007", "Webcam 4K", 95.0),
        ("SKU-008", "Headphones ANC", 150.0),
        ("SKU-009", "Office Chair", 210.0),
        ("SKU-010", "Desk Lamp LED", 35.0),
        ("SKU-011", "Smartphone X", 800.0),
        ("SKU-012", "Tablet Air", 500.0),
        ("SKU-013", "Smart Watch", 199.0),
        ("SKU-014", "Power Bank 20k", 40.0),
        ("SKU-015", "HDMI Cable 2m", 12.0),
        ("SKU-016", "Printer Laser", 250.0),
        ("SKU-017", "Toner Cartridge", 65.0),
        ("SKU-018", "Paper A4 (500sh)", 8.0),
        ("SKU-019", "Router WiFi 6", 120.0),
        ("SKU-020", "Bluetooth Speaker", 55.0)
    ]
    
    try:
        # Очистка перед вставкой для идемпотентности в рамках урока
        cursor.execute("DELETE FROM items")
        cursor.executemany(
            "INSERT INTO items (sku, name, price) VALUES (?, ?, ?)",
            demo_items
        )
        conn.commit()
        logger.info(f"[BeliefState][IMP:9][init_db][POPULATE_ITEMS][Data] Справочник товаров заполнен: {len(demo_items)} позиций [SUCCESS]")
    except Exception as e:
        conn.rollback()
        logger.error(f"[DB][IMP:10][init_db][POPULATE_ITEMS][Exception] Ошибка при заполнении items: {e} [FATAL]")
        raise
    finally:
        conn.close()
    # END_BLOCK_POPULATE_ITEMS
# END_FUNCTION_init_db
