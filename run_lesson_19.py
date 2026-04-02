# FILE: run_lesson_19.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Точка входа для запуска ERP-прототипа Lesson 19.
# SCOPE: Инициализация окружения и запуск Dash сервера.
# INPUT: Командная строка.
# OUTPUT: Работающий веб-интерфейс.
# KEYWORDS: [DOMAIN(8): EntryPoint; CONCEPT(7): Launcher; TECH(9): Dash]
# END_MODULE_CONTRACT

import logging
import sys
import os

# Настройка логирования в консоль и файл
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("lesson_19/app_19.log", encoding='utf-8')
    ]
)
logger = logging.getLogger("Launcher")

def main():
    """
    Основная функция запуска. Использует отложенный импорт для стабильности.
    """
    logger.info("[Launcher][IMP:8][main][START] Запуск Lesson 19 ERP Prototype...")
    
    try:
        # Отложенный импорт
        from lesson_19.app import create_app
        
        app = create_app()
        logger.info("[Launcher][IMP:9][main][RUN] Сервер Dash запускается на http://127.0.0.1:8050")
        
        # Запуск сервера
        app.run(debug=False, port=8050, host='127.0.0.1')
        
    except KeyboardInterrupt:
        logger.info("[Launcher][IMP:7][main][STOP] Сервер остановлен пользователем.")
    except Exception as e:
        logger.critical(f"[Launcher][IMP:10][main][ERROR] Критическая ошибка при запуске: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
