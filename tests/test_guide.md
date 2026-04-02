# QA Test Guide: Lesson 21 (Swarm ETL)

## Summary
Этот документ предназначен для QA-агентов (или субагентов `task`) для верификации ETL-процесса в `lesson_21_swarm_test`.

## Инструменты проверки
- **SQLite3 CLI**: `sqlite3 warehouse.db`
- **Pytest**: `python -m pytest tests/test_lesson_21.py -s -v`

## Сценарии верификации

### 1. Верификация целостности БД (Staging vs Canonical)
После запуска загрузки выполните SQL-запрос:
```sql
SELECT COUNT(*) FROM scores;
```
**Ожидаемый результат:** 2 (если в исходном `data.csv` было 2 полных записи).

### 2. Проверка валидации (NaN Filtering)
Проверьте отсутствие записей с неполными данными:
```sql
SELECT * FROM scores WHERE name IS NULL OR score IS NULL;
```
**Ожидаемый результат:** 0 строк.

## Ожидаемые маркеры в логах [IMP:9-10]
1. `[BeliefState][IMP:9][load_csv_to_db][LOAD][AAGGoal] Данные успешно загружены...`
2. В случае ошибки: `[SystemError][IMP:10][load_csv_to_db]... [FATAL]`

## Чек-лист для QA
- [ ] Таблица `scores` существует.
- [ ] Поле `id` уникально.
- [ ] Логи `IMP:7-8` показывают этапы Extract и Transform.
