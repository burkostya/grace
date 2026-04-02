$START_DEV_PLAN

**PURPOSE:** Создание прототипа ERP-интерфейса на Dash (Lesson_19) с Master-Detail архитектурой и AG Grid.

---

### 1. Draft Code Graph (Черновой Граф Кода)

```xml
<DraftCodeGraph>
  <lesson_19_app_py FILE="lesson_19/app.py" TYPE="UI_LAYER">
    <annotation>Dash приложение: layout и callbacks.</annotation>
    <app_layout_FUNC NAME="layout" TYPE="UI_COMPONENT">
      <annotation>Определение структуры интерфейса (3 колонки).</annotation>
    </app_layout_FUNC>
    <app_callbacks_FUNC NAME="register_callbacks" TYPE="UI_LOGIC">
      <annotation>Регистрация всех Dash callbacks.</annotation>
      <CrossLinks>
        <Link TARGET="lesson_19_handlers_py_get_invoice_lines_FUNC" TYPE="CALLS_FUNCTION" />
        <Link TARGET="lesson_19_handlers_py_generate_mock_data_FUNC" TYPE="CALLS_FUNCTION" />
      </CrossLinks>
    </app_callbacks_FUNC>
  </lesson_19_app_py>

  <lesson_19_handlers_py FILE="lesson_19/handlers.py" TYPE="BUSINESS_LOGIC_LAYER">
    <annotation>Чистая бизнес-логика без зависимостей от Dash.</annotation>
    <lesson_19_handlers_py_generate_mock_data_FUNC NAME="generate_mock_data" TYPE="LOGIC_FUNC">
      <annotation>Генерация 5 накладных и строк к ним.</annotation>
    </lesson_19_handlers_py_generate_mock_data_FUNC>
    <lesson_19_handlers_py_get_invoice_lines_FUNC NAME="get_invoice_lines" TYPE="LOGIC_FUNC">
      <annotation>Получение строк накладной по ID.</annotation>
    </lesson_19_handlers_py_get_invoice_lines_FUNC>
  </lesson_19_handlers_py>

  <lesson_19_db_manager_py FILE="lesson_19/db_manager.py" TYPE="DATA_ACCESS_LAYER">
    <annotation>Работа с SQLite базой erp_base.db.</annotation>
    <db_init_FUNC NAME="init_db" TYPE="DB_OP">
      <annotation>Создание таблиц invoices и invoice_lines.</annotation>
    </db_init_FUNC>
  </lesson_19_db_manager_py>
</DraftCodeGraph>
```

---

### 2. Step-by-step Data Flow (Пошаговый Поток Данных)

1.  **Инициализация:** При запуске `app.py` вызывается `db_manager.init_db()`, создающая таблицы, если их нет.
2.  **Генерация:** Пользователь жмет "Сгенерировать" -> Callback вызывает `handlers.generate_mock_data()` -> Данные пишутся в SQLite -> Обновляется Master-Grid.
3.  **Выбор:** Пользователь кликает на строку в Master-Grid -> Callback берет `invoice_id` -> Вызывает `handlers.get_invoice_lines(id)` -> Данные отображаются в Detail-Grid.
4.  **Редактирование:** Пользователь меняет "Количество" в Detail-Grid -> Нажимает "Сохранить" -> Callback отправляет данные в `handlers.update_invoice_lines()` -> БД обновляется -> Пересчитываются итоги -> Обновляются оба грида и график.

---

### 3. Acceptance Criteria (Критерии Приемки)

- [ ] **Критерий 1:** Приложение запускается в `lesson_19/app.py` без ошибок импорта.
- [ ] **Критерий 2:** Кнопка генерации создает ровно 5 накладных с корректными суммами.
- [ ] **Критерий 3:** Выбор накладной в левом гриде мгновенно обновляет центральный грид.
- [ ] **Критерий 4:** Редактирование количества товара и сохранение корректно обновляет общую сумму накладной в БД и на графике.
- [ ] **Критерий 5:** Все тесты в `lesson_19/tests/` проходят (100% PASS).
- [ ] **Критерий 6:** Код содержит семантическую разметку и LDD логирование.

$END_DEV_PLAN
