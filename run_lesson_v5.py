# FILE:run_lesson_v5.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Точка входа для запуска Gradio интерфейса урока lesson_v5.
# SCOPE:Инициализация и запуск веб-сервера UI.
# INPUT:Нет.
# OUTPUT:Запущенный сервер Gradio.
# KEYWORDS:[DOMAIN(8): UI; CONCEPT(7): EntryPoint; TECH(9): Gradio]
# LINKS:[USES_API(8): gradio; CALLS_FUNCTION(9): lesson_v5.src.ui_controller.create_ui]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание скрипта запуска UI в корне проекта.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Запускает UI сервер] => main
# END_MODULE_MAP

import logging
from lesson_v5.src.ui_controller import create_ui

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s][IMP:9][RUNNER] %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Запускает интерфейс Gradio для lesson_v5."""
    # START_BLOCK_LAUNCH_UI: [Запуск сервера]
    logger.info("[BeliefState][IMP:9][RUNNER][LAUNCH_UI][Start] Запуск Gradio сервера для lesson_v5... [VALUE]")
    try:
        demo = create_ui()
        demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][RUNNER][LAUNCH_UI][Exception] Ошибка при запуске сервера: {e} [FATAL]")
    # END_BLOCK_LAUNCH_UI

if __name__ == "__main__":
    main()
