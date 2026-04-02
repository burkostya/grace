$START_DOC_NAME

**PURPOSE:** Спецификация требований для прототипа ERP-интерфейса на Dash (Урок 21).
**SCOPE:** SQLite DB, Dash UI, Ag-Grid, LDD 2.0, Pytest.
**KEYWORDS:** ERP, Dash, Ag-Grid, SQLite, LDD, 100% Reliability Pattern.

$START_DOCUMENT_PLAN
### План Документа

**SECTION_GOALS:**
- GOAL Создать надежный интерфейс работы с накладными без выпадающих списков => [GOAL_RELIABLE_UI]
- GOAL Обеспечить 100% покрытие тестами бизнес-логики и коллбеков => [GOAL_TEST_COVERAGE]

**SECTION_USE_CASES:**
- USE_CASE Пользователь -> Поиск товара -> Список найденных товаров => [UC_SEARCH_ITEM]
- USE_CASE Пользователь -> Добавление товара в накладную -> Обновление сумм и графиков => [UC_ADD_ITEM]
- USE_CASE Пользователь -> Изменение количества -> Пересчет накладной => [UC_EDIT_QTY]

$END_DOCUMENT_PLAN

$START_SECTION_REQUIREMENTS
### Функциональные требования

$START_ARTIFACT_DB_SCHEMA
#### Схема БД

**TYPE:** DATA_FORMAT
**KEYWORDS:** SQLite, Schema

$START_CONTRACT
**PURPOSE:** Определение структуры таблиц для хранения данных ERP.
**DESCRIPTION:** 
1. `invoices`: id, date, client_name, total_sum
2. `items`: id, sku, name, price
3. `invoice_lines`: id, invoice_id, item_id, qty, price, line_sum
**RATIONALE:** Минимально необходимый набор таблиц для эмуляции работы с накладными.
**ACCEPTANCE_CRITERIA:** Таблицы созданы, заполнены демо-данными (~20 позиций items).
$END_CONTRACT
$END_ARTIFACT_DB_SCHEMA

$START_ARTIFACT_UI_LAYOUT
#### Структура UI

**TYPE:** NFR
**KEYWORDS:** Dash, Bootstrap, Ag-Grid

$START_CONTRACT
**PURPOSE:** Описание компоновки интерфейса.
**DESCRIPTION:** 
- Верхняя панель: Кнопки "Демо-данные", "Аналитика".
- Лево: Список накладных (Master).
- Центр: Блок А (Поиск + Мини-грид) и Блок Б (Строки накладной).
- Право: График (Аналитика).
**RATIONALE:** Разделение на 3 колонки обеспечивает удобство работы и наглядность.
**ACCEPTANCE_CRITERIA:** Интерфейс соответствует описанию в `dash_good.md`.
$END_CONTRACT
$END_ARTIFACT_UI_LAYOUT

$END_SECTION_REQUIREMENTS

$END_DOC_NAME
