# FILE: lesson_v7/src/ui_controller.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Реализация контроллера UI для Gradio интерфейса.
# SCOPE: Обработка событий UI, вызов бизнес-логики, построение графиков Plotly.
# INPUT: Параметры из UI (a, c, x_min, x_max), команды (Generate Data, Draw Graph).
# OUTPUT: Обновление таблицы данных, построение графика, обновление конфигурации.
# KEYWORDS:[DOMAIN(8): UIController; CONCEPT(7): EventHandling; TECH(9): Gradio, Plotly]
# LINKS:[USES_API(10): config_manager; USES_API(10): parabola_logic; USES_API(10): database_manager]
# END_MODULE_CONTRACT
#
# START_INVARIANTS:
# - Функция generate_data_handler ВСЕГДА сохраняет параметры в config.json и БД.
# - Функция draw_graph_handler ВСЕГДА возвращает корректный Plotly Figure.
# - Функция load_table_handler ВСЕГДА возвращает pandas DataFrame.
# END_INVARIANTS
#
# START_RATIONALE:
# Q: Почему используются отдельные обработчики для каждой кнопки?
# A: Это обеспечивает модульность и упрощает тестирование (headless-тестирование) каждой функции независимо.
# Q: Почему используется Plotly вместо Matplotlib?
# A: Plotly обеспечивает интерактивные графики, которые лучше интегрируются с Gradio и предоставляют лучший UX.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание UI контроллера.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Обработчик кнопки Generate Data: генерация и сохранение точек] => generate_data_handler
# FUNC 10[Обработчик кнопки Draw Graph: построение графика по данным из БД] => draw_graph_handler
# FUNC 10[Обработчик обновления таблицы: загрузка данных из БД] => load_table_handler
# FUNC 10[Создает и настраивает Gradio интерфейс] => create_gradio_interface
# END_MODULE_MAP
#
# START_USE_CASES:
# -[generate_data_handler]: User (UI) -> ClickGenerate -> DataGenerated
# -[draw_graph_handler]: User (UI) -> ClickDrawGraph -> GraphDisplayed
# -[load_table_handler]: Application (UIUpdate) -> LoadTable -> TableUpdated
# -[create_gradio_interface]: Application (Startup) -> CreateUI -> InterfaceReady
# END_USE_CASES

import logging
from pathlib import Path

# Импорт модулей приложения
from .config_manager import load_config, save_config
from .parabola_logic import generate_points
from .database_manager import init_database, save_points, load_points

