

# Инструкция для AI-агента: Создание учебного приложения на Dash (Lesson_X)

## Общая задача
Спроектируйте и реализуйте новое учебное приложение в директории `lesson_X` (где `X` — следующий доступный порядковый номер урока). Приложение должно генерировать точки параболы $y = ax^2 + c$, отображать их в **редактируемой таблице** и демонстрировать архитектурные стандарты фреймворка промтов что тебе загружены (изоляция слоев, Agentic UX, Headless-тестирование, LDD). Для получения очередного номера урока считай список текущих папок и увеличь номер урока на один. Для чистоты эксперимента, не читай файлы из lesson-папок для генерации нового урока, чтобы не подглядывать в уже ранее сделанный код.

**UI-ФРЕЙМВОРК:** Dash + dash-bootstrap-components + dash DataTable (вместо Gradio).

**КРИТИЧЕСКОЕ ПРАВИЛО ОКРУЖЕНИЯ:** Приложение создается в рамках непрерывного учебного процесса. **ЗАПРЕЩАЕТСЯ** создавать новые виртуальные окружения (VENV) или переустанавливать библиотеки, если они уже есть в системе (pandas, dash, dash-bootstrap-components, plotly, pytest). Если какой-то пакет отсутствует, установить его через `pip install` без создания VENV. Вся изоляция достигается исключительно инкапсуляцией файлов внутри папки `lesson_X/`.

## Бизнес-требования и Функциональность

### 1. Единый файл конфигурации (State Management)
*   Приложение должно использовать единый файл `config.json` (внутри папки урока) для хранения текущих параметров генерации: коэффициентов `a` и `c`, а также диапазона `x_min`, `x_max`.
*   Работу с файлом конфигурации (чтение/запись) необходимо вынести в строго отдельный модуль (например, `config_manager.py`).

### 2. Графический интерфейс (Dash)

**Архитектура UI — строгое разделение слоёв:**

```
lesson_X/
├── app.py              # Dash app: layout + callbacks (тонкий glue-слой)
├── handlers.py         # Чистые Python-функции бизнес-логики (БЕЗ импорта dash)
├── config_manager.py   # Работа с config.json
├── db_manager.py       # Работа с SQLite
├── config.json         # Параметры
├── parabola.db         # SQLite база
└── tests/
    ├── test_handlers.py    # Headless-тесты чистой логики
    └── test_callbacks.py   # Тесты callback-функций (без сервера)
```

**Критическое правило:** Файл `handlers.py` **НЕ ДОЛЖЕН** импортировать ничего из `dash`. Он содержит только чистые функции вида `f(inputs) → outputs`. Файл `app.py` содержит только layout и callback-обёртки, которые вызывают функции из `handlers.py`.

Интерфейс должен использовать `dash-bootstrap-components` для компоновки и быть разделён на две колонки:

*   **Левая колонка (Управление и таблица данных):**
    *   Поля ввода `dbc.Input` для `a`, `c`, `x_min`, `x_max` с подписями `dbc.Label`.
    *   **Кнопка 1 ("Generate Data"):** Сохраняет введенные параметры в `config.json`, выполняет расчет точек параболы и сохраняет их в базу данных SQLite. После нажатия таблица обновляется данными из БД.
    *   **Кнопка 2 ("Draw Graph"):** Считывает данные **из таблицы** (а не из БД!) и строит график. Это позволяет увидеть эффект ручного редактирования.
    *   **Кнопка 3 ("Save Edits"):** Записывает текущее состояние таблицы (с учётом ручных правок) обратно в БД SQLite.
    *   Компонент `dash_table.DataTable` с **редактируемыми ячейками**:
        *   Колонки: `x`, `y`, `y_edited` (пользователь может вручную менять `y_edited`)
        *   Колонка `x` — только чтение
        *   Колонка `y` — исходное значение, только чтение
        *   Колонка `y_edited` — **редактируемая**, инициализируется копией `y`
        *   Строки можно удалять (`row_deletable=True`)
    
*   **Правая колонка (График):**
    *   Компонент `dcc.Graph` для интерактивного графика Plotly.
    *   График должен отображать **две кривые**: исходную параболу (`y`) и отредактированную (`y_edited`), чтобы было видно разницу.

**Пример структуры layout (ориентир для агента):**

ВНИМАНИЕ! Примеры кода идут без семантической разметки, код готового приложения должен иметь встроенную документацию на контрактах и сегментирован START-END тегами.

