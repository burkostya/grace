# FILE: app.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Основной файл приложения на Gradio для визуализации параболы.
# SCOPE: Пользовательский интерфейс (Gradio).
# KEYWORDS: [DOMAIN(9): UI; TECH(8): Gradio; TECH(7): Plotly]
# LINKS: [CALLS(9): ui_controller]
# END_MODULE_CONTRACT

import gradio as gr
import logging
from ui_controller import UIController

# Настройка логирования для приложения
logger = logging.getLogger(__name__)

# Инициализация контроллера
controller = UIController()

# START_BLOCK_UI_DEFINITION: [Описание интерфейса Gradio.]
with gr.Blocks(title="Генератор Параболы (Учебный пример)") as demo:
    gr.Markdown("""
    # 📈 Генератор Параболы
    Учебный пример для студентов: демонстрация работы с SQLite, Gradio и Pytest.
    Формула: **y = ax² + c**
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            a_input = gr.Slider(minimum=-10, maximum=10, value=1, label="Коэффициент 'a'")
            c_input = gr.Slider(minimum=-50, maximum=50, value=0, label="Смещение 'c'")
            
            btn_generate = gr.Button("1. Generate Data", variant="primary")
            btn_draw = gr.Button("2. Draw Graph", variant="secondary")
            
        with gr.Column(scale=2):
            plot_output = gr.Plot(label="График")
            table_output = gr.Dataframe(label="Данные из SQLite", interactive=False)

    # Привязка событий
    # Кнопка Generate обновляет таблицу
    btn_generate.click(
        fn=controller.handle_generate,
        inputs=[a_input, c_input],
        outputs=[table_output]
    )
    
    # Кнопка Draw обновляет график
    btn_draw.click(
        fn=controller.handle_draw,
        inputs=[],
        outputs=[plot_output]
    )

# END_BLOCK_UI_DEFINITION

if __name__ == "__main__":
    logger.info("[TraceCheck][app][Main][StepComplete] Запуск Gradio интерфейса [SUCCESS]")
    demo.launch()
