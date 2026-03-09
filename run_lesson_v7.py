# FILE: run_lesson_v7.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Точка запуска Gradio сервера для приложения lesson_v7.
# SCOPE: Инициализация логирования, создание интерфейса и запуск сервера.
# INPUT: Отсутствует (запуск из командной строки).
# OUTPUT: Запуск Gradio сервера в браузере.
# KEYWORDS:[DOMAIN(6): EntryPoint; CONCEPT(5): ServerStartup; TECH(9): Gradio]
# LINKS:[CALLS(10): ui_controller.create_gradio_interface]
# END_MODULE_CONTRACT
#
# START_INVARIANTS:
# - Сервер ВСЕГДА запускается на порту 7860 (или следующем доступном).
# - При успешном запуске выводится URL интерфейса в консоль.
# END_INVARIANTS
#
# START_RATIONALE:
# Q: Почему отдельный файл запуска в корне проекта?
# A: Это обеспечивает удобный доступ к приложению из любого места и соответствует паттерну "Entry Point" для учебных проектов.
# Q: Почему используется share=False?
# A: share=False обеспечивает локальный доступ без создания публичной ссылки, что безопаснее для учебных целей.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание точки запуска приложения.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Главная функция: инициализация и запуск Gradio сервера] => main
# END_MODULE_MAP
#
# START_USE_CASES:
# -[main]: User (CommandLine) -> StartApplication -> GradioServerRunning
# END_USE_CASES

import logging
from pathlib import Path

# Импорт контроллера UI
from lesson_v7.src.ui_controller import create_gradio_interface

# Настройка логирования
LOG_FILE = Path(__file__).parent / "lesson_v7" / "app_v7.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE: Главная функция: инициализация и запуск Gradio сервера.
# INPUTS: 
# - Нет
# OUTPUTS: 
# - None (бесконечный цикл сервера)
# SIDE_EFFECTS: Запускает Gradio сервер и открывает браузер.
# KEYWORDS:[PATTERN(9): ServerStartup; CONCEPT(10): ApplicationEntry]
# END_CONTRACT
def main():
    """Главная функция запуска приложения."""
    
    # START_BLOCK_LOG_STARTUP: [Логирование запуска]
    logger.info("=" * 60)
    logger.info("[AppStart][IMP:10][main][LOG_STARTUP][Startup] Запуск приложения Lesson v7 [INFO]")
    logger.info("=" * 60)
    # END_BLOCK_LOG_STARTUP
    
    # START_BLOCK_CREATE_INTERFACE: [Создание интерфейса]
    try:
        logger.info(f"[AppStart][IMP:7][main][CREATE_INTERFACE][InterfaceInit] Создание Gradio интерфейса [INFO]")
        interface = create_gradio_interface()
        logger.info(f"[BeliefState][IMP:9][main][CREATE_INTERFACE][InterfaceReady] Интерфейс успешно создан [SUCCESS]")
    except Exception as e:
        logger.critical(f"[AppStart][IMP:10][main][CREATE_INTERFACE][ExceptionEnrichment] Критическая ошибка при создании интерфейса. Err: {e} [FATAL]")
        return
    # END_BLOCK_CREATE_INTERFACE
    
    # START_BLOCK_LAUNCH_SERVER: [Запуск сервера]
    try:
        logger.info(f"[AppStart][IMP:7][main][LAUNCH_SERVER][ServerLaunch] Запуск Gradio сервера [INFO]")
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True
        )
    except Exception as e:
        logger.critical(f"[AppStart][IMP:10][main][LAUNCH_SERVER][ExceptionEnrichment] Критическая ошибка при запуске сервера. Err: {e} [FATAL]")
    # END_BLOCK_LAUNCH_SERVER
# END_FUNCTION_main

if __name__ == "__main__":
    main()
