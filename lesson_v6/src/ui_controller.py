# FILE: lesson_v6/src/ui_controller.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Контроллер Gradio интерфейса для Lesson 6.
# SCOPE: Обработка событий UI, обновление конфигурации, генерация данных, визуализация.
# INPUT: Параметры из UI (a, c, x_min, x_max), действия пользователя (кнопки).
# OUTPUT: Обновленный DataFrame, Plotly Figure, сообщения о статусе.
# KEYWORDS:[DOMAIN(8): UserInterface; CONCEPT(7): Gradio; TECH(9): Plotly]
# LINKS:[USES_API(8): config_manager, database_manager, parabola_logic]
# END_MODULE_CONTRACT
#
# START_INVARIANTS:
# - Функция generate_data_handler ВСЕГДА обновляет config.json и перезаписывает БД.
# - Функция draw_graph_handler ВСЕГДА возвращает объект Plotly Figure.
# END_INVARIANTS
#
# START_RATIONALE:
# Q: Почему обработчики возвращают кортежи (component1, component2)?
# A: Gradio поддерживает множественный возврат для одновременного обновления нескольких компонентов.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание UI контроллера с LDD 2.0 логированием.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Обработчик кнопки Generate Data] => generate_data_handler
# FUNC 10[Обработчик кнопки Draw Graph] => draw_graph_handler
# FUNC 10[Создание интерфейса Gradio] => create_interface
# END_MODULE_MAP
#
# START_USE_CASES:
# -[generate_data_handler]: User (UI) -> GenerateData -> DataGeneratedAndDisplayed
# -[draw_graph_handler]: User (UI) -> DrawGraph -> GraphDisplayed
# END_USE_CASES

import logging
import pandas as pd
import plotly.graph_objects as go

# Импорт модулей проекта
from lesson_v6 import CONFIG_PATH, DB_PATH, LOG_PATH
from lesson_v6.src.config_manager import load_config, save_config
from lesson_v6.src.database_manager import initialize_database, save_points, load_points
from lesson_v6.src.parabola_logic import calculate_parabola_points

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# START_FUNCTION_generate_data_handler
# START_CONTRACT:
# PURPOSE: Обработчик кнопки "Generate Data" - генерация и сохранение точек.
# INPUTS: 
# - [Коэффициент a] => a: float
# - [Коэффициент c] => c: float
# - [Минимальное значение x] => x_min: float
# - [Максимальное значение x] => x_max: float
# OUTPUTS: 
# - tuple - (pd.DataFrame, str) - DataFrame с данными, сообщение о статусе
# SIDE_EFFECTS: Обновляет config.json, перезаписывает таблицу points в БД.
# KEYWORDS:[PATTERN(6): EventHandler; CONCEPT(8): StateUpdate]
# END_CONTRACT
def generate_data_handler(a: float, c: float, x_min: float, x_max: float) -> tuple:
    """Обрабатывает нажатие кнопки Generate Data."""
    
    # START_BLOCK_VALIDATE_INPUT: [Валидация входных параметров]
    if x_min >= x_max:
        error_msg = f"Ошибка: x_min ({x_min}) должен быть меньше x_max ({x_max})"
        logger.error(f"[ValidationError][IMP:7][generate_data_handler][VALIDATE_INPUT][ConditionCheck] {error_msg} [ERROR]")
        return None, error_msg
    # END_BLOCK_VALIDATE_INPUT

    # START_BLOCK_UPDATE_CONFIG: [Обновление конфигурации]
    try:
        config = {'a': a, 'c': c, 'x_min': x_min, 'x_max': x_max}
        save_config(config, CONFIG_PATH)
        logger.info(f"[ConfigUpdate][IMP:8][generate_data_handler][UPDATE_CONFIG][ReturnData] Конфигурация обновлена: {config} [VALUE]")
    except Exception as e:
        error_msg = f"Ошибка сохранения конфигурации: {e}"
        logger.critical(f"[SystemError][IMP:10][generate_data_handler][UPDATE_CONFIG][ExceptionEnrichment] {error_msg} [FATAL]")
        return None, error_msg
    # END_BLOCK_UPDATE_CONFIG

    # START_BLOCK_INITIALIZE_DATABASE: [Инициализация БД]
    try:
        initialize_database(DB_PATH)
        logger.info(f"[DatabaseInit][IMP:8][generate_data_handler][INITIALIZE_DATABASE][ReturnData] База данных инициализирована [VALUE]")
    except Exception as e:
        error_msg = f"Ошибка инициализации БД: {e}"
        logger.critical(f"[SystemError][IMP:10][generate_data_handler][INITIALIZE_DATABASE][ExceptionEnrichment] {error_msg} [FATAL]")
        return None, error_msg
    # END_BLOCK_INITIALIZE_DATABASE

    # START_BLOCK_CALCULATE_POINTS: [Расчет точек параболы]
    try:
        points = calculate_parabola_points(a, c, x_min, x_max)
        logger.info(f"[Calculation][IMP:9][generate_data_handler][CALCULATE_POINTS][ReturnData] Рассчитано {len(points)} точек [VALUE]")
    except Exception as e:
        error_msg = f"Ошибка расчета точек: {e}"
        logger.critical(f"[SystemError][IMP:10][generate_data_handler][CALCULATE_POINTS][ExceptionEnrichment] {error_msg} [FATAL]")
        return None, error_msg
    # END_BLOCK_CALCULATE_POINTS

    # START_BLOCK_SAVE_POINTS: [Сохранение точек в БД]
    try:
        save_points(points, DB_PATH)
        logger.info(f"[DatabaseSave][IMP:9][generate_data_handler][SAVE_POINTS][ReturnData] Точки успешно сохранены в БД [VALUE]")
    except Exception as e:
        error_msg = f"Ошибка сохранения точек: {e}"
        logger.critical(f"[SystemError][IMP:10][generate_data_handler][SAVE_POINTS][ExceptionEnrichment] {error_msg} [FATAL]")
        return None, error_msg
    # END_BLOCK_SAVE_POINTS

    # START_BLOCK_RETURN_DATAFRAME: [Формирование и возврат DataFrame]
    df = pd.DataFrame(points)
    success_msg = f"[OK] Сгенерировано {len(points)} точек параболы"
    logger.info(f"[BeliefState][IMP:9][generate_data_handler][RETURN_DATAFRAME][ReturnData] {success_msg} [VALUE]")
    return df, success_msg
    # END_BLOCK_RETURN_DATAFRAME
