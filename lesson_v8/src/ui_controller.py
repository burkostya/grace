# FILE: lesson_v8/src/ui_controller.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Контроллер Gradio интерфейса для визуализации генерации параболы.
# SCOPE: Создание и управление UI с двумя колонками (управление и график).
# INPUT: Значения параметров из UI (a, c, x_min, x_max).
# OUTPUT: DataFrame с точками для таблицы, Plotly Figure для графика.
# KEYWORDS:[DOMAIN(9): UserInterface; CONCEPT(8): Gradio; TECH(9): Plotly]
# LINKS:[USES_API(8): config_manager, parabola_logic, database_manager; USES_API(9): gradio, plotly]
# END_MODULE_CONTRACT
#
# START_INVARIANTS:
# - Функция handle_generate ВСЕГДА возвращает кортеж (DataFrame, None).
# - Функция handle_draw_graph ВСЕГДА возвращает кортеж (None, Plotly Figure).
# - При успешной генерации config.json ОБНОВЛЯЕТСЯ с новыми параметрами.
# END_INVARIANTS
#
# START_RATIONALE:
# Q: Почему используется Gradio вместо других UI фреймворков?
# A: Gradio обеспечивает быстрое создание интерактивных интерфейсов для ML/научных приложений с минимальным кодом.
# Q: Почему интерфейс разделен на две колонки?
# A: Это соответствует требованиям: левая колонка для управления и данных, правая для визуализации.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание UI контроллера Gradio.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Обработчик кнопки Generate Data] => handle_generate
# FUNC 10[Обработчик кнопки Draw Graph] => handle_draw_graph
# FUNC 10[Создает и возвращает Gradio интерфейс] => create_interface
# END_MODULE_MAP
#
# START_USE_CASES:
# -[handle_generate]: User (ButtonClick) -> GenerateData -> DataSavedInDB
# -[handle_draw_graph]: User (ButtonClick) -> DrawGraph -> GraphDisplayed
# -[create_interface]: Application (Startup) -> CreateUI -> InterfaceReady
# END_USE_CASES

import logging
import os

import gradio as gr
import pandas as pd
import plotly.graph_objects as go

# Настройка логирования в файл
LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "app_v8.log")
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Импорт модулей приложения
from .config_manager import load_config, save_config
from .parabola_logic import generate_parabola_points
from .database_manager import init_database, save_points, load_points


# START_FUNCTION_handle_generate
# START_CONTRACT:
# PURPOSE: Обрабатывает нажатие кнопки Generate Data: сохраняет параметры, генерирует точки, сохраняет в БД.
# INPUTS: 
# - a => a: float (коэффициент при x^2)
# - c => c: float (свободный член)
# - x_min => x_min: float (минимальное значение x)
# - x_max => x_max: float (максимальное значение x)
# OUTPUTS: 
# - tuple - (pd.DataFrame, None) - DataFrame с точками для таблицы, None для графика
# SIDE_EFFECTS: Обновляет config.json, генерирует точки, сохраняет в БД SQLite.
# KEYWORDS:[PATTERN(8): EventHandler; CONCEPT(7): DataGeneration]
# COMPLEXITY_SCORE: 6[Средняя сложность: сохранение конфига, генерация, сохранение в БД.]
# END_CONTRACT
def handle_generate(a: float, c: float, x_min: float, x_max: float) -> tuple:
    """
    Функция выполняет обработку нажатия кнопки Generate Data в Gradio интерфейсе.
    Сохраняет введенные пользователем параметры в config.json, генерирует точки параболы
    по формуле y = ax^2 + c и сохраняет их в базу данных SQLite.
    Возвращает DataFrame с точками для отображения в таблице интерфейса.
    Функция обеспечивает полный цикл генерации данных с сохранением состояния приложения.
    """
    
    # START_BLOCK_VALIDATE_INPUTS: [Проверка входных параметров]
    if x_min >= x_max:
        logger.error(f"[InvalidInput][IMP:9][handle_generate][VALIDATE_INPUTS][ValueError] x_min должен быть меньше x_max. Получены: x_min={x_min}, x_max={x_max} [ERROR]")
        return pd.DataFrame(columns=['x', 'y']), None
    
    logger.debug(f"[ParamsValidated][IMP:4][handle_generate][VALIDATE_INPUTS][ParamCheck] Параметры валидны: a={a}, c={c}, x_min={x_min}, x_max={x_max} [INFO]")
    # END_BLOCK_VALIDATE_INPUTS
    
    # START_BLOCK_SAVE_CONFIG: [Сохранение параметров в config.json]
    try:
        config = {
            'a': a,
            'c': c,
            'x_min': x_min,
            'x_max': x_max
        }
        save_config(config)
        logger.info(f"[ConfigSaved][IMP:8][handle_generate][SAVE_CONFIG][FileOperation] Параметры сохранены в config.json [SUCCESS]")
        
    except Exception as e:
        logger.critical(f"[ConfigError][IMP:10][handle_generate][SAVE_CONFIG][ExceptionEnrichment] Ошибка сохранения конфигурации. Local vars: a={a}, c={c}, x_min={x_min}, x_max={x_max}. Err: {e} [FATAL]")
        return pd.DataFrame(columns=['x', 'y']), None
    # END_BLOCK_SAVE_CONFIG
    
    # START_BLOCK_GENERATE_POINTS: [Генерация точек параболы]
    try:
        df = generate_parabola_points(a, c, x_min, x_max)
        logger.info(f"[PointsGenerated][IMP:9][handle_generate][GENERATE_POINTS][Calculation] Сгенерировано {len(df)} точек [SUCCESS]")
        
    except Exception as e:
        logger.critical(f"[GenerationError][IMP:10][handle_generate][GENERATE_POINTS][ExceptionEnrichment] Ошибка генерации точек. Local vars: a={a}, c={c}, x_min={x_min}, x_max={x_max}. Err: {e} [FATAL]")
        return pd.DataFrame(columns=['x', 'y']), None
    # END_BLOCK_GENERATE_POINTS
    
    # START_BLOCK_SAVE_TO_DATABASE: [Сохранение в БД]
    try:
        init_database()
        save_points(df)
        logger.info(f"[PointsSaved][IMP:9][handle_generate][SAVE_TO_DATABASE][DBOperation] Точки успешно сохранены в БД [SUCCESS]")
        
    except Exception as e:
        logger.critical(f"[DatabaseError][IMP:10][handle_generate][SAVE_TO_DATABASE][ExceptionEnrichment] Ошибка сохранения в БД. Err: {e} [FATAL]")
        return pd.DataFrame(columns=['x', 'y']), None
    # END_BLOCK_SAVE_TO_DATABASE
    
    return df, None
