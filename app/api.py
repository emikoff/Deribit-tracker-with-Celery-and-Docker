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
        ticker (str): Символ торговой пары.

    Returns:
        List[Dict]: Список всех записей о ценах из базы данных.

    Raises:
        HTTPException: 404 ошибка, если данных по тикеру не найдено.
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
        ticker (str): Символ торговой пары.

    Returns:
        Dict: Последняя запись цены с временной меткой.

    Raises:
        HTTPException: 404 ошибка, если тикер не найден в БД.
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
        ticker (str): Символ торговой пары.
        from_ts (int): Начальный таймстамп.
        to_ts (int): Конечный таймстамп.

    Returns:
        List[Dict]: Список цен, отсортированный по времени.

    Raises:
        HTTPException: 400 ошибка при некорректном интервале времени.
        HTTPException: 404 ошибка, если за этот период нет данных.
    """
    if from_ts > to_ts:
        raise HTTPException(status_code=400, detail="Invalid date range")

    data = fetch_prices_by_date(ticker, from_ts, to_ts)
    if not data:
        raise HTTPException(status_code=404, detail="No data found")

    return data
