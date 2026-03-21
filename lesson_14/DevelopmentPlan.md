$START_DEV_PLAN

**PURPOSE:** Создание учебного приложения Lesson 14 для демонстрации работы фреймворка с тригонометрическими функциями, семантической разметкой, LDD и Agentic UX.

---

### 1. Draft Code Graph (Черновой Граф Кода)

```xml
<DraftCodeGraph>
  <Lesson_14_Info FILE="lesson_14/AppGraph.xml" TYPE="LESSON_INFO">
    <keywords>Trigonometry, Gradio, SQLite, LDD 2.0, Agentic UX</keywords>
    <terms>
      <term name="LDD 2.0">Log Driven Development version 2.0 with importance levels [IMP:1-10]</term>
      <term name="Agentic UX">User experience designed for AI agents to interact with and understand</term>
      <term name="Trigonometry">Mathematical functions sin, cos, tan</term>
    </terms>
    <annotation>
      Project for calculating, storing, and visualizing trigonometric functions using a Gradio web interface and a CLI tool.
    </annotation>
    <BusinessScenarios>
      <Scenario>User enters trigonometric parameters in UI -> System calculates points -> Points saved to DB -> Graph rendered</Scenario>
      <Scenario>User uses CLI to generate points based on config -> Points saved to DB</Scenario>
      <Scenario>User uses CLI to export points from DB to CSV</Scenario>
    </BusinessScenarios>
  </Lesson_14_Info>

  <lesson_14_src_config_manager_py FILE="lesson_14/src/config_manager.py" TYPE="DATA_PROCESSING_MODULE">
    <annotation>Manages application configuration and state via a JSON file.</annotation>
    <ConfigManager_CLASS NAME="ConfigManager" TYPE="IS_CLASS_OF_MODULE">
      <annotation>Класс для управления конфигурацией приложения.</annotation>
      <load_config_METHOD NAME="load_config" TYPE="IS_METHOD_OF_CLASS">
        <annotation>Загружает конфигурацию из файла или возвращает дефолтные значения.</annotation>
      </load_config_METHOD>
      <save_config_METHOD NAME="save_config" TYPE="IS_METHOD_OF_CLASS">
        <annotation>Сохраняет текущую или новую конфигурацию в файл.</annotation>
      </save_config_METHOD>
    </ConfigManager_CLASS>
  </lesson_14_src_config_manager_py>

  <lesson_14_src_database_manager_py FILE="lesson_14/src/database_manager.py" TYPE="DATA_PROCESSING_MODULE">
    <annotation>Manages data storage in SQLite for trigonometric points.</annotation>
    <DatabaseManager_CLASS NAME="DatabaseManager" TYPE="IS_CLASS_OF_MODULE">
      <annotation>Класс для управления базой данных.</annotation>
      <init_db_METHOD NAME="init_db" TYPE="IS_METHOD_OF_CLASS">
        <annotation>Инициализирует схему базы данных.</annotation>
      </init_db_METHOD>
      <save_points_METHOD NAME="save_points" TYPE="IS_METHOD_OF_CLASS">
        <annotation>Сохраняет список точек в базу данных после очистки старых данных.</annotation>
      </save_points_METHOD>
      <get_points_METHOD NAME="get_points" TYPE="IS_METHOD_OF_CLASS">
        <annotation>Извлекает все точки из базы данных.</annotation>
      </get_points_METHOD>
    </DatabaseManager_CLASS>
  </lesson_14_src_database_manager_py>

  <lesson_14_src_trig_logic_py FILE="lesson_14/src/trig_logic.py" TYPE="DATA_PROCESSING_MODULE">
    <calculate_trig_points_FUNC NAME="calculate_trig_points" TYPE="IS_FUNCTION_OF_MODULE">
      <annotation>Реализует математическую логику для расчета тригонометрических точек y = sin(x), cos(x), tan(x).</annotation>
    </calculate_trig_points_FUNC>
  </lesson_14_src_trig_logic_py>

  <lesson_14_src_ui_controller_py FILE="lesson_14/src/ui_controller.py" TYPE="IS_CLASS_OF_MODULE">
    <annotation>UI контроллер для управления логикой Gradio и координации между логикой и БД.</annotation>
    <UIController_CLASS NAME="UIController" TYPE="IS_CLASS_OF_MODULE">
      <CrossLinks>
        <Link TARGET="lesson_14_src_database_manager_py" TYPE="CREATES_INSTANCE_OF"/>
        <Link TARGET="lesson_14_src_config_manager_py" TYPE="CREATES_INSTANCE_OF"/>
        <Link TARGET="lesson_14_src_trig_logic_py" TYPE="CALLS_FUNCTION"/>
      </CrossLinks>
      <handle_generate_data_METHOD NAME="handle_generate_data" TYPE="IS_METHOD_OF_CLASS">
        <annotation>Обрабатывает нажатие кнопки "Generate Data": сохраняет конфиг, рассчитывает точки, сохраняет в БД.</annotation>
      </handle_generate_data_METHOD>
      <handle_draw_graph_METHOD NAME="handle_draw_graph" TYPE="IS_METHOD_OF_CLASS">
        <annotation>Обрабатывает нажатие кнопки "Draw Graph": читает из БД и строит Plotly фигуру.</annotation>
      </handle_draw_graph_METHOD>
    </UIController_CLASS>
  </lesson_14_src_ui_controller_py>

  <lesson_14_src_cli_py FILE="lesson_14/src/cli.py" TYPE="DATA_PROCESSING_MODULE">
    <main_FUNC NAME="main" TYPE="IS_FUNCTION_OF_MODULE">
      <annotation>CLI точка входа для генерации точек и экспорта в CSV.</annotation>
      <CrossLinks>
        <Link TARGET="lesson_14_src_config_manager_py" TYPE="USES_CLASS"/>
        <Link TARGET="lesson_14_src_database_manager_py" TYPE="USES_CLASS"/>
        <Link TARGET="lesson_14_src_trig_logic_py" TYPE="CALLS_FUNCTION"/>
      </CrossLinks>
    </main_FUNC>
  </lesson_14_src_cli_py>

  <run_lesson_14_py FILE="run_lesson_14.py" TYPE="DATA_PROCESSING_MODULE">
    <main_FUNC NAME="main" TYPE="IS_FUNCTION_OF_MODULE">
      <annotation>Точка входа для запуска Gradio приложения.</annotation>
      <CrossLinks>
        <Link TARGET="lesson_14_src_ui_controller_py" TYPE="CREATES_INSTANCE_OF"/>
      </CrossLinks>
    </main_FUNC>
  </run_lesson_14_py>

  <ProjectCrossLinks TYPE="MODULE_INTERACTIONS_OVERVIEW">
    <Link SOURCE="run_lesson_14_py" TARGET="lesson_14_src_ui_controller_py" TYPE="INITIALIZES"/>
    <Link SOURCE="lesson_14_src_ui_controller_py" TARGET="lesson_14_src_trig_logic_py" TYPE="DEPENDS_ON"/>
    <Link SOURCE="lesson_14_src_ui_controller_py" TARGET="lesson_14_src_database_manager_py" TYPE="DEPENDS_ON"/>
    <Link SOURCE="lesson_14_src_ui_controller_py" TARGET="lesson_14_src_config_manager_py" TYPE="DEPENDS_ON"/>
    <Link SOURCE="lesson_14_src_cli_py" TARGET="lesson_14_src_trig_logic_py" TYPE="DEPENDS_ON"/>
    <Link SOURCE="lesson_14_src_cli_py" TARGET="lesson_14_src_database_manager_py" TYPE="DEPENDS_ON"/>
    <Link SOURCE="lesson_14_src_cli_py" TARGET="lesson_14_src_config_manager_py" TYPE="DEPENDS_ON"/>
  </ProjectCrossLinks>
</DraftCodeGraph>
```

