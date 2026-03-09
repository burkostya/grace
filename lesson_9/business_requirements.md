$START_DOC_NAME

**PURPOSE:** Определение бизнес-требований для учебного приложения Lesson 9 (Парабола).
**SCOPE:** Генерация данных, хранение в БД, CLI и UI интерфейсы.
**KEYWORDS:** [DOMAIN: Education; CONCEPT: Parabola; TECH: Gradio, SQLite, Plotly]

$START_DOCUMENT_PLAN
### План Документа
**SECTION_GOALS:**
- GOAL Реализация расчета точек параболы y = ax^2 + c => [G_CALC]
- GOAL Обеспечение персистентности данных в SQLite => [G_DB]
- GOAL Предоставление CLI для автоматизации => [G_CLI]
- GOAL Создание интерактивного UI на Gradio => [G_UI]

**SECTION_USE_CASES:**
- USE_CASE Пользователь генерирует данные через UI => [UC_UI_GEN]
- USE_CASE Агент генерирует данные через CLI => [UC_CLI_GEN]
$END_DOCUMENT_PLAN

$START_SECTION_GOALS
### Цели проекта

$START_ARTIFACT_G_CALC
#### Расчет параболы
**TYPE:** GOAL
**KEYWORDS:** [Math, Parabola]
$START_CONTRACT
**PURPOSE:** Вычисление координат (x, y) для функции y = ax^2 + c в заданном диапазоне.
**DESCRIPTION:** Функция принимает a, c, x_min, x_max и шаг, возвращает набор точек.
**RATIONALE:** Базовая математическая логика приложения.
**ACCEPTANCE_CRITERIA:** Точность расчетов соответствует формуле.
$END_CONTRACT
$END_ARTIFACT_G_CALC

$END_SECTION_GOALS

$START_SECTION_USE_CASES
### Сценарии использования

$START_ARTIFACT_UC_UI_GEN
#### Генерация через UI
**TYPE:** USE_CASE
**KEYWORDS:** [UI, Gradio]
$START_CONTRACT
**PURPOSE:** Позволить пользователю визуально управлять параметрами.
**DESCRIPTION:** User -> Вводит a, c, x_min, x_max -> Нажимает 'Generate Data' -> Данные в БД и таблице.
**RATIONALE:** Удобство для человека.
**ACCEPTANCE_CRITERIA:** Данные отображаются в таблице сразу после нажатия.
$END_CONTRACT
$END_ARTIFACT_UC_UI_GEN

$END_SECTION_USE_CASES

$END_DOC_NAME
