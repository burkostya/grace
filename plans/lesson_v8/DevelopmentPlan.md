$START_DEV_PLAN

**PURPOSE:** Проектирование учебного приложения lesson_v8 для генерации точек параболы с соблюдением стандартов Agentic UX, LDD и изоляции слоев.

---

### 1. Draft Code Graph (Черновой Граф Кода)

```xml
<DraftCodeGraph>
  <lesson_v8_config_json FILE="lesson_v8/config.json" TYPE="DATA_FILE">
    <annotation>Файл конфигурации параметров параболы.</annotation>
  </lesson_v8_config_json>

  <config_manager_py FILE="lesson_v8/src/config_manager.py" TYPE="UTILITY">
    <annotation>Управление чтением и записью config.json.</annotation>
  </config_manager_py>

  <parabola_logic_py FILE="lesson_v8/src/parabola_logic.py" TYPE="BUSINESS_LOGIC">
    <annotation>Математический расчет точек параболы y = ax^2 + c.</annotation>
  </parabola_logic_py>

  <database_manager_py FILE="lesson_v8/src/database_manager.py" TYPE="DATA_ACCESS">
    <annotation>Работа с SQLite: создание таблиц, сохранение и чтение точек.</annotation>
  </database_manager_py>

  <cli_py FILE="lesson_v8/src/cli.py" TYPE="INTERFACE">
    <annotation>CLI интерфейс для автономной генерации и экспорта данных.</annotation>
    <CrossLinks>
      <Link TARGET="config_manager_py" TYPE="USES" />
      <Link TARGET="parabola_logic_py" TYPE="USES" />
      <Link TARGET="database_manager_py" TYPE="USES" />
    </CrossLinks>
  </cli_py>

  <ui_controller_py FILE="lesson_v8/src/ui_controller.py" TYPE="INTERFACE">
    <annotation>Контроллер Gradio: обработка ввода, вызов логики и построение графиков.</annotation>
    <CrossLinks>
      <Link TARGET="config_manager_py" TYPE="USES" />
      <Link TARGET="parabola_logic_py" TYPE="USES" />
      <Link TARGET="database_manager_py" TYPE="USES" />
    </CrossLinks>
  </ui_controller_py>

  <run_lesson_v8_py FILE="run_lesson_v8.py" TYPE="ENTRY_POINT">
    <annotation>Точка запуска Gradio сервера.</annotation>
    <CrossLinks>
      <Link TARGET="ui_controller_py" TYPE="CALLS" />
    </CrossLinks>
  </run_lesson_v8_py>
</DraftCodeGraph>
```

---

### 2. Step-by-step Data Flow (Пошаговый Поток Данных)

1. **Инициализация:** При запуске UI или CLI проверяется наличие `config.json`. Если его нет, создается файл с параметрами по умолчанию (a=1, c=0, x_min=-10, x_max=10).
2. **Генерация (CLI/UI):**
   * Считываются параметры из `config.json` (или из полей ввода UI).
   * `parabola_logic.py` генерирует список точек (x, y) на основе векторизованных операций (numpy/pandas).
   * `database_manager.py` очищает старые данные и записывает новые в SQLite таблицу `points`.
   * Логируется AI Belief State: "Ожидаю параболу с вершиной в (0, c)".
3. **Отображение (UI):**
   * `ui_controller.py` запрашивает данные из БД.
   * Данные передаются в `gr.Dataframe` для таблицы.
   * Данные передаются в Plotly для построения интерактивного графика.
4. **Экспорт (CLI):**
   * Команда `export-csv` считывает данные из БД и сохраняет их через `pandas.to_csv()`.

---

### 3. Acceptance Criteria (Критерии Приемки)

- [ ] **Критерий 1:** Все файлы созданы в папке `lesson_v8/` (кроме `run_lesson_v8.py`).
- [ ] **Критерий 2:** Код содержит полную семантическую разметку и LDD логи `[IMP:1-10]`.
- [ ] **Критерий 3:** CLI команда `python lesson_v8/src/cli.py generate` успешно обновляет БД.
- [ ] **Критерий 4:** UI запускается через `python run_lesson_v8.py` и корректно отображает график.
- [ ] **Критерий 5:** Тесты `pytest lesson_v8/tests/` проходят успешно с покрытием 100% бизнес-логики и выводом логов `[IMP:7-10]`.
- [ ] **Критерий 6:** Создан локальный `lesson_v8/AppGraph.xml`.

---

