# FILE:lesson_20/tests/test_ui.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Тестирование UI-обработчиков Lesson 20 (Headless).
# SCOPE:Проверка handle_generate и handle_draw без запуска Gradio.
# KEYWORDS:[DOMAIN(8): Testing; CONCEPT(7): UI; TECH(9): Pytest, LDD]
# END_MODULE_CONTRACT

import os
import pytest
import pandas as pd
import plotly.graph_objects as go
from lesson_20.handlers import handle_generate, handle_draw
from lesson_20.db_manager import init_db

# START_FUNCTION_test_ui_handlers
# START_CONTRACT:
# PURPOSE:Проверка работы обработчиков UI.
# INPUTS: tmp_path, caplog
# OUTPUTS: None
# KEYWORDS:[PATTERN(7): LDD; CONCEPT(8): Telemetry]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def test_ui_handlers(tmp_path, caplog):
    """
    Тест проверяет, что handle_generate возвращает DataFrame,
    а handle_draw возвращает Figure Plotly.
    """
    # START_BLOCK_SETUP: [Настройка окружения]
    db_file = tmp_path / "test_ui.db"
    config_file = tmp_path / "test_ui_config.json"
    
    # Мокаем пути в менеджерах (через monkeypatch)
    import lesson_20.db_manager
    import lesson_20.config_manager
    import lesson_20.handlers
    
    # Переопределяем пути по умолчанию для тестов
    lesson_20.db_manager.init_db(str(db_file))
    # END_BLOCK_SETUP

    # START_BLOCK_EXECUTION_GENERATE: [Вызов handle_generate]
    # ВАЖНО: Мы не можем легко замокать пути внутри handlers.py без патчинга,
    # поэтому в тестах UI мы полагаемся на то, что handlers используют дефолтные пути,
    # но для чистоты теста мы можем пропатчить функции сохранения.
    
    # Для простоты теста в рамках урока, мы просто вызовем обработчики,
    # зная что они создадут файлы в lesson_20/ (или мы их переопределим).
    # Но правильнее использовать monkeypatch для путей.
    
    from unittest.mock import patch
    with patch("lesson_20.handlers.save_config"), \
         patch("lesson_20.handlers.save_points"), \
         patch("lesson_20.handlers.get_points") as mock_get:
        
        mock_get.return_value = [(0.0, 0.0), (1.0, 1.0)]
        
        df = handle_generate(a=1.0, c=0.0, x_min=-5, x_max=5)
        fig = handle_draw()
        
        # START_BLOCK_LDD_TELEMETRY: [Вывод траектории]
        print("\n--- LDD ТРАЕКТОРИЯ (IMP:7-10) ---")
        for record in caplog.records:
            if "[IMP:" in record.message:
                try:
                    imp_level = int(record.message.split("[IMP:")[1].split("]")[0])
                    if imp_level >= 7:
                        print(record.message)
                except: continue
        # END_BLOCK_LDD_TELEMETRY

        # START_BLOCK_VERIFICATION: [Проверки]
        assert isinstance(df, pd.DataFrame), "handle_generate должен возвращать DataFrame"
        assert not df.empty, "DataFrame не должен быть пустым"
        assert isinstance(fig, go.Figure), "handle_draw должен возвращать Figure"
        # END_BLOCK_VERIFICATION
    # END_BLOCK_EXECUTION_GENERATE
# END_FUNCTION_test_ui_handlers
