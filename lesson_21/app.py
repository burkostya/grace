# FILE:lesson_21/app.py
# VERSION:2.0.0
# START_MODULE_CONTRACT:
# PURPOSE:UI и Callbacks для ERP-прототипа на Dash (Flux Pattern).
# SCOPE: Определение макета (3 колонки), управление состоянием через dcc.Store.
# END_MODULE_CONTRACT

import dash
from dash import dcc, html, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import plotly.express as px
import pandas as pd
import logging
import sys
from lesson_21 import handlers, db_manager

# START_BLOCK_LOGGING: [Настройка логирования LDD 2.0]
log_file = "lesson_21/app.log"
logger = logging.getLogger("lesson_21.app")
logger.setLevel(logging.INFO)
if logger.hasHandlers(): logger.handlers.clear()
fh = logging.FileHandler(log_file, mode='a', encoding='utf-8')
fh.setFormatter(logging.Formatter('%(asctime)s [LDD][IMP:10][%(name)s] %(message)s'))
logger.addHandler(fh)
sh = logging.StreamHandler(sys.stdout)
logger.addHandler(sh)
logger.info("[INIT] Модуль app.py v2.0.0 (Flux Pattern) загружен.")
# END_BLOCK_LOGGING

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# START_BLOCK_LAYOUT: [Макет UI]
app.layout = dbc.Container([
    # Глобальное состояние (Flux State)
    dcc.Store(id='db-trigger', data=0),
    dcc.Store(id='selected-invoice-id', data=None),
    dcc.Store(id='selected-search-item-id', data=None),
    
    dbc.Row([
        dbc.Col([
            html.H2("ERP Prototype v2.0.0 (Flux Pattern)", className="text-primary mb-4"),
            dbc.Button("Generate Demo Invoice", id="btn-generate", color="info", className="me-2"),
        ], width=12)
    ], className="mt-3"),

    dbc.Row([
        # 1. Левая колонка (Master)
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Invoices (Master)"),
                dbc.CardBody([
                    dag.AgGrid(
                        id="grid-invoices",
                        columnDefs=[
                            {"field": "id", "headerName": "ID", "width": 70},
                            {"field": "date", "headerName": "Date"},
                            {"field": "client_name", "headerName": "Client"},
                            {"field": "total_sum", "headerName": "Total", "valueFormatter": {"function": "d3.format('($,.2f')(params.value)"}},
                        ],
                        rowData=[],
                        getRowId="params.data.id",
                        dashGridOptions={"rowSelection": "single"},
                        style={"height": "600px"}
                    )
                ])
            ])
        ], width=3),

        # 2. Центральная колонка (Search & Detail)
        dbc.Col([
            # Блок 1: Поиск и добавление
            dbc.Card([
                dbc.CardHeader("Block 1: Search & Add Item"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(dbc.Input(id="input-search", placeholder="Search..."), width=8),
                        dbc.Col(dbc.Button("Search", id="btn-search", color="primary", className="w-100"), width=4),
                    ], className="mb-2"),
                    dag.AgGrid(
                        id="grid-search-results",
                        columnDefs=[
                            {"field": "sku", "headerName": "SKU"},
                            {"field": "name", "headerName": "Name"},
                            {"field": "price", "headerName": "Price"},
                        ],
                        rowData=[],
                        getRowId="params.data.id",
                        dashGridOptions={"rowSelection": "single"},
                        style={"height": "200px"},
                        className="mb-2"
                    ),
                    dbc.Row([
                        dbc.Col(dbc.Input(id="input-qty", type="number", value=1, min=1), width=4),
                        dbc.Col(dbc.Button("Add Selected Item", id="btn-add-item", color="success", className="w-100"), width=8),
                    ])
                ])
            ], className="mb-3"),

            # Блок 2: Строки накладной
            dbc.Card([
                dbc.CardHeader("Block 2: Invoice Lines (Detail)"),
                dbc.CardBody([
                    dag.AgGrid(
                        id="grid-lines",
                        columnDefs=[
                            {"field": "name", "headerName": "Item Name"},
                            {"field": "sku", "headerName": "SKU", "width": 100},
                            {"field": "qty", "headerName": "Qty", "editable": True, "cellDataType": "number"},
                            {"field": "price", "headerName": "Price"},
                            {"field": "line_sum", "headerName": "Sum"},
                        ],
                        rowData=[],
                        getRowId="params.data.line_id",
                        dashGridOptions={"rowSelection": "single"},
                        style={"height": "300px"}
                    ),
                    dbc.Button("Delete Selected Line", id="btn-delete-line", color="danger", className="mt-2 w-100")
                ])
            ])
        ], width=5),

        # 3. Правая колонка (Analytics)
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Analytics"),
                dbc.CardBody([dcc.Graph(id="graph-analytics")])
            ])
        ], width=4)
    ])
], fluid=True)
# END_BLOCK_LAYOUT

# START_BLOCK_CALLBACKS: [Flux Pattern Callbacks]

