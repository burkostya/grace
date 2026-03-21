$START_DOC_NAME: business_requirements.md

**PURPOSE:** Создание учебного приложения Lesson_16 для демонстрации фреймворка промптов (LDD, Agentic UX, Headless Testing).
**SCOPE:** Генерация точек параболы, хранение в SQLite, UI на Gradio, CLI управление.
**KEYWORDS:** [DOMAIN: Education; CONCEPT: Parabola Generation; TECH: Gradio, SQLite, Plotly]

$START_DOCUMENT_PLAN
### План Документа
**SECTION_GOALS:**
- GOAL Реализовать расчет точек параболы y = ax^2 + c => [GOAL_CALCULATION]
- GOAL Обеспечить хранение параметров в config.json => [GOAL_CONFIG_STORAGE]
- GOAL Реализовать хранение точек в SQLite => [GOAL_DB_STORAGE]
- GOAL Создать UI на Gradio с двумя колонками => [GOAL_UI_GRADIO]
- GOAL Создать CLI для автономного управления => [GOAL_CLI_UX]
- GOAL Покрыть логику тестами (Backend, CLI, UI) => [GOAL_TESTING]

**SECTION_USE_CASES:**
- USE_CASE Пользователь генерирует данные через UI => [UC_UI_GENERATE]
- USE_CASE Пользователь строит график через UI => [UC_UI_PLOT]
- USE_CASE Агент генерирует данные через CLI => [UC_CLI_GENERATE]
- USE_CASE Агент экспортирует данные в CSV через CLI => [UC_CLI_EXPORT]
$END_DOCUMENT_PLAN

$START_SECTION_FUNCTIONAL_REQUIREMENTS
### Функциональные требования

$START_ARTIFACT_GOAL_CALCULATION
#### Расчет параболы
**TYPE:** GOAL
**KEYWORDS:** [CONCEPT: Math; TECH: Python]
$START_CONTRACT
**PURPOSE:** Вычисление значений y для заданного диапазона x.
**DESCRIPTION:** На основе параметров a, c, x_min, x_max генерируется набор точек (x, y).
**RATIONALE:** Базовая математическая логика приложения.
**ACCEPTANCE_CRITERIA:** Корректный расчет y = ax^2 + c для всех x в диапазоне.
$END_CONTRACT
$END_ARTIFACT_GOAL_CALCULATION

$START_ARTIFACT_GOAL_CONFIG_STORAGE
#### Управление конфигурацией
**TYPE:** GOAL
**KEYWORDS:** [FORMAT: JSON; TECH: config_manager]
$START_CONTRACT
**PURPOSE:** Сохранение и чтение параметров a, c, x_min, x_max.
**DESCRIPTION:** Использование config.json для синхронизации состояния между UI и CLI.
**RATIONALE:** State Management через файловую систему.
**ACCEPTANCE_CRITERIA:** Параметры сохраняются при изменении в UI и считываются CLI.
$END_CONTRACT
$END_ARTIFACT_GOAL_CONFIG_STORAGE

$START_ARTIFACT_GOAL_DB_STORAGE
#### Хранение в БД
**TYPE:** GOAL
**KEYWORDS:** [TECH: SQLite; DOMAIN: Data Persistence]
$START_CONTRACT
**PURPOSE:** Сохранение рассчитанных точек в базу данных.
**DESCRIPTION:** Таблица 'points' с колонками x, y.
**RATIONALE:** Демонстрация работы с персистентным хранилищем.
**ACCEPTANCE_CRITERIA:** Данные успешно записываются и считываются из SQLite.
$END_CONTRACT
$END_ARTIFACT_GOAL_DB_STORAGE

$START_ARTIFACT_GOAL_UI_GRADIO
#### Интерфейс Gradio
**TYPE:** GOAL
**KEYWORDS:** [TECH: Gradio; UI: Two-Column]
$START_CONTRACT
**PURPOSE:** Визуальное управление и отображение данных.
**DESCRIPTION:** Левая колонка: ввод параметров, кнопка "Generate Data", кнопка "Draw Graph", таблица. Правая колонка: график Plotly.
**RATIONALE:** User Experience для человека.
**ACCEPTANCE_CRITERIA:** UI корректно отображает таблицу и график после нажатия соответствующих кнопок.
$END_CONTRACT
$END_ARTIFACT_GOAL_UI_GRADIO

$START_ARTIFACT_GOAL_CLI_UX
#### CLI (Agentic UX)
**TYPE:** GOAL
**KEYWORDS:** [TECH: argparse; CONCEPT: Agentic UX]
$START_CONTRACT
**PURPOSE:** Автономное управление бэкендом.
**DESCRIPTION:** Команды 'generate' (использует config.json) и 'export-csv --out <file>'.
**RATIONALE:** Возможность управления приложением без UI (для агентов).
**ACCEPTANCE_CRITERIA:** Команды выполняются успешно и производят ожидаемый эффект.
$END_CONTRACT
$END_ARTIFACT_GOAL_CLI_UX

$END_SECTION_FUNCTIONAL_REQUIREMENTS

$START_SECTION_USE_CASES
### Сценарии использования

$START_ARTIFACT_UC_UI_GENERATE
#### Генерация через UI
**TYPE:** USE_CASE
$START_CONTRACT
**PURPOSE:** Пользователь хочет обновить данные.
**DESCRIPTION:** User -> Вводит a, c, x_min, x_max -> Нажимает "Generate Data" -> Параметры в config.json, точки в БД, таблица обновлена.
**RATIONALE:** Основной флоу работы с данными.
**ACCEPTANCE_CRITERIA:** Таблица в UI отображает новые данные.
$END_CONTRACT
$END_ARTIFACT_UC_UI_GENERATE

$END_SECTION_USE_CASES

$END_DOC_NAME
