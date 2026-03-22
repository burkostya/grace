$START_DOC_NAME

**PURPOSE:** Бизнес-требования для учебного приложения Lesson 18 (Генератор параболы).
**SCOPE:** Генерация данных, хранение в SQLite, визуализация через Gradio/Plotly.
**KEYWORDS:** [DOMAIN: Education; CONCEPT: Parabola; TECH: Gradio, SQLite, Plotly]

$START_DOCUMENT_PLAN
### План Документа
**SECTION_GOALS:**
- GOAL Реализовать генератор точек параболы y = ax^2 + c => [GOAL_GENERATION]
- GOAL Обеспечить сохранение параметров в config.json => [GOAL_CONFIG]
- GOAL Реализовать хранение точек в SQLite => [GOAL_STORAGE]
- GOAL Создать интерактивный UI на Gradio => [GOAL_UI]

**SECTION_USE_CASES:**
- USE_CASE Пользователь -> Изменяет параметры и нажимает 'Generate Data' -> Данные сохранены в БД и отображены в таблице => [UC_GENERATE]
- USE_CASE Пользователь -> Нажимает 'Draw Graph' -> График параболы отображен в UI => [UC_DRAW]
$END_DOCUMENT_PLAN

$START_SECTION_FUNCTIONAL_REQUIREMENTS
### Функциональные требования

$START_ARTIFACT_CONFIG_MANAGER
#### Config Manager
**TYPE:** GOAL
**KEYWORDS:** [TECH: JSON; PATTERN: Singleton-like]
$START_CONTRACT
**PURPOSE:** Управление файлом config.json.
**DESCRIPTION:** Чтение и запись параметров a, c, x_min, x_max.
**RATIONALE:** Изоляция логики управления состоянием от UI и расчетов.
**ACCEPTANCE_CRITERIA:**
- Файл config.json создается автоматически, если его нет.
- Параметры корректно сохраняются и считываются.
$END_CONTRACT
$END_ARTIFACT_CONFIG_MANAGER

$START_ARTIFACT_DATA_PROCESSOR
#### Data Processor
**TYPE:** GOAL
**KEYWORDS:** [TECH: SQLite, Pandas; CONCEPT: Math]
$START_CONTRACT
**PURPOSE:** Расчет точек параболы и работа с БД.
**DESCRIPTION:** Вычисление y = ax^2 + c для заданного диапазона и сохранение в SQLite.
**RATIONALE:** Отделение математической логики и работы с данными от интерфейса.
**ACCEPTANCE_CRITERIA:**
- Точки рассчитываются верно.
- Данные сохраняются в таблицу 'points' в SQLite.
- Старые данные очищаются перед новой генерацией.
$END_CONTRACT
$END_ARTIFACT_DATA_PROCESSOR

$START_ARTIFACT_UI_GRADIO
#### Gradio UI
**TYPE:** GOAL
**KEYWORDS:** [TECH: Gradio, Plotly]
$START_CONTRACT
**PURPOSE:** Визуализация и управление.
**DESCRIPTION:** Двухколоночный интерфейс с ползунками, таблицей и графиком.
**RATIONALE:** Обеспечение Agentic UX и наглядности.
**ACCEPTANCE_CRITERIA:**
- Левая колонка: Слайдеры (a, c, x_min, x_max), кнопки, таблица.
- Правая колонка: Интерактивный график Plotly.
- Кнопка 'Generate Data' обновляет таблицу.
- Кнопка 'Draw Graph' обновляет график.
$END_CONTRACT
$END_ARTIFACT_UI_GRADIO

$END_SECTION_FUNCTIONAL_REQUIREMENTS

$END_DOC_NAME
