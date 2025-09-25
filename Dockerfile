# === Stage 1: Build dependencies ===
FROM python:3.10-slim as builder

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости в отдельный слой
RUN pip install --no-cache-dir --user -r requirements.txt

# === Stage 2: Runtime ===
FROM python:3.10-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем установленные пакеты из builder
COPY --from=builder /root/.local /root/.local

# Копируем только нужный код (остальное игнорируется через .dockerignore)
COPY . .

# Убедимся, что PATH включает установленные пакеты
ENV PATH=/root/.local/bin:$PATH

# Создаём непривилегированного пользователя
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
WORKDIR /home/appuser/app

# Копируем проект в домашнюю директорию пользователя
COPY --from=0 --chown=appuser:appuser /app /home/appuser/app

# Указываем команду запуска
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]