# Настройка логирования
LOG_FILE = Path(__file__).parent.parent / "app_v7.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# START_FUNCTION_generate_data_handler
# START_CONTRACT:
# PURPOSE: Обработчик кнопки Generate Data: генерация и сохранение точек.
# INPUTS: 
# - Коэффициент a => a: float
# - Свободный член c => c: float
# - Минимальное значение x => x_min: float
# - Максимальное значение x => x_max: float
# OUTPUTS: 
# - str - Статус операции
# SIDE_EFFECTS: Сохраняет параметры в config.json, генерирует точки, сохраняет в БД.
# KEYWORDS:[PATTERN(7): EventHandler; CONCEPT(8): DataGeneration]
# END_CONTRACT
def generate_data_handler(a: float, c: float, x_min: float, x_max: float) -> str:
    """Обработчик кнопки Generate Data."""
    
    # START_BLOCK_VALIDATE_INPUTS: [Валидация входных параметров]
    logger.info(f"[UI][IMP:7][generate_data_handler][VALIDATE_INPUTS][ButtonClick] Нажата кнопка Generate Data. Параметры: a={a}, c={c}, x_range=({x_min}, {x_max}) [INFO]")
    
    if x_min >= x_max:
        logger.warning(f"[UI][IMP:8][generate_data_handler][VALIDATE_INPUTS][RangeCheck] x_min >= x_max. Local vars: x_min={x_min}, x_max={x_max} [WARN]")
        return "[ERROR] Ошибка: x_min должен быть меньше x_max."
    # END_BLOCK_VALIDATE_INPUTS
    
    # START_BLOCK_SAVE_CONFIG: [Сохранение конфигурации]
    try:
        config_data = {
            "a": a,
            "c": c,
            "x_min": x_min,
            "x_max": x_max
        }
        save_config(config_data)
        logger.info(f"[BeliefState][IMP:9][generate_data_handler][SAVE_CONFIG][ConfigSaved] Конфигурация обновлена [SUCCESS]")
    except Exception as e:
        logger.error(f"[UI][IMP:10][generate_data_handler][SAVE_CONFIG][ExceptionEnrichment] Ошибка сохранения конфигурации. Local vars: config_data={config_data}. Err: {e} [FATAL]")
        return f"[ERROR] Ошибка сохранения конфигурации: {e}"
    # END_BLOCK_SAVE_CONFIG
    
    # START_BLOCK_GENERATE_POINTS: [Генерация точек]
    try:
        points = generate_points(a, c, x_min, x_max)
        logger.info(f"[BeliefState][IMP:9][generate_data_handler][GENERATE_POINTS][PointsGenerated] Сгенерировано {len(points)} точек [VALUE]")
    except Exception as e:
        logger.error(f"[UI][IMP:10][generate_data_handler][GENERATE_POINTS][ExceptionEnrichment] Ошибка генерации точек. Err: {e} [FATAL]")
        return f"[ERROR] Ошибка генерации точек: {e}"
    # END_BLOCK_GENERATE_POINTS
    
    # START_BLOCK_SAVE_TO_DB: [Сохранение в БД]
    try:
        init_database()
        save_points(points)
        logger.info(f"[BeliefState][IMP:9][generate_data_handler][SAVE_TO_DB][DataSaved] Точки успешно сохранены в БД [SUCCESS]")
        return f"[OK] Сгенерировано и сохранено {len(points)} точек в БД."
    except Exception as e:
        logger.error(f"[UI][IMP:10][generate_data_handler][SAVE_TO_DB][ExceptionEnrichment] Ошибка сохранения в БД. Err: {e} [FATAL]")
        return f"[ERROR] Ошибка сохранения в БД: {e}"
    # END_BLOCK_SAVE_TO_DB
# END_FUNCTION_generate_data_handler

# START_FUNCTION_draw_graph_handler
# START_CONTRACT:
# PURPOSE: Обработчик кнопки Draw Graph: построение графика по данным из БД.
# INPUTS: 
# - Нет
# OUTPUTS: 
# - plotly.graph_objects.Figure - График параболы
# SIDE_EFFECTS: Отсутствует (только чтение из БД).
# KEYWORDS:[PATTERN(7): EventHandler; CONCEPT(8): Visualization]
# END_CONTRACT
def draw_graph_handler():
    """Обработчик кнопки Draw Graph."""
    
    # START_BLOCK_LOAD_POINTS: [Загрузка точек из БД]
    logger.info(f"[UI][IMP:7][draw_graph_handler][LOAD_POINTS][ButtonClick] Нажата кнопка Draw Graph [INFO]")
    
    try:
        points = load_points()
        logger.info(f"[BeliefState][IMP:9][draw_graph_handler][LOAD_POINTS][DataLoaded] Загружено {len(points)} точек из БД [VALUE]")
    except Exception as e:
        logger.error(f"[UI][IMP:10][draw_graph_handler][LOAD_POINTS][ExceptionEnrichment] Ошибка загрузки из БД. Err: {e} [FATAL]")
        # Возвращаем пустой график при ошибке
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.update_layout(title="[ERROR] Ошибка загрузки данных")
        return fig
    # END_BLOCK_LOAD_POINTS
    
    # START_BLOCK_CREATE_PLOT: [Создание графика Plotly]
    try:
        import plotly.graph_objects as go
        
        if not points:
            logger.warning(f"[UI][IMP:8][draw_graph_handler][CREATE_PLOT][EmptyData] База данных пуста. Отображение пустого графика. [WARN]")
            fig = go.Figure()
            fig.update_layout(title="Нет данных для отображения. Сначала нажмите 'Generate Data'.")
            return fig
        
        # Разделение координат
        x_values = [point[0] for point in points]
        y_values = [point[1] for point in points]
        
        # Создание графика
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode='lines+markers',
            name='Парабола',
            line=dict(color='blue', width=2),
            marker=dict(size=4)
        ))
        
        # Настройка макета
        fig.update_layout(
            title='График параболы y = ax² + c',
            xaxis_title='X',
            yaxis_title='Y',
            hovermode='closest',
            template='plotly_white'
        )
        
        logger.info(f"[BeliefState][IMP:9][draw_graph_handler][CREATE_PLOT][GraphCreated] График успешно создан [SUCCESS]")
        return fig
        
    except ImportError:
        logger.error(f"[UI][IMP:10][draw_graph_handler][CREATE_PLOT][LibraryError] plotly не установлен. [FATAL]")
        # Возвращаем текстовое представление при отсутствии библиотеки
        fig = go.Figure()
        fig.update_layout(title="[ERROR] Ошибка: plotly не установлен")
        return fig
    except Exception as e:
        logger.critical(f"[UI][IMP:10][draw_graph_handler][CREATE_PLOT][ExceptionEnrichment] Ошибка создания графика. Local vars: points_count={len(points)}. Err: {e} [FATAL]")
        fig = go.Figure()
        fig.update_layout(title="[ERROR] Ошибка создания графика")
        return fig
    # END_BLOCK_CREATE_PLOT
