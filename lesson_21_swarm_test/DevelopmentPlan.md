# Development Plan: Lesson 21 (Swarm Test)

$START_DEV_PLAN

**PURPOSE:** Пошаговая реализация ETL-модуля для тестирования новой архитектуры 7.1.17.

---

### 1. Draft Code Graph (Черновой Граф Кода)

```xml
<DraftCodeGraph>
  <lesson_21_etl_py FILE="lesson_21_swarm_test/etl_module.py" TYPE="DATA_PROCESSING_MODULE">
    <annotation>Основной модуль обработки данных.</annotation>
    <load_csv_to_db_FUNC NAME="load_csv_to_db" TYPE="MAIN_ETL_FUNCTION">
      <annotation>Загружает CSV в SQLite с валидацией.</annotation>
    </load_csv_to_db_FUNC>
  </lesson_21_etl_py>
</DraftCodeGraph>
```

---

### 2. Step-by-step Data Flow (Пошаговый Поток Данных)

1.  **Extract:** Загрузка `data.csv` через Pandas. (Используйте `read` для проверки наличия файла).
2.  **Transform:** Удаление `NaN` и приведение типов.
3.  **Load:** Запись в SQLite через `to_sql` (используйте временные таблицы для надежности, если данных много).
4.  **Logging:** Каждая стадия должна иметь лог `[IMP:7-8]`. Финал — `[IMP:9]`.

---

### 3. Acceptance Criteria (Критерии Приемки)

- [ ] Создан `etl_module.py` с полной семантической разметкой.
- [ ] Созданы тесты в `tests/test_lesson_21.py` с использованием `tmp_path`.
- [ ] Создан `tests/test_guide.md` с описанием SQL-запросов для проверки.
- [ ] Все тесты проходят (100% PASS).

$END_DEV_PLAN