# --- ГРУППА 1: Управление Состоянием (State Setters) ---

@callback(
    Output('selected-invoice-id', 'data'),
    Input('grid-invoices', 'selectedRows')
)
def set_selected_invoice(selected_rows):
    inv_id = selected_rows[0]['id'] if selected_rows else None
    logger.info(f"[UI][IMP:7][set_selected_invoice] Selected Invoice ID: {inv_id}")
    return inv_id

@callback(
    Output('selected-search-item-id', 'data'),
    Input('grid-search-results', 'selectedRows')
)
def set_selected_item(selected_rows):
    item_id = selected_rows[0]['id'] if selected_rows else None
    logger.info(f"[UI][IMP:7][set_selected_item] Selected Item ID: {item_id}")
    return item_id

# --- ГРУППА 2: Операции Записи (Write Actions -> DB Trigger) ---

@callback(
    Output('db-trigger', 'data'),
    Input('btn-generate', 'n_clicks'),
    Input('btn-add-item', 'n_clicks'),
    Input('btn-delete-line', 'n_clicks'),
    Input('grid-lines', 'cellValueChanged'),
    State('selected-invoice-id', 'data'),
    State('selected-search-item-id', 'data'),
    State('input-qty', 'value'),
    State('grid-lines', 'selectedRows'),
    State('db-trigger', 'data'),
    prevent_initial_call=True
)
def handle_db_writes(btn_gen, btn_add, btn_del, cell_change, inv_id, item_id, qty, selected_lines, trigger_val):
    triggered_id = ctx.triggered_id
    logger.info(f"[UI][IMP:7][handle_db_writes] Triggered by: {triggered_id}")

    # Гарантируем, что trigger_val - число
    current_trigger = trigger_val if trigger_val is not None else 0

    success = False
    if triggered_id == 'btn-generate':
        handlers.create_demo_invoice(f"Client {pd.Timestamp.now().strftime('%H:%M:%S')}")
        success = True
    
    elif triggered_id == 'btn-add-item' and inv_id and item_id:
        success = handlers.add_line_to_invoice(inv_id, item_id, qty)
    
    elif triggered_id == 'btn-delete-line' and selected_lines:
        line_id = selected_lines[0]['line_id']
        success = handlers.delete_line(line_id)

    elif triggered_id == 'grid-lines' and cell_change:
        logger.info(f"[DebugProbe] cell_change: {cell_change}")
        change = cell_change[0]
        # В Ag-Grid colId может отличаться от field. Проверяем оба.
        if change.get('colId') == 'qty' or change.get('field') == 'qty':
            line_id = change['data']['line_id']
            # В Dash Ag-Grid новое значение в поле 'value'
            new_qty = int(change['value'])
            success = handlers.update_line_qty(line_id, new_qty)
            logger.info(f"[DebugProbe] Update success: {success}")

    if success:
        return current_trigger + 1
    return dash.no_update

# --- ГРУППА 3: Операции Чтения (Read Actions / UI Updaters) ---

@callback(
    Output('grid-invoices', 'rowData'),
    Input('db-trigger', 'data')
)
def update_invoices_grid(trigger):
    logger.info(f"[UI][IMP:7][update_invoices_grid] Refreshing invoices. Trigger: {trigger}")
    return handlers.get_invoices()

@callback(
    Output('graph-analytics', 'figure'),
    Input('db-trigger', 'data')
)
def update_analytics_graph(trigger):
    logger.info(f"[UI][IMP:7][update_analytics_graph] Refreshing analytics. Trigger: {trigger}")
    invoices = handlers.get_invoices()
    df = pd.DataFrame(invoices)
    if not df.empty:
        return px.bar(df, x="client_name", y="total_sum", title="Invoice Totals", color="total_sum")
    return px.bar(title="No Data")

@callback(
    Output('grid-lines', 'rowData'),
    Input('selected-invoice-id', 'data'),
    Input('db-trigger', 'data')
)
def update_lines_grid(inv_id, trigger):
    logger.info(f"[UI][IMP:7][update_lines_grid] Refreshing lines for {inv_id}. Trigger: {trigger}")
    if not inv_id: return []
    return handlers.get_invoice_lines(inv_id)

@callback(
    Output('grid-search-results', 'rowData'),
    Input('btn-search', 'n_clicks'),
    State('input-search', 'value'),
    prevent_initial_call=False
)
def update_search_results(n_clicks, keyword):
    logger.info(f"[UI][IMP:7][update_search_results] Searching for: {keyword!r}")
    # Если поиск пустой, возвращаем все товары для удобства
    search_term = keyword if keyword else ""
    results = handlers.search_items(search_term)
    logger.info(f"[BeliefState][IMP:9][update_search_results] Found {len(results)} items")
    return results

# END_BLOCK_CALLBACKS

if __name__ == "__main__":
    db_manager.init_db()
    app.run(debug=True, port=8051, use_reloader=False)
