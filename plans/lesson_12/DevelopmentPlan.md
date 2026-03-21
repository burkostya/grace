$START_DEV_PLAN

**PURPOSE:** Создание учебного приложения на Dash (Lesson 12) для генерации и редактирования параболы с акцентом на Headless-тестирование UI и LDD 2.0.

---

### 1. Draft Code Graph (Черновой Граф Кода)

```xml
<DraftCodeGraph>
  <lesson_12_DIR PATH="lesson_12/" TYPE="DIRECTORY">
    <annotation>Корневая папка урока 12.</annotation>
    
    <handlers_py FILE="lesson_12/handlers.py" TYPE="LOGIC_LAYER">
      <annotation>Чистая бизнес-логика (без Dash). Расчет точек, построение Figure.</annotation>
      <generate_parabola_points_FUNC NAME="generate_parabola_points" TYPE="FUNCTION" />
      <build_comparison_figure_FUNC NAME="build_comparison_figure" TYPE="FUNCTION" />
    </handlers_py>

    <config_manager_py FILE="lesson_12/config_manager.py" TYPE="DATA_LAYER">
      <annotation>Управление config.json (a, c, x_min, x_max).</annotation>
    </config_manager_py>

    <db_manager_py FILE="lesson_12/db_manager.py" TYPE="DATA_LAYER">
      <annotation>Управление SQLite (parabola.db).</annotation>
    </db_manager_py>

    <app_py FILE="lesson_12/app.py" TYPE="UI_LAYER">
      <annotation>Dash Layout + Callbacks (тонкие обертки над handlers).</annotation>
      <on_generate_CALLBACK NAME="on_generate" TYPE="CALLBACK" />
      <on_draw_CALLBACK NAME="on_draw" TYPE="CALLBACK" />
      <on_save_CALLBACK NAME="on_save" TYPE="CALLBACK" />
    </app_py>

    <cli_py FILE="lesson_12/cli.py" TYPE="AGENTIC_UX">
      <annotation>CLI интерфейс для автономных агентов.</annotation>
    </cli_py>

    <tests_DIR PATH="lesson_12/tests/" TYPE="DIRECTORY">
      <test_handlers_py FILE="lesson_12/tests/test_handlers.py" TYPE="HEADLESS_TEST" />
      <test_callbacks_py FILE="lesson_12/tests/test_callbacks.py" TYPE="HEADLESS_UI_TEST" />
      <test_cli_py FILE="lesson_12/tests/test_cli.py" TYPE="SMOKE_TEST" />
    </tests_DIR>
  </lesson_12_DIR>
  
  <run_lesson_12_py FILE="run_lesson_12.py" TYPE="ENTRY_POINT">
    <annotation>Точка запуска (Debug/Prod через Waitress).</annotation>
  </run_lesson_12_py>
</DraftCodeGraph>
```

---

### 2. Step-by-step Data Flow (Пошаговый Поток Данных)

1.  **Инициализация:** `app.py` загружает начальные параметры из `config_manager.py`.
2.  **Генерация (UI/CLI):** 
    *   Пользователь жмет "Generate".
    *   `handlers.generate_parabola_points` создает DataFrame.
    *   `db_manager` сохраняет данные в SQLite.
    *   `config_manager` обновляет `config.json`.
    *   Данные возвращаются в `DataTable` (y_edited = y).
3.  **Редактирование:** Пользователь меняет значения в колонке `y_edited` грида.
4.  **Отрисовка:** 
    *   Пользователь жмет "Draw Graph".
    *   `handlers.build_comparison_figure` получает текущий `data` из грида (со всеми правками).
    *   Plotly Figure отображает две кривые: Original и Edited.
5.  **Сохранение правок:** `db_manager` обновляет записи в SQLite на основе текущего состояния грида.

---

### 3. Acceptance Criteria (Критерии Приемки)

- [ ] **Изоляция:** `handlers.py` не содержит импортов `dash`, `dash_bootstrap_components` или `dash_table`.
- [ ] **Headless UI Testing:** Тесты в `test_callbacks.py` вызывают функции-callback'и напрямую как Python-функции и проверяют возвращаемые типы (list[dict] для таблиц, go.Figure для графиков).
- [ ] **Редактируемый грид:** Колонка `y_edited` в `DataTable` доступна для ввода, изменения отображаются на графике после нажатия "Draw Graph".
- [ ] **LDD 2.0:** Логи в `lesson_12/app_12.log` содержат метки `[IMP:1-10]` и описание "AI Belief State".
- [ ] **CLI:** Команды `generate` и `export-csv` работают корректно.
- [ ] **Prod Mode:** `python run_lesson_12.py --prod` запускает сервер через `waitress`.

$END_DEV_PLAN
