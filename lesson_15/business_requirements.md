$START_DOC_NAME

**PURPOSE:** Создание учебного приложения Lesson_15 для демонстрации работы фреймворка промптов (изоляция слоев, Agentic UX, Headless-тестирование, LDD).
**SCOPE:** Генерация точек параболы, сохранение в SQLite, визуализация через Gradio/Plotly, управление через CLI.
**KEYWORDS:** DOMAIN(Education): Parabola Generation; CONCEPT(Architecture): Layer Isolation, LDD 2.0, Agentic UX.

$START_DOCUMENT_PLAN
### План Документа

**SECTION_GOALS:**
- GOAL Реализовать расчет точек параболы и сохранение в БД => [GOAL_BACKEND]
- GOAL Создать CLI интерфейс для автономного управления => [GOAL_CLI]
- GOAL Разработать UI на Gradio с разделением на колонки => [GOAL_UI]
- GOAL Обеспечить 100% покрытие тестами с генерацией семантического контекста => [GOAL_TESTING]

**SECTION_USE_CASES:**
- USE_CASE User -> Input Parameters -> Data Generated & Saved => [UC_GENERATE]
- USE_CASE User -> Click Draw -> Graph Displayed => [UC_DRAW]
- USE_CASE Agent -> CLI Command -> CSV Exported => [UC_CLI_EXPORT]

$END_DOCUMENT_PLAN

$START_SECTION_REQUIREMENTS
### Бизнес-требования

$START_ARTIFACT_CONFIG
#### Configuration Management

**TYPE:** DATA_FORMAT
**KEYWORDS:** JSON, StateManagement

$START_CONTRACT
**PURPOSE:** Хранение параметров генерации (a, c, x_min, x_max).
**DESCRIPTION:** Файл `lesson_15/config.json`.
**RATIONALE:** Обеспечение консистентности параметров между UI, CLI и Backend.
**ACCEPTANCE_CRITERIA:**
- Чтение и запись через `config_manager.py`.
- Автоматическое использование параметров в CLI `generate`.
$END_CONTRACT
$END_ARTIFACT_CONFIG

$START_ARTIFACT_UI
#### Gradio UI Layout

**TYPE:** NFR
**KEYWORDS:** Gradio, Plotly, Two-Column

$START_CONTRACT
**PURPOSE:** Визуальное управление и отображение данных.
**DESCRIPTION:** 
- Левая колонка: Слайдеры (a, c, x_min, x_max), Кнопки "Generate Data" и "Draw Graph", Таблица.
- Правая колонка: Интерактивный график Plotly.
**RATIONALE:** Демонстрация разделения ответственности и удобства пользователя.
**ACCEPTANCE_CRITERIA:**
- Кнопка "Generate Data" обновляет БД и таблицу.
- Кнопка "Draw Graph" строит график на основе данных из БД.
$END_CONTRACT
$END_ARTIFACT_UI

$END_SECTION_REQUIREMENTS

$END_DOC_NAME