```python
import dash
from dash import html, dcc, dash_table, Input, Output, State
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            # Поля ввода параметров
            dbc.Card([
                dbc.CardBody([
                    dbc.Label("a"), dbc.Input(id="input-a", type="number", value=1),
                    dbc.Label("c"), dbc.Input(id="input-c", type="number", value=0),
                    dbc.Label("x_min"), dbc.Input(id="input-xmin", type="number", value=-10),
                    dbc.Label("x_max"), dbc.Input(id="input-xmax", type="number", value=10),
                ])
            ], className="mb-3"),
            # Кнопки
            dbc.ButtonGroup([
                dbc.Button("Generate Data", id="btn-generate", color="primary"),
                dbc.Button("Draw Graph", id="btn-draw", color="success"),
                dbc.Button("Save Edits", id="btn-save", color="warning"),
            ], className="mb-3"),
            # Редактируемая таблица
            dash_table.DataTable(
                id="data-table",
                columns=[
                    {"name": "x", "id": "x", "editable": False},
                    {"name": "y (original)", "id": "y", "editable": False},
                    {"name": "y (edited)", "id": "y_edited", "editable": True,
                     "type": "numeric"},
                ],
                data=[],
                row_deletable=True,
                style_table={"overflowY": "auto", "maxHeight": "500px"},
                style_cell={"textAlign": "center"},
                style_header={"fontWeight": "bold"},
            ),
        ], width=5),
        dbc.Col([
            dcc.Graph(id="graph-parabola", style={"height": "600px"})
        ], width=7),
    ])
], fluid=True)
```

*   *Точка запуска UI:* В корне проекта создать скрипт `run_lesson_X.py`, который импортирует `app` и запускает `app.run(debug=True, port=8050)`.

### 3. Паттерн Callbacks → Handlers (Headless-тестируемость)

**Каждый callback в `app.py` должен быть тонкой обёрткой над чистой функцией из `handlers.py`:**

```python
# ===== handlers.py (ЧИСТАЯ ЛОГИКА, без dash) =====
import pandas as pd

def generate_parabola_points(a: float, c: float, 
                              x_min: float, x_max: float,
                              step: float = 1.0) -> pd.DataFrame:
    """Генерирует точки параболы y = ax^2 + c."""
    import numpy as np
    x_values = np.arange(x_min, x_max + step, step)
    y_values = a * x_values**2 + c
    df = pd.DataFrame({"x": x_values, "y": y_values, "y_edited": y_values})
    return df

def build_comparison_figure(table_data: list[dict]) -> "plotly.graph_objects.Figure":
    """Строит график с двумя кривыми из данных таблицы."""
    import plotly.graph_objects as go
    df = pd.DataFrame(table_data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["x"], y=df["y"], 
                              mode="lines+markers", name="Original"))
    fig.add_trace(go.Scatter(x=df["x"], y=df["y_edited"], 
                              mode="lines+markers", name="Edited"))
    fig.update_layout(template="plotly_white", 
                       title="Parabola: Original vs Edited")
    return fig

def prepare_table_records(df: pd.DataFrame) -> list[dict]:
    """Конвертирует DataFrame в формат для DataTable."""
    return df.to_dict("records")


# ===== app.py (ТОНКИЙ GLUE) =====
from dash import Input, Output, State, callback, no_update
from handlers import generate_parabola_points, build_comparison_figure

@callback(
    Output("data-table", "data"),
    Input("btn-generate", "n_clicks"),
    State("input-a", "value"),
    State("input-c", "value"),
    State("input-xmin", "value"),
    State("input-xmax", "value"),
    prevent_initial_call=True
)
def on_generate(n_clicks, a, c, x_min, x_max):
    df = generate_parabola_points(a, c, x_min, x_max)
    # Здесь же сохраняем в БД и конфиг
    save_config(a, c, x_min, x_max)   # из config_manager
    save_to_db(df)                      # из db_manager
    return df.to_dict("records")

@callback(
    Output("graph-parabola", "figure"),
    Input("btn-draw", "n_clicks"),
    State("data-table", "data"),
    prevent_initial_call=True
)
def on_draw(n_clicks, table_data):
    if not table_data:
        return no_update
    return build_comparison_figure(table_data)
```

