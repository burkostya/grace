# FILE: lesson_22/ui.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Графический интерфейс на Gradio для управления параметрами и визуализации параболы.
# SCOPE: Создание компонентов UI, обработка событий и интеграция с бэкендом.
# INPUT: Пользовательские коэффициенты и команды.
# OUTPUT: Обновленная таблица данных и график Plotly.
# KEYWORDS:[DOMAIN(8): Frontend; CONCEPT(7): UI_Controller; TECH(9): Gradio, Plotly]
# LINKS:[USES_API(8): gradio, plotly, pandas]
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Почему используется двухколоночная структура?
# A: Улучшенная эргономика: разделение ввода/таблицы (слева) и визуального результата (справа).
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Первичное создание модуля ui.]
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC 10[Обрабатывает генерацию данных: сохраняет конфиг, считает и пишет в БД] => handle_generate
# FUNC 10[Обрабатывает отрисовку графика: читает из БД и возвращает Plotly Figure] => handle_draw
# FUNC 10[Конструирует интерфейс Gradio] => create_ui
# END_MODULE_MAP

import gradio as gr
import pandas as pd
import plotly.express as px
import logging
from lesson_22.config_manager import load_config, save_config
from lesson_22.db_manager import init_db, save_points, get_points
from lesson_22.calculator import calculate_parabola

logger = logging.getLogger(__name__)


# START_FUNCTION_handle_generate
# START_CONTRACT:
# PURPOSE: Сохраняет конфиг, генерирует точки и возвращает DataFrame для таблицы.
# INPUTS:
# - float => a, c, x_min, x_max: Параметры параболы.
# - str => db_path, config_path: Опциональные пути для тестов.
# OUTPUTS:
# - pd.DataFrame - Таблица с данными.
# SIDE_EFFECTS: Изменение config.json и points_22.db.
# KEYWORDS:[PATTERN(6): EventController; CONCEPT(8): DataGeneration]
# COMPLEXITY_SCORE: 6
# END_CONTRACT
def handle_generate(
    a,
    c,
    x_min,
    x_max,
    db_path: str = "lesson_22/points_22.db",
    config_path: str = "lesson_22/config.json",
) -> pd.DataFrame:
    """
    Контроллер кнопки 'Generate Data'. Он последовательно:
    1. Сохраняет параметры в JSON.
    2. Рассчитывает точки.
    3. Сохраняет их в SQLite.
    4. Считывает обратно для отображения в UI.
    """
    # START_BLOCK_PROCESS_GENERATE: [Оркестрация генерации данных]
    logger.info(
        f"[UI][IMP:8][handle_generate][PROCESS_GENERATE][Start] Инициация генерации данных: a={a}, c={c} [INFO]"
    )

    # 1. Сохранение конфигурации
    save_config(a, c, x_min, x_max, config_path=config_path)

    # 2. Расчет
    points = calculate_parabola(a, c, x_min, x_max)

    # 3. Сохранение в БД
    save_points(points, db_path=db_path)

    # 4. Чтение для таблицы
    db_data = get_points(db_path=db_path)
    # BUG_FIX_CONTEXT: Используем явную установку колонок для корректной типизации
    df = pd.DataFrame(db_data)
    if not df.empty:
        df.columns = ["x", "y"]

    logger.info(
        f"[BeliefState][IMP:9][handle_generate][PROCESS_GENERATE][Success] Данные сгенерированы и возвращены в UI. [SUCCESS]"
    )
    return df
    # END_BLOCK_PROCESS_GENERATE


# END_FUNCTION_handle_generate


