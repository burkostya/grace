# FILE: ui_controller.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Контроллер для связи Gradio UI с бэкендом (DataGenerator).
# SCOPE: Обработка событий UI, преобразование данных для отображения.
# INPUT: Параметры из Gradio (a, c).
# OUTPUT: Pandas DataFrame для таблиц, Plotly Figure для графиков.
# KEYWORDS: [DOMAIN(9): UI_Logic; TECH(8): Pandas; TECH(7): Plotly; CONCEPT(6): Controller]
# LINKS: [USES_API(8): pandas; USES_API(7): plotly; CALLS(9): datagenerator]
# END_MODULE_CONTRACT
# START_MODULE_MAP:
# CLASS 9 [Управляет логикой взаимодействия UI и данных] => UIController
# METHOD 8 [Инициализирует контроллер и бэкенд] => __init__
# METHOD 9 [Обрабатывает генерацию и возвращает DataFrame] => handle_generate
# METHOD 9 [Создает график на основе данных из БД] => handle_draw
# END_MODULE_MAP

import pandas as pd
import plotly.express as px
import logging
from Archive.datagenerator import DataGenerator

logger = logging.getLogger(__name__)

# START_CLASS_UIController
# START_CONTRACT:
# PURPOSE: Класс-контроллер для изоляции логики UI от бэкенда.
# ATTRIBUTES:
# - [Экземпляр генератора данных] => generator: DataGenerator
# KEYWORDS: [PATTERN(8): Controller; TECH(7): Gradio_Integration]
# END_CONTRACT
class UIController:
    """Контроллер для управления данными в интерфейсе."""

    # START_METHOD___init__
    # START_CONTRACT:
    # PURPOSE: Инициализация контроллера.
    # END_CONTRACT
    def __init__(self, db_path: str = "parabola.db"):
        self.generator = DataGenerator(db_path)
        logger.info(f"[TraceCheck][UIController][INIT][StepComplete] Контроллер инициализирован с БД: {db_path} [SUCCESS]")
    # END_METHOD___init__

    # START_METHOD_handle_generate
    # START_CONTRACT:
    # PURPOSE: Вызывает генерацию данных и возвращает их в формате DataFrame.
    # INPUTS:
    # - [Коэффициент a] => a: float
    # - [Смещение c] => c: float
    # OUTPUTS:
    # - [Pandas DataFrame с точками] => pd.DataFrame
    # KEYWORDS: [CONCEPT(7): DataConversion]
    # END_CONTRACT
    def handle_generate(self, a: float, c: float):
        """Обработчик кнопки Generate."""
        # START_BLOCK_GENERATE_AND_FETCH: [Вызов бэкенда и получение данных.]
        logger.debug(f"[SelfCheck][UIController][handle_generate][CallExternal] Запуск генерации: a={a}, c={c} [ATTEMPT]")
        self.generator.generate_points(a, c)
        data = self.generator.get_all_points()
        
        df = pd.DataFrame(data, columns=['x', 'y'])
        logger.debug(f"[VarCheck][UIController][handle_generate][ReturnData] Сформирован DataFrame: {df.shape} [VALUE]")
        return df
        # END_BLOCK_GENERATE_AND_FETCH
    # END_METHOD_handle_generate

    # START_METHOD_handle_draw
    # START_CONTRACT:
    # PURPOSE: Создает объект графика Plotly на основе текущих данных в БД.
    # OUTPUTS:
    # - [Объект фигуры Plotly] => plotly.graph_objects.Figure
    # KEYWORDS: [TECH(8): Plotly; CONCEPT(7): Visualization]
    # END_CONTRACT
    def handle_draw(self):
        """Обработчик кнопки Draw."""
        # START_BLOCK_CREATE_PLOT: [Чтение данных и отрисовка.]
        logger.debug(f"[SelfCheck][UIController][handle_draw][CallExternal] Подготовка графика [ATTEMPT]")
        data = self.generator.get_all_points()
        if not data:
            logger.warning(f"[VarCheck][UIController][handle_draw][ConditionCheck] Данные отсутствуют [FAIL]")
            return None
            
        df = pd.DataFrame(data, columns=['x', 'y'])
        fig = px.line(df, x='x', y='y', title=f"График параболы")
        fig.update_traces(mode='lines+markers')
        
        logger.info(f"[TraceCheck][UIController][handle_draw][StepComplete] График успешно создан [SUCCESS]")
        return fig
        # END_BLOCK_CREATE_PLOT
    # END_METHOD_handle_draw

# END_CLASS_UIController
