#!/bin/bash

echo "Запуск форматирования кода..."

echo "Black форматирование..."
python3 -m black .

echo "Сортировка импортов..."
python3 -m isort .

echo "Проверка стиля..."
python3 -m flake8 .

echo "Проверка типов..."
python3 -m mypy .

echo "Форматирование завершено!"