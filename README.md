# Deribit Price API

Сервис для периодического сбора и предоставления цен с биржи Deribit.

## Архитектура

- **FastAPI**: Веб-API фреймворк для REST эндпоинтов
- **PostgreSQL**: Основная база данных для хранения цен
- **Celery + Redis**: Система очередей задач для периодического получения цен
- **Docker**: Контейнеризация всех сервисов

## Компоненты

### Основные модули
- `app/api.py`: FastAPI приложение с тремя эндпоинтами
- `app/services.py`: Бизнес-логика с универсальной функцией `execute_query`
- `app/db.py`: Управление подключением к БД с механизмом повторных попыток
- `app/celery_app.py`: Конфигурация Celery с расписанием задач
- `app/tasks.py`: Celery задача для получения и сохранения цен
- `app/derbit.py`: Интеграция с API Deribit с таймаутами

### База данных
Таблица `index_prices` содержит:
- `ticker` (string): Торговая пара (например, "btc_usd", "eth_usd")
- `price` (float): Индексная цена с Deribit
- `timestamp_ms` (bigint): Временная метка в миллисекундах

## Быстрый старт с Docker

### Запуск всех сервисов
```bash
docker-compose up -d
```

### Просмотр логов
```bash
docker-compose logs -f
```

### Остановка сервисов
```bash
docker-compose down
```

## Ручная установка

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Запуск сервисов
```bash
# Запуск Celery worker
celery -A app.celery_app worker --loglevel=info

# Запуск Celery beat (планировщик)
celery -A app.celery_app beat --loglevel=info

# Запуск FastAPI сервера
uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
```

### Переменные окружения
Создайте файл `.env` на основе `.env.example`:
```bash
# APP
ENV=local

# POSTGRES
POSTGRES_DB=deribit
POSTGRES_USER=user
POSTGRES_PASSWORD=your_password_here
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# REDIS / CELERY
REDIS_HOST=redis
REDIS_PORT=6379

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

## API Эндпоинты

> **Интерактивная документация (Swagger UI):** Доступна по адресу: [http://localhost:8000/docs](http://localhost:8000/docs) после запуска приложения.

Все эндпоинты требуют параметр `ticker` (например, `ticker=btc_usd`):

### Получить все исторические цены
```bash
GET /prices?ticker=btc_usd
```

### Получить последнюю цену
```bash
GET /prices/latest?ticker=eth_usd
```

### Получить цены в диапазоне дат
```bash
GET /prices/by-date?ticker=btc_usd&from_ts=1700000000000&to_ts=1701000000000
```
Параметры `from_ts` и `to_ts` в миллисекундах.

## Тестирование

### Запуск тестов
```bash
pytest
```

### Тестирование API
После запуска сервисов:
```bash
curl "http://localhost:8000/prices?ticker=btc_usd"
curl "http://localhost:8000/prices?ticker=eth_usd"
curl "http://localhost:8000/prices/latest?ticker=eth_usd"
curl "http://localhost:8000/prices/latest?ticker=btc_usd"
curl "http://localhost:8000/prices/by-date?ticker=btc_usd&from_ts=1735689600000&to_ts=1767225599000"
curl "http://localhost:8000/prices/by-date?ticker=eth_usd&from_ts=1735689600000&to_ts=1767225599000"
```
Примечание по формату времени: Параметры from_ts и to_ts передаются как Unix Timestamp в миллисекундах (13 знаков).

- 1735689600000 — соответствует 01.01.2026 00:00:00 UTC
- 1767225599000 — соответствует 31.12.2026 23:59:59 UTC

## Архитектурные решения

1. **PostgreSQL**: Выбрана как надежная реляционная БД для хранения цен
2. **Celery + Redis**: Используется для периодического получения данных с отдельными процессами worker и beat
3. **Без ORM**: Используется чистый SQL для простоты и явного контроля запросов
4. **Милисекундные временные метки**: Позволяют точную фильтрацию по времени
5. **Слой services**: Изолирует бизнес-логику от API эндпоинтов
6. **Повторные попытки подключения**: База данных включает логику повторных попыток для запуска контейнеров
7. **Контекстные менеджеры**: Все подключения к БД используют `with` для гарантированного закрытия

## Docker сервисы

- **postgres**: PostgreSQL 17 с автоматической инициализацией БД
- **redis**: Redis 7 для брокера Celery
- **worker**: Celery worker для выполнения задач
- **beat**: Celery beat для планирования периодических задач
- **api**: FastAPI приложение на порту 8000

## Примечания

- Worker и Beat запускаются как отдельные процессы (не используется флаг `-B`)
- Инициализация БД выполняется через `init.sql` в docker-compose
- Зависимости сервисов: API зависит от PostgreSQL и Redis
- Данные о ценах получаются с API Deribit каждую минуту (настраивается в `celery_app.py`)
- Все HTTP запросы к внешним API имеют таймаут 10 секунд