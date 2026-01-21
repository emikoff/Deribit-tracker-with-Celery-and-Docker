import requests


def get_index_data(symbol: str) -> float:
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

    data = resp.json()

    result = {
        "price": data["result"]["index_price"],
        "timestamp": data["usOut"],
    }

    return result
