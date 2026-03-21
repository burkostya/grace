$START_DEV_PLAN

**PURPOSE:** План разработки учебного приложения Lesson_13 с использованием семантической разметки, LDD и Agentic UX.

---

### 1. Draft Code Graph (Черновой Граф Кода)

```xml
<DraftCodeGraph>
  <lesson_13_src_config_manager_py FILE="lesson_13/src/config_manager.py" TYPE="MODULE">
    <annotation>Управление состоянием через config.json.</annotation>
    <ConfigManager_CLASS NAME="ConfigManager" TYPE="CLASS">
      <load_config_METHOD NAME="load_config" TYPE="METHOD" />
      <save_config_METHOD NAME="save_config" TYPE="METHOD" />
    </ConfigManager_CLASS>
  </lesson_13_src_config_manager_py>

  <lesson_13_src_database_manager_py FILE="lesson_13/src/database_manager.py" TYPE="MODULE">
    <annotation>Работа с SQLite БД.</annotation>
    <DatabaseManager_CLASS NAME="DatabaseManager" TYPE="CLASS">
      <init_db_METHOD NAME="init_db" TYPE="METHOD" />
      <save_points_METHOD NAME="save_points" TYPE="METHOD" />
      <get_points_METHOD NAME="get_points" TYPE="METHOD" />
    </DatabaseManager_CLASS>
  </lesson_13_src_database_manager_py>

  <lesson_13_src_parabola_logic_py FILE="lesson_13/src/parabola_logic.py" TYPE="MODULE">
    <annotation>Бизнес-логика расчета параболы.</annotation>
    <calculate_parabola_FUNCTION NAME="calculate_parabola" TYPE="FUNCTION" />
  </lesson_13_src_parabola_logic_py>

  <lesson_13_src_ui_controller_py FILE="lesson_13/src/ui_controller.py" TYPE="MODULE">
    <annotation>Логика интерфейса Gradio.</annotation>
    <UIController_CLASS NAME="UIController" TYPE="CLASS">
      <generate_data_handler_METHOD NAME="generate_data_handler" TYPE="METHOD" />
      <draw_graph_handler_METHOD NAME="draw_graph_handler" TYPE="METHOD" />
    </UIController_CLASS>
  </lesson_13_src_ui_controller_py>

  <lesson_13_src_cli_py FILE="lesson_13/src/cli.py" TYPE="MODULE">
    <annotation>Agentic UX CLI интерфейс.</annotation>
    <main_FUNCTION NAME="main" TYPE="FUNCTION" />
  </lesson_13_src_cli_py>

  <run_lesson_13_py FILE="run_lesson_13.py" TYPE="ENTRY_POINT">
    <annotation>Точка запуска Gradio UI.</annotation>
  </run_lesson_13_py>
</DraftCodeGraph>
```

---

### 2. Step-by-step Data Flow (Пошаговый Поток Данных)

1.  **Инициализация:** Приложение загружает `config.json` через `ConfigManager`. Если файла нет, создаются значения по умолчанию.
2.  **Генерация (UI/CLI):**
    *   Считываются параметры `a, c, x_min, x_max`.
    *   `parabola_logic` вычисляет точки.
    *   `DatabaseManager` сохраняет точки в SQLite.
    *   `ConfigManager` обновляет `config.json`.
3.  **Отображение (UI):**
    *   `UIController` запрашивает данные из БД.
    *   Данные передаются в `gr.Dataframe`.
    *   `Plotly` строит график на основе данных из БД.
4.  **Экспорт (CLI):**
    *   `cli.py` вызывает `DatabaseManager.get_points()`.
    *   Данные сохраняются в CSV.

---

### 3. Acceptance Criteria (Критерии Приемки)

- [ ] **Критерий 1:** Все файлы содержат семантическую разметку (`START_BLOCK`, `MODULE_CONTRACT`, `LDD logs`).
- [ ] **Критерий 2:** Логи пишутся в `lesson_13/app_13.log` с использованием шкалы `IMP:1-10`.
- [ ] **Критерий 3:** CLI команды `generate` и `export-csv` работают корректно.
- [ ] **Критерий 4:** UI Headless тесты подтверждают корректность возвращаемых типов Gradio.
- [ ] **Критерий 5:** `pytest` выводит логи `IMP:7-10` в консоль через `caplog`.
- [ ] **Критерий 6:** Создан локальный `lesson_13/AppGraph.xml`.

$END_DEV_PLAN
