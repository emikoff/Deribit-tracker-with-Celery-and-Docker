from typing import List, Dict
from fastapi import FastAPI, Query, HTTPException

from app.services import (
    fetch_prices_by_ticker,
    fetch_latest_price,
    fetch_prices_by_date,
)

app = FastAPI(title="Deribit Price API")


@app.get("/prices", response_model=List[Dict])
def get_prices(ticker: str = Query(...)):
    """
    Получает полную историю цен для указанного тикера.

    Args:
        \n\tticker (str): Символ торговой пары (btc_usd или eth_usd).

    Returns:
        \n\tList[Dict]: Список всех записей о ценах из базы данных.

    Raises:
        \n\tHTTPException: 404 ошибка, если данных по тикеру не найдено.
    """
    data = fetch_prices_by_ticker(ticker)
    if not data:
        raise HTTPException(status_code=404, detail="No data found")
    return data


@app.get("/prices/latest")
def get_latest_price(ticker: str = Query(...)):
    """
    Получает самую свежую (последнюю) цену для указанного тикера.

    Args:
        \n\tticker (str): Символ торговой пары (btc_usd или eth_usd).

    Returns:
        \n\tDict: Последняя запись цены с временной меткой.

    Raises:
        \n\tHTTPException: 404 ошибка, если тикер не найден в БД.
    """
    data = fetch_latest_price(ticker)
    if data is None:
        raise HTTPException(status_code=404, detail="No data found")
    return data


@app.get("/prices/by-date", response_model=List[Dict])
def get_prices_by_date(
    ticker: str = Query(...),
    from_ts: int = Query(...),
    to_ts: int = Query(...),
):
    """
    Получает историю цен в заданном временном диапазоне.

    Args:
        \n\tticker (str): Символ торговой пары (btc_usd или eth_usd).
        \n\tfrom_ts (int): Начальный таймстамп (1767225600000000 - 01.01.2026).
        \n\tto_ts (int): Конечный таймстамп (1798761599000000 - 31.12.2026).

    Returns:
        \n\tList[Dict]: Список цен, отсортированный по времени.

    Raises:
        \n\tHTTPException: 400 ошибка при некорректном интервале времени.
        \n\tHTTPException: 404 ошибка, если за этот период нет данных.
    """
    if from_ts > to_ts:
        raise HTTPException(status_code=400, detail="Invalid date range")

    data = fetch_prices_by_date(ticker, from_ts, to_ts)
    if not data:
        raise HTTPException(status_code=404, detail="No data found")

    return data
