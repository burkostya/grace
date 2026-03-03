# FILE: run_lesson.py
# VERSION: 1.0.0
# PURPOSE: Скрипт для корректного запуска приложения lesson_v2 из корня проекта.

import sys
import os

# Добавляем текущую директорию в путь поиска модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from lesson_v2.src.main import launch_app
    print("Запуск Parabola Pro из lesson_v2...")
    demo = launch_app()
    demo.launch()
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Убедитесь, что вы запускаете скрипт из корня проекта.")
except Exception as e:
    print(f"Произошла ошибка при запуске: {e}")
