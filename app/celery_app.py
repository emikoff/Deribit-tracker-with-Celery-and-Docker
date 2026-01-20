"""
Конфигурация Celery и Celery Beat для управления фоновыми задачами.

Этот модуль инициализирует экземпляр приложения Celery, настраивает брокер сообщений,
бэкенд для хранения результатов и определяет расписание (Beat) для периодического
сбора цен с биржи.

Переменные окружения:
    CELERY_BROKER_URL (str): URL для подключения к брокеру (например, Redis или RabbitMQ).
    CELERY_RESULT_BACKEND (str): URL бэкенда для хранения состояний задач.
"""

import os
from celery import Celery

# from celery.schedules import crontab

celery_app = Celery(
    "deribit_tasks",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)

celery_app.conf.update(
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "app.tasks.fetch_and_store_prices",
        "schedule": 60.0,  # crontab(minute="*")
        "kwargs": {"tickers": ["btc_usd", "eth_usd"]},
    },
}

from app import tasks
