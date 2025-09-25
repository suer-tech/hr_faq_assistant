#!/bin/bash

echo "Запускаем PostgreSQL..."
docker-compose up -d postgres

echo "Ждём 10 секунд..."
sleep 10

echo "Векторизуем документы..."
python scripts/ingest.py

echo "Запускаем API..."
python scripts/run_api.py