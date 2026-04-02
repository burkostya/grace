$START_DOC_NAME

**PURPOSE:** Создание учебного приложения Lesson 20 для демонстрации фреймворка промтов (изоляция слоев, Agentic UX, Headless-тестирование, LDD).
**SCOPE:** Генерация точек параболы y = ax^2 + c, сохранение в SQLite, визуализация через Gradio и Plotly.
**KEYWORDS:** [DOMAIN: Education; CONCEPT: Parabola Generation; TECH: Gradio, Plotly, SQLite, LDD]

$START_DOCUMENT_PLAN
### План Документа

**SECTION_GOALS:**
- GOAL Реализовать расчет точек параболы и сохранение в БД => [GOAL_CALC_DB]
- GOAL Обеспечить управление через Gradio с сохранением конфига => [GOAL_UI_CONFIG]
- GOAL Покрыть бизнес-логику тестами (Backend & UI Headless) => [GOAL_TESTING]

**SECTION_USE_CASES:**
- USE_CASE Пользователь вводит параметры -> Нажимает Generate -> Данные в БД и таблице => [UC_GENERATE]
- USE_CASE Пользователь нажимает Draw Graph -> График строится по данным из БД => [UC_DRAW]

$END_DOCUMENT_PLAN

$START_SECTION_REQUIREMENTS
### Функциональные требования

$START_ARTIFACT_CONFIG_MANAGER
#### Config Manager

**TYPE:** DATA_FORMAT
**KEYWORDS:** [CONCEPT: State Management; TECH: JSON]

$START_CONTRACT
**PURPOSE:** Управление файлом config.json (a, c, x_min, x_max).
**DESCRIPTION:** Модуль для чтения и записи параметров генерации.
**RATIONALE:** Изоляция управления состоянием от бизнес-логики.
**ACCEPTANCE_CRITERIA:** Параметры корректно сохраняются и считываются.
$END_CONTRACT
$END_ARTIFACT_CONFIG_MANAGER

$START_ARTIFACT_DB_MANAGER
#### DB Manager

**TYPE:** DATA_FORMAT
**KEYWORDS:** [TECH: SQLite]

$START_CONTRACT
**PURPOSE:** Хранение точек параболы (x, y).
**DESCRIPTION:** Создание таблицы и вставка/выборка данных.
**RATIONALE:** Демонстрация работы с персистентным хранилищем.
**ACCEPTANCE_CRITERIA:** Данные сохраняются без потерь и считываются для графика.
$END_CONTRACT
$END_ARTIFACT_DB_MANAGER

$END_SECTION_REQUIREMENTS

$END_DOC_NAME