# END_FUNCTION_generate_data_handler

# START_FUNCTION_draw_graph_handler
# START_CONTRACT:
# PURPOSE: Обработчик кнопки "Draw Graph" - построение графика.
# INPUTS: Отсутствуют (данные берутся из БД).
# OUTPUTS: 
# - go.Figure - Объект графика Plotly
# SIDE_EFFECTS: Отсутствуют.
# KEYWORDS:[PATTERN(6): EventHandler; CONCEPT(8): Visualization]
# END_CONTRACT
def draw_graph_handler() -> go.Figure:
    """Обрабатывает нажатие кнопки Draw Graph."""
    
    # START_BLOCK_LOAD_POINTS: [Загрузка точек из БД]
    try:
        points = load_points(DB_PATH)
        logger.info(f"[DatabaseLoad][IMP:8][draw_graph_handler][LOAD_POINTS][ReturnData] Загружено {len(points)} точек из БД [VALUE]")
    except Exception as e:
        error_msg = f"Ошибка загрузки точек: {e}"
        logger.critical(f"[SystemError][IMP:10][draw_graph_handler][LOAD_POINTS][ExceptionEnrichment] {error_msg} [FATAL]")
        # Возвращаем пустой график с ошибкой
        fig = go.Figure()
        fig.update_layout(title=f"Ошибка: {error_msg}")
        return fig
    # END_BLOCK_LOAD_POINTS

    # START_BLOCK_CREATE_PLOT: [Создание графика Plotly]
    if not points:
        logger.warning(f"[DataCheck][IMP:5][draw_graph_handler][CREATE_PLOT][ConditionCheck] Нет данных для построения графика [WARN]")
        fig = go.Figure()
        fig.update_layout(title="Нет данных. Сначала нажмите 'Generate Data'")
        return fig
    
    x_values = [p['x'] for p in points]
    y_values = [p['y'] for p in points]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines+markers',
        name='Парабола',
        line=dict(color='blue', width=2),
        marker=dict(size=4)
    ))
    
    fig.update_layout(
        title='График параболы',
        xaxis_title='X',
        yaxis_title='Y',
        hovermode='closest'
    )
    
    logger.info(f"[BeliefState][IMP:9][draw_graph_handler][CREATE_PLOT][ReturnData] График успешно создан с {len(points)} точками [VALUE]")
    return fig
    # END_BLOCK_CREATE_PLOT
