# FILE: run_lesson_v6.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Точка входа для запуска UI Lesson 6.
# SCOPE: Инициализация и запуск Gradio сервера.
# INPUT: Отсутствует (запускается как скрипт).
# OUTPUT: Запуск веб-сервера Gradio.
# KEYWORDS:[DOMAIN(8): ApplicationEntry; CONCEPT(7): GradioServer; TECH(9): WebUI]
# LINKS:[USES_API(8): ui_controller]
# END_MODULE_CONTRACT
#
# START_INVARIANTS:
# - Скрипт ВСЕГДА запускает Gradio сервер на порту 7860.
# END_INVARIANTS
#
# START_RATIONALE:
# Q: Почему отдельный файл запуска, а не в ui_controller?
# A: Разделение логики контроллера и точки входа соответствует принципу разделения ответственности.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание точки входа для запуска UI.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Главная точка входа приложения] => main
# END_MODULE_MAP
#
# START_USE_CASES:
# -[main]: User (Startup) -> LaunchApplication -> GradioServerRunning
# END_USE_CASES

import logging
import sys

# Импорт модулей проекта
from lesson_v6 import LOG_PATH
from lesson_v6.src.ui_controller import create_interface

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE: Главная точка входа - запуск Gradio сервера.
# INPUTS: Отсутствуют.
# OUTPUTS: 
# - None
# SIDE_EFFECTS: Запускает веб-сервер Gradio.
# KEYWORDS:[PATTERN(6): EntryPoint; CONCEPT(8): ServerStartup]
# END_CONTRACT
def main():
    """Запускает приложение Lesson 6."""
    
    # START_BLOCK_CREATE_INTERFACE: [Создание интерфейса]
    try:
        interface = create_interface()
        logger.info(f"[InterfaceCreation][IMP:8][main][CREATE_INTERFACE][ReturnData] Интерфейс успешно создан [VALUE]")
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][main][CREATE_INTERFACE][ExceptionEnrichment] Ошибка создания интерфейса. Err: {e} [FATAL]")
        sys.exit(1)
    # END_BLOCK_CREATE_INTERFACE

    # START_BLOCK_LAUNCH_SERVER: [Запуск сервера]
    try:
        logger.info(f"[ServerStartup][IMP:9][main][LAUNCH_SERVER][ReturnData] Запуск Gradio сервера на порту 7860 [VALUE]")
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True
        )
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][main][LAUNCH_SERVER][ExceptionEnrichment] Ошибка запуска сервера. Err: {e} [FATAL]")
        sys.exit(1)
    # END_BLOCK_LAUNCH_SERVER
# END_FUNCTION_main

if __name__ == '__main__':
    main()
