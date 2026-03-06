# FILE: lesson_v6/__init__.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Инициализация пакета Lesson 6.
# SCOPE: Определение корневых путей проекта.
# INPUT: Отсутствует.
# OUTPUT: Константы путей к директориям и файлам.
# KEYWORDS:[DOMAIN(8): ProjectStructure; CONCEPT(7): PathManagement]
# END_MODULE_CONTRACT

import os

# START_BLOCK_PATH_CONSTANTS: [Определение путей к директориям и файлам]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
TESTS_DIR = os.path.join(BASE_DIR, "tests")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
DB_PATH = os.path.join(BASE_DIR, "parabola.db")
LOG_PATH = os.path.join(BASE_DIR, "app_v6.log")
# END_BLOCK_PATH_CONSTANTS
