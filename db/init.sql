CREATE TABLE IF NOT EXISTS index_prices (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL,
    price NUMERIC NOT NULL,
    timestamp_ms BIGINT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_index_prices_ticker
    ON index_prices (ticker);

CREATE INDEX IF NOT EXISTS idx_index_prices_timestamp
    ON index_prices (timestamp_ms);