---

### 2. Step-by-step Data Flow (Пошаговый Поток Данных)

1. **Шаг 1: Инициализация приложения**
   - Пользователь запускает `run_lesson_14.py`
   - Создается экземпляр `UIController`
   - Контроллер инициализирует `DatabaseManager` и `ConfigManager`
   - Логируется инициализация с IMP:7

2. **Шаг 2: Генерация данных через UI**
   - Пользователь вводит параметры (функция, диапазон x, количество точек)
   - Нажимает кнопку "Generate Data"
   - Контроллер вызывает `handle_generate_data`:
     - Сохраняет параметры в `config.json`
     - Вызывает `calculate_trig_points` для расчета точек
     - Сохраняет точки в SQLite БД
     - Возвращает DataFrame для отображения
   - Логируется каждый шаг с соответствующим IMP уровнем

3. **Шаг 3: Отрисовка графика**
   - Пользователь нажимает кнопку "Draw Graph"
   - Контроллер вызывает `handle_draw_graph`
   - Извлекает точки из БД
   - Создает Plotly Figure с графиком
   - Возвращает Figure для отображения в UI
   - Логируется процесс создания графика

4. **Шаг 4: CLI операции**
   - Агент вызывает `python -m lesson_14.src.cli generate`
   - CLI читает параметры из `config.json`
   - Вызывает `calculate_trig_points`
   - Сохраняет точки в БД
   - Возвращает exit code 0

5. **Шаг 5: Экспорт данных**
   - Агент вызывает `python -m lesson_14.src.cli export-csv --out <filename>`
   - CLI читает точки из БД
   - Экспортирует в CSV файл
   - Возвращает exit code 0

---

### 3. Acceptance Criteria (Критерии Приемки)

- [ ] **Критерий 1:** Приложение использует семантическую разметку (START_MODULE_CONTRACT, START_FUNCTION, START_BLOCK, KEYWORDS, LINKS)
- [ ] **Критерий 2:** Логирование соответствует LDD 2.0 (шкала IMP:1-10, AI Belief State в критических точках)
- [ ] **Критерий 3:** CLI поддерживает команды `generate` и `export-csv --out <filename>` с exit code 0
- [ ] **Критерий 4:** UI на Gradio имеет две колонки (управление + таблица | график)
- [ ] **Критерий 5:** Backend тесты используют `caplog` для вывода логов IMP:7-10
- [ ] **Критерий 6:** CLI тесты проходят через `subprocess.run`
- [ ] **Критерий 7:** UI тесты проходят через headless-тестирование (эмуляция кликов)
- [ ] **Критерий 8:** Создан локальный `AppGraph.xml` в папке урока
- [ ] **Критерий 9:** Создан `business_requirements.md` с описанием целей

$END_DEV_PLAN
