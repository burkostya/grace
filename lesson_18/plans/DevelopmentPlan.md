$START_DEV_PLAN

**PURPOSE:** План разработки учебного приложения Lesson 18 (Генератор параболы).

---

### 1. Draft Code Graph (Черновой Граф Кода)

```xml
<DraftCodeGraph>
  <lesson_18_src_config_manager_py FILE="lesson_18/src/config_manager.py" TYPE="MODULE">
    <annotation>Управление файлом config.json.</annotation>
    <ConfigManager_CLASS NAME="ConfigManager" TYPE="IS_CLASS_OF_MODULE">
      <load_config_METHOD NAME="load_config" TYPE="IS_METHOD_OF_CLASS" />
      <save_config_METHOD NAME="save_config" TYPE="IS_METHOD_OF_CLASS" />
    </ConfigManager_CLASS>
  </lesson_18_src_config_manager_py>

  <lesson_18_src_data_processor_py FILE="lesson_18/src/data_processor.py" TYPE="MODULE">
    <annotation>Расчет точек параболы и работа с SQLite.</annotation>
    <DataProcessor_CLASS NAME="DataProcessor" TYPE="IS_CLASS_OF_MODULE">
      <generate_points_METHOD NAME="generate_points" TYPE="IS_METHOD_OF_CLASS" />
      <save_to_db_METHOD NAME="save_to_db" TYPE="IS_METHOD_OF_CLASS" />
      <load_from_db_METHOD NAME="load_from_db" TYPE="IS_METHOD_OF_CLASS" />
    </DataProcessor_CLASS>
  </lesson_18_src_data_processor_py>

  <lesson_18_src_ui_controller_py FILE="lesson_18/src/ui_controller.py" TYPE="MODULE">
    <annotation>Контроллер UI Gradio и обработчики событий.</annotation>
    <UIController_CLASS NAME="UIController" TYPE="IS_CLASS_OF_MODULE">
      <handle_generate_METHOD NAME="handle_generate" TYPE="IS_METHOD_OF_CLASS" />
      <handle_draw_METHOD NAME="handle_draw" TYPE="IS_METHOD_OF_CLASS" />
      <create_ui_METHOD NAME="create_ui" TYPE="IS_METHOD_OF_CLASS" />
    </UIController_CLASS>
  </lesson_18_src_ui_controller_py>

  <run_lesson_18_py FILE="run_lesson_18.py" TYPE="ENTRY_POINT">
    <annotation>Точка запуска приложения.</annotation>
  </run_lesson_18_py>

  <tests_test_lesson_18_py FILE="tests/test_lesson_18.py" TYPE="TEST_MODULE">
    <annotation>Тесты бэкенда и UI Headless.</annotation>
  </tests_test_lesson_18_py>
</DraftCodeGraph>
```

---

### 2. Step-by-step Data Flow (Пошаговый Поток Данных)

1.  **Инициализация:** `run_lesson_18.py` вызывает `UIController.create_ui()`. `ConfigManager` загружает начальные параметры из `config.json`.
2.  **Генерация данных (UC_GENERATE):**
    - Пользователь нажимает "Generate Data".
    - `UIController.handle_generate` получает параметры (a, c, x_min, x_max).
    - `ConfigManager.save_config` сохраняет их.
    - `DataProcessor.generate_points` рассчитывает DataFrame с точками (x, y).
    - `DataProcessor.save_to_db` записывает DataFrame в SQLite таблицу `points`.
    - `UIController` возвращает DataFrame для отображения в компоненте `Dataframe`.
3.  **Отрисовка графика (UC_DRAW):**
    - Пользователь нажимает "Draw Graph".
    - `DataProcessor.load_from_db` считывает данные из SQLite.
    - `UIController.handle_draw` создает объект `plotly.graph_objects.Figure`.
    - `UIController` возвращает Figure для отображения в компоненте `Plot`.

---

### 3. Acceptance Criteria (Критерии Приемки)

- [ ] **Критерий 1:** Все файлы созданы в `lesson_18/` (кроме `run_lesson_18.py` и тестов в `tests/`).
- [ ] **Критерий 2:** Код размечен семантическими тегами (CONTRACT, START_BLOCK, LDD логирование).
- [ ] **Критерий 3:** Логи пишутся в `lesson_18/app_18.log` с использованием `[IMP:1-10]`.
- [ ] **Критерий 4:** Тесты в `tests/test_lesson_18.py` покрывают расчеты, БД и UI Headless (без запуска сервера).
- [ ] **Критерий 5:** Тесты выводят логи `[IMP:7-10]` через `caplog`.
- [ ] **Критерий 6:** `AppGraph.xml` создан в `lesson_18/` после успешных тестов.

$END_DEV_PLAN
