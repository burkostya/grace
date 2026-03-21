$START_DOC_NAME: lesson_10/business_requirements.md

**PURPOSE:** Создание учебного приложения для генерации и визуализации параболы с соблюдением архитектурных стандартов (изоляция слоев, Agentic UX, LDD).
**SCOPE:** Генерация данных, хранение в SQLite, управление конфигурацией, CLI и Gradio UI.
**KEYWORDS:** DOMAIN(Education), PATTERN(Layered Architecture), TECH(Python, Gradio, SQLite, Plotly)

$START_DOCUMENT_PLAN
### План Документа
**SECTION_GOALS:**
- GOAL Реализация расчета параболы y = ax^2 + c => GOAL_PARABOLA_CALC
- GOAL Управление состоянием через config.json => GOAL_CONFIG_MGMT
- GOAL Хранение данных в SQLite => GOAL_DB_STORAGE
- GOAL Предоставление CLI для автономных агентов => GOAL_CLI_UX
- GOAL Интерактивный UI на Gradio => GOAL_GRADIO_UI

**SECTION_USE_CASES:**
- USE_CASE Пользователь -> Изменяет параметры -> Параметры сохраняются в config.json => UC_UPDATE_CONFIG
- USE_CASE Пользователь/CLI -> Запускает генерацию -> Данные в БД обновляются => UC_GENERATE_DATA
- USE_CASE Пользователь -> Нажимает Draw Graph -> Отображается график Plotly => UC_DRAW_GRAPH
- USE_CASE CLI -> Экспорт в CSV -> Создается файл с данными => UC_EXPORT_CSV
$END_DOCUMENT_PLAN

$START_SECTION_FUNCTIONAL_REQUIREMENTS
### Функциональные требования

$START_ARTIFACT_CONFIG_MGMT
#### Управление конфигурацией
**TYPE:** GOAL
**KEYWORDS:** StateManagement, JSON

$START_CONTRACT
**PURPOSE:** Обеспечить сохранение и чтение параметров a, c, x_min, x_max.
**DESCRIPTION:** Модуль config_manager.py должен атомарно читать и записывать config.json в папке урока.
**RATIONALE:** Изоляция управления состоянием от бизнес-логики.
**ACCEPTANCE_CRITERIA:**
- Файл config.json создается автоматически с дефолтными значениями.
- Изменения в UI или CLI корректно отражаются в файле.
$END_CONTRACT
$END_ARTIFACT_CONFIG_MGMT

$START_ARTIFACT_DB_STORAGE
#### Хранение данных
**TYPE:** GOAL
**KEYWORDS:** SQLite, Persistence

$START_CONTRACT
**PURPOSE:** Хранение вычисленных точек параболы.
**DESCRIPTION:** Таблица `points` с колонками `x`, `y`.
**RATIONALE:** Обеспечение доступа к данным для UI и CLI независимо от процесса генерации.
**ACCEPTANCE_CRITERIA:**
- Данные сохраняются в lesson_10/data.db.
- Таблица очищается перед новой генерацией.
$END_CONTRACT
$END_ARTIFACT_DB_STORAGE

$END_SECTION_FUNCTIONAL_REQUIREMENTS

$END_DOC_NAME
