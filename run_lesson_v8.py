# FILE: run_lesson_v8.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Точка запуска Gradio сервера для приложения lesson_v8.
# SCOPE: Инициализация и запуск веб-интерфейса генератора параболы.
# INPUT: Отсутствует (скрипт запускается без аргументов).
# OUTPUT: Запущенный Gradio сервер (в браузере пользователя).
# KEYWORDS:[DOMAIN(9): ApplicationEntry; CONCEPT(8): ServerStartup; TECH(9): Gradio]
# LINKS:[CALLS(8): lesson_v8.src.ui_controller.create_interface]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание точки запуска приложения.]
# END_CHANGE_SUMMARY

"""
Точка запуска приложения lesson_v8 для генерации параболы.

Скрипт инициализирует и запускает Gradio сервер с интерактивным интерфейсом
для генерации и визуализации точек параболы y = ax^2 + c.
"""

import logging
import os

# Настройка логирования в файл
LOG_FILE = os.path.join(os.path.dirname(__file__), "lesson_v8", "app_v8.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """
    Главная функция запуска приложения.
    Создает Gradio интерфейс и запускает сервер.
    """
    logger.info("[ApplicationStarted][IMP:9][main][STARTUP][Application] Запуск приложения lesson_v8 [INFO]")
    
    try:
        # Импорт контроллера UI
        from lesson_v8.src.ui_controller import create_interface
        
        # Создание интерфейса
        logger.info("[CreatingInterface][IMP:8][main][CREATE_INTERFACE][UIOperation] Создание Gradio интерфейса [INFO]")
        interface = create_interface()
        
        # Запуск сервера
        logger.info("[LaunchingServer][IMP:9][main][LAUNCH_SERVER][ServerOperation] Запуск Gradio сервера [INFO]")
        print("\n" + "="*60)
        print("Генератор параболы lesson_v8")
        print("="*60)
        print("\nПриложение запускается в браузере...")
        print("Для остановки сервера нажмите Ctrl+C в терминале\n")
        
        interface.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            inbrowser=True
        )
        
    except KeyboardInterrupt:
        logger.info("[ApplicationStopped][IMP:8][main][SHUTDOWN][Application] Приложение остановлено пользователем [INFO]")
        print("\nПриложение остановлено")
        
    except Exception as e:
        logger.critical(f"[ApplicationError][IMP:10][main][CRASH][ExceptionEnrichment] Критическая ошибка приложения. Err: {e} [FATAL]")
        print(f"\nКритическая ошибка: {e}")
        raise


if __name__ == '__main__':
    main()
