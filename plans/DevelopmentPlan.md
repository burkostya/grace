$START_DEV_PLAN

**PURPOSE:** План разработки учебного приложения "Генератор Параболы" с разделением на бэкенд, контроллер интерфейса и UI на Gradio.

---

### 1. Draft Code Graph (Черновой Граф Кода)

```xml
<DraftCodeGraph>
  <datagenerator_py FILE="datagenerator.py" TYPE="BACKEND_MODULE">
    <annotation>Логика расчета параболы и работа с SQLite.</annotation>
    <DataGenerator_CLASS NAME="DataGenerator" TYPE="IS_CLASS_OF_MODULE">
      <annotation>Управляет соединением с БД и генерацией данных.</annotation>
      <generate_points_METHOD NAME="generate_points" TYPE="IS_METHOD_OF_CLASS">
        <annotation>Рассчитывает y = ax^2 + c и пишет в БД.</annotation>
      </generate_points_METHOD>
      <get_all_points_METHOD NAME="get_all_points" TYPE="IS_METHOD_OF_CLASS">
        <annotation>Читает все точки из БД.</annotation>
      </get_all_points_METHOD>
    </DataGenerator_CLASS>
  </datagenerator_py>

  <ui_controller_py FILE="ui_controller.py" TYPE="CONTROLLER_MODULE">
    <annotation>Прослойка между UI и бэкендом для тестируемости.</annotation>
    <UIController_CLASS NAME="UIController" TYPE="IS_CLASS_OF_MODULE">
      <handle_generate_METHOD NAME="handle_generate" TYPE="IS_METHOD_OF_CLASS">
        <annotation>Вызывает генератор и возвращает данные для таблицы.</annotation>
        <CrossLinks>
          <Link TARGET="datagenerator_py_DataGenerator_generate_points_METHOD" TYPE="CALLS_METHOD" />
        </CrossLinks>
      </handle_generate_METHOD>
      <handle_draw_METHOD NAME="handle_draw" TYPE="IS_METHOD_OF_CLASS">
        <annotation>Подготавливает данные для Plotly/Matplotlib.</annotation>
      </handle_draw_METHOD>
    </UIController_CLASS>
  </ui_controller_py>

  <app_py FILE="app.py" TYPE="UI_MODULE">
    <annotation>Точка входа, описание интерфейса Gradio.</annotation>
  </app_py>
</DraftCodeGraph>
```

---

### 2. Step-by-step Data Flow (Пошаговый Поток Данных)

1.  **Инициализация:** При старте `DataGenerator` проверяет наличие таблицы в `parabola.db`.
2.  **Генерация:** 
    - Пользователь вводит `a` и `c` в Gradio.
    - `app.py` вызывает `UIController.handle_generate(a, c)`.
    - `UIController` вызывает `DataGenerator.generate_points(a, c)`.
    - `DataGenerator` очищает старые данные, считает новые в цикле (или векторизованно) и делает `commit` в SQLite.
3.  **Отображение:**
    - `UIController` возвращает `pandas.DataFrame` в `app.py`.
    - Gradio отображает DataFrame в компоненте `gr.Dataframe`.
4.  **Визуализация:**
    - Пользователь жмет "Draw".
    - `UIController.handle_draw()` запрашивает данные из БД и возвращает объект фигуры (Plotly).

---

### 3. Acceptance Criteria (Критерии Приемки)

- [ ] **Бэкенд:** `pytest test_datagenerator.py` проходит (проверка CRUD операций в SQLite).
- [ ] **Контроллер:** `pytest test_ui_controller.py` проходит (проверка логики без запуска браузера).
- [ ] **Интерфейс:** При запуске `python app.py` открывается Gradio, кнопки работают корректно.
- [ ] **Разметка:** Все файлы содержат `START_MODULE_CONTRACT`, `MODULE_MAP` и логические блоки.

$END_DEV_PLAN