# END_FUNCTION_handle_generate


# START_FUNCTION_handle_draw_graph
# START_CONTRACT:
# PURPOSE: Обрабатывает нажатие кнопки Draw Graph: считывает данные из БД и строит график.
# INPUTS: 
# Отсутствуют (функция не принимает аргументов от UI)
# OUTPUTS: 
# - tuple - (None, go.Figure) - None для таблицы, Plotly Figure для графика
# SIDE_EFFECTS: Отсутствуют (чистая функция чтения).
# KEYWORDS:[PATTERN(8): EventHandler; CONCEPT(7): DataVisualization]
# COMPLEXITY_SCORE: 4[Низкая сложность: чтение из БД, создание графика.]
# END_CONTRACT
def handle_draw_graph() -> tuple:
    """
    Функция выполняет обработку нажатия кнопки Draw Graph в Gradio интерфейсе.
    Считывает текущие данные точек параболы из базы данных SQLite и строит
    интерактивный график с использованием библиотеки Plotly.
    Возвращает Plotly Figure для отображения в правой колонке интерфейса.
    Если база данных пуста, создается пустой график.
    """
    
    # START_BLOCK_LOAD_FROM_DATABASE: [Загрузка данных из БД]
    try:
        df = load_points()
        logger.info(f"[PointsLoaded][IMP:8][handle_draw_graph][LOAD_FROM_DATABASE][DBOperation] Загружено {len(df)} точек из БД [SUCCESS]")
        
    except Exception as e:
        logger.critical(f"[DatabaseError][IMP:10][handle_draw_graph][LOAD_FROM_DATABASE][ExceptionEnrichment] Ошибка загрузки из БД. Err: {e} [FATAL]")
        return None, go.Figure()
    # END_BLOCK_LOAD_FROM_DATABASE
    
    # START_BLOCK_CREATE_GRAPH: [Создание Plotly графика]
    try:
        fig = go.Figure()
        
        if len(df) > 0:
            fig.add_trace(go.Scatter(
                x=df['x'],
                y=df['y'],
                mode='lines+markers',
                name='Парабола',
                line=dict(color='blue', width=2),
                marker=dict(size=4)
            ))
            
            fig.update_layout(
                title='График параболы y = ax^2 + c',
                xaxis_title='x',
                yaxis_title='y',
                hovermode='closest'
            )
            
            logger.info(f"[GraphCreated][IMP:9][handle_draw_graph][CREATE_GRAPH][Visualization] График создан с {len(df)} точками [SUCCESS]")
        else:
            fig.update_layout(
                title='График параболы (нет данных)',
                xaxis_title='x',
                yaxis_title='y'
            )
            
            logger.warning(f"[EmptyData][IMP:7][handle_draw_graph][CREATE_GRAPH][DataCheck] База данных пуста, создан пустой график [WARN]")
        
        return None, fig
        
    except Exception as e:
        logger.critical(f"[SystemError][IMP:10][handle_draw_graph][CREATE_GRAPH][ExceptionEnrichment] Ошибка создания графика. Err: {e} [FATAL]")
        return None, go.Figure()
    # END_BLOCK_CREATE_GRAPH
