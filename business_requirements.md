$START_DOC_NAME

**PURPOSE:** Описание бизнес-требований к учебному приложению "Генератор Параболы" для демонстрации студентам принципов разработки по фреймворку KiloCode.
**SCOPE:** Бэкенд (SQLite), Фронтенд (Gradio), Тестирование (Pytest).
**KEYWORDS:** [DOMAIN(9): Education; TECH(8): SQLite, Gradio, Pytest; CONCEPT(7): Parabola]

$START_DOCUMENT_PLAN
### План Документа

**SECTION_GOALS:**
- GOAL Демонстрация разделения ответственности между бэкендом и фронтендом => [GOAL_DECOUPLING]
- GOAL Обучение студентов написанию тестов для разных слоев приложения => [GOAL_TESTING]
- GOAL Использование семантической разметки KiloCode для прозрачности кода => [GOAL_SEMANTIC_MARKUP]

**SECTION_USE_CASES:**
- USE_CASE Студент (Backend) -> Запуск тестов бэкенда -> Подтверждение корректности БД => [UC_BACKEND_TEST]
- USE_CASE Пользователь (UI) -> Настройка параметров и нажатие Generate -> Данные в БД => [UC_GENERATE_DATA]
- USE_CASE Пользователь (UI) -> Нажатие Draw -> Визуализация графика => [UC_DRAW_GRAPH]

$END_DOCUMENT_PLAN

$START_SECTION_REQUIREMENTS
### Требования к функциональности

$START_ARTIFACT_BACKEND
#### Бэкенд (Data Generator)

**TYPE:** NFR
**KEYWORDS:** [TECH(9): SQLite; CONCEPT(8): Parabola]

$START_CONTRACT
**PURPOSE:** Генерация точек параболы y = ax^2 + c и сохранение в SQLite.
**DESCRIPTION:** Модуль должен принимать коэффициент 'a' и смещение 'c', генерировать набор точек и сохранять их в таблицу `points` (x, y).
**RATIONALE:** Показывает работу с персистентным хранилищем и математической логикой.
**ACCEPTANCE_CRITERIA:**
- Создается файл базы данных `parabola.db`.
- Таблица содержит корректные расчеты.
- Наличие pytest-тестов, проверяющих запись и чтение.
$END_CONTRACT
$END_ARTIFACT_BACKEND

$START_ARTIFACT_FRONTEND
#### Фронтенд (Gradio UI)

**TYPE:** USE_CASE
**KEYWORDS:** [TECH(9): Gradio; TECH(7): Plotly/Matplotlib]

$START_CONTRACT
**PURPOSE:** Интерфейс для управления генерацией и отображения данных.
**DESCRIPTION:** 
1. Слайдеры/поля для ввода 'a' и 'c'.
2. Кнопка "Generate" для вызова бэкенда.
3. Таблица (Dataframe) для просмотра сырых данных.
4. Кнопка "Draw" для отрисовки графика.
**RATIONALE:** Демонстрация современного UI-фреймворка для Python.
**ACCEPTANCE_CRITERIA:**
- Интерфейс запускается локально.
- Данные в таблице обновляются после генерации.
- График соответствует данным в БД.
$END_CONTRACT
$END_ARTIFACT_FRONTEND

$END_SECTION_REQUIREMENTS

$END_DOC_NAME
