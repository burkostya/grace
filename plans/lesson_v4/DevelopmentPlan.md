$START_DEV_PLAN

**PURPOSE:** План реализации Lesson_v4: Генератор параболы с SQLite, CLI и Gradio (повторение паттернов lesson_v3 для закрепления навыков).

---

### 1. Draft Code Graph (Черновой Граф Кода)

```xml
<DraftCodeGraph>
  <config_manager_py FILE="lesson_v4/src/config_manager.py" TYPE="MODULE">
    <annotation>Управление файлом config.json (чтение/запись).</annotation>
  </config_manager_py>
  
  <database_manager_py FILE="lesson_v4/src/database_manager.py" TYPE="MODULE">
    <annotation>Работа с SQLite: создание таблиц, запись точек, чтение для графиков.</annotation>
  </database_manager_py>
  
  <parabola_logic_py FILE="lesson_v4/src/parabola_logic.py" TYPE="MODULE">
    <annotation>Математический расчет точек параболы.</annotation>
  </parabola_logic_py>
  
  <cli_py FILE="lesson_v4/src/cli.py" TYPE="ENTRY_POINT">
    <annotation>CLI интерфейс для автономной генерации и экспорта.</annotation>
    <CrossLinks>
      <Link TARGET="parabola_logic_py" TYPE="USES" />
      <Link TARGET="config_manager_py" TYPE="USES" />
      <Link TARGET="database_manager_py" TYPE="USES" />
    </CrossLinks>
  </cli_py>
  
  <ui_controller_py FILE="lesson_v4/src/ui_controller.py" TYPE="MODULE">
    <annotation>Контроллер для Gradio: обработка кнопок, обновление UI.</annotation>
  </ui_controller_py>
  
  <run_lesson_v4_py FILE="run_lesson_v4.py" TYPE="ENTRY_POINT">
    <annotation>Запуск Gradio сервера.</annotation>
  </run_lesson_v4_py>
</DraftCodeGraph>
```

---

### 2. Step-by-step Data Flow (Пошаговый Поток Данных)

1.  **Инициализация:** При старте UI или CLI проверяется наличие `config.json`. Если нет — создается с дефолтными значениями (a=1.0, c=0.0, x_min=-5, x_max=5).
2.  **Генерация (UI/CLI):**
    *   Считываются параметры (из UI полей или из `config.json`).
    *   `config_manager` сохраняет их в файл.
    *   `parabola_logic` вычисляет массив точек (x, y) по формуле y = ax² + c.
    *   `database_manager` очищает старые данные и записывает новые в SQLite.
    *   Логируется каждый шаг с `IMP:7-9` (фиксация AI Belief State).
3.  **Отображение (UI):**
    *   `ui_controller` запрашивает данные из БД.
    *   Формирует `pandas.DataFrame` для таблицы.
    *   Создает `plotly.graph_objects.Figure` для графика.
4.  **Экспорт (CLI):**
    *   `database_manager` выгружает данные из БД.
    *   Сохранение в CSV через `pandas`.

---

### 3. Acceptance Criteria (Критерии Приемки)

- [ ] **Критерий 1:** Файл `lesson_v4/config.json` корректно обновляется при генерации.
- [ ] **Критерий 2:** База `lesson_v4/parabola.db` содержит актуальные точки после генерации.
- [ ] **Критерий 3:** CLI команда `python lesson_v4/src/cli.py generate` работает без ошибок (exit code 0).
- [ ] **Критерий 4:** CLI команда `python lesson_v4/src/cli.py export-csv --out <file>` создает корректный CSV файл.
- [ ] **Критерий 5:** UI отображает параболу, соответствующую коэффициентам a и c.
- [ ] **Критерий 6:** Тесты `pytest lesson_v4/tests/` проходят на 100%.
- [ ] **Критерий 7:** Логи пишутся в `lesson_v4/app_v4.log` с соблюдением формата LDD (шкала IMP:1-10).
- [ ] **Критерий 8:** Все модули обернуты в семантический экзоскелет (MODULE_CONTRACT, START_BLOCK, CONTRACT).

$END_DEV_PLAN
