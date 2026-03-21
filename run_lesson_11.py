# FILE:run_lesson_11.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Точка входа для запуска Gradio сервера 11-го урока.
# SCOPE:Инициализация базы данных и запуск веб-интерфейса.
# INPUT:Отсутствует (параметры берутся из конфигурации).
# OUTPUT:Запущенный процесс Gradio сервера.
# KEYWORDS:[DOMAIN(9): WebInterface; CONCEPT(8): EntryPoint; TECH(9): Gradio]
# LINKS:[USES_API(9): lesson_11.src.ui_controller; USES_API(8): lesson_11.src.database_manager]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется ленивый импорт внутри main?
# A: Для предотвращения ошибок инициализации при отсутствии зависимостей в окружении до старта логики.
# Q: Почему логирование настраивается вручную?
# A: Для обеспечения соответствия стандарту LDD 2.0 и записи в специфичный файл lesson_11/app_11.log.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание скрипта запуска с поддержкой LDD 2.0 и инициализацией БД.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Основная функция запуска приложения] => main
# END_MODULE_MAP
#
# START_USE_CASES:
# - [main]: User -> Run Script -> Gradio Server Started
# END_USE_CASES

import os
import logging
import sys

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE:Инициализирует окружение, БД и запускает Gradio интерфейс.
# INPUTS: Нет
# OUTPUTS: Нет
# SIDE_EFFECTS: Создает файл лога, инициализирует SQLite БД, запускает HTTP сервер.
# KEYWORDS:[PATTERN(9): Launcher; CONCEPT(8): Initialization]
# COMPLEXITY_SCORE: 6[Средняя сложность из-за настройки логгера и обработки прерываний.]
# END_CONTRACT
def main():
    """
    Основная управляющая функция, которая подготавливает среду выполнения для 11-го урока.
    Она настраивает систему логирования в соответствии с протоколом LDD 2.0,
    выполняет инициализацию таблиц базы данных через database_manager
    и запускает веб-интерфейс Gradio через ui_controller.
    Используется блок try-except для корректного завершения работы при прерывании пользователем.
    """
    
    # START_BLOCK_SETUP_LOGGING: [Настройка LDD 2.0 логирования]
    log_dir = "lesson_11"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_file = os.path.join(log_dir, "app_11.log")
    
    # Настройка корневого логгера для всех модулей
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger("lesson_11_launcher")
    
    logger.info(f"[IMP:9][main][SETUP_LOGGING][IO] Логирование инициализировано в {log_file} [SUCCESS]")
    # END_BLOCK_SETUP_LOGGING

    try:
        # START_BLOCK_LAZY_IMPORTS: [Отложенный импорт тяжелых модулей]
        logger.info("[IMP:5][main][LAZY_IMPORTS][Flow] Загрузка модулей приложения... [INFO]")
        from lesson_11.src.database_manager import init_db
        from lesson_11.src.ui_controller import create_ui
        # END_BLOCK_LAZY_IMPORTS

        # START_BLOCK_INIT_DATABASE: [Инициализация БД]
        logger.info("[IMP:8][main][INIT_DATABASE][IO] Инициализация базы данных... [PROCESS]")
        init_db()
        logger.info("[IMP:9][main][INIT_DATABASE][AI_Belief] База данных готова к работе. [SUCCESS]")
        # END_BLOCK_INIT_DATABASE

        # START_BLOCK_LAUNCH_UI: [Запуск Gradio интерфейса]
        logger.info("[IMP:10][main][LAUNCH_UI][BusinessLogic] Запуск Gradio сервера... [GOAL]")
        ui = create_ui()
        ui.launch(inbrowser=True, share=False)
        # END_BLOCK_LAUNCH_UI

    except KeyboardInterrupt:
        logger.warning("[IMP:7][main][EXCEPTION][Flow] Работа прервана пользователем (KeyboardInterrupt) [STOP]")
    except Exception as e:
        logger.critical(f"[IMP:10][main][EXCEPTION][AI_Belief] Критическая ошибка при запуске: {e} [FATAL]")
        raise

# END_FUNCTION_main

if __name__ == "__main__":
    main()
