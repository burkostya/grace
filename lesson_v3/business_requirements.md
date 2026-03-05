$START_DOC_NAME

**PURPOSE:** Создание учебного приложения Lesson_v3 для генерации точек параболы с соблюдением архитектурных стандартов.
**SCOPE:** Генерация данных, хранение в SQLite, управление конфигурацией через JSON, CLI и Gradio интерфейсы.
**KEYWORDS:** Parabola, SQLite, Gradio, CLI, LDD, Agentic UX.

$START_DOCUMENT_PLAN
### План Документа
**SECTION_GOALS:**
- GOAL Реализовать расчет параболы y = ax^2 + c => [G_CALC]
- GOAL Обеспечить хранение параметров в config.json => [G_CONFIG]
- GOAL Реализовать хранение точек в SQLite => [G_DB]
- GOAL Создать CLI для автономной работы => [G_CLI]
- GOAL Создать UI на Gradio => [G_UI]

**SECTION_USE_CASES:**
- USE_CASE Пользователь генерирует данные через UI => [UC_UI_GEN]
- USE_CASE Агент генерирует данные через CLI => [UC_CLI_GEN]
- USE_CASE Экспорт данных в CSV через CLI => [UC_CLI_EXPORT]
$END_DOCUMENT_PLAN

$START_SECTION_REQUIREMENTS
### Требования

$START_ARTIFACT_FUNCTIONAL
#### Функциональные требования

**TYPE:** GOAL
**KEYWORDS:** Logic, Data

$START_CONTRACT
**PURPOSE:** Описание математической и логической составляющей.
**DESCRIPTION:** 
1. Расчет точек параболы y = a*x^2 + c.
2. Параметры: a, c, x_min, x_max.
3. Сохранение параметров в config.json.
4. Сохранение результатов в таблицу `points` (x, y) базы данных `parabola.db`.
**RATIONALE:** Обеспечение воспроизводимости и разделения ответственности.
**ACCEPTANCE_CRITERIA:** 
- Данные в БД соответствуют формуле.
- Параметры в config.json обновляются при генерации.
$END_CONTRACT
$END_ARTIFACT_FUNCTIONAL

$START_ARTIFACT_INTERFACE
#### Интерфейсные требования

**TYPE:** USE_CASE
**KEYWORDS:** UI, CLI

$START_CONTRACT
**PURPOSE:** Описание способов взаимодействия.
**DESCRIPTION:** 
- **UI:** Две колонки. Слева ввод и кнопки "Generate Data", "Draw Graph". Справа таблица и график Plotly.
- **CLI:** Команды `generate` (берет параметры из конфига) и `export-csv --out <file>`.
**RATIONALE:** Поддержка как человеческого, так и агентского взаимодействия (Agentic UX).
**ACCEPTANCE_CRITERIA:** 
- CLI возвращает exit code 0.
- UI корректно отображает график после нажатия кнопки.
$END_CONTRACT
$END_ARTIFACT_INTERFACE

$END_SECTION_REQUIREMENTS

$END_DOC_NAME
