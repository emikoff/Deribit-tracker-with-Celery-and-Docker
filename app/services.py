from typing import List, Dict, Optional
from app.db import get_db_connection


def execute_query(
    query: str, params: tuple = (), fetch: str = "all", commit: bool = False
):
    """
    Выполняет SQL-запрос к базе данных, управляя жизненным циклом соединения.

    Использует контекстные менеджеры для автоматического закрытия курсора и соединения.
    Поддерживает выборку данных (all/one) и фиксацию изменений (commit).

    Args:
        query (str): SQL-запрос с плейсхолдерами (например, %s).
        params (tuple, optional): Параметры для подстановки в запрос. По умолчанию ().
        fetch (str, optional): Режим получения данных:
            'all' - возвращает все найденные строки (List[Tuple]);
            'one' - возвращает только первую строку (Tuple);
            Любое другое значение или commit=True вернет None.
            По умолчанию 'all'.
        commit (bool, optional): Если True, выполняет conn.commit() после запроса.
            Используется для INSERT, UPDATE, DELETE. По умолчанию False.

    Returns:
        Union[List[Tuple], Tuple, None]:
            - Список кортежей, если fetch='all';
            - Один кортеж, если fetch='one';
            - None, если ничего не найдено, произошел коммит или fetch не задан.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)

            if commit:
                conn.commit()
                return None

            if fetch == "all":
                return cur.fetchall()
            elif fetch == "one":
                return cur.fetchone()
    return None


def fetch_prices_by_ticker(ticker: str) -> List[Dict]:
    """
    Извлекает историю цен из базы данных для конкретного тикера.

    Args:
        ticker (str): Символ актива (например, 'btc_usd').

    Returns:
        List[Dict]: Список словарей с ключами 'ticker', 'price', 'timestamp_ms',
            отсортированный по времени по возрастанию.
    """

    query = """
            SELECT ticker, price, timestamp_ms
            FROM index_prices
            WHERE ticker = %s
            ORDER BY timestamp_ms
            """
    params = (ticker,)

    rows = execute_query(query, params)

    return [{"ticker": r[0], "price": r[1], "timestamp_ms": r[2]} for r in rows]


def fetch_latest_price(ticker: str) -> Optional[Dict]:
    """
    Получает последнюю доступную цену для указанного тикера из БД.

    Args:
        ticker (str): Символ актива.

    Returns:
        Optional[Dict]: Словарь с данными о цене или None, если данных нет.
    """

    query = """
            SELECT ticker, price, timestamp_ms
            FROM index_prices
            WHERE ticker = %s
            ORDER BY timestamp_ms DESC
            LIMIT 1
            """
    params = (ticker,)

    row = execute_query(query, params, fetch="one")

    if row is None:
        return None

    return {"ticker": row[0], "price": row[1], "timestamp_ms": row[2]}


def fetch_prices_by_date(ticker: str, from_ts: int, to_ts: int) -> List[Dict]:
    """
    Извлекает цены за определенный временной интервал.

    Args:
        ticker (str): Символ актива.
        from_ts (int): Начало интервала (timestamp в мс).
        to_ts (int): Конец интервала (timestamp в мс).

    Returns:
        List[Dict]: Список цен, попавших в диапазон [from_ts, to_ts].
    """

    query = """
    SELECT ticker, price, timestamp_ms
    FROM index_prices
    WHERE ticker = %s
    AND timestamp_ms BETWEEN %s AND %s
    ORDER BY timestamp_ms
    """
    params = (ticker, from_ts, to_ts)

    rows = execute_query(query, params)

    return [{"ticker": r[0], "price": r[1], "timestamp_ms": r[2]} for r in rows]


def save_price(ticker: str, price: float, timestamp_ms: int) -> None:
    """
    Сохраняет новую запись о цене в базу данных.

    Args:
        ticker (str): Символ актива.
        price (float): Значение цены.
        timestamp_ms (int): Время фиксации цены в миллисекундах.
    """

    query = """
        INSERT INTO index_prices (ticker, price, timestamp_ms)
        VALUES (%s, %s, %s)
        """
    params = (ticker, price, timestamp_ms)

    execute_query(query, params, commit=True)
