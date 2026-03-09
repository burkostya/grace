# FILE:run_lesson_9.py
# VERSION:1.1.0
# START_MODULE_CONTRACT:
# PURPOSE:Точка входа для запуска веб-интерфейса приложения Lesson 9.
# SCOPE: Инициализация БД и запуск Gradio сервера с обработкой ошибок.
# INPUT:Нет.
# OUTPUT: Запущенный веб-сервер.
# KEYWORDS:[DOMAIN(8): EntryPoint; CONCEPT(7): Server; TECH(9): gradio]
# LINKS:[USES_MODULE(9): ui_controller, database_manager]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.1.0 - Переход на паттерн запуска из v8: отложенный импорт, обработка KeyboardInterrupt, inbrowser=True.]
# PREV_CHANGE_SUMMARY: [v1.0.0 - Первичное создание скрипта.]
# END_CHANGE_SUMMARY

import logging
import os
import sys

# Настройка логгера для LDD 2.0
LOG_FILE = os.path.join(os.path.dirname(__file__), "lesson_9", "app_9.log")
logger = logging.getLogger("lesson_9")
if not logger.handlers:
    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE:Инициализация ресурсов и запуск UI с защитой от сбоев.
# INPUTS: None
# OUTPUTS: None
# SIDE_EFFECTS: Запуск блокирующего процесса веб-сервера.
# KEYWORDS:[PATTERN(7): Bootstrapper; CONCEPT(8): Runtime]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def main():
    """
    Функция выполняет предварительную подготовку (инициализация БД) 
    и запускает сервер Gradio. Использует отложенный импорт для 
    предотвращения проблем с окружением при инициализации.
    """
    logger.info(f"[System][IMP:10][main][START][Success] Запуск приложения Lesson 9... [SUCCESS]")
    
    try:
        # START_BLOCK_INIT: [Инициализация БД и отложенный импорт]
        from lesson_9.src.database_manager import init_db
        from lesson_9.src.ui_controller import create_ui
        
        init_db()
        # END_BLOCK_INIT

        # START_BLOCK_LAUNCH: [Запуск интерфейса]
        print("\n" + "="*60)
        print("Генератор параболы Lesson 9")
        print("="*60)
        print("\nПриложение запускается в браузере...")
        
        ui = create_ui()
        ui.launch(
            server_name="127.0.0.1", 
            server_port=7860, 
            share=False,
            inbrowser=True
        )
        # END_BLOCK_LAUNCH
        
    except KeyboardInterrupt:
        logger.info("[System][IMP:8][main][STOP][User] Приложение остановлено пользователем. [INFO]")
        print("\nПриложение остановлено")
        
    except Exception as e:
        logger.critical(f"[System][IMP:10][main][CRASH][Error] Критическая ошибка: {e} [FATAL]")
        print(f"\nКритическая ошибка: {e}")
        sys.exit(1)
# END_FUNCTION_main

if __name__ == "__main__":
    main()
