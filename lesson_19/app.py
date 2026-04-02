# FILE: lesson_19/app.py
# VERSION: 1.0.1
# START_MODULE_CONTRACT:
# PURPOSE: Dash приложение для ERP-прототипа.
# SCOPE: Layout, Callbacks, UI-логика.
# INPUT: Пользовательские действия в браузере.
# OUTPUT: Интерактивный ERP-интерфейс.
# KEYWORDS: [DOMAIN(8): UI; CONCEPT(7): Dash; TECH(9): AGGrid]
# LINKS: [USES_API(8): dash, dash_ag_grid, handlers, db_manager, config_manager]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.1 - Вынос логики callbacks в отдельные функции для удобства тестирования.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Инициализация приложения и layout] => create_app
# FUNC 9[Регистрация callbacks] => register_callbacks
# FUNC 9[Логика обновления Master-Grid] => update_master_logic
# FUNC 9[Логика обновления Detail-Grid] => update_detail_logic
# FUNC 9[Логика переключения графика] => toggle_chart_logic
# END_MODULE_MAP

import dash
from dash import dcc, html, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import plotly.express as px
import pandas as pd
import logging
import os

from .db_manager import init_db
from .config_manager import load_config, get_products
from .handlers import generate_mock_data, get_invoices, get_invoice_lines, update_invoice_lines

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Загрузка конфига
CONFIG = load_config("lesson_19/config.json")
DB_PATH = CONFIG["db_path"]

# Инициализация БД
init_db(DB_PATH)

# START_FUNCTION_update_master_logic
def update_master_logic(trigger_id, db_path):
    if trigger_id == "btn-generate":
        generate_mock_data(db_path)
        logger.info(f"[BeliefState][IMP:9][update_master_logic][GENERATE] Данные перегенерированы [VALUE]")
    
    invoices = get_invoices(db_path)
    df = pd.DataFrame(invoices)
    
    if df.empty:
        fig = px.bar(title="Нет данных")
    else:
        fig = px.bar(df, x="id", y="total_amount", title="Суммы накладных", labels={"id": "ID Накладной", "total_amount": "Сумма"})
    
    return invoices, fig
# END_FUNCTION_update_master_logic

# START_FUNCTION_update_detail_logic
def update_detail_logic(selected_rows, db_path):
    if not selected_rows:
        logger.debug(f"[UI][IMP:4][update_detail_logic][EMPTY] Строка не выбрана [INFO]")
        return [], "Выберите накладную", True
    
    inv_id = selected_rows[0]["id"]
    lines = get_invoice_lines(db_path, inv_id)
    logger.info(f"[BeliefState][IMP:9][update_detail_logic][FETCH] Загружены строки для ID {inv_id} [VALUE]")
    return lines, f"Накладная №{inv_id}", False
# END_FUNCTION_update_detail_logic

# START_FUNCTION_toggle_chart_logic
def toggle_chart_logic(n_clicks, current_style):
    if n_clicks is None:
        return current_style
    
    if current_style and current_style.get("display") == "none":
        return {"display": "block"}
    else:
        return {"display": "none"}
# END_FUNCTION_toggle_chart_logic

# START_FUNCTION_create_app
def create_app():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    products_list = list(get_products().keys())

    app.layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("ERP Прототип: Накладные", className="text-primary"),
                dbc.Button("Сгенерировать демо-данные", id="btn-generate", color="success", className="me-2"),
                dbc.Button("Показать/Скрыть Аналитику", id="btn-toggle-chart", color="info"),
            ], width=12, className="mb-4 mt-4")
        ]),
        dbc.Row([
            dbc.Col([
                html.H4("Список накладных"),
                dag.AgGrid(
                    id="grid-master",
                    columnDefs=[
                        {"field": "id", "headerName": "ID", "width": 70},
                        {"field": "date", "headerName": "Дата"},
                        {"field": "client", "headerName": "Клиент"},
                        {"field": "total_amount", "headerName": "Сумма", "valueFormatter": {"function": "d3.format(',.2f')(params.value)"}},
                    ],
                    rowData=[],
                    dashGridOptions={"rowSelection": "single"},
                    style={"height": "500px", "width": "100%"}
                )
            ], width=4),
            dbc.Col([
                html.H4(id="detail-header", children="Выберите накладную"),
                dag.AgGrid(
                    id="grid-detail",
                    columnDefs=[
                        {"field": "product", "headerName": "Товар", "editable": True, 
                         "cellEditor": "agSelectCellEditor", "cellEditorParams": {"values": products_list}},
                        {"field": "quantity", "headerName": "Кол-во", "editable": True, "type": "numericColumn"},
                        {"field": "price", "headerName": "Цена", "editable": False},
                        {"field": "amount", "headerName": "Сумма", "editable": False, "valueFormatter": {"function": "d3.format(',.2f')(params.value)"}},
                    ],
                    rowData=[],
                    style={"height": "400px", "width": "100%"},
                    dashGridOptions={"stopEditingWhenCellsLoseFocus": True}
                ),
                dbc.Button("Сохранить изменения", id="btn-save", color="primary", className="mt-3", disabled=True)
            ], width=4),
            dbc.Col([
                html.Div(id="chart-container", children=[
                    html.H4("Аналитика по суммам"),
                    dcc.Graph(id="chart-invoices")
                ], style={"display": "block"})
            ], width=4, id="col-chart")
        ])
    ], fluid=True)

    register_callbacks(app)
    return app
# END_FUNCTION_create_app

# START_FUNCTION_register_callbacks
def register_callbacks(app):
    @app.callback(
        [Output("grid-master", "rowData"),
         Output("chart-invoices", "figure")],
        [Input("btn-generate", "n_clicks"),
         Input("btn-save", "n_clicks")],
        prevent_initial_call=False
    )
    def update_master_and_chart(n_gen, n_save):
        return update_master_logic(ctx.triggered_id, DB_PATH)

    @app.callback(
        [Output("grid-detail", "rowData"),
         Output("detail-header", "children"),
         Output("btn-save", "disabled")],
        [Input("grid-master", "selectedRows")]
    )
    def update_detail(selected_rows):
        return update_detail_logic(selected_rows, DB_PATH)

    @app.callback(
        Output("btn-save", "n_clicks"),
        [Input("btn-save", "n_clicks")],
        [State("grid-master", "selectedRows"),
         State("grid-detail", "rowData")],
        prevent_initial_call=True
    )
    def save_changes(n_clicks, selected_rows, detail_data):
        if not selected_rows or not detail_data:
            return dash.no_update
        inv_id = selected_rows[0]["id"]
        update_invoice_lines(DB_PATH, inv_id, detail_data)
        logger.info(f"[BeliefState][IMP:10][save_changes][SAVE] Изменения сохранены для ID {inv_id} [SUCCESS]")
        return n_clicks

    @app.callback(
        Output("col-chart", "style"),
        [Input("btn-toggle-chart", "n_clicks")],
        [State("col-chart", "style")]
    )
    def toggle_chart(n_clicks, current_style):
        return toggle_chart_logic(n_clicks, current_style)
# END_FUNCTION_register_callbacks

if __name__ == "__main__":
    app = create_app()
    app.run_server(debug=True)
