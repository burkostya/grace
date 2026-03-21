# FILE:lesson_11/src/ui_controller.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Управление пользовательским интерфейсом Gradio для визуализации параболы.
# SCOPE:Создание макета UI, обработка событий кнопок, интеграция с логикой, БД и конфигом.
# INPUT:Параметры параболы от пользователя через Gradio компоненты.
# OUTPUT:Объект gr.Blocks, DataFrame с точками, Plotly Figure.
# KEYWORDS:[DOMAIN(8): UI; CONCEPT(7): Controller; TECH(9): Gradio, Plotly]
# LINKS:[USES_API(8): gradio, plotly.graph_objects, pandas; READS_DATA_FROM(7): database_manager, config_manager]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется разделение на две колонки?
# A: Согласно ТЗ, для удобства пользователя: слева управление и данные, справа визуализация.
# Q: Зачем нужны отложенные импорты внутри функций (если применимо)?
# A: В данном модуле импорты на уровне модуля допустимы, но для запуска рекомендуется Lazy Import в main.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичная реализация контроллера UI с LDD 2.0 логированием и семантической разметкой.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Обрабатывает генерацию данных и сохранение] => handle_generate
# FUNC 10[Отрисовывает график на основе данных из БД] => handle_draw
# FUNC 10[Создает и настраивает интерфейс Gradio] => create_ui
# END_MODULE_MAP
#
# START_USE_CASES:
# - [handle_generate]: User -> Click "Generate" -> DataGeneratedAndSaved
# - [handle_draw]: User -> Click "Draw" -> GraphRendered
# - [create_ui]: System -> InitializeUI -> UIReady
# END_USE_CASES

import gradio as gr
import pandas as pd
import plotly.graph_objects as go
import logging
import os

# Импорт внутренних модулей
from lesson_11.src.config_manager import load_config, save_config
from lesson_11.src.database_manager import save_points, get_points, init_db
from lesson_11.src.parabola_logic import calculate_points

# START_BLOCK_LOGGING_SETUP: [Настройка LDD 2.0 логирования]
LOG_FILE = "lesson_11/app_11.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logger = logging.getLogger("ui_controller")
# END_BLOCK_LOGGING_SETUP

# START_FUNCTION_handle_generate
# START_CONTRACT:
# PURPOSE:Генерирует точки параболы, сохраняет конфиг и данные в БД.
# INPUTS: 
# - float => a: Коэффициент a
# - float => c: Коэффициент c
# - float => x_min: Минимум x
# - float => x_max: Максимум x
# OUTPUTS: 
# - pd.DataFrame - Таблица с рассчитанными точками
# SIDE_EFFECTS: Обновляет config.json и parabola_11.db.
# KEYWORDS:[PATTERN(8): ActionHandler; CONCEPT(9): DataFlow]
# COMPLEXITY_SCORE: 6[Координация нескольких модулей: логика, БД, конфиг.]
# END_CONTRACT
def handle_generate(a, c, x_min, x_max):
    """
    Функция-обработчик для кнопки генерации данных. Она собирает параметры из UI,
    сохраняет их в файл конфигурации для персистентности настроек пользователя,
    вызывает математический модуль для расчета точек и передает результат в БД.
    Возвращает DataFrame для отображения в компоненте gr.Dataframe.
    """
    logger.info(f"[Flow][IMP:5][handle_generate][START][Params] a={a}, c={c}, x_min={x_min}, x_max={x_max} [INFO]")
    
    # START_BLOCK_SAVE_CONFIG: [Сохранение параметров в конфиг]
    config = {
        "a": a,
        "c": c,
        "x_min": x_min,
        "x_max": x_max
    }
    save_config(config)
    logger.debug(f"[IO][IMP:7][handle_generate][SAVE_CONFIG][Success] Конфигурация обновлена [SUCCESS]")
    # END_BLOCK_SAVE_CONFIG
    
    # START_BLOCK_CALCULATE: [Расчет точек]
    points = calculate_points(a, c, x_min, x_max)
    logger.info(f"[BusinessLogic][IMP:9][handle_generate][CALCULATE][Result] Рассчитано {len(points)} точек [VALUE]")
    # END_BLOCK_CALCULATE
    
    # START_BLOCK_DB_PERSIST: [Сохранение в БД]
    save_points(points)
    logger.info(f"[IO][IMP:8][handle_generate][DB_PERSIST][Success] Точки сохранены в БД [SUCCESS]")
    # END_BLOCK_DB_PERSIST
    
    # START_BLOCK_PREPARE_DF: [Подготовка DataFrame для UI]
    df = pd.DataFrame(points, columns=['x', 'y'])
    logger.debug(f"[Trace][IMP:3][handle_generate][PREPARE_DF][Done] DataFrame создан. Строк: {len(df)} [SUCCESS]")
    return df
    # END_BLOCK_PREPARE_DF
# END_FUNCTION_handle_generate

