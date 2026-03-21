$START_DEV_PLAN

**PURPOSE:** Реализация учебного примера Lesson_15 (Парабола $y = ax^2 + c$) с соблюдением стандартов фреймворка промптов.

---

### 1. Draft Code Graph (Черновой Граф Кода)

```xml
<DraftCodeGraph>
  <lesson_15_src_config_manager_py FILE="lesson_15/src/config_manager.py" TYPE="MODULE">
    <annotation>Управление чтением/записью config.json.</annotation>
    <ConfigManager_CLASS NAME="ConfigManager" TYPE="CLASS">
      <load_METHOD NAME="load" TYPE="METHOD" />
      <save_METHOD NAME="save" TYPE="METHOD" />
    </ConfigManager_CLASS>
  </lesson_15_src_config_manager_py>

  <lesson_15_src_database_manager_py FILE="lesson_15/src/database_manager.py" TYPE="MODULE">
    <annotation>Управление SQLite БД для хранения точек.</annotation>
    <DatabaseManager_CLASS NAME="DatabaseManager" TYPE="CLASS">
      <init_db_METHOD NAME="init_db" TYPE="METHOD" />
      <save_points_METHOD NAME="save_points" TYPE="METHOD" />
      <get_points_METHOD NAME="get_points" TYPE="METHOD" />
    </DatabaseManager_CLASS>
  </lesson_15_src_database_manager_py>

  <lesson_15_src_parabola_logic_py FILE="lesson_15/src/parabola_logic.py" TYPE="MODULE">
    <annotation>Бизнес-логика расчета точек параболы.</annotation>
    <generate_points_FUNC NAME="generate_points" TYPE="FUNCTION">
      <CrossLinks>
        <Link TARGET="lesson_15_src_config_manager_py" TYPE="READS_CONFIG" />
      </CrossLinks>
    </generate_points_FUNC>
  </lesson_15_src_parabola_logic_py>

  <lesson_15_src_cli_py FILE="lesson_15/src/cli.py" TYPE="MODULE">
    <annotation>CLI интерфейс (Agentic UX).</annotation>
    <main_FUNC NAME="main" TYPE="FUNCTION" />
  </lesson_15_src_cli_py>

  <lesson_15_src_ui_controller_py FILE="lesson_15/src/ui_controller.py" TYPE="MODULE">
    <annotation>Контроллеры для Gradio UI.</annotation>
    <on_generate_FUNC NAME="on_generate" TYPE="FUNCTION" />
    <on_draw_FUNC NAME="on_draw" TYPE="FUNCTION" />
  </lesson_15_src_ui_controller_py>

  <run_lesson_15_py FILE="run_lesson_15.py" TYPE="ENTRY_POINT">
    <annotation>Точка запуска Gradio сервера.</annotation>
  </run_lesson_15_py>
</DraftCodeGraph>
```

---

### 2. Step-by-step Data Flow (Пошаговый Поток Данных)

1.  **Инициализация:** `run_lesson_15.py` запускает Gradio. `ConfigManager` загружает начальные параметры из `config.json`.
2.  **Генерация (UI/CLI):**
    - Пользователь (UI) или Агент (CLI) инициирует генерацию.
    - `ConfigManager` сохраняет текущие параметры (если из UI).
    - `parabola_logic` рассчитывает точки $y = ax^2 + c$ для диапазона $[x_{min}, x_{max}]$.
    - `DatabaseManager` сохраняет точки в SQLite.
    - Логирование каждого шага с `[IMP:7-10]` в `lesson_15/app_15.log`.
3.  **Отображение:**
    - UI вызывает `DatabaseManager.get_points()`.
    - Данные отображаются в `gr.Dataframe`.
    - `Plotly` строит график на основе полученных данных.
4.  **Экспорт (CLI):**
    - Команда `export-csv` считывает данные из БД и записывает в файл.

---

### 3. Acceptance Criteria (Критерии Приемки)

- [ ] **Критерий 1:** Изоляция слоев (Бизнес-логика не знает о UI/CLI).
- [ ] **Критерий 2:** CLI поддерживает `generate` (автоматически из конфига) и `export-csv`.
- [ ] **Критерий 3:** UI разделен на 2 колонки, график интерактивный (Plotly).
- [ ] **Критерий 4:** Логирование LDD 2.0 в `lesson_15/app_15.log` с AI Belief State.
- [ ] **Критерий 5:** 100% покрытие тестами (Backend, CLI Smoke, UI Headless).
- [ ] **Критерий 6:** Наличие локального `AppGraph.xml` в `lesson_15/`.

$END_DEV_PLAN
