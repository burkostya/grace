# FILE: run_lesson_18.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Точка входа для запуска приложения Lesson 18 (Генератор параболы).
# SCOPE: Инициализация логирования, импорт контроллера и запуск Gradio.
# INPUT: Нет.
# OUTPUT: Запущенный веб-сервер Gradio.
# KEYWORDS: [DOMAIN(8): EntryPoint; CONCEPT(7): Startup; TECH(9): Gradio]
# LINKS: [USES_API(8): logging, gradio]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание точки входа с настройкой логирования и ленивым импортом.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Основная функция запуска приложения] => main
# END_MODULE_MAP
#
# START_USE_CASES:
# - [main]: System -> Start Application -> Gradio Server Running
# END_USE_CASES

import logging
import sys
import os

# START_FUNCTION_setup_logging
# START_CONTRACT:
# PURPOSE: Настройка логирования в файл и консоль.
# INPUTS: Нет
# OUTPUTS: Нет
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def setup_logging():
    """
    Настраивает логирование так, чтобы сообщения выводились в файл lesson_18/app_18.log
    и в стандартный поток вывода (stdout) для видимости в терминале.
    """
    log_file = "lesson_18/app_18.log"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.info(f"[System][IMP:10][run_lesson_18][setup_logging][IO] Логирование инициализировано. [SUCCESS]")
# END_FUNCTION_setup_logging

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE: Главная функция запуска.
# INPUTS: Нет
# OUTPUTS: Нет
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def main():
    """
    Основная точка входа. Использует ленивый импорт для ускорения инициализации
    и предотвращения ошибок окружения при запуске.
    """
    setup_logging()
    
    # START_BLOCK_LAZY_IMPORT: [Ленивый импорт тяжелых библиотек]
    try:
        from lesson_18.src.ui_controller import UIController
        logger = logging.getLogger(__name__)
        logger.info(f"[System][IMP:9][run_lesson_18][main][Flow] Импорт UIController выполнен. [SUCCESS]")
    except ImportError as e:
        print(f"CRITICAL ERROR: Could not import UIController. {e}")
        sys.exit(1)
    # END_BLOCK_LAZY_IMPORT

    # START_BLOCK_LAUNCH_UI: [Запуск интерфейса]
    try:
        controller = UIController()
        ui = controller.create_ui()
        
        logger.info(f"[BeliefState][IMP:10][run_lesson_18][main][Flow] Запуск Gradio сервера... [VALUE]")
        ui.launch(inbrowser=True, share=False)
    except KeyboardInterrupt:
        logger.info(f"[System][IMP:10][run_lesson_18][main][Flow] Приложение остановлено пользователем. [INFO]")
    except Exception as e:
        logger.critical(f"[System][IMP:10][run_lesson_18][main][Exception] Критическая ошибка при запуске: {e}. [FATAL]")
    # END_BLOCK_LAUNCH_UI

if __name__ == "__main__":
    main()
# END_FUNCTION_main