## Требования к разработке и архитектуре
1.  **Соблюдение фреймворка промптов:** Весь код должен быть обернут в "Семантический Экзоскелет" (теги `START_BLOCK`, `MODULE_CONTRACT` и т.д.). Контракты должны быть написаны в парадигме "Zero-Context Survival" для будущих агентов. Если фреймворк тебе с этими понятиями не доступен, то останови работу и сообщи пользователю об ошибке настройки агентской среды.
2.  **Логирование (LDD 2.0):** Логи пишутся в изолированный файл `lesson_X/app_X.log`. Строго использовать шкалу `[IMP:1-10]` и фиксировать "AI Belief State" в критических точках алгоритма.
3.  **AppGraph:** Только после успешного завершения кодирования и прохождения всех тестов, создайте ЛОКАЛЬНЫЙ `AppGraph.xml` в папке уроке, корневой граф не обновляйте.

## Стратегия Тестирования (100% покрытие бизнес-логики в `lesson_X/tests/`)

Реализуйте тесты на `pytest`, генерирующие семантический контекст:

### 1. Headless-тест чистой логики (`test_handlers.py`)
**Без запуска Dash-сервера. Без браузера. Просто pytest.**

```python
# test_handlers.py
import pytest
import pandas as pd
from handlers import generate_parabola_points, build_comparison_figure

class TestParabolaGeneration:
    def test_basic_parabola(self):
        """y = 1*x^2 + 0 при x=[-2,2] -> y=[4,1,0,1,4]"""
        df = generate_parabola_points(a=1, c=0, x_min=-2, x_max=2, step=1)
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["x", "y", "y_edited"]
        assert df.loc[df["x"] == 0, "y"].values[0] == 0
        assert df.loc[df["x"] == 2, "y"].values[0] == 4

    def test_with_offset(self):
        """y = 2*x^2 + 5 при x=0 -> y=5"""
        df = generate_parabola_points(a=2, c=5, x_min=0, x_max=0, step=1)
        assert df["y"].values[0] == 5

    def test_edited_column_initialized(self):
        """y_edited должна быть копией y при генерации"""
        df = generate_parabola_points(a=1, c=0, x_min=-1, x_max=1)
        assert (df["y"] == df["y_edited"]).all()

class TestGraphBuilding:
    def test_returns_figure(self):
        data = [{"x": 0, "y": 0, "y_edited": 5},
                {"x": 1, "y": 1, "y_edited": 3}]
        fig = build_comparison_figure(data)
        assert fig is not None
        assert len(fig.data) == 2  # две кривые
        assert fig.data[0].name == "Original"
        assert fig.data[1].name == "Edited"

    def test_edited_values_reflected(self):
        """График должен показывать изменённые значения"""
        data = [{"x": 0, "y": 0, "y_edited": 99}]
        fig = build_comparison_figure(data)
        assert fig.data[1].y[0] == 99  # Edited кривая
```

### 2. Callback Integration Test (`test_callbacks.py`)
Тест callback-функций **вызывая их как обычные Python-функции** (без сервера):

```python
# test_callbacks.py
"""
Тестируем callback-обёртки из app.py напрямую.
Dash callback — это обычная Python-функция, которую можно вызвать.
"""
import pytest

def test_on_generate_returns_records():
    """Callback генерации должен вернуть list[dict] для DataTable"""
    from app import on_generate
    result = on_generate(n_clicks=1, a=1, c=0, x_min=-2, x_max=2)
    assert isinstance(result, list)
    assert len(result) > 0
    assert "x" in result[0]
    assert "y" in result[0]
    assert "y_edited" in result[0]

def test_on_draw_returns_figure():
    """Callback отрисовки должен вернуть Plotly Figure"""
    from app import on_draw
    import plotly.graph_objects as go
    test_data = [{"x": 0, "y": 0, "y_edited": 0},
                 {"x": 1, "y": 1, "y_edited": 2}]
    fig = on_draw(n_clicks=1, table_data=test_data)
    assert isinstance(fig, go.Figure)
```

### Эквивалент Gradio headless-тестирования

| Gradio | Dash (наш подход) |
|---|---|
| Обработчик = обычная функция | Обработчик в `handlers.py` = обычная функция |
| `fn(input) → output` | `handler(inputs) → outputs` |
| `gr.Blocks()` не нужен для теста | `app.server` не нужен для теста |
| Тест: `assert fn(5) == 25` | Тест: `assert generate_parabola_points(1,0,-2,2)...` |

**Принцип один и тот же:** бизнес-логика живёт в чистых функциях, UI — тонкая обёртка.
