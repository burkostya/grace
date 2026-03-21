$START_DEV_PLAN

**PURPOSE:** План разработки учебного приложения Lesson 10 (Парабола).

---

### 1. Draft Code Graph (Черновой Граф Кода)

```xml
<DraftCodeGraph>
  <lesson_10_src_config_manager_py FILE="lesson_10/src/config_manager.py" TYPE="MODULE">
    <annotation>Управление файлом config.json.</annotation>
  </lesson_10_src_config_manager_py>
  
  <lesson_10_src_database_manager_py FILE="lesson_10/src/database_manager.py" TYPE="MODULE">
    <annotation>Работа с SQLite БД.</annotation>
  </lesson_10_src_database_manager_py>
  
  <lesson_10_src_parabola_logic_py FILE="lesson_10/src/parabola_logic.py" TYPE="MODULE">
    <annotation>Математический расчет параболы.</annotation>
  </lesson_10_src_parabola_logic_py>
  
  <lesson_10_src_ui_controller_py FILE="lesson_10/src/ui_controller.py" TYPE="MODULE">
    <annotation>Логика управления Gradio UI.</annotation>
  </lesson_10_src_ui_controller_py>
  
  <lesson_10_src_cli_py FILE="lesson_10/src/cli.py" TYPE="MODULE">
    <annotation>Точка входа CLI.</annotation>
  </lesson_10_src_cli_py>
  
  <run_lesson_10_py FILE="run_lesson_10.py" TYPE="ENTRY_POINT">
    <annotation>Запуск Gradio сервера.</annotation>
  </run_lesson_10_py>
</DraftCodeGraph>
```

---

### 2. Step-by-step Data Flow (Пошаговый Поток Данных)

1.  **Инициализация:** При запуске любого компонента проверяется наличие `config.json`. Если нет — создается с дефолтами (a=1, c=0, x_min=-10, x_max=10).
2.  **Генерация (CLI/UI):**
    *   Считываются параметры из `config.json`.
    *   `parabola_logic` вычисляет список точек (x, y).
    *   `database_manager` очищает таблицу и записывает новые точки.
    *   Логируется AI Belief State: "Ожидаю N точек в БД".
3.  **Визуализация (UI):**
    *   `ui_controller` запрашивает данные из БД через `database_manager`.
    *   Данные преобразуются в `pandas.DataFrame` для таблицы и `plotly.graph_objects` для графика.
4.  **Экспорт (CLI):**
    *   Команда `export-csv` выгружает данные из БД в файл.

---

### 3. Acceptance Criteria (Критерии Приемки)

- [ ] **Критерий 1:** Все файлы содержат семантическую разметку (START_BLOCK, CONTRACT).
- [ ] **Критерий 2:** Логи пишутся в `lesson_10/app_10.log` с использованием IMP шкалы.
- [ ] **Критерий 3:** `pytest` проходит успешно, включая Headless UI тест.
- [ ] **Критерий 4:** CLI команда `generate` работает без передачи аргументов (берет из конфига).
- [ ] **Критерий 5:** Создан локальный `lesson_10/AppGraph.xml`.

$END_DEV_PLAN
