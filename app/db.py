import time
from app.config import settings
import psycopg2


def get_db_connection(retries: int = 10, delay: int = 2):
    """
    Устанавливает соединение с базой данных PostgreSQL с механизмом повторных попыток.

    Функция считывает параметры подключения из переменных окружения и пытается
    установить связь. Если база данных временно недоступна (например, при запуске
    в Docker-контейнерах), функция ожидает указанное время и повторяет попытку.

    Args:
        retries (int): Максимальное количество попыток подключения. По умолчанию 10.
        delay (int): Задержка в секундах между попытками. По умолчанию 2.

    Returns:
        psycopg2.extensions.connection: Объект активного соединения с базой данных.

    Raises:
        psycopg2.OperationalError: Если после всех попыток не удалось подключиться к БД.
        KeyError: Если отсутствуют необходимые переменные окружения.

    Example:
        >>> conn = get_db_connection(retries=5, delay=1)
        >>> cursor = conn.cursor()
    """
    for attempt in range(retries):
        try:
            return psycopg2.connect(
                dbname=settings.POSTGRES_DB,
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
                host=settings.POSTGRES_HOST,
                port=settings.POSTGRES_PORT,
            )
        except psycopg2.OperationalError:
            if attempt == retries - 1:
                raise
            time.sleep(delay)
