$START_DEV_PLAN

**PURPOSE:** План реализации учебного приложения "Parabola Pro" в папке lesson_v2.

---

### 1. Draft Code Graph (Черновой Граф Кода)

```xml
<DraftCodeGraph>
  <lesson_v2_src_data_generator_py FILE="lesson_v2/src/data_generator.py" TYPE="BACKEND_MODULE">
    <annotation>Логика расчета и работа с БД SQLite.</annotation>
    <DataGeneratorPro_CLASS NAME="DataGeneratorPro" TYPE="IS_CLASS_OF_MODULE">
      <generate_points_METHOD NAME="generate_points" TYPE="IS_METHOD_OF_CLASS">
        <annotation>Расчет y=ax^2+c в диапазоне [x_min, x_max].</annotation>
      </generate_points_METHOD>
    </DataGeneratorPro_CLASS>
  </lesson_v2_src_data_generator_py>

  <lesson_v2_src_ui_controller_py FILE="lesson_v2/src/ui_controller.py" TYPE="CONTROLLER_MODULE">
    <annotation>Координация между UI и Backend.</annotation>
    <UIControllerPro_CLASS NAME="UIControllerPro" TYPE="IS_CLASS_OF_MODULE">
      <handle_generate_METHOD NAME="handle_generate" TYPE="IS_METHOD_OF_CLASS" />
      <handle_draw_METHOD NAME="handle_draw" TYPE="IS_METHOD_OF_CLASS" />
    </UIControllerPro_CLASS>
  </lesson_v2_src_ui_controller_py>

  <lesson_v2_src_main_py FILE="lesson_v2/src/main.py" TYPE="UI_MODULE">
    <annotation>Точка входа, описание Gradio интерфейса.</annotation>
  </lesson_v2_src_main_py>

  <lesson_v2_tests_test_app_py FILE="lesson_v2/tests/test_app.py" TYPE="TEST_MODULE">
    <annotation>Интеграционные тесты всего цикла.</annotation>
  </lesson_v2_tests_test_app_py>
</DraftCodeGraph>
```

---

### 2. Step-by-step Data Flow (Пошаговый Поток Данных)

1.  **Input:** Пользователь вводит `a, c, x_min, x_max` в UI.
2.  **Action:** `UIControllerPro` получает данные и вызывает `DataGeneratorPro.generate_points()`.
3.  **Storage:** `DataGeneratorPro` создает/очищает `parabola_pro.db` и записывает новые точки.
4.  **Fetch:** `UIControllerPro` запрашивает данные из БД для таблицы и графика.
5.  **Output:** Gradio отображает `pandas.DataFrame` и `plotly.Figure`.

---

### 3. Acceptance Criteria (Критерии Приемки)

- [ ] **Backend Test:** `pytest lesson_v2/tests/` подтверждает корректность расчетов в БД.
- [ ] **UI Logic Test:** Тесты контроллера имитируют нажатие кнопок и проверяют возвращаемые типы (DataFrame, Figure).
- [ ] **Isolation:** Все файлы (БД, логи, код) находятся внутри `lesson_v2/`.
- [ ] **Markup:** 100% файлов используют семантическую разметку KiloCode.

$END_DEV_PLAN
