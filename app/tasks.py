from app.celery_app import celery_app
from app.services import save_price
from app.derbit import get_index_price, get_time
from app.config import settings


@celery_app.task
def fetch_and_store_prices():
    """
    Фоновая задача для получения и сохранения текущих цен.

    Задача последовательно обращается к API Deribit для получения актуальных
    индексных цен и текущего серверного времени, после чего
    записывает полученные данные в базу данных.

    Returns:
        str: Статус завершения задачи ("Prices stored").

    Note:
        Задача использует список валют из settings.tickers. Обычно настраивается
        как периодическая (Celery Beat). В случае сбоя API Deribit или ошибки БД,
        задача сгенерирует исключение, которое будет зафиксировано в логах воркера.

    Example:
        >>> fetch_and_store_prices.delay()
    """
    for ticker in settings.tickers:
        price = get_index_price(ticker)
        time = get_time()
        save_price(ticker, price, time)

    return "Prices stored"
