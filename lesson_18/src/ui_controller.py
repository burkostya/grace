# FILE: lesson_18/src/ui_controller.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Контроллер интерфейса Gradio для управления генератором параболы.
# SCOPE: Определение UI компонентов, обработка событий, визуализация Plotly.
# INPUT: Пользовательский ввод через Gradio компоненты.
# OUTPUT: Обновленные компоненты Gradio (Dataframe, Plot).
# KEYWORDS: [DOMAIN(8): UI; CONCEPT(7): Visualization; TECH(9): Gradio, Plotly]
# LINKS: [USES_API(8): gradio, plotly.graph_objects]
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание контроллера UI и обработчиков событий.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# CLASS 10[Класс для управления UI и событиями] => UIController
# END_MODULE_MAP
#
# START_USE_CASES:
# - [UIController]: User -> Adjust Sliders -> Generate Data -> View Table -> Draw Graph -> View Plot
# END_USE_CASES

import gradio as gr
import plotly.graph_objects as go
import pandas as pd
import logging
from lesson_18.src.config_manager import ConfigManager
from lesson_18.src.data_processor import DataProcessor

logger = logging.getLogger(__name__)

# START_FUNCTION_UIController
# START_CONTRACT:
# PURPOSE: Класс для создания и управления интерфейсом Gradio.
# KEYWORDS: [PATTERN(7): Controller]
# COMPLEXITY_SCORE: 7
# END_CONTRACT
class UIController:
    """
    UIController связывает ConfigManager и DataProcessor с интерфейсом Gradio.
    Он обрабатывает нажатия кнопок и обновляет визуальные компоненты.
    """

    def __init__(self):
        self.config_manager = ConfigManager()
        self.data_processor = DataProcessor()
        self.config = self.config_manager.load_config()

    # START_FUNCTION_handle_generate
    # START_CONTRACT:
    # PURPOSE: Обработка нажатия кнопки 'Generate Data'.
    # INPUTS:
    # - float => a: Коэффициент a
    # - float => c: Коэффициент c
    # - float => x_min: Минимум x
    # - float => x_max: Максимум x
    # OUTPUTS: 
    # - pd.DataFrame - Данные для таблицы
    # COMPLEXITY_SCORE: 5
    # END_CONTRACT
    def handle_generate(self, a: float, c: float, x_min: float, x_max: float) -> pd.DataFrame:
        """
        Сохраняет параметры в конфиг, генерирует точки и сохраняет их в БД.
        """
        # START_BLOCK_GENERATE_FLOW: [Поток генерации данных]
        new_config = {"a": a, "c": c, "x_min": x_min, "x_max": x_max}
        self.config_manager.save_config(new_config)
        
        df = self.data_processor.generate_points(a, c, x_min, x_max)
        self.data_processor.save_to_db(df)
        
        logger.info(f"[UI][IMP:9][UIController][handle_generate][Flow] Данные сгенерированы и сохранены. [SUCCESS]")
        return df
        # END_BLOCK_GENERATE_FLOW

    # START_FUNCTION_handle_draw
    # START_CONTRACT:
    # PURPOSE: Обработка нажатия кнопки 'Draw Graph'.
    # INPUTS: Нет
    # OUTPUTS: 
    # - go.Figure - Объект графика Plotly
    # COMPLEXITY_SCORE: 5
    # END_CONTRACT
    def handle_draw(self) -> go.Figure:
        """
        Загружает данные из БД и строит график Plotly.
        """
        # START_BLOCK_DRAW_FLOW: [Поток отрисовки графика]
        df = self.data_processor.load_from_db()
        
        if df.empty:
            logger.warning(f"[UI][IMP:8][UIController][handle_draw][Condition] БД пуста. Нечего рисовать. [WARN]")
            fig = go.Figure()
            fig.add_annotation(text="No data in DB. Click 'Generate Data' first.", showarrow=False)
            return fig

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['x'], y=df['y'], mode='lines+markers', name='Parabola'))
        fig.update_layout(title="Parabola Visualization (y = ax^2 + c)", xaxis_title="X", yaxis_title="Y")
        
        logger.info(f"[BeliefState][IMP:9][UIController][handle_draw][Flow] График построен для {len(df)} точек. [VALUE]")
        return fig
        # END_BLOCK_DRAW_FLOW

    # START_FUNCTION_create_ui
    # START_CONTRACT:
    # PURPOSE: Определение структуры интерфейса Gradio.
    # INPUTS: Нет
    # OUTPUTS: 
    # - gr.Blocks - Объект интерфейса
    # COMPLEXITY_SCORE: 8
    # END_CONTRACT
    def create_ui(self) -> gr.Blocks:
        """
        Создает двухколоночный интерфейс Gradio.
        """
        # START_BLOCK_UI_LAYOUT: [Компоновка интерфейса]
        with gr.Blocks(title="Lesson 18: Parabola Generator") as ui:
            gr.Markdown("# Parabola Generator (y = ax^2 + c)")
            
            with gr.Row():
                # Левая колонка: Управление и Таблица
                with gr.Column(scale=1):
                    gr.Markdown("### Parameters")
                    a_slider = gr.Slider(minimum=-10, maximum=10, value=self.config["a"], label="Coefficient a")
                    c_slider = gr.Slider(minimum=-50, maximum=50, value=self.config["c"], label="Coefficient c")
                    x_min_slider = gr.Slider(minimum=-100, maximum=0, value=self.config["x_min"], label="X Min")
                    x_max_slider = gr.Slider(minimum=0, maximum=100, value=self.config["x_max"], label="X Max")
                    
                    with gr.Row():
                        gen_btn = gr.Button("Generate Data", variant="primary")
                        draw_btn = gr.Button("Draw Graph")
                    
                    gr.Markdown("### Data Table")
                    data_table = gr.Dataframe(headers=["x", "y"], label="Generated Points")
                
                # Правая колонка: График
                with gr.Column(scale=1):
                    gr.Markdown("### Visualization")
                    plot_output = gr.Plot(label="Parabola Graph")

            # START_BLOCK_UI_EVENTS: [Привязка событий]
            gen_btn.click(
                fn=self.handle_generate,
                inputs=[a_slider, c_slider, x_min_slider, x_max_slider],
                outputs=data_table
            )
            
            draw_btn.click(
                fn=self.handle_draw,
                inputs=[],
                outputs=plot_output
            )
            # END_BLOCK_UI_EVENTS
            
            logger.info(f"[UI][IMP:7][UIController][create_ui][Flow] Интерфейс Gradio инициализирован. [SUCCESS]")
            return ui
        # END_BLOCK_UI_LAYOUT
# END_FUNCTION_UIController
