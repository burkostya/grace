# FILE:run_lesson_12.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Точка входа для запуска приложения Dash (Lesson 12).
# SCOPE: Поддержка Debug и Prod (Waitress) режимов.
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.1 - Исправление семантической разметки: добавлены MODULE_MAP, USE_CASES и контракты.]
# PREV_CHANGE_SUMMARY: [v1.0.0 - Создание лончера приложения.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Запуск сервера Dash/Waitress] => main
# END_MODULE_MAP
#
# START_USE_CASES:
# - [main]: User -> CLIArgs -> ServerStarted
# END_USE_CASES

import sys
import os

# Добавляем текущую директорию в путь для корректных импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# START_FUNCTION_main
# START_CONTRACT:
# PURPOSE: Инициализация и запуск веб-сервера.
# INPUTS: None (sys.argv)
# OUTPUTS: None
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def main():
    """
    Функция инициализирует приложение Dash и запускает его либо во встроенном
    отладочном сервере, либо через промышленный сервер Waitress, если передан флаг --prod.
    """
    # START_BLOCK_INIT: [Инициализация и выбор режима]
    # Отложенный импорт для ускорения инициализации и предотвращения ошибок окружения
    from lesson_12.app import app, server
    
    port = 8050
    
    if "--prod" in sys.argv:
        from waitress import serve
        print(f"Starting PRODUCTION server (Waitress) on http://0.0.0.0:{port}")
        # threads=8 для обеспечения многопоточности на Windows
        serve(server, host="0.0.0.0", port=port, threads=8)
    else:
        print(f"Starting DEVELOPMENT server (Dash Debug) on http://127.0.0.1:{port}")
        app.run(debug=True, port=port)
    # END_BLOCK_INIT

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
        sys.exit(0)
# END_FUNCTION_main
