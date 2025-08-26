#!/bin/bash

set -e  # Прекратить выполнение при любой ошибке

# Очищаем предыдущие результаты
echo "=== Очистка старых отчётов ==="
rm -rf ./allure-results/* ./allure-report/ || true

# Запускаем тесты
echo "=== Запуск тестов ==="
pytest tests/ -v --alluredir=./allure-results || {
    echo "Тесты упали!";
    exit 1;
}

# Генерируем отчёт
echo "=== Генерация отчёта ==="
allure generate ./allure-results -o ./allure-report --clean

echo "=== Готово! Отчёт сохранён в allure-report/ ==="

# Открываем отчёт в браузере (опционально)
if command -v allure &>/dev/null; then
    allure open ./allure-report
else
    echo "Allure не установлен, отчёт не открыт"
fi