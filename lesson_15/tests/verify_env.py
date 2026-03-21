# FILE: lesson_15/tests/verify_env.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Проверка наличия библиотек, необходимых для Lesson_15.
# SCOPE: Окружение, зависимости (Gradio, Plotly, Pandas, Pytest).
# END_MODULE_CONTRACT

import pkg_resources
import sys

def check_env():
    required = ["pandas", "gradio", "plotly", "pytest"]
    print(f"Python: {sys.version}")
    print("\n--- Required Libraries ---")
    for lib in required:
        try:
            version = pkg_resources.get_distribution(lib).version
            print(f"{lib}=={version} [OK]")
        except pkg_resources.DistributionNotFound:
            print(f"{lib} [MISSING]")

if __name__ == "__main__":
    check_env()
