# FILE: test_lib.py
# VERSION: 1.1.0
# START_MODULE_CONTRACT:
# PURPOSE: Скрипт для проверки версий установленных библиотек и окружения.
# SCOPE: Окружение, зависимости.
# KEYWORDS: [DOMAIN(9): Environment; TECH(8): Python; CONCEPT(7): VersionCheck]
# END_MODULE_CONTRACT

import sys
import platform
import importlib.metadata

def check_versions():
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Executable: {sys.executable}")
    
    libs = ["dash", "dash_bootstrap_components", "dash_ag_grid", "pandas"]
    print("\n--- Libraries ---")
    for lib in libs:
        try:
            version = importlib.metadata.version(lib)
            print(f"{lib}=={version}")
        except importlib.metadata.PackageNotFoundError:
            print(f"{lib} is not installed")

if __name__ == "__main__":
    check_versions()
