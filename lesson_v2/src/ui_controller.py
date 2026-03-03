# FILE: lesson_v2/src/ui_controller.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Контроллер для связи UI (Gradio) и Backend (DataGeneratorPro).
# SCOPE: Контроллер, логика интерфейса.
# KEYWORDS: [DOMAIN(9): Controller; TECH(8): Plotly; CONCEPT(7): Decoupling]
# END_MODULE_CONTRACT
# START_MODULE_MAP:
# CLASS 9 [Управляет логикой UI] => UIControllerPro
# METHOD 8 [Обработка генерации] => handle_generate
# METHOD 8 [Обработка отрисовки] => handle_draw
# END_MODULE_MAP

import plotly.graph_objects as go
import logging
from .data_generator import DataGeneratorPro

logger = logging.getLogger(__name__)

# START_CLASS_UIControllerPro
class UIControllerPro:
    """Контроллер для управления данными в интерфейсе."""

    def __init__(self):
        self.generator = DataGeneratorPro()

    # START_METHOD_handle_generate
    def handle_generate(self, a: float, c: float, x_min: float, x_max: float):
        # START_BLOCK_CALL_BACKEND: [Вызов генератора.]
        logger.debug(f"[SelfCheck][UIControllerPro][handle_generate][CallExternal] Запуск генерации: a={a}, c={c}, range=[{x_min}, {x_max}] [ATTEMPT]")
        self.generator.generate_points(a, c, x_min, x_max)
        df = self.generator.get_all_points()
        logger.info(f"[TraceCheck][UIControllerPro][handle_generate][StepComplete] Данные получены [SUCCESS]")
        return df
        # END_BLOCK_CALL_BACKEND

    # START_METHOD_handle_draw
    def handle_draw(self):
        # START_BLOCK_CREATE_PLOT: [Создание графика Plotly.]
        df = self.generator.get_all_points()
        if df.empty:
            logger.warning(f"[VarCheck][UIControllerPro][handle_draw][ConditionCheck] Данные пусты [FAIL]")
            return go.Figure()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['x'], y=df['y'], mode='lines+markers', name='Parabola'))
        fig.update_layout(title="Parabola Pro Visualization", xaxis_title="X", yaxis_title="Y")
        
        logger.info(f"[TraceCheck][UIControllerPro][handle_draw][StepComplete] График построен [SUCCESS]")
        return fig
        # END_BLOCK_CREATE_PLOT
# END_CLASS_UIControllerPro
