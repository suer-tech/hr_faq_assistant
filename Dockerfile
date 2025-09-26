FROM python:3.10-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    postgresql-client \
    tesseract-ocr \
    libtesseract-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаём непривилегированного пользователя
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Указываем команду запуска
CMD ["bash", "-c", "python scripts/setup_db.py && python scripts/ingest.py && python scripts/run_api.py"]