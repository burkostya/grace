# Test Guide: Lesson 22 (Parabola Visualizer)

## Входные данные для проверки
1. **Конфигурация (config.json):**
   - Файл создается в `lesson_22/`.
   - Ожидаемые ключи: `a`, `c`, `x_min`, `x_max`.
2. **База данных (points_22.db):**
   - Таблица `points` с колонками `id`, `x`, `y`.

## Верификация через SQL
Для проверки корректности сохранения данных используйте запросы:
```sql
-- Проверка количества точек (должно соответствовать диапазону и шагу 0.5)
SELECT COUNT(*) FROM points;

-- Проверка экстремума (для a=1, c=0 вершина в (0,0))
SELECT * FROM points WHERE x = 0;

-- Проверка границ
SELECT * FROM points ORDER BY x LIMIT 1;
SELECT * FROM points ORDER BY x DESC LIMIT 1;
```

## Маркеры в логах (app_22.log)
Ищите следующие записи уровня `[IMP:9-10]`:
- `[BeliefState][IMP:9][save_config]` — подтверждение сохранения настроек.
- `[BeliefState][IMP:9][calculate_parabola]` — подтверждение расчета точек.
- `[BeliefState][IMP:9][save_points]` — подтверждение записи в SQLite.
- `[System][IMP:10][create_ui]` — подтверждение успешного запуска интерфейса.

## Как запустить приложение
```bash
python run_lesson_22.py
```
После запуска откроется вкладка в браузере. Нажмите "Generate Data", затем "Draw Graph".
