# FILE:lesson_21/handlers.py
# VERSION:1.2.0
# START_MODULE_CONTRACT:
# PURPOSE:Чистая бизнес-логика для ERP-прототипа (Flux Pattern).
# SCOPE: Поиск товаров, управление накладными и их строками, пересчет сумм.
# END_MODULE_CONTRACT

import logging
from datetime import datetime
from lesson_21 import db_manager

logger = logging.getLogger("lesson_21.handlers")

def search_items(keyword: str) -> list:
    conn = db_manager.get_connection(db_manager.DB_PATH)
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM items WHERE name LIKE ? OR sku LIKE ?"
        param = f"%{keyword}%"
        cursor.execute(query, (param, param))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def add_line_to_invoice(inv_id: int, item_id: int, qty: int) -> bool:
    conn = db_manager.get_connection(db_manager.DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT price FROM items WHERE id = ?", (item_id,))
        item = cursor.fetchone()
        if not item: return False
        
        price = item['price']
        line_sum = price * qty
        
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute(
            "INSERT INTO invoice_lines (invoice_id, item_id, qty, price, line_sum) VALUES (?, ?, ?, ?, ?)",
            (inv_id, item_id, qty, price, line_sum)
        )
        cursor.execute(
            "UPDATE invoices SET total_sum = (SELECT SUM(line_sum) FROM invoice_lines WHERE invoice_id = ?) WHERE id = ?",
            (inv_id, inv_id)
        )
        conn.commit()
        logger.info(f"[LDD][IMP:9] Added item {item_id} to invoice {inv_id}")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"[LDD][IMP:10] Error adding line: {e}")
        return False
    finally:
        conn.close()

def delete_line(line_id: int) -> bool:
    """
    Удаляет строку накладной и пересчитывает итоговую сумму накладной.
    """
    conn = db_manager.get_connection(db_manager.DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT invoice_id FROM invoice_lines WHERE id = ?", (line_id,))
        row = cursor.fetchone()
        if not row: return False
        inv_id = row['invoice_id']
        
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute("DELETE FROM invoice_lines WHERE id = ?", (line_id,))
        cursor.execute(
            "UPDATE invoices SET total_sum = COALESCE((SELECT SUM(line_sum) FROM invoice_lines WHERE invoice_id = ?), 0) WHERE id = ?",
            (inv_id, inv_id)
        )
        conn.commit()
        logger.info(f"[LDD][IMP:9] Deleted line {line_id} from invoice {inv_id}")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"[LDD][IMP:10] Error deleting line: {e}")
        return False
    finally:
        conn.close()

def update_line_qty(line_id: int, new_qty: int) -> bool:
    """
    Обновляет количество в строке и пересчитывает итоги.
    """
    conn = db_manager.get_connection(db_manager.DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT invoice_id, price FROM invoice_lines WHERE id = ?", (line_id,))
        line = cursor.fetchone()
        if not line: return False
        
        inv_id = line['invoice_id']
        price = line['price']
        new_line_sum = price * new_qty
        
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute(
            "UPDATE invoice_lines SET qty = ?, line_sum = ? WHERE id = ?",
            (new_qty, new_line_sum, line_id)
        )
        cursor.execute(
            "UPDATE invoices SET total_sum = (SELECT SUM(line_sum) FROM invoice_lines WHERE invoice_id = ?) WHERE id = ?",
            (inv_id, inv_id)
        )
        conn.commit()
        logger.info(f"[LDD][IMP:9] Updated line {line_id} qty to {new_qty}")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"[LDD][IMP:10] Error updating qty: {e}")
        return False
    finally:
        conn.close()

def get_invoices() -> list:
    conn = db_manager.get_connection(db_manager.DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM invoices ORDER BY date DESC")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()

def get_invoice_lines(inv_id: int) -> list:
    conn = db_manager.get_connection(db_manager.DB_PATH)
    try:
        cursor = conn.cursor()
        query = """
            SELECT il.id as line_id, i.sku, i.name, il.qty, il.price, il.line_sum
            FROM invoice_lines il
            JOIN items i ON il.item_id = i.id
            WHERE il.invoice_id = ?
        """
        cursor.execute(query, (inv_id,))
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()

def create_demo_invoice(client_name: str = "Demo Client") -> int:
    conn = db_manager.get_connection(db_manager.DB_PATH)
    try:
        cursor = conn.cursor()
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute(
            "INSERT INTO invoices (date, client_name, total_sum) VALUES (?, ?, ?)",
            (date_str, client_name, 0.0)
        )
        new_id = cursor.lastrowid
        conn.commit()
        return new_id
    finally:
        conn.close()
