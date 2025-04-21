# Sprint_7
Финальный проект 7 спринта. Тестирование API Яндекс Самокат

## 📌 Содержание
1. [Структура проекта](#-структура-проекта)
2. [Установка](#-установка)
3. [Запуск тестов](#-запуск-тестов)
4. [Отчеты](#-отчеты)
5. [Технологии](#-технологии)

---

## 📂 Структура проекта

```tree
Sprint_7/
├── api/
│   ├── __init__.py
│   ├── courier_api.py
│   └── order_api.py
├── data/
│   ├── __init__.py
│   └── test_data.py
├── tests/
│   ├── __init__.py
│   ├── test_courier.py
│   ├── test_order.py
│   └── test_additional.py
├── conftest.py
├── requirements.txt
├── README.md
└── run_tests.sh
```

## ⚙️ Установка

1. **Клонировать репозиторий**:
   ```bash
   git clone https://github.com/QA-FS-17/Sprint_7.git
   cd Sprint_7

2. **Установить зависимости**:
   ```bash
   pip install -r requirements.txt

3. **Установить Allure (для отчетов)**:
   ```bash
    brew install allure # Linux/macOS
   
    scoop install allure # Windows

## 🚀 Запуск тестов
1. **Запуск всех тестов с генерацией отчетов Allure**:
   ```bash
   ./run_tests.sh  # Для Linux/macOS

2. **Или вручную**:
   ```bash
    pytest --alluredir=allure_results
   
    allure serve allure_results
   
## 📊 Отчеты
**Отчеты генерируются в формате Allure. После запуска тестов**:    

    allure serve allure_results  # Просмотр в браузере

**Или для статического отчета**:

    allure generate allure_results -o allure_report --clean

## 🛠 Технологии
```tree
Python 3.9+

Pytest (тестовый фреймворк)

Selenium WebDriver (автоматизация браузера)

Allure (отчеты)

```