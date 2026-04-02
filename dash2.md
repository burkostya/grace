Чтобы гарантировать **абсолютную надежность, нулевой риск конфликта версий и полное отсутствие ошибок `Duplicate callback outputs`**, мы должны отказаться от попыток сделать интерфейс "модным" (SPA-подобным, с редактированием ячеек на лету и сложными роутерами событий). 

Мы применим железобетонный архитектурный паттерн из мира React, адаптированный для Dash — **Flux Pattern (Через глобальные сигналы `dcc.Store`)**. 

Суть в том, чтобы **полностью отвязать события записи от событий чтения**. Никаких сложных диспетчеров (`dash.ctx.triggered_id`), в которых путаются LLM. 
1. Любое действие пользователя (Добавить товар, Удалить товар, Сгенерировать) вызывает callback, который обновляет БД и меняет **один** невидимый счетчик `dcc.Store(id='db-trigger')`.
2. Каждая таблица и график имеют свой **собственный, изолированный callback**, который слушает только этот `db-trigger` (и читает актуальные данные из БД). 

Таким образом, Dash физически не сможет выдать ошибку `Duplicate Outputs`, так как у каждого элемента интерфейса будет строго один источник обновления. А отказ от редактирования внутри AG Grid (`editable: False`) исключит баги версионности JS-оберток.

---

### Готовое задание для AI-агента (Максимальная надежность)

Скопируйте и передайте этот текст агенту:

```markdown
# Инструкция для AI-агента: Создание сверхнадежного ERP-прототипа на Dash (Lesson_X)

## Общая задача
Спроектируйте прототип ERP-приложения в директории `lesson_X` (вычислите следующий номер урока). 
**ГЛАВНЫЙ КРИТЕРИЙ:** Абсолютная отказоустойчивость сервера и клиента. Юзабилити вторично. Полный отказ от зависимых от версии "фишек" (inline-редактирование ячеек, всплывающие окна, сложные cellEditors). 

**АРХИТЕКТУРНЫЙ ПАТТЕРН (ОБЯЗАТЕЛЬНО К ИСПОЛНЕНИЮ): Dash Flux / Event Sourcing.**
Для исключения ошибки `Duplicate callback outputs` запрещается обновлять таблицы напрямую из кнопок. Вы обязаны использовать механизм глобального сигнала через `dcc.Store`. 

## Структура файлов и Слои (Zero-Context Survival)
```
lesson_X/
├── app.py              # UI, Callbacks (Строго по паттерну Flux)
├── handlers.py         # Чистая логика Python, работа с DB (без импортов Dash)
├── db_manager.py       # SQLite CRUD (invoices, items, invoice_lines)
└── tests/
    └── test_handlers.py    # Pytest для логики
