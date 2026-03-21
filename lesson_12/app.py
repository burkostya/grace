# FILE:lesson_12/app.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Главный модуль UI на Dash.
# SCOPE: Layout, Callbacks, интеграция слоев.
# KEYWORDS:[DOMAIN(9): UI; TECH(8): Dash]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.1 - Исправление семантической разметки: добавлены MODULE_MAP, USE_CASES и контракты callback-функций.]
# PREV_CHANGE_SUMMARY: [v1.0.0 - Создание основного модуля UI.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 6[Callback генерации данных] => on_generate
# FUNC 6[Callback отрисовки графика] => on_draw
# FUNC 6[Callback сохранения правок] => on_save
# END_MODULE_MAP
#
# START_USE_CASES:
# - [on_generate]: User -> ClickGenerate -> TableUpdated
# - [on_draw]: User -> ClickDraw -> GraphUpdated
# - [on_save]: User -> ClickSave -> DBUpdated
# END_USE_CASES

import dash
from dash import html, dcc, dash_table, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
import logging
import os

# Импорты внутренних слоев
from .handlers import generate_parabola_points, build_comparison_figure
from .config_manager import save_config, load_config
from .db_manager import init_db, save_points, load_points, update_points_from_dict

# Настройка логирования
LOG_FILE = os.path.join(os.path.dirname(__file__), "app_12.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
logger = logging.getLogger("lesson_12.app")

# Инициализация БД
init_db()

# Инициализация приложения
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server # Для Waitress

# Загрузка начальных данных
initial_config = load_config()

# START_BLOCK_LAYOUT: [Определение структуры интерфейса]
app.layout = dbc.Container([
    dbc.Row([
        html.H2("Lesson 12: Dash Parabola Editor", className="text-center my-4")
    ]),
    dbc.Row([
        # Левая колонка: Управление и Таблица
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Parameters"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([dbc.Label("a"), dbc.Input(id="input-a", type="number", value=initial_config['a'])]),
                        dbc.Col([dbc.Label("c"), dbc.Input(id="input-c", type="number", value=initial_config['c'])]),
                    ], className="mb-2"),
                    dbc.Row([
                        dbc.Col([dbc.Label("x_min"), dbc.Input(id="input-xmin", type="number", value=initial_config['x_min'])]),
                        dbc.Col([dbc.Label("x_max"), dbc.Input(id="input-xmax", type="number", value=initial_config['x_max'])]),
                    ]),
                ])
            ], className="mb-3"),
            
            dbc.ButtonGroup([
                dbc.Button("Generate Data", id="btn-generate", color="primary"),
                dbc.Button("Draw Graph", id="btn-draw", color="success"),
                dbc.Button("Save Edits", id="btn-save", color="warning"),
            ], className="mb-3 w-100"),
            
            dash_table.DataTable(
                id="data-table",
                columns=[
                    {"name": "x", "id": "x", "editable": False},
                    {"name": "y (original)", "id": "y", "editable": False},
                    {"name": "y (edited)", "id": "y_edited", "editable": True, "type": "numeric"},
                ],
                data=load_points().to_dict("records"),
                row_deletable=True,
                style_table={"overflowY": "auto", "maxHeight": "400px"},
                style_cell={"textAlign": "center", "padding": "5px"},
                style_header={"backgroundColor": "#f8f9fa", "fontWeight": "bold"},
                page_size=15
            ),
            html.Div(id="status-msg", className="mt-2 text-muted small")
        ], width=5),
        
        # Правая колонка: График
        dbc.Col([
            dcc.Graph(id="graph-parabola", style={"height": "600px"})
        ], width=7),
    ])
], fluid=True)
# END_BLOCK_LAYOUT

# START_FUNCTION_on_generate
# START_CONTRACT:
# PURPOSE: Обработка нажатия кнопки генерации данных.
# INPUTS: 
# - n_clicks: int
# - a: float
# - c: float
# - x_min: float
# - x_max: float
# OUTPUTS: 
# - list[dict] - Данные для таблицы
# - str - Статусное сообщение
# COMPLEXITY_SCORE: 4
# END_CONTRACT
@callback(
    Output("data-table", "data"),
    Output("status-msg", "children", allow_duplicate=True),
    Input("btn-generate", "n_clicks"),
    State("input-a", "value"),
    State("input-c", "value"),
    State("input-xmin", "value"),
    State("input-xmax", "value"),
    prevent_initial_call=True
)
def on_generate(n_clicks, a, c, x_min, x_max):
    """
    Callback для генерации новых данных. 
    Вызывает чистую функцию из handlers, сохраняет в БД и конфиг.
    """
    # START_BLOCK_GENERATE: [Генерация и сохранение]
    logger.info(f"[UI][IMP:6][on_generate][Click] Нажата кнопка генерации. [EVENT]")
    
    df = generate_parabola_points(a, c, x_min, x_max)
    save_config(a, c, x_min, x_max)
    save_points(df)
    
    logger.info(f"[BeliefState][IMP:9][on_generate][Success] Данные обновлены. [VALUE]")
    return df.to_dict("records"), f"Generated {len(df)} points at {a}, {c}"
    # END_BLOCK_GENERATE

# START_FUNCTION_on_draw
# START_CONTRACT:
# PURPOSE: Обработка нажатия кнопки отрисовки графика.
# INPUTS: 
# - n_clicks: int
# - table_data: list[dict]
# OUTPUTS: 
# - go.Figure
# COMPLEXITY_SCORE: 3
# END_CONTRACT
@callback(
    Output("graph-parabola", "figure"),
    Input("btn-draw", "n_clicks"),
    State("data-table", "data"),
    prevent_initial_call=True
)
def on_draw(n_clicks, table_data):
    """
    Callback для отрисовки графика.
    Берет данные НАПРЯМУЮ из таблицы (включая ручные правки).
    """
    # START_BLOCK_DRAW: [Отрисовка]
    logger.info(f"[UI][IMP:6][on_draw][Click] Нажата кнопка отрисовки. [EVENT]")
    if not table_data:
        logger.debug("[UI][IMP:4][on_draw][Skip] Данные отсутствуют. [INFO]")
        return no_update
    
    fig = build_comparison_figure(table_data)
    logger.info(f"[BeliefState][IMP:9][on_draw][Success] График обновлен. [VALUE]")
    return fig
    # END_BLOCK_DRAW

# START_FUNCTION_on_save
# START_CONTRACT:
# PURPOSE: Обработка нажатия кнопки сохранения правок.
# INPUTS: 
# - n_clicks: int
# - table_data: list[dict]
# OUTPUTS: 
# - str - Статусное сообщение
# COMPLEXITY_SCORE: 3
# END_CONTRACT
@callback(
    Output("status-msg", "children", allow_duplicate=True),
    Input("btn-save", "n_clicks"),
    State("data-table", "data"),
    prevent_initial_call=True
)
def on_save(n_clicks, table_data):
    """
    Callback для сохранения правок из таблицы в БД.
    """
    # START_BLOCK_SAVE: [Сохранение]
    logger.info(f"[UI][IMP:6][on_save][Click] Нажата кнопка сохранения правок. [EVENT]")
    if not table_data:
        return "No data to save"
    
    update_points_from_dict(table_data)
    logger.info(f"[BeliefState][IMP:9][on_save][Success] Правки сохранены в БД. [VALUE]")
    return f"Saved {len(table_data)} records to database (including edits)."
    # END_BLOCK_SAVE
# END_FUNCTION_on_save
