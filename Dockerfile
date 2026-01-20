FROM python:3.13-slim

# Установка рабочей директории внутри контейнера
WORKDIR /app

# системные зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY . .

# Отключаем буферизацию логов для корректного отображения в Docker logs
ENV PYTHONUNBUFFERED=1

# Команда по умолчанию (может быть переопределена в docker-compose)
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
