# FILE:concat_folder.py
# VERSION:1.1.0
# START_MODULE_CONTRACT:
# PURPOSE:Утилита для склейки файлов из указанной директории в один текстовый файл для внешнего аудита.
# SCOPE: Сканирование файловой системы, фильтрация по директориям и расширениям, конкатенация.
# INPUT: Относительный путь к директории через аргументы командной строки.
# OUTPUT: Файл в корне проекта с расширением _concat.txt.
# KEYWORDS:[DOMAIN(8): FileSystem; CONCEPT(7): Concatenation; TECH(9): PythonCLI]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.1.0 - Переименование в concat_folder.py, добавлена фильтрация расширений (исключен .db).]
# PREV_CHANGE_SUMMARY: [v1.0.0 - Создание утилиты для склейки файлов уроков.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Основная логика сканирования и склейки] => run_concat
# FUNC 5[Точка входа CLI] => main
# END_MODULE_MAP

import os
import argparse
import logging
from pathlib import Path

# Настройка логирования в стиле LDD
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# START_FUNCTION_run_concat
# START_CONTRACT:
# PURPOSE:Рекурсивно обходит директорию и записывает содержимое текстовых файлов в один выходной файл.
# INPUTS: 
# - [Путь к исходной директории] => target_dir: str
# OUTPUTS: 
# - [str] - Путь к созданному файлу.
# SIDE_EFFECTS: Создает новый файл в корне проекта.
# KEYWORDS:[PATTERN(6): Iterator; CONCEPT(8): FileIO]
# END_CONTRACT
def run_concat(target_dir: str) -> str:
    """Сканирует директорию и объединяет файлы в один, исключая бинарные и служебные файлы."""
    
    # START_BLOCK_INITIALIZE: [Подготовка путей и исключений]
    project_root = Path.cwd().resolve()
    start_dir_abs = (project_root / target_dir).resolve()
    
    if not start_dir_abs.is_dir():
        logger.error(f"[SystemError][IMP:10][run_concat][INITIALIZE][Check] Директория не найдена: {target_dir} [FAIL]")
        raise FileNotFoundError(f"Директория не найдена: {target_dir}")

    # Формируем имя выходного файла
    safe_name = target_dir.replace('/', '_').replace('\\', '_')
    output_filename = f"{safe_name}_concat.txt"
    output_path = project_root / output_filename
    
    excluded_dirs = {'.git', '__pycache__', 'venv', '.idea', '.vscode'}
    # BUG_FIX_CONTEXT: Исключаем .db, так как это бинарный файл и он портит текстовую склейку.
    excluded_extensions = {'.db', '.pyc', '.exe', '.bin'}
    processed_count = 0
    # END_BLOCK_INITIALIZE

    logger.info(f"[Flow][IMP:7][run_concat][INITIALIZE][Start] Начало обработки {target_dir} => {output_filename} [INFO]")

    # START_BLOCK_PROCESS_FILES: [Обход и запись]
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(start_dir_abs):
            # Фильтрация исключаемых директорий
            dirs[:] = [d for d in dirs if d not in excluded_dirs]

            for filename in files:
                file_path = Path(root) / filename
                
                # START_BLOCK_FILTER_FILE: [Проверка расширения и пути]
                if file_path.suffix.lower() in excluded_extensions:
                    logger.debug(f"[Filter][IMP:3][run_concat][PROCESS_FILES][SkipExtension] Пропуск бинарного файла: {filename} [SKIP]")
                    continue
                
                if file_path == output_path:
                    continue
                # END_BLOCK_FILTER_FILE

                try:
                    rel_path = file_path.relative_to(project_root)
                    file_size = file_path.stat().st_size
                    
                    logger.debug(f"[FileCheck][IMP:3][run_concat][PROCESS_FILES][Read] Чтение {rel_path} [SUCCESS]")
                    
                    outfile.write(f"$START_FILE {rel_path} {file_size}\n")
                    
                    # Читаем файл как текст, игнорируя ошибки кодировки для безопасности
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                        content = infile.read()
                        outfile.write(content.strip() + "\n")
                    
                    outfile.write(f"$END_FILE {rel_path}\n\n")
                    processed_count += 1
                    
                except Exception as e:
                    logger.warning(f"[IOError][IMP:8][run_concat][PROCESS_FILES][Exception] Ошибка файла {filename}: {e} [WARN]")
                    outfile.write(f"ERROR_READING_FILE {filename}: {e}\n")
    # END_BLOCK_PROCESS_FILES

    logger.info(f"[BeliefState][IMP:9][run_concat][FINALIZE][Result] Готово. Обработано {processed_count} файлов. [VALUE]")
    return str(output_path)
# END_FUNCTION_run_concat

# START_FUNCTION_main
def main():
    parser = argparse.ArgumentParser(description="Склейка файлов директории в один файл.")
    parser.add_argument("path", help="Относительный путь к папке (например, lesson_v3)")
    args = parser.parse_args()

    try:
        result_path = run_concat(args.path)
        print(f"Результат сохранен в: {result_path}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
# END_FUNCTION_main