# END_FUNCTION_handle_draw_graph


# START_FUNCTION_create_interface
# START_CONTRACT:
# PURPOSE: Создает и возвращает Gradio интерфейс с двумя колонками (управление и график).
# INPUTS: 
# Отсутствуют (функция не принимает аргументов)
# OUTPUTS: 
# - gr.Blocks - Объект Gradio интерфейса
# SIDE_EFFECTS: Отсутствует (функция создает интерфейс, но не запускает его).
# KEYWORDS:[PATTERN(9): FactoryPattern; CONCEPT(8): UIComposition]
# COMPLEXITY_SCORE: 5[Средняя сложность: создание компонентов UI и связывание обработчиков.]
# END_CONTRACT
def create_interface() -> gr.Blocks:
    """
    Функция выполняет создание Gradio интерфейса для приложения генерации параболы.
    Интерфейс разделен на две колонки: левая для управления и отображения таблицы данных,
    правая для визуализации графика параболы.
    Левая колонка содержит поля ввода для параметров a, c, x_min, x_max с ползунками,
    кнопку Generate Data для генерации точек, кнопку Draw Graph для построения графика
    и компонент Dataframe для отображения таблицы точек.
    Правая колонка содержит компонент Plot для интерактивного графика Plotly.
    """
    
    # START_BLOCK_LOAD_INITIAL_CONFIG: [Загрузка начальных параметров]
    try:
        config = load_config()
        initial_a = config['a']
        initial_c = config['c']
        initial_x_min = config['x_min']
        initial_x_max = config['x_max']
        
        logger.info(f"[ConfigLoaded][IMP:8][create_interface][LOAD_INITIAL_CONFIG][DataLoad] Начальные параметры загружены: a={initial_a}, c={initial_c}, x_min={initial_x_min}, x_max={initial_x_max} [SUCCESS]")
        
    except Exception as e:
        logger.warning(f"[ConfigWarning][IMP:7][create_interface][LOAD_INITIAL_CONFIG][ExceptionEnrichment] Ошибка загрузки конфигурации, используются дефолтные значения. Err: {e} [WARN]")
        initial_a = 1.0
        initial_c = 0.0
        initial_x_min = -10.0
        initial_x_max = 10.0
    # END_BLOCK_LOAD_INITIAL_CONFIG
    
    # START_BLOCK_CREATE_INTERFACE: [Создание компонентов UI]
    with gr.Blocks(title="Генератор параболы") as interface:
        gr.Markdown("# Генератор параболы y = ax^2 + c")
        
        with gr.Row():
            # Левая колонка: Управление и таблица данных
            with gr.Column():
                gr.Markdown("## Параметры параболы")
                
                a_input = gr.Slider(
                    minimum=-10.0,
                    maximum=10.0,
                    step=0.1,
                    value=initial_a,
                    label="Коэффициент a"
                )
                
                c_input = gr.Slider(
                    minimum=-10.0,
                    maximum=10.0,
                    step=0.1,
                    value=initial_c,
                    label="Коэффициент c"
                )
                
                x_min_input = gr.Slider(
                    minimum=-50.0,
                    maximum=0.0,
                    step=1.0,
                    value=initial_x_min,
                    label="x_min"
                )
                
                x_max_input = gr.Slider(
                    minimum=0.0,
                    maximum=50.0,
                    step=1.0,
                    value=initial_x_max,
                    label="x_max"
                )
                
                with gr.Row():
                    generate_btn = gr.Button("Generate Data", variant="primary")
                    draw_btn = gr.Button("Draw Graph", variant="secondary")
                
                gr.Markdown("## Таблица точек")
                dataframe_output = gr.Dataframe(
                    label="Точки параболы",
                    headers=["x", "y"],
                    datatype=["number", "number"]
                )
            
            # Правая колонка: График
            with gr.Column():
                gr.Markdown("## График")
                plot_output = gr.Plot(label="Интерактивный график")
        
        # START_BLOCK_BIND_HANDLERS: [Связывание обработчиков событий]
        generate_btn.click(
            fn=handle_generate,
            inputs=[a_input, c_input, x_min_input, x_max_input],
            outputs=[dataframe_output, plot_output]
        )
        
        draw_btn.click(
            fn=handle_draw_graph,
            inputs=[],
            outputs=[dataframe_output, plot_output]
        )
        # END_BLOCK_BIND_HANDLERS
        
        logger.info(f"[InterfaceCreated][IMP:9][create_interface][CREATE_INTERFACE][UIOperation] Gradio интерфейс успешно создан [SUCCESS]")
    # END_BLOCK_CREATE_INTERFACE
    
    return interface
# END_FUNCTION_create_interface
