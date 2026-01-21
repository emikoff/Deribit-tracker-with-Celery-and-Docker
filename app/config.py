import os


class Settings:
    """
    Класс для управления конфигурацией приложения.

    Инкапсулирует параметры подключения к базе данных и настройки
    бизнес-логики, считывая их из переменных окружения. Предоставляет
    значения по умолчанию для удобства локальной разработки.
    """

    # Параметры подключения к PostgreSQL
    POSTGRES_DB = os.getenv("POSTGRES_DB", "deribit")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

    @property
    def tickers(self) -> list[str]:
        """
        Преобразует строку тикеров из переменной окружения TICKERS в список.

        Returns:
            list[str]: Список тикеров (например, ['btc_usd', 'eth_usd']).
        """
        raw_tickers = os.getenv("TICKERS", "btc_usd, eth_usd")
        return [t.strip() for t in raw_tickers.split(",") if t.strip()]


settings = Settings()
