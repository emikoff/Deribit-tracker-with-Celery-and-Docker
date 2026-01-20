import requests


def get_index_price(symbol: str) -> float:
    """
    Запрашивает текущую цену индекса через API Deribit.

    Args:
        symbol (str): Имя индекса (например, 'btc_usd').

    Returns:
        float: Текущая цена индекса.

    Raises:
        requests.exceptions.HTTPError: Если API вернуло ошибку.
    """
    url = "https://www.deribit.com/api/v2/public/get_index_price"
    resp = requests.get(url, params={"index_name": symbol}, timeout=10)
    resp.raise_for_status()
    return resp.json()["result"]["index_price"]


def get_time() -> int:
    """
    Получает текущее серверное время Deribit.

    Returns:
        int: Текущее время в миллисекундах.

    Raises:
        requests.exceptions.HTTPError: Если запрос к API завершился неудачей.
    """
    url = "https://www.deribit.com/api/v2/public/get_time"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()["result"]