```

## Требования к UI (Строго статический Layout)
Используем `dbc.Container(fluid=True)`. Интерфейс делится на 3 колонки.

**Скрытые элементы (Global State):**
В layout добавить:
1. `dcc.Store(id='db-trigger', data=0)` — счетчик изменений БД.
2. `dcc.Store(id='selected-invoice-id', data=None)` — хранит ID выбранной накладной.
3. `dcc.Store(id='selected-search-item-id', data=None)` — хранит ID выбранного в поиске товара.

**Левая колонка (Мастер):**
* Кнопка `dbc.Button(id='btn-generate', "Сгенерировать данные")`
* `dag.AgGrid(id='grid-invoices')`. Колонки: ID, Дата, Клиент, Сумма. **Только чтение (`editable: False`).** Одиночное выделение строк.

**Центральная колонка (Детали и Формы):**
Разделена на два статичных блока `dbc.Card`:
* **Блок 1: Поиск и добавление.**
  * `dbc.Input(id='input-search')` + `dbc.Button(id='btn-search', "Найти товар")`
  * Мини `dag.AgGrid(id='grid-search-results')`. Только чтение. Одиночное выделение строк.
  * `dbc.Input(id='input-qty', type='number', value=1)` + `dbc.Button(id='btn-add-item', "Добавить выбранный товар")`.
* **Блок 2: Строки накладной.**
  * `dag.AgGrid(id='grid-lines')`. Колонки: Товар, Кол-во, Цена, Сумма. **Только чтение (`editable: False`)**. Никакого редактирования в ячейках!
  * Кнопка `dbc.Button(id='btn-delete-line', "Удалить выделенную строку", color="danger")` под гридом.

**Правая колонка (Аналитика):**
* `dcc.Graph(id='graph-analytics')` (Bar chart: Суммы накладных).

## Жесткие правила Callbacks (Flux Pattern)

Вы обязаны написать ровно следующий набор Callbacks. Отклонение приведет к сбою (Duplicate Outputs).

**ГРУППА 1: Управление Состоянием (State Setters)**
1. `@callback(Output('selected-invoice-id', 'data'), Input('grid-invoices', 'selectedRows'))` — извлекает ID из выделенной строки.
2. `@callback(Output('selected-search-item-id', 'data'), Input('grid-search-results', 'selectedRows'))` — извлекает ID товара.

**ГРУППА 2: Операции Записи (Write Actions -> DB Trigger)**
Все кнопки, меняющие данные, работают в одном callback, который возвращает +1 к счетчику `db-trigger`.
```python
@callback(
    Output('db-trigger', 'data'),
    Input('btn-generate', 'n_clicks'),
    Input('btn-add-item', 'n_clicks'),
    Input('btn-delete-line', 'n_clicks'),
    State('selected-invoice-id', 'data'),
    State('selected-search-item-id', 'data'),
    State('input-qty', 'value'),
    State('grid-lines', 'selectedRows'),
    State('db-trigger', 'data'),
    prevent_initial_call=True
)
def handle_db_writes(btn_gen, btn_add, btn_del, inv_id, item_id, qty, selected_lines, trigger_val):
    # Используй dash.ctx.triggered_id чтобы понять, какая кнопка нажата.
    # Вызови нужную функцию из handlers.py (создать БД, добавить строку, удалить строку).
    # Функция в handlers.py сама должна пересчитать сумму накладной.
    # Если операция успешна, вернуть trigger_val + 1. Иначе dash.no_update.
```

**ГРУППА 3: Операции Чтения (Read Actions / UI Updaters)**
Каждый компонент обновляется СТРОГО СВОИМ изолированным callback.
1. **Обновление Накладных:** `@callback(Output('grid-invoices', 'rowData'), Input('db-trigger', 'data'))` -> вызывает `handlers.get_all_invoices()`.
2. **Обновление Графика:** `@callback(Output('graph-analytics', 'figure'), Input('db-trigger', 'data'))` -> вызывает `handlers.get_analytics_fig_data()`.
3. **Обновление Строк:** `@callback(Output('grid-lines', 'rowData'), Input('selected-invoice-id', 'data'), Input('db-trigger', 'data'))` -> если `inv_id` есть, вызывает `handlers.get_lines(inv_id)`, иначе пустой список.
4. **Поиск Товара:** `@callback(Output('grid-search-results', 'rowData'), Input('btn-search', 'n_clicks'), State('input-search', 'value'))` -> изолированный вызов БД (чтение).

## Разработка Бизнес-Логики (`handlers.py`)
Функции записи должны быть идемпотентны и самостоятельно управлять пересчетом `total_sum` в таблице `invoices` через `db_manager.py`. `handlers.py` не должен ничего знать про `dcc.Store` или `dash.ctx`.

Внедрить LDD (Логирование в `app.log`) и написать тесты в `tests/test_handlers.py`.
```

### Почему эта инструкция сработает идеально?
1. **Устранение корня проблемы:** LLM не придется строить монструозные графы возврата данных. Группа 3 четко показывает: один Output = один Input (глобальный триггер).
2. **Устранение JS-рисков:** Мы убрали `editable: True` и `agSelectCellEditor`. AG Grid используется исключительно как рендерер статических JSON-данных (таблиц), что работает безупречно в любой версии Dash/Grid.
3. **Управление ошибками пользователя:** Если оператор ошибся в количестве товара, он просто нажимает выделяет строку в накладной, жмет "Удалить" и добавляет заново с правильным числом. Это не так "красиво", как двойной клик по ячейке, но это **никогда** не сломается в production-среде Dash.