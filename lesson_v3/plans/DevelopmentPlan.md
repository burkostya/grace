$START_DEV_PLAN

**PURPOSE:** План реализации Lesson_v3: Генератор параболы с SQLite, CLI и Gradio.

---

### 1. Draft Code Graph (Черновой Граф Кода)

```xml
<DraftCodeGraph>
  <config_manager_py FILE="lesson_v3/src/config_manager.py" TYPE="MODULE">
    <annotation>Управление файлом config.json (чтение/запись).</annotation>
  </config_manager_py>
  
  <database_manager_py FILE="lesson_v3/src/database_manager.py" TYPE="MODULE">
    <annotation>Работа с SQLite: создание таблиц, запись точек, чтение для графиков.</annotation>
  </database_manager_py>
  
  <parabola_logic_py FILE="lesson_v3/src/parabola_logic.py" TYPE="MODULE">
    <annotation>Математический расчет точек параболы.</annotation>
  </parabola_logic_py>
  
  <cli_py FILE="lesson_v3/src/cli.py" TYPE="ENTRY_POINT">
    <annotation>CLI интерфейс для автономной генерации и экспорта.</annotation>
    <CrossLinks>
      <Link TARGET="parabola_logic_py" TYPE="USES" />
      <Link TARGET="config_manager_py" TYPE="USES" />
      <Link TARGET="database_manager_py" TYPE="USES" />
    </CrossLinks>
  </cli_py>
  
  <ui_controller_py FILE="lesson_v3/src/ui_controller.py" TYPE="MODULE">
    <annotation>Контроллер для Gradio: обработка кнопок, обновление UI.</annotation>
  </ui_controller_py>
  
  <run_lesson_v3_py FILE="run_lesson_v3.py" TYPE="ENTRY_POINT">
    <annotation>Запуск Gradio сервера.</annotation>
  </run_lesson_v3_py>
</DraftCodeGraph>
```

---

### 2. Step-by-step Data Flow (Пошаговый Поток Данных)

1.  **Инициализация:** При старте UI или CLI проверяется наличие `config.json`. Если нет — создается с дефолтными значениями.
2.  **Генерация (UI/CLI):**
    *   Считываются параметры (из UI полей или из `config.json`).
    *   `config_manager` сохраняет их в файл.
    *   `parabola_logic` вычисляет массив точек.
    *   `database_manager` очищает старые данные и записывает новые в SQLite.
    *   Логируется каждый шаг с `IMP:7-9`.
3.  **Отображение (UI):**
    *   `ui_controller` запрашивает данные из БД.
    *   Формирует `pandas.DataFrame` для таблицы.
    *   Создает `plotly.graph_objects.Figure` для графика.
4.  **Экспорт (CLI):**
    *   `database_manager` выгружает данные.
    *   Сохранение в CSV через `pandas`.

---

### 3. Acceptance Criteria (Критерии Приемки)

- [ ] **Критерий 1:** Файл `lesson_v3/config.json` корректно обновляется.
- [ ] **Критерий 2:** База `lesson_v3/parabola.db` содержит актуальные точки после генерации.
- [ ] **Критерий 3:** CLI команда `python lesson_v3/src/cli.py generate` работает без ошибок.
- [ ] **Критерий 4:** UI отображает параболу, соответствующую коэффициентам.
- [ ] **Критерий 5:** Тесты `pytest lesson_v3/tests/` проходят на 100%.
- [ ] **Критерий 6:** Логи пишутся в `lesson_v3/app_v3.log` с соблюдением формата LDD.

$END_DEV_PLAN
