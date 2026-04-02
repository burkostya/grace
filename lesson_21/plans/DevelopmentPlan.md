$START_DEV_PLAN

**PURPOSE:** План разработки ERP-прототипа на Dash (Урок 21).

---

### 1. Draft Code Graph (Черновой Граф Кода)

```xml
<DraftCodeGraph>
  <db_manager_py FILE="lesson_21/db_manager.py" TYPE="MODULE">
    <annotation>Управление SQLite БД: создание таблиц, инициализация демо-данных.</annotation>
    <db_manager_init_db_FUNC NAME="init_db" TYPE="FUNCTION">
      <annotation>Создает таблицы и заполняет справочник товаров.</annotation>
    </db_manager_init_db_FUNC>
    <db_manager_get_connection_FUNC NAME="get_connection" TYPE="FUNCTION">
      <annotation>Возвращает соединение с БД.</annotation>
    </db_manager_get_connection_FUNC>
  </db_manager_py>

  <handlers_py FILE="lesson_21/handlers.py" TYPE="MODULE">
    <annotation>Чистая бизнес-логика (БЕЗ Dash). Работает с базовыми типами Python.</annotation>
    <handlers_search_items_FUNC NAME="search_items" TYPE="FUNCTION">
      <annotation>Поиск товаров по LIKE %keyword%.</annotation>
    </handlers_search_items_FUNC>
    <handlers_add_line_to_invoice_FUNC NAME="add_line_to_invoice" TYPE="FUNCTION">
      <annotation>Добавляет строку в накладную и пересчитывает общую сумму.</annotation>
    </handlers_add_line_to_invoice_FUNC>
    <handlers_update_line_qty_FUNC NAME="update_line_qty" TYPE="FUNCTION">
      <annotation>Обновляет количество в строке и пересчитывает суммы.</annotation>
    </handlers_update_line_qty_FUNC>
    <handlers_get_invoices_FUNC NAME="get_invoices" TYPE="FUNCTION">
      <annotation>Возвращает список всех накладных.</annotation>
    </handlers_get_invoices_FUNC>
    <handlers_get_invoice_lines_FUNC NAME="get_invoice_lines" TYPE="FUNCTION">
      <annotation>Возвращает строки конкретной накладной.</annotation>
    </handlers_get_invoice_lines_FUNC>
  </handlers_py>

  <app_py FILE="lesson_21/app.py" TYPE="MODULE">
    <annotation>UI и Callbacks. Маршрутизация данных между UI и handlers.</annotation>
    <app_layout_VAR NAME="layout" TYPE="VARIABLE">
      <annotation>Dash layout с 3 колонками.</annotation>
    </app_layout_VAR>
    <app_callbacks_BLOCK NAME="callbacks" TYPE="BLOCK">
      <annotation>Обработка событий: выбор накладной, поиск, добавление, редактирование.</annotation>
    </app_callbacks_BLOCK>
  </app_py>

  <test_handlers_py FILE="lesson_21/tests/test_handlers.py" TYPE="TEST_MODULE">
    <annotation>Тесты бизнес-логики (pytest).</annotation>
  </test_handlers_py>

  <test_callbacks_py FILE="lesson_21/tests/test_callbacks.py" TYPE="TEST_MODULE">
    <annotation>Тесты коллбеков (mock-данные).</annotation>
  </test_callbacks_py>
</DraftCodeGraph>
```

---

### 2. Step-by-step Data Flow (Пошаговый Поток Данных)

1.  **Инициализация:** `db_manager.init_db()` создает `erp_base.db` и наполняет `items`.
2.  **Загрузка Master:** `app.py` вызывает `handlers.get_invoices()`, данные отображаются в левом гриде.
3.  **Выбор накладной:** Пользователь выбирает строку -> `inv_id` сохраняется в `dcc.Store` -> разблокируется Блок А.
4.  **Поиск товара:** Ввод текста -> `handlers.search_items(keyword)` -> обновление мини-грида.
5.  **Добавление товара:** Выбор товара + кол-во -> `handlers.add_line_to_invoice(inv_id, item_id, qty)` -> обновление БД -> обновление всех гридов и графика.
6.  **Редактирование:** Изменение `qty` в Блоке Б -> `handlers.update_line_qty()` -> обновление БД -> обновление всех гридов и графика.

---

### 3. Acceptance Criteria (Критерии Приемки)

- [ ] **Критерий 1:** База данных `erp_base.db` создается корректно с 3 таблицами и демо-данными.
- [ ] **Критерий 2:** Интерфейс разделен на 3 колонки (Master, Search/Detail, Analytics).
- [ ] **Критерий 3:** Поиск товаров работает через SQL `LIKE`.
- [ ] **Критерий 4:** Добавление и редактирование строк накладной корректно пересчитывает `total_sum` в `invoices`.
- [ ] **Критерий 5:** График аналитики обновляется автоматически.
- [ ] **Критерий 6:** Тесты `test_handlers.py` и `test_callbacks.py` проходят успешно (100% покрытие логики).
- [ ] **Критерий 7:** Логирование LDD 2.0 ведется в `lesson_21/app.log` с использованием `IMP:1-10`.

$END_DEV_PLAN
