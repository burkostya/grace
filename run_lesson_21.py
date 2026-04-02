# FILE:run_lesson_21.py
# VERSION:1.2.0
import sys
import os

def main():
    sys.path.append(os.getcwd())
    # Отключаем прокси, если они есть, для локальной работы
    os.environ['HTTP_PROXY'] = ''
    os.environ['HTTPS_PROXY'] = ''
    
    from lesson_21.app import app
    from lesson_21 import db_manager
    
    print("[Launcher] Initializing DB...")
    db_manager.init_db()
    
    print("[Launcher] Starting Dash Server on http://127.0.0.1:8051")
    # use_reloader=False КРИТИЧНО для предотвращения дублирования коллбеков в режиме отладки
    app.run(debug=True, port=8051, use_reloader=False)

if __name__ == "__main__":
    main()
