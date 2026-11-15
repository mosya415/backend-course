# Сервис модерации объявлений

## Запуск

Нужен Python 3.12 или новее.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
fastapi dev
```

## ДЗ 1. HTTP API

`POST /predict` принимает JSON с обязательными полями `seller_id`, `is_verified_seller`, `item_id`, `name`, `description`, `category`, `images_qty`. Пример:

```json
{"seller_id": 13, "is_verified_seller": false, "item_id": 42, "name": "Стол", "description": "Деревянный стол", "category": 2, "images_qty": 0}
```

При успехе тело ответа — JSON-значение `true`, если обнаружено нарушение, или `false` в остальных случаях. Нарушение фиксируется, когда продавец не подтверждён и у объявления нет изображений. Ошибки разбора и валидации запроса дают HTTP 400, внутренние ошибки сервиса — HTTP 500.

HTTP-слой находится в `routers/`, правило модерации — в `services/`, доступ к данным объявления из текущего запроса — в `repositories/`.

```bash
python -m pytest -v tests
```

## ДЗ 2. Asyncio и потоки

Решения основной части и двух бонусов лежат в `hw2/`. Условия, тесты и
заготовки взяты из [репозитория курса](https://github.com/dalegorov-study/auth/tree/b018e93d14e58a3021cc097aacdca7dab31958f5/homework).

Тесты каждой задачи запускаются из её папки.

```bash
python -m pip install -r hw2/requirements.txt
for task in hw2/0*/; do
    (cd "$task" && python -m pytest -v) || break
done
```