### 4. Detailed Module Specifications (Детальная Спецификация Модулей)

#### 4.1. config_manager.py
**Отвечает за:** Чтение и запись конфигурации в JSON формате.
**Ключевые функции:**
- `load_config()` - загружает конфиг из файла, создает дефолтный если отсутствует
- `save_config(config_dict)` - сохраняет конфиг в файл
**Логирование:** IMP:7-8 для операций чтения/записи файла

#### 4.2. parabola_logic.py
**Отвечает за:** Математические вычисления точек параболы.
**Ключевые функции:**
- `generate_parabola_points(a, c, x_min, x_max, num_points=100)` - генерирует DataFrame с точками
**Логирование:** IMP:9-10 для AI Belief State о форме параболы

#### 4.3. database_manager.py
**Отвечает за:** Работу с SQLite базой данных.
**Ключевые функции:**
- `init_database()` - создает таблицу points если не существует
- `clear_points()` - очищает таблицу
- `save_points(df)` - сохраняет DataFrame в БД
- `load_points()` - загружает точки из БД в DataFrame
**Логирование:** IMP:7-8 для операций с БД

#### 4.4. cli.py
**Отвечает за:** CLI интерфейс для автономного управления.
**Ключевые команды:**
- `generate` - генерация точек с параметрами из config.json
- `export-csv --out <filename>` - экспорт данных в CSV
**Логирование:** IMP:9-10 для логики команд

#### 4.5. ui_controller.py
**Отвечает за:** Gradio интерфейс и обработку событий.
**Ключевые функции:**
- `handle_generate(a, c, x_min, x_max)` - обработчик кнопки Generate Data
- `handle_draw_graph()` - обработчик кнопки Draw Graph
- `create_interface()` - создание Gradio интерфейса
**Логирование:** IMP:7-10 для UI событий

---

### 5. Testing Strategy (Стратегия Тестирования)

#### 5.1. Backend & LDD Tests (test_app.py)
- Тест загрузки конфига с дефолтными значениями
- Тест сохранения и загрузки конфига
- Тест генерации точек параболы (проверка формулы y = ax^2 + c)
- Тест сохранения и загрузки точек в БД
- **Обязательно:** Использование `caplog` для вывода логов IMP:7-10

#### 5.2. CLI Smoke Tests
- Тест команды `generate` через `subprocess.run`
- Тест команды `export-csv` через `subprocess.run`
- Проверка exit code 0 и корректного вывода

#### 5.3. UI Headless Tests
- Тест обработчика `handle_generate` (проверка типа возвращаемого DataFrame)
- Тест обработчика `handle_draw_graph` (проверка типа Plotly Figure)
- Проверка обновления config.json

---

### 6. File Structure (Структура Файлов)

```
lesson_v8/
├── __init__.py
├── config.json
├── src/
│   ├── __init__.py
│   ├── cli.py
│   ├── config_manager.py
│   ├── database_manager.py
│   ├── parabola_logic.py
│   └── ui_controller.py
├── tests/
│   ├── __init__.py
│   └── test_app.py
└── AppGraph.xml

run_lesson_v8.py (в корне проекта)
```

---

### 7. Implementation Order (Порядок Реализации)

1. Создать структуру папок lesson_v8/
2. Реализовать config_manager.py (базовый модуль)
3. Реализовать parabola_logic.py (бизнес-логика)
4. Реализовать database_manager.py (доступ к данным)
5. Реализовать cli.py (CLI интерфейс)
6. Реализовать ui_controller.py (Gradio интерфейс)
7. Создать run_lesson_v8.py (точка запуска)
8. Написать тесты (test_app.py)
9. Создать AppGraph.xml (после успешного прохождения тестов)

---

### 8. Key Constraints (Ключевые Ограничения)

- **ЗАПРЕЩЕНО:** Создавать новые виртуальные окружения
- **ЗАПРЕЩЕНО:** Читая код предыдущих уроков для генерации нового
- **ОБЯЗАТЕЛЬНО:** Использовать семантический экзоскелет (START_BLOCK, MODULE_CONTRACT)
- **ОБЯЗАТЕЛЬНО:** Логирование в файл lesson_v8/app_v8.log с форматом [IMP:1-10]
- **ОБЯЗАТЕЛЬНО:** 100% покрытие бизнес-логики тестами
- **ОБЯЗАТЕЛЬНО:** Создание локального AppGraph.xml только после успешных тестов

---

$END_DEV_PLAN
