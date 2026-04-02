# FILE: run_lesson_22.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Главная точка входа приложения Lesson 22.
# SCOPE: Настройка логирования и запуск Gradio сервера.
# INPUT: Отсутствует (аргументы командной строки не требуются).
# OUTPUT: Запущенный веб-интерфейс.
# KEYWORDS:[DOMAIN(8): EntryPoint; CONCEPT(7): ApplicationRoot; TECH(9): Main]
# LINKS:[USES_API(8): logging, gradio]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется отложенный импорт (Lazy Import)?
# A: Это ускоряет первичный запуск скрипта и предотвращает проблемы инициализации до настройки логирования.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание лаунчера run_lesson_22.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Конфигурирует окружение и запускает UI] => main
# END_MODULE_MAP

import logging
import os
import sys


# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE: Инициализирует логирование и запускает интерфейс.
# INPUTS: Нет.
# OUTPUTS: Нет.
# SIDE_EFFECTS: Запуск веб-сервера.
# KEYWORDS:[PATTERN(6): Startup; CONCEPT(8): Initialization]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def main():
    """
    Основная функция запуска. Настраивает вывод логов в файл lesson_22/app_22.log
    и в stdout. Затем импортирует и запускает Gradio.
    """
    # START_BLOCK_SETUP_LOGGING: [Настройка изолированного логирования]
    log_dir = "lesson_22"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "app_22.log")

    # Сброс существующих логов (для чистоты эксперимента)
    if os.path.exists(log_file):
        os.remove(log_file)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    logger = logging.getLogger(__name__)
    logger.info(
        f"[System][IMP:10][main][SETUP_LOGGING][Start] Запуск приложения Lesson 22. [INFO]"
    )
    # END_BLOCK_SETUP_LOGGING

    # START_BLOCK_LAUNCH_UI: [Ленивый импорт и старт сервера]
    try:
        from lesson_22.ui import create_ui

        ui_app = create_ui()

        logger.info(
            f"[BeliefState][IMP:9][main][LAUNCH_UI][Ready] Сервер Gradio готов к работе. [VALUE]"
        )

        # Запуск интерфейса
        # inbrowser=True: Автоматически открывает вкладку в браузере
        ui_app.launch(inbrowser=True)

    except KeyboardInterrupt:
        logger.info(
            f"[System][IMP:8][main][LAUNCH_UI][Stop] Приложение остановлено пользователем. [STOP]"
        )
    except Exception as e:
        logger.critical(
            f"[SystemError][IMP:10][main][LAUNCH_UI][Fatal] Непредвиденная ошибка при запуске: {e} [FATAL]"
        )
    # END_BLOCK_LAUNCH_UI


# END_FUNCTION_main

if __name__ == "__main__":
    main()
# END_FUNCTION_main