# END_FUNCTION_draw_graph_handler

# START_FUNCTION_load_table_handler
# START_CONTRACT:
# PURPOSE: Обработчик обновления таблицы: загрузка данных из БД.
# INPUTS: 
# - Нет
# OUTPUTS: 
# - pandas.DataFrame - Таблица с точками
# SIDE_EFFECTS: Отсутствует (только чтение из БД).
# KEYWORDS:[PATTERN(6): DataRetrieval; CONCEPT(7): TabularDisplay]
# END_CONTRACT
def load_table_handler():
    """Обработчик обновления таблицы данных."""
    
    # START_BLOCK_LOAD_POINTS: [Загрузка точек из БД]
    logger.debug(f"[UI][IMP:4][load_table_handler][LOAD_POINTS][TableUpdate] Обновление таблицы данных [INFO]")
    
    try:
        points = load_points()
        logger.info(f"[BeliefState][IMP:9][load_table_handler][LOAD_POINTS][DataLoaded] Загружено {len(points)} точек для таблицы [VALUE]")
    except Exception as e:
        logger.error(f"[UI][IMP:10][load_table_handler][LOAD_POINTS][ExceptionEnrichment] Ошибка загрузки из БД. Err: {e} [FATAL]")
        # Возвращаем пустой DataFrame при ошибке
        import pandas as pd
        return pd.DataFrame(columns=['x', 'y'])
    # END_BLOCK_LOAD_POINTS
    
    # START_BLOCK_CREATE_DATAFRAME: [Создание DataFrame]
    try:
        import pandas as pd
        
        if not points:
            logger.warning(f"[UI][IMP:8][load_table_handler][CREATE_DATAFRAME][EmptyData] База данных пуста. Возврат пустого DataFrame. [WARN]")
            return pd.DataFrame(columns=['x', 'y'])
        
        df = pd.DataFrame(points, columns=['x', 'y'])
        logger.info(f"[BeliefState][IMP:9][load_table_handler][CREATE_DATAFRAME][TableCreated] Таблица успешно создана [SUCCESS]")
        return df
        
    except ImportError:
        logger.error(f"[UI][IMP:10][load_table_handler][CREATE_DATAFRAME][LibraryError] pandas не установлен. [FATAL]")
        # Возвращаем пустой DataFrame при отсутствии библиотеки
        import pandas as pd
        return pd.DataFrame(columns=['x', 'y'])
    except Exception as e:
        logger.critical(f"[UI][IMP:10][load_table_handler][CREATE_DATAFRAME][ExceptionEnrichment] Ошибка создания DataFrame. Local vars: points_count={len(points)}. Err: {e} [FATAL]")
        import pandas as pd
        return pd.DataFrame(columns=['x', 'y'])
    # END_BLOCK_CREATE_DATAFRAME
# END_FUNCTION_load_table_handler

