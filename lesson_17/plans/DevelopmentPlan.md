$START_DEV_PLAN

**PURPOSE:** План разработки учебного приложения Lesson_17 (Тригонометрическая функция) с соблюдением стандартов LDD, Agentic UX и Headless Testing.

---

### 1. Draft Code Graph (Черновой Граф Кода)

```xml
<DraftCodeGraph>
  <lesson_17_src_config_manager_py FILE="lesson_17/src/config_manager.py" TYPE="MODULE">
    <annotation>Управление config.json (чтение/запись).</annotation>
    <load_config_FUNC NAME="load_config" TYPE="FUNCTION">
      <annotation>Загружает параметры из JSON.</annotation>
    </load_config_FUNC>
    <save_config_FUNC NAME="save_config" TYPE="FUNCTION">
      <annotation>Сохраняет параметры в JSON.</annotation>
    </save_config_FUNC>
  </lesson_17_src_config_manager_py>

  <lesson_17_src_database_manager_py FILE="lesson_17/src/database_manager.py" TYPE="MODULE">
    <annotation>Управление SQLite БД.</annotation>
    <save_points_FUNC NAME="save_points" TYPE="FUNCTION">
      <annotation>Записывает DataFrame в таблицу points.</annotation>
    </save_points_FUNC>
    <get_points_FUNC NAME="get_points" TYPE="FUNCTION">
      <annotation>Считывает точки из таблицы points.</annotation>
    </get_points_FUNC>
  </lesson_17_src_database_manager_py>

  <lesson_17_src_trig_logic_py FILE="lesson_17/src/trig_logic.py" TYPE="MODULE">
    <annotation>Математическая логика расчета.</annotation>
    <calculate_trig_FUNC NAME="calculate_trig" TYPE="FUNCTION">
      <annotation>Генерирует DataFrame с точками (x, y) по формуле y = A * sin(B * x + C) + D.</annotation>
    </calculate_trig_FUNC>
  </lesson_17_src_trig_logic_py>

  <lesson_17_src_ui_controller_py FILE="lesson_17/src/ui_controller.py" TYPE="MODULE">
    <annotation>Обработчики событий Gradio.</annotation>
    <on_generate_click_FUNC NAME="on_generate_click" TYPE="FUNCTION">
      <annotation>Координирует сохранение конфига, расчет и запись в БД.</annotation>
      <CrossLinks>
        <Link TARGET="lesson_17_src_config_manager_py_save_config_FUNC" TYPE="CALLS" />
        <Link TARGET="lesson_17_src_trig_logic_py_calculate_trig_FUNC" TYPE="CALLS" />
        <Link TARGET="lesson_17_src_database_manager_py_save_points_FUNC" TYPE="CALLS" />
      </CrossLinks>
    </on_generate_click_FUNC>
    <on_draw_click_FUNC NAME="on_draw_click" TYPE="FUNCTION">
      <annotation>Считывает данные и возвращает Plotly Figure.</annotation>
      <CrossLinks>
        <Link TARGET="lesson_17_src_database_manager_py_get_points_FUNC" TYPE="CALLS" />
      </CrossLinks>
    </on_draw_click_FUNC>
  </lesson_17_src_ui_controller_py>

  <lesson_17_src_cli_py FILE="lesson_17/src/cli.py" TYPE="MODULE">
    <annotation>Точка входа CLI (Agentic UX).</annotation>
  </lesson_17_src_cli_py>

  <run_lesson_17_py FILE="run_lesson_17.py" TYPE="ENTRY_POINT">
    <annotation>Запуск Gradio UI.</annotation>
  </run_lesson_17_py>
</DraftCodeGraph>
```

---

### 2. Step-by-step Data Flow (Пошаговый Поток Данных)

1.  **Инициализация:** Приложение считывает `config.json` через `config_manager.py`. Если файла нет, используются значения по умолчанию для тригонометрической функции (A, B, C, D, x_min, x_max).
2.  **Генерация (UI/CLI):**
    *   Параметры (A, B, C, D, x_min, x_max) передаются в `trig_logic.py`.
    *   `calculate_trig` создает `pandas.DataFrame` с колонками x и y.
    *   `database_manager.py` сохраняет DataFrame в SQLite (таблица `points`).
    *   Логирование каждого шага с `[IMP:7-9]` в `lesson_17/app_17.log`.
3.  **Визуализация (UI):**
    *   `ui_controller.py` вызывает `get_points` из БД.
    *   Данные передаются в `plotly.express.line` для создания графика.
    *   Gradio обновляет компоненты `Dataframe` и `Plot`.
4.  **Экспорт (CLI):**
    *   Команда `export-csv` считывает данные из БД и сохраняет в файл через `df.to_csv()`.

---

### 3. Acceptance Criteria (Критерии Приемки)

- [ ] **Backend:** Расчет `y = A * sin(B * x + C) + D` корректен. Логи содержат `[IMP:9]` при успешном сохранении в БД.
- [ ] **CLI:** Команда `python lesson_17/src/cli.py generate` работает без ошибок, используя `config.json`.
- [ ] **CLI:** Команда `python lesson_17/src/cli.py export-csv --out test.csv` создает валидный CSV файл.
- [ ] **UI:** Кнопка "Generate Data" обновляет таблицу в интерфейсе.
- [ ] **UI:** Кнопка "Draw Graph" отображает график тригонометрической функции.
- [ ] **Testing:** `pytest lesson_17/tests/` показывает 100% PASS.
- [ ] **Testing:** Тесты выводят логи `[IMP:7-10]` в консоль.
- [ ] **Architecture:** Весь код содержит семантическую разметку (CONTRACT, MODULE_MAP, START_BLOCK).

$END_DEV_PLAN
