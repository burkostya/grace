$START_DEV_PLAN

**PURPOSE:** Проектирование учебного приложения lesson_v7 для генерации точек параболы с соблюдением стандартов Agentic UX, LDD и изоляции слоев.

---

### 1. Draft Code Graph (Черновой Граф Кода)

```xml
<DraftCodeGraph>
  <lesson_v7_config_json FILE="lesson_v7/config.json" TYPE="DATA_FILE">
    <annotation>Файл конфигурации параметров параболы.</annotation>
  </lesson_v7_config_json>

  <config_manager_py FILE="lesson_v7/src/config_manager.py" TYPE="UTILITY">
    <annotation>Управление чтением и записью config.json.</annotation>
  </config_manager_py>

  <parabola_logic_py FILE="lesson_v7/src/parabola_logic.py" TYPE="BUSINESS_LOGIC">
    <annotation>Математический расчет точек параболы y = ax^2 + c.</annotation>
  </parabola_logic_py>

  <database_manager_py FILE="lesson_v7/src/database_manager.py" TYPE="DATA_ACCESS">
    <annotation>Работа с SQLite: создание таблиц, сохранение и чтение точек.</annotation>
  </database_manager_py>

  <cli_py FILE="lesson_v7/src/cli.py" TYPE="INTERFACE">
    <annotation>CLI интерфейс для автономной генерации и экспорта данных.</annotation>
    <CrossLinks>
      <Link TARGET="config_manager_py" TYPE="USES" />
      <Link TARGET="parabola_logic_py" TYPE="USES" />
      <Link TARGET="database_manager_py" TYPE="USES" />
    </CrossLinks>
  </cli_py>

  <ui_controller_py FILE="lesson_v7/src/ui_controller.py" TYPE="INTERFACE">
    <annotation>Контроллер Gradio: обработка ввода, вызов логики и построение графиков.</annotation>
    <CrossLinks>
      <Link TARGET="config_manager_py" TYPE="USES" />
      <Link TARGET="parabola_logic_py" TYPE="USES" />
      <Link TARGET="database_manager_py" TYPE="USES" />
    </CrossLinks>
  </ui_controller_py>

  <run_lesson_v7_py FILE="run_lesson_v7.py" TYPE="ENTRY_POINT">
    <annotation>Точка запуска Gradio сервера.</annotation>
    <CrossLinks>
      <Link TARGET="ui_controller_py" TYPE="CALLS" />
    </CrossLinks>
  </run_lesson_v7_py>
</DraftCodeGraph>
```

---

### 2. Step-by-step Data Flow (Пошаговый Поток Данных)

1.  **Инициализация:** При запуске UI или CLI проверяется наличие `config.json`. Если его нет, создается файл с параметрами по умолчанию (a=1, c=0, x_min=-10, x_max=10).
2.  **Генерация (CLI/UI):**
    *   Считываются параметры из `config.json` (или из полей ввода UI).
    *   `parabola_logic.py` генерирует список точек (x, y) на основе векторизованных операций (numpy/pandas).
    *   `database_manager.py` очищает старые данные и записывает новые в SQLite таблицу `points`.
    *   Логируется AI Belief State: "Ожидаю параболу с вершиной в (0, c)".
3.  **Отображение (UI):**
    *   `ui_controller.py` запрашивает данные из БД.
    *   Данные передаются в `gr.Dataframe` для таблицы.
    *   Данные передаются в Plotly для построения интерактивного графика.
4.  **Экспорт (CLI):**
    *   Команда `export-csv` считывает данные из БД и сохраняет их через `pandas.to_csv()`.

---

### 3. Acceptance Criteria (Критерии Приемки)

- [ ] **Критерий 1:** Все файлы созданы в папке `lesson_v7/` (кроме `run_lesson_v7.py`).
- [ ] **Критерий 2:** Код содержит полную семантическую разметку и LDD логи `[IMP:1-10]`.
- [ ] **Критерий 3:** CLI команда `python lesson_v7/src/cli.py generate` успешно обновляет БД.
- [ ] **Критерий 4:** UI запускается через `python run_lesson_v7.py` и корректно отображает график.
- [ ] **Критерий 5:** Тесты `pytest lesson_v7/tests/` проходят успешно с покрытием 100% бизнес-логики и выводом логов `[IMP:7-10]`.
- [ ] **Критерий 6:** Создан локальный `lesson_v7/AppGraph.xml`.

$END_DEV_PLAN
