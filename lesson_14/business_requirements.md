$START_DOC_NAME

**PURPOSE:** Создание учебного приложения Lesson 14 для демонстрации работы фреймворка с тригонометрическими функциями, семантической разметкой, LDD и Agentic UX.
**SCOPE:** Генерация точек тригонометрических функций (sin, cos, tan), хранение в SQLite, UI на Gradio, CLI интерфейс и автоматизированное тестирование.
**KEYWORDS:** DOMAIN(Education), CONCEPT(Trigonometry), TECH(Python, Gradio, SQLite, Plotly, Pytest)

$START_DOCUMENT_PLAN
### План Документа
**SECTION_GOALS:**
- GOAL Реализовать расчет точек тригонометрических функций sin, cos, tan => GOAL_TRIG_LOGIC
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

$START_ARTIFACT_TRIG_LOGIC
#### Trigonometry Logic
**TYPE:** GOAL
**KEYWORDS:** Math, Algorithm
$START_CONTRACT
**PURPOSE:** Расчет значений y для заданных тригонометрических функций (sin, cos, tan).
**DESCRIPTION:** Функция принимает функцию выбора (sin/cos/tan), диапазон x и количество точек, возвращает список кортежей (x, y).
**RATIONALE:** Основа бизнес-логики приложения для демонстрации математических вычислений.
**ACCEPTANCE_CRITERIA:** Точность расчетов соответствует стандартным математическим функциям Python.
$END_CONTRACT
$END_ARTIFACT_TRIG_LOGIC

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

$START_ARTIFACT_UI_INTERFACE
#### Gradio UI Interface
**TYPE:** GOAL
**KEYWORDS:** UI, Visualization
$START_CONTRACT
**PURPOSE:** Предоставить интерактивный интерфейс для пользователя.
**DESCRIPTION:** Две колонки: управление (слайдеры, кнопки, таблица) и график (Plotly).
**RATIONALE:** Демонстрация разделения слоев (Backend vs Frontend).
**ACCEPTANCE_CRITERIA:** UI корректно отображает данные и поддерживает все операции.
$END_CONTRACT
$END_ARTIFACT_UI_INTERFACE

$START_ARTIFACT_TESTING_LDD
#### Testing with LDD 2.0
**TYPE:** GOAL
**KEYWORDS:** Testing, LDD
$START_CONTRACT
**PURPOSE:** Обеспечить 100% покрытие тестами с семантическим контекстом.
**DESCRIPTION:** Тесты для Backend, CLI и UI с выводом логов IMP:7-10.
**RATIONALE:** Демонстрация методологии LDD для AI-агентов.
**ACCEPTANCE_CRITERIA:** Все тесты проходят, логи IMP:7-10 выводятся в консоль.
$END_CONTRACT
$END_ARTIFACT_TESTING_LDD

$END_SECTION_REQUIREMENTS

$END_DOC_NAME
