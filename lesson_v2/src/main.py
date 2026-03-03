# FILE: lesson_v2/src/main.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Точка входа в приложение Parabola Pro на Gradio.
# KEYWORDS: [TECH(9): Gradio; DOMAIN(8): UI]
# END_MODULE_CONTRACT

import gradio as gr
import logging
from .ui_controller import UIControllerPro

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("lesson_v2/app_pro.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def launch_app():
    controller = UIControllerPro()
    
    with gr.Blocks(title="Parabola Pro (KiloCode Lesson)") as demo:
        gr.Markdown("# 📈 Parabola Pro Generator")
        gr.Markdown("Учебный пример v2: Полный цикл разработки с настройкой диапазона.")
        
        with gr.Row():
            with gr.Column():
                a_input = gr.Number(label="Коэффициент a", value=1.0)
                c_input = gr.Number(label="Смещение c", value=0.0)
                xmin_input = gr.Number(label="X min", value=-10.0)
                xmax_input = gr.Number(label="X max", value=10.0)
                
                btn_generate = gr.Button("🚀 Generate Data", variant="primary")
                btn_draw = gr.Button("🎨 Draw Graph")
            
            with gr.Column():
                table_output = gr.Dataframe(label="Generated Points")
                plot_output = gr.Plot(label="Visualization")
        
        # Привязка событий
        btn_generate.click(
            fn=controller.handle_generate,
            inputs=[a_input, c_input, xmin_input, xmax_input],
            outputs=table_output
        )
        
        btn_draw.click(
            fn=controller.handle_draw,
            inputs=[],
            outputs=plot_output
        )

    return demo

if __name__ == "__main__":
    demo = launch_app()
    demo.launch()
