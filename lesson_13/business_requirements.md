$START_DOC_NAME

**PURPOSE:** Создание учебного приложения Lesson_13 для демонстрации работы фреймворка с семантической разметкой, LDD и Agentic UX.
**SCOPE:** Генерация точек параболы, хранение в SQLite, UI на Gradio, CLI интерфейс и автоматизированное тестирование.
**KEYWORDS:** DOMAIN(Education), CONCEPT(Parabola Generation), TECH(Python, Gradio, SQLite, Plotly, Pytest)

$START_DOCUMENT_PLAN
### План Документа
**SECTION_GOALS:**
- GOAL Реализовать расчет точек параболы y = ax^2 + c => GOAL_PARABOLA_LOGIC
- GOAL Обеспечить хранение состояния в config.json => GOAL_STATE_MANAGEMENT
- GOAL Реализовать хранение данных в SQLite => GOAL_DB_STORAGE
- GOAL Создать Agentic UX через CLI => GOAL_CLI_INTERFACE
- GOAL Создать интерактивный UI на Gradio => GOAL_UI_INTERFACE
- GOAL Обеспечить 100% покрытие тестами с LDD => GOAL_TESTING_LDD

**SECTION_USE_CASES:**
- USE_CASE User -> Input Parameters -> Data Generated & Stored => UC_GENERATE_DATA
- USE_CASE User -> Click Draw -> Graph Displayed => UC_DRAW_GRAPH
- USE_CASE Agent -> CLI Command -> CSV Exported => UC_CLI_EXPORT
$END_DOCUMENT_PLAN

$START_SECTION_REQUIREMENTS
### Функциональные требования

$START_ARTIFACT_PARABOLA_LOGIC
#### Parabola Logic
**TYPE:** GOAL
**KEYWORDS:** Math, Algorithm
$START_CONTRACT
**PURPOSE:** Расчет значений y для заданного диапазона x.
**DESCRIPTION:** Функция принимает a, c, x_min, x_max и возвращает список кортежей (x, y).
**RATIONALE:** Основа бизнес-логики приложения.
**ACCEPTANCE_CRITERIA:** Точность расчетов соответствует формуле y = ax^2 + c.
$END_CONTRACT
$END_ARTIFACT_PARABOLA_LOGIC

$START_ARTIFACT_CLI_UX
#### Agentic CLI UX
**TYPE:** GOAL
**KEYWORDS:** CLI, Automation
$START_CONTRACT
**PURPOSE:** Предоставить интерфейс для автономных агентов.
**DESCRIPTION:** Команды `generate` (использует config.json) и `export-csv`.
**RATIONALE:** Позволяет внешним инструментам управлять бэкендом без UI.
**ACCEPTANCE_CRITERIA:** Команды выполняются успешно, возвращают exit code 0.
$END_CONTRACT
$END_ARTIFACT_CLI_UX

$END_SECTION_REQUIREMENTS

$END_DOC_NAME
