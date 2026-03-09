$START_DEV_PLAN

**PURPOSE:** План разработки учебного приложения Lesson 9 (Парабола) с соблюдением стандартов Agentic UX, LDD и изоляции слоев.

---

### 1. Draft Code Graph (Черновой Граф Кода)

```xml
<DraftCodeGraph>
  <lesson_9_src_config_manager_py FILE="lesson_9/src/config_manager.py" TYPE="MODULE">
    <annotation>Управление файлом config.json (чтение/запись параметров a, c, x_min, x_max).</annotation>
  </lesson_9_src_config_manager_py>
  
  <lesson_9_src_database_manager_py FILE="lesson_9/src/database_manager.py" TYPE="MODULE">
    <annotation>Работа с SQLite: создание таблицы, сохранение точек, чтение для графиков/экспорта.</annotation>
  </lesson_9_src_database_manager_py>
  
  <lesson_9_src_parabola_logic_py FILE="lesson_9/src/parabola_logic.py" TYPE="MODULE">
    <annotation>Математическое ядро: расчет y = ax^2 + c.</annotation>
  </lesson_9_src_parabola_logic_py>
  
  <lesson_9_src_cli_py FILE="lesson_9/src/cli.py" TYPE="MODULE">
    <annotation>Agentic UX: команды generate и export-csv.</annotation>
    <CrossLinks>
      <Link TARGET="lesson_9_src_config_manager_py" TYPE="USES" />
      <Link TARGET="lesson_9_src_database_manager_py" TYPE="USES" />
      <Link TARGET="lesson_9_src_parabola_logic_py" TYPE="USES" />
    </CrossLinks>
  </lesson_9_src_cli_py>
  
  <lesson_9_src_ui_controller_py FILE="lesson_9/src/ui_controller.py" TYPE="MODULE">
    <annotation>Gradio UI: обработчики кнопок, построение Plotly графиков.</annotation>
    <CrossLinks>
      <Link TARGET="lesson_9_src_config_manager_py" TYPE="USES" />
      <Link TARGET="lesson_9_src_database_manager_py" TYPE="USES" />
      <Link TARGET="lesson_9_src_parabola_logic_py" TYPE="USES" />
    </CrossLinks>
  </lesson_9_src_ui_controller_py>
  
  <run_lesson_9_py FILE="run_lesson_9.py" TYPE="ENTRY_POINT">
    <annotation>Запуск Gradio сервера.</annotation>
  </run_lesson_9_py>
</DraftCodeGraph>
```

---

### 2. Step-by-step Data Flow (Пошаговый Поток Данных)

1.  **Инициализация:** Приложение проверяет наличие `config.json`. Если его нет, создаются дефолтные значения.
2.  **Ввод (UI/CLI):** Пользователь меняет параметры. В UI это ползунки, в CLI это чтение из конфига.
3.  **Генерация:**
    *   `config_manager` сохраняет текущие параметры.
    *   `parabola_logic` вычисляет массив точек (x, y).
    *   `database_manager` очищает старые данные и записывает новые в SQLite.
4.  **Отображение:**
    *   UI запрашивает данные из БД и обновляет `Dataframe` компонент.
    *   При нажатии "Draw Graph" UI запрашивает данные из БД и строит Plotly Figure.
5.  **Экспорт:** CLI команда `export-csv` читает данные из БД и пишет в файл.

---

### 3. Acceptance Criteria (Критерии Приемки)

- [ ] **Критерий 1:** Все модули содержат семантическую разметку (START_BLOCK, CONTRACT).
- [ ] **Критерий 2:** Логирование LDD 2.0 ведется в `lesson_9/app_9.log` с использованием IMP:1-10.
- [ ] **Критерий 3:** CLI команда `generate` работает без аргументов, используя `config.json`.
- [ ] **Критерий 4:** Тесты покрывают 100% логики, включая Headless UI тесты.
- [ ] **Критерий 5:** Создан локальный `lesson_9/AppGraph.xml`.

$END_DEV_PLAN
