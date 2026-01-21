# Deribit Price API

Сервис для автоматического сбора индексных цен с биржи Deribit и предоставления доступа к ним через REST API.

## Архитектурные решения (Design Decisions)

При разработке были приняты следующие ключевые решения:

* **Centralized Configuration**: Все настройки (БД, Redis, список тикеров) инкапсулированы в класс `Settings`. Это исключает использование глобальных переменных и делает код соответствующим принципам *12-Factor App*.
* **Decoupling (Слабая связанность)**: Логика конфигурации (`config.py`), подключения к БД (`db.py`) и бизнес-задачи (`tasks.py`) разделены. Это позволяет менять способ хранения настроек или логику коннекта, не затрагивая функционал задач.
* **Resilience (Отказоустойчивость)**: Реализован механизм повторных попыток подключения к PostgreSQL (`retries`), что необходимо при холодном старте всей инфраструктуры через Docker Compose.
* **Raw SQL over ORM**: Для простых операций записи и выборки цен использован чистый SQL. Это минимизирует накладные расходы и демонстрирует навык владения базовыми инструментами работы с БД.
* **Separation of Concerns**: Выделен слой `services` с универсальным исполнителем запросов, что изолирует FastAPI от деталей реализации БД.

## Компоненты

### Основные модули

* `app/config.py`: Централизованная конфигурация через класс `Settings`.
* `app/api.py`: FastAPI приложение с REST эндпоинтами.
* `app/services.py`: Слой бизнес-логики и выполнения запросов.
* `app/db.py`: Логика создания соединений с БД (механизм retries).
* `app/tasks.py`: Фоновые задачи Celery для мониторинга цен.
* `app/celery_app.py`: Настройка планировщика Celery Beat.
* `app/derbit.py`: Клиент для взаимодействия с API Deribit.

## Быстрый старт с Docker

```bash
# Создайте .env на основе примера
cp .env.example .env

# Запуск всей инфраструктуры
docker-compose up -d --build

```

## Переменные окружения

Файл `.env` поддерживает следующие настройки:

```bash
# Список тикеров для мониторинга (через запятую)
TICKERS=btc_usd,eth_usd

# Параметры PostgreSQL
POSTGRES_DB=deribit
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Redis / Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

TICKERS="btc_usd, eth_usd"

```

## API Эндпоинты

Интерактивная документация доступна по адресу: [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)

### Примеры запросов:

* **Все данные**: `GET /prices?ticker=btc_usd`
* **Последняя цена**: `GET /prices/latest?ticker=btc_usd`
* **Фильтр по дате**: `GET /prices/by-date?ticker=btc_usd&from_ts=1735689600000000&to_ts=1767225599000000`

## Тестирование API (cURL)

После запуска контейнеров вы можете проверить работоспособность эндпоинтов с помощью следующих команд:

```bash
# Получение всех данных по тикерам
curl "http://localhost:8000/prices?ticker=btc_usd"
curl "http://localhost:8000/prices?ticker=eth_usd"

# Получение последней цены
curl "http://localhost:8000/prices/latest?ticker=btc_usd"
curl "http://localhost:8000/prices/latest?ticker=eth_usd"

# Фильтрация по дате (пример для 2026 года)
curl "http://localhost:8000/prices/by-date?ticker=btc_usd&from_ts=1767225600000000&to_ts=1798761599000000"
curl "http://localhost:8000/prices/by-date?ticker=eth_usd&from_ts=1767225600000000&to_ts=1798761599000000"

```

> **Важно:** Параметры `from_ts` и `to_ts` передаются в микросекундах (16 знаков). В примерах выше указан диапазон на весь 2026 год.
