# Business Requirements: Swarm ETL Test (Lesson 21)

$START_DOC_NAME

**PURPOSE:** Проверка автономности ИИ-агента в чистой сессии (Zero-Context Survival) при работе с новыми правилами Kilo Code 7.1.17.
**SCOPE:** Реализация простого ETL-пайплайна: чтение CSV, валидация данных, сохранение в SQLite.

$START_SECTION_REQUIREMENTS
### Функциональные требования

$START_ARTIFACT_ETL_LOGIC
**TYPE:** USE_CASE
**KEYWORDS:** [DOMAIN: ETL; TECH: Pandas, SQLite]

$START_CONTRACT
**PURPOSE:** Обработка файла `data.csv` и сохранение в базу `warehouse.db`.
**DESCRIPTION:** 
1. Прочитать `data.csv` (поля: `id`, `name`, `score`).
2. Удалить строки с пустыми значениями.
3. Сохранить в таблицу `scores` базы данных SQLite.
4. В базе данных `id` должен быть первичным ключом.
**RATIONALE:** Проверка работы с файлами, БД и инструментами `bash`, `edit`, `read`.
**ACCEPTANCE_CRITERIA:**
- [ ] Все валидные строки из CSV попали в БД.
- [ ] Логи содержат записи [IMP:9] о начале и конце загрузки.
- [ ] Создан файл `tests/test_guide.md`.
$END_CONTRACT
$END_ARTIFACT_ETL_LOGIC

$END_SECTION_REQUIREMENTS

$END_DOC_NAME
