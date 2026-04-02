# FILE: lesson_19/db_manager.py
# VERSION: 1.0.2
# START_MODULE_CONTRACT:
# PURPOSE: Управление базой данных SQLite для ERP-прототипа.
# SCOPE: Создание таблиц, CRUD операции для накладных и их строк.
# INPUT: Путь к файлу БД.
# OUTPUT: Интерфейс взаимодействия с данными.
# KEYWORDS: [DOMAIN(8): Database; CONCEPT(7): SQLite; TECH(9): SQL]
# LINKS: [USES_API(8): sqlite3]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.2 - Добавлен метод execute_insert для получения ID последней вставленной строки.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Инициализация таблиц БД] => init_db
# FUNC 8[Выполнение запроса без возврата данных] => execute_query
# FUNC 9[Выполнение вставки с возвратом ID] => execute_insert
# FUNC 8[Выполнение запроса с возвратом данных] => fetch_query
# END_MODULE_MAP

import sqlite3
import logging
import os

logger = logging.getLogger(__name__)

# START_FUNCTION_init_db
# START_CONTRACT:
# PURPOSE: Создание таблиц invoices и invoice_lines, если они не существуют.
# INPUTS: 
# - str => db_path: Путь к файлу БД
# OUTPUTS: None
# SIDE_EFFECTS: Создает файл БД и таблицы.
# KEYWORDS: [PATTERN(6): Initialization; CONCEPT(8): Schema]
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def init_db(db_path: str):
    """
    Инициализирует схему базы данных. Создает таблицу накладных (invoices) 
    и таблицу строк накладных (invoice_lines) с внешним ключом.
    """
    # START_BLOCK_CONNECT: [Подключение к БД]
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    logger.debug(f"[DB][IMP:7][init_db][CONNECT] Подключение к {db_path} установлено [SUCCESS]")
    # END_BLOCK_CONNECT

    # START_BLOCK_CREATE_TABLES: [Создание таблиц]
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            client TEXT NOT NULL,
            total_amount REAL DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoice_lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER NOT NULL,
            product TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL,
            amount REAL NOT NULL,
            FOREIGN KEY (invoice_id) REFERENCES invoices (id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()
    logger.info(f"[BeliefState][IMP:9][init_db][CREATE_TABLES] Схема БД инициализирована корректно [VALUE]")
    # END_BLOCK_CREATE_TABLES
# END_FUNCTION_init_db

# START_FUNCTION_execute_query
# START_CONTRACT:
# PURPOSE: Выполнение SQL запроса (INSERT, UPDATE, DELETE).
# INPUTS:
# - str => db_path: Путь к БД
# - str => query: SQL запрос
# - tuple => params: Параметры запроса
# OUTPUTS: None
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def execute_query(db_path: str, query: str, params: tuple = ()):
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        logger.debug(f"[DB][IMP:5][execute_query][EXECUTE] Запрос выполнен: {query[:50]}... [SUCCESS]")
    finally:
        conn.close()
# END_FUNCTION_execute_query

# START_FUNCTION_execute_insert
# START_CONTRACT:
# PURPOSE: Выполнение INSERT запроса и возврат ID новой строки.
# INPUTS:
# - str => db_path: Путь к БД
# - str => query: SQL запрос
# - tuple => params: Параметры запроса
# OUTPUTS:
# - int - ID вставленной строки
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def execute_insert(db_path: str, query: str, params: tuple = ()) -> int:
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute(query, params)
        new_id = cursor.lastrowid
        conn.commit()
        logger.debug(f"[DB][IMP:6][execute_insert][INSERT] Вставлена строка с ID: {new_id} [SUCCESS]")
        return new_id
    finally:
        conn.close()
# END_FUNCTION_execute_insert

# START_FUNCTION_fetch_query
# START_CONTRACT:
# PURPOSE: Выполнение SELECT запроса.
# INPUTS:
# - str => db_path: Путь к БД
# - str => query: SQL запрос
# - tuple => params: Параметры запроса
# OUTPUTS:
# - list - Список строк (кортежей)
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def fetch_query(db_path: str, query: str, params: tuple = ()) -> list:
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        logger.debug(f"[DB][IMP:5][fetch_query][FETCH] Получено строк: {len(result)} [VALUE]")
        return result
    finally:
        conn.close()
# END_FUNCTION_fetch_query
