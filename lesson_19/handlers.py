# FILE: lesson_19/handlers.py
# VERSION: 1.0.3
# START_MODULE_CONTRACT:
# PURPOSE: Чистая бизнес-логика ERP-прототипа.
# SCOPE: Генерация данных, получение строк накладных, обновление данных.
# INPUT: Данные из БД и UI.
# OUTPUT: Обработанные данные для Dash.
# KEYWORDS: [DOMAIN(8): BusinessLogic; CONCEPT(7): DataProcessing; TECH(9): Python]
# LINKS: [USES_API(8): db_manager, config_manager]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.3 - Использование execute_insert для надежного получения ID накладной.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Генерация демо-данных] => generate_mock_data
# FUNC 9[Получение списка накладных] => get_invoices
# FUNC 9[Получение строк накладной] => get_invoice_lines
# FUNC 10[Обновление строк накладной] => update_invoice_lines
# END_MODULE_MAP

import random
import datetime
import logging
from .db_manager import execute_query, fetch_query, execute_insert
from .config_manager import get_products

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# START_FUNCTION_generate_mock_data
# START_CONTRACT:
# PURPOSE: Очистка БД и генерация 5 случайных накладных.
# INPUTS:
# - str => db_path: Путь к БД
# OUTPUTS: None
# SIDE_EFFECTS: Очищает и заполняет таблицы invoices и invoice_lines.
# KEYWORDS: [PATTERN(6): MockData; CONCEPT(8): ETL]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def generate_mock_data(db_path: str):
    """
    Генерирует 5 накладных с 3-5 товарами в каждой.
    """
    # START_BLOCK_CLEANUP: [Очистка таблиц]
    execute_query(db_path, "DELETE FROM invoice_lines")
    execute_query(db_path, "DELETE FROM invoices")
    logger.info(f"[Logic][IMP:7][generate_mock_data][CLEANUP] Таблицы очищены [SUCCESS]")
    # END_BLOCK_CLEANUP

    # START_BLOCK_GENERATE: [Генерация данных]
    products_dict = get_products()
    product_names = list(products_dict.keys())
    clients = ["ООО Ромашка", "ИП Иванов", "ЗАО Вектор", "ПАО Газпром", "ООО Техно"]

    for i in range(5):
        client = random.choice(clients)
        date = (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
        
        # Создаем накладную и получаем её ID
        inv_id = execute_insert(db_path, 
            "INSERT INTO invoices (date, client, total_amount) VALUES (?, ?, 0)", (date, client))
        
        # Генерируем строки (3-5 товаров)
        num_lines = random.randint(3, 5)
        total_inv_amount = 0
        selected_products = random.sample(product_names, num_lines)
        
        for prod_name in selected_products:
            qty = random.randint(1, 10)
            price = products_dict[prod_name]
            amount = qty * price
            total_inv_amount += amount
            execute_query(db_path, 
                "INSERT INTO invoice_lines (invoice_id, product, quantity, price, amount) VALUES (?, ?, ?, ?, ?)",
                (inv_id, prod_name, qty, price, amount)
            )
        
        # Обновляем общую сумму накладной
        execute_query(db_path, "UPDATE invoices SET total_amount = ? WHERE id = ?", (total_inv_amount, inv_id))
    
    logger.info(f"[BeliefState][IMP:9][generate_mock_data][GENERATE] Сгенерировано 5 накладных [VALUE]")
    # END_BLOCK_GENERATE
# END_FUNCTION_generate_mock_data

# START_FUNCTION_get_invoices
# START_CONTRACT:
# PURPOSE: Получение всех накладных для Master-Grid.
# INPUTS:
# - str => db_path: Путь к БД
# OUTPUTS:
# - list - Список словарей для AG Grid
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def get_invoices(db_path: str) -> list:
    """
    Возвращает список всех накладных из БД.
    """
    # START_BLOCK_FETCH: [Получение данных]
    rows = fetch_query(db_path, "SELECT id, date, client, total_amount FROM invoices ORDER BY id DESC")
    result = [{"id": r[0], "date": r[1], "client": r[2], "total_amount": r[3]} for r in rows]
    logger.debug(f"[Logic][IMP:5][get_invoices][FETCH] Получено {len(result)} накладных [VALUE]")
    return result
    # END_BLOCK_FETCH
# END_FUNCTION_get_invoices

# START_FUNCTION_get_invoice_lines
# START_CONTRACT:
# PURPOSE: Получение строк конкретной накладной для Detail-Grid.
# INPUTS:
# - str => db_path: Путь к БД
# - int => inv_id: ID накладной
# OUTPUTS:
# - list - Список словарей для AG Grid
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def get_invoice_lines(db_path: str, inv_id: int) -> list:
    """
    Возвращает строки накладной по её ID.
    """
    # START_BLOCK_FETCH: [Получение данных]
    if inv_id is None:
        return []
    rows = fetch_query(db_path, 
        "SELECT id, product, quantity, price, amount FROM invoice_lines WHERE invoice_id = ?", (inv_id,))
    result = [{"id": r[0], "product": r[1], "quantity": r[2], "price": r[3], "amount": r[4]} for r in rows]
    logger.debug(f"[Logic][IMP:5][get_invoice_lines][FETCH] Получено {len(result)} строк для ID {inv_id} [VALUE]")
    return result
    # END_BLOCK_FETCH
# END_FUNCTION_get_invoice_lines

# START_FUNCTION_update_invoice_lines
# START_CONTRACT:
# PURPOSE: Сохранение изменений в строках накладной и пересчет суммы.
# INPUTS:
# - str => db_path: Путь к БД
# - int => inv_id: ID накладной
# - list => table_data: Данные из AG Grid
# OUTPUTS: None
# SIDE_EFFECTS: Обновляет invoice_lines и invoices.
# KEYWORDS: [PATTERN(6): Update; CONCEPT(8): Consistency]
# COMPLEXITY_SCORE: 7
# END_CONTRACT
def update_invoice_lines(db_path: str, inv_id: int, table_data: list):
    """
    Обновляет строки накладной в БД на основе данных из таблицы.
    Пересчитывает суммы строк и общую сумму накладной.
    """
    # START_BLOCK_UPDATE: [Обновление строк]
    if inv_id is None or not table_data:
        return

    products_dict = get_products()
    total_inv_amount = 0

    for row in table_data:
        prod_name = row.get("product")
        qty = float(row.get("quantity", 0))
        price = products_dict.get(prod_name, 0)
        amount = qty * price
        total_inv_amount += amount
        
        # Обновляем строку (предполагаем, что ID строки не меняется)
        execute_query(db_path, 
            "UPDATE invoice_lines SET product = ?, quantity = ?, price = ?, amount = ? WHERE id = ?",
            (prod_name, qty, price, amount, row.get("id"))
        )
    
    # Обновляем общую сумму накладной
    execute_query(db_path, "UPDATE invoices SET total_amount = ? WHERE id = ?", (total_inv_amount, inv_id))
    logger.info(f"[BeliefState][IMP:9][update_invoice_lines][UPDATE] Накладная {inv_id} обновлена. Новая сумма: {total_inv_amount} [VALUE]")
    # END_BLOCK_UPDATE
# END_FUNCTION_update_invoice_lines
