# FILE:run_lesson_20.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Точка входа для запуска приложения Lesson 20.
# SCOPE:Настройка логирования, инициализация БД и запуск Gradio.
# INPUT:Нет.
# OUTPUT:Запущенный сервер Gradio.
# KEYWORDS:[DOMAIN(8): EntryPoint; CONCEPT(7): Launcher; TECH(9): Gradio, Logging]
# LINKS:[USES_API(8): logging, gradio]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется Lazy Import?
# A: Это предотвращает сбои при инициализации, если окружение еще не полностью готово.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание лаунчера приложения.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Основная функция запуска] => main
# END_MODULE_MAP

import logging
import os
import sys

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE:Настройка окружения и запуск сервера Gradio.
# INPUTS: Нет
# OUTPUTS: Нет
# SIDE_EFFECTS: Запуск HTTP сервера, создание лог-файла.
# KEYWORDS:[PATTERN(6): Launcher]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def main():
    """
    Основная функция запуска приложения. Настраивает логирование в файл и консоль,
    инициализирует базу данных и запускает интерфейс Gradio.
    """
    # START_BLOCK_SETUP_LOGGING: [Настройка логирования LDD 2.0]
    log_path = "lesson_20/app_20.log"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    logger = logging.getLogger("lesson_20")
    logger.setLevel(logging.DEBUG)
    
    # Формат лога LDD 2.0
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Файловый хендлер
    fh = logging.FileHandler(log_path, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    # Консольный хендлер
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    logger.info(f"[Launcher][IMP:8][main][SETUP_LOGGING][Success] Логирование настроено: {log_path}. [SUCCESS]")
    # END_BLOCK_SETUP_LOGGING
    
    # START_BLOCK_LAZY_IMPORTS: [Отложенный импорт модулей]
    try:
        from lesson_20.db_manager import init_db
        from lesson_20.app import create_app
        logger.info(f"[Launcher][IMP:7][main][LAZY_IMPORTS][Success] Модули импортированы. [INFO]")
    except ImportError as e:
        logger.critical(f"[Launcher][IMP:10][main][LAZY_IMPORTS][Error] Ошибка импорта: {e}. [FATAL]")
        return
    # END_BLOCK_LAZY_IMPORTS
    
    # START_BLOCK_INIT_DB: [Инициализация БД]
    init_db()
    logger.info(f"[Launcher][IMP:8][main][INIT_DB][Success] БД инициализирована. [SUCCESS]")
    # END_BLOCK_INIT_DB
    
    # START_BLOCK_LAUNCH_APP: [Запуск Gradio]
    try:
        app = create_app()
        logger.info(f"[Launcher][IMP:9][main][LAUNCH_APP][Status] Запуск сервера Gradio... [VALUE]")
        app.launch(inbrowser=True, share=False)
    except KeyboardInterrupt:
        logger.info(f"[Launcher][IMP:8][main][LAUNCH_APP][Status] Сервер остановлен пользователем. [INFO]")
    except Exception as e:
        logger.error(f"[Launcher][IMP:10][main][LAUNCH_APP][Error] Ошибка запуска: {e}. [FATAL]")
    # END_BLOCK_LAUNCH_APP

if __name__ == "__main__":
    main()
# END_FUNCTION_main