# END_FUNCTION_draw_graph_handler

# START_FUNCTION_create_interface
# START_CONTRACT:
# PURPOSE: Создание и настройка интерфейса Gradio.
# INPUTS: Отсутствуют.
# OUTPUTS: 
# - gr.Blocks - Объект интерфейса Gradio
# SIDE_EFFECTS: Отсутствует (только создание объекта).
# KEYWORDS:[PATTERN(6): Factory; CONCEPT(8): UIComposition]
# END_CONTRACT
def create_interface():
    """Создает интерфейс Gradio."""
    
    # START_BLOCK_LOAD_INITIAL_CONFIG: [Загрузка начальной конфигурации]
    try:
        config = load_config(CONFIG_PATH)
        logger.info(f"[ConfigLoad][IMP:7][create_interface][LOAD_INITIAL_CONFIG][ReturnData] Начальная конфигурация: {config} [VALUE]")
    except Exception as e:
        logger.warning(f"[ConfigLoad][IMP:5][create_interface][LOAD_INITIAL_CONFIG][ConditionCheck] Ошибка загрузки конфигурации, используются значения по умолчанию. Err: {e} [WARN]")
        config = {'a': 1.0, 'c': 0.0, 'x_min': -10.0, 'x_max': 10.0}
    # END_BLOCK_LOAD_INITIAL_CONFIG

    # START_BLOCK_SETUP_INTERFACE: [Настройка компонентов Gradio]
    import gradio as gr
    
    with gr.Blocks(title="Lesson 6 - Парабола") as interface:
        gr.Markdown("# Lesson 6: Генератор параболы")
        gr.Markdown("Генерация точек параболы y = ax² + c и визуализация")
        
        with gr.Row():
            # Левая колонка: Управление и таблица данных
            with gr.Column(scale=1):
                gr.Markdown("## Параметры")
                
                a_slider = gr.Slider(
                    minimum=-10.0,
                    maximum=10.0,
                    step=0.1,
                    value=config['a'],
                    label="Коэффициент a"
                )
                
                c_slider = gr.Slider(
                    minimum=-10.0,
                    maximum=10.0,
                    step=0.1,
                    value=config['c'],
                    label="Коэффициент c"
                )
                
                x_min_slider = gr.Slider(
                    minimum=-50.0,
                    maximum=50.0,
                    step=1.0,
                    value=config['x_min'],
                    label="X мин"
                )
                
                x_max_slider = gr.Slider(
                    minimum=-50.0,
                    maximum=50.0,
                    step=1.0,
                    value=config['x_max'],
                    label="X макс"
                )
                
                generate_btn = gr.Button("Generate Data", variant="primary")
                draw_btn = gr.Button("Draw Graph", variant="secondary")
                
                status_output = gr.Textbox(label="Статус", interactive=False)
                
                gr.Markdown("## Таблица данных")
                dataframe_output = gr.Dataframe(label="Точки параболы")
            
            # Правая колонка: График
            with gr.Column(scale=2):
                gr.Markdown("## График")
                plot_output = gr.Plot(label="График параболы")
        
        # START_BLOCK_SETUP_EVENT_HANDLERS: [Настройка обработчиков событий]
        generate_btn.click(
            fn=generate_data_handler,
            inputs=[a_slider, c_slider, x_min_slider, x_max_slider],
            outputs=[dataframe_output, status_output]
        )
        
        draw_btn.click(
            fn=draw_graph_handler,
            inputs=[],
            outputs=[plot_output]
        )
        # END_BLOCK_SETUP_EVENT_HANDLERS
    
    logger.info(f"[BeliefState][IMP:9][create_interface][SETUP_INTERFACE][ReturnData] Интерфейс Gradio успешно создан [VALUE]")
    return interface
    # END_BLOCK_SETUP_INTERFACE
# END_FUNCTION_create_interface