# START_FUNCTION_handle_draw
# START_CONTRACT:
# PURPOSE: Считывает данные из БД и возвращает график Plotly.
# INPUTS:
# - str => db_path: Опциональный путь для тестов.
# OUTPUTS:
# - plotly.graph_objects.Figure - График параболы.
# SIDE_EFFECTS: Чтение из БД.
# KEYWORDS:[PATTERN(6): VisualController; CONCEPT(8): Rendering]
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def handle_draw(db_path: str = "lesson_22/points_22.db"):
    """
    Контроллер кнопки 'Draw Graph'. Извлекает данные из SQLite и строит
    интерактивный график.
    """
    # START_BLOCK_RENDER_PLOT: [Построение графика]
    logger.info(
        f"[UI][IMP:8][handle_draw][RENDER_PLOT][Start] Запрос на отрисовку графика. [INFO]"
    )

    data = get_points(db_path=db_path)
    if not data:
        logger.warning(
            f"[LogicError][IMP:7][handle_draw][RENDER_PLOT][NoData] БД пуста. Нечего рисовать. [WARN]"
        )
        return px.scatter(title="Нет данных. Нажмите 'Generate Data'")

    df = pd.DataFrame(data)
    if not df.empty:
        df.columns = ["x", "y"]
    fig = px.line(df, x="x", y="y", title="Парабола y = ax² + c", markers=True)
    fig.update_layout(template="plotly_dark")

    logger.info(
        f"[BeliefState][IMP:9][handle_draw][RENDER_PLOT][Success] График отрисован. [SUCCESS]"
    )
    return fig
    # END_BLOCK_RENDER_PLOT


# END_FUNCTION_handle_draw


# START_FUNCTION_create_ui
# START_CONTRACT:
# PURPOSE: Создает и настраивает компоненты интерфейса Gradio.
# INPUTS: Нет.
# OUTPUTS:
# - gr.Blocks - Объект интерфейса.
# SIDE_EFFECTS: Инициализация БД при запуске.
# KEYWORDS:[PATTERN(6): UIFactory; CONCEPT(8): InterfaceSetup]
# COMPLEXITY_SCORE: 7
# END_CONTRACT
def create_ui() -> gr.Blocks:
    """
    Основная функция сборки интерфейса. Определяет стили, колонки и привязки кнопок.
    """
    # START_BLOCK_SETUP_UI: [Сборка Gradio Blocks]
    init_db()  # Гарантируем наличие БД
    config = load_config()

    with gr.Blocks(title="Lesson 22: Parabola Visualizer") as ui:
        gr.Markdown("# Parabola Visualizer (Lesson 22)")
        gr.Markdown("Генерация точек y = ax² + c и визуализация через SQLite и Plotly.")

        with gr.Row():
            # Левая колонка
            with gr.Column(scale=1):
                gr.Markdown("### Настройки")
                a_input = gr.Slider(
                    minimum=-10,
                    maximum=10,
                    step=0.1,
                    value=config["a"],
                    label="Коэффициент a",
                )
                c_input = gr.Slider(
                    minimum=-50,
                    maximum=50,
                    step=1,
                    value=config["c"],
                    label="Коэффициент c",
                )
                x_min_input = gr.Slider(
                    minimum=-100,
                    maximum=0,
                    step=1,
                    value=config["x_min"],
                    label="x_min",
                )
                x_max_input = gr.Slider(
                    minimum=0, maximum=100, step=1, value=config["x_max"], label="x_max"
                )

                with gr.Row():
                    btn_gen = gr.Button("Generate Data", variant="primary")
                    btn_draw = gr.Button("Draw Graph", variant="secondary")

                table_output = gr.Dataframe(
                    label="Точки в БД", headers=["x", "y"], interactive=False
                )

            # Правая колонка
            with gr.Column(scale=2):
                plot_output = gr.Plot(label="Интерактивный график")

        # Привязка событий
        btn_gen.click(
            fn=handle_generate,
            inputs=[a_input, c_input, x_min_input, x_max_input],
            outputs=table_output,
        )

        btn_draw.click(fn=handle_draw, inputs=[], outputs=plot_output)

    logger.info(
        f"[System][IMP:10][create_ui][SETUP_UI][Complete] Интерфейс Gradio успешно собран. [SUCCESS]"
    )
    return ui
    # END_BLOCK_SETUP_UI


# END_FUNCTION_create_ui
