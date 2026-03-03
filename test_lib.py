# FILE: test_lib.py
# VERSION: 1.0.0
# START_MODULE_CONTRACT:
# PURPOSE: Скрипт для проверки версий установленных библиотек и окружения.
# SCOPE: Окружение, зависимости.
# KEYWORDS: [DOMAIN(9): Environment; TECH(8): Python; CONCEPT(7): VersionCheck]
# END_MODULE_CONTRACT

import sys
import platform
import pkg_resources

def check_versions():
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Executable: {sys.executable}")
    
    libs = ["pandas", "fastapi", "pydantic", "requests"]
    print("\n--- Libraries ---")
    for lib in libs:
        try:
            version = pkg_resources.get_distribution(lib).version
            print(f"{lib}=={version}")
        except pkg_resources.DistributionNotFound:
            print(f"{lib} is not installed")

if __name__ == "__main__":
    check_versions()
