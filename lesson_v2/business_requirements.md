$START_DOC_NAME

**PURPOSE:** Описание бизнес-требований к учебному приложению "Parabola Pro" (v2) для демонстрации полного цикла разработки.
**SCOPE:** Бэкенд (SQLite), Контроллер, Фронтенд (Gradio), Автотесты (Pytest).
**KEYWORDS:** [DOMAIN(9): Education; TECH(8): SQLite, Gradio, Plotly; CONCEPT(7): FullCycle]

$START_DOCUMENT_PLAN
### План Документа

**SECTION_GOALS:**
- GOAL Демонстрация полного цикла разработки с нуля в изолированной папке => [GOAL_FULL_CYCLE]
- GOAL Расширение функционала: добавление настройки диапазона X => [GOAL_RANGE_FEATURE]
- GOAL 100% покрытие автотестами логики UI и Backend => [GOAL_TEST_COVERAGE]

**SECTION_USE_CASES:**
- USE_CASE Пользователь -> Установка коэффициентов и диапазона -> Генерация данных в БД => [UC_GENERATE_PRO]
- USE_CASE Пользователь -> Просмотр таблицы и графика -> Визуализация результата => [UC_VISUALIZE_PRO]
- USE_CASE Разработчик -> Запуск pytest -> Автоматическая проверка всех слоев => [UC_AUTO_TEST]

$END_DOCUMENT_PLAN

$START_SECTION_REQUIREMENTS
### Требования к функциональности

$START_ARTIFACT_BACKEND
#### Бэкенд (Data Generator Pro)

**TYPE:** NFR
**KEYWORDS:** [TECH(9): SQLite; CONCEPT(8): MathLogic]

$START_CONTRACT
**PURPOSE:** Расчет точек параболы y = ax^2 + c в заданном диапазоне [x_min, x_max].
**DESCRIPTION:** 
1. Принимает параметры: a, c, x_min, x_max, step.
2. Очищает таблицу `points` перед новой генерацией.
3. Сохраняет результат в `lesson_v2/parabola_pro.db`.
**RATIONALE:** Демонстрация работы с параметризованными расчетами и БД.
**ACCEPTANCE_CRITERIA:**
- Корректный расчет y для каждого x в диапазоне.
- Данные успешно сохраняются и читаются из SQLite.
$END_CONTRACT
$END_ARTIFACT_BACKEND

$START_ARTIFACT_FRONTEND
#### Фронтенд и Контроллер (Gradio UI Pro)

**TYPE:** USE_CASE
**KEYWORDS:** [TECH(9): Gradio; TECH(8): Plotly]

$START_CONTRACT
**PURPOSE:** Интерфейс управления и визуализации.
**DESCRIPTION:** 
1. Поля ввода для a, c, x_min, x_max.
2. Кнопка "Generate" (вызывает расчет).
3. Кнопка "Draw" (строит график Plotly).
4. Таблица для отображения данных.
**RATIONALE:** Показ разделения логики интерфейса и бизнес-логики через контроллер.
**ACCEPTANCE_CRITERIA:**
- UI-тесты (через вызовы функций контроллера) проходят успешно.
- График Plotly отображает данные из БД.
$END_CONTRACT
$END_ARTIFACT_FRONTEND

$END_SECTION_REQUIREMENTS

$END_DOC_NAME
