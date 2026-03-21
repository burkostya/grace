# FILE:lesson_13/src/ui_controller.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Контроллер пользовательского интерфейса для управления логикой Gradio.
# SCOPE: Обработка событий UI, взаимодействие с бизнес-логикой и БД.
# INPUT: Данные из компонентов Gradio (слайдеры, текстовые поля).
# OUTPUT: Данные для компонентов Gradio (DataFrame, Plotly Figure).
# KEYWORDS:[DOMAIN(UI): Gradio; CONCEPT(MVC): Controller; TECH(Plot): Plotly]
# LINKS:[USES_API(Logic): parabola_logic; USES_API(DB): database_manager]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Создание контроллера с обработчиками генерации данных и отрисовки графика.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# CLASS[10][Контроллер UI для Lesson 13] => UIController
# METHOD[9][Генерация данных и сохранение в БД] => handle_generate_data
# METHOD[8][Получение данных из БД и построение графика] => handle_draw_graph
# END_MODULE_MAP

import logging
import pandas as pd
import plotly.graph_objects as go
from .parabola_logic import calculate_parabola_points
from .database_manager import DatabaseManager
from .config_manager import ConfigManager

# Настройка логирования LDD 2.0
logger = logging.getLogger("lesson_13")
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    fh = logging.FileHandler("lesson_13/app_13.log", encoding="utf-8")
    formatter = logging.Formatter('[%(levelname)s]%(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

# START_BLOCK_UI_CONTROLLER_CLASS: [Определение класса UIController]
class UIController:
    """
    Класс UIController инкапсулирует логику обработки пользовательских действий в интерфейсе Gradio.
    Он координирует работу между менеджером конфигурации, логикой вычислений и менеджером базы данных,
    обеспечивая разделение ответственности между представлением и бизнес-логикой.
    """

    def __init__(self, db_path: str = "lesson_13/parabola.db", config_path: str = "lesson_13/config.json"):
        self.db_manager = DatabaseManager(db_path)
        self.db_manager.init_db()
        self.config_manager = ConfigManager(config_path)
        logger.info(f"[UI][IMP:7][UIController][__init__][Init] Контроллер инициализирован. DB: {db_path} [SUCCESS]")

    # START_FUNCTION_handle_generate_data
    # START_CONTRACT:
    # PURPOSE: Обработка нажатия кнопки "Generate Data".
    # INPUTS: 
    # - float => a: Коэффициент A
    # - float => b: Коэффициент B
    # - float => c: Коэффициент C
    # - float => x_start: Начало диапазона
    # - float => x_end: Конец диапазона
    # - int => num_points: Количество точек
    # OUTPUTS: 
    # - pd.DataFrame - Таблица с рассчитанными точками
    # SIDE_EFFECTS: Обновляет config.json и сохраняет точки в parabola.db
    # KEYWORDS:[PATTERN(Action): Handler; CONCEPT(Data): Calculation]
    # COMPLEXITY_SCORE: 6
    # END_CONTRACT
    def handle_generate_data(self, a, b, c, x_start, x_end, num_points):
        """
        Метод выполняет полный цикл генерации данных: сохранение параметров в конфиг,
        расчет точек параболы и их сохранение в базу данных. Возвращает DataFrame для отображения в UI.
        """
        logger.info(f"[UI][IMP:9][UIController][handle_generate_data][Start] Генерация данных для a={a}, b={b}, c={c} [START]")
        
        # START_BLOCK_SAVE_CONFIG: [Сохранение параметров в конфиг]
        try:
            self.config_manager.save_config({
                "a": a,
                "b": b,
                "c": c,
                "x_start": x_start,
                "x_end": x_end,
                "num_points": num_points
            })
            logger.debug(f"[UI][IMP:5][UIController][handle_generate_data][SAVE_CONFIG] Параметры сохранены в конфиг [SUCCESS]")
        except Exception as e:
            logger.error(f"[UI][IMP:10][UIController][handle_generate_data][SAVE_CONFIG] Ошибка сохранения конфига: {e} [FAIL]")
        # END_BLOCK_SAVE_CONFIG

        # START_BLOCK_CALCULATE: [Расчет точек]
        points = calculate_parabola_points(a, b, c, x_start, x_end, num_points)
        df = pd.DataFrame(points, columns=['x', 'y'])
        logger.debug(f"[UI][IMP:4][UIController][handle_generate_data][CALCULATE] Рассчитано {len(df)} точек [INFO]")
        # END_BLOCK_CALCULATE

        # START_BLOCK_DB_SAVE: [Сохранение в БД]
        try:
            self.db_manager.save_points(points)
            logger.info(f"[UI][IMP:8][UIController][handle_generate_data][DB_SAVE] Точки успешно сохранены в БД [SUCCESS]")
        except Exception as e:
            logger.error(f"[UI][IMP:10][UIController][handle_generate_data][DB_SAVE] Ошибка сохранения в БД: {e} [FAIL]")
        # END_BLOCK_DB_SAVE

        return df
    # END_FUNCTION_handle_generate_data

    # START_FUNCTION_handle_draw_graph
    # START_CONTRACT:
    # PURPOSE: Обработка нажатия кнопки "Draw Graph".
    # INPUTS: Нет
    # OUTPUTS: 
    # - go.Figure - Объект графика Plotly
    # SIDE_EFFECTS: Читает данные из parabola.db
    # KEYWORDS:[PATTERN(Action): Handler; CONCEPT(Viz): Plotly]
    # COMPLEXITY_SCORE: 5
    # END_CONTRACT
    def handle_draw_graph(self):
        """
        Метод извлекает последние сохраненные точки из базы данных и строит на их основе
        интерактивный график Plotly.
        """
        logger.info(f"[UI][IMP:9][UIController][handle_draw_graph][Start] Запрос на отрисовку графика [START]")
        
        # START_BLOCK_DB_READ: [Чтение из БД]
        points = self.db_manager.get_points()
        if not points:
            logger.warning(f"[UI][IMP:8][UIController][handle_draw_graph][DB_READ] Данные в БД отсутствуют [EMPTY]")
            fig = go.Figure()
            fig.add_annotation(text="No data in database. Generate data first.", showarrow=False)
            return fig
        # END_BLOCK_DB_READ

        # START_BLOCK_CREATE_PLOT: [Создание графика]
        df = pd.DataFrame(points, columns=['x', 'y'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['x'], y=df['y'], mode='lines+markers', name='Parabola'))
        fig.update_layout(title="Parabola Graph", xaxis_title="X", yaxis_title="Y")
        logger.info(f"[UI][IMP:8][UIController][handle_draw_graph][CREATE_PLOT] График успешно создан [SUCCESS]")
        # END_BLOCK_CREATE_PLOT

        return fig
    # END_FUNCTION_handle_draw_graph

# END_BLOCK_UI_CONTROLLER_CLASS