# START_FUNCTION_create_gradio_interface
# START_CONTRACT:
# PURPOSE: Создание и настройка Gradio интерфейса.
# INPUTS: 
# - Нет
# OUTPUTS: 
# - gr.Blocks - Настроенный Gradio интерфейс
# SIDE_EFFECTS: Отсутствует (только создание объекта интерфейса).
# KEYWORDS:[PATTERN(8): UIBuilder; CONCEPT(9): InterfaceComposition]
# END_CONTRACT
def create_gradio_interface():
    """Создает и настраивает Gradio интерфейс."""
    
    # START_BLOCK_LOAD_DEFAULT_CONFIG: [Загрузка дефолтных значений]
    logger.info(f"[UI][IMP:7][create_gradio_interface][LOAD_DEFAULT_CONFIG][InterfaceInit] Создание Gradio интерфейса [INFO]")
    
    try:
        config = load_config()
        default_a = config['a']
        default_c = config['c']
        default_x_min = config['x_min']
        default_x_max = config['x_max']
        logger.debug(f"[UI][IMP:4][create_gradio_interface][LOAD_DEFAULT_CONFIG][ConfigLoaded] Дефолтные значения: a={default_a}, c={default_c}, x_range=({default_x_min}, {default_x_max}) [INFO]")
    except Exception as e:
        logger.warning(f"[UI][IMP:8][create_gradio_interface][LOAD_DEFAULT_CONFIG][ConfigError] Ошибка загрузки конфигурации. Использование дефолтных значений. Err: {e} [WARN]")
        default_a = 1.0
        default_c = 0.0
        default_x_min = -10.0
        default_x_max = 10.0
    # END_BLOCK_LOAD_DEFAULT_CONFIG
    
    # START_BLOCK_CREATE_INTERFACE: [Создание компонентов Gradio]
    try:
        import gradio as gr
        
        with gr.Blocks(title="Lesson v7 - Парабола") as interface:
            gr.Markdown("# Генератор параболы y = ax² + c")
            
            with gr.Row():
                # Левая колонка: управление и таблица
                with gr.Column():
                    gr.Markdown("### Параметры параболы")
                    
                    a_slider = gr.Slider(
                        minimum=-10.0,
                        maximum=10.0,
                        value=default_a,
                        step=0.1,
                        label="Коэффициент a"
                    )
                    c_slider = gr.Slider(
                        minimum=-10.0,
                        maximum=10.0,
                        value=default_c,
                        step=0.1,
                        label="Коэффициент c"
                    )
                    x_min_slider = gr.Slider(
                        minimum=-100.0,
                        maximum=100.0,
                        value=default_x_min,
                        step=1.0,
                        label="X min"
                    )
                    x_max_slider = gr.Slider(
                        minimum=-100.0,
                        maximum=100.0,
                        value=default_x_max,
                        step=1.0,
                        label="X max"
                    )
                    
                    generate_btn = gr.Button("Generate Data", variant="primary")
                    draw_btn = gr.Button("Draw Graph", variant="secondary")
                    
                    output_text = gr.Textbox(label="Статус", interactive=False)
                    
                    gr.Markdown("### Таблица данных")
                    data_table = gr.Dataframe(label="Точки параболы")
                
                # Правая колонка: график
                with gr.Column():
                    gr.Markdown("### График")
                    plot_display = gr.Plot(label="График параболы")
            
            # START_BLOCK_SETUP_EVENTS: [Настройка обработчиков событий]
            # Обработчик кнопки Generate Data
            generate_btn.click(
                fn=generate_data_handler,
                inputs=[a_slider, c_slider, x_min_slider, x_max_slider],
                outputs=output_text
            ).then(
                fn=load_table_handler,
                outputs=data_table
            )
            
            # Обработчик кнопки Draw Graph
            draw_btn.click(
                fn=draw_graph_handler,
                outputs=plot_display
            )
            
            # Обработчик загрузки страницы: отображение текущей таблицы
            interface.load(
                fn=load_table_handler,
                outputs=data_table
            )
            # END_BLOCK_SETUP_EVENTS
            
        logger.info(f"[BeliefState][IMP:9][create_gradio_interface][CREATE_INTERFACE][InterfaceReady] Gradio интерфейс успешно создан [SUCCESS]")
        return interface
        
    except ImportError:
        logger.error(f"[UI][IMP:10][create_gradio_interface][CREATE_INTERFACE][LibraryError] gradio не установлен. Невозможно создать интерфейс. [FATAL]")
        raise ImportError("gradio не установлен. Установите gradio для работы UI.")
    except Exception as e:
        logger.critical(f"[UI][IMP:10][create_gradio_interface][CREATE_INTERFACE][ExceptionEnrichment] Ошибка создания интерфейса. Err: {e} [FATAL]")
        raise
    # END_BLOCK_CREATE_INTERFACE
# END_FUNCTION_create_gradio_interface