# START_FUNCTION_handle_draw
# START_CONTRACT:
# PURPOSE:Считывает данные из БД и строит график Plotly.
# INPUTS: Нет
# OUTPUTS: 
# - go.Figure - Объект графика Plotly
# SIDE_EFFECTS: Чтение из БД.
# KEYWORDS:[PATTERN(7): Visualization; CONCEPT(8): DataRetrieval]
# COMPLEXITY_SCORE: 5[Построение визуализации на основе внешних данных.]
# END_CONTRACT
def handle_draw():
    """
    Функция-обработчик для кнопки отрисовки. Она извлекает текущий набор точек из БД,
    формирует объект Figure библиотеки Plotly с настроенными осями и заголовком.
    Если данных в БД нет, возвращает пустой график с уведомлением.
    """
    logger.info(f"[Flow][IMP:5][handle_draw][START][Operation] Запрос данных для отрисовки [INFO]")
    
    # START_BLOCK_FETCH_DATA: [Получение данных из БД]
    points = get_points()
    logger.info(f"[IO][IMP:8][handle_draw][FETCH_DATA][Result] Получено {len(points)} точек для графика [VALUE]")
    # END_BLOCK_FETCH_DATA
    
    # START_BLOCK_CREATE_PLOT: [Создание Plotly Figure]
    fig = go.Figure()
    
    if points:
        df = pd.DataFrame(points, columns=['x', 'y'])
        fig.add_trace(go.Scatter(
            x=df['x'], 
            y=df['y'], 
            mode='lines+markers', 
            name='Parabola',
            line=dict(color='firebrick', width=2)
        ))
        fig.update_layout(
            title='Parabola Visualization: y = ax^2 + c',
            xaxis_title='X Axis',
            yaxis_title='Y Axis',
            template='plotly_white'
        )
        logger.info(f"[BeliefState][IMP:9][handle_draw][CREATE_PLOT][Success] График успешно сформирован [SUCCESS]")
    else:
        fig.update_layout(title='No data in database. Please generate data first.')
        logger.warning(f"[Boundary][IMP:8][handle_draw][CREATE_PLOT][NoData] Данные отсутствуют, график пуст [WARN]")
        
    return fig
    # END_BLOCK_CREATE_PLOT
# END_FUNCTION_handle_draw

# START_FUNCTION_create_ui
# START_CONTRACT:
# PURPOSE:Конструирует интерфейс Gradio Blocks.
# INPUTS: Нет
# OUTPUTS: 
# - gr.Blocks - Объект интерфейса
# SIDE_EFFECTS: Инициализирует БД при создании.
# KEYWORDS:[PATTERN(9): Factory; CONCEPT(8): LayoutDesign]
# COMPLEXITY_SCORE: 7[Сложная структура макета с привязкой событий.]
# END_CONTRACT
def create_ui():
    """
    Функция создает структуру интерфейса Gradio. Использует gr.Blocks для гибкого
    управления макетом. Реализует две колонки: панель управления и панель вывода.
    Также загружает начальные значения из конфигурации для удобства пользователя.
    """
    logger.info(f"[Flow][IMP:5][create_ui][START][Operation] Создание интерфейса Gradio [INFO]")
    
    # START_BLOCK_INIT_ENV: [Подготовка окружения]
    # BUG_FIX_CONTEXT: Удален вызов init_db(), так как он выполняется в run_lesson_11.py
    config = load_config()
    # Значения по умолчанию если конфиг пуст
    def_a = config.get("a", 1.0)
    def_c = config.get("c", 0.0)
    def_xmin = config.get("x_min", -10.0)
    def_xmax = config.get("x_max", 10.0)
    logger.debug(f"[Trace][IMP:4][create_ui][INIT_ENV][Config] Начальные значения: a={def_a}, c={def_c} [INFO]")
    # END_BLOCK_INIT_ENV

    # START_BLOCK_LAYOUT: [Определение макета UI]
    with gr.Blocks(title="Parabola Generator v11") as ui:
        gr.Markdown("## Parabola Visualization System (Lesson 11)")
        
        with gr.Row():
            # Левая колонка: Ввод и Таблица
            with gr.Column(scale=1):
                gr.Markdown("### Controls")
                slider_a = gr.Slider(minimum=-10, maximum=10, value=def_a, step=0.1, label="Coefficient a")
                slider_c = gr.Slider(minimum=-50, maximum=50, value=def_c, step=0.5, label="Coefficient c")
                slider_xmin = gr.Slider(minimum=-100, maximum=0, value=def_xmin, step=1, label="X Min")
                slider_xmax = gr.Slider(minimum=0, maximum=100, value=def_xmax, step=1, label="X Max")
                
                btn_generate = gr.Button("Generate Data", variant="primary")
                btn_draw = gr.Button("Draw Graph")
                
                table_output = gr.Dataframe(label="Generated Points", interactive=False)
            
            # Правая колонка: График
            with gr.Column(scale=2):
                gr.Markdown("### Visualization")
                plot_output = gr.Plot(label="Parabola Plot")
        
        # Привязка событий
        btn_generate.click(
            fn=handle_generate,
            inputs=[slider_a, slider_c, slider_xmin, slider_xmax],
            outputs=table_output
        )
        
        btn_draw.click(
            fn=handle_draw,
            inputs=[],
            outputs=plot_output
        )
        
        logger.info(f"[BeliefState][IMP:10][create_ui][LAYOUT][Success] Интерфейс успешно сконструирован [SUCCESS]")
    # END_BLOCK_LAYOUT
    
    return ui
# END_FUNCTION_create_ui
