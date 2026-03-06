$START_DEV_PLAN

**PURPOSE:** Создание учебного приложения Lesson 6 для генерации точек параболы с использованием SQLite, Gradio, Plotly и CLI, демонстрирующего архитектурные стандарты (изоляция слоев, Agentic UX, LDD 2.0).

---

### 1. Draft Code Graph (Черновой Граф Кода)

```xml
<DraftCodeGraph>
  <lesson_v6_src_config_manager_py FILE="lesson_v6/src/config_manager.py" TYPE="MODULE">
    <annotation>Управление файлом config.json (чтение/запись параметров a, c, x_min, x_max).</annotation>
  </lesson_v6_src_config_manager_py>
  
  <lesson_v6_src_database_manager_py FILE="lesson_v6/src/database_manager.py" TYPE="MODULE">
    <annotation>Управление БД SQLite. Создание таблицы points, сохранение и получение данных.</annotation>
  </lesson_v6_src_database_manager_py>

  <lesson_v6_src_parabola_logic_py FILE="lesson_v6/src/parabola_logic.py" TYPE="MODULE">
    <annotation>Математическая логика расчета точек параболы y = ax^2 + c.</annotation>
  </lesson_v6_src_parabola_logic_py>

  <lesson_v6_src_ui_controller_py FILE="lesson_v6/src/ui_controller.py" TYPE="MODULE">
    <annotation>Контроллер Gradio. Обработка нажатий кнопок, обновление конфига, вызов генерации и построение графиков Plotly.</annotation>
    <CrossLinks>
      <Link TARGET="lesson_v6_src_config_manager_py" TYPE="USES" />
      <Link TARGET="lesson_v6_src_database_manager_py" TYPE="USES" />
      <Link TARGET="lesson_v6_src_parabola_logic_py" TYPE="USES" />
    </CrossLinks>
  </lesson_v6_src_ui_controller_py>

  <lesson_v6_src_cli_py FILE="lesson_v6/src/cli.py" TYPE="MODULE">
    <annotation>CLI интерфейс (argparse) для команд generate и export-csv.</annotation>
    <CrossLinks>
      <Link TARGET="lesson_v6_src_config_manager_py" TYPE="USES" />
      <Link TARGET="lesson_v6_src_database_manager_py" TYPE="USES" />
      <Link TARGET="lesson_v6_src_parabola_logic_py" TYPE="USES" />
    </CrossLinks>
  </lesson_v6_src_cli_py>

  <run_lesson_v6_py FILE="run_lesson_v6.py" TYPE="ENTRY_POINT">
    <annotation>Запуск Gradio интерфейса.</annotation>
  </run_lesson_v6_py>
</DraftCodeGraph>
```

---

### 2. Step-by-step Data Flow (Пошаговый Поток Данных)

1.  **Инициализация:** При запуске UI или CLI загружаются параметры из `lesson_v6/config.json`.
2.  **Генерация (Generate Data):**
    *   Пользователь вводит `a, c, x_min, x_max` в UI или запускает `cli.py generate`.
    *   `config_manager` сохраняет параметры в `config.json`.
    *   `parabola_logic` вычисляет список точек $(x, y)$ в заданном диапазоне.
    *   `database_manager` очищает таблицу `points` и записывает новые данные.
    *   UI отображает обновленный `Dataframe`.
3.  **Визуализация (Draw Graph):**
    *   `database_manager` считывает все точки из БД.
    *   `ui_controller` формирует объект `plotly.graph_objects.Figure`.
    *   UI отображает график в правой колонке.
4.  **Экспорт (CLI export-csv):**
    *   `database_manager` считывает данные.
    *   `cli.py` записывает их в CSV файл с заголовками.

---

### 3. Acceptance Criteria (Критерии Приемки)

- [ ] **Структура:** Все файлы созданы в `lesson_v6/` и `run_lesson_v6.py` в корне.
- [ ] **Изоляция:** Логика БД, конфига и математики разделена по модулям.
- [ ] **UI:** Gradio имеет две колонки, кнопки работают корректно, график Plotly интерактивен.
- [ ] **CLI:** Команды `generate` и `export-csv` работают без ошибок.
- [ ] **LDD 2.0:** Файл `lesson_v6/app_v6.log` содержит записи с `[IMP:1-10]` и "AI Belief State".
- [ ] **Тесты:** 100% покрытие (Backend, CLI, Headless UI).
- [ ] **AppGraph:** Корневой `AppGraph.xml` обновлен.

$END_DEV_PLAN
