# FILE: lesson_19/tests/test_callbacks.py
# VERSION: 1.0.1
# START_MODULE_CONTRACT:
# PURPOSE: Тестирование Dash callbacks через логику функций.
# SCOPE: Проверка логики обновления гридов и графиков.
# INPUT: Mock данные и вызовы функций.
# OUTPUT: Результаты тестов.
# KEYWORDS: [DOMAIN(8): Testing; CONCEPT(7): Callbacks; TECH(9): Dash]
# END_MODULE_CONTRACT

import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Добавляем корень проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from lesson_19.app import update_detail_logic, toggle_chart_logic, update_master_logic

# START_FUNCTION_test_update_detail_logic
def test_update_detail_logic():
    """
    Тестирует логику обновления детального грида.
    """
    # Эмулируем выбор строки
    selected_rows = [{"id": 1}]
    db_path = "dummy.db"
    
    with patch("lesson_19.app.get_invoice_lines") as mock_get_lines:
        mock_get_lines.return_value = [{"product": "Test", "quantity": 1, "price": 100, "amount": 100}]
        
        # Вызываем логику напрямую
        res_rows, res_header, res_disabled = update_detail_logic(selected_rows, db_path)
        
        assert len(res_rows) == 1
        assert res_header == "Накладная №1"
        assert res_disabled is False
        mock_get_lines.assert_called_once_with(db_path, 1)
# END_FUNCTION_test_update_detail_logic

# START_FUNCTION_test_toggle_chart_logic
def test_toggle_chart_logic():
    """
    Тестирует логику переключения видимости графика.
    """
    # Тест: скрыть
    res = toggle_chart_logic(1, {"display": "block"})
    assert res == {"display": "none"}
    
    # Тест: показать
    res = toggle_chart_logic(2, {"display": "none"})
    assert res == {"display": "block"}
# END_FUNCTION_test_toggle_chart_logic

# START_FUNCTION_test_update_master_logic
def test_update_master_logic():
    """
    Тестирует логику обновления мастер-грида.
    """
    db_path = "dummy.db"
    with patch("lesson_19.app.get_invoices") as mock_get_inv, \
         patch("lesson_19.app.generate_mock_data") as mock_gen:
        
        mock_get_inv.return_value = [{"id": 1, "total_amount": 100}]
        
        # Тест с генерацией
        rows, fig = update_master_logic("btn-generate", db_path)
        assert len(rows) == 1
        mock_gen.assert_called_once_with(db_path)
        
        # Тест без генерации
        mock_gen.reset_mock()
        rows, fig = update_master_logic(None, db_path)
        assert len(rows) == 1
        mock_gen.assert_not_called()
# END_FUNCTION_test_update_master_logic
